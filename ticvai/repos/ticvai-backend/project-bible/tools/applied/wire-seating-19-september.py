#!/usr/bin/env python3
"""Wire the 21 idle `seating` authoring operations to the seat boards that need them.

`seating.yaml` declares 35 operations. Its 14 runtime operations — holds, availability,
blocks, recommend — are all called. **Not one of its 21 authoring operations is**, while
119 of the 128 seat board screens carry no operation at all.

The contract audit read that as drift. It is the opposite: the two halves are the same
thing and were never joined, because the seat boards were parsed on 18 September and the
title matcher could not reach these names. Every one of the 21 is backed by the 21 August
MoM — *"full and partial (section-level) copy-paste… a layout version-comparison view"*,
*"AI-assisted import (PDF/image + Excel/CSV)"*, *"best-seat ranking… configurable per seat
map/event"*.

**Nothing is authored here.** This writes references to operations that already exist,
which is why it can be an `applied/` one-off rather than contract work. It also removes
the seat entries from `workshop-contract-gap.md`, which proposed authoring `listSeatMap`
and `setSeatMapTemplate` — title-derived duplicates of `getSeatMap` and
`createSeatMapTemplate`.

**On the seven section-type screens.** `BO-955` to `BO-961` all bind `setMapZones`, whose
own summary is *"Standing areas, suites, stages and obstructions"* — one operation for all
of them, which is the shape the 21 August decision asks for: *"section type will be a
configurable attribute set at the section level within a single seat map builder screen."*
Whether those seven collapse into one screen is a separate decision; binding them to one
operation is correct either way and loses nothing if they do.

Idempotent — a screen that already declares an operation is left alone.
Run with no arguments to preview; `--apply` to write.
"""
import io
import sys

import yaml

F = 'screens/P08-venue-back-office.yaml'

# screen -> [(operationId, purpose, trigger)]
WIRING = {
    'BO-954': [('getSeatMap', 'The map being drawn', 'onLoad'),
               ('createSeatMap', 'Start a new map', 'onAction'),
               ('updateSeatMap', 'Save the canvas', 'onAction')],
    'BO-955': [('getSeatMap', 'The map being sectioned', 'onLoad'),
               ('setMapZones', 'Section type, set at the section level', 'onAction')],
    'BO-956': [('listSeats', 'The rows and seats as drawn', 'onLoad'),
               ('updateSeats', 'Renumber, move or relabel', 'onAction')],
    'BO-957': [('setMapZones', 'Standing areas', 'onAction')],
    'BO-958': [('setMapZones', 'Suites and boxes', 'onAction')],
    'BO-959': [('setMapZones', 'Stage and focal point', 'onAction')],
    'BO-960': [('setMapZones', 'Entrances, exits and aisles', 'onAction')],
    'BO-961': [('setMapZones', 'Amenities and obstructions', 'onAction')],
    'BO-962': [('listSeatMapTemplates', 'Templates to start from', 'onLoad'),
               ('createSeatMapTemplate', 'Save this map as a template', 'onAction'),
               ('validateSeatMap', 'Check before publishing', 'onAction'),
               ('publishSeatMap', 'Publish', 'onAction')],
    'BO-963': [('getSeatMapImport', 'How the import went', 'onLoad'),
               ('getImportJob', 'Progress of a running import', 'onLoad')],
    'BO-964': [('importSeatMap', 'Import from a plan or image', 'onAction'),
               ('getImportJob', 'Watch it run', 'onLoad')],
    'BO-965': [('importSeatGeometry', 'Import vector geometry', 'onAction'),
               ('getImportJob', 'Watch it run', 'onLoad')],
    'BO-966': [('importSeatManifest', 'Row and seat naming from a manifest', 'onAction'),
               ('getImportJob', 'Watch it run', 'onLoad')],
    'BO-971': [('validateSeatMap', 'Validate the draft', 'onAction'),
               ('getSeatMapImport', 'What the import produced', 'onLoad')],
    'BO-972': [('commitImportJob', 'Accept the draft', 'onAction'),
               ('publishSeatMap', 'Publish', 'onAction')],
    'BO-974': [('listSeatMapTemplates', 'The library', 'onLoad'),
               ('createSeatMapTemplate', 'Add to the library', 'onAction')],
    'BO-976': [('cloneSeatMap', 'Copy a whole map', 'onAction'),
               ('copySeatMapSection', 'Copy one section into another map', 'onAction')],
    'BO-977': [('diffSeatMapVersions', 'Compare two versions of a layout', 'onLoad')],
    'BO-982': [('validateSeatMap', 'Check before publishing', 'onAction'),
               ('publishSeatMap', 'Publish or roll back', 'onAction')],
    'BO-985': [('listSeatCategories', 'The status and category model', 'onLoad'),
               ('createSeatCategory', 'Add a category', 'onAction')],
    'BO-993': [('getSeatingRules', 'Rules in force', 'onLoad'),
               ('setSeatingRules', 'Best-seat ranking, per map', 'onAction')],
    'BO-995': [('assignSeats', 'Pick and hold the best available seats', 'onAction')],
}

INVALIDATES = {
    'createSeatMap': ['listSeatMaps'], 'updateSeatMap': ['getSeatMap', 'listSeatMaps'],
    'publishSeatMap': ['listSeatMaps', 'getSeatMap'], 'updateSeats': ['listSeats'],
    'setMapZones': ['getSeatMap'], 'createSeatCategory': ['listSeatCategories'],
    'createSeatMapTemplate': ['listSeatMapTemplates'], 'cloneSeatMap': ['listSeatMaps'],
    'copySeatMapSection': ['getSeatMap'], 'commitImportJob': ['listSeatMaps'],
    'setSeatingRules': ['getSeatingRules'], 'importSeatMap': ['getImportJob'],
    'importSeatManifest': ['getImportJob'], 'importSeatGeometry': ['getImportJob'],
}


def main():
    apply = '--apply' in sys.argv
    d = yaml.safe_load(io.open(F, encoding='utf8'))
    by_id = {s['id']: s for s in d['screens']}

    added = 0
    touched = []
    for sid, ops in sorted(WIRING.items()):
        s = by_id.get(sid)
        if not s:
            print('  %s not found' % sid)
            continue
        have = {a.get('operationId') for a in (s.get('apis') or [])}
        new = []
        for oid, purpose, trigger in ops:
            if oid in have:
                continue
            entry = {'operationId': oid, 'contract': 'seating',
                     'purpose': purpose, 'trigger': trigger}
            if INVALIDATES.get(oid):
                entry['invalidates'] = INVALIDATES[oid]
            new.append(entry)
        if new:
            s.setdefault('apis', []).extend(new)
            added += len(new)
            touched.append((sid, s['name'], [n['operationId'] for n in new]))

    for sid, name, ops in touched:
        print('  %-9s %-44s %s' % (sid, name[:44], ', '.join(ops)))
    print('\n%d reference(s) across %d screen(s)' % (added, len(touched)))

    wired = set()
    for s in d['screens']:
        for a in (s.get('apis') or []):
            if a.get('contract') == 'seating':
                wired.add(a['operationId'])
    print('seating operations now reached: %d' % len(wired))

    if not apply:
        print('\n  nothing written — pass --apply')
        return
    io.open(F, 'w', encoding='utf8').write(
        yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
    print('  -> %s' % F)


if __name__ == '__main__':
    main()
