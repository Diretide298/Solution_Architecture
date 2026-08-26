# Coverage — the three uncounted sheets

**113 requirements on three sheets nobody had counted.** Every figure quoted since 30 July —
3,184 across 21 domains — was the Functionality sheet alone (CF-60).

Counted 17 August. **They do not all belong in the same denominator**, which is the reason the
omission survived: two of the three sheets ask for something other than software.

| Sheet | Reqs | What it is |
|---|---|---|
| Disaster Recovery & BCP | 62 | **Infrastructure and operations.** Backup, replication, restore drills, runbooks |
| Training, Knowledge Transfer & Support | 40 | **A delivery commitment, not a system requirement.** What Softlabs will teach, to whom |
| Compliance & Security | 11 | **Partly software, partly policy.** SSO and MFA are contracted; key rotation and security event logging are not |
| | **113** | |

## Why they are not simply added to 3,184

**The 40 training requirements are things a person does, not things a system has.** *"System
provider shall deliver administrator training"* has no screen, no operation and no table. They
belong in the statement of work, and counting them as uncovered platform requirements would
make the coverage figure meaningless in the other direction.

**The 62 DR requirements are mostly infrastructure.** Backup schedules and replication are
real and must be designed, but they are Dinesh's layer rather than a contract. Two of them —
RPO and RTO — do sit in the platform, and they are the subject of CF-64.

**Only the 11 security requirements compete for the same denominator**, and seven of those are
already covered by identity and pii.

## The finding that changes CF-64

> **11.** Recovery Point Objective (RPO) — System shall support **configurable** recovery point objectives.

> **12.** Recovery Time Objective (RTO) — System shall support **configurable** recovery time objectives.

**Configurable.** The matrix does not ask us to hit a number; it asks the platform to let a
tenant choose one. That is a narrower question than CF-64 has been carrying since 6 August.

It does not make the question go away. **A configurable RPO still needs a floor** — offering
RPO near zero requires synchronous replication and a second site, and that is a topology
decision made once. **What we need from the client is the tightest RPO any tenant may buy**,
not the RPO for Miral, and that is a smaller and more answerable question.

## Line-by-line

### Compliance & Security

| Ref | Requirement | Where it lands | |
|---|---|---|---|
| 1 | Privacy & Compliance Management Provide data privacy and compliance management | pii schema, DSAR operations, consent records | ✅ |
| 2 | PCI-DSS Compliance Provide PCI-DSS compliance features such as payment tokeniz | CF-68 PaymentProvider, tokenisation is the gateway's | 🟡 |
| 3 | Enterprise Security Controls Provide enterprise security features including SS | identity contract | ✅ |
| 4 | Secrets Management System shall securely manage credentials, encryption keys,  | audit artefact class — not built | 🔴 |
| 5 | Security Event Monitoring System shall generate and expose security events inc | audit artefact class — not built | 🔴 |
| 6 | Security Incident Logging System shall maintain detailed logs of security inci | audit artefact class — not built | 🔴 |
| 7 | Encryption Key Rotation System shall support periodic encryption key rotation, | storage-design.md names a vault; no rotation policy | 🟡 |
| 8 | API Security Protection System shall provide API security controls including r | — | 🔴 |
| 9 | Web Application Firewall (WAF) Support System shall support integration with W | — | 🔴 |
| 10 | AI Data Residency AI services shall support deployment models that comply with | pii schema, DSAR operations, consent records | ✅ |
| 11 | SIEM Integration To provide a security solution that helps organizations recog | — | 🔴 |

### Disaster Recovery & BCP

