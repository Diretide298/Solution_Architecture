#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Take `bookResource` off the two guest surfaces, per the 26 August minute.

**`check-screens` caught this, which is the system working.** `bookResource` became
staff-only earlier today when the minute was finally read:

> *"a guest always books a product or package — **never a resource directly, and never a
> specific room/vehicle/instructor by itself** — across all sales channels."*

The contract changed and two guest screens kept calling it, so the checker reported a
guest surface declaring an operation carrying a staff permission. **That is the contract
layer doing its job**: a decision taken in one place surfaced as an error in another
three steps away.

**Nothing is lost, which is why this is safe.** Both screens already carry
`createTableReservation` and `updateTableReservation` — the product-mediated path the
minute describes. The guest books a table or a cabana *product*; `allocateResources`
picks which cabana, rotating across the pool per the same minute.

`getResourceAvailability` stays. A guest may see when something is free; what they may
not do is address a specific resource to book it.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import sys

import yaml

TARGETS = (('screens/P01-guest-web-storefront.yaml', 'WEB-031'),
           ('screens/P02-guest-mobile-app.yaml', 'GST-070'))


def main():
    apply = '--apply' in sys.argv
    removed = 0
    for f, sid in TARGETS:
        d = yaml.safe_load(io.open(f, encoding='utf8'))
        changed = False
        for s in d['screens']:
            if s['id'] != sid:
                continue
            before = len(s.get('apis') or [])
            s['apis'] = [a for a in (s.get('apis') or [])
                         if a.get('operationId') != 'bookResource']
            gone = before - len(s['apis'])
            if gone:
                removed += gone
                changed = True
                left = [a.get('operationId') for a in s['apis']]
                print('  %-9s %-34s -%d, keeps %s' % (sid, s['name'][:34], gone,
                                                      ', '.join(left[:4])))
        if changed and apply:
            io.open(f, 'w', encoding='utf8').write(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
            print('  -> %s' % f)
    print('\n%d reference(s) removed' % removed)
    if not apply:
        print('\n  nothing written — pass --apply')


if __name__ == '__main__':
    main()
