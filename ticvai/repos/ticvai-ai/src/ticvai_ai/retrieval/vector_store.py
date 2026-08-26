"""Vector store abstraction.

Two implementations exist deliberately. Qdrant was proposed on 12 Aug 2026,
pending confirmation of UAE data residency with the Dubai Compliance Authority
(CF-20). Writing against this interface with a pgvector fallback costs about two
days and removes a hard dependency on an external ruling — if Qdrant fails
residency, the decision becomes a config change rather than a rewrite.

Tenant isolation here is partition-level, never filter-level. A forgotten filter
in a query builder is a cross-client data breach; a missing collection is a
loud failure. This distinction is the single most important thing in this module.
"""

from __future__ import annotations

import abc
import logging
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol, Sequence
from uuid import UUID

logger = logging.getLogger(__name__)


class DistanceMetric(StrEnum):
    COSINE = "cosine"
    DOT = "dot"
    EUCLIDEAN = "euclidean"


@dataclass(frozen=True, slots=True)
class TenantScope:
    """Identifies the isolation boundary for every operation.

    ``jurisdiction`` is carried because a cell never spans jurisdictions
    (Project Direction §3.3.1) and the vector store must not either.
    """

    tenant_id: UUID
    jurisdiction: str

    def collection_name(self, namespace: str) -> str:
        """Physical collection for this tenant and namespace.

        Isolation is achieved by *separate collections*, not by adding a
        ``tenant_id`` filter to a shared collection. There is no query path that
        can accidentally span tenants because there is no shared collection to
        span.
        """
        if not namespace or not namespace.replace("_", "").isalnum():
            raise ValueError(f"Namespace must be alphanumeric with underscores, got {namespace!r}")

        return f"t_{self.tenant_id.hex}__{namespace}"


@dataclass(slots=True)
class Document:
    id: str
    content: str
    embedding: Sequence[float]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SearchHit:
    id: str
    content: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)


class EmbeddingProvider(Protocol):
    """Kept separate from the store so the embedding model can be swapped
    without touching persistence, and so a residency-constrained deployment can
    use a local model with a remote store or vice versa."""

    async def embed(self, texts: Sequence[str]) -> list[list[float]]: ...

    @property
    def dimensions(self) -> int: ...


