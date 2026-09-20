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
| `platform.scope` | 465 |
| `identity.role` | 360 |
| `platform.configuration_profile` | 185 |
| `pii.subject` | 150 |
| `access.admission_rules` | 138 |
| `ledger.legal_entity` | 115 |
| `catalogue.variant` | 91 |
| `subscription.plan` | 30 |
| `ai.knowledge_collection` | 29 |
| `accreditation.programme` | 10 |

`platform.scope` is reached by 289 of 353 — **the tenancy spine, and almost
everything hangs off it.** `identity.role` at 207 is the authorisation spine.

**A first pass walked the other way** — asking who points *at* a root — and left 222
tables reaching nothing, including `identity.role` itself, because `principal` points
at `role` rather than the reverse. **The direction was the bug, not the data.**

## `marketing` — 62 tables

**Root: `marketing.guest_profile`**  ·  own 0 · reach 0 · out 4

> **Overridden.** The arithmetic picks `marketing.campaign`. **`campaign` scores higher and a campaign is something done *to* a guest.** The schema is a CRM: the profile is what persists and campaigns come and go.


- **Reaches the root through nothing** — `agent_availability`, `attribution_touch`, `audience_activation`, `audience_list`, `badge`, `campaign`, `campaign_target`, `case`, `case_message`, `challenge`, `challenge_progress`, `consent_purpose`, `consent_record`, `conversation`, `conversation_message`, `customer_badge`, `duplicate_candidate`, `form_definition`, `form_submission`, `guest_attribute_model`, `guest_device`, `guest_document`, `guest_extra_field`, `guest_extra_option`, `guest_extra_value`, `guest_relationship`, `identity_rules`, `invitation`, `invitation_campaign`, `journey`, `journey_enrollment`, `journey_step`, `kiosk_assist_session`, `lost_item`, `loyalty_campaign`, `loyalty_points`, `loyalty_position`, `loyalty_programme`, `loyalty_rule`, `message_delivery`, `message_dispatch`, `message_template`, `message_trigger`, `points_earning_rule`, `points_redemption_rule`, `privacy_incident`, `programme_tier`, `referral`, `retention_policy`, `review`, `review_response`, `reward`, `reward_assignment`, `segment`, `segment_criterion`, `sla_policy`, `subscription`, `suppression`, `touch_point`, `waiver_signature`, `wishlist_item`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `control` — 49 tables

**Root: `control.cell`**  ·  own 19 · reach 24 · out 2

- **1 step from the root** — `archival_job`, `backup_run`, `cell_cluster`, `cell_instance`, `cell_job`, `cell_tenant`, `environment`, `migration_plan_cell`, `migration_run`, `migration_run_cell`, `migration_run_tenant`, `rollout_cell`, `rollout_tenant`, `scaling_policy`, `tenant_migration`, `tenant_migration_plan`, `waf_rule`

- **Reaches the root through nothing** — `api_client`, `api_licence`, `api_limit`, `api_version`, `burst_environment`, `channel_listing`, `content_block`, `developer_account`, `footer_config`, `integration_listing`, `invoice`, `invoice_line`, `licence_add_on`, `migration`, `migration_plan`, `onboarding_application`, `partner_agreement`, `partner_user`, `release`, `release_component`, `rollout`, `sandbox`, `seo_metadata`, `support_notice`, `tenant`, `upgrade_schedule`, `url_redirect`, `usage_record`, `venue_type_template`, `webhook_delivery`, `webhook_subscription`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `fnb` — 37 tables

**Root: `fnb.service_order`**  ·  own 1 · reach 1 · out 4

> **Overridden.** The arithmetic picks `fnb.table_visit`. **`table_visit` scores higher and not every F&B order has a table** — a kiosk order, a lounger delivery and a collection order have none. The order is the constant.

- **1 step from the root** — `service_order_line`

- **Reaches the root through nothing** — `bill_split`, `cold_chain_event`, `combo`, `combo_slot`, `corrective_action`, `delivery_location`, `delivery_location_outlet`, `dining_table`, `guest_note`, `ingredient_substitute`, `kitchen_exception`, `kitchen_station`, `kitchen_ticket`, `kitchen_ticket_line`, `location_session`, `menu`, `menu_item`, `menu_item_modifier`, `menu_section`, `modifier_group`, `modifier_option`, `product_recommendation`, `production_plan`, `production_run`, `recipe`, `recipe_ingredient`, `reservation_table`, `sold_out_item`, `sub_bill`, `substitution_rule`, `table_reservation`, `table_session`, `table_visit`, `temperature_log`, `waitlist_entry`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `orders` — 33 tables

**Root: `orders.sales_order`**  ·  own 13 · reach 36 · out 5

