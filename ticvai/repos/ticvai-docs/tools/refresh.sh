#!/usr/bin/env bash
# Regenerate every derived artefact, in dependency order.
#
# Run this after any change to contracts, screens, flows, states or events. Everything below is
# derived; nothing in it should ever be edited by hand. The order matters — the domain closure
# reads the lineage, and the status reads the closure.
set -euo pipefail

# **34 of the 88 tools print a character Windows cp1252 cannot encode.** `audit-workbooks` dies on
# the `→` in its own heading; the checkers survive only because an em dash happens to exist in
# cp1252. Setting this once here beats patching 34 files, and beats each tool needing an
# environment variable it cannot set for itself.
export PYTHONIOENCODING=utf-8

# **`python3` on Windows may be the Microsoft Store stub, which prints an error and exits 0.**
# `set -e` cannot catch a success, so every call below would quietly do nothing and the run would
# report PASS having written nothing. Resolve a real interpreter once and fail loudly if there is
# none — the 40 call sites below keep saying `python3` and none of them need to know.
_PY=""
for _c in python3 python py; do
  if command -v "$_c" >/dev/null 2>&1 && "$_c" -c 'import sys; sys.exit(0)' >/dev/null 2>&1; then
    _PY="$(command -v "$_c")"; break
  fi
done
if [ -z "$_PY" ]; then
  echo "no working Python found — 'python3' here is the Microsoft Store stub, which exits 0" >&2
  exit 1
fi
python3() { "$_PY" "$@"; }
echo "python: $_PY ($("$_PY" -V 2>&1))"

cd "$(dirname "$0")/.."

# **First, because twenty-plus tools read the lineage as authoritative.** An operation added to a
# contract was invisible to `check-package`, `check-screens`, `derive-relationships`, the workbooks
# and the viewer until somebody remembered to run this by hand -- and `check-package` failed the
# package for the gap, correctly, with nothing in the pipeline able to close it. On 10 September it
# was holding nine: seven `relinquish*` operations renamed at some point from `release*`, and the
# two step-up operations added the same day.
#
# **Additive only.** The entries that came with the original dump carry judgements a derivation
# cannot reproduce -- an audience narrowed by hand, a service assignment that is a deployment
# decision rather than a contract fact -- so an entry that exists is left exactly as it is. Verified
# on the run that added those nine: 0 removed, 0 existing entries changed. `--audit` still reports
# the 1,445 entries that differ, and reads only; the rebuild it argues for is a separate job that
# somebody has to decide on rather than have happen to them.
python3 tools/derive-lineage.py --apply
python3 tools/derive-schema.py
python3 tools/derive-relationships.py
python3 tools/derive-ddl.py --apply
python3 tools/derive-burst-scope.py --apply
python3 tools/derive-sizing.py --apply
python3 tools/derive-table-notes.py --apply
python3 tools/derive-schema-roots.py
python3 tools/derive-frontend.py
python3 tools/derive-board-panel-map.py
python3 tools/derive-diagrams.py
python3 tools/build-schema-workbook.py
python3 tools/build-services-workbook.py 2>/dev/null || true
# **The screens are authored before anything reads them.** Everything below this comment writes
# into screens/P*.yaml, and everything after it — the boards, the id register, the screen index,
# the mirrors — is built from what these leave behind. Running them later would publish an index
# of the previous run's screens, which is the mistake the mirrors block at the bottom records.
#
# All six are idempotent and say "nothing to do" on a second run. They are ordered by what they
# depend on: machines and names first, then the graph, then the labels on it.
# **Only tools that fill blanks belong here. Tools that assert content do not.**
# Each of the three below skips an edge that already has a transition, so a trigger somebody
# wrote by hand survives a rebuild. They recompute from a source of truth — the flows, the
# entry points, what a destination declares it needs — and add nothing where an answer exists.
#
# Three others were removed on 9 September: `apply-p04-machines`, `apply-naming-and-navsets` and
# `wire-pack-boards`. They assert their own content and overwrite a block that differs, which was
# right for applying a decision once and wrong for a command people run to rebuild. A probe field
# added by hand inside `machine` was silently reverted by the next run, which is how this was
# found. **They are one-off corrections, already applied; run them deliberately, not on a
# rebuild.** Their effects live in screens/P*.yaml and are preserved by the generators' carry
# rules, so nothing here needs to re-assert them.
python3 tools/derive-transitions-from-flows.py --apply --adopt   # 94 flows -> triggers, +107 edges
python3 tools/label-launcher-edges.py --apply            # home screens are launchers
python3 tools/derive-carries-from-entrystate.py --apply  # carries, from what the destination needs
# **A screen that calls `getEntitlement(entitlementId)` and declares no `entitlementId`
# cannot know which ticket it is showing.** This fills that blank from the operation's own
# path, and it earns its place here because it happened twice on 10 September alone —
# once for five new P04 screens and once for thirteen when guest web and mobile were
# brought to parity. It runs before derive-carries, which reads what it writes.
python3 tools/derive-entrystate-params.py --apply
# **135 screens gained components the first time this was run, on 10 September.** It had
# been sitting in tools/ unrun, which is why check-bindings reports 634 components carrying
# `Structure from the wireframe board. Components not yet enumerated.` — the enumeration
# was available and nothing ran it. Same lesson as index-boards: a derive tool outside this
# script is a number nobody is keeping true.
python3 tools/derive-components.py --apply

