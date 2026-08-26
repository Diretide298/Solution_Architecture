# Schema roots — the primary table of each schema, and how the rest derive from it

**Derived by `tools/derive-schema-roots.py`. Do not hand-edit.**

The relationship graph knows every edge and nothing said which table each schema is
*about*. This does. **A root chosen by one number is a root nobody can argue with and
nobody should trust**, so three signals are scored and disagreements are stated:

| Signal | What it means |
|---|---|
| **Own** | tables inside this schema that point at it |
| **Reach** | tables anywhere in the package that point at it |
| **Out** | tables it points at — a root points at few, a leaf at many |

Ambient edges are excluded throughout: a lineage coupling is two tables written by one
operation, which is a fact about the code rather than about the data.


## The spine — where dependencies actually stop

**Following every table's own outbound keys to a fixed point gives 42 terminal
tables**, and the distribution is the honest shape of the package:

| Terminal table | Tables that reach it |
|---|---:|
| `platform.scope_node` | 305 |
| `identity.role` | 217 |
| `platform.configuration_profile` | 95 |
| `ledger.legal_entity` | 81 |
| `pii.subject` | 66 |
| `access.admission_profile` | 61 |
| `control.plan` | 25 |
| `catalogue.variant` | 22 |
| `ai.knowledge_collection` | 20 |
| `control.developer_account` | 8 |

`platform.scope_node` is reached by 289 of 353 — **the tenancy spine, and almost
everything hangs off it.** `identity.role` at 207 is the authorisation spine.

**A first pass walked the other way** — asking who points *at* a root — and left 222
tables reaching nothing, including `identity.role` itself, because `principal` points
at `role` rather than the reverse. **The direction was the bug, not the data.**

## `control` — 41 tables

**Root: `control.cell`**  ·  own 11 · reach 11 · out 3

- **1 step from the root** — `cell_cluster`, `cell_job`, `environment`, `migration_plan_cell`, `migration_run`, `migration_run_cell`, `rollout_cell`, `tenant_migration`, `tenant_migration_plan`

- **Reaches the root through nothing** — `api_client`, `api_licence`, `api_quota`, `api_version`, `channel_listing`, `content_block`, `developer_account`, `footer_config`, `integration_listing`, `invoice`, `invoice_line`, `licence_add_on`, `migration`, `migration_plan`, `onboarding_application`, `partner_agreement`, `partner_user`, `plan`, `release`, `rollout`, `sandbox`, `seo_metadata`, `subscription`, `support_notice`, `tenant`, `upgrade_schedule`, `url_redirect`, `usage_record`, `venue_type_template`, `webhook_delivery`, `webhook_subscription`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `marketing` — 37 tables

**Root: `marketing.guest_profile`**  ·  own 0 · reach 0 · out 3

> **Overridden.** The arithmetic picks `marketing.campaign`. **`campaign` scores higher and a campaign is something done *to* a guest.** The schema is a CRM: the profile is what persists and campaigns come and go.


- **Reaches the root through nothing** — `agent_availability`, `attribution_touch`, `campaign`, `case`, `case_message`, `challenge`, `challenge_progress`, `consent_purpose`, `consent_record`, `conversation`, `conversation_message`, `form_definition`, `form_submission`, `guest_device`, `guest_document`, `invitation`, `invitation_campaign`, `journey`, `journey_entrant`, `kiosk_assist_session`, `lost_item`, `loyalty_position`, `loyalty_programme`, `loyalty_tier`, `message_delivery`, `message_dispatch`, `message_template`, `message_trigger`, `privacy_incident`, `referral`, `review`, `segment`, `segment_criterion`, `suppression`, `touch_point`, `wishlist_item`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `fnb` — 34 tables

**Root: `fnb.fnb_order`**  ·  own 1 · reach 1 · out 3

> **Overridden.** The arithmetic picks `fnb.table_visit`. **`table_visit` scores higher and not every F&B order has a table** — a kiosk order, a lounger delivery and a collection order have none. The order is the constant.

- **1 step from the root** — `fnb_order_line`

- **Reaches the root through nothing** — `bill_split`, `cold_chain_event`, `combo`, `combo_slot`, `corrective_action`, `delivery_location`, `delivery_location_outlet`, `eighty_six_event`, `guest_note`, `kitchen_exception`, `kitchen_station`, `kitchen_ticket`, `kitchen_ticket_line`, `location_code`, `location_session`, `menu`, `menu_item`, `menu_section`, `modifier_group`, `modifier_option`, `production_plan`, `production_run`, `recipe`, `recipe_ingredient`, `sub_bill`, `substitution_rule`, `table`, `table_reservation`, `table_session`, `table_visit`, `temperature_log`, `waitlist_entry`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `orders` — 34 tables

