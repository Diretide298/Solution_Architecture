# -*- coding: utf-8 -*-
"""Build the HLD and LLD pack: handoff/hld-lld/ and its Claude Design folder.

    python tools/build-hld-lld.py

Writes
    handoff/hld-lld/README.md
    handoff/hld-lld/TICVAI-HLD.md, TICVAI-HLD.svg     classic high-level design (boxes and connection types)
    handoff/hld-lld/TICVAI-LLD.md, TICVAI-LLD.svg     Azure low-level design (region, VNet, tiers, security)
    handoff/hld-lld/TICVAI - Azure Cloud Specs & Cost.xlsx
    handoff/hld-lld/TICVAI-LLD-AWS.md, TICVAI-LLD-AWS.svg    the same cell on AWS me-central-1 (CHG-R3-001)
    handoff/hld-lld/TICVAI - AWS Cloud Specs & Cost.xlsx     the AWS workbook, with an Azure-vs-AWS sheet
    handoff/design-batches/HLD-LLD/BRIEF.md, architecture.json

The format follows the three samples Chinmay supplied on 30 September (a classic HLD, an Azure LLD and a
specs-and-cost workbook with and without high availability). The content comes from the package: the five
deployables and their modules (handoff/service-decomposition.json, ADR-0055), the Terraform cell defaults
(repos/ticvai-infra/terraform/modules/cell), and the decisions of 30 September (ADR-0049 Qdrant one
collection per tenant, UAE hosting only; ADR-0056; ADR-0057 broker is the client's choice; ADR-0058).
Prices are estimates for Azure UAE North and say so; the workbook keeps them in editable cells. Unit prices
were checked against the Azure Retail Prices API (uaenorth, pay as you go, 730 hours) on 30 September 2026, and
the infrastructure answers of that day were folded in: Azure Managed Redis instead of the retiring Azure Cache
for Redis, CNI Overlay with a subnet per pool, egress through the NAT Gateway, NSGs at the edges only, a Gateway
API ingress, a GatewaySubnet (docs/active/infra-answers-30-september.md).

Rechecked 1 October 2026 against the ADRs accepted or amended that day: ADR-0061 replica floors (12 a cell, 13
in a large one) in the text and in the node counts; ADR-0060 with Chinmay's decision that production PostgreSQL
is zone-redundant on every tier (the shared cell included), the SLO per tier still with the client, DR in UAE
Central; the separate qdrant and broker node pools the Terraform builds; the broker recommendation (RabbitMQ on
CloudAMQP, the client's choice by 12 October) and ADR-0058's amendment (drain loop, Relay:BatchSize, republish
from the outbox); the waiting room at the edge (ADR-0066), the one-second browse cache (ADR-0065), per-tenant
request budgets (ADR-0064), one device register (ADR-0067), admission policy in Access (ADR-0068), e-invoicing
through a provider adapter (ADR-0062), encryption and keys (ADR-0063) and the in-park 3D navigation assets
(ADR-0069). The prices are still those of 30 September; the without-HA sheet was recomputed (see NOTES_NO_HA).

`terraform_agrees()` reads the Terraform cell module and stops the build if the pack and the module disagree on
the address plan, the replica floors, the node pools or the PostgreSQL HA mode.
"""
import io
import json
import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "handoff" / "hld-lld"
DESIGN = ROOT / "handoff" / "design-batches" / "HLD-LLD"
TF = ROOT / "repos" / "ticvai-infra" / "terraform" / "modules" / "cell"
DATE = "1 October 2026"  # the pack's date; the prices keep their own date in PRICE_SOURCE
PRICE_SOURCE = ("Azure Retail Prices API (prices.azure.com), region uaenorth, pay as you go, 730 hours a month, "
                "pulled 30 September 2026; vendor prices (CloudAMQP, Confluent) from the vendors' pages the same "
                "day. Working: docs/active/infra-answers-30-september.md, section 4b.")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------------------------------------
# The architecture, once. Both diagrams, both documents and the Claude Design brief read from here.
# ---------------------------------------------------------------------------------------------------------
dec = json.loads((ROOT / "handoff" / "service-decomposition.json").read_text(encoding="utf-8"))
MODULES = {}
for name, svc in dec["services"].items():
    MODULES.setdefault(svc.get("deployable", "?"), []).append(name.replace("Service", ""))
DEPLOYABLES = dec.get("deployables", {})

# Connection types: the sample's legend, plus the two TICVAI needs (events, local network).
LINK = {
    "api":      ("Real-time API call (HTTPS)",              "#F2A900", None),
    "direct":   ("Real-time direct call (database, cache)", "#D62828", None),
    "event":    ("Event through the broker",                "#7B2CBF", None),
    "batch":    ("Batch process",                           "#111111", "8,5"),
    "sync":     ("Near-real-time sync (offline-first)",     "#F2A900", "8,5"),
    "internet": ("Internet (TLS) / VPN",                    "#2F80ED", None),
    "wireless": ("4G / Wi-Fi",                              "#2E9E44", None),
    "lan":      ("Venue local network",                     "#2E9E44", "3,4"),
    "repl":     ("Replication",                             "#D62828", "8,5"),
}

# id: (label, sublabel, x, y, w, h). Columns: stores the deployables use (x=270) with their replicas and
# archives beside them (x=70); deployables (x=540); AI stores and the device API (x=780); front ends (x=1000);
# the outside world (x=1300). Lines between neighbouring columns run in the gaps; longer ones are routed.
HLD_NODES = {
    "replica":   ("Read replicas", "x2, operational reads", 70, 110, 150, 70),
    "blob":      ("Blob storage", "media, 3D maps, dumps", 70, 510, 150, 70),
    "pg":        ("PostgreSQL 16", "zone-redundant; DB per tenant", 270, 110, 180, 70),
    "rpt":       ("Reporting replica", "lag-tolerant, no writes", 270, 210, 180, 70),
    "redis":     ("Redis", "Managed Redis / ElastiCache", 270, 310, 180, 70),
    "broker":    ("Event broker", "RabbitMQ (rec.) or Kafka", 270, 410, 180, 70),
    "workers":   ("workers", "outbox relay, consumers, jobs", 270, 510, 180, 70),
    "commerce":  ("commerce", "sale path", 540, 110, 160, 70),
    "operations":("operations", "back office, engagement", 540, 210, 160, 70),
    "ai":        ("ticvai-ai", "AI engine (Python)", 540, 330, 160, 70),
    "access":    ("access", "gate hot path", 540, 510, 160, 70),
    "waf":       ("Edge + WAF", "Front Door / CloudFront", 780, 60, 170, 60),
    "wroom":     ("Waiting room", "on-sale; admission token", 780, 165, 170, 60),
    "qdrant":    ("Qdrant", "one collection per tenant", 780, 300, 150, 70),
    "llm":       ("Azure OpenAI", "LLM, UAE region", 780, 410, 150, 60),
    "posapi":    ("Device API", "one device register", 780, 600, 160, 70),
    "fe_b2c":    ("Guest web", "B2C front end", 1000, 110, 160, 60),
    "fe_b2b":    ("Partner Portal", "B2B front end", 1000, 210, 160, 60),
    "fe_bo":     ("Back office", "Venue Mgmt, CMS, Console", 1000, 310, 160, 60),
    "pubapi":    ("Public API", "partners' systems, OTAs", 1000, 410, 160, 60),
    "u_b2c":     ("B2C guest", "web and mobile app", 1300, 110, 150, 60),
    "u_b2b":     ("B2B partner", "hotels, agents", 1300, 210, 150, 60),
    "u_ops":     ("Venue operators", "and TICVAI staff", 1300, 310, 150, 60),
    "ext3p":     ("3rd parties", "OTAs, ERP, developers", 1300, 410, 150, 60),
    "pay":       ("Payments", "Stripe, Network Intl.", 1300, 540, 150, 60),
    "einv":      ("E-invoicing", "accredited provider", 1300, 630, 150, 60),
    "msg":       ("Messaging", "email, SMS, WhatsApp, push", 1300, 720, 150, 60),
    "pos":       ("POS", "terminal, tablet", 90, 850, 120, 60),
    "kds":       ("Kitchen display", "stations", 230, 850, 120, 60),
    "kiosk":     ("Kiosks", "self-service", 370, 850, 120, 60),
    "edge":      ("Venue edge node", "access + policy, offline", 560, 800, 170, 70),
    "turn":      ("Turnstiles", "gates, readers", 800, 850, 120, 60),
    "hand":      ("Handhelds", "scanners, staff app", 940, 850, 120, 60),
}
HLD_ZONES = [
    # (label, x, y, w, h, fill, stroke)
    ("TICVAI CLOUD - Azure UAE North or AWS me-central-1 (one cell per region)", 40, 20, 1160, 680, "#FFF3CC", "#333333"),
    ("VENUE SITE (each venue)", 40, 730, 1160, 250, "#DCE6F5", "#333333"),
    ("ONSITE SALES", 70, 780, 440, 180, "#F7CFB5", "#333333"),
    ("ACCESS CONTROL", 780, 780, 300, 180, "#F7CFB5", "#333333"),
]
# (from, to, type or "type+type" for a double line, waypoints)
HLD_LINKS = [
    ("u_b2c", "fe_b2c", "internet", None), ("u_b2b", "fe_b2b", "internet", None),
    ("u_ops", "fe_bo", "internet", None), ("ext3p", "pubapi", "internet", None),
    ("fe_b2c", "waf", "api", None), ("fe_b2b", "waf", "api", None), ("fe_bo", "waf", "api", None),
    ("pubapi", "waf", "api", None),
    ("waf", "commerce", "api", None), ("waf", "operations", "api", None),
    ("waf", "wroom", "api", None), ("wroom", "commerce", "api", None),
    ("commerce", "pg", "direct", None), ("commerce", "redis", "direct", None),
    ("operations", "pg", "direct", None), ("operations", "rpt", "direct", None), ("access", "pg", "direct", None),
    ("pg", "replica", "repl", None), ("pg", "rpt", "repl", None),
    ("commerce", "broker", "event", None), ("operations", "broker", "event", None), ("ai", "broker", "event", None),
    ("workers", "broker", "event", None),
    ("workers", "pg", "direct", [(252, 530), (252, 160)]),
    ("workers", "blob", "batch", None),
    ("ai", "qdrant", "direct", None), ("ai", "llm", "api", None),
    ("commerce", "pay", "api", [(745, 170), (745, 562)]),
    ("workers", "einv", "api", [(350, 686), (1250, 686)]),
    ("workers", "msg", "api", [(372, 693), (1240, 693)]),
    ("pos", "posapi", "internet+sync", [(150, 790)]), ("kiosk", "posapi", "internet+api", [(430, 790)]),
    ("posapi", "commerce", "api", [(760, 600), (760, 185), (700, 170)]),
    ("pos", "kds", "lan", None),
    ("edge", "access", "internet+sync", None),
    ("turn", "edge", "lan", None), ("hand", "edge", "wireless", [(1000, 815)]),
]

# LLD boxes: id: (label, lines, x, y, w, h, fill). The AKS pools are the five the Terraform cell module builds
# (main.tf): system, workload, ai, qdrant, broker; qdrant and broker share snet-aks-data and its taint.
LLD_NODES = {
    "users":   ("Users", ["B2C guests", "B2B partners", "Venue operators"], 30, 330, 150, 110, "#FFFFFF"),
    "fd":      ("Azure Front Door Premium", ["WAF: OWASP + bot rules,", "rate rules per client IP", "on-sale waiting-room page",
                "TLS 1.2+, custom domains", "Private Link to origin"], 220, 310, 190, 140, "#FFFFFF"),
    "ilb":     ("Ingress (internal LB)", ["Gateway API ingress", "(AKS App Routing)", "Private Link service"], 470, 330, 170, 110, "#EEF4FF"),
    "sys":     ("AKS system pool", ["D4s v5, 2-4 nodes, zones 1-3", "+ ingress gateway pods"], 690, 145, 190, 70, "#EEF4FF"),
    "wl":      ("AKS workload pool", ["D8s v5, 3-20 nodes, 3 zones", "floors: commerce 3, access 2,", "operations 2, workers 2"],
                690, 227, 190, 90, "#EEF4FF"),
    "aip":     ("AKS AI GPU pool", ["NV6ads A10 v5 x2, 1 a zone", "tainted; ticvai-ai 2/1/0,", "BGE-M3, reranker, NER"],
                690, 329, 190, 90, "#EEF4FF"),
    "qdrant":  ("AKS qdrant pool", ["E4s v5 x3, one per zone", "Qdrant, replication 2, TLS"], 690, 431, 190, 72, "#EEF4FF"),
    "broker":  ("AKS broker pool", ["D2s v5 x3, while self-run;", "recommended: CloudAMQP", "UAE North, Private Link"],
                690, 515, 190, 90, "#EEF4FF"),
    "pg":      ("PostgreSQL Flexible Server 16", ["GP D4ds v5, zone-redundant HA", "on every production tier", "control DB + DB per tenant",
                "PITR 35 days, UAE only"], 950, 150, 220, 110, "#FFFFFF"),
    "ro":      ("Read replicas x2", ["GP D4ds v5", "gate checks never read here"], 950, 280, 220, 70, "#FFFFFF"),
    "rpt":     ("Reporting + AI log DB", ["reporting replica (D2ds v5)", "AI log DB (D4ds v5, 1 TB)"], 950, 370, 220, 80, "#FFFFFF"),
    "pe":      ("Private endpoints", ["Azure Managed Redis B10 (12 GB)", "Key Vault", "Blob storage (ZRS)", "Container Registry",
                "managed broker, if chosen"], 950, 470, 220, 125, "#FFFFFF"),
    "bastion": ("Azure Bastion", ["admin access only", "no public SSH / RDP"], 470, 560, 170, 80, "#FFFFFF"),
    "nat":     ("NAT Gateway", ["one static egress IP;", "AKS outbound type"], 470, 700, 170, 80, "#FFFFFF"),
    "extp":    ("External providers", ["Payments, e-invoicing", "messaging, Azure OpenAI"], 220, 700, 190, 80, "#FFFFFF"),
    "ops":     ("Operations", ["Azure Monitor + Log Analytics", "Azure Backup, Defender", "Entra ID, subscription"], 30, 560, 180, 100, "#FFFFFF"),
    "dr":      ("UAE Central (DR module)", ["geo-redundant backup; async", "replica for tenants buying DR", "access-restricted, no zone HA"],
                950, 690, 230, 95, "#FFFFFF"),
    "venue":   ("Venue site", ["POS, kiosks, KDS", "venue edge node (offline)", "turnstiles, handhelds on LAN"], 1250, 300, 190, 110, "#FFFFFF"),
    "vpn":     ("Site-to-site VPN", ["dedicated tier, GatewaySubnet;", "others: Internet + mTLS"], 1250, 450, 190, 80, "#FFFFFF"),
}
# Frames a line may start or end on without being a box: (label, x, y, w, h)
LLD_FRAMES = {"aks": ("AKS cluster", 670, 130, 230, 510)}
LLD_LINKS = [
    ("users", "fd", "internet", None), ("fd", "ilb", "api", None),
    ("ilb", "wl", "api", None), ("ilb", "aip", "api", None),
    ("wl", "pg", "direct", None), ("wl", "ro", "direct", None), ("wl", "pe", "direct", None),
    ("aip", "rpt", "direct", None), ("aip", "qdrant", "direct", None),
    ("wl", "broker", "event", [(912, 300), (912, 560)]),
    ("pg", "ro", "repl", None), ("pg", "rpt", "repl", [(1180, 215), (1180, 405)]),
    ("pg", "dr", "repl", [(1195, 185), (1195, 737)]),
    ("aks", "nat", "api", [(785, 740)]), ("nat", "extp", "api", None),
    ("bastion", "sys", "internet", [(660, 600), (660, 180)]),
    ("venue", "fd", "internet", [(1345, 85), (315, 85)]),
    ("venue", "vpn", "internet", None),
    ("vpn", "ilb", "sync", [(1225, 490), (1225, 676), (650, 676), (650, 420)]),
]
SUBNETS = [
    # (name, cidr, holds, rule). Mirrors address_plan in repos/ticvai-infra/terraform/modules/cell/variables.tf
    # (network.tf builds it); change both together. NSGs sit at the edges only; east-west rules between the
    # AKS pools are Cilium network policies, because ingress pods and CoreDNS on the system pool must reach
    # every node and an NSG between node subnets would break the cluster.
    ("snet-ingress", "10.20.0.0/24", "Internal load balancer and Private Link service for Front Door",
     "NSG: no Internet inbound; Private Link service network policies disabled"),
    ("snet-agc", "10.20.2.0/24", "Reserved: Application Gateway for Containers, only if chosen over App Routing",
     "Not created; delegated subnet if used"),
    ("snet-aks-system", "10.20.4.0/22", "AKS system pool, and the ingress gateway pods (they tolerate its taint)",
     "No NSG; egress through the NAT Gateway"),
    ("snet-aks-workload", "10.20.8.0/21", "Workload pool: commerce, access, operations, workers",
     "No NSG; Cilium policy: inbound from the ingress gateway; egress through the NAT Gateway"),
    ("snet-aks-ai", "10.20.16.0/22", "AI GPU pool (the only AI pool): ticvai-ai, BGE-M3 and its reranker, Presidio and "
     "the Arabic NER",
     "No NSG; Cilium policy: inbound from the ingress gateway and the workload pool; read-only role on "
     "transactional schemas (ADR-0020, amended by ADR-0049)"),
    ("snet-aks-data", "10.20.20.0/23", "The qdrant pool (Qdrant cluster) and, while the broker is self-run, the broker "
     "pool; both tainted ticvai.io/pool=data",
     "No NSG; Cilium policy: inbound from the workload and AI pools only; Qdrant needs each tenant's "
     "collection-scoped JWT"),
    ("snet-postgres", "10.20.24.0/24", "PostgreSQL Flexible Server (delegated subnet), replicas, AI log DB",
     "NSG: 5432 (6432 for built-in PgBouncer) from the AKS subnets; all traffic inside the subnet (HA "
     "replication); outbound 443 to the Storage tag (WAL archive); public access disabled"),
    ("snet-private-endpoints", "10.20.25.0/24", "Azure Managed Redis, Key Vault, Blob storage, Container Registry "
     "(and the managed broker's Private Link if one is chosen: CloudAMQP is recommended, ADR-0057)",
     "NSG: inbound from the AKS subnets only; private DNS zones; public access disabled on every resource"),
    ("AzureBastionSubnet", "10.20.26.0/26", "Azure Bastion", "The only administrative path in"),
    ("GatewaySubnet", "10.20.27.0/27", "VPN gateway for dedicated-tier venues' site-to-site VPN",
     "Created empty; the gateway is added when a venue needs it. No NSG (Azure does not support one here)"),
    ("snet-jump", "10.20.28.0/27", "Reserved: a jump VM, only if the AKS API is private and Bastion stays Basic",
     "Not created"),
]
POD_CIDR = "10.244.0.0/16"  # CNI Overlay pod range, outside the VNet (Terraform default, variables.tf)
AKS_SERVICE_CIDR = "10.100.0.0/16"  # Terraform default (modules/cell/variables.tf)
RESERVED_SUBNETS = {"snet-agc", "snet-jump"}  # in the plan, not created (network.tf header)

# Replica floors per deployable (ADR-0061, accepted 1 October 2026): replica_floors in the Terraform cell module,
# x-ticvai-replica-floors in deploy/a- and b-*.yml, DEPLOYABLE_FLOORS in tools/derive-sizing.py.
FLOORS = [
    # (unit, deployable, floor, why)
    ("commerce", "commerce", 3, "One per zone: the sale path survives a zone loss without a cold start"),
    ("access", "access", 2, "Cloud side only; the gate decides locally (ADR-0013)"),
    ("operations", "operations", 2, "Back office tolerates a short scale-out"),
    ("workers", "workers", 2, "Relay leases fail over between replicas (ADR-0058, amended 1 October)"),
    ("ai-realtime", "ticvai-ai", 2, "Fraud scoring and recommendations; fail open. 3 in a large cell (AI design 4.3)"),
    ("ai-interactive", "ticvai-ai", 1, "Assistants tolerate a short outage"),
    ("ai-batch", "ticvai-ai", 0, "Scales from zero on queue depth"),
]
FLOOR_TOTAL = sum(f[2] for f in FLOORS)  # 12; 13 in a large cell

# What the pack says about the cell module; terraform_agrees() checks each against the .tf files.
TF_EXPECT = {
    "vnet_address_space": "10.20.0.0/16", "pod_cidr": POD_CIDR, "service_cidr": AKS_SERVICE_CIDR,
    "database_sku": "GP_Standard_D4ds_v5", "database_storage_mb": "262144", "read_replica_count": "2",
    "enable_reporting_replica": "true", "database_high_availability": "true", "backup_retention_days": "35",
    "geo_redundant_backup_enabled": "false",
    "redis_sku": "Balanced_B10", "redis_high_availability": "true",
    "system_node_size": "Standard_D4s_v5",
    "workload_node_size": "Standard_D8s_v5", "workload_min_nodes": "3", "workload_max_nodes": "20",
    "ai_node_size": "Standard_D8s_v5", "ai_min_nodes": "2", "ai_max_nodes": "4",
    "qdrant_node_size": "Standard_E4s_v5", "qdrant_nodes": "3",
    "broker_self_hosted": "true", "broker_node_size": "Standard_D2s_v5", "broker_nodes": "3",
}
TF_MAIN_MUST = [
    'mode                      = "ZoneRedundant"', 'network_plugin_mode = "overlay"', 'network_policy      = "cilium"',
    'outbound_type       = "userAssignedNATGateway"', 'sku_tier            = "Standard"',
    'name                         = "system"', "min_count                    = 2", "max_count                    = 4",
    'name                  = "workload"', 'name                  = "ai"', 'name                  = "qdrant"',
    'name                  = "broker"', 'value     = "LTREE,BTREE_GIST,PGCRYPTO,PG_STAT_STATEMENTS"',
]


def _tf_block(text, name):
    m = re.search(r'variable "%s" \{\n(.*?)\n\}\n' % re.escape(name), text, re.S)
    if not m:
        raise SystemExit(f"ERROR terraform: variable {name} not found in variables.tf")
    return m.group(1)


def _tf_map(block):
    m = re.search(r"default = \{\n(.*?)\n  \}", block, re.S)
    return {k: v for k, v in re.findall(r'"([^"]+)"\s*=\s*"?([^"\s#]+)"?', m.group(1))} if m else {}


def terraform_agrees():
    """The pack's numbers against the Terraform cell module. Returns a list of disagreements (must be empty)."""
    var = (TF / "variables.tf").read_text(encoding="utf-8")
    main = (TF / "main.tf").read_text(encoding="utf-8")
    bad = []
    for k, want in TF_EXPECT.items():
        m = re.search(r'default\s*=\s*"?([^"\n]+?)"?\s*$', _tf_block(var, k), re.M)
        got = m.group(1).strip() if m else None
        if got != want:
            bad.append(f"{k}: Terraform {got!r}, pack {want!r}")
    plan = _tf_map(_tf_block(var, "address_plan"))
    ours = {n: c for n, c, _, _ in SUBNETS if n not in RESERVED_SUBNETS}
    if plan != ours:
        bad.append(f"address_plan: Terraform {plan}, pack {ours}")
    floors = {k: int(v) for k, v in _tf_map(_tf_block(var, "replica_floors")).items()}
    if floors != {u: f for u, _, f, _ in FLOORS}:
        bad.append(f"replica_floors: Terraform {floors}, pack {[(u, f) for u, _, f, _ in FLOORS]}")
    for must in TF_MAIN_MUST:
        if must not in main:
            bad.append(f"main.tf no longer has: {must}")
    if '"SameZone"' in main:
        bad.append("main.tf sets SameZone HA somewhere; the pack says zone-redundant on every production tier")
    return bad