class VectorStore(abc.ABC):
    """Storage-agnostic interface. Capability code depends on this, never on a
    concrete driver."""

    @abc.abstractmethod
    async def ensure_collection(
        self,
        scope: TenantScope,
        namespace: str,
        dimensions: int,
        metric: DistanceMetric = DistanceMetric.COSINE,
    ) -> None:
        """Idempotently create the tenant's collection."""

    @abc.abstractmethod
    async def upsert(
        self,
        scope: TenantScope,
        namespace: str,
        documents: Sequence[Document],
    ) -> int:
        """Insert or replace documents. Returns the count written."""

    @abc.abstractmethod
    async def search(
        self,
        scope: TenantScope,
        namespace: str,
        query_embedding: Sequence[float],
        limit: int = 10,
        score_threshold: float | None = None,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[SearchHit]:
        """Nearest neighbours within one tenant's collection.

        ``metadata_filter`` narrows *within* a tenant — venue, language, product
        category. It is never the mechanism for tenant isolation.
        """

    @abc.abstractmethod
    async def delete(
        self,
        scope: TenantScope,
        namespace: str,
        ids: Sequence[str],
    ) -> int:
        """Delete by id. Used by DSAR erasure fan-out."""

    @abc.abstractmethod
    async def drop_collection(self, scope: TenantScope, namespace: str) -> None:
        """Remove a tenant's collection entirely. Used on offboarding."""

    @abc.abstractmethod
    async def health(self) -> bool: ...


class QdrantVectorStore(VectorStore):
    """Qdrant implementation.

    Deployment must sit in-jurisdiction alongside the cell it serves. A shared
    global Qdrant cluster would violate the residency position in §3.3.10 even
    though the vectors are derived data.
    """

    def __init__(self, client: Any, *, on_disk_payload: bool = True) -> None:
        self._client = client
        self._on_disk_payload = on_disk_payload

    async def ensure_collection(
        self,
        scope: TenantScope,
        namespace: str,
        dimensions: int,
        metric: DistanceMetric = DistanceMetric.COSINE,
    ) -> None:
        from qdrant_client.models import Distance, VectorParams

        name = scope.collection_name(namespace)

        if await self._client.collection_exists(name):
            return

        await self._client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(
                size=dimensions,
                distance={
                    DistanceMetric.COSINE: Distance.COSINE,
                    DistanceMetric.DOT: Distance.DOT,
                    DistanceMetric.EUCLIDEAN: Distance.EUCLID,
                }[metric],
                on_disk=self._on_disk_payload,
            ),
        )
        logger.info("Created Qdrant collection %s for tenant %s", name, scope.tenant_id)

    async def upsert(
        self,
        scope: TenantScope,
        namespace: str,
        documents: Sequence[Document],
    ) -> int:
        from qdrant_client.models import PointStruct

        if not documents:
            return 0

        points = [
            PointStruct(
                id=doc.id,
                vector=list(doc.embedding),
                payload={"content": doc.content, **doc.metadata},
            )
            for doc in documents
        ]

        await self._client.upsert(
            collection_name=scope.collection_name(namespace),
            points=points,
            wait=True,
        )
        return len(points)

    async def search(
        self,
        scope: TenantScope,
        namespace: str,
        query_embedding: Sequence[float],
        limit: int = 10,
        score_threshold: float | None = None,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[SearchHit]:
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        query_filter = None
        if metadata_filter:
            query_filter = Filter(
                must=[
                    FieldCondition(key=key, match=MatchValue(value=value))
                    for key, value in metadata_filter.items()
                ]
            )

        results = await self._client.search(
            collection_name=scope.collection_name(namespace),
            query_vector=list(query_embedding),
            limit=limit,
            score_threshold=score_threshold,
            query_filter=query_filter,
            with_payload=True,
        )

        return [
            SearchHit(
                id=str(point.id),
                content=(point.payload or {}).get("content", ""),
                score=point.score,
                metadata={k: v for k, v in (point.payload or {}).items() if k != "content"},
            )
            for point in results
        ]

    async def delete(self, scope: TenantScope, namespace: str, ids: Sequence[str]) -> int:
        from qdrant_client.models import PointIdsList

        if not ids:
            return 0

        await self._client.delete(
            collection_name=scope.collection_name(namespace),
            points_selector=PointIdsList(points=list(ids)),
            wait=True,
        )
        return len(ids)

    async def drop_collection(self, scope: TenantScope, namespace: str) -> None:
        name = scope.collection_name(namespace)
        await self._client.delete_collection(collection_name=name)
        logger.warning("Dropped Qdrant collection %s", name)

    async def health(self) -> bool:
        try:
            await self._client.get_collections()
            return True
        except Exception:
            logger.exception("Qdrant health check failed")
            return False


class PgVectorStore(VectorStore):
    """pgvector fallback.

    Lower ceiling than Qdrant at scale, but it inherits the cell's existing
    residency posture, backup regime and connection pooling — which is exactly
    why it is the safe default until CF-20 resolves. Each tenant gets its own
    table rather than a shared table with a tenant column, preserving the
    partition-not-filter isolation rule.
    """

    def __init__(self, pool: Any, schema: str = "ai") -> None:
        self._pool = pool
        self._schema = schema

    def _table(self, scope: TenantScope, namespace: str) -> str:
        return f'"{self._schema}"."{scope.collection_name(namespace)}"'

    async def ensure_collection(
        self,
        scope: TenantScope,
        namespace: str,
        dimensions: int,
        metric: DistanceMetric = DistanceMetric.COSINE,
    ) -> None:
        table = self._table(scope, namespace)
        ops = {
            DistanceMetric.COSINE: "vector_cosine_ops",
            DistanceMetric.DOT: "vector_ip_ops",
            DistanceMetric.EUCLIDEAN: "vector_l2_ops",
        }[metric]

        async with self._pool.acquire() as conn:
            await conn.execute(f'CREATE SCHEMA IF NOT EXISTS "{self._schema}"')
            await conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id         text PRIMARY KEY,
                    content    text NOT NULL,
                    embedding  vector({dimensions}) NOT NULL,
                    metadata   jsonb NOT NULL DEFAULT '{{}}'::jsonb,
                    created_at timestamptz NOT NULL DEFAULT now()
                )
                """
            )
            await conn.execute(
                f"""
                CREATE INDEX IF NOT EXISTS
                    {scope.collection_name(namespace)}_embedding_idx
                ON {table} USING hnsw (embedding {ops})
                """
            )
            await conn.execute(
                f"""
                CREATE INDEX IF NOT EXISTS
                    {scope.collection_name(namespace)}_metadata_idx
                ON {table} USING gin (metadata)
                """
            )

        logger.info("Ensured pgvector table %s", table)

    async def upsert(
        self,
        scope: TenantScope,
        namespace: str,
        documents: Sequence[Document],
    ) -> int:
        import json

        if not documents:
            return 0

        table = self._table(scope, namespace)

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                await conn.executemany(
                    f"""
                    INSERT INTO {table} (id, content, embedding, metadata)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (id) DO UPDATE
                        SET content = EXCLUDED.content,
                            embedding = EXCLUDED.embedding,
                            metadata = EXCLUDED.metadata
                    """,
                    [
                        (doc.id, doc.content, list(doc.embedding), json.dumps(doc.metadata))
                        for doc in documents
                    ],
                )

        return len(documents)

    async def search(
        self,
        scope: TenantScope,
        namespace: str,
        query_embedding: Sequence[float],
        limit: int = 10,
        score_threshold: float | None = None,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[SearchHit]:
        import json

        table = self._table(scope, namespace)
        params: list[Any] = [list(query_embedding)]
        where = ""

        if metadata_filter:
            params.append(json.dumps(metadata_filter))
            where = f"WHERE metadata @> ${len(params)}::jsonb"

        params.append(limit)

        sql = f"""
            SELECT id, content, metadata, 1 - (embedding <=> $1::vector) AS score
              FROM {table}
              {where}
             ORDER BY embedding <=> $1::vector
             LIMIT ${len(params)}
        """

        async with self._pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)

        hits = [
            SearchHit(
                id=row["id"],
                content=row["content"],
                score=float(row["score"]),
                metadata=json.loads(row["metadata"]) if isinstance(row["metadata"], str) else row["metadata"],
            )
            for row in rows
        ]

        if score_threshold is not None:
            hits = [hit for hit in hits if hit.score >= score_threshold]

        return hits

    async def delete(self, scope: TenantScope, namespace: str, ids: Sequence[str]) -> int:
        if not ids:
            return 0

        table = self._table(scope, namespace)

        async with self._pool.acquire() as conn:
            result = await conn.execute(f"DELETE FROM {table} WHERE id = ANY($1)", list(ids))

        return int(result.split()[-1]) if result else 0

    async def drop_collection(self, scope: TenantScope, namespace: str) -> None:
        table = self._table(scope, namespace)
        async with self._pool.acquire() as conn:
            await conn.execute(f"DROP TABLE IF EXISTS {table}")
        logger.warning("Dropped pgvector table %s", table)

    async def health(self) -> bool:
        try:
            async with self._pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception:
            logger.exception("pgvector health check failed")
            return False
