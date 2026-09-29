-- Declared references inside the control database, applied after every table exists.
-- **Separate file because the schemas cannot be ordered so every reference precedes
-- its use** — orders reaches catalogue, catalogue reaches platform, and something
-- reaches back. Tables first, constraints last, is the only ordering that terminates.
--
-- 24 of 778 declared references. The ones that reach the
-- other database are in ../990-cross-database-references.sql and are not constraints
-- any more.

ALTER TABLE control.api_licence ADD CONSTRAINT api_licence_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES control.tenant(id);
ALTER TABLE control.cell_job ADD CONSTRAINT cell_job_cell_id_fkey FOREIGN KEY (cell_id) REFERENCES control.cell(id);
ALTER TABLE control.credit_note_line ADD CONSTRAINT credit_note_line_credit_note_id_fkey FOREIGN KEY (credit_note_id) REFERENCES control.credit_note(id);
ALTER TABLE control.environment ADD CONSTRAINT environment_cell_id_fkey FOREIGN KEY (cell_id) REFERENCES control.cell(id);
ALTER TABLE control.invoice_line ADD CONSTRAINT invoice_line_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES control.invoice(id);
ALTER TABLE control.licence_add_on_limit ADD CONSTRAINT licence_add_on_limit_licence_add_on_id_fkey FOREIGN KEY (licence_add_on_id) REFERENCES control.licence_add_on(id);
ALTER TABLE control.migration ADD CONSTRAINT migration_release_id_fkey FOREIGN KEY (release_id) REFERENCES control.release(id);
ALTER TABLE control.migration_plan_cell ADD CONSTRAINT migration_plan_cell_cell_id_fkey FOREIGN KEY (cell_id) REFERENCES control.cell(id);
ALTER TABLE control.migration_plan_cell ADD CONSTRAINT migration_plan_cell_migration_plan_id_fkey FOREIGN KEY (migration_plan_id) REFERENCES control.migration_plan(id);
ALTER TABLE control.migration_run ADD CONSTRAINT migration_run_canary_cell_id_fkey FOREIGN KEY (canary_cell_id) REFERENCES control.cell(id);
ALTER TABLE control.migration_run_cell ADD CONSTRAINT migration_run_cell_migration_run_id_fkey FOREIGN KEY (migration_run_id) REFERENCES control.migration_run(id);
ALTER TABLE control.migration_run_tenant ADD CONSTRAINT migration_run_tenant_migration_run_id_fkey FOREIGN KEY (migration_run_id) REFERENCES control.migration_run(id);
ALTER TABLE control.onboarding_application ADD CONSTRAINT onboarding_application_venue_type_template_id_fkey FOREIGN KEY (venue_type_template_id) REFERENCES control.venue_type_template(id);
ALTER TABLE control.partner_agreement ADD CONSTRAINT partner_agreement_partner_id_fkey FOREIGN KEY (partner_id) REFERENCES control.partner(id);
ALTER TABLE control.partner_application_review_task ADD CONSTRAINT partner_application_review_task_partner_application_id_fkey FOREIGN KEY (partner_application_id) REFERENCES control.partner_application(id);
ALTER TABLE control.partner_commission_rule_tier ADD CONSTRAINT partner_commission_rule_tier_partner_commission_rule_id_fkey FOREIGN KEY (partner_commission_rule_id) REFERENCES control.partner_commission_rule(id);
ALTER TABLE control.partner_rate_volume_band ADD CONSTRAINT partner_rate_volume_band_partner_rate_id_fkey FOREIGN KEY (partner_rate_id) REFERENCES control.partner_rate(id);
ALTER TABLE control.partner_user ADD CONSTRAINT partner_user_partner_id_fkey FOREIGN KEY (partner_id) REFERENCES control.partner(id);
ALTER TABLE control.release_component ADD CONSTRAINT release_component_release_id_fkey FOREIGN KEY (release_id) REFERENCES control.release(id);
ALTER TABLE control.rollout ADD CONSTRAINT rollout_release_id_fkey FOREIGN KEY (release_id) REFERENCES control.release(id);
ALTER TABLE control.rollout_cell ADD CONSTRAINT rollout_cell_cell_id_fkey FOREIGN KEY (cell_id) REFERENCES control.cell(id);
ALTER TABLE control.tenant_migration ADD CONSTRAINT tenant_migration_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES control.tenant_migration_plan(id);
ALTER TABLE control.tenant_migration ADD CONSTRAINT tenant_migration_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES control.tenant(id);
ALTER TABLE control.tenant_migration_plan ADD CONSTRAINT tenant_migration_plan_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES control.tenant(id);