# **Before the boards are drawn, so every screen knows where it was drawn.** Five P04 screens
# added by hand from the client-approved POS prototype carried no `wireframe` block at all, and a
# screen with no anchor is a card nothing can link to. The anchor is the platform's own
# `wireframeBoard` plus the id, so there is nothing here to decide -- and it never overwrites an
# anchor that exists, which is what keeps the client-pack links intact.
python3 tools/derive-board-anchors.py --apply

python3 tools/derive-wireframes.py
# **`board-index.json` was stale for a week and nothing said so.** It is derived from the
# board files, it was never in this script, and on 10 September it still named 170 boards of
# which 141 were no longer on disk. A number that is expensive to derive gets derived
# carelessly — which is the reason the tool exists, and the reason it belongs here.
python3 tools/index-boards.py
# The Claude Design work list, and what each shipped app demands of a signed-in user.
# Both are derived from the screens and both go stale the moment a screen changes.
python3 tools/derive-design-manifest.py
python3 tools/derive-app-roles.py
# **Retired 10 September.** `derive-pack-boards.py` drew every pack screen a second time on
# its own `WS##` board — 728 screens rendered twice, and a reviewer looking at two drawings
# of one screen cannot tell it is one screen. The workshop grouping is now a badge and a
# filter on the platform board, from the `source.pack`/`source.board` the screens already
# carry. The tool still runs by hand if the client ever wants the separate files back.
# **The id register has to be current before check-screens runs**, because that check now
# fails on a screen issued above the recorded high-water mark - which is the whole point of
# it, and also means a stale register fails the package for a screen that is perfectly fine.
python3 tools/derive-id-register.py --apply
python3 tools/link-screens-contracts.py

