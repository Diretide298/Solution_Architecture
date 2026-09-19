#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wire the DAM and Upsell/Cross-Sell boards to their extended contracts.

Both packs were `AUTHOR` on the scope test and both now have the operations. Two
things are worth recording about what the authoring found:

**`assets` already had `MediaRights` and I nearly wrote a second one.** The splice
guard refused. The existing schema tracked *what the licence is*; the board asks for
*where it may go and who renews it*, so the four missing fields were added to the
schema that existed rather than a rival being defined beside it.

**`promotions` already had `getRecommendations`.** Same guard, same near-miss, and
this one matters more: the runtime recommendation call exists and works, and what the
Upsell pack actually lacks is everything around it — strategies, product
relationships, measured affinity, outcome recording, experiments and suppression. The
call that looked like the centre of the pack was the one part already built.

The DAM permissions are `ASSET_LIBRARY_*` and not `ASSET_*`; the latter are physical
assets in `maintenance`. Collapsing them would have given whoever services a turnstile
the right to publish the brand library.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import sys

import yaml

FILES = ('screens/P13-white-label-cms.yaml', 'screens/P09-platform-admin-console.yaml')

WIRING = {
    # ------------------------------------------------ DAM, board 1: the library
    'CMS-061': [('searchMedia', 'assets', 'The estate, counted and charted', 'onLoad'),
                ('getMediaUsageAnalytics', 'assets', 'Storage, uploads and library health', 'onLoad')],
    'CMS-062': [('searchMedia', 'assets', 'Browse and filter the library', 'onLoad'),
                ('listCollections', 'assets', 'Collections to file into', 'onLoad')],
    'CMS-063': [('createUpload', 'assets', 'Start an upload', 'onAction'),
                ('completeUpload', 'assets', 'Finish it', 'onAction'),
                ('analyseMediaAsset', 'assets', 'Auto-tag on ingest', 'onAction')],
    'CMS-064': [('listCollections', 'assets', 'Folders and collections', 'onLoad'),
                ('createCollection', 'assets', 'Create one', 'onAction')],
    'CMS-065': [('getMediaTaxonomy', 'assets', 'Categories and metadata fields', 'onLoad'),
                ('setMediaTaxonomy', 'assets', 'Define them', 'onAction')],
    'CMS-066': [('setMediaAssetTags', 'assets', 'Tags and keywords, with their origin', 'onAction'),
                ('getMediaTaxonomy', 'assets', 'The controlled vocabularies', 'onLoad')],
    'CMS-067': [('searchMedia', 'assets', 'Advanced search', 'onLoad')],
    'CMS-068': [('getMediaAsset', 'assets', 'The asset, in full', 'onLoad'),
                ('listMediaAssetVersions', 'assets', 'Its revisions', 'onLoad'),
                ('getMediaDistribution', 'assets', 'Where it is used', 'onLoad')],
    'CMS-069': [('bulkUpdateMediaAssets', 'assets', 'Retag, reclassify or archive many', 'onAction')],
    'CMS-070': [('getMediaUsageAnalytics', 'assets', 'Activity and library health', 'onLoad')],

    # ------------------------------------------- DAM, board 2: intelligence
    'CMS-071': [('getMediaUsageAnalytics', 'assets', 'What the library looks like to AI', 'onLoad')],
    'CMS-072': [('analyseMediaAsset', 'assets', 'Auto-tag and describe', 'onAction'),
                ('setMediaAssetTags', 'assets', 'Promote the proposals', 'onAction')],
    'CMS-073': [('searchMedia', 'assets', 'Semantic search', 'onLoad')],
    'CMS-074': [('findSimilarMediaAssets', 'assets', 'Visually similar and related', 'onLoad')],
    'CMS-075': [('findSimilarMediaAssets', 'assets', 'Duplicates above the threshold', 'onLoad'),
                ('deleteMediaAsset', 'assets', 'Retire the copy', 'onAction')],
    'CMS-076': [('listMediaAssetVersions', 'assets', 'Revision history', 'onLoad'),
                ('replaceMediaAsset', 'assets', 'Replace the current version', 'onAction')],
    'CMS-077': [('listMediaAssetVersions', 'assets', 'Two versions, and what replacing breaks',
                 'onLoad')],
    'CMS-078': [('listMediaRenditions', 'assets', 'The derived sizes', 'onLoad'),
                ('requestMediaRendition', 'assets', 'Generate one', 'onAction')],
    'CMS-079': [('listMediaRenditions', 'assets', 'Processing state and readiness', 'onLoad')],
    'CMS-080': [('getMediaUsageAnalytics', 'assets', 'Quality and coverage', 'onLoad')],

    # -------------------------------------- DAM, board 3: governance and rights
    'CMS-081': [('getExpiringRights', 'assets', 'Rights about to lapse', 'onLoad'),
                ('getMediaUsageAnalytics', 'assets', 'Governance coverage', 'onLoad')],
    'CMS-082': [('updateMediaAsset', 'assets', 'Set owner and responsibility', 'onAction'),
                ('getMediaAsset', 'assets', 'The asset being assigned', 'onLoad')],
    'CMS-083': [('setMediaAssetRights', 'assets', 'Licence, territory, channel and expiry',
                 'onAction')],
    'CMS-084': [('setMediaAssetApproval', 'assets', 'Submit, approve or reject', 'onAction')],
    'CMS-085': [('setMediaAssetApproval', 'assets', 'Publication eligibility, computed', 'onLoad')],
    'CMS-086': [('listAccessPolicies', 'identity', 'Who may see which assets', 'onLoad'),
                ('createAccessPolicy', 'identity', 'Write an asset access policy', 'onAction')],
    'CMS-087': [('createMediaShare', 'assets', 'Share externally, on terms', 'onAction')],
    'CMS-088': [('getExpiringRights', 'assets', 'What lapses, and what it would break', 'onLoad'),
                ('setMediaAssetRights', 'assets', 'Renew', 'onAction')],
    'CMS-089': [('listMediaAssetAudit', 'assets', 'Edits and distribution together', 'onLoad')],
    'CMS-090': [('getExpiringRights', 'assets', 'Risk from lapsing rights', 'onLoad')],

    # ------------------------------------ DAM, board 4: distribution and delivery
    'CMS-091': [('getMediaDistribution', 'assets', 'Delivery across channels', 'onLoad')],
    'CMS-092': [('getMediaDistribution', 'assets', 'Where each asset appears', 'onLoad')],
    'CMS-093': [('setMediaDistributionChannels', 'assets', 'CDN, signing and defaults', 'onAction')],
    'CMS-094': [('setMediaDistributionChannels', 'assets', 'Signed URLs and rendition delivery',
                 'onAction'),
                ('listMediaRenditions', 'assets', 'What can be delivered', 'onLoad')],
    'CMS-095': [('replaceMediaAsset', 'assets', 'Replace and propagate', 'onAction'),
                ('getMediaDistribution', 'assets', 'Everywhere it would propagate to', 'onLoad')],
    'CMS-096': [('setMediaDistributionChannels', 'assets', 'Fallback and expiry behaviour',
                 'onAction')],
    'CMS-097': [('getMediaDistribution', 'assets', 'What the API exposes', 'onLoad')],
    'CMS-098': [('getMediaUsageAnalytics', 'assets', 'Delivery health', 'onLoad')],
    'CMS-099': [('getMediaUsageAnalytics', 'assets', 'Usage and performance', 'onLoad')],
    'CMS-100': [('getMediaUsageAnalytics', 'assets', 'Distribution intelligence', 'onLoad')],

    # ---------------------------------- Upsell, board 1: recommendation strategy
    'ADM-639': [('listRecommendationStrategies', 'promotions', 'Strategies in force', 'onLoad'),
                ('getRecommendationPerformance', 'promotions', 'How they are doing', 'onLoad')],
    'ADM-640': [('listRecommendationStrategies', 'promotions', 'The strategies', 'onLoad'),
                ('createRecommendationStrategy', 'promotions', 'Define one', 'onAction'),
                ('updateRecommendationStrategy', 'promotions', 'Change one', 'onAction')],
    'ADM-641': [('updateRecommendationStrategy', 'promotions', 'Objective and KPI', 'onAction')],
    'ADM-642': [('listProductRelationships', 'promotions', 'Ladders and cross-sells', 'onLoad'),
                ('setProductRelationships', 'promotions', 'Declare them', 'onAction')],
    'ADM-643': [('updateRecommendationStrategy', 'promotions', 'Placements and touchpoints',
                 'onAction')],
    'ADM-644': [('updateRecommendationStrategy', 'promotions', 'Channels and journey', 'onAction')],
    'ADM-645': [('setRecommendationSuppression', 'promotions', 'Caps, fatigue and exclusions',
                 'onAction'),
                ('updateRecommendationStrategy', 'promotions', 'Priority and ranking', 'onAction')],
    'ADM-646': [('updateRecommendationStrategy', 'promotions', 'Commercial guardrails', 'onAction')],
    'ADM-647': [('listRecommendationStrategies', 'promotions', 'Policy and governance', 'onLoad')],
    'ADM-648': [('simulateRecommendationStrategy', 'promotions', 'Replay against history',
                 'onAction')],

    # ----------------------------------------- Upsell, board 2: upsell and upgrade
    'ADM-649': [('getRecommendationPerformance', 'promotions', 'Upgrade performance', 'onLoad')],
    'ADM-650': [('listProductRelationships', 'promotions', 'The ladder', 'onLoad'),
                ('setProductRelationships', 'promotions', 'Order it', 'onAction')],
    'ADM-651': [('updateRecommendationStrategy', 'promotions', 'Eligibility and qualification',
                 'onAction')],
    'ADM-652': [('quoteUpgrade', 'promotions', 'The price gap, and what the guest gains', 'onAction')],
    'ADM-653': [('quoteUpgrade', 'promotions', 'Ticket, experience and bundle upgrades', 'onAction')],
    'ADM-654': [('quoteUpgrade', 'promotions', 'Membership and pass upgrades', 'onAction')],
    'ADM-655': [('updateRecommendationStrategy', 'promotions', 'Cart and checkout placements',
                 'onAction')],
    'ADM-656': [('updateRecommendationStrategy', 'promotions', 'Post-purchase placements',
                 'onAction'),
                ('quoteUpgrade', 'promotions', 'Upgrade after the fact', 'onAction')],
    'ADM-657': [('getRecommendationPerformance', 'promotions', 'Propensity and opportunity',
                 'onLoad')],
    'ADM-658': [('simulateRecommendationStrategy', 'promotions', 'Simulate the ladder', 'onAction')],

    # -------------------------------------------- Upsell, board 3: cross-sell
    'ADM-659': [('getRecommendationPerformance', 'promotions', 'Cross-sell performance', 'onLoad')],
    'ADM-660': [('setProductRelationships', 'promotions', 'Build the relationships', 'onAction')],
    'ADM-661': [('getProductAffinity', 'promotions', 'The affinity matrix, measured', 'onLoad')],
    'ADM-662': [('getProductAffinity', 'promotions', 'Frequently bought together, with lift',
                 'onLoad')],
    'ADM-663': [('setProductRelationships', 'promotions', 'Across categories', 'onAction')],
    'ADM-664': [('setProductRelationships', 'promotions', 'Across attractions and partners',
                 'onAction')],
    'ADM-665': [('updateRecommendationStrategy', 'promotions', 'Exclude what is in the basket',
                 'onAction')],
    'ADM-666': [('updateRecommendationStrategy', 'promotions', 'Require availability', 'onAction')],
    'ADM-667': [('getProductAffinity', 'promotions', 'Discovery and scoring', 'onLoad')],
    'ADM-668': [('simulateRecommendationStrategy', 'promotions', 'Simulate cross-sell', 'onAction')],

    # --------------------------------------- Upsell, board 4: journey and context
    'ADM-669': [('getRecommendationPerformance', 'promotions', 'By journey stage', 'onLoad')],
    'ADM-670': [('listRecommendationStrategies', 'promotions', 'Touchpoints in use', 'onLoad')],
    'ADM-671': [('updateRecommendationStrategy', 'promotions', 'Context rules', 'onAction')],
    'ADM-672': [('updateRecommendationStrategy', 'promotions', 'Pre-purchase placements',
                 'onAction')],
    'ADM-673': [('updateRecommendationStrategy', 'promotions', 'Pre-visit placements', 'onAction')],
    'ADM-674': [('updateRecommendationStrategy', 'promotions', 'In-venue and location-aware',
                 'onAction')],
    'ADM-675': [('updateRecommendationStrategy', 'promotions', 'Visit state and timing', 'onAction')],
    'ADM-676': [('listRecommendationStrategies', 'promotions', 'Across channels', 'onLoad')],
    'ADM-677': [('setRecommendationSuppression', 'promotions', 'Triggers and frequency', 'onAction')],
    'ADM-678': [('explainRecommendation', 'promotions', 'The decision trace', 'onAction'),
                ('simulateRecommendationStrategy', 'promotions', 'Simulate the journey', 'onAction')],

    # ------------------------------------ Upsell, board 5: personalisation and NBO
    'ADM-679': [('getRecommendationPerformance', 'promotions', 'Personalisation performance',
                 'onLoad')],
    'ADM-680': [('getGuestProfile', 'marketing-crm', 'The guest behind the recommendation',
                 'onLoad'),
                ('explainRecommendation', 'promotions', 'What we would offer them', 'onAction')],
    'ADM-681': [('updateRecommendationStrategy', 'promotions', 'Which signals count', 'onAction')],
    'ADM-682': [('getRecommendationPerformance', 'promotions', 'Propensity and intent', 'onLoad')],
    'ADM-683': [('updateRecommendationStrategy', 'promotions', 'Next-best-offer policy', 'onAction'),
                ('explainRecommendation', 'promotions', 'Trace a decision', 'onAction')],
    'ADM-684': [('updateRecommendationStrategy', 'promotions', 'Ranking and decision policy',
                 'onAction')],
    'ADM-685': [('setRecommendationSuppression', 'promotions', 'Preference, fatigue, suppression',
                 'onAction')],
    'ADM-686': [('explainRecommendation', 'promotions', 'Anonymous and known, side by side',
                 'onAction')],
    'ADM-687': [('explainRecommendation', 'promotions', 'Factors and confidence', 'onAction')],
    'ADM-688': [('simulateRecommendationStrategy', 'promotions', 'The NBO lab', 'onAction')],

    # ------------------------------------------- Upsell, board 6: performance
    'ADM-689': [('getRecommendationPerformance', 'promotions', 'The headline numbers', 'onLoad')],
    'ADM-690': [('getRecommendationPerformance', 'promotions', 'By strategy and placement',
                 'onLoad')],
    'ADM-691': [('listRecommendationExperiments', 'promotions', 'Experiments running', 'onLoad'),
                ('createRecommendationExperiment', 'promotions', 'Start one', 'onAction')],
    'ADM-692': [('listRecommendationExperiments', 'promotions', 'Results so far', 'onLoad'),
                ('concludeRecommendationExperiment', 'promotions', 'Declare a winner', 'onAction')],
    'ADM-693': [('getRecommendationPerformance', 'promotions', 'Attributed against incremental',
                 'onLoad')],
    'ADM-694': [('getRecommendationPerformance', 'promotions', 'Model performance over time',
                 'onLoad')],
    'ADM-695': [('listRecommendationStrategies', 'promotions', 'What is deployed where', 'onLoad'),
                ('updateRecommendationStrategy', 'promotions', 'Pause or retire', 'onAction')],
    'ADM-696': [('explainRecommendation', 'promotions', 'Explainability and safety', 'onAction')],
    'ADM-697': [('explainRecommendation', 'promotions', 'Investigate one decision', 'onAction')],
    'ADM-698': [('simulateRecommendationStrategy', 'promotions', 'Optimisation lab', 'onAction')],
}

