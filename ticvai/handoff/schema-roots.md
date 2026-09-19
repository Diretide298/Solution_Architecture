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
| `platform.scope` | 417 |
| `identity.role` | 329 |
| `ledger.legal_entity` | 147 |
| `subscription.plan` | 144 |
| `platform.configuration_profile` | 130 |
| `resources.resource_type` | 118 |
| `pii.subject` | 92 |
| `access.admission_rules` | 77 |
| `catalogue.variant` | 25 |
| `ai.knowledge_collection` | 21 |

`platform.scope` is reached by 289 of 353 — **the tenancy spine, and almost
everything hangs off it.** `identity.role` at 207 is the authorisation spine.

**A first pass walked the other way** — asking who points *at* a root — and left 222
tables reaching nothing, including `identity.role` itself, because `principal` points
at `role` rather than the reverse. **The direction was the bug, not the data.**

## `control` — 49 tables

**Root: `control.cell`**  ·  own 19 · reach 19 · out 2

- **1 step from the root** — `archival_job`, `backup_run`, `cell_cluster`, `cell_instance`, `cell_job`, `cell_tenant`, `environment`, `migration_plan_cell`, `migration_run`, `migration_run_cell`, `migration_run_tenant`, `rollout_cell`, `rollout_tenant`, `scaling_policy`, `tenant_migration`, `tenant_migration_plan`, `waf_rule`

- **Reaches the root through nothing** — `api_client`, `api_licence`, `api_limit`, `api_version`, `burst_environment`, `channel_listing`, `content_block`, `developer_account`, `footer_config`, `integration_listing`, `invoice`, `invoice_line`, `licence_add_on`, `migration`, `migration_plan`, `onboarding_application`, `partner_agreement`, `partner_user`, `release`, `release_component`, `rollout`, `sandbox`, `seo_metadata`, `support_notice`, `tenant`, `upgrade_schedule`, `url_redirect`, `usage_record`, `venue_type_template`, `webhook_delivery`, `webhook_subscription`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `marketing` — 45 tables

**Root: `marketing.guest_profile`**  ·  own 0 · reach 0 · out 4

> **Overridden.** The arithmetic picks `marketing.segment`. **`campaign` scores higher and a campaign is something done *to* a guest.** The schema is a CRM: the profile is what persists and campaigns come and go.


- **Reaches the root through nothing** — `agent_availability`, `attribution_touch`, `audience_activation`, `audience_list`, `campaign`, `case`, `case_message`, `challenge`, `challenge_progress`, `consent_purpose`, `consent_record`, `conversation`, `conversation_message`, `duplicate_candidate`, `form_definition`, `form_submission`, `guest_attribute_model`, `guest_device`, `guest_document`, `guest_relationship`, `identity_rules`, `invitation`, `invitation_campaign`, `journey`, `journey_enrollment`, `kiosk_assist_session`, `lost_item`, `loyalty_position`, `loyalty_programme`, `loyalty_tier`, `message_delivery`, `message_dispatch`, `message_template`, `message_trigger`, `privacy_incident`, `referral`, `retention_policy`, `review`, `segment`, `segment_criterion`, `subscription`, `suppression`, `touch_point`, `wishlist_item`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `fnb` — 34 tables

**Root: `fnb.service_order`**  ·  own 2 · reach 2 · out 3

> **Overridden.** The arithmetic picks `fnb.table_visit`. **`table_visit` scores higher and not every F&B order has a table** — a kiosk order, a lounger delivery and a collection order have none. The order is the constant.

- **1 step from the root** — `service_order_line`

- **Reaches the root through nothing** — `bill_split`, `cold_chain_event`, `combo`, `combo_slot`, `corrective_action`, `delivery_location`, `delivery_location_outlet`, `dining_table`, `guest_note`, `kitchen_exception`, `kitchen_station`, `kitchen_ticket`, `kitchen_ticket_line`, `location_code`, `location_session`, `menu`, `menu_item`, `menu_section`, `modifier_group`, `modifier_option`, `production_plan`, `production_run`, `recipe`, `recipe_ingredient`, `sold_out_item`, `sub_bill`, `substitution_rule`, `table_reservation`, `table_session`, `table_visit`, `temperature_log`, `waitlist_entry`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `orders` — 32 tables

**Root: `orders.sales_order`**  ·  own 11 · reach 30 · out 5