python3 - <<'PY'
import yaml, glob, json
# **Every open in this block names its encoding.** Windows defaults to cp1252, and the moment a
# note in the lineage carried a curly quote the whole refresh died here — after the screens had
# been rewritten and before anything downstream ran, which is the worst place to stop.
lin = json.load(open('handoff/api-data-lineage.json', encoding='utf-8'))
idx = {}
for f in sorted(glob.glob('screens/P*.yaml')):
    d = yaml.safe_load(open(f, encoding='utf-8')); p = d['platform']
    for s in d['screens']:
        ops = [a.get('operationId') for a in (s.get('apis') or []) if a.get('operationId')]
        reads, writes, svcs, stores = set(), set(), set(), set()
        for o in ops:
            v = lin.get(o)
            if not v: continue
            reads |= set(v['reads']); writes |= set(v['writes'])
            if v.get('service'): svcs.add(v['service'])
            stores |= set(v.get('stores') or [])
        nav = s.get('navigation') or {}
        # **A destination id is not a transition.** Until 9 September this index carried `exits`
        # and nothing else about behaviour, so whoever built from it got a list of screen ids and
        # had to invent every trigger, every carried value and every drawer for themselves. The
        # fields below are the ones a builder cannot guess: how the move is made, what state
        # travels with it, what the screen holds mid-process, and what closing an overlay does.
        idx[s['id']] = dict(name=s['name'], platform=p['code'], platformName=p['shortName'],
            operator=p.get('operator'), app=p['app'], route=s['implementation']['route'],
            operations=ops, services=sorted(svcs),
            stores=sorted(stores), reads=sorted(reads), writes=sorted(writes), storedProcedures=[],
            wave=s['wave'], offline=bool((s.get('states') or {}).get('offline')), specified=True,
            exits=nav.get('exitTo') or [],
            pattern=s.get('pattern'), entryFrom=nav.get('entryFrom') or [],
            transitions=nav.get('transitions') or [],
            machine=s.get('machine') or None,
            states=s.get('states') or {},
            overlays=s.get('overlays') or [])
json.dump(idx, open('handoff/screen-index.json', 'w', encoding='utf-8'), indent=1)
print(f"screen-index: {len(idx)}")
PY

for d in ai; do
  python3 tools/derive-domain.py "$d" --quiet
  python3 tools/build-status.py --domain "$d" >/dev/null
  python3 tools/render-domain.py "$d"
done

python3 tools/build-backlog-index.py
python3 tools/build-cluster-index.py
python3 tools/sync-project-bible.py
python3 tools/derive-platform.py
python3 tools/derive-platform-deployment.py
python3 tools/build-audience.py
python3 tools/build-status.py

# **Mirrors last.** They copy handoff/, and build-status writes handoff/ — running the copy at the
# top of this script mirrored the previous run's numbers and then failed its own drift check.
#
# **Last means last, and it was not.** `build-status --domain ai` writes `handoff/status-ai.json`
# and `sync-counts` rewrites README, COVERAGE, OVERVIEW and MANIFEST — both of them *after* the
# copy. So every run finished with the mirrors one file behind and `check-package` reported six
# out-of-sync mirrors, once per repo, on a package that was otherwise clean. The comment was
# right and the order underneath it was not.
python3 tools/derive-overview.py
python3 tools/build-status.py --domain ai
python3 tools/sync-counts.py
python3 tools/derive-mirrors.py

echo
# **Four checkers existed and this script never ran them.** `audit-workbooks` had in fact
# never completed on Windows at all — it died on the `→` in its own first heading. A check
# nobody runs is a check nobody has, so every checking tool in tools/ is now in this list.
# One-shot repairs stay out: they assert content rather than report on it.
for t in check-screens check-frontend check-flows check-board-flows check-session-entry check-step-up check-states check-config-scope check-wireframes check-backlog check-traceability check-package check-screen-redundancy check-bindings check-migrations audit-links audit-workbooks audit-pack-citations; do
  # **A report that stops at the first failure is not a report.** `set -e` plus `pipefail` meant
  # one checker returning non-zero killed the whole run: for most of 9 September this script died
  # at check-flows and nobody saw the eight checks below it, including the ones that were passing.
  printf "  %-22s" "$t"; python3 "tools/$t.py" 2>&1 | tail -1 || true
done

# **Coverage is a number that can quietly go down.** A regeneration that dropped transitions would
# still pass every check above — nothing fails for an edge nobody labelled — so it is printed here
# next to the checks rather than left to be noticed later.
printf "  %-22s" "transition coverage"; python3 tools/audit-transitions.py 2>&1 | grep '^ALL'