- **1 step from the root** — `credit_override`, `deposit`, `discount`, `group_booking`, `membership_renewal`, `order_fee`, `order_line`, `payment`, `payment_link`, `refund`, `reservation`, `ticket_transfer`, `upgrade`
- **2 steps from the root** — `chargeback`, `payment_tip`

- **Reaches the root through nothing** — `b2b_credit`, `cart`, `cart_line`, `cash_count_line`, `cash_movement`, `deposit_box`, `fraud_rule`, `invitation`, `invitation_allowance`, `no_sale_event`, `pos_shift`, `refund_policy`, `resale_listing`, `sales_order_unassigned`, `stored_value_authorisation`, `ticket_template`, `wallet_pass`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `catalogue` — 30 tables

**Root: `catalogue.event`**  ·  own 6 · reach 10 · out 2

- **1 step from the root** — `event_capacity_profile`, `event_registration`, `event_resource_plan`, `event_schedule`, `performance`
- **2 steps from the root** — `channel_capacity`, `waitlist_entry`
- **3 steps from the root** — `channel_allocation`, `inventory_hold`

- **Reaches the root through nothing** — `alternative_code`, `donation_campaign`, `entitlement_template`, `event_reschedule`, `event_type`, `import_job`, `membership_benefit`, `membership_programme`, `plan_benefit`, `prepaid_minutes`, `price`, `price_list`, `product`, `product_category`, `product_version`, `published_bundle`, `session_template`, `space`, `variant`, `variant_dimension`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `platform` — 26 tables

**Root: `platform.scope`**  ·  own 12 · reach 94 · out 0

- **1 step from the root** — `audit_record`, `cross_region_entitlement`, `outlet`, `region_settings`, `sale_board`, `tenant`, `venue_settings`, `workstation`
- **2 steps from the root** — `device`, `sale_board_page`
- **3 steps from the root** — `device_heartbeat`, `sale_board_tile`

- **Reaches the root through nothing** — `audit_read`, `cell_endpoint`, `configuration_profile`, `connectivity_policy`, `dead_letter`, `denomination`, `dsar_request`, `guest_link`, `offline_policy`, `outbox`, `profile_deployment`, `schema_version`, `wallet_authorisation`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `identity` — 26 tables

**Root: `identity.principal`**  ·  own 16 · reach 143 · out 2

- **1 step from the root** — `access_decision`, `access_override`, `authz_audit`, `delegated_access`, `membership_history`, `mfa_challenge`, `mfa_method`, `mfa_recovery_code`, `principal_credential`, `refresh_token`, `role_permission`, `session`

- **Reaches the root through nothing** — `access_policy`, `access_policy_version`, `benefit_usage`, `customer_membership`, `guest_session`, `module`, `otp_challenge`, `password_policy`, `permission`, `role`, `segregation_rule`, `sso_group_mapping`, `sso_provider`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `wallet` — 25 tables

**Root: `wallet.wallet`**  ·  own 9 · reach 9 · out 1

- **1 step from the root** — `adjustment`, `balance`, `credential`, `credit_lot`, `dispute`, `hold`, `restriction`, `shared_wallet`, `wallet_transaction`

- **Reaches the root through nothing** — `accounting_mapping`, `channel_rules`, `configuration_version`, `consumption_policy`, `credit_eligibility`, `credit_type`, `funding_rules`, `gift_card`, `gift_card_product`, `refund_policy`, `risk_rules`, `shared_wallet_member`, `transfer_rules`, `voucher_type`, `wallet_type`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `rental` — 23 tables

**Root: `rental.booking`**  ·  own 4 · reach 4 · out 5

- **1 step from the root** — `agreement_item`, `incident`, `override`, `settlement`
- **2 steps from the root** — `inspection_item`

- **Reaches the root through nothing** — `agreement`, `agreement_rules`, `agreement_signature`, `availability_rules`, `blackout`, `damage_assessment`, `deposit_policy`, `duration_rules`, `equipment_assignment`, `fee_policy`, `inspection`, `inventory_model`, `location_rule`, `operational_rules`, `participant`, `pricing_profile`, `product`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `payments` — 23 tables

**Root: `payments.method`**  ·  own 3 · reach 4 · out 0

- **1 step from the root** — `eligibility_rule`, `fee_rule`, `method_config`

- **Reaches the root through nothing** — `authentication_policy`, `chargeback_evidence`, `credit_account`, `currency_rule`, `deposit_activity`, `failover_policy`, `hosted_checkout`, `matching_rules`, `merchant_account`, `mixed_tender_rules`, `payment_terms`, `provider`, `provider_connection`, `reconciliation_source`, `risk_rules`, `routing_rule`, `stored_forward`, `terminal`, `token`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `games` — 21 tables

