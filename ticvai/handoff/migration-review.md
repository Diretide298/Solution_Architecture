# Migration changes for a person

**Written by `tools/derive-ddl.py` in frozen mode (20261002). Do not edit; it is rewritten on every run.**

The baseline migrations under `backend/` are frozen at `r1 (a1ba956)` (`tools/check-migration-freeze.py`). `derive-ddl.py` writes additive changes (new tables, columns and indexes) as the next forward migration, `backend/<area>/V<nnnn>__*.sql`. **The changes below it does not write**, because each has a data question behind it: which rows survive a drop, what fills a new NOT NULL column, whether a rename is a rename. Write each as a forward migration by hand; once a forward migration carries it, it leaves this list.

**5 change(s).**

| Kind | Database | Object | Change | What a person does |
|---|---|---|---|---|
| constraint added | control | `control.outbox_republish outbox_republish_tenant_id_fkey` | `ALTER TABLE control.outbox_republish ADD CONSTRAINT outbox_republish_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES control.tenant(id)` | existing rows may violate it: validate, then add by hand (NOT VALID, then VALIDATE) |
| constraint added | tenant | `access.device_placement device_placement_device_id_fkey` | `ALTER TABLE access.device_placement ADD CONSTRAINT device_placement_device_id_fkey FOREIGN KEY (device_id) REFERENCES platform.device(id)` | existing rows may violate it: validate, then add by hand (NOT VALID, then VALIDATE) |
| constraint added | tenant | `access.podium_shift podium_shift_access_device_id_fkey` | `ALTER TABLE access.podium_shift ADD CONSTRAINT podium_shift_access_device_id_fkey FOREIGN KEY (access_device_id) REFERENCES platform.device(id)` | existing rows may violate it: validate, then add by hand (NOT VALID, then VALIDATE) |
| constraint added | tenant | `catalogue.waiting_room_setting waiting_room_setting_performance_id_fkey` | `ALTER TABLE catalogue.waiting_room_setting ADD CONSTRAINT waiting_room_setting_performance_id_fkey FOREIGN KEY (performance_id) REFERENCES catalogue.performance(id)` | existing rows may violate it: validate, then add by hand (NOT VALID, then VALIDATE) |
| constraint added | tenant | `catalogue.waiting_room_setting waiting_room_setting_updated_by_principal_id_fkey` | `ALTER TABLE catalogue.waiting_room_setting ADD CONSTRAINT waiting_room_setting_updated_by_principal_id_fkey FOREIGN KEY (updated_by_principal_id) REFERENCES identity.principal(id)` | existing rows may violate it: validate, then add by hand (NOT VALID, then VALIDATE) |