# ---------------------------------------------------------------------------------------------------------
# SVG
# ---------------------------------------------------------------------------------------------------------
def box3d(x, y, w, h, label, sub=None):
    d = 10  # depth of the 3D face, as in the sample
    s = []
    s.append(f'<polygon points="{x},{y} {x+d},{y-d} {x+w+d},{y-d} {x+w},{y}" fill="#E6E6E6" stroke="#8A8A8A"/>')
    s.append(f'<polygon points="{x+w},{y} {x+w+d},{y-d} {x+w+d},{y+h-d} {x+w},{y+h}" fill="#9E9E9E" stroke="#8A8A8A"/>')
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#g)" stroke="#8A8A8A"/>')
    cy = y + h / 2 - (7 if sub else 0)
    s.append(f'<text x="{x+w/2}" y="{cy+5}" text-anchor="middle" font-size="15" font-weight="600">{esc(label)}</text>')
    if sub:
        s.append(f'<text x="{x+w/2}" y="{cy+23}" text-anchor="middle" font-size="11" fill="#333">{esc(sub)}</text>')
    return "\n".join(s)


def toward(n, pt):
    """Where the line from box n's centre towards pt leaves the box."""
    x, y, w, h = n
    cx, cy = x + w / 2, y + h / 2
    dx, dy = pt[0] - cx, pt[1] - cy
    if dx == 0 and dy == 0:
        return cx, cy
    sx = (w / 2) / abs(dx) if dx else float("inf")
    sy = (h / 2) / abs(dy) if dy else float("inf")
    t = min(sx, sy)
    return cx + dx * t, cy + dy * t


