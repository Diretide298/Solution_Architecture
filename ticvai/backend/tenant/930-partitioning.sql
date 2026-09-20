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
-- `scope_level` column here is `text`, derived from contracts that declare it as a string.
-- **Emitting an unused type would imply a constraint nothing enforces**, so the gap is named here
-- instead: scope levels are validated by the application, not by the database.
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


-- **34 tables qualify today** — a NOT NULL `venue_id` in the schema reference.
-- Listed rather than counted, because ADR-0044's rule is checkable and the list is how.

--   access.access_point
--   access.parking_facility
--   access.scan_event
--   catalogue.donation_campaign
--   catalogue.event
--   catalogue.price_list
--   catalogue.product
--   catalogue.published_bundle
--   fnb.delivery_location
--   games.card
--   games.game
--   games.prize
--   inventory.location
--   inventory.requisition
--   ledger.price_variance
--   maintenance.inspection
--   marketing.lost_item
--   orders.cart
--   orders.deposit_box
--   orders.pos_shift
--   orders.refund_policy
--   orders.reservation
--   orders.sales_order
--   platform.outlet
--   platform.sale_board
--   platform.workstation
--   rental.agreement
--   rental.product
--   resources.resource
--   seating.seat_category
--   seating.seat_map
--   venuemap.map
--   workforce.announcement
--   workforce.rota_assignment
