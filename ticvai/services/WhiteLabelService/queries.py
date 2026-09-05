"""Generated. The declared reads and writes of each operation."""

READS = {
 "claimCustomDomain": [
  "SELECT * FROM control.tenant LIMIT 50",
  "SELECT * FROM whitelabel.custom_domain LIMIT 50"
 ],
 "createBanner": [
  "SELECT * FROM whitelabel.banner LIMIT 50"
 ],
 "createContentBlock": [
  "SELECT * FROM marketing.segment LIMIT 50"
 ],
 "createContentPage": [
  "SELECT * FROM whitelabel.content_page WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createPreview": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "createPromoBlock": [
  "SELECT * FROM whitelabel.promo_block WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "deleteBanner": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "deleteContentPage": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "deletePromoBlock": [
  "SELECT * FROM whitelabel.promo_block WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "diffConfigVersion": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "getAppIcons": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "getBrandIdentity": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "getFeatureToggles": [
  "SELECT * FROM whitelabel.feature_toggle LIMIT 50"
 ],
 "getFonts": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "getHomepageLayout": [
  "SELECT * FROM whitelabel.homepage_section LIMIT 50"
 ],
 "getModuleEnablement": [
  "SELECT * FROM whitelabel.module_enablement LIMIT 50"
 ],
 "getNavigation": [
  "SELECT * FROM whitelabel.navigation_item LIMIT 50"
 ],
 "getTenantAppStatus": [
  "SELECT * FROM whitelabel.config_version WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "getTenantConfig": [
  "SELECT * FROM whitelabel.feature_toggle LIMIT 50",
  "SELECT * FROM whitelabel.homepage_section LIMIT 50",
  "SELECT * FROM whitelabel.module_enablement LIMIT 50",
  "SELECT * FROM whitelabel.navigation_item LIMIT 50",
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "getTheme": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "listBanners": [
  "SELECT * FROM whitelabel.banner LIMIT 50"
 ],
 "listConfigVersions": [
  "SELECT * FROM whitelabel.config_version WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listContentPages": [
  "SELECT * FROM whitelabel.content_page WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listCustomDomains": [
  "SELECT * FROM whitelabel.custom_domain LIMIT 50"
 ],
 "listFaqs": [
  "SELECT * FROM whitelabel.faq_category WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listPolicies": [
  "SELECT * FROM whitelabel.policy WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listPromoBlocks": [
  "SELECT * FROM whitelabel.promo_block WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "publishContentBlock": [
  "SELECT * FROM control.content_block WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "publishTenantConfig": [
  "SELECT * FROM whitelabel.config_version WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "releaseCustomDomain": [
  "SELECT * FROM whitelabel.config_version WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM whitelabel.custom_domain LIMIT 50"
 ],
 "restoreConfigVersion": [
  "SELECT * FROM whitelabel.feature_toggle LIMIT 50",
  "SELECT * FROM whitelabel.homepage_section LIMIT 50",
  "SELECT * FROM whitelabel.module_enablement LIMIT 50",
  "SELECT * FROM whitelabel.navigation_item LIMIT 50",
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "setAppIcons": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "setBrandIdentity": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "setFaqs": [
  "SELECT * FROM whitelabel.faq_category WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setFeatureToggles": [
  "SELECT * FROM whitelabel.feature_toggle LIMIT 50"
 ],
 "setFonts": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "setFooter": [
  "SELECT * FROM control.footer_config WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setHeader": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "setHomepageLayout": [
  "SELECT * FROM whitelabel.homepage_section LIMIT 50"
 ],
 "setLanguages": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "setMaintenanceMode": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "setModuleEnablement": [
  "SELECT * FROM whitelabel.module_enablement LIMIT 50"
 ],
 "setNavigation": [
  "SELECT * FROM whitelabel.navigation_item LIMIT 50"
 ],
 "setPolicy": [
  "SELECT * FROM whitelabel.policy WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setTheme": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "updateBanner": [
  "SELECT * FROM whitelabel.banner LIMIT 50"
 ],
 "updateContentPage": [
  "SELECT * FROM whitelabel.content_page WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "updatePromoBlock": [
  "SELECT * FROM whitelabel.promo_block WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "validateTenantConfig": [
  "SELECT * FROM whitelabel.tenant_config LIMIT 50"
 ],
 "verifyCustomDomain": [
  "SELECT * FROM whitelabel.custom_domain LIMIT 50"
 ]
}

WRITES = {
 "claimCustomDomain": [
  "SELECT id FROM whitelabel.custom_domain ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createBanner": [
  "SELECT id FROM whitelabel.banner ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createContentBlock": [
  "SELECT id FROM control.content_block WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createContentPage": [
  "SELECT id FROM whitelabel.content_page WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPreview": [
  "SELECT id FROM whitelabel.tenant_config ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPromoBlock": [
  "SELECT id FROM whitelabel.promo_block WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "deleteBanner": [
  "SELECT id FROM whitelabel.tenant_config ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "deleteContentPage": [
  "SELECT id FROM whitelabel.tenant_config ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "deletePromoBlock": [
  "SELECT id FROM whitelabel.promo_block WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "publishContentBlock": [
  "SELECT id FROM control.content_block WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "publishTenantConfig": [
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM whitelabel.config_version WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "releaseCustomDomain": [
  "SELECT id FROM whitelabel.custom_domain ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "restoreConfigVersion": [
  "SELECT id FROM whitelabel.feature_toggle ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM whitelabel.homepage_section ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setAppIcons": [
  "SELECT id FROM whitelabel.tenant_config ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setBrandIdentity": [
  "SELECT id FROM whitelabel.tenant_config ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setFaqs": [
  "SELECT id FROM whitelabel.faq_category WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setFeatureToggles": [
  "SELECT id FROM whitelabel.feature_toggle ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setFonts": [
  "SELECT id FROM whitelabel.tenant_config ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setFooter": [
  "SELECT id FROM control.footer_config WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setHeader": [
  "SELECT id FROM whitelabel.tenant_config ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setHomepageLayout": [
  "SELECT id FROM whitelabel.homepage_section ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setLanguages": [
  "SELECT id FROM whitelabel.tenant_config ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setMaintenanceMode": [
  "SELECT id FROM whitelabel.tenant_config ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setModuleEnablement": [
  "SELECT id FROM whitelabel.module_enablement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setNavigation": [
  "SELECT id FROM whitelabel.navigation_item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setPolicy": [
  "SELECT id FROM whitelabel.policy WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setTheme": [
  "SELECT id FROM whitelabel.tenant_config ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateBanner": [
  "SELECT id FROM whitelabel.banner ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateContentPage": [
  "SELECT id FROM whitelabel.content_page WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updatePromoBlock": [
  "SELECT id FROM whitelabel.promo_block WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "validateTenantConfig": [
  "SELECT id FROM whitelabel.tenant_config ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "verifyCustomDomain": [
  "SELECT id FROM whitelabel.custom_domain ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "claimCustomDomain": [
  "cache:idempotency:bench"
 ],
 "createBanner": [
  "cache:idempotency:bench"
 ],
 "createContentBlock": [
  "cache:idempotency:bench"
 ],
 "createContentPage": [
  "cache:idempotency:bench"
 ],
 "createPreview": [
  "cache:idempotency:bench"
 ],
 "createPromoBlock": [
  "cache:idempotency:bench"
 ],
 "deleteBanner": [
  "cache:idempotency:bench"
 ],
 "deleteContentPage": [
  "cache:idempotency:bench"
 ],
 "deletePromoBlock": [
  "cache:idempotency:bench"
 ],
 "getFeatureToggles": [
  "cache:resolution:bench"
 ],
 "getModuleEnablement": [
  "cache:resolution:bench"
 ],
 "getNavigation": [
  "cache:resolution:bench"
 ],
 "getTenantConfig": [
  "cache:resolution:bench"
 ],
 "getTheme": [
  "cache:resolution:bench"
 ],
 "publishContentBlock": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "publishTenantConfig": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "releaseCustomDomain": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "restoreConfigVersion": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setAppIcons": [
  "cache:idempotency:bench"
 ],
 "setBrandIdentity": [
  "cache:idempotency:bench"
 ],
 "setFaqs": [
  "cache:idempotency:bench"
 ],
 "setFeatureToggles": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setFonts": [
  "cache:idempotency:bench"
 ],
 "setFooter": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setHeader": [
  "cache:idempotency:bench"
 ],
 "setHomepageLayout": [
  "cache:idempotency:bench"
 ],
 "setLanguages": [
  "cache:idempotency:bench"
 ],
 "setMaintenanceMode": [
  "cache:idempotency:bench"
 ],
 "setModuleEnablement": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setNavigation": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setPolicy": [
  "cache:idempotency:bench"
 ],
 "setTheme": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "updateBanner": [
  "cache:idempotency:bench"
 ],
 "updateContentPage": [
  "cache:idempotency:bench"
 ],
 "updatePromoBlock": [
  "cache:idempotency:bench"
 ],
 "validateTenantConfig": [
  "cache:idempotency:bench"
 ],
 "verifyCustomDomain": [
  "cache:idempotency:bench"
 ]
}