def facing(a, b):
    """Anchors on the edges of a and b that face each other, so a line between neighbours stays in the gap."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    gapx = max(bx - (ax + aw), ax - (bx + bw))
    gapy = max(by - (ay + ah), ay - (by + bh))
    if gapx >= 0:
        x1 = ax + aw if bx > ax else ax
        x2 = bx if bx > ax else bx + bw
        return (x1, ay + ah / 2), (x2, by + bh / 2)
    if gapy >= 0:
        y1 = ay + ah if by > ay else ay
        y2 = by if by > ay else by + bh
        return (ax + aw / 2, y1), (bx + bw / 2, y2)
    return toward(a, (bx + bw / 2, by + bh / 2)), toward(b, (ax + aw / 2, ay + ah / 2))


def route(a, b, via):
    if not via:
        return list(facing(a, b))
    return [toward(a, via[0])] + list(via) + [toward(b, via[-1])]


def polyline(points, kind, off=(0, 0)):
    _, color, dash = LINK[kind]
    da = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{x + off[0]:.0f},{y + off[1]:.0f}" for x, y in points)
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.4"{da}/>'


def draw_link(points, kinds):
    kinds = kinds.split("+")
    if len(kinds) == 1:
        return polyline(points, kinds[0])
    (x1, y1), (x2, y2) = points[0], points[-1]
    off = (0, 2.6) if abs(x2 - x1) >= abs(y2 - y1) else (2.6, 0)
    return "\n".join([polyline(points, kinds[0], (-off[0], -off[1])), polyline(points, kinds[1], off)])


def seg_hits(x1, y1, x2, y2, l, t, r, bt):
    p = [-(x2 - x1), x2 - x1, -(y2 - y1), y2 - y1]
    q = [x1 - l, r - x1, y1 - t, bt - y1]
    u1, u2 = 0.0, 1.0
    for pi, qi in zip(p, q):
        if pi == 0:
            if qi < 0:
                return False
            continue
        u = qi / pi
        if pi < 0:
            u1 = max(u1, u)
        else:
            u2 = min(u2, u)
    return u1 < u2


def crossings(boxes, links):
    """Every line segment that runs through a box other than its own two ends. Must be empty."""
    bad = []
    for a, b, kinds, pts in links:
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            for k, (x, y, w, h) in boxes.items():
                if k in (a, b):
                    continue
                if seg_hits(x1, y1, x2, y2, x + 3, y + 3, x + w - 3, y + h - 3):
                    bad.append(f"{a} -> {b} crosses {k}")
    return sorted(set(bad))


def legend(x, y, kinds):
    h = 50 + 26 * len(kinds)
    s = [f'<rect x="{x}" y="{y}" width="330" height="{h}" fill="#FFFFFF" stroke="#111" stroke-width="2"/>',
         f'<text x="{x+30}" y="{y+34}" font-size="20" font-weight="700">CONNECTIONS</text>']
    for i, k in enumerate(kinds):
        label, color, dash = LINK[k]
        yy = y + 60 + 26 * i
        da = f' stroke-dasharray="{dash}"' if dash else ""
        s.append(f'<line x1="{x+18}" y1="{yy}" x2="{x+78}" y2="{yy}" stroke="{color}" stroke-width="2.4"{da}/>')
        s.append(f'<text x="{x+90}" y="{yy+5}" font-size="13">{esc(label)}</text>')
    return "\n".join(s)


SVG_HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            'font-family="Segoe UI, Arial, sans-serif" fill="#111">\n'
            '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9D9D9"/>'
            '<stop offset="1" stop-color="#BDBDBD"/></linearGradient></defs>\n'
            '<rect width="100%" height="100%" fill="#FFFFFF"/>\n')


CROSS = {}


def hld_svg():
    s = [SVG_HEAD.format(w=1570, h=1150)]
    for label, x, y, w, h, fill, stroke in HLD_ZONES:
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
        big = label.startswith("TICVAI") or label.startswith("VENUE SITE")
        ly = y + 28 if big else y + h - 16
        s.append(f'<text x="{x+14}" y="{ly}" font-size="{20 if big else 18}">{esc(label)}</text>')
    geo = {k: (v[2], v[3], v[4], v[5]) for k, v in HLD_NODES.items()}
    drawn = [(a, b, kind, route(geo[a], geo[b], via)) for a, b, kind, via in HLD_LINKS]
    CROSS["hld"] = crossings(geo, drawn)
    for a, b, kind, pts in drawn:
        s.append(draw_link(pts, kind))
    for k, (label, sub, x, y, w, h) in HLD_NODES.items():
        s.append(box3d(x, y, w, h, label, sub))
    s.append('<text x="1300" y="36" font-size="24" font-weight="700">TICVAI PLATFORM HLD</text>')
    s.append(f'<text x="1300" y="58" font-size="12" fill="#555">{DATE}</text>')
    s.append(legend(1220, 830, ["api", "direct", "event", "batch", "sync", "internet", "wireless", "lan", "repl"]))
    s.append("</svg>\n")
    return "\n".join(s)


def lld_box(x, y, w, h, title, lines, fill):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="#2F6DB5" stroke-width="1.4"/>',
         f'<text x="{x+w/2}" y="{y+22}" text-anchor="middle" font-size="13.5" font-weight="700">{esc(title)}</text>']
    for i, t in enumerate(lines):
        s.append(f'<text x="{x+w/2}" y="{y+42+i*17}" text-anchor="middle" font-size="11.5" fill="#333">{esc(t)}</text>')
    return "\n".join(s)


def _lld_svg(key, nodes, frames, links, title, sub, region, foot, frame_labels):
    s = [SVG_HEAD.format(w=1600, h=820)]
    s.append(f'<text x="30" y="40" font-size="24" font-weight="700">{esc(title)}</text>')
    s.append(f'<text x="30" y="64" font-size="12" fill="#555">{esc(sub)}</text>')
    s.append('<rect x="450" y="100" width="760" height="560" rx="6" fill="#F4FBF4" stroke="#2E9E44" stroke-width="2.4"/>')
    s.append(f'<text x="466" y="126" font-size="16" font-weight="700">{esc(region)}</text>')
    s.append(f'<text x="466" y="654" font-size="11.5" fill="#333">{esc(foot)}</text>')
    for label, x, y, w, h in [(frame_labels[0], 670, 130, 230, 510), (frame_labels[1], 935, 130, 250, 495)]:
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="#6A7FA8" stroke-dasharray="6,4"/>')
        s.append(f'<text x="{x+10}" y="{y+h-8}" font-size="12" fill="#2F4B7C">{esc(label)}</text>')
    geo = {k: (v[2], v[3], v[4], v[5]) for k, v in nodes.items()}
    ends = dict(geo, **{k: v[1:] for k, v in frames.items()})
    drawn = [(a, b, kind, route(ends[a], ends[b], via)) for a, b, kind, via in links]
    CROSS[key] = crossings(geo, drawn)
    for a, b, kind, pts in drawn:
        s.append(draw_link(pts, kind))
    for k, (t, lines, x, y, w, h, fill) in nodes.items():
        if k == "dr" and "OPEN" in t:  # an undecided box is drawn dashed and amber (CHG-R3-001)
            s.append(f'<rect x="{x-4}" y="{y-4}" width="{w+8}" height="{h+8}" rx="10" fill="none" stroke="#D98E04" '
                     'stroke-width="2" stroke-dasharray="7,4"/>')
        s.append(lld_box(x, y, w, h, t, lines, fill))
    s.append(legend(1250, 580, ["internet", "api", "direct", "event", "sync", "repl"]))
    s.append("</svg>\n")
    return "\n".join(s)


def lld_svg():
    return _lld_svg("lld", LLD_NODES, LLD_FRAMES, LLD_LINKS, "TICVAI PLATFORM LLD - Azure",
                    f"{DATE} - production cell, with high availability", 'Region "UAE North" - VNet 10.20.0.0/16',
                    "zones 1-3; every store in the UAE (backups and DR included)", ("AKS cluster (Standard tier)", "Data tier"))


def aws_lld_svg():
    return _lld_svg("lld-aws", AWS_LLD_NODES, AWS_LLD_FRAMES, AWS_LLD_LINKS, "TICVAI PLATFORM LLD - AWS",
                    f"{AWS_DATE} - production cell, with high availability",
                    'Region "me-central-1" (UAE) - VPC 10.20.0.0/16',
                    "AZs a-c; every store in the UAE; DR open (one AWS region in the UAE)", ("EKS cluster", "Data tier"))


# ---------------------------------------------------------------------------------------------------------
# Cost workbook. Unit prices are USD per month (730 hours, Linux, pay as you go) estimated for UAE North;
# every one is an editable cell, and the totals are formulas.
# ---------------------------------------------------------------------------------------------------------
AED = 3.6725
MARGIN = 0.20
# (group, service type, description, specs, qty, unit USD, scaled qty or None = same)
# Node counts carry ADR-0061's floors. Pod sizes are assumptions until tools/bench.py measures them: a .NET
# replica requests about 1 vCPU and 2 GB; an AI pod about 1 vCPU (4 October, CHG-R11-001: it mostly waits on the
# provider's streamed answer). A D8s v5 node leaves about 7 vCPU to pods. The AI pool is a GPU node pool and the only
# AI pool (Chinmay, 4 October: "Naaa dont keep AI CPU node at all"): NV6ads A10 v5, $0.649/h = $473.77 a month,
# carrying the ticvai-ai pods, Presidio, and on the GPU at fp16 BGE-M3, its reranker and the Arabic NER.
PROD_HA = [
    ("Compute (AKS)", "Azure Kubernetes Service", "Control plane, Standard tier",
     "Uptime SLA, zone-redundant control plane", 1, 73, None),
    ("Compute (AKS)", "Virtual Machines (AKS nodes)", "System node pool (and the ingress gateway pods)",
     "D4s v5 (4 vCPU, 16 GB), Linux, autoscale 2-4 across zones 1-3 (Terraform); budgeted at 3, one per zone",
     3, 175, None),
    ("Compute (AKS)", "Virtual Machines (AKS nodes)", "Workload pool: commerce, access, operations, workers",
     "D8s v5 (8 vCPU, 32 GB), Linux, autoscale 3-20 across zones. Carries the replica floors (ADR-0061): "
     "commerce 3 (one per zone), access 2, operations 2, workers 2 = 9 replicas, three to a node at about 1 vCPU "
     "each. Scaled up, 6 nodes hold a large cell's peak of 34 (commerce 17, operations 12, access 3, workers 2)",
     3, 350, 6),
    ("Compute (AKS)", "Virtual Machines (AKS nodes)",
     "AI GPU pool: ticvai-ai, BGE-M3 and its reranker, Presidio and the Arabic NER (CHG-R11-001)",
     "NV6ads A10 v5 (6 vCPU, 55 GB, 1/6 A10 with 4 GB), Linux, tainted, one node per zone. Carries the floors: real-time 2, "
     "interactive 1, batch 0 (about 1 vCPU a pod), Presidio on the CPU, and on the GPU at fp16 BGE-M3 (about "
     "1.1 GB), its reranker (about 1.1 GB) and the Arabic NER (about 0.3 GB); a large cell's third real-time "
     "replica fits. No AI CPU pool and no Presidio pool. Sizing to confirm by the Sprint 2 benchmark; step up to "
     "NV12ads A10 v5 ($947.54) on CPU saturation or GPU memory pressure. AWS me-central-1: g6.2xlarge "
     "($876.31 a node; the AWS workbook, CHG-R3-001)", 2, 473.77, 4),
    ("Vector store", "Virtual Machines (AKS nodes)", "Qdrant cluster, one collection per tenant (ADR-0049)",
     "qdrant node pool: E4s v5 (4 vCPU, 32 GB) x3, one per zone, replication factor 2. Open-source Qdrant 1.16 or "
     "later from the official Helm chart; TLS; collection-scoped JWT per tenant", 3, 225, None),
    ("Vector store", "Managed Disks", "Qdrant storage",
     "Premium SSD P15 256 GB per node. Snapshots per collection go to Blob by a CronJob (azcopy)", 3, 38, None),
    ("Event broker", "Virtual Machines (AKS nodes)",
     "Broker cluster: RabbitMQ recommended, or Kafka (the client's choice, due 12 October; ADR-0057, proposed)",
     "broker node pool: D2s v5 (2 vCPU, 8 GB) x3, zones 1-3, self-run with the RabbitMQ Cluster Operator: the "
     "Terraform default (broker_self_hosted) and the fallback. The recommendation is CloudAMQP in UAE North, "
     "3 nodes with PrivateLink, $396-696: it replaces this line and the disks (+$68 to +$368) and removes this "
     "pool (Defender about $41 less)", 3, 88, None),
    ("Event broker", "Managed Disks", "Broker storage: quorum queues or Kafka logs",
     "Premium SSD P10 128 GB per node", 3, 21.5, None),
    ("Database", "Azure Database for PostgreSQL", "Primary with zone-redundant standby: control DB + DB per tenant",
     "Flexible Server 16, General Purpose D4ds v5 (4 vCore, 16 GB) x2 (primary + standby in another zone). "
     "Zone-redundant on every production tier, the shared cell included (ADR-0060; Chinmay, 1 October). Priced "
     "the same as the same-zone HA the shared tier had before", 2, 320, None),
    ("Database", "Azure Database for PostgreSQL", "Storage, primary and standby",
     "256 GB Premium SSD each; PITR backup 35 days included up to storage size", 2, 36, None),
    ("Database", "Azure Database for PostgreSQL", "Read replicas (operational reads; gate checks never read here)",
     "General Purpose D4ds v5 + 256 GB each", 2, 356, None),
    ("Database", "Azure Database for PostgreSQL", "Reporting replica (lag-tolerant, no writes)",
     "General Purpose D2ds v5 (2 vCore, 8 GB) + 256 GB", 1, 196, None),
    ("Database", "Azure Database for PostgreSQL", "AI log database (decision records, prompts)",
     "General Purpose D4ds v5 + 1 TB. A writable server of its own (ADR-0020, amended by ADR-0049); not yet in "
     "the Terraform cell module", 1, 460, None),
    ("Cache", "Azure Managed Redis",
     "Sessions, idempotency keys, per-tenant request budgets (ADR-0064), waiting-room positions (ADR-0066), "
     "the one-second browse cache (ADR-0065, proposed), AI features",
     "Balanced B10 (12 GB), high availability, zone-redundant, private endpoint. $0.45045/h per instance; "
     "budgeted as two instance meters until the HA price is confirmed. Replaces Azure Cache for Redis "
     "(retiring; no new caches for new customers from 1 October 2026)", 1, 658, None),
    ("Storage", "Storage account (Blob, ZRS)",
     "Media (including venue 3D models and navigation files, ADR-0069), exports, Qdrant snapshots, database dumps",
     "Hot tier, zone-redundant, 2 TB, UAE North only", 1, 60, None),
    ("Storage", "Container Registry", "Images for the five deployables", "Standard", 1, 20, None),
    ("Security", "Key Vault",
     "Secrets (the Qdrant API key and the waiting-room token key, each read only by its issuer), per-tenant keys",
     "Premium: HSM-backed keys that wrap each tenant's data key for field-level encryption (ADR-0063, proposed); "
     "the Terraform sets Premium only on the isolated tier today. Scales with tenants: +$1.32 per tenant per "
     "month for an HSM key (about $264 at 200 tenants)", 1, 10, None),
    ("Network", "Azure Front Door", "Single entry for web, apps and APIs, with WAF; the on-sale waiting-room page",
     "Premium: WAF managed rules, bot protection and rate rules per client IP, Private Link origin; the waiting-room "
     "page is served from its cache (ADR-0066). Base $330 + 2 TB edge-to-client in zone 7 at $0.11/GB ($225) + "
     "about 50 million requests ($84, an assumption) + edge-to-origin", 1, 650, 2),
    ("Network", "NAT Gateway", "One static egress IP for payment, e-invoicing and messaging allow-lists",
     "730 hours, 1 TB processed", 1, 80, None),
    ("Network", "Azure Bastion", "Administrative access only",
     "Basic, 730 hours. Standard ($212) if the AKS API is private and kubectl goes through Bastion", 1, 139, None),
    ("Network", "Private Link", "Private endpoints and private DNS zones", "About 6 endpoints", 1, 50, None),
    ("Network", "Bandwidth", "Egress through the NAT Gateway to providers",
     "First 100 GB free, then $0.181/GB. Azure origin to Front Door is free; the web traffic is in the Front "
     "Door line", 1, 20, 2),
    ("Operations", "Azure Monitor / Log Analytics", "Logs, metrics, alerts, dashboards", "About 60 GB ingested a month", 1, 200, None),
    ("Operations", "Azure Backup", "Snapshots of Qdrant and broker disks", "Daily, 30 days, UAE North", 1, 40, None),
    ("Operations", "Microsoft Defender for Cloud", "Containers, databases and storage",
     "Defender for Containers: 70 vCores x $0.00941/h ($481); Defender for PostgreSQL: 5 servers x $15 ($75); "
     "Defender for Storage: about $10 per account, 2 accounts. Defender for Servers P1 instead of Containers: "
     "about $165 in all. Pick the plan, then re-price", 1, 575, None),
    ("AI (usage)", "Azure OpenAI", "Language model calls (re-billed per token, AI-D02)",
     "Usage-based; not a fixed hosting cost", 1, 0, None),
]
# Without zone-level HA, but PostgreSQL keeps its zone-redundant standby: Chinmay decided on 1 October that
# production PostgreSQL is zone-redundant on every tier (ADR-0060), and the Terraform allows no standby only in
# pre-production. NOTES_NO_HA says what moved that day and why.
PROD_NO_HA = [
    ("Compute (AKS)", "Azure Kubernetes Service", "Control plane, Standard tier", "Uptime SLA", 1, 73, None),
    ("Compute (AKS)", "Virtual Machines (AKS nodes)", "System node pool (and the ingress gateway pods)",
     "D4s v5 (4 vCPU, 16 GB), Linux, one zone", 2, 175, None),
    ("Compute (AKS)", "Virtual Machines (AKS nodes)", "Workload pool: commerce, access, operations, workers",
     "D8s v5 (8 vCPU, 32 GB), Linux, autoscale 2-10. Carries the floors (ADR-0061): 9 replicas on 2 nodes; in "
     "one zone commerce's three replicas cannot be one per zone", 2, 350, 4),
    ("Compute (AKS)", "Virtual Machines (AKS nodes)",
     "AI GPU pool: ticvai-ai, BGE-M3 and its reranker, Presidio and the Arabic NER (CHG-R11-001)",
     "NV6ads A10 v5 (6 vCPU, 55 GB, 1/6 A10 with 4 GB), Linux, tainted, one node. Carries the floors (real-time 2, interactive 1, "
     "about 1 vCPU a pod) beside Presidio and, on the GPU, BGE-M3, its reranker and the Arabic NER. With the node "
     "down the scrubber is down and LLM calls are refused (503 scrubber-unavailable), never sent raw",
     1, 473.77, 2),
    ("Vector store", "Virtual Machines (AKS nodes)", "Qdrant, one collection per tenant (ADR-0049)",
     "E4s v5 (4 vCPU, 32 GB), single node", 1, 225, None),
    ("Vector store", "Managed Disks", "Qdrant storage", "Premium SSD P15 256 GB", 1, 38, None),
    ("Event broker", "Virtual Machines (AKS nodes)",
     "Broker: RabbitMQ recommended, or Kafka (the client's choice, due 12 October; ADR-0057, proposed)",
     "D2s v5 (2 vCPU, 8 GB), single node, self-run", 1, 88, None),
    ("Event broker", "Managed Disks", "Broker storage", "Premium SSD P10 128 GB", 1, 21.5, None),
    ("Database", "Azure Database for PostgreSQL", "Primary with zone-redundant standby: control DB + DB per tenant",
     "Flexible Server 16, General Purpose D4ds v5 (4 vCore, 16 GB) x2 (primary + standby in another zone). The "
     "standby stays on this sheet: production PostgreSQL is zone-redundant on every tier (ADR-0060; Chinmay, "
     "1 October), and database_high_availability is false only for pre-production", 2, 320, None),
    ("Database", "Azure Database for PostgreSQL", "Storage, primary and standby",
     "256 GB Premium SSD each; PITR backup 35 days", 2, 36, None),
    ("Database", "Azure Database for PostgreSQL", "Read replica (operational reads; gate checks never read here)",
     "General Purpose D4ds v5 + 256 GB", 1, 356, None),
    ("Database", "Azure Database for PostgreSQL", "Reporting replica (lag-tolerant, no writes)",
     "General Purpose D2ds v5 (2 vCore, 8 GB) + 256 GB. Reporting never reads an operational replica (ADR-0016; "
     "the Terraform's enable_reporting_replica)", 1, 196, None),
    ("Database", "Azure Database for PostgreSQL", "AI log database",
     "General Purpose D2ds v5 + 512 GB; not yet in the Terraform cell module", 1, 230, None),
    ("Cache", "Azure Managed Redis", "Sessions, idempotency keys, request budgets, waiting-room positions, caches",
     "Balanced B10 (12 GB), one node, no high availability; $0.45045/h. The Terraform keeps "
     "redis_high_availability = false for pre-production: a production cell without it is the client's call "
     "(ADR-0060)", 1, 329, None),
    ("Storage", "Storage account (Blob, LRS)", "Media (including venue 3D models), exports, Qdrant snapshots, database dumps",
     "Hot tier, 2 TB, UAE North only", 1, 45, None),
    ("Storage", "Container Registry", "Images for the five deployables", "Standard", 1, 20, None),
    ("Security", "Key Vault", "Secrets (the Qdrant API key and the waiting-room token key), per-tenant keys",
     "Standard. Premium if ADR-0063's HSM-wrapped tenant keys are accepted (+$1.32 per tenant per month)", 1, 5, None),
    ("Network", "Azure Front Door", "Single entry for web, apps and APIs, with WAF; the on-sale waiting-room page",
     "Premium: WAF managed rules, bot protection and rate rules per client IP. Base $330 + 2 TB edge-to-client in "
     "zone 7 ($225) + about 50 million requests ($84, an assumption) + edge-to-origin", 1, 650, 2),
    ("Network", "NAT Gateway", "One static egress IP for payment, e-invoicing and messaging allow-lists",
     "730 hours, 1 TB processed", 1, 80, None),
    ("Network", "Azure Bastion", "Administrative access only", "Basic, 730 hours", 1, 139, None),
    ("Network", "Private Link", "Private endpoints and private DNS zones",
     "About 6 endpoints. No store has a public endpoint, with or without HA", 1, 50, None),
    ("Network", "Bandwidth", "Egress through the NAT Gateway to providers",
     "First 100 GB free, then $0.181/GB; the web traffic is in the Front Door line", 1, 20, 2),
    ("Operations", "Azure Monitor / Log Analytics", "Logs, metrics, alerts", "About 40 GB ingested a month", 1, 140, None),
    ("Operations", "Microsoft Defender for Cloud", "Containers, databases and storage",
     "Defender for Containers: 46 vCores ($316); PostgreSQL: 4 servers ($60); Storage (about $10)", 1, 386, None),
    ("AI (usage)", "Azure OpenAI", "Language model calls (re-billed per token, AI-D02)", "Usage-based", 1, 0, None),
]
PREPROD = [
    ("Compute (AKS)", "Azure Kubernetes Service", "Control plane", "Free tier", 1, 0, None),
    ("Compute (AKS)", "Virtual Machines (AKS nodes)", "System and workload nodes, all five deployables",
     "D8s v5 (8 vCPU, 32 GB) x2 + D4s v5 x1, Linux. One replica per unit: the ADR-0061 floors are for "
     "production cells", 1, 875, None),
    ("Vector store", "Virtual Machines (AKS nodes)", "Qdrant, single node", "E2s v5 (2 vCPU, 16 GB) + P10 128 GB", 1, 132, None),
    ("Event broker", "Virtual Machines (AKS nodes)", "RabbitMQ, single node, whichever broker production uses",
     "D2s v5 (2 vCPU, 8 GB). With Kafka in production, add an Event Hubs Standard namespace (about $30)", 1, 88, None),
    ("Event broker", "Managed Disks", "Broker storage", "Premium SSD P10 128 GB", 1, 21.5, None),
    ("Database", "Azure Database for PostgreSQL", "Control DB + test tenant DBs + AI log DB",
     "Flexible Server 16, General Purpose D2ds v5 + 256 GB, no standby (database_high_availability = false: "
     "pre-production only), no replicas", 1, 196, None),
    ("Cache", "Azure Managed Redis", "Test cache", "Balanced B1 (1 GB), one node (B0, about $53, if enough)", 1, 133, None),
    ("Storage", "Storage account (Blob, LRS)", "Test media and snapshots", "Hot tier, 500 GB", 1, 15, None),
    ("Security", "Key Vault", "Test secrets", "Standard", 1, 5, None),
    ("Network", "Front Door, NAT, Bastion, Registry", "Shared with production", "Separate routes and WAF policy", 1, 0, None),
    ("Operations", "Azure Monitor / Log Analytics", "Logs and metrics", "About 20 GB ingested a month", 1, 70, None),
]

# **Staged cost (Chinmay, 4 October 2026, CHG-R11-003: "Staged: start ~$1.9k").** Launch on Stage 1 and grow to the
# full cell (Stage 2 = the two sheets above) later; Stage 0 is a reference line only. Each line says where its price
# comes from: "workbook" is this file's own unit price (Azure Retail Prices API, 30 September); "Retail API, 4 Oct"
# is the Azure Retail Prices API (prices.azure.com, uaenorth or the service's billing zone) read on 4 October 2026.
# Shape from the 25 September AWS hosting-cost board (Stage 0 one server, Stage 1 two servers + LB + PostgreSQL
# Multi-AZ + GPU, Stage 2 the shared cell), priced here on Azure UAE North.
STAGE_1 = [
    ("Compute (AKS)", "Azure Kubernetes Service", "Control plane, Free tier",
     "No uptime SLA at launch; Standard tier ($73) from Stage 2. Workbook (pre-production line)", 1, 0, None),
    ("Compute (AKS)", "Virtual Machines (AKS nodes)",
     "Two nodes running every deployable, Redis, Qdrant and the broker in-cluster",
     "D8s v5 (8 vCPU, 32 GB), Linux, one per zone. The same images and Helm chart as the cell; one replica per "
     "deployable across the two nodes (ADR-0061 as amended 4 October: the floors apply from Stage 2). Workbook",
     2, 350, None),
    ("Vector store", "Managed Disks", "Qdrant storage (single in-cluster node)", "Premium SSD P15 256 GB. Workbook",
     1, 38, None),
    ("Event broker", "Managed Disks", "Broker storage (RabbitMQ single in-cluster node)",
     "Premium SSD P10 128 GB. Workbook", 1, 21.5, None),
    ("Cache", "Managed Disks", "Redis persistence (single in-cluster node, append-only file)",
     "Premium SSD P10 128 GB. Workbook (the broker disk's price)", 1, 21.5, None),
    ("Network", "Load Balancer", "Standard load balancer in front of the ingress; its outbound rule carries the "
     "static egress IP", "First 5 rules $0.025/h ($18.25) + about 1 TB processed at $0.005/GB ($5). Retail API, 4 Oct",
     1, 23.25, None),
    ("Network", "Public IP", "One static egress IP for the payment, e-invoicing and messaging allow-lists",
     "Standard IPv4 static, $0.005/h, on the load balancer's outbound rule (the NAT Gateway, $80, from Stage 2). "
     "Retail API, 4 Oct", 1, 3.65, None),
    ("Database", "Azure Database for PostgreSQL", "Primary with zone-redundant standby: control DB + DB per tenant",
     "Flexible Server 16, General Purpose D4ds v5 (4 vCore, 16 GB) x2 (primary + standby in another zone): "
     "ADR-0060 holds at every stage. No read or reporting replica at launch. Workbook", 2, 320, None),
    ("Database", "Azure Database for PostgreSQL", "Storage, primary and standby",
     "256 GB Premium SSD each; PITR backup 35 days. Workbook", 2, 36, None),
    ("AI", "Virtual Machines (AKS nodes)",
     "AI GPU node: ticvai-ai, Presidio, the Arabic NER, BGE-M3 and its reranker (CHG-R11-001)",
     "NV6ads A10 v5 (6 vCPU, 55 GB, 1/6 A10 with 4 GB), tainted, one node; the AI log tables live in the main "
     "PostgreSQL server at launch. $0.649/h. Retail API, 4 Oct", 1, 473.77, None),
    ("Storage", "Storage account (Blob, LRS)", "Media (including venue 3D models), exports, snapshots, dumps",
     "Hot tier, 2 TB, UAE North only. Workbook", 1, 45, None),
    ("Storage", "Container Registry", "Images for the five deployables", "Standard. Workbook", 1, 20, None),
    ("Security", "Key Vault", "Secrets and per-tenant keys", "Standard. Workbook", 1, 5, None),
    ("Network", "Azure Front Door", "TLS and WAF entry for web, apps and APIs, sized for launch",
     "Standard (not Premium): base $35 + 500 GB edge-to-client in zone 7 at $0.11/GB ($55) + about 10 million "
     "requests at $0.0108 per 10,000 ($10.80). Custom WAF and rate rules only; the managed OWASP and bot rule "
     "sets and the Private Link origin need Premium (Stage 2). Retail API, 4 Oct", 1, 100.80, None),
    ("Network", "Bandwidth", "Egress to the providers", "First 100 GB free, then $0.181/GB. Workbook", 1, 20, None),
    ("Operations", "Azure Monitor / Log Analytics", "Logs, metrics, alerts at launch volume",
     "About 20 GB ingested a month. Workbook (the pre-production rate)", 1, 70, None),
    ("AI (usage)", "LLM providers", "Language model calls (re-billed per token, AI-D02)", "Usage-based", 1, 0, None),
]
STAGE_1_PREPROD = [
    ("Compute (AKS)", "Azure Kubernetes Service", "Control plane", "Free tier. Workbook", 1, 0, None),
    ("Compute (AKS)", "Virtual Machines (AKS nodes)", "One node: every deployable, Redis, Qdrant and the broker",
     "D8s v5 (8 vCPU, 32 GB), Linux, one replica each. No GPU node: the models run on its CPU at test volume (an "
     "assumption to confirm in Sprint 2). Workbook", 1, 350, None),
    ("Database", "Azure Database for PostgreSQL", "Control DB + test tenant DBs",
     "General Purpose D2ds v5 + 256 GB, no standby (pre-production only). Workbook", 1, 196, None),
    ("Storage", "Storage account (Blob, LRS)", "Test media and snapshots", "Hot tier, 500 GB. Workbook", 1, 15, None),
    ("Security", "Key Vault", "Test secrets", "Standard. Workbook", 1, 5, None),
    ("Network", "Front Door, load balancer, registry, Log Analytics", "Shared with Stage 1 production",
     "Separate routes and WAF policy", 1, 0, None),
]
STAGE_0 = [
    ("Compute", "Virtual Machines", "One server running everything (reference only, not the plan)",
     "D16s v5 (16 vCPU, 64 GB), Linux, $0.942/h. No zone redundancy anywhere. Retail API, 4 Oct", 1, 687.66, None),
    ("AI", "Virtual Machines", "AI GPU node", "NV6ads A10 v5, $0.649/h. Retail API, 4 Oct", 1, 473.77, None),
]
NOTES_STAGES = [
    "Staged (Chinmay, 4 October 2026, CHG-R11-003: \"Staged: start ~$1.9k\"): launch on Stage 1, move to Stage 2 "
    "(the full cell on the other two sheets: $5,327.27 a month without zone-level HA, $8,295.04 with it) when the "
    "first trigger below fires. His ~$1.9k was the servers, PostgreSQL and the GPU node alone ($1,885.77 here); the "
    "rest of the launch platform brings Stage 1 production to the total above.",
    "Move to Stage 2 when any of these holds: a paying venue needs the availability targets of ADR-0060 (99.95% "
    "for cloud commerce; Stage 1 runs one replica per deployable, so a node or zone loss is an outage until it "
    "reschedules); traffic beyond Stage 1 capacity is sustained (CPU above about 70% on both nodes at the daily "
    "peak for a week, or the GPU node at its CPU or memory limit); a large on-sale is booked; or a client needs "
    "Premium WAF (managed OWASP and bot rules) or a private origin.",
    "ADR-0061's replica floors apply from Stage 2; at Stage 1 they are relaxed to one replica per deployable "
    "across the two nodes (ADR-0061, amended 4 October). PostgreSQL keeps its zone-redundant standby at every "
    "stage (ADR-0060).",
    "Not included at Stage 1: Defender for Cloud (about $150-200 at this size if taken), Azure Bastion, Private "
    "Link, a NAT Gateway, Azure Managed Redis, the AI log server, read and reporting replicas: each comes with "
    "Stage 2. LLM tokens, SMS, email, payment and e-invoicing fees are usage, not hosting.",
    "Stage 0 is a reference line only (one server and the GPU node, no PostgreSQL service, no redundancy): it is "
    "not the plan.",
]

NOTES_PROD = [
    "Prices: " + PRICE_SOURCE + " Confirm each line in the Azure pricing calculator for UAE North before "
    "quoting; reserved instances (1 or 3 years) lower compute by roughly 30-55%.",
    "Redis is Azure Managed Redis (ADR-0032, amended 30 September). Azure Cache for Redis retires on 30 September "
    "2028 and new customers cannot create it from 1 October 2026, so the platform does not start on it.",
    "Every store is hosted in the UAE, backups and disaster recovery included (DR in UAE Central, ADR-0060). "
    "Qdrant was approved on that condition (30 September).",
    "One production cell serves many tenants: each tenant has its own PostgreSQL database and its own Qdrant "
    "collection with a collection-scoped key.",
    "Node counts carry the replica floors of ADR-0061 (accepted 1 October): commerce 3, access 2, operations 2, "
    "workers 2, ticvai-ai real-time 2 (3 in a large cell), interactive 1, batch 0: 12 a cell, 13 in a large one. "
    "Pod sizes are assumptions until tools/bench.py measures them: about 1 vCPU for a .NET replica and about "
    "1 vCPU for an AI pod, which mostly waits on the provider's streamed answer (AI design 4.3).",
    "AI hosting (Chinmay, 4 October, CHG-R11-001): we host the embedding model (BGE-M3), its reranker, Presidio "
    "and the Arabic NER, together with the ticvai-ai pods, on one AI GPU node pool (NV6ads A10 v5, $473.77 a "
    "month a node; one node without HA, two with HA, one per zone); never an LLM, which stays with the providers "
    "(Core42 Compass, OpenAI UAE, BYOK). The 2 x D8s v5 AI CPU pool ($700) is gone: $8,047.50 became $8,295.04 "
    "with HA, $5,553.50 became $5,327.27 without. Defender for Containers is not re-priced for the GPU nodes' "
    "vCores (6 a node against the D8s v5's 8, so slightly lower). On AWS (me-central-1) the node is a "
    "g6.2xlarge (one L4 with 24 GB, 8 vCPU), $1.20043 an hour, $876.31 a month, offered in the region (AWS Price "
    "List API, 4 October; CHG-R3-001): the AWS workbook beside this one.",
    "\"When scaled up\" doubles the autoscaled lines (workload and AI GPU pools, Front Door traffic, bandwidth) for "
    "busy periods such as a holiday peak. A large on-sale runs in its own burst environment (ADR-0035, amended "
    "3 September; deploy/c-flash-sale.yml), not priced here.",
    "Not included: Azure OpenAI tokens (billed per use), SMS, email and WhatsApp fees, payment provider fees, "
    "the e-invoicing provider (ADR-0062, proposed: the client names it), the DR module in UAE Central (bought "
    "per tenant), Apple and Google developer accounts, and venue hardware.",
    "The venue edge node (one per venue, runs the gates and POS offline) is venue hardware, not Azure: "
    "recommended 8 cores, 32 GB RAM, 1 TB SSD, two units per venue for failover.",
    "The event broker is the client's choice, due Monday 12 October (ADR-0057, proposed; "
    "docs/active/broker-decision-pack.md). We recommend RabbitMQ on CloudAMQP in UAE North: 3 nodes, $297-597 + "
    "$99 PrivateLink ($396-696), once 84codes confirms in writing that backups, settings and logs stay in UAE "
    "North. The sheet prices the fallback, RabbitMQ self-run on AKS (the Terraform default), because the plan "
    "is picked by the sprint-2 load test. Kafka alternatives: Event Hubs Standard with the Kafka endpoint "
    "$60-130 (10 topics per namespace); Premium 1 PU about $1,072; Confluent Cloud Enterprise about "
    "$1,280-1,640.",
    "Front Door is a global service. It holds no personal data: it caches only public content (the on-sale "
    "waiting-room page, ADR-0066; public media such as the venue 3D models, ADR-0069) and decrypts at the edge "
    "nearest the user. Its WAF logs go to the UAE North Log Analytics workspace.",
]
NOTES_NO_HA = [
    "Single zone for everything except PostgreSQL: a zone outage stops the cloud services until they are "
    "restored, and the database fails over to its standby. Venue gates and POS keep working on the venue edge "
    "node, offline.",
    "Not suitable for the cloud availability targets (ADR-0060, proposed: 99.95% for cloud commerce, 99.9% for "
    "the back office); use the high-availability sheet. Whether production may run this way is the client's "
    "answer to ADR-0060.",
    "Recomputed 1 October 2026 (prices unchanged, those of 30 September): $4,531.50 became $5,553.50. "
    "PostgreSQL gains its zone-redundant standby, because production PostgreSQL is zone-redundant on every "
    "tier (ADR-0060, Chinmay, 1 October): +$320 compute, +$36 storage. A reporting replica of its own, because "
    "reporting never reads an operational replica (ADR-0016, the Terraform's enable_reporting_replica): "
    "+$196. A second AI node, because one node cannot hold the AI floors beside the embedding model and "
    "reranker (ADR-0061): +$350. The Private Link line the sheet lacked: +$50. Defender for the extra 8 vCores "
    "and the fourth PostgreSQL server: +$70.",
    "Recomputed 4 October 2026 (Chinmay, CHG-R11-001): the AI pool is one GPU node, NV6ads A10 v5 at $473.77, "
    "carrying the ticvai-ai pods, Presidio, the Arabic NER, BGE-M3 and its reranker, in place of the two D8s v5 "
    "AI nodes ($700): $5,553.50 became $5,327.27.",
]
NOTES_PREPROD = [
    "One pre-production environment for acceptance testing and client demos; development runs locally on "
    "docker-compose (deploy/*.yml) and on this cluster.",
    "Zero-priced lines are covered by production.",
]

# ---------------------------------------------------------------------------------------------------------
# AWS (CHG-R3-001). The same cell, service for service, on AWS me-central-1 (Middle East, UAE). Chinmay,
# 4 October 2026: "HLD and LLD you didnt add AWS you just did azure add that in as well"; the AI GPU node runs
# "in Azure and aws hosted in UAE north" (CHG-R11-001). Every AWS unit price below comes from AWS_RATE, read from
# the AWS Price List API's public bulk offer files for me-central-1; nothing is estimated from another region.
# What the files do not price is said to be "to confirm" in the line, never filled in.
# ---------------------------------------------------------------------------------------------------------
AWS_DATE = "4 October 2026"
HOURS = 730
AWS_PRICE_SOURCE = ("AWS Price List API, public bulk offer files (pricing.us-east-1.amazonaws.com/offers/v1.0/aws/"
                    "<service>/current/me-central-1/index.json; CloudFront's global file), region me-central-1 "
                    "(Middle East, UAE), on demand, Linux, 730 hours a month, pulled 4 October 2026 (files "
                    "published 11 September to 3 October 2026; each rate names its file and date in AWS_RATE).")
# key: (USD, per, what, offer file and its publication date)
AWS_RATE = {
    "eks":            (0.10, "hour", "EKS cluster, standard support", "AmazonEKS 2026-09-28"),
    "m6i.large":      (0.1177, "hour", "EC2 m6i.large (2 vCPU, 8 GiB), Linux", "AmazonEC2 2026-09-25"),
    "m6i.xlarge":     (0.2354, "hour", "EC2 m6i.xlarge (4 vCPU, 16 GiB), Linux", "AmazonEC2 2026-09-25"),
    "m6i.2xlarge":    (0.4708, "hour", "EC2 m6i.2xlarge (8 vCPU, 32 GiB), Linux", "AmazonEC2 2026-09-25"),
    "m6i.4xlarge":    (0.9416, "hour", "EC2 m6i.4xlarge (16 vCPU, 64 GiB), Linux", "AmazonEC2 2026-09-25"),
    "r6i.large":      (0.1551, "hour", "EC2 r6i.large (2 vCPU, 16 GiB), Linux", "AmazonEC2 2026-09-25"),
    "r6i.xlarge":     (0.3102, "hour", "EC2 r6i.xlarge (4 vCPU, 32 GiB), Linux", "AmazonEC2 2026-09-25"),
    "g6.xlarge":      (0.98824, "hour", "EC2 g6.xlarge (4 vCPU, 16 GiB, 1 x L4 24 GB), Linux", "AmazonEC2 2026-09-25"),
    "g6.2xlarge":     (1.20043, "hour", "EC2 g6.2xlarge (8 vCPU, 32 GiB, 1 x L4 24 GB), Linux", "AmazonEC2 2026-09-25"),
    "g5.xlarge":      (1.234, "hour", "EC2 g5.xlarge (4 vCPU, 16 GiB, 1 x A10G 24 GB), Linux", "AmazonEC2 2026-09-25"),
    "g5.2xlarge":     (1.48669, "hour", "EC2 g5.2xlarge (8 vCPU, 32 GiB, 1 x A10G 24 GB), Linux", "AmazonEC2 2026-09-25"),
    "gp3":            (0.0968, "GB-month", "EBS gp3 volume", "AmazonEC2 2026-09-25"),
    "ebs-snap":       (0.055, "GB-month", "EBS snapshot storage", "AmazonEC2 2026-09-25"),
    "nat":            (0.0528, "hour", "NAT Gateway (zonal; the Regional NAT Gateway is the same rate)", "AmazonEC2 2026-09-25"),
    "nat-gb":         (0.0528, "GB", "NAT Gateway data processed", "AmazonEC2 2026-09-25"),
    "ipv4":           (0.005, "hour", "Public IPv4 address (Elastic IP), in use", "AmazonVPC 2026-09-17"),
    "vpce":           (0.0121, "hour", "Interface VPC endpoint, per AZ", "AmazonVPC 2026-09-17"),
    "vpce-gb":        (0.01, "GB", "Interface VPC endpoint data processed, first 1 PB", "AmazonVPC 2026-09-17"),
    "rds-m6g.large":  (0.193, "hour", "RDS PostgreSQL db.m6g.large (2 vCPU, 8 GiB), single-AZ", "AmazonRDS 2026-10-01"),
    "rds-m6g.xlarge": (0.386, "hour", "RDS PostgreSQL db.m6g.xlarge (4 vCPU, 16 GiB), single-AZ", "AmazonRDS 2026-10-01"),
    "rds-m6g.xlarge-maz": (0.772, "hour", "RDS PostgreSQL db.m6g.xlarge, Multi-AZ DB instance", "AmazonRDS 2026-10-01"),
    "rds-gp3":        (0.14, "GB-month", "RDS gp3 storage, single-AZ", "AmazonRDS 2026-10-01"),
    "rds-gp3-maz":    (0.279, "GB-month", "RDS gp3 storage, Multi-AZ", "AmazonRDS 2026-10-01"),
    "rds-backup":     (0.1045, "GB-month", "RDS backup storage beyond the free allocation", "AmazonRDS 2026-10-01"),
    "aurora-r6g.large":  (0.313, "hour", "Aurora PostgreSQL db.r6g.large (2 vCPU, 16 GiB), Standard", "AmazonRDS 2026-10-01"),
    "aurora-r6g.xlarge": (0.627, "hour", "Aurora PostgreSQL db.r6g.xlarge (4 vCPU, 32 GiB), Standard", "AmazonRDS 2026-10-01"),
    "aurora-storage": (0.121, "GB-month", "Aurora storage, Standard", "AmazonRDS 2026-10-01"),
    "aurora-io":      (0.242, "million I/O", "Aurora I/O requests, Standard", "AmazonRDS 2026-10-01"),
    "valkey-r7g.large": (0.2142, "hour", "ElastiCache Valkey cache.r7g.large (13.07 GiB)", "AmazonElastiCache 2026-09-14"),
    "valkey-m7g.large": (0.153, "hour", "ElastiCache Valkey cache.m7g.large (6.38 GiB)", "AmazonElastiCache 2026-09-14"),
    "redis-r7g.large":  (0.2678, "hour", "ElastiCache Redis OSS cache.r7g.large", "AmazonElastiCache 2026-09-14"),
    "mq-rabbit-3x":   (1.005, "hour", "Amazon MQ for RabbitMQ, 3-node cluster mq.m7g.large", "AmazonMQ 2026-09-11"),
    "mq-storage":     (0.121, "GB-month", "Amazon MQ RabbitMQ storage", "AmazonMQ 2026-09-11"),
    "s3":             (0.025, "GB-month", "S3 Standard, first 50 TB", "AmazonS3 2026-09-28"),
    "ecr":            (0.10, "GB-month", "ECR storage", "AmazonECR 2026-09-11"),
    "secret":         (0.40, "secret-month", "Secrets Manager secret", "AWSSecretsManager 2026-09-11"),
    "kms-key":        (1.00, "key-month", "KMS customer managed key", "awskms 2026-09-11"),
    "cf-gb":          (0.110, "GB", "CloudFront data transfer out, Middle East, first 10 TB", "AmazonCloudFront 2026-10-03"),
    "cf-req":         (0.0120, "10,000 HTTPS requests", "CloudFront HTTPS requests, Middle East", "AmazonCloudFront 2026-10-03"),
    "waf-acl":        (5.0, "web ACL-month", "WAF web ACL", "awswaf 2026-09-14"),
    "waf-rule":       (1.0, "rule-month", "WAF rule or managed rule group", "awswaf 2026-09-14"),
    "waf-req":        (0.60, "million requests", "WAF requests", "awswaf 2026-09-14"),
    "waf-bot":        (10.0, "month", "WAF Bot Control (common), subscription", "awswaf 2026-09-14"),
    "waf-bot-req":    (1.0, "million requests", "WAF Bot Control requests beyond the first 10 million", "awswaf 2026-09-14"),
    "alb":            (0.028224, "hour", "Application Load Balancer", "AWSELB 2026-09-11"),
    "alb-lcu":        (0.00896, "LCU-hour", "Application Load Balancer capacity unit", "AWSELB 2026-09-11"),
    "egress":         (0.117, "GB", "Data transfer out to the Internet, first 10 TB (the file's description says $0.117, "
                       "its price column $0.11; the higher is used)", "AWSDataTransfer 2026-09-16"),
    "to-bahrain":     (0.09, "GB", "Data transfer me-central-1 to me-south-1 (description $0.09, price column $0.085)",
                       "AWSDataTransfer 2026-09-16"),
    "cw-ingest":      (0.63, "GB", "CloudWatch Logs ingestion, Standard class", "AmazonCloudWatch 2026-09-22"),
    "cw-store":       (0.033, "GB-month", "CloudWatch Logs storage", "AmazonCloudWatch 2026-09-22"),
    "cw-metric":      (0.30, "metric-month", "CloudWatch custom metric, first 10,000", "AmazonCloudWatch 2026-09-22"),
    "gd-eks":         (1.58, "vCPU-month", "GuardDuty EKS Runtime Monitoring, first 500 vCPU", "AmazonGuardDuty 2026-09-17"),
    "gd-rds":         (1.03, "vCPU-month", "GuardDuty RDS Protection", "AmazonGuardDuty 2026-09-17"),
    "gd-logs":        (1.25, "GB", "GuardDuty VPC flow and DNS log analysis, first 500 GB", "AmazonGuardDuty 2026-09-17"),
    "gd-trail":       (5.0, "million events", "GuardDuty CloudTrail event analysis", "AmazonGuardDuty 2026-09-17"),
    "insp-ec2":       (0.0021, "instance-hour", "Inspector EC2 scanning", "AmazonInspectorV2 2026-09-11"),
    "sh-ec2":         (0.0056944, "instance-hour", "Security Hub Essentials, per EC2 instance", "AWSSecurityHub 2026-09-30"),
}
# Prices the files do not give, or that depend on a choice not yet made. Each is "to confirm", never filled in.
AWS_TO_CONFIRM = [
    "g6 capacity in each of me-central-1's three AZs (the Price List API lists g6.2xlarge for the region, not per AZ)",
    "whether a Regional NAT Gateway presents one egress IP for all three AZs (priced here as three zonal gateways, "
    "three IPs to allow-list)",
    "CloudFront VPC origins and Systems Manager Session Manager: no charge line in the price list files",
    "AWS WAF on CloudFront is a global web ACL: the me-central-1 WAF rates are used, to check against the bill",
    "S3 and ECR requests, KMS and Secrets Manager API calls, RDS backup beyond the free allocation: usage, not priced",
    "CloudAMQP on AWS me-central-1 (the broker the client may take; on Azure it is in UAE North)",
    "Aurora I/O volume (Aurora is not chosen; its I/O cost is unknown until the load test)",
    "Volumes behind usage lines (logs, metrics, LCUs, GuardDuty data, requests): assumptions, as on the Azure sheets",
]


def _h(k, n=1):
    """A month (730 hours) of n units of an hourly AWS rate."""
    return round(AWS_RATE[k][0] * HOURS * n, 2)


def _q(k, qty):
    """qty units of a non-hourly AWS rate (GB, keys, requests in the rate's own unit)."""
    return round(AWS_RATE[k][0] * qty, 2)


def _usd(x):
    return f"${x:,.2f}"


NODE_ROOT_GB = 80  # gp3 root volume per EKS node (images, logs, the GPU node's model cache)


def _root(n):
    return (f"gp3 {NODE_ROOT_GB} GB per node at $0.0968 per GB-month ({_usd(_q('gp3', NODE_ROOT_GB))} a node), {n} nodes. "
            "The Azure sheets carry no OS-disk line", round(_q("gp3", NODE_ROOT_GB), 2))


def _cf(gb, mreq):
    tot = round(_q("cf-gb", gb) + _q("cf-req", mreq * 100), 2)
    return (f"{gb:,} GB to viewers in the Middle East at $0.110/GB ({_usd(_q('cf-gb', gb))}) + about {mreq} million HTTPS "
            f"requests at $0.0120 per 10,000 ({_usd(_q('cf-req', mreq * 100))}). Origin fetches from the ALB are free; a VPC "
            "origin keeps the ALB private (no charge line in the price list, to confirm)", tot)


def _waf(rules, mreq, bot):
    parts = [_q("waf-acl", 1), _q("waf-rule", rules), _q("waf-req", mreq)]
    text = (f"Web ACL $5 + about {rules} rules and managed rule groups (AWS managed core rule set for OWASP, "
            f"rate-based rules per client IP) at $1 ({_usd(parts[1])}) + {mreq} million requests at $0.60 per million "
            f"({_usd(parts[2])})")
    if bot:
        parts += [_q("waf-bot", 1), _q("waf-bot-req", max(mreq - 10, 0))]
        text += f" + Bot Control (common) $10 + {max(mreq - 10, 0)} million requests beyond the first 10 million at $1 per million ({_usd(parts[4])})"
    return text + ". A CloudFront web ACL is global: the me-central-1 rates, to confirm on the bill", round(sum(parts), 2)


def _alb(lcu):
    tot = round(_h("alb") + _h("alb-lcu", lcu), 2)
    return (f"$0.028224/h ({_usd(_h('alb'))}) + about {lcu} LCU on average at $0.00896 per LCU-hour "
            f"({_usd(_h('alb-lcu', lcu))}, an assumption). AWS Load Balancer Controller on the system node group", tot)


def _nat(n, tb=1):
    gw, gb, ip = _h("nat", n), _q("nat-gb", tb * 1024), _h("ipv4", n)
    return (f"{n} zonal NAT Gateway{'s, one per AZ' if n > 1 else ''} at $0.0528/h ({_usd(gw)}) + {tb} TB processed at "
            f"$0.0528/GB ({_usd(gb)}) + {n} Elastic IP{'s' if n > 1 else ''} at $0.005/h ({_usd(ip)})"
            + (". Three IPs to allow-list, not one; a Regional NAT Gateway (same hourly rate) may present fewer, to confirm"
               if n > 1 else ""), round(gw + gb + ip, 2))


def _vpce(endpoints, azs, gb=100):
    hrs, data = _h("vpce", endpoints * azs), _q("vpce-gb", gb)
    return (f"{endpoints} interface endpoints (ECR api and dkr, Secrets Manager, KMS, STS, CloudWatch Logs) x {azs} AZ"
            f"{'s' if azs > 1 else ''} at $0.0121/h ({_usd(hrs)}) + about {gb} GB processed at $0.01/GB ({_usd(data)}); "
            "S3 through a gateway endpoint (free); Route 53 private hosted zones", round(hrs + data, 2))


def _egress(gb=200):
    tot = _q("egress", gb - 100)
    return (f"About {gb} GB a month: the first 100 GB free, then $0.117/GB ({_usd(tot)}). The ALB-to-CloudFront traffic "
            "is free; the web traffic is in the CloudFront line", tot)


def _cw(gb, metrics):
    a, b, c = _q("cw-ingest", gb), _q("cw-store", gb), _q("cw-metric", metrics)
    return (f"About {gb} GB of logs ingested at $0.63/GB ({_usd(a)}), stored at $0.033 per GB-month ({_usd(b)} in the first "
            f"month, growing with retention), about {metrics} custom metrics at $0.30 ({_usd(c)})", round(a + b + c, 2))


def _sec(eks_vcpu, rds_vcpu, log_gb, trail_m, instances):
    p = [_q("gd-eks", eks_vcpu), _q("gd-rds", rds_vcpu), _q("gd-logs", log_gb), _q("gd-trail", trail_m),
         _h("insp-ec2", instances), _h("sh-ec2", instances)]
    return (f"GuardDuty EKS Runtime Monitoring {eks_vcpu} vCPU x $1.58 ({_usd(p[0])}); RDS Protection {rds_vcpu} vCPU x "
            f"$1.03 ({_usd(p[1])}); VPC flow and DNS logs about {log_gb} GB x $1.25 ({_usd(p[2])}) and about {trail_m} "
            f"million CloudTrail events ({_usd(p[3])}); Inspector {instances} instances x 730 h x $0.0021 ({_usd(p[4])}); "
            f"Security Hub Essentials {instances} instances x 730 h x $0.0056944 ({_usd(p[5])}). Volumes are assumptions",
            round(sum(p), 2))


def _rds(inst, gb, maz=False):
    return round(_h(inst) + _q("rds-gp3-maz" if maz else "rds-gp3", gb), 2)


_GPU_SPEC = ("g6.2xlarge (8 vCPU, 32 GiB, 1 x NVIDIA L4 24 GB), $1.20043/h, tainted. Offered in me-central-1 (EC2 price "
             "list of 25 September); g6 capacity in each AZ to confirm. Carries the floors (real-time 2, interactive 1, "
             "batch 0, about 1 vCPU a pod), Presidio on the CPU, and on the GPU BGE-M3, its reranker and the Arabic NER; "
             "never an LLM. g6.xlarge ($721.42) has 4 vCPU, too few for the AI pods beside Presidio; g5.xlarge "
             "($900.82) costs more with 4 vCPU; g5.2xlarge $1,085.28")

_r = {k: v for k, v in [("ha_root", _root(14)), ("noha_root", _root(7)), ("ha_cf", _cf(2048, 50)),
                         ("ha_waf", _waf(8, 50, True)), ("alb2", _alb(2)), ("alb1", _alb(1)), ("nat3", _nat(3)),
                         ("nat1", _nat(1)), ("vpce3", _vpce(6, 3)), ("vpce1", _vpce(6, 1)), ("egress", _egress()),
                         ("cw60", _cw(60, 200)), ("cw40", _cw(40, 150)), ("cw20", _cw(20, 100)), ("cw20p", _cw(20, 50)),
                         ("sec_ha", _sec(70, 18, 20, 2, 14)), ("sec_noha", _sec(38, 12, 15, 2, 7)),
                         ("s1_cf", _cf(500, 10)), ("s1_waf", _waf(5, 10, False)), ("s1_root", _root(3)),
                         ("pre_root", _root(3)), ("s1p_root", _root(1))]}

# (group, service type, description, specs, qty, unit USD, scaled qty or None = same): the Azure rows' shape.
AWS_PROD_HA = [
    ("Compute (EKS)", "Amazon EKS", "Control plane, standard support",
     "$0.10/h; the uptime SLA is included (the AKS Standard tier line)", 1, _h("eks"), None),
    ("Compute (EKS)", "EC2 (EKS managed node group)", "System node group (and the ingress controller pods)",
     "m6i.xlarge (4 vCPU, 16 GiB; the D4s v5 line), Linux, $0.2354/h, autoscale 2-4 across AZs a-c; budgeted at 3, "
     "one per AZ", 3, _h("m6i.xlarge"), None),
    ("Compute (EKS)", "EC2 (EKS managed node group)", "Workload node group: commerce, access, operations, workers",
     "m6i.2xlarge (8 vCPU, 32 GiB; the D8s v5 line), $0.4708/h, autoscale 3-20 across AZs. Carries ADR-0061's floors "
     "as on Azure: 9 replicas, commerce one per AZ. Scaled up, 6 nodes", 3, _h("m6i.2xlarge"), 6),
    ("Compute (EKS)", "EC2 (EKS managed node group)",
     "AI GPU node group: ticvai-ai, BGE-M3 and its reranker, Presidio and the Arabic NER (CHG-R11-001)",
     _GPU_SPEC + ". One node per AZ", 2, _h("g6.2xlarge"), 4),
    ("Compute (EKS)", "EBS (gp3)", "Node root volumes", _r["ha_root"][0] + " (3 system, 3 workload, 2 GPU, 3 qdrant, "
     "3 broker; 19 scaled up)", 14, _r["ha_root"][1], 19),
    ("Vector store", "EC2 (EKS managed node group)", "Qdrant cluster, one collection per tenant (ADR-0049)",
     "qdrant node group: r6i.xlarge (4 vCPU, 32 GiB; the E4s v5 line), $0.3102/h, x3 one per AZ, replication factor 2, "
     "TLS, collection-scoped JWT per tenant; tainted ticvai.io/pool=data", 3, _h("r6i.xlarge"), None),
    ("Vector store", "EBS (gp3)", "Qdrant storage",
     "gp3 256 GB per node at $0.0968 per GB-month. Snapshots per collection go to S3 by a CronJob", 3, _q("gp3", 256), None),
    ("Event broker", "EC2 (EKS managed node group)",
     "Broker cluster: RabbitMQ recommended, or Kafka (the client's choice; ADR-0057, proposed)",
     "broker node group: m6i.large (2 vCPU, 8 GiB; the D2s v5 line), $0.1177/h, x3 across AZs, self-run with the "
     "RabbitMQ Cluster Operator, as on Azure (broker_self_hosted). Managed alternative: Amazon MQ for RabbitMQ, 3-node "
     f"mq.m7g.large cluster at $1.005/h ({_usd(_h('mq-rabbit-3x'))}) plus storage at $0.121 per GB-month; CloudAMQP in "
     "me-central-1 to confirm", 3, _h("m6i.large"), None),
    ("Event broker", "EBS (gp3)", "Broker storage: quorum queues or Kafka logs", "gp3 128 GB per node", 3, _q("gp3", 128), None),
    ("Database", "Amazon RDS for PostgreSQL", "Primary with a Multi-AZ standby: control DB + DB per tenant",
     "PostgreSQL 16, db.m6g.xlarge (4 vCPU, 16 GiB, Graviton; the D4ds v5 line), Multi-AZ DB instance (synchronous "
     "standby in another AZ, automatic failover), $0.772/h, twice the single-AZ rate. Multi-AZ on every production "
     "tier (ADR-0060). RDS, not Aurora (see the notes)", 1, _h("rds-m6g.xlarge-maz"), None),
    ("Database", "Amazon RDS for PostgreSQL", "Storage, primary and standby",
     "gp3 256 GB Multi-AZ at $0.279 per GB-month; automated backups (PITR up to 35 days) free up to the provisioned "
     "storage, then $0.1045 per GB-month (not priced)", 1, _q("rds-gp3-maz", 256), None),
    ("Database", "Amazon RDS for PostgreSQL", "Read replicas (operational reads; gate checks never read here)",
     "db.m6g.xlarge single-AZ ($0.386/h) + gp3 256 GB ($0.14 per GB-month) each, in different AZs", 2,
     _rds("rds-m6g.xlarge", 256), None),
    ("Database", "Amazon RDS for PostgreSQL", "Reporting replica (lag-tolerant, no writes)",
     "db.m6g.large (2 vCPU, 8 GiB; the D2ds v5 line), $0.193/h, + gp3 256 GB", 1, _rds("rds-m6g.large", 256), None),
    ("Database", "Amazon RDS for PostgreSQL", "AI log database (decision records, prompts)",
     "db.m6g.xlarge single-AZ + gp3 1,024 GB. A writable instance of its own (ADR-0020, amended by ADR-0049)", 1,
     _rds("rds-m6g.xlarge", 1024), None),
    ("Cache", "Amazon ElastiCache (Valkey)",
     "Sessions, idempotency keys, per-tenant request budgets (ADR-0064), waiting-room positions (ADR-0066), "
     "the one-second browse cache (ADR-0065, proposed), AI features",
     "cache.r7g.large (13.07 GiB; the B10 12 GB line), $0.2142/h, a primary and one replica in another AZ, Multi-AZ "
     "with automatic failover. Valkey is the Redis-compatible engine ElastiCache prices lowest (Redis OSS $0.2678/h)",
     2, _h("valkey-r7g.large"), None),
    ("Storage", "Amazon S3",
     "Media (including venue 3D models and navigation files, ADR-0069), exports, Qdrant snapshots, database dumps",
     "S3 Standard, 2,048 GB at $0.025 per GB-month, stored across AZs (the ZRS line), me-central-1 only; requests "
     "not priced", 1, _q("s3", 2048), None),
    ("Storage", "Amazon ECR", "Images for the five deployables", "About 100 GB at $0.10 per GB-month (an assumption)",
     1, _q("ecr", 100), None),
    ("Security", "AWS Secrets Manager",
     "Secrets (the Qdrant API key and the waiting-room token key, each read only by its issuer)",
     "About 20 secrets at $0.40 a month (an assumption); API calls $0.05 per 10,000 (not priced)", 20, _q("secret", 1), None),
    ("Security", "AWS KMS", "Platform keys and per-tenant keys (ADR-0063 wraps each tenant's data key; BYOK)",
     "Customer managed keys at $1 a month; KMS keeps keys in FIPS 140-3 validated HSMs, so no premium tier is needed "
     "(Key Vault Premium on Azure). 5 platform keys budgeted; +$1 a tenant a month (about $200 at 200 tenants); BYOK "
     "by importing key material; requests $0.03 per 10,000 (not priced)", 5, _q("kms-key", 1), None),
    ("Network", "Amazon CloudFront",
     "Single entry for web, apps and APIs; the on-sale waiting-room page from its cache (ADR-0066)",
     _r["ha_cf"][0], 1, _r["ha_cf"][1], 2),
    ("Network", "AWS WAF", "WAF on CloudFront: OWASP and bot rules, rate rules per client IP",
     _r["ha_waf"][0], 1, _r["ha_waf"][1], 2),
    ("Network", "Elastic Load Balancing (ALB)",
     "Ingress: an internal Application Load Balancer, CloudFront's VPC origin (the internal LB and Private Link line)",
     _r["alb2"][0], 1, _r["alb2"][1], 2),
    ("Network", "NAT Gateway", "Static egress IPs for payment, e-invoicing and messaging allow-lists",
     _r["nat3"][0], 1, _r["nat3"][1], None),
    ("Network", "Systems Manager Session Manager", "Administrative access only (the Azure Bastion line)",
     "No charge line in the me-central-1 Systems Manager price list (11 September), to confirm; no inbound port, "
     "no SSH keys; sessions logged to CloudWatch", 1, 0, None),
    ("Network", "AWS PrivateLink (VPC endpoints)", "Private endpoints and private DNS (the Private Link line)",
     _r["vpce3"][0], 1, _r["vpce3"][1], None),
    ("Network", "Data transfer out", "Egress through the NAT Gateways to providers", _r["egress"][0], 1,
     _r["egress"][1], 2),
    ("Operations", "Amazon CloudWatch", "Logs, metrics, alerts, dashboards", _r["cw60"][0], 1, _r["cw60"][1], None),
    ("Operations", "AWS Backup", "Snapshots of the Qdrant and broker volumes",
     "Daily EBS snapshots, 30 days, in me-central-1: about 500 GB of incremental snapshot storage at $0.055 per "
     "GB-month (an assumption)", 1, _q("ebs-snap", 500), None),
    ("Operations", "GuardDuty, Inspector, Security Hub",
     "Threat detection for EKS, RDS and the account, node scanning, posture (the Defender for Cloud line)",
     _r["sec_ha"][0], 1, _r["sec_ha"][1], None),
    ("AI (usage)", "LLM providers", "Language model calls (re-billed per token, AI-D02)",
     "Usage-based; not a fixed hosting cost", 1, 0, None),
]
AWS_PROD_NO_HA = [
    ("Compute (EKS)", "Amazon EKS", "Control plane, standard support", "$0.10/h; uptime SLA included", 1, _h("eks"), None),
    ("Compute (EKS)", "EC2 (EKS managed node group)", "System node group (and the ingress controller pods)",
     "m6i.xlarge (4 vCPU, 16 GiB), Linux, one AZ", 2, _h("m6i.xlarge"), None),
    ("Compute (EKS)", "EC2 (EKS managed node group)", "Workload node group: commerce, access, operations, workers",
     "m6i.2xlarge (8 vCPU, 32 GiB), autoscale 2-10. Carries the floors (ADR-0061): 9 replicas on 2 nodes; in one AZ "
     "commerce's three replicas cannot be one per AZ", 2, _h("m6i.2xlarge"), 4),
    ("Compute (EKS)", "EC2 (EKS managed node group)",
     "AI GPU node group: ticvai-ai, BGE-M3 and its reranker, Presidio and the Arabic NER (CHG-R11-001)",
     _GPU_SPEC + ". One node. With it down the scrubber is down and LLM calls are refused (503 scrubber-unavailable), "
     "never sent raw", 1, _h("g6.2xlarge"), 2),
    ("Compute (EKS)", "EBS (gp3)", "Node root volumes", _r["noha_root"][0] + " (2 system, 2 workload, 1 GPU, 1 qdrant, "
     "1 broker; 10 scaled up)", 7, _r["noha_root"][1], 10),
    ("Vector store", "EC2 (EKS managed node group)", "Qdrant, one collection per tenant (ADR-0049)",
     "r6i.xlarge (4 vCPU, 32 GiB), single node", 1, _h("r6i.xlarge"), None),
    ("Vector store", "EBS (gp3)", "Qdrant storage", "gp3 256 GB", 1, _q("gp3", 256), None),
    ("Event broker", "EC2 (EKS managed node group)",
     "Broker: RabbitMQ recommended, or Kafka (the client's choice; ADR-0057, proposed)",
     "m6i.large (2 vCPU, 8 GiB), single node, self-run", 1, _h("m6i.large"), None),
    ("Event broker", "EBS (gp3)", "Broker storage", "gp3 128 GB", 1, _q("gp3", 128), None),
    ("Database", "Amazon RDS for PostgreSQL", "Primary with a Multi-AZ standby: control DB + DB per tenant",
     "PostgreSQL 16, db.m6g.xlarge Multi-AZ, $0.772/h. The standby stays on this sheet: production PostgreSQL is "
     "zone-redundant on every tier (ADR-0060; Chinmay, 1 October)", 1, _h("rds-m6g.xlarge-maz"), None),
    ("Database", "Amazon RDS for PostgreSQL", "Storage, primary and standby", "gp3 256 GB Multi-AZ at $0.279; PITR 35 days",
     1, _q("rds-gp3-maz", 256), None),
    ("Database", "Amazon RDS for PostgreSQL", "Read replica (operational reads; gate checks never read here)",
     "db.m6g.xlarge single-AZ + gp3 256 GB", 1, _rds("rds-m6g.xlarge", 256), None),
    ("Database", "Amazon RDS for PostgreSQL", "Reporting replica (lag-tolerant, no writes)",
     "db.m6g.large + gp3 256 GB. Reporting never reads an operational replica (ADR-0016)", 1,
     _rds("rds-m6g.large", 256), None),
    ("Database", "Amazon RDS for PostgreSQL", "AI log database", "db.m6g.large + gp3 512 GB", 1,
     _rds("rds-m6g.large", 512), None),
    ("Cache", "Amazon ElastiCache (Valkey)", "Sessions, idempotency keys, request budgets, waiting-room positions, caches",
     "cache.r7g.large (13.07 GiB), one node, no replica; $0.2142/h. A production cell without the replica is the "
     "client's call (ADR-0060)", 1, _h("valkey-r7g.large"), None),
    ("Storage", "Amazon S3", "Media (including venue 3D models), exports, Qdrant snapshots, database dumps",
     "S3 Standard, 2,048 GB, me-central-1 only (S3 has no single-AZ hot class: One Zone-IA is infrequent access)", 1,
     _q("s3", 2048), None),
    ("Storage", "Amazon ECR", "Images for the five deployables", "About 100 GB", 1, _q("ecr", 100), None),
    ("Security", "AWS Secrets Manager", "Secrets (the Qdrant API key and the waiting-room token key)",
     "About 20 secrets at $0.40", 20, _q("secret", 1), None),
    ("Security", "AWS KMS", "Platform and per-tenant keys", "5 customer managed keys at $1 (+$1 a tenant a month)", 5,
     _q("kms-key", 1), None),
    ("Network", "Amazon CloudFront", "Single entry for web, apps and APIs; the on-sale waiting-room page",
     _r["ha_cf"][0], 1, _r["ha_cf"][1], 2),
    ("Network", "AWS WAF", "WAF on CloudFront: OWASP and bot rules, rate rules per client IP", _r["ha_waf"][0], 1,
     _r["ha_waf"][1], 2),
    ("Network", "Elastic Load Balancing (ALB)", "Ingress: an internal ALB, CloudFront's VPC origin", _r["alb2"][0], 1,
     _r["alb2"][1], 2),
    ("Network", "NAT Gateway", "One static egress IP for the allow-lists", _r["nat1"][0], 1, _r["nat1"][1], None),
    ("Network", "Systems Manager Session Manager", "Administrative access only",
     "No charge line in the price list, to confirm", 1, 0, None),
    ("Network", "AWS PrivateLink (VPC endpoints)", "Private endpoints and private DNS. No store has a public endpoint, "
     "with or without HA", _r["vpce1"][0], 1, _r["vpce1"][1], None),
    ("Network", "Data transfer out", "Egress through the NAT Gateway to providers", _r["egress"][0], 1,
     _r["egress"][1], 2),
    ("Operations", "Amazon CloudWatch", "Logs, metrics, alerts", _r["cw40"][0], 1, _r["cw40"][1], None),
    ("Operations", "AWS Backup", "Snapshots of the Qdrant and broker volumes",
     "About 200 GB of incremental EBS snapshots at $0.055 per GB-month", 1, _q("ebs-snap", 200), None),
    ("Operations", "GuardDuty, Inspector, Security Hub", "Threat detection, scanning, posture",
     _r["sec_noha"][0], 1, _r["sec_noha"][1], None),
    ("AI (usage)", "LLM providers", "Language model calls (re-billed per token, AI-D02)", "Usage-based", 1, 0, None),
]
AWS_PREPROD = [
    ("Compute (EKS)", "Amazon EKS", "Control plane",
     "$0.10/h: EKS has no free tier (AKS Free on Azure); a namespace on the production cluster would save it", 1,
     _h("eks"), None),
    ("Compute (EKS)", "EC2 (EKS managed node group)", "System and workload nodes, all five deployables",
     "m6i.2xlarge (8 vCPU, 32 GiB) x2 + m6i.xlarge x1, Linux. One replica per unit: the ADR-0061 floors are for "
     "production cells", 1, round(_h("m6i.2xlarge", 2) + _h("m6i.xlarge"), 2), None),
    ("Compute (EKS)", "EBS (gp3)", "Node root volumes", _r["pre_root"][0], 3, _r["pre_root"][1], None),
    ("Vector store", "EC2 (EKS managed node group)", "Qdrant, single node",
     "r6i.large (2 vCPU, 16 GiB; the E2s v5 line) + gp3 128 GB", 1, round(_h("r6i.large") + _q("gp3", 128), 2), None),
    ("Event broker", "EC2 (EKS managed node group)", "RabbitMQ, single node, whichever broker production uses",
     "m6i.large (2 vCPU, 8 GiB)", 1, _h("m6i.large"), None),
    ("Event broker", "EBS (gp3)", "Broker storage", "gp3 128 GB", 1, _q("gp3", 128), None),
    ("Database", "Amazon RDS for PostgreSQL", "Control DB + test tenant DBs + AI log DB",
     "PostgreSQL 16, db.m6g.large single-AZ + gp3 256 GB, no standby (pre-production only), no replicas", 1,
     _rds("rds-m6g.large", 256), None),
    ("Cache", "Amazon ElastiCache (Valkey)", "Test cache",
     "cache.m7g.large (6.38 GiB), one node, $0.153/h (no smaller Valkey node is listed for me-central-1)", 1,
     _h("valkey-m7g.large"), None),
    ("Storage", "Amazon S3", "Test media and snapshots", "S3 Standard, 500 GB", 1, _q("s3", 500), None),
    ("Security", "AWS Secrets Manager", "Test secrets", "About 5 secrets at $0.40", 5, _q("secret", 1), None),
    ("Network", "CloudFront, WAF, ALB, NAT, ECR", "Shared with production", "Separate behaviours and web ACL rules",
     1, 0, None),
    ("Operations", "Amazon CloudWatch", "Logs and metrics", _r["cw20p"][0], 1, _r["cw20p"][1], None),
]
AWS_STAGE_1 = [
    ("Compute (EKS)", "Amazon EKS", "Control plane",
     "$0.10/h. EKS has no free tier (AKS Free at Stage 1 on Azure)", 1, _h("eks"), None),
    ("Compute (EKS)", "EC2 (EKS managed node group)",
     "Two nodes running every deployable, Redis, Qdrant and the broker in-cluster",
     "m6i.2xlarge (8 vCPU, 32 GiB), Linux, $0.4708/h, one per AZ. The same images and Helm chart as the cell; one "
     "replica per deployable across the two nodes (ADR-0061 as amended 4 October: the floors apply from Stage 2)",
     2, _h("m6i.2xlarge"), None),
    ("Compute (EKS)", "EBS (gp3)", "Node root volumes", _r["s1_root"][0] + " (the two nodes and the GPU node)", 3,
     _r["s1_root"][1], None),
    ("Vector store", "EBS (gp3)", "Qdrant storage (single in-cluster node)", "gp3 256 GB", 1, _q("gp3", 256), None),
    ("Event broker", "EBS (gp3)", "Broker storage (RabbitMQ single in-cluster node)", "gp3 128 GB", 1, _q("gp3", 128), None),
    ("Cache", "EBS (gp3)", "Redis persistence (single in-cluster node, append-only file)", "gp3 128 GB", 1,
     _q("gp3", 128), None),
    ("Network", "Elastic Load Balancing (ALB)", "Ingress: an internal ALB, CloudFront's VPC origin", _r["alb1"][0], 1,
     _r["alb1"][1], None),
    ("Network", "NAT Gateway", "One static egress IP for the payment, e-invoicing and messaging allow-lists",
     _r["nat1"][0] + ". The nodes stay in private subnets (on Azure the load balancer's outbound rule carries the IP)",
     1, _r["nat1"][1], None),
    ("Database", "Amazon RDS for PostgreSQL", "Primary with a Multi-AZ standby: control DB + DB per tenant",
     "PostgreSQL 16, db.m6g.xlarge Multi-AZ, $0.772/h: ADR-0060 holds at every stage. No read or reporting replica "
     "at launch", 1, _h("rds-m6g.xlarge-maz"), None),
    ("Database", "Amazon RDS for PostgreSQL", "Storage, primary and standby", "gp3 256 GB Multi-AZ at $0.279; PITR 35 days",
     1, _q("rds-gp3-maz", 256), None),
    ("AI", "EC2 (EKS managed node group)",
     "AI GPU node: ticvai-ai, Presidio, the Arabic NER, BGE-M3 and its reranker (CHG-R11-001)",
     _GPU_SPEC + ". One node; the AI log tables live in the main PostgreSQL at launch", 1, _h("g6.2xlarge"), None),
    ("Storage", "Amazon S3", "Media (including venue 3D models), exports, snapshots, dumps",
     "S3 Standard, 2,048 GB, me-central-1 only", 1, _q("s3", 2048), None),
    ("Storage", "Amazon ECR", "Images for the five deployables", "About 100 GB", 1, _q("ecr", 100), None),
    ("Security", "AWS Secrets Manager", "Secrets", "About 20 secrets at $0.40", 20, _q("secret", 1), None),
    ("Security", "AWS KMS", "Platform and per-tenant keys", "5 customer managed keys at $1", 5, _q("kms-key", 1), None),
    ("Network", "Amazon CloudFront", "TLS entry for web, apps and APIs, sized for launch", _r["s1_cf"][0], 1,
     _r["s1_cf"][1], None),
    ("Network", "AWS WAF", "WAF on CloudFront, sized for launch: core rule set and rate rules; no Bot Control",
     _r["s1_waf"][0], 1, _r["s1_waf"][1], None),
    ("Network", "Data transfer out", "Egress to the providers", _r["egress"][0], 1, _r["egress"][1], None),
    ("Operations", "Amazon CloudWatch", "Logs, metrics, alerts at launch volume", _r["cw20"][0], 1, _r["cw20"][1], None),
    ("AI (usage)", "LLM providers", "Language model calls (re-billed per token, AI-D02)", "Usage-based", 1, 0, None),
]
AWS_STAGE_1_PREPROD = [
    ("Compute (EKS)", "Amazon EKS", "Control plane",
     "$0.10/h, a cluster of its own (a namespace on the Stage 1 cluster would save it)", 1, _h("eks"), None),
    ("Compute (EKS)", "EC2 (EKS managed node group)", "One node: every deployable, Redis, Qdrant and the broker",
     "m6i.2xlarge (8 vCPU, 32 GiB), one replica each. No GPU node: the models run on its CPU at test volume (an "
     "assumption to confirm in Sprint 2)", 1, _h("m6i.2xlarge"), None),
    ("Compute (EKS)", "EBS (gp3)", "Node root volume", _r["s1p_root"][0], 1, _r["s1p_root"][1], None),
    ("Database", "Amazon RDS for PostgreSQL", "Control DB + test tenant DBs",
     "db.m6g.large single-AZ + gp3 256 GB, no standby (pre-production only)", 1, _rds("rds-m6g.large", 256), None),
    ("Storage", "Amazon S3", "Test media and snapshots", "S3 Standard, 500 GB", 1, _q("s3", 500), None),
    ("Security", "AWS Secrets Manager", "Test secrets", "About 5 secrets at $0.40", 5, _q("secret", 1), None),
    ("Network", "CloudFront, WAF, ALB, NAT, ECR, CloudWatch", "Shared with Stage 1 production",
     "Separate behaviours and web ACL rules", 1, 0, None),
]
AWS_STAGE_0 = [
    ("Compute", "EC2", "One server running everything (reference only, not the plan)",
     "m6i.4xlarge (16 vCPU, 64 GiB), Linux, $0.9416/h. No AZ redundancy anywhere", 1, _h("m6i.4xlarge"), None),
    ("AI", "EC2", "AI GPU node", "g6.2xlarge, $1.20043/h", 1, _h("g6.2xlarge"), None),
]

AWS_DB_CHOICE = (
    f"RDS for PostgreSQL 16 (Multi-AZ DB instance), not Aurora PostgreSQL. Like for like, RDS costs less: the primary "
    f"with its standby is {_usd(_h('rds-m6g.xlarge-maz'))} (db.m6g.xlarge Multi-AZ) and the two read replicas and the "
    f"reporting replica {_usd(_h('rds-m6g.xlarge', 2) + _h('rds-m6g.large'))}, "
    f"{_usd(_h('rds-m6g.xlarge-maz') + _h('rds-m6g.xlarge', 2) + _h('rds-m6g.large'))} of instances in all; Aurora "
    f"PostgreSQL lists no general-purpose (db.m) class in me-central-1, only r and t, so the same shape is a db.r6g.xlarge writer and two readers (one is the "
    f"failover target, so it doubles as a replica) plus a db.r6g.large reporting reader, "
    f"{_usd(_h('aurora-r6g.xlarge', 3) + _h('aurora-r6g.large'))}, before Aurora's $0.242 per million I/O requests (a "
    f"volume nobody knows until the load test). RDS also matches the Azure design one for one (Flexible Server: a "
    f"standby that does not serve reads, separate replicas), so the Terraform module, the runbooks and ADR-0060 carry "
    f"over. Aurora's case is a faster failover (about 30 seconds against one to two minutes) and up to 15 readers; "
    f"revisit it if the commerce target (99.95%) needs that.")

AWS_GPU_CHOICE = (
    f"g6.2xlarge (8 vCPU, 32 GiB, one NVIDIA L4 with 24 GB) at $1.20043 an hour, {_usd(_h('g6.2xlarge'))} a month a "
    f"node: g6 is offered in me-central-1 (the EC2 offer file of 25 September lists g6.xlarge to g6.48xlarge). "
    f"g6.xlarge ({_usd(_h('g6.xlarge'))}) has 4 vCPU, too few for three AI pods at about 1 vCPU each beside Presidio "
    f"and the node's own daemons; g5.xlarge ({_usd(_h('g5.xlarge'))}, A10G) costs more and also has 4 vCPU; g5.2xlarge "
    f"is {_usd(_h('g5.2xlarge'))}. The L4's 24 GB is six times the 4 GB of Azure's NV6ads A10 v5 slice, so the "
    f"GPU-memory step-up Azure keeps in reserve (NV12ads) is not needed on AWS; the AWS node costs "
    f"{_usd(_h('g6.2xlarge') - 473.77)} a month more than Azure's. Whether each of the three AZs has g6 capacity is to "
    f"confirm before the HA node group is built.")

# **Disaster recovery on AWS is OPEN (CHG-R3-001).** AWS has one region in the UAE (me-central-1); Azure's DR region,
# UAE Central, has no AWS counterpart. Nothing here decides it: the LLD draws the DR box as "open" while this is None.
AWS_DR_DECISION = None
AWS_DR_OPTIONS = [
    # (option, what it is, residency, consequences)
    ("A. Multi-AZ only, backups in-region",
     "Everything in me-central-1 across three AZs; RDS automated backups and snapshots, AWS Backup vaults (a "
     "logically air-gapped vault included) and S3 copies all in me-central-1",
     "Keeps every store in the UAE (ADR-0009, the condition Qdrant was approved on)",
     "No region-level DR: a regional outage stops the cloud services until AWS restores the region (venues keep "
     "running on their edge nodes). RPO is the last in-region backup, RTO the region's recovery, with no bound we "
     "control. The cheapest; the tenant-selectable DR module of ADR-0060 has nowhere to go"),
    ("B. Cross-region to Bahrain (me-south-1)",
     "An RDS cross-region read replica or snapshot copies, S3 replication, and a standby EKS cell in me-south-1",
     "Breaks UAE residency: Bahrain is outside the UAE. Needs the client's (and, for regulated data, the "
     "regulator's) written acceptance, and reverses the basis Qdrant was approved on",
     "Real regional DR (RPO minutes with a replica, RTO hours with a rehearsed runbook), as Azure's UAE Central gives. "
     "Adds a second cell's cost and cross-region transfer (about $0.09 per GB out of me-central-1 to me-south-1)"),
    ("C. On-premises or another provider in the UAE",
     "A recovery site in the UAE outside AWS: the client's data centre, a UAE colocation, or Azure UAE North or "
     "Central as the DR side of an AWS primary",
     "Keeps every store in the UAE",
     "Cross-provider replication (PostgreSQL logical replication or dumps, S3 to Blob or object-store copies, Qdrant "
     "snapshots), two sets of tooling and skills, Internet egress at $0.117 per GB; the most work to build and "
     "rehearse"),
]
AWS_DR_OPEN = ("OPEN, not decided (CHG-R3-001). AWS has one region in the UAE (me-central-1, three AZs); Azure's DR "
               "region, UAE Central, has no AWS counterpart. The options and what each costs are below; the choice is "
               "Chinmay's and the client's, because two of the three trade residency or money against recovery.")

# Azure component -> AWS component, service for service (the HLD and the AWS LLD print this table).
AWS_MAP = [
    ("Azure Front Door Premium + WAF (waiting-room page from cache)",
     "Amazon CloudFront + AWS WAF (managed core rule set, Bot Control, rate-based rules); the waiting-room page from "
     "CloudFront's cache"),
    ("Internal load balancer + Private Link service; AKS App Routing (Gateway API)",
     "Internal Application Load Balancer (AWS Load Balancer Controller, Gateway API or Ingress), CloudFront VPC origin"),
    ("AKS, Standard tier: system, workload, AI GPU, qdrant and broker pools",
     "Amazon EKS: system, workload, AI GPU, qdrant and broker managed node groups, the same taints"),
    ("AKS AI GPU pool: NV6ads A10 v5 (1/6 A10, 4 GB)", "EKS GPU node group: g6.2xlarge (1 x L4, 24 GB)"),
    ("Azure Database for PostgreSQL Flexible Server 16, zone-redundant HA",
     "Amazon RDS for PostgreSQL 16, Multi-AZ DB instance (not Aurora)"),
    ("Read replicas x2, reporting replica, AI log DB",
     "RDS read replicas x2 (db.m6g.xlarge), a reporting replica (db.m6g.large), an AI log DB instance"),
    ("Azure Managed Redis (Balanced B10, HA)", "Amazon ElastiCache for Valkey (cache.r7g.large, primary + replica, Multi-AZ)"),
    ("Event broker self-run on the AKS broker pool (CloudAMQP recommended)",
     "Self-run on the EKS broker node group (RabbitMQ Cluster Operator), as on Azure; Amazon MQ for RabbitMQ the "
     "managed option"),
    ("Qdrant on the AKS qdrant pool, Premium SSD", "Qdrant on the EKS qdrant node group (r6i.xlarge), EBS gp3"),
    ("Managed Disks (Premium SSD)", "Amazon EBS gp3"),
    ("Blob storage (ZRS)", "Amazon S3 Standard (multi-AZ), S3 gateway endpoint"),
    ("Container Registry", "Amazon ECR"),
    ("Key Vault (secrets; Premium HSM keys for ADR-0063)",
     "AWS Secrets Manager + AWS KMS customer managed keys (HSM-backed; BYOK by import)"),
    ("NAT Gateway (one static egress IP)", "NAT Gateway, one per AZ, with Elastic IPs (three IPs to allow-list)"),
    ("Azure Bastion", "AWS Systems Manager Session Manager"),
    ("Private Link private endpoints + private DNS zones",
     "AWS PrivateLink interface VPC endpoints + Route 53 private hosted zones"),
    ("NSGs at the edges, Cilium network policy inside", "Security groups at the edges, Cilium (or VPC CNI) network policy inside"),
    ("VPN gateway in GatewaySubnet (dedicated-tier venues)", "AWS Site-to-Site VPN on a virtual private gateway or Transit Gateway"),
    ("Azure Monitor + Log Analytics", "Amazon CloudWatch (Logs, metrics, Container Insights)"),
    ("Microsoft Defender for Cloud", "Amazon GuardDuty (EKS Runtime, RDS Protection) + Amazon Inspector + AWS Security Hub"),
    ("Azure Backup", "AWS Backup (EBS snapshots); RDS automated backups and PITR"),
    ("Entra ID (administrators); managed identities (workload identity)",
     "IAM Identity Center (administrators); EKS Pod Identity (or IRSA) for workloads"),
    ("DR in UAE Central (ADR-0060)", "OPEN: AWS has one UAE region (see Disaster recovery)"),
]

# The VPC mirrors the Azure address plan: the same /16 and the same blocks, each split into one subnet per AZ
# (an AWS subnet lives in one AZ). A cell runs on one provider, so the range is reused; change it if an AWS cell
# and an Azure cell are ever peered. (name, block, per-AZ subnets a / b / c, holds, rule)
AWS_SUBNETS = [
    ("ingress", "10.20.0.0/24", "10.20.0.0/26, 10.20.0.64/26, 10.20.0.128/26",
     "Internal Application Load Balancer, CloudFront's VPC origin (snet-ingress)",
     "Security group: inbound 443 only from the CloudFront origin-facing prefix list"),
    ("public", "10.20.2.0/24", "10.20.2.0/26, 10.20.2.64/26, 10.20.2.128/26",
     "NAT Gateways and their Elastic IPs, nothing else (takes snet-agc's reserved block)",
     "Route to the Internet gateway; no instance, no load balancer"),
    ("eks-system", "10.20.4.0/22", "10.20.4.0/24, 10.20.5.0/24, 10.20.6.0/24",
     "EKS system node group and the ingress controller pods", "Egress through the NAT Gateway of its AZ"),
    ("eks-workload", "10.20.8.0/21", "10.20.8.0/23, 10.20.10.0/23, 10.20.12.0/23",
     "Workload node group: commerce, access, operations, workers",
     "Network policy: inbound from the ingress controller; egress through the NAT Gateway"),
    ("eks-ai", "10.20.16.0/22", "10.20.16.0/24, 10.20.17.0/24, 10.20.18.0/24",
     "AI GPU node group (the only AI group): ticvai-ai, BGE-M3 and its reranker, Presidio and the Arabic NER",
     "Network policy: inbound from the ingress controller and the workload group; read-only role on transactional "
     "schemas (ADR-0020, amended by ADR-0049)"),
    ("eks-data", "10.20.20.0/23", "10.20.20.0/25, 10.20.20.128/25, 10.20.21.0/25",
     "qdrant node group and, while the broker is self-run, the broker node group; both tainted ticvai.io/pool=data",
     "Network policy: inbound from the workload and AI groups only; Qdrant needs each tenant's collection-scoped JWT"),
    ("db", "10.20.24.0/24", "10.20.24.0/26, 10.20.24.64/26, 10.20.24.128/26",
     "RDS DB subnet group: the primary and its Multi-AZ standby, replicas, the AI log DB",
     "Security group: 5432 from the EKS node and pod security groups; not publicly accessible"),
    ("endpoints", "10.20.25.0/24", "10.20.25.0/26, 10.20.25.64/26, 10.20.25.128/26",
     "Interface VPC endpoints, the ElastiCache subnet group (and Amazon MQ if chosen)",
     "Security group: inbound from the EKS subnets only; private DNS on; no public endpoint"),
    ("(none: no Bastion)", "10.20.26.0/26", "-",
     "Not created: Session Manager reaches the nodes through the ssm endpoints or the NAT Gateway", "Reserved"),
    ("tgw-attach", "10.20.27.0/27", "10.20.27.0/28, 10.20.27.16/28 (a third /28 needs 10.20.27.32/28)",
     "Transit Gateway or VPN attachment for dedicated-tier venues' site-to-site VPN (GatewaySubnet)",
     "Created when a venue needs it"),
    ("pods (secondary CIDR)", "100.64.0.0/16", "100.64.0.0/18, 100.64.64.0/18, 100.64.128.0/18",
     "Pod addresses: VPC CNI custom networking, so pods do not use the node subnets (the CNI Overlay range on Azure)",
     "Must not overlap the client's ranges or a venue LAN on the VPN"),
    ("EKS services", "10.100.0.0/16", "-", "Kubernetes service range (service_ipv4_cidr)", "Internal only"),
]

AWS_LLD_NODES = {
    "users":   ("Users", ["B2C guests", "B2B partners", "Venue operators"], 30, 330, 150, 110, "#FFFFFF"),
    "fd":      ("CloudFront + AWS WAF", ["WAF: OWASP core + bot rules,", "rate rules per client IP", "on-sale waiting-room page",
                "TLS 1.2+, custom domains", "VPC origin to the ALB"], 220, 310, 190, 140, "#FFFFFF"),
    "ilb":     ("Ingress (internal ALB)", ["AWS Load Balancer Controller", "Gateway API / Ingress", "CloudFront VPC origin"],
                470, 330, 170, 110, "#FFF4E5"),
    "sys":     ("EKS system node group", ["m6i.xlarge, 2-4 nodes, AZs a-c", "+ ingress controller pods"], 690, 145, 190, 70, "#FFF4E5"),
    "wl":      ("EKS workload node group", ["m6i.2xlarge, 3-20 nodes, 3 AZs", "floors: commerce 3, access 2,", "operations 2, workers 2"],
                690, 227, 190, 90, "#FFF4E5"),
    "aip":     ("EKS AI GPU node group", ["g6.2xlarge x2 (L4), 1 an AZ", "tainted; ticvai-ai 2/1/0,", "BGE-M3, reranker, NER"],
                690, 329, 190, 90, "#FFF4E5"),
    "qdrant":  ("EKS qdrant node group", ["r6i.xlarge x3, one per AZ", "Qdrant, replication 2, TLS"], 690, 431, 190, 72, "#FFF4E5"),
    "broker":  ("EKS broker node group", ["m6i.large x3, while self-run;", "managed option: Amazon MQ", "for RabbitMQ, 3 nodes"],
                690, 515, 190, 90, "#FFF4E5"),
    "pg":      ("RDS for PostgreSQL 16", ["db.m6g.xlarge, Multi-AZ", "on every production tier", "control DB + DB per tenant",
                "PITR 35 days, UAE only"], 950, 150, 220, 110, "#FFFFFF"),
    "ro":      ("Read replicas x2", ["db.m6g.xlarge", "gate checks never read here"], 950, 280, 220, 70, "#FFFFFF"),
    "rpt":     ("Reporting + AI log DB", ["reporting replica (db.m6g.large)", "AI log DB (db.m6g.xlarge, 1 TB)"],
                950, 370, 220, 80, "#FFFFFF"),
    "pe":      ("VPC endpoints + services", ["ElastiCache Valkey r7g.large x2", "Secrets Manager, KMS", "S3 (gateway endpoint)",
                "ECR", "Amazon MQ, if chosen"], 950, 470, 220, 125, "#FFFFFF"),
    "bastion": ("SSM Session Manager", ["admin access only", "no SSH, no inbound port"], 470, 560, 170, 80, "#FFFFFF"),
    "nat":     ("NAT Gateway x3", ["one per AZ, Elastic IPs;", "the allow-listed egress"], 470, 700, 170, 80, "#FFFFFF"),
    "extp":    ("External providers", ["Payments, e-invoicing", "messaging, LLM providers"], 220, 700, 190, 80, "#FFFFFF"),
    "ops":     ("Operations", ["CloudWatch, AWS Backup", "GuardDuty, Security Hub", "Inspector, IAM Identity Ctr"],
                30, 560, 180, 100, "#FFFFFF"),
    "dr":      ("DR: OPEN (not decided)", ["one AWS region in the UAE;", "A in-region backups, B Bahrain", "(not UAE), C other provider"],
                950, 690, 230, 95, "#FFFFFF"),
    "venue":   ("Venue site", ["POS, kiosks, KDS", "venue edge node (offline)", "turnstiles, handhelds on LAN"], 1250, 300, 190, 110, "#FFFFFF"),
    "vpn":     ("Site-to-site VPN", ["dedicated tier: VGW or TGW;", "others: Internet + mTLS"], 1250, 450, 190, 80, "#FFFFFF"),
}
AWS_LLD_FRAMES = {"aks": ("EKS cluster", 670, 130, 230, 510)}
AWS_LLD_LINKS = LLD_LINKS  # the same lines between the same boxes; clouds_agree() holds the two drawings together


def clouds_agree():
    """The AWS cell against the Azure one (CHG-R3-001): the same boxes and lines in the LLD, the same cost groups on
    every sheet, every Azure service type mapped, every AWS price from AWS_RATE or said to be free or unpriced, and
    the AWS DR box open while no DR decision is recorded. Returns the disagreements (must be empty)."""
    bad = []
    if set(LLD_NODES) != set(AWS_LLD_NODES):
        bad.append(f"LLD boxes differ: Azure only {sorted(set(LLD_NODES) - set(AWS_LLD_NODES))}, "
                   f"AWS only {sorted(set(AWS_LLD_NODES) - set(LLD_NODES))}")
    if [(a, b, t) for a, b, t, _ in LLD_LINKS] != [(a, b, t) for a, b, t, _ in AWS_LLD_LINKS]:
        bad.append("LLD lines differ between Azure and AWS")
    norm = lambda rows: {g.replace("AKS", "EKS") for g, *_ in rows}
    for name, az, aw in [("with HA", PROD_HA, AWS_PROD_HA), ("without HA", PROD_NO_HA, AWS_PROD_NO_HA),
                         ("pre-production", PREPROD, AWS_PREPROD), ("Stage 1", STAGE_1, AWS_STAGE_1),
                         ("Stage 1 pre-production", STAGE_1_PREPROD, AWS_STAGE_1_PREPROD), ("Stage 0", STAGE_0, AWS_STAGE_0)]:
        if norm(az) - norm(aw):
            bad.append(f"{name}: cost groups on Azure with no AWS line: {sorted(norm(az) - norm(aw))}")
        for g, typ, desc, spec, qty, unit, _ in aw:
            if not unit and not re.search(r"usage|no charge|shared", f"{spec} {typ} {desc}", re.I):
                bad.append(f"{name}: AWS line '{desc}' has no price and does not say why")
    mapped = " ".join(a for a, _ in AWS_MAP)
    for typ in sorted({r[1] for r in PROD_HA if r[0] != "AI (usage)"}):
        key = {"Virtual Machines (AKS nodes)": "AKS", "Azure Kubernetes Service": "AKS",
               "Storage account (Blob, ZRS)": "Blob", "Azure Database for PostgreSQL": "PostgreSQL",
               "Private Link": "Private Link", "Bandwidth": "NAT Gateway",
               "Azure Monitor / Log Analytics": "Log Analytics"}.get(typ, typ)
        if key not in mapped:
            bad.append(f"AWS_MAP does not map the Azure service type {typ!r}")
    if AWS_DR_DECISION is None and "OPEN" not in AWS_LLD_NODES["dr"][0]:
        bad.append("AWS DR is not decided, but the AWS LLD's DR box does not say OPEN")
    return bad


NOTES_AWS_PROD = [
    "Prices: " + AWS_PRICE_SOURCE + " Savings Plans or reserved instances (1 or 3 years) lower compute by roughly "
    "30-60%; confirm each line in the AWS Pricing Calculator for me-central-1 before quoting.",
    "The same cell as the Azure sheets, service for service (the AWS LLD, TICVAI-LLD-AWS.md, has the mapping): the "
    "same five node groups and ADR-0061 floors, the same stores, the same entry. Region me-central-1 (Middle East, "
    "UAE), three AZs; every store stays in the UAE.",
    "Database: " + AWS_DB_CHOICE,
    "AI GPU node: " + AWS_GPU_CHOICE,
    "Disaster recovery on AWS is open (CHG-R3-001): AWS has one UAE region. The options (in-region backups only; "
    "Bahrain, which breaks UAE residency; another provider or on premises in the UAE) are in TICVAI-LLD-AWS.md. "
    "No DR cost is on these sheets.",
    "The broker matches the Azure choice: self-run on its own node group (the fallback the Terraform builds) until "
    "the client picks (ADR-0057, due 12 October). Amazon MQ for RabbitMQ is AWS's managed option (3 x mq.m7g.large, "
    f"{_usd(_h('mq-rabbit-3x'))} a month plus storage); CloudAMQP's availability in me-central-1 is to confirm.",
    "Differences that move the total: EKS has no free tier ($73 for every cluster, pre-production included); the "
    "NAT Gateway is zonal, so HA means three gateways and three egress IPs for the providers to allow-list; every "
    "EC2 node carries an EBS root volume; the AWS GPU node (a whole L4, 24 GB) costs more than Azure's A10 slice; "
    "the edge (CloudFront + WAF) and the security tooling (GuardDuty, Inspector, Security Hub) cost less than Front "
    "Door Premium and Defender for Cloud at these volumes.",
    "Not included: LLM tokens, SMS, email and WhatsApp fees, payment provider fees, the e-invoicing provider, DR "
    "(open), Apple and Google developer accounts, venue hardware, AWS Support plans (Business support is a "
    "percentage of the bill).",
    "To confirm (the price list does not settle them): " + "; ".join(AWS_TO_CONFIRM) + ".",
]
NOTES_AWS_NO_HA = [
    "Single AZ for everything except PostgreSQL, whose Multi-AZ standby stays (ADR-0060): an AZ outage stops the "
    "cloud services until they are restored; the database fails over. Venue gates and POS keep working on the venue "
    "edge node, offline. As on the Azure sheet, whether production may run this way is the client's answer to "
    "ADR-0060.",
]
NOTES_AWS_HA = [
    "AZs a-c in me-central-1: the PostgreSQL Multi-AZ standby (every production tier, ADR-0060), the Qdrant and "
    "broker three-node clusters, the EKS node groups across AZs, ElastiCache with a replica in another AZ, a NAT "
    "Gateway in each AZ. The shape of a shared cell and of a dedicated one.",
    "Availability targets per tier are the Azure sheet's (ADR-0060, proposed, with the client).",
]
NOTES_AWS_STAGES = [
    "Staged as on Azure (Chinmay, 4 October 2026, CHG-R11-003): launch on Stage 1, move to Stage 2 (the full cell on "
    "the other two sheets) on the same triggers as the Azure Stages sheet: a paying venue needing ADR-0060's targets, "
    "traffic beyond Stage 1 sustained, a large on-sale booked, or a client needing Bot Control or a private origin.",
    "Stage 1 on AWS differs from Azure's in three lines: the EKS control plane ($73; AKS Free on Azure), a NAT Gateway "
    "for the static egress IP (on Azure the load balancer's outbound rule carries it), and the GPU node (g6.2xlarge, a "
    "whole L4). WAF on CloudFront carries AWS's managed core rule set even at launch; Bot Control waits for Stage 2.",
    "Not included at Stage 1: GuardDuty, Inspector, Security Hub, VPC interface endpoints, ElastiCache, the AI log "
    "instance, read and reporting replicas: each comes with Stage 2. Session Manager has no charge line.",
    "Stage 0 is a reference line only (one m6i.4xlarge and the GPU node): it is not the plan. The 25 September AWS "
    "board's $716 for it included more than the instance.",
]
NOTES_AWS_PREPROD = NOTES_PREPROD


thin = Side(style="thin", color="999999")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HEAD_FILL = PatternFill("solid", fgColor="1F3056")
ENV_FILL = PatternFill("solid", fgColor="DCE6F5")
TOT_FILL = PatternFill("solid", fgColor="FFF3CC")
WRAP = Alignment(wrap_text=True, vertical="top")


TOTAL_ROWS = {}  # (sheet title, environment) -> the row of its "USD - Total cost per month" (the comparison sheet reads it)


def cost_block(ws, r, env, rows, notes, scaled_col=True, cloud=None):
    cloud = cloud or AZURE
    heads = ["Environment", "Group", f"{cloud['name']} service type", "Service description", "Region", "Specs description",
             "Qty", "Unit price (USD / month)", "Estimated monthly cost (USD)"]
    if scaled_col:
        heads.append("When solution is scaled up (USD)")
    for c, h in enumerate(heads, 1):
        cell = ws.cell(r, c, h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = HEAD_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = BORDER
    first = r + 1
    for i, (grp, typ, desc, spec, qty, unit, sq) in enumerate(rows):
        rr = first + i
        region = cloud["global_region"] if typ in cloud["global_types"] else cloud["region"]
        vals = [env if i == 0 else None, grp, typ, desc, region, spec, qty, unit]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(rr, c, v)
            cell.alignment = WRAP
            cell.border = BORDER
        ws.cell(rr, 9, f"=G{rr}*H{rr}").number_format = "#,##0"
        ws.cell(rr, 9).border = BORDER
        ws.cell(rr, 8).number_format = "#,##0.##"
        if scaled_col:
            ws.cell(rr, 10, f"={sq}*H{rr}" if sq else f"=I{rr}").number_format = "#,##0"
            ws.cell(rr, 10).border = BORDER
    last = first + len(rows) - 1
    ws.merge_cells(start_row=first, start_column=1, end_row=last, end_column=1)
    envc = ws.cell(first, 1)
    envc.fill = ENV_FILL
    envc.font = Font(bold=True, size=12)
    envc.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
    r = last + 1
    TOTAL_ROWS[(ws.title, env)] = r
    totals = [("USD - Total cost per month", f"=SUM(I{first}:I{last})", f"=SUM(J{first}:J{last})"),
              ("AED - Total cost per month", f"=I{r}*$C$3", f"=J{r}*$C$3"),
              ("AED - Total cost per year", f"=I{r+1}*12", None),
              ("AED - Total price per year with margin", f"=I{r+2}*(1+$C$4)", None)]
    for j, (label, f1, f2) in enumerate(totals):
        ws.cell(r + j, 6, label).font = Font(bold=True)
        ws.cell(r + j, 6).alignment = Alignment(horizontal="right")
        c = ws.cell(r + j, 9, f1)
        c.number_format = "#,##0"
        c.font = Font(bold=True)
        c.fill = TOT_FILL
        if scaled_col and f2:
            c2 = ws.cell(r + j, 10, f2)
            c2.number_format = "#,##0"
            c2.fill = TOT_FILL
    r += len(totals) + 1
    ws.cell(r, 2, f"Notes - {env}").font = Font(bold=True)
    for n in notes:
        r += 1
        ws.cell(r, 2, n).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=9)
        ws.row_dimensions[r].height = 32
    return r + 3


def _sheet_head(ws, title, prices):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=14)
    ws["B3"], ws["C3"] = "AED per USD", AED
    ws["B4"], ws["C4"] = "Margin", MARGIN
    ws["C4"].number_format = "0%"
    ws["D3"] = "Edit the rate, the margin and any unit price; every total is a formula."
    ws["D4"] = prices


