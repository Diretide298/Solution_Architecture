-- The venue partitioning mechanism (ADR-0005, ADR-0044).
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- ADR-0044, signed off 18 September 2026: a table whose `venue_id` is NOT NULL partitions by list
-- on it, carries `venue_id` as the leading column of its primary key, and every foreign key into
-- it is composite. **What lives here is the mechanism; the tables declare their own partitioning
-- where they are created.**
--
-- **Every partitioned table needs a DEFAULT partition.** Misconfiguration should be loud rather
-- than silently lossy — an insert for an unprovisioned venue lands somewhere it can be found.
--
-- **One thing from the old baseline is deliberately not carried: the `platform.scope_level` enum.**
-- It existed so a `venue_id` column could not resolve to a workstation, paired with a composite
-- foreign key in a `V0003a__scope-typing.sql` that is not part of this generation. Every
-- `scope_level` column here is `text`; where its contract declares the enum, the column carries a
-- `<table>_<column>_chk` CHECK with the contract's values, like every other contract enum. That a
-- `venue_id` resolves to a venue and not a workstation is still the application's to check.
--
-- **Partitions are named `<table>_<venue uuid hex>`, not naming-and-style 6.1's
-- `<table>_v<venue_number>`.** Nothing in the package defines or allocates a venue number, so
-- there is nothing to derive the 6.1 name from; that is a decision to make, not a rename.
CREATE OR REPLACE FUNCTION platform.ensure_venue_partition(target regclass, venue_id uuid)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    part_name text;
    parent_name text := target::text;
BEGIN
    part_name := replace(split_part(parent_name, '.', 2) || '_' ||
                         replace(venue_id::text, '-', ''), '.', '_');
    IF to_regclass(format('%I.%I', split_part(parent_name, '.', 1), part_name)) IS NOT NULL THEN
        RETURN;
    END IF;
    EXECUTE format('CREATE TABLE %I.%I PARTITION OF %s FOR VALUES IN (%L)',
                   split_part(parent_name, '.', 1), part_name, target, venue_id);
END
$$;


-- **89 tables qualify today** — a NOT NULL `venue_id` in the schema reference.
-- Listed rather than counted, because ADR-0044's rule is checkable and the list is how.

--   access.access_device
--   access.access_incident
--   access.access_map
--   access.access_point
--   access.access_point_configuration
--   access.access_point_group
--   access.attraction_access
--   access.biometric_audit_event
--   access.biometric_profile
--   access.companion_rule
--   access.credential_issuance_retry_policy
--   access.device_configuration
--   access.edge_node
--   access.edge_package
--   access.face_reenrolment_attempt
--   access.gate_lane
--   access.gate_mode_change
--   access.gate_mode_policy
--   access.gate_outcome_profile
--   access.group_admission_rule
--   access.media_compatibility_test
--   access.offline_policy
--   access.operating_calendar_entry
--   access.parking_facility
--   access.podium
--   access.podium_shift
--   access.scan_event
--   ai.guided_choice_suggestion
--   ai.history_import
--   ai.history_observation
--   ai.venue_settings
--   catalogue.donation_campaign
--   catalogue.event
--   catalogue.price_list
--   catalogue.product
--   catalogue.published_bundle
--   fnb.delivery_location
--   games.card
--   games.game
--   games.prize
--   inventory.item
--   inventory.location
--   inventory.requisition
--   ledger.price_variance
--   maintenance.asset
--   maintenance.incident
--   maintenance.inspection
--   maintenance.work_order
--   marketing.lost_item
--   marketing.review
--   orders.cart
--   orders.deposit_box
--   orders.pos_shift
--   orders.refund_policy
--   orders.reservation
--   orders.sales_order
--   platform.outlet
--   platform.sale_board
--   platform.workstation
--   promotions.bundle
--   promotions.campaign
--   promotions.coupon_campaign
--   promotions.promotion
--   promotions.promotion_alert
--   promotions.promotion_audit
--   promotions.promotion_channel_publication
--   promotions.promotion_conflict
--   promotions.promotion_evaluation_trace
--   promotions.promotion_rule
--   promotions.stacking_rule
--   promotions.voucher_batch
--   queue.queue
--   rental.agreement
--   rental.product
--   resources.resource
--   seating.seat_category
--   seating.seat_map
--   transport.favourite_route
--   transport.network_import
--   transport.pass_type
--   transport.route
--   transport.station
--   venuemap.map
--   venuemap.visit_plan
--   whitelabel.guided_choice
--   workforce.announcement
--   workforce.labour_budget
--   workforce.rota_assignment
--   workforce.staff_conversation