INVALIDATES = {
    'setMediaTaxonomy': ['getMediaTaxonomy'],
    'setMediaAssetTags': ['searchMedia', 'getMediaAsset'],
    'analyseMediaAsset': ['getMediaAsset'],
    'requestMediaRendition': ['listMediaRenditions'],
    'setMediaAssetRights': ['getMediaAsset', 'getExpiringRights'],
    'setMediaAssetApproval': ['getMediaAsset', 'searchMedia'],
    'createMediaShare': ['listMediaAssetAudit'],
    'setMediaDistributionChannels': ['getMediaDistribution'],
    'bulkUpdateMediaAssets': ['searchMedia', 'getMediaUsageAnalytics'],
    'replaceMediaAsset': ['listMediaAssetVersions', 'getMediaDistribution'],
    'createUpload': ['searchMedia'],
    'completeUpload': ['searchMedia', 'getMediaUsageAnalytics'],
    'createCollection': ['listCollections'],
    'deleteMediaAsset': ['searchMedia'],
    'createRecommendationStrategy': ['listRecommendationStrategies'],
    'updateRecommendationStrategy': ['listRecommendationStrategies'],
    'setProductRelationships': ['listProductRelationships'],
    'setRecommendationSuppression': ['listRecommendationStrategies'],
    'createRecommendationExperiment': ['listRecommendationExperiments'],
    'concludeRecommendationExperiment': ['listRecommendationExperiments',
                                         'listRecommendationStrategies'],
}


