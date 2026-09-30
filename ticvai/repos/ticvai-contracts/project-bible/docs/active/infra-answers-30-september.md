# Infrastructure answers: Qdrant, PostgreSQL extensions, the broker, the network and the cost sheet

> **Date:** 30 September 2026 · **For:** Chinmay and the engineers · **Instead of:** waiting for Dinesh on
> ADR-0049 action 4 and ADR-0057 action 3
> **Read first:** `handoff/hld-lld/TICVAI-HLD.md`, `TICVAI-LLD.md`, the cost workbook, ADR-0049, 0056, 0057, 0058,
> `repos/ticvai-infra/terraform/modules/cell/main.tf`
> **Prices:** Azure Retail Prices API (`prices.azure.com`), region `uaenorth`, pay-as-you-go, pulled 30 September
> 2026, 730 hours a month. Vendor prices are list prices from the vendors' own pages on the same day.
> **Status: applied 30 September 2026 (Chinmay approved).** Folded in: Azure Managed Redis instead of Azure Cache
> for Redis (Terraform, HLD/LLD, workbook, ADR-0032 amendment, AI design table); the workbook corrections
> (Defender, Front Door vs bandwidth, broker disks, Redis re-priced, price date and source stated; HA $7,860 →
> $8,048, non-HA $4,325 → $4,532, pre-prod $1,506 → $1,536); the network (CNI Overlay with a subnet per pool
> and AI and data pools, `userAssignedNATGateway`, NSGs at the edges only with the Postgres HA and Storage
> rules, a Gateway API ingress instead of NGINX, GatewaySubnet 10.20.27.0/27, `snet-agc` and `snet-jump`
> reserved; the Terraform cell module now builds this plan in `network.tf`); ADR-0049 amendment (self-hosted
> Qdrant, HS256 key as a Key Vault secret, planned rotation, snapshot CronJob to Blob; action 4 closed);
> ADR-0057 amendment (UAE North broker options and prices; action 3 closed); pgvector removed from
> `handoff/schema.md` and `contracts/satellite/ai.yaml`. **Not applied:** `pg_stat_statements` in
> `001-extensions.sql`, PG17, the `PgVectorStore` fallback in `ticvai-ai`, the pgvector text of
> `docs/architecture/ai-system-design.md`, and one production HA mode for PostgreSQL (left as an LLD open point).

## The four answers in brief

1. **Qdrant:** self-host open-source Qdrant on our own AKS with the official Helm chart. Collection-scoped JWT
   works there (open source since 1.9). Managed Cloud in UAE North could not be confirmed. Hybrid Cloud keeps
   the data in our cluster, but it needs an Enterprise contract and sends metadata to `cloud.qdrant.io`.
2. **PostgreSQL extensions:** the package uses `ltree`, `btree_gist` and `pgcrypto`. The Terraform allow-list
   also has `pg_stat_statements`. All four are supported on PG16 in Azure. None needs a change to
   `shared_preload_libraries`, because `pg_stat_statements` is preloaded on every server. Nothing is
   unsupported. PG16, 17 and 18 are all available, and UAE North has zone-redundant HA.
3. **Broker:** Azure has no first-party RabbitMQ. If the client picks RabbitMQ, use **CloudAMQP in UAE North**
   (a 3-node cluster at $297–597 a month, plus $99 for private connectivity) or the RabbitMQ Cluster Operator
   on our AKS (about $320 a month plus our time). If the client picks Kafka, use **Event Hubs Standard with the
   Kafka endpoint** (about $60–130 a month) if we can live with at most 10 topics per namespace. Otherwise
   Premium costs about $1,070 a month. Confluent Cloud serves UAE North, but a private-network cluster starts
   at about $1,300 a month.
4. **Network and cost:** the address ranges don't overlap, and every subnet meets Azure's minimum size. What
   is wrong is how the parts are wired:
   - The Terraform builds flat Azure CNI in one subnet, not the LLD's four pool subnets.
   - AKS egress does not go through the NAT Gateway.
   - The subnet-to-subnet NSG rules would break the cluster.
   - The NGINX ingress is being retired.
   - There is no GatewaySubnet for the site-to-site VPN.

   Most cost lines are within 15% of retail. The exceptions:
   - **Redis:** Azure Cache for Redis is being retired, and new customers can no longer create it from
     1 October 2026.
   - **Defender:** about 3–4 times too low.
   - **Front Door and bandwidth:** the traffic is booked in the wrong line.
   - **Broker disks:** missing.

---

## 1. Qdrant hosting in UAE North

### Answer