**Root: `orders.sales_order`**  ·  own 8 · reach 17 · out 5

- **1 step from the root** — `donation_line`, `order_discount`, `order_line`, `order_media_link`, `payment`, `refund`, `reservation`, `ticket_transfer`
- **2 steps from the root** — `chargeback`, `payment_tip`

- **Reaches the root through nothing** — `b2b_credit`, `cart`, `cart_line`, `cash_count_line`, `cash_movement`, `credit_override`, `deposit_box`, `fraud_rule`, `group_booking`, `invitation`, `invitation_allowance`, `no_sale_event`, `payment_link`, `payment_provider`, `payment_routing`, `payment_token`, `refund_policy`, `resale_listing`, `sales_order_unassigned`, `shift`, `stored_value_authorisation`, `ticket_template`, `wallet_pass`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `platform` — 24 tables

**Root: `platform.scope_node`**  ·  own 12 · reach 76 · out 0

- **1 step from the root** — `audit_record`, `outlet`, `redemption_right`, `region_settings`, `sale_board`, `tenant`, `venue_settings`, `workstation`
- **2 steps from the root** — `device`, `sale_board_page`
- **3 steps from the root** — `device_heartbeat`, `sale_board_tile`

- **Reaches the root through nothing** — `audit_read`, `configuration_profile`, `connectivity_policy`, `denomination`, `dsar_request`, `guest_link`, `offline_policy`, `outbox`, `profile_deployment`, `schema_version`, `wallet_authorisation`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `inventory` — 19 tables

**Root: `inventory.item`**  ·  own 10 · reach 12 · out 2

- **1 step from the root** — `count_line`, `goods_receipt_line`, `movement`, `purchase_order_line`, `quotation_line`, `requisition_line`, `serialised_item`, `stock_batch`, `stock_level`, `transfer_line`

- **Reaches the root through nothing** — `count`, `goods_receipt`, `location`, `purchase_order`, `quotation`, `requisition`, `supplier`, `transfer`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `catalogue` — 18 tables

**Root: `catalogue.product`**  ·  own 4 · reach 11 · out 4

- **1 step from the root** — `alternative_code`, `attribute_axis`, `product_version`, `variant`
- **2 steps from the root** — `price`, `waitlist_entry`

- **Reaches the root through nothing** — `channel_allocation`, `donation_campaign`, `entitlement_template`, `envelope`, `event`, `import_job`, `inventory_lease`, `performance`, `price_list`, `product_category`, `published_bundle`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `ledger` — 18 tables

**Root: `ledger.account`**  ·  own 10 · reach 15 · out 1

- **1 step from the root** — `account_mapping`, `deposit`, `entry`, `journal_line`, `recognition_schedule`, `tax_code`
- **2 steps from the root** — `journal_entry`, `tax_exemption`
- **3 steps from the root** — `price_variance`

- **Reaches the root through nothing** — `cost_center`, `event_budget`, `fiscal_period`, `fx_rate`, `inter_entity_obligation`, `legal_entity`, `settlement`, `settlement_exception`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `identity` — 16 tables

**Root: `identity.principal`**  ·  own 12 · reach 120 · out 2

- **1 step from the root** — `authz_audit`, `grant`, `mfa_challenge`, `mfa_method`, `mfa_recovery_code`, `principal_credential`, `role_permission`, `session`

- **Reaches the root through nothing** — `guest_session`, `otp_challenge`, `password_policy`, `role`, `segregation_rule`, `sso_group_mapping`, `sso_provider`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `ai` — 15 tables

**Root: `ai.index_source`**  ·  own 2 · reach 5 · out 1

- **1 step from the root** — `index_entry`, `index_job`

- **Reaches the root through nothing** — `chunk_ref`, `conversation`, `interaction`, `knowledge_collection`, `knowledge_document`, `layout_draft`, `message`, `policy`, `proposed_action`, `provider`, `suggestion`, `suggestion_outcome`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `retail` — 14 tables

**Root: `retail.sale`**  ·  own 5 · reach 5 · out 4

- **1 step from the root** — `exchange`, `return`, `sale_line`, `shop_and_drop`
- **2 steps from the root** — `return_line`, `shop_and_drop_line`