def main():
    apply = '--apply' in sys.argv
    added = 0
    touched = []
    missing = set(WIRING)
    for f in FILES:
        d = yaml.safe_load(io.open(f, encoding='utf8'))
        by_id = {s['id']: s for s in d['screens']}
        changed = False
        for sid, ops in sorted(WIRING.items()):
            s = by_id.get(sid)
            if not s:
                continue
            missing.discard(sid)
            have = {a.get('operationId') for a in (s.get('apis') or [])}
            new = []
            for oid, contract, purpose, trigger in ops:
                if oid in have:
                    continue
                entry = {'operationId': oid, 'contract': contract,
                         'purpose': purpose, 'trigger': trigger,
                         'provenance': 'board reading, 19 September 2026'}
                if INVALIDATES.get(oid):
                    entry['invalidates'] = INVALIDATES[oid]
                new.append(entry)
            if new:
                s.setdefault('apis', []).extend(new)
                added += len(new)
                changed = True
                touched.append((sid, s['name'], [n['operationId'] for n in new]))
        if changed and apply:
            io.open(f, 'w', encoding='utf8').write(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
            print('  -> %s' % f)

    for sid, name, ops in touched:
        print('  %-9s %-46s %s' % (sid, name[:46], ', '.join(ops)))
    if missing:
        print('\n  NOT FOUND: %s' % ', '.join(sorted(missing)))
    print('\n%d reference(s) across %d screen(s)' % (added, len(touched)))
    if not apply:
        print('\n  nothing written — pass --apply')


if __name__ == '__main__':
    main()