| | (a) Self-host on our AKS | (b) Qdrant Hybrid Cloud on our AKS | (c) Qdrant Managed Cloud |
|---|---|---|---|
| Where the data lives | Our AKS in UAE North, on our Azure disks | Our AKS in UAE North; "all user data will stay securely within your environment" | Qdrant's own cloud account. **Whether an Azure UAE North region is offered could not be confirmed** (no public region list) |
| What leaves the UAE | Nothing | The cloud agent opens an outbound connection to `cloud.qdrant.io:443`. It sends metrics, cluster metadata and "database configuration and collection information", and no points or payloads. Our collection names contain tenant ids (`t_<tenantId>_bge-m3-v1`), so tenant ids leave the country | Everything, unless a UAE region exists |
| Collection-scoped JWT (ADR-0049) | **Yes.** Set `service.api_key` and `service.jwt_rbac: true`; available since v1.9.0 | Not stated on the pages read. The operator runs the same engine, so it very likely works, but confirm with Qdrant before signing | Yes: "Granular access API key authentication is enabled by default" |
| Licence and cost | Apache 2.0, no licence fee. The VMs and disks are already in the sheet: about $800 a month for 3 × E4s v5 plus 3 × P15 | **Enterprise plan only; price on request** ("Talk to our engineers") | Usage-based (vCPU, memory, storage); no list prices on the pricing page |
| Operations | Ours: upgrades, rebalancing, backups and monitoring. The plain Helm chart does not give zero-downtime upgrades, automatic shard rebalancing or cluster backup | Qdrant's operator does upgrades and rebalancing; we run the cluster | Qdrant does it all |

**Qdrant also sells "Private Cloud"**, its Enterprise Operator on our Kubernetes with no connection to Qdrant
at all. It fixes the metadata problem of Hybrid Cloud, and its price is also on request.

### Details the engineers need

- **The JWT is signed with the admin API key itself (HS256).** Our token issuer holds `service.api_key` and
  mints each tenant's token, putting `{"access":[{"collection":"t_<id>_bge-m3-v1","access":"r"}]}` and `exp`
  in the claims. Three things follow:
  - **Key Vault holds it as a *secret*, not an HSM key.** Key Vault keys cannot do HMAC signing. The LLD's line
    "signed with a key in Key Vault" and the workbook's "Premium (HSM-backed keys) … Qdrant JWT signing keys"
    are therefore wrong about the mechanism.
  - **Rotating the API key breaks every tenant's token at once.** Qdrant says so: tokens are not migrated when
    the admin key rotates. Rotation has to be a planned event: new key, reissue every token, rolling restart.
  - **Only the issuer may see the API key**, never `ticvai-ai`. That is what ADR-0049 already says.
- **Aliases:** ADR-0049 has the retrieval client read the alias `tenant_<id>`. The docs I read do not say
  whether a token scoped to the collection also works through its alias. Test this on day one. The `access`
  claim is a list, so the token can name both the collection and the alias.
- **Version:** pin 1.16 or later, because ADR-0049's reasoning assumes that payload-filter RBAC is gone
  (deprecated in 1.15, removed in 1.16).
- **Snapshots to Blob:** Qdrant's snapshot storage supports only `local` and `s3`. **Azure Blob is not a
  native target.** Take snapshots to local disk and copy them to the UAE storage account with a CronJob
  (azcopy with workload identity). Or put an S3-compatible gateway in front of Blob. Azure Disk snapshots are a
  second line, not a replacement: Qdrant's own snapshot is the consistent one.
- **TLS is required.** Qdrant warns that sending an API key over plain HTTP is insecure. Enable TLS on the
  service or use a mesh.
- **Sizing check:** 20,000 chunks × 1,024 dimensions × 4 bytes is about 80 MB of dense vectors per tenant.
  Add sparse vectors and the HNSW index and it is roughly 0.2 GB. At 200 tenants with replication factor 2
  that is under 100 GB of RAM-and-disk working set across three 32 GB nodes, which fits. The disks
  (256 GB each) are comfortable.

### Recommendation

**Choose (a): self-hosted open-source Qdrant, official Helm chart, 3 nodes, replication factor 2, one per
zone.** It is the only option that meets the residency condition without an argument about metadata. It
needs no contract, and JWT RBAC is documented for it. Use (b) or Private Cloud only if running Qdrant proves
too much for the team, and only after compliance accepts the metadata flow (Hybrid) or the price (Private
Cloud). Rule out (c) until Qdrant shows us, in writing, a UAE North region
(`qcloud cloud-region list --cloud-provider azure`).

### What changes

- **ADR-0049:** close action 4 with "self-hosted chosen; Hybrid Cloud needs Enterprise and sends collection
  metadata to cloud.qdrant.io". Add four notes: the key is HS256 and signed with the API key, rotation reissues
  every token, aliases need a test, and snapshots go to Blob by copy because Blob is not native.
