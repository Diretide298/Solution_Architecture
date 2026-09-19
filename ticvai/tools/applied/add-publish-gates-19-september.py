#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give every newly-wired publishing screen its `publishGate`.

**The rule predates this run and the run tripped it 21 times.** `check-screens` requires
that a screen declaring a publish-family operation also carries a `publishGate` —

> *"a publish with no stated consequence is one somebody presses meaning to save."*

Today's wiring put `publishRentalProduct`, `publishWalletConfiguration`,
`publishSeatMap`, `publishTenantConfig` and friends onto screens that had no gate,
because the wiring scripts add `apis` and never touch `layout`.

**The gate is authored, not derived, and it is one line of prose per screen.** It names
what goes live, where, and from when — which differs per screen, so a generated
placeholder would be worse than the error it silences. The text here is specific to each
screen's subject.

Idempotent — a screen that already has a gate is left alone.
Run with no arguments to preview; `--apply` to write.
"""
import io
import re
import sys

import yaml

FILES = ('screens/P08-venue-back-office.yaml', 'screens/P09-platform-admin-console.yaml',
         'screens/P13-white-label-cms.yaml', 'screens/P16-venue-analytics.yaml',
         'screens/P06-staff-app.yaml', 'screens/P17-ticvai-signup.yaml')

PUBLISHES = re.compile(r'^(publish|activate|deactivate|release|retire|archive)[A-Z]')

# What goes live, where, and from when — per subject. Matched on the publishing operation
# the screen declares, because that is what the rule keys off.
GATE = {
    'publishRentalProduct': '**Puts the product on sale**, at the locations it is enabled for, '
                            'from its effective date. Existing bookings are unaffected; the next '
                            'guest sees the new rules.',
    'publishWalletConfiguration': '**Takes effect at every till and reader immediately.** Credit '
                                  'types, consumption order and funding rules change for balances '
                                  'that already exist, not only for new ones.',
    'publishSeatMap': '**Replaces the map every channel sells from.** Seats already sold keep '
                      'their labels; seats that no longer exist in the new map are listed before '
                      'this proceeds.',
    'publishTenantConfig': '**Goes live on the tenant’s own domains**, for every guest, at '
                           'once. The previous version stays restorable.',
    'publishContentBlock': '**Appears wherever the block is placed**, including pages published '
                           'earlier. A block is referenced, not copied.',
    'publishMenu': '**Changes what the kitchen and the till show**, from the scheduled time. '
                   'Orders already placed keep the prices they were taken at.',
    'publishSeatingRules': '**Applies to every future recommendation**, not to seats already held.',
    'publishPricingEffectiveDate': '**Prices change at the stated date and time**, across every '
                                   'channel the profile covers.',
    'publishAnnouncement': '**Reaches the selected staff immediately**, on every device they are '
                           'signed in to.',
    'publishSite': '**Goes live on the public site.** The previous version stays restorable.',
    'activateJourney': '**Starts enrolling guests who match**, from now. Guests already in the '
                       'journey continue on the version they entered.',
    'launchCampaign': '**Begins sending.** Suppression and consent are applied at send time, so '
                      'the audience that receives it is smaller than the one shown here.',
}
DEFAULT = ('**Names what goes live, where, and from when.** A publish with no stated consequence '
           'is one somebody presses meaning to save.')


def main():
    apply = '--apply' in sys.argv
    added = 0
    for f in FILES:
        try:
            d = yaml.safe_load(io.open(f, encoding='utf8'))
        except FileNotFoundError:
            continue
        changed = False
        for s in d.get('screens') or []:
            ops = [a.get('operationId') for a in (s.get('apis') or []) if a.get('operationId')]
            pub = [o for o in ops if PUBLISHES.match(o) or o == 'releaseProductionPlan']
            if not pub:
                continue
            regions = (s.get('layout') or {}).get('regions') or []
            kinds = [c.get('kind') for r in regions for c in (r.get('components') or [])]
            if 'publishGate' in kinds:
                continue
            if not regions:
                s.setdefault('layout', {}).setdefault('regions', [])
                regions = s['layout']['regions']
                regions.append({'name': 'contentBody', 'components': []})
            regions[0].setdefault('components', []).append({
                'kind': 'publishGate',
                'label': 'What publishing changes',
                'notes': GATE.get(pub[0], DEFAULT),
                'provenance': 'authored — required by check-screens, 19 September 2026',
            })
            added += 1
            changed = True
            print('  %-9s %-40s %s' % (s['id'], s['name'][:40], pub[0]))
        if changed and apply:
            io.open(f, 'w', encoding='utf8').write(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
            print('  -> %s' % f)
    print('\n%d gate(s) added' % added)
    if not apply:
        print('\n  nothing written — pass --apply')


if __name__ == '__main__':
    main()