| Ref | Requirement | Where it lands | |
|---|---|---|---|
| 1 | Automated Backups - System shall perform automated backups. | infrastructure — ADR-0017 deployment models | 🔴 |
| 2 | Scheduled Backups - System shall support configurable backup schedules. | infrastructure — ADR-0017 deployment models | 🔴 |
| 3 | Full Backups - System shall support full system backups. | infrastructure — ADR-0017 deployment models | 🔴 |
| 4 | Incremental Backups - System shall support incremental backups. | infrastructure — ADR-0017 deployment models | 🔴 |
| 5 | Differential Backups - System shall support differential backups. | infrastructure — ADR-0017 deployment models | 🔴 |
| 6 | Database Backups - System shall perform database backups. | infrastructure — ADR-0017 deployment models | 🔴 |
| 7 | File Storage Backups - System shall perform file and document backups. | infrastructure — ADR-0017 deployment models | 🔴 |
| 8 | Configuration Backups - System shall backup platform configurations. | infrastructure — ADR-0017 deployment models | 🔴 |
| 9 | Backup Encryption - System shall encrypt backup data. | infrastructure — ADR-0017 deployment models | 🔴 |
| 10 | Backup Retention Policies - System shall support configurable backup retention | infrastructure — ADR-0017 deployment models | 🔴 |
| 11 | Recovery Point Objective (RPO) - System shall support configurable recovery po | **configurable** — the platform provides the range, the tenant picks | 🟡 |
| 12 | Recovery Time Objective (RTO) - System shall support configurable recovery tim | **configurable** — the platform provides the range, the tenant picks | 🟡 |
| 13 | Point-in-Time Recovery - System shall support point-in-time restoration. | — | 🔴 |
| 14 | Database Recovery - System shall support database restoration. | — | 🔴 |
| 15 | File Recovery - System shall support recovery of files and documents. | operational documentation — not an artefact class we track | 🔴 |
| 16 | Configuration Recovery - System shall support restoration of platform configur | — | 🔴 |
| 17 | Tenant Recovery - System shall support recovery of individual tenant environme | — | 🔴 |
| 18 | Environment Recovery - System shall support recovery of complete environments. | — | 🔴 |
| 19 | Selective Recovery - System shall support selective restoration of data. | — | 🔴 |
| 20 | Recovery Verification - System shall validate recovery integrity after restora | — | 🔴 |
| 21 | High Availability Architecture - System shall support high availability deploy | — | 🔴 |
| 22 | Redundant Services - System shall support service redundancy. | — | 🔴 |
| 23 | Database Replication - System shall support database replication. | ADR-0016 analytical replica; DR replica not designed | 🔴 |
| 24 | Load Balancing - System shall support load balancing. | — | 🔴 |
| 25 | Multi-Node Deployment - System shall support multi-node deployments. | — | 🔴 |
| 26 | Automatic Failover - System shall support automatic failover. | ADR-0016 analytical replica; DR replica not designed | 🔴 |
| 27 | Manual Failover - System shall support manual failover procedures. | ADR-0016 analytical replica; DR replica not designed | 🔴 |
| 28 | Service Health Monitoring - System shall monitor service availability. | observability doc; no contract | 🔴 |
| 29 | Availability Reporting - System shall provide availability reporting. | — | 🔴 |
| 30 | Uptime Monitoring - System shall monitor platform uptime. | observability doc; no contract | 🔴 |
| 31 | Disaster Recovery Plan - System provider shall maintain a disaster recovery pl | operational documentation — not an artefact class we track | 🔴 |
| 32 | Disaster Recovery Procedures - System shall support documented disaster recove | operational documentation — not an artefact class we track | 🔴 |
| 33 | Disaster Recovery Testing - System shall support periodic disaster recovery te | — | 🔴 |
| 34 | Disaster Recovery Reporting - System shall provide disaster recovery test repo | — | 🔴 |
| 35 | Secondary Environment - System shall support secondary recovery environments. | — | 🔴 |
| 36 | Cross-Region Recovery - System shall support cross-region recovery. | — | 🔴 |
| 37 | Geographic Redundancy - System shall support geographically distributed infras | — | 🔴 |
| 38 | Recovery Automation - System shall support automated recovery procedures. | operational documentation — not an artefact class we track | 🔴 |
| 39 | Emergency Recovery Mode - System shall support emergency recovery operations. | — | 🔴 |
| 40 | Disaster Audit Logs - System shall maintain disaster recovery audit logs. | audit artefact class — not built | 🔴 |
| 41 | Business Continuity Plan - System provider shall maintain a business continuit | operational documentation — not an artefact class we track | 🔴 |
| 42 | Critical Service Identification - System shall identify critical business serv | — | 🔴 |
| 43 | Continuity Procedures - System shall support continuity procedures for critica | operational documentation — not an artefact class we track | 🔴 |
| 44 | Operational Continuity Monitoring - System shall monitor continuity readiness. | observability doc; no contract | 🔴 |
| 45 | Continuity Testing - System shall support periodic continuity testing. | — | 🔴 |
| 46 | Incident Escalation Procedures - System shall support incident escalation proc | operational documentation — not an artefact class we track | 🔴 |
| 47 | Service Restoration Procedures - System shall support service restoration proc | operational documentation — not an artefact class we track | 🔴 |
| 48 | Crisis Communication Procedures - System shall support crisis communication pr | operational documentation — not an artefact class we track | 🔴 |
| 49 | Business Impact Reporting - System shall support business impact reporting. | — | 🔴 |
| 50 | Continuity Audit Reporting - System shall provide continuity audit reports. | audit artefact class — not built | 🔴 |
| 51 | Backup Access Control - System shall restrict access to backup data. | infrastructure — ADR-0017 deployment models | 🔴 |
| 52 | Recovery Authorization Controls - System shall require authorization for recov | — | 🔴 |
| 53 | Backup Audit Logs - System shall maintain audit logs for backup operations. | audit artefact class — not built | 🔴 |
| 54 | Recovery Audit Logs - System shall maintain audit logs for recovery operations | audit artefact class — not built | 🔴 |
| 55 | Backup Integrity Validation - System shall validate backup integrity. | infrastructure — ADR-0017 deployment models | 🔴 |
| 56 | Backup Tamper Protection - System shall protect backups against unauthorized m | infrastructure — ADR-0017 deployment models | 🔴 |
| 57 | Compliance Retention Support - System shall support regulatory retention requi | — | 🔴 |
| 58 | Recovery Compliance Reporting - System shall provide recovery compliance repor | — | 🔴 |
| 59 | Data Sovereignty Support - System shall support regional data residency requir | — | 🔴 |
| 60 | Backup & Recovery Dashboards - System shall provide backup and recovery dashbo | infrastructure — ADR-0017 deployment models | 🔴 |
| 61 | System shall maintain documented recovery runbooks, recovery playbooks, operat | operational documentation — not an artefact class we track | 🔴 |
| 1 | System shall support scheduled disaster recovery simulations, tabletop exercis | ADR-0016 analytical replica; DR replica not designed | 🔴 |

### Training, Knowledge Transfer & Support

All 40 are delivery commitments. Not itemised here because none maps to an artefact — they
belong in the SOW and should be tracked against it, not against the platform.

## What this changes

| | |
|---|---|
| Platform requirements | **3,184 + 11 = 3,195** — the security sheet joins the denominator |
| Infrastructure requirements | **62**, tracked separately, owned by Dinesh |
| Delivery commitments | **40**, belong in the statement of work |

**Adding 113 to a coverage figure would have been the wrong correction.** Two of the three
sheets measure something else, and the honest fix is three denominators rather than one bigger
one.