- **1 step from the root** — `credit_override`, `donation_line`, `group_booking`, `order_discount`, `order_line`, `order_media_link`, `payment`, `payment_link`, `refund`, `reservation`, `ticket_transfer`
- **2 steps from the root** — `chargeback`, `payment_tip`

- **Reaches the root through nothing** — `b2b_credit`, `cart`, `cart_line`, `cash_count_line`, `cash_movement`, `deposit_box`, `fraud_rule`, `invitation`, `invitation_allowance`, `no_sale_event`, `payment_routing`, `pos_shift`, `refund_policy`, `resale_listing`, `sales_order_unassigned`, `stored_value_authorisation`, `ticket_template`, `wallet_pass`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `catalogue` — 27 tables

**Root: `catalogue.event`**  ·  own 6 · reach 10 · out 2

- **1 step from the root** — `event_capacity_profile`, `event_registration`, `event_resource_plan`, `event_schedule`, `performance`
- **2 steps from the root** — `channel_capacity`, `waitlist_entry`
- **3 steps from the root** — `channel_allocation`, `inventory_hold`

- **Reaches the root through nothing** — `alternative_code`, `donation_campaign`, `entitlement_template`, `event_reschedule`, `event_type`, `import_job`, `prepaid_minutes`, `price`, `price_list`, `product`, `product_category`, `product_version`, `published_bundle`, `session_template`, `space`, `variant`, `variant_dimension`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `platform` — 25 tables

**Root: `platform.scope`**  ·  own 13 · reach 93 · out 0

- **1 step from the root** — `audit_record`, `cross_region_entitlement`, `outlet`, `region_settings`, `sale_board`, `tenant`, `venue_settings`, `workstation`
- **2 steps from the root** — `device`, `sale_board_page`
- **3 steps from the root** — `device_heartbeat`, `sale_board_tile`

- **Reaches the root through nothing** — `audit_read`, `configuration_profile`, `connectivity_policy`, `dead_letter`, `denomination`, `dsar_request`, `guest_link`, `offline_policy`, `outbox`, `profile_deployment`, `schema_version`, `wallet_authorisation`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `wallet` — 23 tables

**Root: `wallet.wallet`**  ·  own 7 · reach 7 · out 1

- **1 step from the root** — `adjustment`, `credential`, `credit_lot`, `dispute`, `restriction`, `shared_wallet`, `wallet_transaction`

- **Reaches the root through nothing** — `accounting_mapping`, `channel_rules`, `configuration_version`, `consumption_policy`, `credit_eligibility`, `credit_type`, `funding_rules`, `gift_card`, `gift_card_product`, `refund_policy`, `risk_rules`, `shared_wallet_member`, `transfer_rules`, `voucher_type`, `wallet_type`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `games` — 21 tables

**Root: `games.game`**  ·  own 5 · reach 5 · out 3

- **1 step from the root** — `gameplay_transaction`, `operational_config`, `play`, `pricing`, `reader`
- **2 steps from the root** — `reader_deployment`

- **Reaches the root through nothing** — `attraction_type`, `authorisation`, `card`, `card_expiry_rules`, `credit_ledger`, `entitlement`, `kiosk_config`, `prize`, `prize_cost`, `reader_profile`, `redemption`, `redemption_line`, `redemption_rules`, `validation_rules`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `identity` — 20 tables

**Root: `identity.principal`**  ·  own 14 · reach 134 · out 2

- **1 step from the root** — `access_decision`, `access_override`, `authz_audit`, `delegated_access`, `mfa_challenge`, `mfa_method`, `mfa_recovery_code`, `principal_credential`, `role_permission`, `session`

- **Reaches the root through nothing** — `access_policy`, `access_policy_version`, `guest_session`, `otp_challenge`, `password_policy`, `role`, `segregation_rule`, `sso_group_mapping`, `sso_provider`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `reporting` — 20 tables

**Root: `reporting.report_definition`**  ·  own 11 · reach 11 · out 1

- **1 step from the root** — `dashboard_tile`, `delivery`, `execution`, `report_column`, `report_field`, `report_filter`, `report_parameter`, `schedule`, `subscription`
- **2 steps from the root** — `export`

- **Reaches the root through nothing** — `alert`, `alert_rule`, `anomaly`, `dashboard`, `kpi_definition`, `kpi_target`, `pipeline`, `schedule_recipient`, `semantic_model`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `rental` — 20 tables