def cost_sheet(wb, title, prod_rows, prod_notes, cloud=None):
    cloud = cloud or AZURE
    ws = wb.create_sheet(title)
    _sheet_head(ws, f"TICVAI - {cloud['name']} cloud specs and cost ({title.lower()})", "Prices: " + cloud["price_source"])
    r = cost_block(ws, 6, "Production", prod_rows, cloud["notes_prod"] + prod_notes, cloud=cloud)
    cost_block(ws, r, "Pre-production", cloud["preprod"], cloud["notes_preprod"], cloud=cloud)
    widths = [16, 16, 26, 38, 11, 46, 6, 14, 16, 18]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A7"
    return ws


def stages_sheet(wb, cloud=None):
    """Stage 1 (launch), its pre-production, and Stage 0 for reference (CHG-R11-003)."""
    cloud = cloud or AZURE
    ws = wb.create_sheet("Stages")
    _sheet_head(ws, f"TICVAI - {cloud['name']} cloud specs and cost, staged (Stage 1 launch; Stage 2 = the full cell sheets)",
                cloud["stage_prices"])
    r = cost_block(ws, 6, "Stage 1 production (launch)", cloud["stage_1"], cloud["notes_stages"], scaled_col=False, cloud=cloud)
    r = cost_block(ws, r, "Stage 1 pre-production", cloud["stage_1_pre"], [], scaled_col=False, cloud=cloud)
    cost_block(ws, r, "Stage 0 (reference only)", cloud["stage_0"], [], scaled_col=False, cloud=cloud)
    widths = [16, 16, 26, 38, 11, 46, 6, 14, 16]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A7"
    return ws