**Root: `games.game`**  ·  own 5 · reach 5 · out 3

- **1 step from the root** — `gameplay_transaction`, `operational_config`, `play`, `pricing`, `reader`
- **2 steps from the root** — `reader_deployment`

- **Reaches the root through nothing** — `attraction_type`, `authorisation`, `card`, `card_expiry_rules`, `credit_ledger`, `entitlement`, `kiosk_config`, `prize`, `prize_cost`, `reader_profile`, `redemption`, `redemption_line`, `redemption_rules`, `validation_rules`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `workforce` — 21 tables

**Root: `workforce.employee`**  ·  own 5 · reach 5 · out 2

- **1 step from the root** — `employment`, `leave_balance`, `sync_conflict`, `work_assignment`

- **Reaches the root through nothing** — `announcement`, `announcement_receipt`, `attendance`, `field_ownership`, `integration_source`, `job_title`, `leave_request`, `leave_type`, `open_shift`, `rota_assignment`, `shift`, `shift_swap`, `shift_template`, `staffing_rules`, `sync_run`, `training_record`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `inventory` — 21 tables

**Root: `inventory.item`**  ·  own 11 · reach 18 · out 2

- **1 step from the root** — `count_line`, `goods_receipt_line`, `movement`, `purchase_order_line`, `quotation_line`, `requisition_line`, `serialised_item`, `stock_batch`, `stock_level`, `stock_reservation`, `transfer_line`

- **Reaches the root through nothing** — `count`, `goods_receipt`, `location`, `purchase_order`, `quotation`, `requisition`, `supplier`, `supplier_contract`, `transfer`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `seating` — 20 tables

**Root: `seating.seat_map`**  ·  own 7 · reach 9 · out 1

- **1 step from the root** — `accessible`, `import_job`, `recommendation_rules`, `seat`, `seat_rules`, `seating_rules`, `zone`
- **2 steps from the root** — `seat_block_item`, `seat_hold_item`

- **Reaches the root through nothing** — `group_request`, `hold_pool`, `hold_type`, `reassignment`, `seat_block`, `seat_category`, `seat_hold`, `seat_map_template`, `section`, `section_row`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `reporting` — 20 tables

**Root: `reporting.report_definition`**  ·  own 11 · reach 11 · out 1

- **1 step from the root** — `dashboard_tile`, `delivery`, `execution`, `report_column`, `report_field`, `report_filter`, `report_parameter`, `schedule`, `subscription`
- **2 steps from the root** — `export`

- **Reaches the root through nothing** — `alert`, `alert_rule`, `anomaly`, `dashboard`, `kpi_definition`, `kpi_target`, `pipeline`, `schedule_recipient`, `semantic_model`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `ledger` — 18 tables

**Root: `ledger.account`**  ·  own 10 · reach 16 · out 1

- **1 step from the root** — `account_mapping`, `deposit`, `journal_line`, `posting`, `recognition_schedule`, `tax_code`
- **2 steps from the root** — `journal_entry`, `tax_exemption`
- **3 steps from the root** — `price_variance`

- **Reaches the root through nothing** — `cost_center`, `event_budget`, `fiscal_period`, `fx_rate`, `inter_entity_obligation`, `legal_entity`, `settlement`, `settlement_exception`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `promotions` — 16 tables

**Root: `promotions.promotion`**  ·  own 0 · reach 2 · out 1

> **Overridden.** The arithmetic picks `promotions.bundle`. **`bundle` scores higher because bundle lines point at it.** A bundle is one kind of promotion, not the thing promotions are about.


- **Reaches the root through nothing** — `allocation_component`, `allocation_split`, `bundle`, `bundle_choice_group`, `bundle_component`, `coupon_campaign`, `coupon_code`, `product_relationship`, `recommendation_experiment`, `recommendation_outcome`, `recommendation_strategy`, `recommendation_suppression`, `upsell_rule`, `voucher`, `voucher_batch`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `resources` — 16 tables

**Root: `resources.resource`**  ·  own 8 · reach 11 · out 3

- **1 step from the root** — `booking`, `resource_audit`, `resource_block`, `resource_dependency`, `resource_relation`, `resource_requirement`, `resource_schedule`

- **Reaches the root through nothing** — `allocation_policy`, `attribute_definition`, `qualification`, `resource_category`, `resource_package`, `resource_type`, `session_participant`, `venue_assignment`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `ai` — 16 tables

**Root: `ai.index_source`**  ·  own 3 · reach 10 · out 1

- **1 step from the root** — `index_entry`, `index_failure`, `index_job`

- **Reaches the root through nothing** — `activity`, `chunk_ref`, `conversation`, `knowledge_collection`, `knowledge_document`, `layout_draft`, `message`, `policy`, `proposed_action`, `provider`, `suggestion`, `suggestion_outcome`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `approvals` — 15 tables