**Root: `rental.product`**  ·  own 6 · reach 9 · out 6

- **1 step from the root** — `blackout`, `booking`, `deposit_policy`, `fee_policy`, `pricing_profile`
- **2 steps from the root** — `incident`, `override`, `settlement`

- **Reaches the root through nothing** — `agreement_rules`, `agreement_signature`, `availability_rules`, `damage_assessment`, `duration_rules`, `equipment_assignment`, `inspection`, `inventory_model`, `location_rule`, `operational_rules`, `participant`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `inventory` — 19 tables

**Root: `inventory.item`**  ·  own 10 · reach 13 · out 3

- **1 step from the root** — `count_line`, `goods_receipt_line`, `movement`, `purchase_order_line`, `quotation_line`, `requisition_line`, `serialised_item`, `stock_batch`, `stock_level`, `transfer_line`

- **Reaches the root through nothing** — `count`, `goods_receipt`, `location`, `purchase_order`, `quotation`, `requisition`, `supplier`, `transfer`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `seating` — 18 tables

**Root: `seating.seat_map`**  ·  own 7 · reach 9 · out 1

- **1 step from the root** — `accessible`, `import_job`, `recommendation_rules`, `seat`, `seat_rules`, `seating_rules`, `zone`

- **Reaches the root through nothing** — `group_request`, `hold_pool`, `hold_type`, `reassignment`, `seat_block`, `seat_category`, `seat_hold`, `seat_map_template`, `section`, `section_row`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `payments` — 18 tables

**Root: `payments.provider_connection`**  ·  own 2 · reach 2 · out 1

- **1 step from the root** — `reconciliation_source`, `terminal`

- **Reaches the root through nothing** — `authentication_policy`, `chargeback_evidence`, `credit_account`, `failover_policy`, `hosted_checkout`, `matching_rules`, `merchant_account`, `method`, `mixed_tender_rules`, `payment_terms`, `provider`, `risk_rules`, `routing_rule`, `stored_forward`, `token`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `ledger` — 18 tables

**Root: `ledger.account`**  ·  own 10 · reach 16 · out 1

- **1 step from the root** — `account_mapping`, `deposit`, `journal_line`, `posting`, `recognition_schedule`, `tax_code`
- **2 steps from the root** — `journal_entry`, `tax_exemption`
- **3 steps from the root** — `price_variance`

- **Reaches the root through nothing** — `cost_center`, `event_budget`, `fiscal_period`, `fx_rate`, `inter_entity_obligation`, `legal_entity`, `settlement`, `settlement_exception`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `ai` — 16 tables

**Root: `ai.index_source`**  ·  own 3 · reach 6 · out 1

- **1 step from the root** — `index_entry`, `index_failure`, `index_job`

- **Reaches the root through nothing** — `activity`, `chunk_ref`, `conversation`, `knowledge_collection`, `knowledge_document`, `layout_draft`, `message`, `policy`, `proposed_action`, `provider`, `suggestion`, `suggestion_outcome`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `resources` — 16 tables

**Root: `resources.resource`**  ·  own 8 · reach 10 · out 3

- **1 step from the root** — `booking`, `resource_audit`, `resource_block`, `resource_dependency`, `resource_relation`, `resource_requirement`, `resource_schedule`

- **Reaches the root through nothing** — `allocation_policy`, `attribute_definition`, `qualification`, `resource_category`, `resource_package`, `resource_type`, `session_participant`, `venue_assignment`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `promotions` — 16 tables

**Root: `promotions.promotion`**  ·  own 0 · reach 1 · out 1

> **Overridden.** The arithmetic picks `promotions.bundle`. **`bundle` scores higher because bundle lines point at it.** A bundle is one kind of promotion, not the thing promotions are about.


- **Reaches the root through nothing** — `allocation_component`, `allocation_split`, `bundle`, `bundle_choice_group`, `bundle_component`, `coupon_campaign`, `coupon_code`, `product_relationship`, `recommendation_experiment`, `recommendation_outcome`, `recommendation_strategy`, `recommendation_suppression`, `upsell_rule`, `voucher`, `voucher_batch`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `approvals` — 15 tables

**Root: `approvals.request`**  ·  own 5 · reach 16 · out 2

- **1 step from the root** — `accreditation_badge`, `decision`, `decision_record`, `escalation`, `signature`