- **Reaches the root through nothing** — `gift_card`, `merchandise`, `reservation`, `reservation_line`, `return_policy`, `wallet`, `wallet_transaction`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `whitelabel` — 13 tables

**Root: `whitelabel.tenant_config`**  ·  own 3 · reach 3 · out 4

- **1 step from the root** — `banner`, `feature_toggle`, `module_enablement`

- **Reaches the root through nothing** — `config_version`, `content_page`, `custom_domain`, `faq_category`, `faq_entry`, `homepage_section`, `navigation_item`, `policy`, `promo_block`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `reporting` — 13 tables

**Root: `reporting.report_definition`**  ·  own 7 · reach 7 · out 1

- **1 step from the root** — `dashboard_tile`, `execution`, `report_column`, `report_field`, `report_filter`, `report_parameter`, `schedule`
- **2 steps from the root** — `export`

- **Reaches the root through nothing** — `alert`, `alert_rule`, `dashboard`, `schedule_recipient`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `promotions` — 11 tables

**Root: `promotions.promotion`**  ·  own 0 · reach 1 · out 1

> **Overridden.** The arithmetic picks `promotions.bundle`. **`bundle` scores higher because bundle lines point at it.** A bundle is one kind of promotion, not the thing promotions are about.


- **Reaches the root through nothing** — `allocation_component`, `allocation_split`, `bundle`, `bundle_choice_group`, `bundle_component`, `coupon_campaign`, `coupon_code`, `upsell_rule`, `voucher`, `voucher_batch`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `seating` — 11 tables

**Root: `seating.seat_map`**  ·  own 4 · reach 5 · out 1

- **1 step from the root** — `import_job`, `seat`, `seating_rules`, `zone`

- **Reaches the root through nothing** — `seat_block`, `seat_category`, `seat_hold`, `seat_map_template`, `section`, `section_row`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `games` — 8 tables

**Root: `games.play`**  ·  own 1 · reach 1 · out 2


- **Reaches the root through nothing** — `card`, `credit_ledger`, `game`, `prize`, `reader_profile`, `redemption`, `redemption_line`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `maintenance` — 8 tables

**Root: `maintenance.asset`**  ·  own 4 · reach 13 · out 3

- **1 step from the root** — `incident`, `inspection`, `maintenance_plan`, `work_order`
- **2 steps from the root** — `work_order_attachment`

- **Reaches the root through nothing** — `inspection_template`, `inspection_template_item`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `access` — 8 tables

**Root: `access.entitlement`**  ·  own 1 · reach 2 · out 4

> **Overridden.** The arithmetic picks `access.access_point`. **`access_point` has more inbound edges and the schema is about entitlements.** A gate is equipment; the thing being admitted is the point. `entitlement` also did not exist as a table until 18 August, which is why the arithmetic still favours the gate.


- **Reaches the root through nothing** — `access_point`, `admission_profile`, `blacklist`, `parking_entitlement`, `parking_facility`, `scan_event`, `scan_event_unassigned`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `approvals` — 6 tables

**Root: `approvals.request`**  ·  own 2 · reach 7 · out 2

- **1 step from the root** — `decision`, `escalation`

- **Reaches the root through nothing** — `delegation`, `matrix`, `rule`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `workforce` — 5 tables

**Root: `workforce.rota_assignment`**  ·  own 2 · reach 2 · out 4

- **1 step from the root** — `attendance`, `shift_swap`

- **Reaches the root through nothing** — `announcement`, `announcement_receipt`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `queue` — 4 tables

**Root: `queue.queue`**  ·  own 3 · reach 4 · out 4

- **1 step from the root** — `entry`, `feed`, `reading`

## `pii` — 4 tables

**Root: `pii.subject`**  ·  own 4 · reach 58 · out 1

- **1 step from the root** — `subject_biometric`, `subject_contact`, `subject_document`

## `resources` — 4 tables

**Root: `resources.resource`**  ·  own 2 · reach 2 · out 2

- **1 step from the root** — `booking`

- **Reaches the root through nothing** — `qualification`, `session_participant`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `venuemap` — 4 tables

**Root: `venuemap.point`**  ·  own 3 · reach 5 · out 4

- **1 step from the root** — `path`

- **Reaches the root through nothing** — `import_job`, `map`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `assets` — 4 tables

**Root: `assets.media_asset`**  ·  own 2 · reach 4 · out 2

- **1 step from the root** — `media_collection`, `media_usage`

- **Reaches the root through nothing** — `media_upload`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `sync` — 1 tables

**Root: `sync.rejection`**  ·  own 0 · reach 0 · out 2