- **LLD, Security:** "readable only with that tenant's collection-scoped JWT, signed with the Qdrant API key
  held as a Key Vault secret by the token issuer". Remove the "Open points" bullet about Qdrant.
- **Workbook, Key Vault line:** the HSM justification should not mention Qdrant.
- **SETUP-QDRANT ticket:** add TLS, the snapshot CronJob to Blob, and a check that alias access works with a
  collection-scoped token.

### Sources (read 30 September 2026)

- Qdrant security, JWT RBAC (v1.9.0, HS256, api_key, `exp`, cloud default, rotation note): https://qdrant.tech/documentation/security/
- Qdrant Hybrid Cloud (operator, cloud agent, telemetry, Enterprise only): https://qdrant.tech/documentation/hybrid-cloud/ and https://qdrant.tech/hybrid-cloud
- Qdrant pricing (Hybrid: talk to engineers; Standard: usage-based, AWS/Azure/GCP): https://qdrant.tech/pricing/
- Qdrant Cloud cluster creation (no region list): https://qdrant.tech/documentation/cloud/create-cluster/ ; Azure launch post, 17 January 2024, lists no regions: https://qdrant.tech/blog/qdrant-cloud-on-microsoft-azure/
- Snapshot storage `local` or `s3` only: https://qdrant.tech/documentation/guides/configuration/
- Helm chart and its limits; Private Cloud: https://qdrant.tech/documentation/installation/
- Payload-filter RBAC removed in 1.16: ADR-0049 and https://oneuptime.com/blog/post/2026-08-28-qdrant-jwt-rbac-tenant-isolation-payload-filters/view (secondary source)

---

## 2. PostgreSQL 16 extensions on Azure Flexible Server

### What the package uses

| Extension | Where | Used for |
|---|---|---|
| `ltree` | `backend/control/001-extensions.sql`, `backend/tenant/001-extensions.sql`; `scope_path` on nearly every table; GiST indexes in `910-indexes.sql` | Scope tree and the RLS predicate |
| `btree_gist` | same files | Mixed GiST indexes |
| `pgcrypto` | same files | **Created but not called.** No `digest`, `crypt`, `pgp_*` or `gen_random_bytes` anywhere in `backend/`, and `gen_random_uuid()` is core since PG13. Harmless to keep |
| `pg_stat_statements` | Terraform `azure.extensions` only | Query monitoring. No migration runs `CREATE EXTENSION` for it |
| `vector` (pgvector) | **Not used.** Terraform excludes it on purpose (ADR-0049). Still named in `handoff/schema.md:52` and `contracts/satellite/ai.yaml:47`, and `repos/ticvai-ai/.../vector_store.py` keeps a `PgVectorStore` fallback | Stale references |

Nothing uses `pg_partman`, `pg_cron`, `citext`, `pg_trgm`, `uuid-ossp`, `postgis` or `pgaudit`. ADR-0056's
monthly partitions are made by a kernel job, not by `pg_partman`.

### Azure support (PG16 column of Microsoft's extension list, page dated 10 July 2026)

| Extension | PG16 version | Allow-list (`azure.extensions`) | `shared_preload_libraries` |
|---|---|---|---|
| `ltree` | 1.2 | Yes | No |
| `btree_gist` | 1.7 | Yes | No |
| `pgcrypto` | 1.3 | Yes | No. On Azure Linux 3.0, OpenSSL 3 "legacy" ciphers and digests (Blowfish-CBC, CAST, DES, RC4, MD4, RIPEMD-160 and others) are not available. We call none of them |
| `pg_stat_statements` | 1.10 | Yes | **Already preloaded on every server**; only allow-list plus `CREATE EXTENSION` are needed |
| *for reference:* `vector` | 0.8.2 | Yes | No |
| *for reference:* `pg_cron`, `pg_partman` | 1.6, 5.4.3 | Yes | **Yes** (a restart is needed). `pg_cron` runs from one database, which fits badly with a database per tenant. Keep the kernel job |

**Nothing the package uses is unsupported.** The Terraform allow-list
`LTREE,BTREE_GIST,PGCRYPTO,PG_STAT_STATEMENTS` is correct and complete.

### Versions and region

- Azure supports PG **16 (16.15), 17 (17.11) and 18 (18.6)**. The versions page is dated 26 August 2026. All
  four of our extensions exist on 17 and 18 too.
- **UAE North** is listed with Intel v3/v4/v5 compute, **zone-redundant HA**, same-zone HA and geo-redundant
  backup. **UAE Central** is marked access-restricted (support request needed) and has no zone-redundant HA,
  but it has geo-redundant backup. UAE North's geo-backup pair is therefore in the same country. Setting
  `geo_redundant_backup_enabled = true` is compatible with residency once access to UAE Central is granted.