def _plain_sheet(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows():
        for c in row:
            c.alignment = WRAP
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = HEAD_FILL


def compare_sheet(wb):
    """Azure against AWS (CHG-R3-001): the AWS figures are formulas on this workbook's own totals; the Azure ones are
    the Azure workbook's totals as generated (a separate file, so values)."""
    ws = wb.create_sheet("Azure vs AWS")
    _sheet_head(ws, "TICVAI - Azure UAE North against AWS me-central-1 (USD a month, production unless said)",
                "Azure: " + PRICE_SOURCE + " AWS: " + AWS_PRICE_SOURCE)
    heads = ["Line", "Azure UAE North (USD / month)", "AWS me-central-1 (USD / month)", "AWS - Azure (USD)",
             "AWS against Azure", "Azure (AED / month)", "AWS (AED / month)", "AWS (AED a year with margin)"]
    for c, h in enumerate(heads, 1):
        cell = ws.cell(6, c, h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = HEAD_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = BORDER
    t = lambda sheet, env: f"='{sheet}'!I{TOTAL_ROWS[(sheet, env)]}"
    lines = [
        ("Stage 1 production (launch)", month(STAGE_1), t("Stages", "Stage 1 production (launch)")),
        ("Stage 1 pre-production", month(STAGE_1_PREPROD), t("Stages", "Stage 1 pre-production")),
        ("Stage 1 in all", month(STAGE_1) + month(STAGE_1_PREPROD), "=C7+C8"),
        ("Full cell (Stage 2) without zone-level HA", month(PROD_NO_HA), t("Infra without HA", "Production")),
        ("Full cell (Stage 2) with high availability", month(PROD_HA), t("Infra with High Availability", "Production")),
        ("Pre-production beside the full cell", month(PREPROD), t("Infra with High Availability", "Pre-production")),
        ("Stage 0 (reference only)", month(STAGE_0), t("Stages", "Stage 0 (reference only)")),
    ]
    for i, (label, az, aw) in enumerate(lines):
        r = 7 + i
        vals = [label, round(az, 2), aw, f"=C{r}-B{r}", f"=C{r}/B{r}-1", f"=B{r}*$C$3", f"=C{r}*$C$3",
                f"=G{r}*12*(1+$C$4)"]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(r, c, v)
            cell.border = BORDER
            cell.alignment = WRAP
            cell.number_format = "+0.0%;-0.0%" if c == 5 else "#,##0.00"
    r = 7 + len(lines) + 1
    ws.cell(r, 1, "Notes").font = Font(bold=True)
    for n in [
        "The same cell on both clouds, service for service (TICVAI-LLD-AWS.md has the mapping). The AWS column is a "
        "formula on this workbook's sheets, so it follows any unit price edited there; the Azure column is the Azure "
        "workbook's totals as generated on " + AWS_DATE + ".",
        "Where AWS costs more: the EKS control plane at every stage (no free tier), the GPU node (a whole L4 with 24 GB "
        "against Azure's 4 GB A10 slice), three NAT Gateways for HA, EBS root volumes on every node, PrivateLink "
        "endpoints per AZ. Where it costs less: the edge (CloudFront + WAF against Front Door Premium), the security "
        "tooling (GuardDuty, Inspector, Security Hub against Defender for Cloud), Bastion (Session Manager has no "
        "charge line), the cache and the read replicas.",
        "Disaster recovery is not in either column: Azure's DR module (UAE Central) is bought per tenant, and on AWS DR "
        "is open (one AWS region in the UAE; see TICVAI-LLD-AWS.md).",
        "On-demand list prices on both sides; reserved capacity or savings plans move both by a similar 30-60% on "
        "compute.",
    ]:
        r += 1
        ws.cell(r, 1, n).alignment = WRAP
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
        ws.row_dimensions[r].height = 45
    for i, w in enumerate([44, 18, 18, 16, 14, 16, 16, 20], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A7"
    return ws


def build_workbook(path, cloud=None):
    cloud = cloud or AZURE
    wb = Workbook()
    wb.remove(wb.active)
    stages_sheet(wb, cloud)
    cost_sheet(wb, "Infra without HA", cloud["no_ha"], cloud["no_ha_notes"], cloud)
    cost_sheet(wb, "Infra with High Availability", cloud["ha"], cloud["ha_notes"], cloud)
    ws = wb.create_sheet("Deployables")
    ws.append(["Deployable", "What it is", "Modules", "Runs on", "Replica floor (ADR-0061)"])
    runs = cloud["runs"]
    floor_text = {}
    for unit, dep, f, why in FLOORS:
        floor_text.setdefault(dep, []).append((unit, f, why))
    for k, v in DEPLOYABLES.items():
        fl = floor_text.get(k, [])
        ft = (f"{fl[0][1]}: {fl[0][2]}" if len(fl) == 1 else
              f"{sum(f for _, f, _ in fl)}: " + "; ".join(f"{u} {f}" for u, f, _ in fl) + " (real-time 3 in a large cell)")
        ws.append([k, v, ", ".join(sorted(MODULES.get(k, []))) or "-", runs.get(k, ""), ft])
    ws.append(["Total at the floor", "", "", "", f"{FLOOR_TOTAL} a cell; {FLOOR_TOTAL + 1} in a large cell"])
    ws.append([])
    ws.append(["Data stores", "", "", "", ""])
    for row in cloud["stores"]:
        ws.append(list(row))
    _plain_sheet(ws, [18, 70, 60, 34, 40])
    ws = wb.create_sheet("Network")
    ws.append(cloud["net_head"])
    for row in cloud["net_rows"]:
        ws.append(list(row))
    _plain_sheet(ws, cloud["net_widths"])
    if cloud["name"] == "AWS":
        ws = wb.create_sheet("Service map")
        ws.append(["Azure (UAE North)", "AWS (me-central-1, UAE)"])
        for a, b in AWS_MAP:
            ws.append([a, b])
        _plain_sheet(ws, [60, 80])
        ws = wb.create_sheet("DR (open)")
        ws.append(["Option", "What it is", "UAE residency", "Consequences"])
        for row in AWS_DR_OPTIONS:
            ws.append(list(row))
        ws.append(["Status", AWS_DR_OPEN, "", ""])
        _plain_sheet(ws, [30, 60, 50, 70])
        ws = wb.create_sheet("AWS rates")
        ws.append(["Key", "USD", "Per", "What", "Offer file and its publication date"])
        for k, (usd, per, what, src) in AWS_RATE.items():
            ws.append([k, usd, per, what, src])
        ws.append([])
        ws.append(["To confirm", "", "", "; ".join(AWS_TO_CONFIRM), AWS_PRICE_SOURCE])
        _plain_sheet(ws, [20, 12, 20, 70, 40])
        compare_sheet(wb)
    wb.calculation.fullCalcOnLoad = True  # the totals are formulas; Excel computes them on open
    wb.save(path)


AZURE = dict(
    name="Azure", region="UAE North", global_region="Global", global_types={"Azure Front Door"},
    price_source=PRICE_SOURCE, notes_prod=NOTES_PROD, preprod=PREPROD, notes_preprod=NOTES_PREPROD,
    stage_prices="Prices: per line, the workbook's own unit price or the Azure Retail Prices API read on 4 October 2026.",
    stage_1=STAGE_1, stage_1_pre=STAGE_1_PREPROD, stage_0=STAGE_0, notes_stages=NOTES_STAGES,
    no_ha=PROD_NO_HA, no_ha_notes=NOTES_NO_HA, ha=PROD_HA, ha_notes=[
        "Zones 1-3 in UAE North: PostgreSQL zone-redundant standby (on every production tier, ADR-0060), Qdrant "
        "and broker three-node clusters, AKS node pools across zones, Azure Managed Redis with high availability "
        "(zone-redundant). This is the shape of a shared cell and of a dedicated one.",
        "Availability targets per tier (ADR-0060, proposed, with the client): 99.99% for venue operations "
        "(gate, POS, KDS) measured locally; 99.95% for commerce in the cloud; 99.9% for back office and "
        "operations; 99.5% for AI and engagement. Only an active-active, two-region design reaches 99.99% for "
        "the whole cloud path."],
    runs={"commerce": "Workload pool", "access": "Workload pool (and the venue edge node)",
          "operations": "Workload pool", "ticvai-ai": "AI GPU pool (tainted)", "workers": "Workload pool"},
    stores=[("PostgreSQL 16", "Control DB and one database per tenant, zone-redundant on every production tier "
             "(ADR-0060); read replicas; reporting replica; AI log DB", "", "Flexible Server", ""),
            ("Qdrant", "Vectors; one collection per tenant, collection-scoped JWT (ADR-0049)", "", "qdrant pool", ""),
            ("Redis", "Sessions, idempotency, per-tenant request budgets (ADR-0064), waiting-room positions "
             "(ADR-0066), the one-second browse cache (ADR-0065, proposed)", "", "Azure Managed Redis", ""),
            ("Event broker", "RabbitMQ recommended (CloudAMQP, UAE North) or Kafka, the client's choice by 12 "
             "October (ADR-0057); outbox relay per region in workers (ADR-0058, amended 1 October)", "",
             "broker pool while self-run; Private Link if managed", ""),
            ("Blob storage", "Media (including venue 3D models and navigation files, ADR-0069), exports, "
             "snapshots, dumps", "", "Storage account", "")],
    net_head=["Subnet", "Address range", "Holds", "Rule"],
    net_rows=list(SUBNETS) + [
        ("AKS pod range (CNI Overlay)", POD_CIDR, "Pod addresses, outside the VNet (Terraform default)",
         "Must not overlap a peered VNet, the client's ranges or a venue LAN on the VPN; 100.64.0.0/16 if in doubt"),
        ("AKS service range", AKS_SERVICE_CIDR, "Kubernetes services (Terraform default)", "Internal only")],
    net_widths=[24, 16, 60, 70],
)
AWS = dict(
    name="AWS", region="me-central-1 (UAE)", global_region="Global (edge)", global_types={"Amazon CloudFront", "AWS WAF"},
    price_source=AWS_PRICE_SOURCE, notes_prod=NOTES_AWS_PROD, preprod=AWS_PREPROD, notes_preprod=NOTES_AWS_PREPROD,
    stage_prices="Prices: per line, from the AWS Price List API (me-central-1) pulled 4 October 2026; the AWS rates sheet "
                 "has each rate and its file.",
    stage_1=AWS_STAGE_1, stage_1_pre=AWS_STAGE_1_PREPROD, stage_0=AWS_STAGE_0, notes_stages=NOTES_AWS_STAGES,
    no_ha=AWS_PROD_NO_HA, no_ha_notes=NOTES_AWS_NO_HA, ha=AWS_PROD_HA, ha_notes=NOTES_AWS_HA,
    runs={"commerce": "Workload node group", "access": "Workload node group (and the venue edge node)",
          "operations": "Workload node group", "ticvai-ai": "AI GPU node group (tainted)",
          "workers": "Workload node group"},
    stores=[("PostgreSQL 16", "Control DB and one database per tenant, Multi-AZ on every production tier (ADR-0060); "
             "read replicas; reporting replica; AI log DB", "", "Amazon RDS for PostgreSQL (not Aurora)", ""),
            ("Qdrant", "Vectors; one collection per tenant, collection-scoped JWT (ADR-0049)", "", "qdrant node group", ""),
            ("Redis", "Sessions, idempotency, per-tenant request budgets (ADR-0064), waiting-room positions "
             "(ADR-0066), the one-second browse cache (ADR-0065, proposed)", "", "Amazon ElastiCache for Valkey", ""),
            ("Event broker", "RabbitMQ recommended or Kafka, the client's choice by 12 October (ADR-0057); outbox relay "
             "per region in workers (ADR-0058, amended 1 October)", "",
             "broker node group while self-run; Amazon MQ for RabbitMQ if managed", ""),
            ("Object storage", "Media (including venue 3D models and navigation files, ADR-0069), exports, "
             "snapshots, dumps", "", "Amazon S3", "")],
    net_head=["Subnet", "Block", "Per-AZ subnets (a, b, c)", "Holds", "Rule"],
    net_rows=AWS_SUBNETS,
    net_widths=[22, 16, 40, 60, 60],
)


# ---------------------------------------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------------------------------------
def month(rows):
    return sum(r[4] * r[5] for r in rows)


def floor_cell(dep):
    fl = [(u, f) for u, d, f, _ in FLOORS if d == dep]
    if len(fl) == 1:
        return str(fl[0][1])
    return f"{sum(f for _, f in fl)}: " + ", ".join(f"{u} {f}" for u, f in fl) + " (real-time 3 in a large cell)"


def hld_md():
    rows = "\n".join(f"| **{k}** | {v} | {', '.join(sorted(MODULES.get(k, []))) or '-'} | {floor_cell(k)} |"
                     for k, v in DEPLOYABLES.items())
    links = "\n".join(f"| {HLD_NODES[a][0]} | {HLD_NODES[b][0]} | {' and '.join(LINK[k][0] for k in t.split('+'))} |"
                      for a, b, t, _ in HLD_LINKS)
    aws_map = "\n".join(f"| {a} | {b} |" for a, b in AWS_MAP)
    return f"""# TICVAI platform: high-level design

> **Date:** {DATE} · **Generated by** `tools/build-hld-lld.py` · **Diagram:** [`TICVAI-HLD.svg`](TICVAI-HLD.svg)
> **Follows** the classic HLD format supplied on 30 September: the cloud, the venue site and the outside world as
> boxes, and every line typed by how the two ends talk.
> **Rechecked 1 October** against the ADRs accepted or amended that day (0058 amended, 0060 to 0068) and the
> Terraform cell module. The generator stops if the address plan, the replica floors, the node pools or the
> PostgreSQL HA mode disagree with the Terraform.

![TICVAI HLD](TICVAI-HLD.svg)

## The shape in one paragraph

One cell per region, in Azure UAE North or, the same cell service for service, in AWS me-central-1 (UAE; see
"On AWS" below and [`TICVAI-LLD-AWS.md`](TICVAI-LLD-AWS.md)). Inside it, 17 modules in one .NET solution run as five deployables
(ADR-0055), each with a replica floor that survives the loss of one zone (ADR-0061): {FLOOR_TOTAL} replicas a cell,
{FLOOR_TOTAL + 1} in a large one. Each tenant has its own PostgreSQL database and its own Qdrant collection (ADR-0038,
amended by ADR-0040 on instance count; ADR-0049). Modules in different deployables talk through events on the
broker, written first to an outbox in the same transaction (ADR-0033, amended by ADR-0058). Everything enters
through Front Door, where the on-sale waiting room also sits (ADR-0066). At each venue an edge node runs the gates
and the POS on its own when the Internet is down (ADR-0013), and syncs when it is back.

## Deployables

| Deployable | What it is | Modules | Replica floor (ADR-0061) |
|---|---|---|---|
{rows}

Above its floor each deployable autoscales on requests per second (ADR-0032, amended by ADR-0038 and ADR-0064), with no maximum. The floors are
`replica_floors` in the Terraform cell module (an output the bootstrap Helm values read), `x-ticvai-replica-floors`
in `deploy/a-independent-tenant.yml` and `deploy/b-shared-platform.yml`, and `DEPLOYABLE_FLOORS` in
`tools/derive-sizing.py`. A flash-sale burst environment does not use them: its floor is the expected peak
(ADR-0035, amended 3 September).

## Data stores

| Store | Holds | Decision |
|---|---|---|
| PostgreSQL 16 | A control database, one database per tenant, read replicas, a reporting replica and the AI log database. The primary has a zone-redundant standby on every production tier, the shared cell included | ADR-0038 (amended by ADR-0040), ADR-0056 (UUIDv7 ids, monthly partitions), ADR-0060 (zone-redundant HA decided by Chinmay on 1 October; the rest of ADR-0060 is proposed) |
| Qdrant | The AI knowledge index: one collection per tenant, each with its own collection-scoped key; venue scope is a filter the retrieval client always adds | ADR-0049 (approved 30 September on condition of UAE hosting) |
| Azure Managed Redis | Sessions, idempotency keys, per-tenant request budgets, waiting-room positions, the one-second browse availability cache (not Azure Cache for Redis, which is retiring) | ADR-0032 (amended 30 September for the product, and by ADR-0064), ADR-0064, ADR-0065 (proposed), ADR-0066 |
| Event broker | Events between deployables. **RabbitMQ is recommended, run by CloudAMQP in UAE North** (three nodes, Private Link); Kafka on Event Hubs is the alternative. The client chooses by Monday 12 October | ADR-0057 (proposed), ADR-0058 (amended 1 October); `docs/active/broker-decision-pack.md` |
| Blob storage | Media (including each venue's 3D model and navigation file), exports, Qdrant snapshots, database dumps | ADR-0047, ADR-0069 |

## On the request path

- **One entry.** Front Door Premium with WAF: OWASP and bot rules, and rate rules per client IP against abuse.
- **The on-sale waiting room sits at the edge, apart from the ride queue** (ADR-0066, amended ADR-0012's Q2). The
  waiting page is static and served from Front Door's cache; a guest's position comes from a Redis counter (no
  database write); a release controller admits guests per second from the health of `commerce` (latency and 429
  rate). An admitted guest gets a short-lived signed admission token (the signing key is a Key Vault secret).
  **Only online cart holds need it**: `addCartLine` forwards it and `acquireInventoryHold` checks the signature in
  middleware, with no database read, for a `cart` hold on a performance whose room is on. A `workstation` hold (a
  till, a kiosk, an edge node) is not behind the room. The endpoints (`enterWaitingRoom`,
  `getWaitingRoomPosition`, and `getWaitingRoomStatus`, `setWaitingRoomSetting` for operators) are Catalogue's, in
  `commerce`. A vendor room (for example Queue-it) stays the fallback, and the client's decision.
- **Browse availability is read from a cache at most about one second old** (ADR-0065, **proposed**, waiting on
  Chinmay because it reverses F01/F07's "never cached"): key per tenant, performance and channel in Redis, one
  recompute per key per second, `asOf` on the response. The hold on the primary stays the only correctness check.
- **Every tenant has a request budget** (ADR-0064): a token bucket per tenant and audience in the kernel middleware
  of `commerce`, `access` and `operations`, counted in Redis so every replica agrees; a share of in-flight work per
  tenant enforced only above 70% of a replica's limit. Every operation declares `429` with `Retry-After` and the
  `RateLimit-*` headers. Front Door's per-IP rules are the outer layer for abuse, not the fairness model.
- **Events.** One relay per region, in `workers`, drains each tenant database's outbox and publishes in batches
  (`Relay:BatchSize` 200 in the shared cells, 1,000 in a burst environment); every consumer records what it handled
  in its tenant database's inbox, so the effect happens once (ADR-0058, amended 1 October). The LLD has the detail.

## Connections

| From | To | How |
|---|---|---|
{links}

## At the venue

- **Onsite sales:** POS terminals and kiosks call the device API over the Internet; the kitchen display takes
  orders from the POS on the venue network. Offline, the POS keeps selling and syncs later.
- **One device register** (ADR-0067): every POS, kiosk, KDS, turnstile and handheld is registered once in
  `platform.device` (Tenancy, in `commerce`), with its versions, health and one lifecycle. Access keeps only where
  a device is placed (`access.device_placement`). Heartbeats have one path.
- **Access control:** turnstiles and handhelds talk to the venue edge node on the venue network or Wi-Fi. The
  edge node holds the offline package: the valid entitlements and **the active guest admission policy version**,
  because guest admission policy lives in Access only and the gate offline evaluates the same version as
  `validateAccess` online (ADR-0068). It decides in under 300 ms, records the policy version on each scan, and
  syncs scans to the cloud as soon as it can.
- **In-park 3D navigation** (ADR-0069): the guest app draws the venue from a GLB model and routes on a pathway and
  location file with GPS. Both are stored per venue in the platform's asset store, in the tenant's region (UAE
  North for a UAE tenant), and delivered through Front Door with the asset module's rules. No asset goes to a
  third-party map service.

## Outside the cloud

- **Payments** are called by `commerce` over HTTPS.
- **E-invoicing** goes through a provider adapter (ADR-0062, **proposed**: the client names the accredited provider,
  the mandate date and the B2C scope). `issueTaxInvoice` and `issueCreditMemo` write the document and an outbox
  row; a job in `workers` transmits over HTTP through the NAT Gateway's static IP; a business rejection stops for
  a person; the provider's callback comes in on its own authenticated endpoint.
- **Messaging** (email, SMS, WhatsApp, push) is sent by jobs in `workers`, also through the NAT Gateway.

## What this does not show

Per-screen flows (see `diagrams/lld/`), the AI internals (`docs/architecture/ai-system-design.md`) and sizing
(`handoff/sizing.json`). The Azure network, security, availability and cost are in [`TICVAI-LLD.md`](TICVAI-LLD.md)
and the Azure cost workbook; the AWS ones in [`TICVAI-LLD-AWS.md`](TICVAI-LLD-AWS.md) and the AWS cost workbook.

## On AWS (me-central-1)

Added {AWS_DATE} (CHG-R3-001; Chinmay: "HLD and LLD you didnt add AWS you just did azure add that in as well"). The
cell above runs on AWS in me-central-1 (Middle East, UAE, three AZs) with the same deployables, floors, stores and
lines; only the services under them change. **Disaster recovery on AWS is open**: AWS has one region in the UAE
(see [`TICVAI-LLD-AWS.md`](TICVAI-LLD-AWS.md)).

| Azure (UAE North) | AWS (me-central-1) |
|---|---|
{aws_map}

Monthly, production, on-demand: Stage 1 **${month(AWS_STAGE_1):,.2f}** on AWS against ${month(STAGE_1):,.2f} on Azure;
the full cell **${month(AWS_PROD_NO_HA):,.2f}** without zone-level HA (Azure ${month(PROD_NO_HA):,.2f}) and
**${month(AWS_PROD_HA):,.2f}** with it (Azure ${month(PROD_HA):,.2f}). The AWS workbook has the lines and an Azure-vs-AWS sheet.
"""


def lld_md():
    sn = "\n".join(f"| `{a}` | {b} | {c} | {d} |" for a, b, c, d in SUBNETS)
    fl = "\n".join(f"| `{u}` | `{d}` | {f} | {w} |" for u, d, f, w in FLOORS)
    ha, noha, pre = month(PROD_HA), month(PROD_NO_HA), month(PREPROD)
    return f"""# TICVAI platform: low-level design (Azure)

> **Date:** {DATE} · **Generated by** `tools/build-hld-lld.py` · **Diagram:** [`TICVAI-LLD.svg`](TICVAI-LLD.svg)
> **Costs:** [`TICVAI - Azure Cloud Specs & Cost.xlsx`](TICVAI%20-%20Azure%20Cloud%20Specs%20%26%20Cost.xlsx): production with high availability
> **${ha:,.2f}** a month, without zone-level HA **${noha:,.2f}**, pre-production **${pre:,.2f}** (prices of 30 September);
> **staged** (CHG-R11-003): launch on Stage 1 at **${month(STAGE_1):,.2f}** a month in production plus **${month(STAGE_1_PREPROD):,.2f}** of
> pre-production; the figures before it are Stage 2, the full cell
> **Source of sizes:** the Terraform cell module (`repos/ticvai-infra/terraform/modules/cell`), `handoff/sizing.json`,
> the decisions of 30 September and the ADRs of 1 October. The generator checks the Terraform before it writes.
> **AWS:** the same cell, service for service, on AWS me-central-1 (UAE): [`TICVAI-LLD-AWS.md`](TICVAI-LLD-AWS.md) and
> its own cost workbook (CHG-R3-001, {AWS_DATE})

![TICVAI LLD](TICVAI-LLD.svg)

## Region and residency

- **Region:** Azure UAE North, availability zones 1-3. **Every store stays in the UAE**, including backups,
  snapshots and disaster recovery: the condition Qdrant was approved on (30 September) and ADR-0009 (section 2
  amended by ADR-0049).
- **Disaster recovery is in UAE Central** (ADR-0060): the in-country pair for geo-redundant backup, and the region
  of the tenant-selectable DR module. UAE Central is access-restricted (a support request is needed) and has no
  zone-redundant HA.
- **One cell per region.** A cell serves many tenants; each tenant has its own PostgreSQL database and its own
  Qdrant collection.

## Tiers

| Tier | What runs there | Size (production, with HA) |
|---|---|---|
| Edge | Azure Front Door Premium with WAF (OWASP and bot rules, rate rules per client IP), TLS 1.2+, Private Link to the origin. Serves the on-sale waiting-room page from its cache (ADR-0066) | One profile |
| Ingress | A Gateway API ingress: the AKS App Routing add-on's Gateway API implementation behind an internal load balancer, published to Front Door by Private Link. Not NGINX (ingress-nginx is out of maintenance; the add-on's NGINX is supported only through November 2026). Application Gateway for Containers is the alternative, with `snet-agc` reserved. Installed at bootstrap, not by the Terraform | In the system pool; the gateway pods tolerate its `CriticalAddonsOnly` taint |
| AKS cluster | Azure CNI Overlay (pods from `{POD_CIDR}`, outside the VNet), Cilium network policy and data plane, egress through the NAT Gateway (`userAssignedNATGateway`), five node pools, a subnet per pool (the qdrant and broker pools share `snet-aks-data`) | Standard tier |
| AKS system pool | Kubernetes system services, the ingress gateway | D4s v5, autoscale 2-4 nodes, zones 1-3 |
| AKS workload pool | `commerce`, `access`, `operations`, `workers`: floors 3, 2, 2 and 2 | D8s v5, autoscale 3-20 nodes, zones 1-3 |
| AKS AI GPU pool | The only AI pool (CHG-R11-001): `ticvai-ai` (real-time 2, 3 in a large cell; interactive 1; batch 0; about 1 vCPU a pod), Presidio, and on the GPU BGE-M3, its reranker and the Arabic NER; never an LLM; tainted `ticvai.io/pool=ai` | NV6ads A10 v5 (6 vCPU, 55 GB, 1/6 A10 with 4 GB): 2 nodes, one per zone (1 without HA); step up to NV12ads A10 v5 on CPU or GPU memory pressure |
| AKS qdrant pool | Qdrant 1.16 or later, open source, official Helm chart: 3 nodes, one per zone, replication factor 2, TLS on the service; tainted `ticvai.io/pool=data` | E4s v5 x3, Premium SSD P15 256 GB each |
| AKS broker pool | The broker while it is self-run: RabbitMQ on the Cluster Operator, 3 nodes, quorum queues on persistent disks; tainted `ticvai.io/pool=data`. Not built (`broker_self_hosted = false`) if the client takes the recommended CloudAMQP | D2s v5 x3, Premium SSD P10 128 GB each |
| Database | PostgreSQL Flexible Server 16: primary with a zone-redundant standby on every production tier, the shared cell included (ADR-0060, decided 1 October); 2 read replicas; a reporting replica; the AI log database (a server of its own, ADR-0020 as amended by ADR-0049; not yet in the Terraform cell module) | General Purpose D4ds v5, 256 GB each; reporting D2ds v5; AI log D4ds v5 with 1 TB |
| Private endpoints | Azure Managed Redis Balanced B10 (12 GB), zone-redundant; Key Vault; Blob storage (ZRS); Container Registry; the managed broker's Private Link if one is chosen | Public access disabled |

## Replica floors (ADR-0061, accepted 1 October)

| Unit | Deployable | Floor | Why |
|---|---|---:|---|
{fl}
| **Total** | | **{FLOOR_TOTAL}** | {FLOOR_TOTAL + 1} in a large cell |

A floor is survivability, not load: enough replicas to lose one zone and keep serving. It is each Deployment's
`minReplicas`, from the Terraform output `replica_floors`; above it each unit autoscales on requests per second
(ADR-0032, amended by ADR-0038 and ADR-0064), with no maximum. **The node counts carry the floors:** three workload nodes hold the nine .NET floor
replicas, one `commerce` replica per zone; two AI GPU nodes hold the three AI floor pods beside Presidio,
BGE-M3, its reranker and the Arabic NER, and a large cell's third real-time pod fits on them. Pod sizes are
assumptions (about 1 vCPU for a .NET replica, about 1 vCPU for an AI pod) until `tools/bench.py` measures them in
sprint 2.

## Network

VNet `10.20.0.0/16` (proposed; confirm against the client's address plan before the first deploy).

| Subnet | Range | Holds | Rule |
|---|---|---|---|
{sn}
| AKS pods (CNI Overlay) | `{POD_CIDR}` | Pod range, outside the VNet (Terraform default) | Must not overlap a peered VNet, the client's ranges or a venue LAN on the VPN; `100.64.0.0/16` if in doubt |
| AKS services | `{AKS_SERVICE_CIDR}` | Kubernetes service range (Terraform default) | Internal only |

The Terraform cell module builds this plan (`network.tf`, `address_plan` in `variables.tf`); the two reserved
ranges (`snet-agc`, `snet-jump`) are not created until they are needed.

- **Inbound:** only through Front Door (web, apps, APIs, venue devices) and Bastion (administrators). No
  resource has a public database, cache or storage endpoint.
- **Outbound:** through the NAT Gateway's one static IP, which payment, e-invoicing and messaging providers can
  allow-list. AKS uses it as its outbound type (`userAssignedNATGateway`), and the NAT Gateway is attached to every
  node subnet.
- **NSGs at the edges, Cilium inside.** NSGs guard the ingress, PostgreSQL and private-endpoint subnets. The
  rules between AKS pools (workload to broker, AI to Qdrant) are Cilium network policies: the ingress gateway
  and CoreDNS run on the system pool and must reach every node, which subnet-to-subnet NSGs would block.
- **Venues:** devices reach the cloud over the Internet with TLS and device certificates; a dedicated-tier
  tenant may add a site-to-site VPN, whose gateway goes in `GatewaySubnet`. Turnstiles and handhelds only talk
  to the venue edge node.
- **Front Door is global.** It holds no personal data: it caches only public content (the waiting-room page,
  public media such as the venue 3D models) and decrypts at the edge location nearest the user (normally in the
  UAE for UAE users, not guaranteed): data in transit only. Its WAF logs stay in the UAE North workspace.

## Request path and limits

- **Waiting room** (ADR-0066): positions in Redis, the page from Front Door's cache, a release controller paced
  on `commerce`'s latency and 429 rate, and a signed admission token (key: a Key Vault secret) checked in
  middleware on online `cart` holds only (`addCartLine`, `acquireInventoryHold`). Till, kiosk and edge-node holds
  are not behind it.
- **Request budgets** (ADR-0064): a token bucket per tenant and audience in `commerce`, `access` and `operations`,
  shared through Redis (per-replica buckets if Redis is down); `429` with `Retry-After` and `RateLimit-*` headers.
- **Browse cache** (ADR-0065, proposed): availability from Redis, at most about one second old, single-flight per
  key; the hold on the primary decides.

## Events: relay, inbox and republish

- **One relay per region, in `workers`** (ADR-0058, amended 1 October). One loop per tenant database under a lease
  (`control.outbox_relay`), so one publisher per tenant and order per aggregate holds. **A full batch polls again
  at once** (the drain loop); a partial batch waits 100 ms; an empty poll backs off to 2 s.
- **`Relay:BatchSize` is configuration:** 200 in the shared cells, 1,000 in a flash-sale burst environment (set in
  its warming state), at most 5,000. Planning ceiling: **about 8,700 events a second per tenant database in a
  burst**, against 2,270-2,850 at the on-sale peak; the sprint-2 load test runs 3,500 a second and measures lag.
- **Interfaces:** modules enqueue through `IOutbox` in their own transaction; the relay publishes through
  `IBrokerPublisher` (a batch keyed by aggregate id, confirmed together); consumers subscribe through
  `IEventSubscriber` and write `kernel.inbox` (AI: `ai.inbox`) in the same transaction as their effect.
- **Republish from the outbox, by tenant and time range,** after a broker rebuild or a DR failover: `republishOutbox`
  (`POST /outbox-republishes`, `PLATFORM_CELL_MANAGE`), `listOutboxRepublishes`, `getOutboxRepublish`,
  `cancelOutboxRepublish`. Each job is a row in `control.outbox_republish`; live events go first; one republish per
  tenant at a time; only the hot outbox partitions.

## Security

- **Identity:** Entra ID for administrators; the platform's own identity for staff, guests and partners.
  Workloads use managed identities (workload identity) to reach Key Vault, storage, Redis and the registry.
- **Tenant isolation:** each tenant's database (with row-level security for venue scope) and each tenant's
  Qdrant collection, readable only with that tenant's collection-scoped JWT, signed (HS256) with the Qdrant
  API key, which the token issuer holds as a Key Vault secret. Rotating that key reissues every tenant's token
  at once, so it is a planned event (ADR-0049).
- **Least privilege between deployables:** one PostgreSQL role per deployable; the AI role is read-only on the
  transactional schemas (ADR-0020, amended by ADR-0049; ADR-0055).
- **Encryption** (ADR-0063, **proposed**): platform-managed keys at rest on every store (PostgreSQL and its
  backups, Blob, Redis, the Qdrant and broker disks; a managed broker's own encryption is part of its residency
  check); TLS everywhere, Qdrant and the broker included; customer-managed keys only for a tenant on a pinned,
  dedicated instance; identity-document numbers encrypted by the application with a data key per tenant wrapped
  by an HSM-backed Key Vault key, with a blind index for lookup (not `pgcrypto`). **No biometric template is
  stored in TICVAI**: the facial-reader vendor holds it; the platform keeps a reference and the consent.
- **Secrets:** Key Vault only; nothing in images or config maps. The secrets that sign rather than encrypt (the
  Qdrant API key, the waiting-room token key) are read only by their issuers.

## Availability, backup and recovery

**Targets per tier** (ADR-0060, **proposed**: the client has not yet said what the 99.99% agreed on 31 July
covers, nor accepted a target per tier):

| Tier | Monthly target | Measured |
|---|---|---|
| Venue operations: gate, POS, KDS (local-first, ADR-0013) | 99.99% | At the device and the edge node; a cloud outage does not count against it |
| Commerce in the cloud: guest purchase, sync, payments | 99.95% (about 22 minutes) | A synthetic purchase every minute, per region |
| Back office and operations | 99.9% | Synthetic sign-in and key reads |
| AI and engagement | 99.5%; RTO 4 h, RPO 15 min | Gateway health |

| Store | High availability | Backup |
|---|---|---|
| PostgreSQL | Zone-redundant standby on every production tier, automatic failover (pre-production has none) | Point-in-time restore 35 days; a nightly dump per tenant to Blob (UAE) for single-tenant restore; geo-redundant backup to UAE Central once access is granted (`geo_redundant_backup_enabled` is false until then) |
| Qdrant | Three nodes across zones, replication factor 2 | Snapshot per collection to local disk, copied to Blob (UAE) by a CronJob with azcopy (Blob is not a native snapshot target); disk snapshots as a second line |
| Broker | Three nodes across zones, self-run or CloudAMQP's three-node cluster | The outbox is the record: after a rebuild the relay republishes (`republishOutbox`) and the inboxes absorb duplicates |
| Redis | Azure Managed Redis, high availability, zone-redundant | Not backed up: it only holds what can be rebuilt |
| AKS | Nodes across zones; replica floors per deployable, `commerce` one per zone (ADR-0061) | Rebuilt from the registry and Terraform |

**Disaster recovery** (ADR-0060): a tenant-selectable module. With it, an asynchronous cross-region read replica in
UAE Central (RPO minutes, RTO 4 hours with a rehearsed runbook); without it, geo-restore from backup (RPO about
an hour, RTO up to 24 hours). The broker is not geo-paired: in a failover the DR broker starts empty and the relay
republishes from the promoted tenant databases. Qdrant collections are restored from their snapshots into the DR
cluster, in the UAE.

The venue edge node keeps gates and POS running through any cloud outage and syncs afterwards.

## Environments

| Environment | Purpose | Shape |
|---|---|---|
| Production | Live tenants, shared and dedicated cells | This document, with high availability (`deploy/b-shared-platform.yml`, `deploy/a-independent-tenant.yml` for the local shape) |
| Burst | One large on-sale (ADR-0035, amended 3 September) | Its own environment behind the waiting room; floors are the expected peak; `Relay:BatchSize` 1,000 (`deploy/c-flash-sale.yml`) |
| Venue on premise | Gates and POS offline (ADR-0046) | The venue edge node: PostgreSQL, Redis, RabbitMQ, a single-node Qdrant (`deploy/d-venue-local-offline.yml`) |
| Pre-production | Acceptance tests and client demos | One small cluster, single-node stores, no PostgreSQL standby (see the cost workbook) |
| Development | Day-to-day work | docker-compose locally (PostgreSQL 16, Redis, RabbitMQ; Qdrant in the venue-local profile) |

## Open points

- **The broker** is the client's choice, due Monday 12 October (ADR-0057, proposed). We recommend RabbitMQ on
  CloudAMQP in UAE North, once 84codes confirms in writing that backups, settings and logs stay there. Choosing it
  sets `broker_self_hosted = false` (no broker pool) and adds its Private Link in `snet-private-endpoints`; the
  workbook then swaps $328.50 of self-run broker for $396-696.
- **The availability targets** are with the client (ADR-0060): what the 99.99% covers, the target per tier, and
  the cost of zone-level HA (${ha:,.2f} against ${noha:,.2f} a month). PostgreSQL is zone-redundant either way.
- **UAE Central:** Dinesh requests access for the DR module and the geo-redundant backup pair (ADR-0060 action 5).
- **The AI log server** (ADR-0020, amended by ADR-0049) is priced and drawn but not in the Terraform cell module.
- **Key Vault SKU:** ADR-0063 (proposed) wraps each tenant's data key with an HSM-backed key, which needs Premium;
  the Terraform sets Premium only on the isolated tier.
- Whether the AKS API server is private. If it is, Bastion Basic cannot tunnel `kubectl`: Bastion Standard
  ($212 a month) or a jump VM in `snet-jump`.
- The ingress: confirm that the App Routing add-on's Gateway API implementation is generally available in UAE
  North before SETUP; otherwise Application Gateway for Containers in `snet-agc`.
- Prices in the workbook were checked against the Azure Retail Prices API on 30 September; confirm them in the
  Azure pricing calculator for UAE North before quoting. The Azure Managed Redis HA price (one or two instance
  meters) is unconfirmed. Pod sizes behind the node counts are assumptions until the sprint-2 benchmark.
"""


def aws_lld_md():
    amap = "\n".join(f"| {a} | {b} |" for a, b in AWS_MAP)
    sn = "\n".join(f"| `{a}` | `{b}` | {c} | {d} | {e} |" for a, b, c, d, e in AWS_SUBNETS)
    dr = "\n".join(f"| **{a}** | {b} | {c} | {d} |" for a, b, c, d in AWS_DR_OPTIONS)
    rates = "\n".join(f"| `{k}` | {v[0]:g} | {v[1]} | {v[2]} | {v[3]} |" for k, v in AWS_RATE.items())
    todo = "\n".join(f"- {t}" for t in AWS_TO_CONFIRM)
    ha, noha, pre = month(AWS_PROD_HA), month(AWS_PROD_NO_HA), month(AWS_PREPROD)
    s1, s1p = month(AWS_STAGE_1), month(AWS_STAGE_1_PREPROD)
    return f"""# TICVAI platform: low-level design (AWS)

> **Date:** {AWS_DATE} · **Generated by** `tools/build-hld-lld.py` · **Diagram:** [`TICVAI-LLD-AWS.svg`](TICVAI-LLD-AWS.svg)
> **Why:** CHG-R3-001. Chinmay, 4 October 2026: "HLD and LLD you didnt add AWS you just did azure add that in as
> well". The same cell as [`TICVAI-LLD.md`](TICVAI-LLD.md) (Azure), service for service, on AWS me-central-1.
> **Costs:** [`TICVAI - AWS Cloud Specs & Cost.xlsx`](TICVAI%20-%20AWS%20Cloud%20Specs%20%26%20Cost.xlsx): production
> with high availability **${ha:,.2f}** a month, without zone-level HA **${noha:,.2f}**, pre-production **${pre:,.2f}**;
> **staged**: Stage 1 **${s1:,.2f}** a month in production plus **${s1p:,.2f}** of pre-production. Its "Azure vs AWS"
> sheet sets these beside the Azure figures.
> **Prices:** {AWS_PRICE_SOURCE}
> **The generator holds the two clouds together** (`clouds_agree()`): the same boxes and lines in both LLDs, the
> same cost groups on every sheet, every Azure service mapped, every AWS price from the rate table, and the DR box
> open until a DR decision is recorded.

![TICVAI LLD on AWS](TICVAI-LLD-AWS.svg)

## Azure to AWS, service for service

| Azure (UAE North) | AWS (me-central-1, UAE) |
|---|---|
{amap}

Everything above the infrastructure is the same on both: the five deployables and their replica floors (ADR-0061),
one PostgreSQL database and one Qdrant collection per tenant, the outbox relay and inboxes (ADR-0058), the waiting
room (ADR-0066), the request budgets (ADR-0064), the venue edge node (ADR-0013). Kubernetes manifests and Helm
charts carry over; the Terraform cell module is Azure today, so an AWS cell needs its own module (no Block A task
builds one yet: a plan change if one is added).

## Region and residency

- **Region:** AWS me-central-1 (Middle East, UAE), three Availability Zones (a, b, c). **Every store stays in the
  UAE**, backups and snapshots included: the condition Qdrant was approved on (30 September) and ADR-0009.
- **CloudFront and the WAF are global**, as Front Door is: they cache only public content (the waiting-room page,
  public media) and decrypt at the edge nearest the user; WAF logs go to CloudWatch Logs in me-central-1.
- **One cell per region.** A cell serves many tenants; each tenant has its own PostgreSQL database and its own
  Qdrant collection.

## Disaster recovery: OPEN

{AWS_DR_OPEN}

| Option | What it is | UAE residency | Consequences |
|---|---|---|---|
{dr}

What does not change with the choice: PostgreSQL is Multi-AZ on every production tier (ADR-0060); RDS keeps
point-in-time restore for 35 days in me-central-1; the outbox is the record, so a rebuilt broker is refilled by
`republishOutbox`; the venue edge node keeps gates and POS running through any cloud outage. The LLD draws the DR
box dashed, as open.

## Tiers

| Tier | What runs there | Size (production, with HA) |
|---|---|---|
| Edge | CloudFront with AWS WAF (AWS managed core rule set for OWASP, Bot Control, rate-based rules per client IP), TLS 1.2+, a VPC origin to the internal ALB. Serves the on-sale waiting-room page from its cache (ADR-0066) | One distribution, one web ACL |
| Ingress | An internal Application Load Balancer run by the AWS Load Balancer Controller (Gateway API or Ingress), reachable only as CloudFront's VPC origin | In the system node group |
| EKS cluster | Amazon EKS, VPC CNI with custom networking (pods from the secondary range `100.64.0.0/16`, outside the node subnets), Cilium (or the VPC CNI's own) network policy, egress through the NAT Gateways, five managed node groups, a subnet per group and AZ | Standard support |
| EKS system node group | Kubernetes system services, the ingress controller | m6i.xlarge, autoscale 2-4, AZs a-c |
| EKS workload node group | `commerce`, `access`, `operations`, `workers`: floors 3, 2, 2 and 2 | m6i.2xlarge, autoscale 3-20, AZs a-c |
| EKS AI GPU node group | The only AI group (CHG-R11-001): `ticvai-ai` (real-time 2, 3 in a large cell; interactive 1; batch 0), Presidio, and on the GPU BGE-M3, its reranker and the Arabic NER; never an LLM; tainted `ticvai.io/pool=ai` | g6.2xlarge (8 vCPU, 32 GiB, 1 x L4 24 GB): 2 nodes, one per AZ (1 without HA) |
| EKS qdrant node group | Qdrant 1.16 or later, official Helm chart, 3 nodes one per AZ, replication factor 2, TLS; tainted `ticvai.io/pool=data` | r6i.xlarge x3, gp3 256 GB each |
| EKS broker node group | The broker while self-run: RabbitMQ on the Cluster Operator, 3 nodes, quorum queues; tainted `ticvai.io/pool=data`. Not built if a managed broker is chosen (Amazon MQ for RabbitMQ on AWS) | m6i.large x3, gp3 128 GB each |
| Database | Amazon RDS for PostgreSQL 16: a Multi-AZ DB instance (synchronous standby, automatic failover) on every production tier (ADR-0060); 2 read replicas; a reporting replica; the AI log database (an instance of its own, ADR-0020 as amended by ADR-0049) | db.m6g.xlarge, gp3 256 GB; reporting db.m6g.large; AI log db.m6g.xlarge with 1 TB |
| Data services | ElastiCache for Valkey (primary + replica, Multi-AZ); Secrets Manager; KMS; S3 (gateway endpoint); ECR; Amazon MQ if chosen | No public endpoint |

**RDS, not Aurora.** {AWS_DB_CHOICE}

**The AI GPU node.** {AWS_GPU_CHOICE}

## Network

VPC `10.20.0.0/16`, the Azure address plan block for block, each block split into one subnet per AZ (an AWS subnet
lives in one AZ). A cell runs on one provider, so the range is reused; change it if an AWS cell and an Azure cell
are ever peered.

| Subnet | Block | Per-AZ subnets (a, b, c) | Holds | Rule |
|---|---|---|---|---|
{sn}

- **Inbound:** only through CloudFront (web, apps, APIs, venue devices) and Session Manager (administrators, no
  inbound port). No database, cache or bucket has a public endpoint.
- **Outbound:** through a NAT Gateway in each AZ, each with an Elastic IP, so the payment, e-invoicing and messaging
  providers allow-list three addresses (one on Azure). A Regional NAT Gateway may present fewer: to confirm.
- **Security groups at the edges, network policy inside**, as NSGs and Cilium on Azure.
- **Venues:** devices reach the cloud over the Internet with TLS and device certificates; a dedicated-tier tenant
  may add a site-to-site VPN on a virtual private gateway or a Transit Gateway.

## Security

- **Identity:** IAM Identity Center for administrators; workloads use EKS Pod Identity (or IRSA) to reach Secrets
  Manager, KMS, S3, ElastiCache and ECR.
- **Keys** (ADR-0063, proposed): KMS customer managed keys, held in FIPS 140-3 validated HSMs, wrap each tenant's
  data key; BYOK by importing key material. Unlike Key Vault, no premium tier is needed for HSM-backed keys.
- **Secrets:** Secrets Manager only; the Qdrant API key and the waiting-room token key are read only by their issuers.
- **Detection:** GuardDuty (EKS Runtime Monitoring, RDS Protection, VPC flow, DNS and CloudTrail analysis),
  Inspector (node and image scanning) and Security Hub: the Defender for Cloud line.
- Tenant isolation, least privilege between deployables and encryption in transit are the Azure LLD's, unchanged.

## Availability and backup

| Store | High availability | Backup |
|---|---|---|
| PostgreSQL | RDS Multi-AZ on every production tier, automatic failover (pre-production has none) | Point-in-time restore 35 days in me-central-1; a nightly dump per tenant to S3 for single-tenant restore. Cross-region: open (DR) |
| Qdrant | Three nodes across AZs, replication factor 2 | Snapshot per collection to S3 by a CronJob; EBS snapshots by AWS Backup as a second line |
| Broker | Three nodes across AZs (self-run or Amazon MQ's three-node cluster) | The outbox is the record: after a rebuild the relay republishes |
| Redis | ElastiCache Valkey, a replica in another AZ, automatic failover | Not backed up: it only holds what can be rebuilt |
| EKS | Node groups across AZs; replica floors, `commerce` one per AZ (ADR-0061) | Rebuilt from ECR and the infrastructure code |

## Open points

- **DR** (above): A, B or C, Chinmay's and the client's call.
- **The broker** is the client's choice (ADR-0057, due 12 October). On AWS the managed RabbitMQ is Amazon MQ (3 x
  mq.m7g.large, ${_h('mq-rabbit-3x'):,.2f} a month plus storage); CloudAMQP in me-central-1 is to confirm.
- **The Terraform**: the cell module is Azure; an AWS cell module is not planned in Block A.
- **g6 capacity** in each AZ before the HA GPU node group is built.

## Prices to confirm

{todo}

## The rates behind the AWS workbook

| Key | USD | Per | What | Offer file (publication date) |
|---|---:|---|---|---|
{rates}
"""


def readme():
    return f"""# HLD and LLD

> **Date:** {DATE}. Generated by `tools/build-hld-lld.py`; re-run it after any change to the deployables,
> the Terraform cell module or the decisions it quotes. It reads the Terraform cell module and stops if the
> address plan, the replica floors, the node pools or the PostgreSQL HA mode disagree with the pack.

| File | What it is |
|---|---|
| [`TICVAI-HLD.md`](TICVAI-HLD.md) and [`TICVAI-HLD.svg`](TICVAI-HLD.svg) | High-level design: the cloud, the venue site and the outside world, every connection typed |
| [`TICVAI-LLD.md`](TICVAI-LLD.md) and [`TICVAI-LLD.svg`](TICVAI-LLD.svg) | Low-level design on Azure: region, VNet and subnets, tiers, replica floors, events, security, availability, environments |
| `TICVAI - Azure Cloud Specs & Cost.xlsx` | Specs and monthly cost, without and with high availability, for production and pre-production; editable rate, margin and prices |
| [`TICVAI-LLD-AWS.md`](TICVAI-LLD-AWS.md) and [`TICVAI-LLD-AWS.svg`](TICVAI-LLD-AWS.svg) | The same cell on AWS me-central-1 (UAE), service for service: the mapping, VPC and subnets, tiers, the RDS and GPU choices, DR (open) (CHG-R3-001, {AWS_DATE}) |
| `TICVAI - AWS Cloud Specs & Cost.xlsx` | The AWS workbook in the same layout (Stages, without and with HA, Deployables, Network), plus the service map, the DR options, the AWS rates with their offer files, and an Azure-vs-AWS sheet |

Monthly totals (USD, prices of 30 September 2026): with high availability ${month(PROD_HA):,.2f}; without zone-level
HA ${month(PROD_NO_HA):,.2f} (PostgreSQL stays zone-redundant; recomputed 1 and 4 October, see the sheet's notes; the AI pool is one GPU node pool since 4 October, CHG-R11-001);
pre-production ${month(PREPROD):,.2f}. **Staged (CHG-R11-003):** the platform launches on Stage 1, ${month(STAGE_1):,.2f}
a month in production plus ${month(STAGE_1_PREPROD):,.2f} of pre-production (the workbook's Stages sheet); the totals above
are Stage 2, the full cell.

**AWS me-central-1** (CHG-R3-001; AWS Price List API, pulled {AWS_DATE}): Stage 1 ${month(AWS_STAGE_1):,.2f} a month in
production plus ${month(AWS_STAGE_1_PREPROD):,.2f} of pre-production; the full cell ${month(AWS_PROD_NO_HA):,.2f} without
zone-level HA and ${month(AWS_PROD_HA):,.2f} with it; pre-production ${month(AWS_PREPROD):,.2f}. Disaster recovery on AWS
is open (one AWS region in the UAE).

The polished drawings are made in Claude Design from [`../design-batches/HLD-LLD/`](../design-batches/HLD-LLD/BRIEF.md).
"""


def design_brief():
    return f"""# Claude Design: TICVAI HLD and LLD

> **Date:** {DATE}. The data in `architecture.json` is generated by `tools/build-hld-lld.py`; do not edit it
> by hand.

## What to make

**One working file: `return/TICVAI Architecture.dc.html`**, with two pages:

1. **`#hld`: the high-level design.** The classic style: grey 3D boxes, a pale yellow zone for the Azure cloud,
   a pale blue zone for the venue site with orange sub-zones for onsite sales and access control, the
   outside world on the right, and a CONNECTIONS legend. Every line is coloured and dashed by its type
   (`links[].type` in `architecture.json`, legend in `linkTypes`). The draft to improve is
   `../../hld-lld/TICVAI-HLD.svg`.
2. **`#lld`: the Azure low-level design.** The Azure style: the region as a green outline, the VNet inside it,
   tiers left to right (edge, ingress, the five AKS node pools, data tier), Azure service icons, NSG shields on
   each inbound path, public IPs only where `architecture.json` says so, and a side panel for operations
   (monitor, backup, Defender). The DR region (UAE Central, the `dr` box) sits outside the UAE North outline.
   Venue site on the right with the Internet cloud between. The draft is `../../hld-lld/TICVAI-LLD.svg`.
3. **`#lld-aws`: the AWS low-level design** (CHG-R3-001). The same layout and the same boxes and lines as `#lld`
   (`lldAws` in `architecture.json`), in the AWS style: the region me-central-1 as the outline, the VPC inside it,
   the EKS node groups, the data tier, AWS service icons drawn inline. The `dr` box is **open** (no DR decided on
   AWS): draw it dashed and amber, outside the region. The draft is `../../hld-lld/TICVAI-LLD-AWS.svg`.

## Reference

Chinmay supplied two samples of the format on 30 September (a classic HLD and an Azure LLD for another
operator). **They are attached to the session, not stored here.** Match their visual language; take no names,
logos or content from them. Use TICVAI's names only, and no client names.

## Rules

- Every box and line comes from `architecture.json`. Do not add a component, and do not drop one; if something
  looks missing, list it in `return/FINDINGS.md`.
- Each page fits a 16:9 slide at 1920 x 1080 and prints on A3 landscape.
- The legend lists only the connection types the page uses.
- No external requests except Google Fonts. Azure icons are drawn inline as simple SVG, not fetched.
- Also export each page as `return/TICVAI-HLD.svg`, `return/TICVAI-LLD.svg` and `return/TICVAI-LLD-AWS.svg`.

## When it comes back

Copy the two SVGs over the drafts in `handoff/hld-lld/` only after Chinmay has approved them, and keep
`tools/build-hld-lld.py` as the source of the data.
"""


def architecture_json():
    return json.dumps({
        "date": DATE,
        "linkTypes": {k: {"label": v[0], "color": v[1], "dash": v[2]} for k, v in LINK.items()},
        "hld": {
            "zones": [dict(zip(["label", "x", "y", "w", "h", "fill", "stroke"], z)) for z in HLD_ZONES],
            "nodes": [dict(id=k, label=v[0], sub=v[1], x=v[2], y=v[3], w=v[4], h=v[5]) for k, v in HLD_NODES.items()],
            "links": [dict(source=a, target=b, type=t, via=v) for a, b, t, v in HLD_LINKS],
        },
        "lld": {
            "region": "UAE North, zones 1-3, VNet 10.20.0.0/16; DR in UAE Central (the dr box, outside the region)",
            "nodes": [dict(id=k, label=v[0], lines=v[1], x=v[2], y=v[3], w=v[4], h=v[5]) for k, v in LLD_NODES.items()],
            "frames": {k: dict(label=v[0], x=v[1], y=v[2], w=v[3], h=v[4]) for k, v in LLD_FRAMES.items()},
            "links": [dict(source=a, target=b, type=t, via=v) for a, b, t, v in LLD_LINKS],
            "subnets": [dict(zip(["name", "cidr", "holds", "rule"], s)) for s in SUBNETS],
        },
        "lldAws": {
            "date": AWS_DATE,
            "region": "AWS me-central-1 (UAE), AZs a-c, VPC 10.20.0.0/16; DR OPEN (the dr box, outside the region)",
            "nodes": [dict(id=k, label=v[0], lines=v[1], x=v[2], y=v[3], w=v[4], h=v[5]) for k, v in AWS_LLD_NODES.items()],
            "frames": {k: dict(label=v[0], x=v[1], y=v[2], w=v[3], h=v[4]) for k, v in AWS_LLD_FRAMES.items()},
            "links": [dict(source=a, target=b, type=t, via=v) for a, b, t, v in AWS_LLD_LINKS],
            "subnets": [dict(zip(["name", "block", "perAz", "holds", "rule"], s)) for s in AWS_SUBNETS],
            "serviceMap": [dict(azure=a, aws=b) for a, b in AWS_MAP],
            "dr": dict(status="open", options=[o[0] for o in AWS_DR_OPTIONS]),
        },
        "deployables": {k: {"what": v, "modules": sorted(MODULES.get(k, []))} for k, v in DEPLOYABLES.items()},
        "replicaFloors": [dict(unit=u, deployable=d, floor=f, why=w) for u, d, f, w in FLOORS],
    }, indent=1, ensure_ascii=False) + "\n"


def main():
    bad = terraform_agrees()
    for b in bad:
        print(f"ERROR terraform: {b}")
    clouds = clouds_agree()
    for b in clouds:
        print(f"ERROR clouds: {b}")
    bad = bad + clouds
    hld, lld, lld_aws = hld_svg(), lld_svg(), aws_lld_svg()
    for k, v in CROSS.items():
        for c in v:
            print(f"ERROR {k}: {c}")
    if bad or any(CROSS.values()):
        raise SystemExit(1)  # nothing written: the pack on disk stays the last good one
    write(OUT / "TICVAI-HLD.svg", hld)
    write(OUT / "TICVAI-LLD.svg", lld)
    write(OUT / "TICVAI-HLD.md", hld_md())
    write(OUT / "TICVAI-LLD.md", lld_md())
    write(OUT / "TICVAI-LLD-AWS.svg", lld_aws)
    write(OUT / "TICVAI-LLD-AWS.md", aws_lld_md())
    write(OUT / "README.md", readme())
    build_workbook(OUT / "TICVAI - Azure Cloud Specs & Cost.xlsx", AZURE)
    build_workbook(OUT / "TICVAI - AWS Cloud Specs & Cost.xlsx", AWS)
    write(DESIGN / "BRIEF.md", design_brief())
    write(DESIGN / "architecture.json", architecture_json())
    (DESIGN / "return").mkdir(parents=True, exist_ok=True)
    keep = DESIGN / "return" / ".gitkeep"
    if not keep.exists():
        write(keep, "")
    print("hld-lld: 3 diagrams, 3 documents, 2 workbooks; Claude Design brief and architecture.json; "
          f"Terraform agrees; Azure and AWS agree; no line crosses a box. Monthly USD, Azure: HA {month(PROD_HA):,.2f}, "
          f"without zone HA {month(PROD_NO_HA):,.2f}, pre-production {month(PREPROD):,.2f}; Stage 1 "
          f"{month(STAGE_1):,.2f} + pre-production {month(STAGE_1_PREPROD):,.2f}; Stage 0 {month(STAGE_0):,.2f}. "
          f"AWS: HA {month(AWS_PROD_HA):,.2f}, without zone HA {month(AWS_PROD_NO_HA):,.2f}, pre-production "
          f"{month(AWS_PREPROD):,.2f}; Stage 1 {month(AWS_STAGE_1):,.2f} + pre-production "
          f"{month(AWS_STAGE_1_PREPROD):,.2f}; Stage 0 {month(AWS_STAGE_0):,.2f}")


if __name__ == "__main__":
    main()
