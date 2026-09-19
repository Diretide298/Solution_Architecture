#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Three screens whose only operation was read off their own title.

`check-screens` calls this out precisely:

> *"declares one operation and it is its own title with 'list' in front — the
> declaration was read off the name, so it is evidence of nothing about what the screen
> does."*

**It is the title-matcher failure this whole run was about, surviving in three corners.**
A `Dashboard Library` that declares `listDashboards` has said nothing: every library
lists the thing it is a library of. What makes it a screen is what you can *do* there.

So each gains the operation it exists for, from the board:

    ANL-021  Dashboard Library          you open one, and you start a new one
    EMP-088  Overdue Rental Management  you contact the guest — that is the whole job
    SGN-005  Sales Channel Assessment   the answers are scored, not just listed

**`listSaleChannel` on SGN-005 is worth a note.** It is one of three operations dropped
earlier in this run to clear checker errors, and later found to exist in the contracts
after all. It stays; what it lacked was the act beside it.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import sys

import yaml

WIRING = {
    'screens/P16-venue-analytics.yaml': {
        'ANL-021': [('getDashboard', 'reporting', 'Open one', 'onAction'),
                    ('createDashboard', 'reporting', 'Start a new one', 'onAction')],
    },
    'screens/P08-venue-back-office.yaml': {
        # Board 7.8. The list is the prompt; contacting the guest is the work.
        #
        # **BO-561 is the master; EMP-088 is its twin.** The first cut wrote EMP-088 and
        # `check-screens` reported the drift — the third time in this run that a twin was
        # edited instead of its master. `apply-rental-staff-app.py` copies it across.
        #
        # **`returnRental` was here and does not belong.** It takes a `bookingId`, which an
        # overdue *list* has no way to supply, and the checker said so: *"calls operations
        # needing bookingId and its entryState declares none — the screen cannot know what
        # it is showing."* Closing a rental out happens on the return screens, which have
        # the booking. Dropping it is the fix, not a workaround for the error.
        'BO-561': [('sendTransactionalMessage', 'marketing-crm',
                    'Contact the guest about an overdue rental', 'onAction')],
    },
    'screens/P09-platform-admin-console.yaml': {
        # Licensing board 2.5 — one of ten assessment screens, and the answers feed
        # the VSI score that produces the package.
        #
        # **ADM-383 is the master and SGN-005 is its `source.sameAs` twin.** Writing the
        # twin alone is what `check-screens` caught the first time this ran: the pair must
        # stay byte-identical, so the master is edited and
        # `apply-subscription-placement.py` copies it across. Editing the twin directly
        # would be overwritten by the next placement run anyway.
        'ADM-383': [('scoreVsiAssessment', 'subscription',
                     'Record the answers and score them', 'onAction')],
    },
}

INVALIDATES = {
    'createDashboard': ['listDashboards'],
    'returnRental': ['listOverdueRentals', 'listRentalBookings'],
}


def main():
    apply = '--apply' in sys.argv
    added = 0
    for f, screens in WIRING.items():
        d = yaml.safe_load(io.open(f, encoding='utf8'))
        changed = False
        by_id = {s['id']: s for s in d['screens']}
        for sid, ops in screens.items():
            s = by_id.get(sid)
            if not s:
                print('  %s not found in %s' % (sid, f))
                continue
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
                print('  %-9s %-38s + %s' % (sid, s['name'][:38],
                                             ', '.join(n['operationId'] for n in new)))
        if changed and apply:
            io.open(f, 'w', encoding='utf8').write(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
            print('  -> %s' % f)
    print('\n%d reference(s) added' % added)
    if not apply:
        print('\n  nothing written — pass --apply')


if __name__ == '__main__':
    main()