**Root: `approvals.request`**  ·  own 5 · reach 16 · out 2

- **1 step from the root** — `accreditation_badge`, `decision`, `decision_record`, `escalation`, `signature`

- **Reaches the root through nothing** — `approver_availability`, `control_policy`, `delegation`, `evidence_package`, `matrix`, `retention_policy`, `rule`, `sla_policy`, `step_up_policy`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `whitelabel` — 13 tables

**Root: `whitelabel.tenant_config`**  ·  own 3 · reach 3 · out 4

- **1 step from the root** — `banner`, `feature_toggle`, `module_enablement`

- **Reaches the root through nothing** — `config_version`, `content_page`, `custom_domain`, `faq_category`, `faq_entry`, `homepage_section`, `navigation_item`, `policy`, `promo_block`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `accreditation` — 13 tables

**Root: `accreditation.programme`**  ·  own 5 · reach 5 · out 0

- **1 step from the root** — `application`, `holder`, `notification_rules`, `requirements`, `validity`
- **2 steps from the root** — `audit`, `credential`, `document`, `holder_access`

- **Reaches the root through nothing** — `access_profile`, `badge_template`, `print_job`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `retail` — 13 tables

**Root: `retail.sale`**  ·  own 5 · reach 5 · out 4

- **1 step from the root** — `exchange`, `return`, `sale_line`, `shop_and_drop`
- **2 steps from the root** — `return_line`, `shop_and_drop_line`

- **Reaches the root through nothing** — `merchandise`, `product_recommendation`, `reservation`, `reservation_line`, `return_policy`, `store_rule`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `subscription` — 13 tables

**Root: `subscription.plan`**  ·  own 1 · reach 7 · out 0

- **1 step from the root** — `contract`

- **Reaches the root through nothing** — `capacity_pack`, `enforcement_policy`, `go_live_readiness`, `licensing_model`, `module_listing`, `partner_quote`, `tier_allowance`, `tier_module`, `trial_config`, `vsi_assessment`, `vsi_model`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `assets` — 12 tables

**Root: `assets.media_asset`**  ·  own 2 · reach 19 · out 2

- **1 step from the root** — `media_collection`, `media_usage`

- **Reaches the root through nothing** — `approval`, `asset_version`, `audit`, `distribution_channel`, `media_upload`, `rendition`, `share`, `tag`, `taxonomy`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `access` — 10 tables

**Root: `access.entitlement`**  ·  own 2 · reach 13 · out 6

> **Overridden.** The arithmetic picks `access.entitlement`. **`access_point` has more inbound edges and the schema is about entitlements.** A gate is equipment; the thing being admitted is the point. `entitlement` also did not exist as a table until 18 August, which is why the arithmetic still favours the gate.

- **1 step from the root** — `scan_event`

- **Reaches the root through nothing** — `access_change`, `access_point`, `admission_rules`, `blacklist`, `entry_rule_point`, `parking_entitlement`, `parking_facility`, `scan_event_unassigned`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `maintenance` — 10 tables

**Root: `maintenance.asset`**  ·  own 4 · reach 20 · out 5

- **1 step from the root** — `incident`, `inspection`, `preventive_plan`, `work_order`
- **2 steps from the root** — `inspection_item`, `work_order_attachment`

- **Reaches the root through nothing** — `asset_category`, `inspection_template`, `inspection_template_item`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `tenancy` — 7 tables

**Root: `tenancy.device_firmware`**  ·  own 1 · reach 1 · out 1

- **1 step from the root** — `device_rollout`

- **Reaches the root through nothing** — `device_assignment`, `device_audit`, `device_credential`, `device_tamper_event`, `device_telemetry`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `venuemap` — 4 tables

**Root: `venuemap.point`**  ·  own 3 · reach 5 · out 4

- **1 step from the root** — `path`

- **Reaches the root through nothing** — `import_job`, `map`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `queue` — 4 tables

**Root: `queue.queue`**  ·  own 4 · reach 5 · out 5

- **1 step from the root** — `entry`, `feed`, `reading`

## `pii` — 4 tables

**Root: `pii.subject`**  ·  own 4 · reach 61 · out 1

- **1 step from the root** — `subject_biometric`, `subject_contact`, `subject_document`

## `sync` — 3 tables

**Root: `sync.cell_connection`**  ·  own 0 · reach 0 · out 2


- **Reaches the root through nothing** — `cross_cell_request`, `rejection`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `pricing` — 3 tables

**Root: `pricing.dynamic_price_rule`**  ·  own 2 · reach 2 · out 3

- **1 step from the root** — `dynamic_price_action`, `dynamic_price_condition`

