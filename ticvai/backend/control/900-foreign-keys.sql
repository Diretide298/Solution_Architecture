-- Declared references inside the control database, applied after every table exists.
-- **Separate file because the schemas cannot be ordered so every reference precedes
-- its use** — orders reaches catalogue, catalogue reaches platform, and something
-- reaches back. Tables first, constraints last, is the only ordering that terminates.
--
-- 24 of 589 declared references. The ones that reach the
-- other database are in ../990-cross-database-references.sql and are not constraints
-- any more.

ALTER TABLE control.api_licence ADD CONSTRAINT fk_api_licence_tenant_id FOREIGN KEY (tenant_id) REFERENCES control.tenant(id);
ALTER TABLE control.cell_job ADD CONSTRAINT fk_cell_job_cell_id FOREIGN KEY (cell_id) REFERENCES control.cell(id);
ALTER TABLE control.environment ADD CONSTRAINT fk_environment_cell_id FOREIGN KEY (cell_id) REFERENCES control.cell(id);
ALTER TABLE control.invoice_line ADD CONSTRAINT fk_invoice_line_invoice_id FOREIGN KEY (invoice_id) REFERENCES control.invoice(id);
ALTER TABLE control.licence_add_on ADD CONSTRAINT fk_licence_add_on_plan_id FOREIGN KEY (plan_id) REFERENCES control.subscription_plan(id);
ALTER TABLE control.migration ADD CONSTRAINT fk_migration_release_id FOREIGN KEY (release_id) REFERENCES control.release(id);
ALTER TABLE control.migration_plan_cell ADD CONSTRAINT fk_migration_plan_cell_cell_id FOREIGN KEY (cell_id) REFERENCES control.cell(id);
ALTER TABLE control.migration_plan_cell ADD CONSTRAINT fk_migration_plan_cell_migration_plan_id FOREIGN KEY (migration_plan_id) REFERENCES control.migration_plan(id);
ALTER TABLE control.migration_run ADD CONSTRAINT fk_migration_run_canary_cell_id FOREIGN KEY (canary_cell_id) REFERENCES control.cell(id);
ALTER TABLE control.migration_run ADD CONSTRAINT fk_migration_run_plan_id FOREIGN KEY (plan_id) REFERENCES control.subscription_plan(id);
ALTER TABLE control.migration_run_cell ADD CONSTRAINT fk_migration_run_cell_migration_run_id FOREIGN KEY (migration_run_id) REFERENCES control.migration_run(id);
ALTER TABLE control.migration_run_tenant ADD CONSTRAINT fk_migration_run_tenant_migration_run_id FOREIGN KEY (migration_run_id) REFERENCES control.migration_run(id);
ALTER TABLE control.onboarding_application ADD CONSTRAINT fk_onboarding_application_venue_type_template_id FOREIGN KEY (venue_type_template_id) REFERENCES control.venue_type_template(id);
ALTER TABLE control.release ADD CONSTRAINT fk_release_plan_id FOREIGN KEY (plan_id) REFERENCES control.subscription_plan(id);
ALTER TABLE control.release_component ADD CONSTRAINT fk_release_component_release_id FOREIGN KEY (release_id) REFERENCES control.release(id);
ALTER TABLE control.rollout ADD CONSTRAINT fk_rollout_release_id FOREIGN KEY (release_id) REFERENCES control.release(id);
ALTER TABLE control.rollout_cell ADD CONSTRAINT fk_rollout_cell_cell_id FOREIGN KEY (cell_id) REFERENCES control.cell(id);
ALTER TABLE control.subscription ADD CONSTRAINT fk_subscription_plan_id FOREIGN KEY (plan_id) REFERENCES control.subscription_plan(id);
ALTER TABLE control.tenant ADD CONSTRAINT fk_tenant_plan_id FOREIGN KEY (plan_id) REFERENCES control.subscription_plan(id);
ALTER TABLE control.tenant ADD CONSTRAINT fk_tenant_subscription FOREIGN KEY (subscription) REFERENCES control.subscription(id);
ALTER TABLE control.tenant_migration ADD CONSTRAINT fk_tenant_migration_plan_id FOREIGN KEY (plan_id) REFERENCES control.tenant_migration_plan(id);
ALTER TABLE control.tenant_migration ADD CONSTRAINT fk_tenant_migration_tenant_id FOREIGN KEY (tenant_id) REFERENCES control.tenant(id);
ALTER TABLE control.tenant_migration_plan ADD CONSTRAINT fk_tenant_migration_plan_tenant_id FOREIGN KEY (tenant_id) REFERENCES control.tenant(id);
ALTER TABLE control.webhook_delivery ADD CONSTRAINT fk_webhook_delivery_subscription_id FOREIGN KEY (subscription_id) REFERENCES control.subscription(id);