- **Reaches the root through nothing** — `approver_availability`, `control_policy`, `delegation`, `evidence_package`, `matrix`, `retention_policy`, `rule`, `sla_policy`, `step_up_policy`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `accreditation` — 13 tables

**Root: `accreditation.programme`**  ·  own 5 · reach 5 · out 0

- **1 step from the root** — `application`, `holder`, `notification_rules`, `requirements`, `validity`
- **2 steps from the root** — `audit`, `credential`, `document`, `holder_access`

- **Reaches the root through nothing** — `access_profile`, `badge_template`, `print_job`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `whitelabel` — 13 tables

**Root: `whitelabel.tenant_config`**  ·  own 3 · reach 3 · out 4

- **1 step from the root** — `banner`, `feature_toggle`, `module_enablement`

- **Reaches the root through nothing** — `config_version`, `content_page`, `custom_domain`, `faq_category`, `faq_entry`, `homepage_section`, `navigation_item`, `policy`, `promo_block`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `retail` — 12 tables

**Root: `retail.sale`**  ·  own 5 · reach 5 · out 4

- **1 step from the root** — `exchange`, `return`, `sale_line`, `shop_and_drop`
- **2 steps from the root** — `return_line`, `shop_and_drop_line`

- **Reaches the root through nothing** — `merchandise`, `reservation`, `reservation_line`, `return_policy`, `store_rule`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `assets` — 12 tables

**Root: `assets.media_asset`**  ·  own 2 · reach 4 · out 2

- **1 step from the root** — `media_collection`, `media_usage`

- **Reaches the root through nothing** — `approval`, `asset_version`, `audit`, `distribution_channel`, `media_upload`, `rendition`, `share`, `tag`, `taxonomy`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `subscription` — 11 tables

**Root: `subscription.plan`**  ·  own 1 · reach 7 · out 0

- **1 step from the root** — `contract`

- **Reaches the root through nothing** — `capacity_pack`, `enforcement_policy`, `go_live_readiness`, `licensing_model`, `module_listing`, `partner_quote`, `trial_config`, `vsi_assessment`, `vsi_model`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `workforce` — 10 tables

**Root: `workforce.rota_assignment`**  ·  own 3 · reach 3 · out 5

- **1 step from the root** — `attendance`, `open_shift`, `shift_swap`

- **Reaches the root through nothing** — `announcement`, `announcement_receipt`, `leave_request`, `shift_template`, `staffing_rules`, `training_record`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `maintenance` — 9 tables

**Root: `maintenance.asset`**  ·  own 5 · reach 34 · out 5

- **1 step from the root** — `asset_category`, `incident`, `inspection`, `preventive_plan`, `work_order`
- **2 steps from the root** — `inspection_template`, `work_order_attachment`
- **3 steps from the root** — `inspection_template_item`

## `access` — 8 tables

**Root: `access.entitlement`**  ·  own 2 · reach 9 · out 6

> **Overridden.** The arithmetic picks `access.entitlement`. **`access_point` has more inbound edges and the schema is about entitlements.** A gate is equipment; the thing being admitted is the point. `entitlement` also did not exist as a table until 18 August, which is why the arithmetic still favours the gate.

- **1 step from the root** — `scan_event`

- **Reaches the root through nothing** — `access_point`, `admission_rules`, `blacklist`, `parking_entitlement`, `parking_facility`, `scan_event_unassigned`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `tenancy` — 7 tables

**Root: `tenancy.device_firmware`**  ·  own 1 · reach 1 · out 1

- **1 step from the root** — `device_rollout`

- **Reaches the root through nothing** — `device_assignment`, `device_audit`, `device_credential`, `device_tamper_event`, `device_telemetry`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `queue` — 4 tables

**Root: `queue.queue`**  ·  own 4 · reach 5 · out 5

- **1 step from the root** — `entry`, `feed`, `reading`

## `pii` — 4 tables

**Root: `pii.subject`**  ·  own 4 · reach 61 · out 1

- **1 step from the root** — `subject_biometric`, `subject_contact`, `subject_document`

## `venuemap` — 4 tables

**Root: `venuemap.point`**  ·  own 3 · reach 5 · out 4

- **1 step from the root** — `path`

- **Reaches the root through nothing** — `import_job`, `map`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `sync` — 1 tables

**Root: `sync.rejection`**  ·  own 0 · reach 0 · out 2