- The Terraform sets `high_availability.mode = "SameZone"` for the shared tier and `ZoneRedundant` only for
  dedicated and isolated tiers. The LLD promises zone-redundant for production. Decide which one is true.
- Azure also has a **built-in PgBouncer** (port 6432). It is an alternative to running pgbouncer ourselves.

### Recommendation

- **Keep the three extensions and the allow-list as they are.** Add `CREATE EXTENSION IF NOT EXISTS
  pg_stat_statements;` to `backend/control/001-extensions.sql`; otherwise the allow-list entry does nothing.
- **Consider PG17 before the first migration.** It gets a year more community support than 16, supports all
  our extensions, and has native failover of logical replication slots, which helps the venue-promotion path
  in `cells-and-tenancy.md`. PG18 would give a native `uuidv7()`, but ADR-0056 generates ids in the
  application anyway, and 18 is the newest release on Azure. This is Chinmay's call. Nothing forces a change.
- **Remove the pgvector leftovers** so no one provisions against them.

### What changes

- `handoff/schema.md:52`: extensions are `ltree`, `btree_gist`, `pgcrypto`, `pg_stat_statements` (no `vector`).
- `contracts/satellite/ai.yaml:47`: rewrite the pgvector paragraph to match ADR-0049 (Qdrant, a collection per
  tenant).
- `ticvai-ai` `PgVectorStore`: delete it, or mark it dev-only.
- HLD/LLD: "PostgreSQL 16" becomes "PostgreSQL 16 (17 possible; decide before MIG-BASELINE)", if Chinmay wants
  that option open. State one HA mode for production.

### Sources (read 30 September 2026)

- Extension versions by PG version, with preload markers (page date 10 July 2026): https://learn.microsoft.com/en-us/azure/postgresql/extensions/concepts-extensions-versions
- Extension considerations: `pg_stat_statements` preloaded, pgcrypto and OpenSSL 3, pg_cron (page date 12 August 2026): https://learn.microsoft.com/en-us/azure/postgresql/extensions/concepts-extensions-considerations
- Supported versions (page date 26 August 2026): https://learn.microsoft.com/en-us/azure/postgresql/configure-maintain/concepts-supported-versions
- Region table, UAE North and UAE Central (updated 5 September 2026): https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/overview

---

## 3. The broker in UAE North

### Answer

**Azure has no first-party RabbitMQ.** There is no RabbitMQ (or Kafka-branded) product in the Azure Retail
Prices catalogue. Microsoft's own RabbitMQ page is about *bridging* RabbitMQ to Service Bus. Service Bus
speaks AMQP 1.0, not RabbitMQ's AMQP 0-9-1, and ADR-0057 rules it out.

#### If the client picks RabbitMQ

| Option | UAE North | Small production price | Notes |
|---|---|---|---|
| **CloudAMQP (dedicated)** | **Yes.** UAE North has been in their Azure region list since 21 October 2019 | 3-node **Big Bunny $297/month** or **Happy Hare $597/month**, plus **$99/month** for VPC peering or PrivateLink. Same price on Azure and AWS | Managed by 84codes. Confirm with them in writing that backups, definitions and logs stay in UAE North. Their control plane is outside the UAE |
| **RabbitMQ Cluster Operator on our AKS** | Yes (our cluster) | 3 × D2s v5 ($258) + 3 × P10 disks ($65) ≈ **$320/month**, plus our time | Operator and Messaging Topology Operator are MPL 2.0 and use the official RabbitMQ image. **Do not use the Bitnami chart.** Bitnami moved its images behind a paid subscription on 29 September 2025, and the free ones are frozen as `bitnamilegacy` |
| Azure Service Bus | Yes | Standard $10/month + operations; Premium 1 MU ≈ $715/month | Not RabbitMQ. Ruled out (ADR-0057) |

#### If the client picks Kafka

| Option | UAE North | Small production price | Notes |
|---|---|---|---|
| **Event Hubs Standard + Kafka endpoint** | Standard, Premium and Dedicated are all priced in `uaenorth` | 2 TUs × $0.0396/h ≈ **$58/month**, plus ingress events at $0.037 per million (a few dollars at our volume). The price list also has a "Standard Kafka Endpoint" meter at $0.09/h (≈ $66/month); I could not confirm whether Microsoft bills it on top. **Budget $60–130/month** | Kafka is supported from Standard up. Private Link is available on Standard. **Limit: 10 event hubs (topics) per namespace** and 7 days' retention. With 69 events plus dead-letter topics, that forces a few coarse topics (for example one per deployable) or a second namespace |
| Event Hubs Premium | Priced in `uaenorth` ($1.469/PU-hour) | 1 PU ≈ **$1,072/month** | 100 event hubs per PU, 90 days' retention, resource isolation |
| **Confluent Cloud on Azure** | **Yes**, `uaenorth` for Basic, Standard, Enterprise and Dedicated. **UAE Central is not listed** | Standard ≈ $0.75/eCKU-hour ≈ **$550/month** but public endpoints only. **Enterprise (private networking) ≈ $1.75–2.25/eCKU-hour ≈ $1,280–1,640/month**, plus $0.02–0.05/GB throughput and $0.08/GB-month storage | A second vendor contract. Public endpoints conflict with the LLD's "no public endpoints", so in practice this means Enterprise |

### Recommendation

- **RabbitMQ (still our recommendation to the client): CloudAMQP, 3-node Big Bunny or Happy Hare, with
  PrivateLink, in UAE North: about $400–700 a month.** It meets the ADR's "managed, if one exists there". It
  costs about the same as running it ourselves once our time is counted, and nobody on the team has run
  RabbitMQ. The fallback is the RabbitMQ Cluster Operator on the data pool (the sheet's current assumption).
  Get the residency answer from 84codes before signing.
- **Kafka: Event Hubs Standard with the Kafka endpoint**, if the topic design fits in 10 event hubs.
  Otherwise use Premium (about $1,070). Confluent only if the client already has a Confluent contract.

### What changes

- **ADR-0057:** close action 3 with the table above. Add under Kafka: "Event Hubs Standard allows 10 topics
  per namespace; design topics per deployable, not per event."
- **Workbook broker line:** see section 4. The self-hosted line lacks disks. If CloudAMQP is chosen, replace
  the three D2s v5 ($264) with $396–696.
- **LLD:** Open points, broker. A managed broker also removes the broker from `snet-aks-data` and adds a
  private endpoint in `snet-private-endpoints`.

### Sources (read 30 September 2026)

- Azure Retail Prices API, `uaenorth` (Event Hubs, Service Bus meters; no RabbitMQ product): https://prices.azure.com/api/retail/prices
- Microsoft, integrating Service Bus with RabbitMQ: https://learn.microsoft.com/azure/service-bus-messaging/service-bus-integrate-with-rabbitmq
- CloudAMQP Azure regions incl. UAE North (21 October 2019): https://www.cloudamqp.com/blog/new-azure-regions-added.html ; plans and 3-node prices: https://www.cloudamqp.com/plans.html
- RabbitMQ Kubernetes operators (MPL 2.0): https://www.rabbitmq.com/kubernetes/operator/operator-overview
- Bitnami image change (29 September 2025): https://www.docker.com/blog/broadcoms-new-bitnami-restrictions-migrate-easily-with-docker/
- Event Hubs tiers, Kafka and quotas (page date 25 August 2026): https://learn.microsoft.com/en-us/azure/event-hubs/compare-tiers
- Confluent Cloud regions (uaenorth yes, uaecentral no): https://docs.confluent.io/cloud/current/clusters/regions.html ; pricing: https://www.confluent.io/confluent-cloud/pricing/

---

## 4. The VNet 10.20.0.0/16 and the cost workbook

### 4a. The address plan

**Overlaps:** none. The ranges are 0.0/24, 4.0/22, 8.0/21, 16.0/22, 20.0/23, 24.0/24, 25.0/24 and 26.0/26,
all within 10.20.0.0/16. The AKS service range 10.100.0.0/16 is outside the VNet. Free space: 10.20.1.0–3.255,
22.0–23.255, and 26.64 upwards.

**Azure minimums are met:**
- `AzureBastionSubnet` is /26 (the required minimum).
- The PostgreSQL delegated subnet is /24; the minimum is /28, and one HA server uses 4 addresses.
  /24 is right, because **a delegated subnet cannot grow once a server is in it**.

**Problems, in order of how much they matter:**

1. **The Terraform does not build the LLD's network.** `main.tf` sets `network_plugin = "azure"` with no
   `network_plugin_mode`. That is **flat Azure CNI (node-subnet mode)**, in which every pod takes a VNet
   address. It also puts the system pool and the workload pool in **one** subnet (`var.compute_subnet_id`) and
   has **no AI pool and no data pool**.
   - In flat mode each node reserves max-pods + 1 addresses. The workload pool at 20 nodes (+1 surge) needs
     651 addresses at the default of 30 pods, which fits in /21. At 110 pods it needs 2,331, which does not fit
     in /21 (2,043 usable).
   - **Recommendation: Azure CNI Overlay** (`network_plugin_mode = "overlay"`, which is also AKS's default when
     no plugin is named). Give each pool its own `vnet_subnet_id`, and set the pod range explicitly, for example
     `pod_cidr = 10.244.0.0/16`. With overlay, node subnets only need node addresses. The /22 and /21 are then
     generous, and pods never consume VNet space.
   - The pod range must not overlap the VNet, the service range, any peered VNet, the client's ranges or any
     **venue LAN reached over site-to-site VPN**. Venue LANs are often 10.x. If in doubt, use 100.64.0.0/16.
   - Check also that `network_policy = "cilium"` is paired with `network_data_plane = "cilium"`. The azurerm
     4.x provider expects the two together.
2. **Egress does not go through the NAT Gateway.** The cluster has no `outbound_type`, so AKS uses its own
   load-balancer public IP. The payment and e-invoicing allow-list would then see a different address from the
   one the LLD promises. Set `outbound_type = "userAssignedNATGateway"` and attach the NAT Gateway to every
   node subnet.
3. **The NSG rules between node subnets would break the cluster.** The LLD's "workload: inbound from
   snet-ingress only" and "AI: inbound from ingress and workload" conflict with how AKS works:
   - Ingress-controller pods run on the system pool. Traffic from them to workload pods comes from
     `snet-aks-system`, not from `snet-ingress`.
   - metrics-server and CoreDNS on the system pool must reach every node.

   **Keep NSGs at the edges** (Postgres, private endpoints, Bastion, ingress). **Enforce the east-west rules
   (workload → data, AI → Qdrant) with Cilium network policies**, which are already chosen.
4. **Postgres NSG:** besides 5432 from the AKS subnets, allow **5432 inside `snet-postgres`** (HA replication)
   and **outbound to the `Storage` service tag** (WAL archive). Otherwise zone-redundant HA fails. If the
   built-in PgBouncer is used, open 6432.
5. **The ingress controller is being retired.** The upstream ingress-nginx project stopped maintenance in March
   2026. Microsoft supports the App Routing add-on's NGINX only **through November 2026**, and its direction
   is Gateway API: an Istio-based ingress in the App Routing add-on, or Application Gateway for Containers.
   The LLD's "NGINX ingress behind an internal load balancer" should become a Gateway API ingress. If
   Application Gateway for Containers is chosen, it needs its own delegated subnet; reserve 10.20.2.0/24.
6. **The system pool is tainted.** `only_critical_addons_enabled = true` means the LLD's "ingress in the system
   pool" will not schedule without tolerations. Either give the ingress its own small pool or add the
   toleration.
7. **Nothing is reserved for the site-to-site VPN** that the LLD offers dedicated-tier venues. Reserve
   `GatewaySubnet` 10.20.27.0/27.
8. **Administrator access to the AKS API:** the LLD does not say whether the API server is private. If it is,
   Bastion *Basic* cannot tunnel `kubectl`. That needs Bastion Standard ($212/month), or a small jump VM behind
   Basic. Decide, and add a subnet for the jump VM (for example 10.20.28.0/27) if needed.
9. **Front Door is global, not "UAE North".** It stores nothing, but it decrypts requests at the edge location
   nearest the user. For UAE users that is normally a UAE location, but this is not guaranteed. Tell compliance
   it is data in transit only, and keep the WAF logs in the UAE North Log Analytics workspace.

**Proposed plan (changes in bold):**

| Subnet | Range | Change |
|---|---|---|
| snet-ingress | 10.20.0.0/24 | Private Link service needs `privateLinkServiceNetworkPolicies` disabled |
| **snet-agc** (only if Application Gateway for Containers) | **10.20.2.0/24** | New, delegated |
| snet-aks-system | 10.20.4.0/22 | Own `vnet_subnet_id` in Terraform |
| snet-aks-workload | 10.20.8.0/21 | Own `vnet_subnet_id` |
| snet-aks-ai | 10.20.16.0/22 | New node pool in Terraform |
| snet-aks-data | 10.20.20.0/23 | New node pool in Terraform (taint for Qdrant and the broker) |
| snet-postgres | 10.20.24.0/24 | NSG rules above |
| snet-private-endpoints | 10.20.25.0/24 | Private DNS zones for Redis, Key Vault, Blob, ACR (and Event Hubs or CloudAMQP if chosen) |
| AzureBastionSubnet | 10.20.26.0/26 | - |
| **GatewaySubnet** | **10.20.27.0/27** | New, reserved for venue VPN |
| **snet-jump** (if private API server) | **10.20.28.0/27** | New |
| **Pod range (overlay)** | **10.244.0.0/16** (or 100.64.0.0/16) | New; not in the VNet |
| AKS services | 10.100.0.0/16 | - |

### 4b. The cost workbook against retail prices (UAE North, 30 September 2026)

**Within about 15%, no change needed.** Computed from retail at 730 hours:

| Line | Sheet | Retail |
|---|---|---|
| AKS Standard tier | $73 | $73.00 |
| D4s v5 | $175 | $171.55 |
| D8s v5 | $350 | $343.83 |
| D2s v5 | $88 | $86.14 |
| E4s v5 | $225 | $226.30 |
| E2s v5 + P10 | $132 | $134.65 |
| P15 disk | $38 | $41.47 (9% low) |
| PG GP D4ds v5 | $320 | $316.82 |
| PG storage 256 GB | $36 | $35.33 ($0.138/GB) |
| Read replica D4ds v5 + 256 GB | $356 | $352.15 |
| D2ds v5 + 256 GB | $196 | $193.74 |
| D2ds v5 + 512 GB | $230 | $229.07 |
| AI log D4ds v5 + 1 TB | $460 | $458.13 |
| NAT Gateway, 730 h + 1 TB | $80 | $79.93 (+$3.65 for its public IP) |
| Bastion Basic | $139 | $138.70 |
| Container Registry Standard | $20 | $20.27 |
| Private Link, 6 endpoints + DNS zones | $50 | ≈ $47 |
| Blob Hot LRS 2 TB | $45 | $41.52 + transactions |
| Blob Hot ZRS 2 TB | $60 | $51.90 + transactions |
| Log Analytics 60 / 40 / 20 GB | $200 / $140 / $70 | $3.29/GB after 5 GB free per billing account: $181–197 / $115–132 / $49–66 |
| Key Vault Standard | $5 | fine |

**Lines off by more than 15%, or wrong for another reason:**

| Sheet and line | Now | Corrected | Why |
|---|---|---|---|
| **HA, Redis Premium P2 (13 GB)** | $1,000 | Retail is $1,069 (P2 two-node, $1.465/h), but **re-price as Azure Managed Redis Balanced B10 (12 GB): $329–658** | **Azure Cache for Redis (Basic, Standard and Premium) retires on 30 September 2028. Creating new caches is blocked for new customers from 1 October 2026**, per Microsoft's "what's new" page. Sources disagree on when existing customers are blocked. Do not start a new platform on it. Managed Redis is zone-redundant by default. The B10 meter is $0.45045/h per instance ($329/month). The pricing page shows separate one-node and two-node (HA) columns, whose amounts did not load, so budget **$658** for HA until confirmed |
| **Non-HA, Redis Standard C4 (13 GB)** | $400 | $506 at retail (+26%); **re-price as Managed Redis B10: $329 (one node)** | Same retirement. The C4 two-node price is $0.693/h |
| **Pre-prod, Redis Standard C1** | $125 | $133 at retail; **re-price as Managed Redis B1: about $133, or B0: about $53** | Same retirement |
| **HA, Microsoft Defender for Cloud** | $150 | **≈ $575** | "Servers, containers and databases": Defender for Containers is $0.00941 per vCore-hour. 70 vCores (3×4 + 3×8 + 2×8 + 3×4 + 3×2) cost $481. Defender for PostgreSQL is $15 per server-month × 5 = $75. Defender for Storage is about $10 per account. With Defender for Servers P1 instead of Containers the nodes cost $4.91 each (14 nodes ≈ $69), so about $165 in total. Pick the plan, then price it |
| **Non-HA, Defender** | $100 | **≈ $316** | 38 vCores ($261) + 3 PostgreSQL servers ($45) + storage ($10) |
| **Front Door Premium (both sheets)** | $450 | **≈ $650** | Base $330. Edge-to-client traffic is in zone 7 (Middle East and Africa) at $0.11/GB, so 2 TB is $225. Requests at $0.0168 per 10,000: 50 million a month is $84 (an assumption, not a measurement). Edge-to-origin is about $0.06/GB. The sheet's 2 TB belongs here |
| **Bandwidth (both sheets)** | $180 | **≈ $20** | Traffic from an Azure origin to Front Door is free. What is left is egress through the NAT Gateway to providers: the first 100 GB free, then $0.181/GB. Together with the Front Door line, the pair goes from $630 to about $670 (+6%). The total barely moves, but the traffic is booked in the wrong line |
| **Broker (HA)** | $264 (VMs only) | **$329** | Missing 3 × P10 disks ($21.50 each). Quorum queues and Kafka logs need persistent disks. If CloudAMQP: $396–696 |
| **Broker (non-HA and pre-prod)** | $88 | **$110** | One P10 disk missing |
| **Key Vault Premium (HA)** | $10 | $10 now; **+$1.32 per tenant per month** if each tenant has an HSM key (about $264 at 200 tenants) | Scales with tenants. The Qdrant signing key is a secret and does not need Premium (section 1) |
| **Bastion** | $139 (Basic) | $139, or **$212 for Standard** | Only if the AKS API is private and we want `kubectl` through Bastion (4a, item 8) |
| Pre-prod Blob 500 GB | $15 | $10 | Small; leave it |
| "Region" column on Front Door | UAE North | Global | Label only |

**Effect on the totals** (RabbitMQ self-hosted, Managed Redis HA at $658, Defender for Containers):
- The HA production month goes from **$7,860 to about $8,050** (+2%).
- The non-HA production month goes from **$4,325 to about $4,530** (+5%).
- The totals are sound. Some lines inside them are wrong, and the Redis line points at a product we should not
  buy.

### What changes

- **LLD, Network:**
  - CNI Overlay and the pod range.
  - One subnet per pool.
  - Egress through the NAT Gateway (`userAssignedNATGateway`).
  - NSGs at the edges, Cilium policy east-west.
  - The Postgres intra-subnet and Storage rules.
  - GatewaySubnet (and the jump subnet, or Bastion Standard).
  - Gateway API ingress instead of NGINX.
- **LLD, Tiers and Private endpoints:** "Redis Premium (13 GB)" becomes "Azure Managed Redis B10 (12 GB),
  zone-redundant". **HLD, Data stores:** say the same.
- **Terraform cell module:**
  - `network_plugin_mode = "overlay"`, `pod_cidr`, `outbound_type`.
  - Per-pool subnets; the AI and data pools.
  - Replace `azurerm_redis_cache` (retiring; `capacity = 1` also means P1 at 6 GB, not the LLD's 13 GB) with
    `azurerm_managed_redis`.
  - A single HA mode for production.
  - This is infrastructure code in `repos/ticvai-infra`, so it needs its own ticket.
- **Workbook:** the Redis lines (both sheets and pre-prod), Defender, Front Door and Bandwidth (move the
  traffic), broker disks. Add a note that Key Vault scales with tenants.
- **ADR-0032 (Redis):** add a line: "Azure Managed Redis, not Azure Cache for Redis (retiring 30 September
  2028; creation blocked for new customers from 1 October 2026)."

### Sources (read 30 September 2026)

- Azure Retail Prices API, `armRegionName eq 'uaenorth'`: Virtual Machines, Azure Database for PostgreSQL, Redis Cache, Azure Managed Redis, Azure Kubernetes Service, Azure Bastion, Key Vault, Container Registry, Storage, Bandwidth, Log Analytics, Microsoft Defender for Cloud, Event Hubs, Service Bus. NAT Gateway, Private Link, Private DNS and Front Door are global meters. https://prices.azure.com/api/retail/prices
- Front Door pricing model (origin to Front Door free; Premium base $330) (page date 25 September 2025): https://learn.microsoft.com/en-us/azure/frontdoor/understanding-pricing ; zone 7 is Middle East and Africa: https://azure.microsoft.com/en-us/pricing/details/frontdoor/
- Azure Cache for Redis retirement FAQ (retirement 30 September 2028; updated 18 August 2026): https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/retirement-faq ; creation-block dates: https://docs.azure.cn/en-us/azure-cache-for-redis/cache-whats-new (states 1 October 2026 for new customers, and has conflicting text for existing customers)
- Azure Managed Redis tiers and HA (page date 28 May 2026): https://learn.microsoft.com/en-us/azure/redis/overview ; pricing columns: https://azure.microsoft.com/en-us/pricing/details/managed-redis/
- Azure CNI Overlay (default mode, pod CIDR 10.244.0.0/16, per-pool subnets) (page date 31 July 2026): https://learn.microsoft.com/en-us/azure/aks/azure-cni-overlay
- PostgreSQL private access: /28 minimum, 4 addresses per HA server, subnet cannot grow, NSG 5432 and Storage (page date 13 July 2026): https://learn.microsoft.com/en-us/azure/postgresql/network/concepts-networking-private
- Ingress-NGINX and the AKS App Routing add-on (support through November 2026) (13 November 2025): https://blog.aks.azure.com/2025/11/13/ingress-nginx-update

---

## Not confirmed: please check before relying on it

- Whether Qdrant Managed Cloud offers Azure UAE North. Ask Qdrant, or run `qcloud cloud-region list`.
- Whether Hybrid Cloud clusters expose `jwt_rbac`, and the Hybrid and Private Cloud prices. Ask Qdrant sales.
- Whether a collection-scoped JWT works through an alias. Test it.
- Whether Event Hubs bills the "Standard Kafka Endpoint" meter on top of throughput units.
- Whether the Azure Managed Redis HA price is one or two instance meters.
- Whether CloudAMQP keeps backups, definitions and logs inside UAE North.
- When existing Azure customers can no longer create Azure Cache for Redis. Microsoft's pages disagree.
