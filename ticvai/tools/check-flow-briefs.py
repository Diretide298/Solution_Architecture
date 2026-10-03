#!/usr/bin/env python3
"""Validate the Block A flow design briefs (handoff/flow-briefs/*.yaml).

Shape: audit/ticvai/apply/FLOW-BRIEF-BRIEF.md (3 October 2026). Each file has `process` and
`flows:` keyed by flow id; each flow carries title, process, trigger, actors, inputs, processing,
outputs, steps, motion, decisions, sources and open.

Checks, per flow:
  - every required key is present (and non-empty where it must be);
  - the key is a flow id in flows/F*.yaml, or `proposed: true` with a NEW- key (a journey the
    package has no flow for yet: reported as a warning, not an error);
  - inputs: each has name, formats, limits, validation (non-empty) and source;
  - outputs: each has name, states and failure_branches;
  - steps: non-empty, each with a screen id that exists in screens/P*.yaml;
  - every `contract#operationId` written anywhere in the flow exists in contracts/;
  - every `screen` / `screens` value and every `flow` / `related_flows` value exists;
  - motion is present: a non-empty list, or the string `none`.

References (`see: <process>#<flow>`), so a flow or a screen's detail is written once:
  - a flow whose whole body is `see: <process>#<flow>` (plus an optional `note`) is a copy kept in another
    process (the owner, the process of the trigger screen); the target brief must exist, hold that flow
    with a full body, and the flow id must match;
  - an input or output `{screen: <id>, see: <process>#<flow>}` points at the flow that details that
    screen's inputs or outputs; the target must exist with a full body;
  - a flow written out in full in two briefs is an error: keep one, point at it from the other.

Usage (from the ticvai folder):
  python tools/check-flow-briefs.py                 # every handoff/flow-briefs/*.yaml
  python tools/check-flow-briefs.py handoff/flow-briefs/ai.yaml ...
Exit 1 on any error; warnings do not fail.
"""
import glob
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = ['title', 'process', 'trigger', 'actors', 'inputs', 'processing', 'outputs', 'steps',
            'motion', 'decisions', 'sources', 'open']
NON_EMPTY = ['title', 'process', 'trigger', 'actors', 'outputs', 'steps', 'motion', 'decisions', 'sources']
INPUT_KEYS = ['name', 'formats', 'limits', 'validation', 'source']
OUTPUT_KEYS = ['name', 'states', 'failure_branches']
SCREEN_RE = re.compile(r'^([A-Z]{2,5}-\d{2,4})\b')
SEE_RE = re.compile(r'^([a-z][a-z0-9-]*)#([A-Z]+[-A-Z0-9]*)$')
BRIEFS = {}  # process -> flows mapping, for resolving `see:` references
OP_RE = re.compile(r'\b([a-z][a-z0-9-]*)#([a-z][A-Za-z0-9]*)\b')


def load_yaml(path):
    with open(path, encoding='utf-8') as fh:
        return yaml.safe_load(fh)


def package():
    screens = set()
    for f in glob.glob(os.path.join(ROOT, 'screens', 'P*.yaml')):
        for s in (load_yaml(f) or {}).get('screens') or []:
            if isinstance(s, dict) and s.get('id'):
                screens.add(s['id'])
    ops = {}
    for f in glob.glob(os.path.join(ROOT, 'contracts', '*', '*.yaml')):
        name = os.path.splitext(os.path.basename(f))[0]
        found = ops.setdefault(name, set())
        for item in ((load_yaml(f) or {}).get('paths') or {}).values():
            for op in (item or {}).values():
                if isinstance(op, dict) and op.get('operationId'):
                    found.add(op['operationId'])
    flows = set()
    for f in glob.glob(os.path.join(ROOT, 'flows', 'F*.yaml')):
        y = load_yaml(f) or {}
        if y.get('id'):
            flows.add(str(y['id']))
    return screens, ops, flows


def empty(v):
    return v is None or (isinstance(v, (str, list, dict)) and len(v) == 0)


def walk(node, path=''):
    """Yield (path, key, value) for every mapping entry, and (path, None, str) for every string."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield path, k, v
            yield from walk(v, f'{path}.{k}')
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, f'{path}[{i}]')
    elif isinstance(node, str):
        yield path, None, node


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def resolve_see(ref):
    """Return None when `ref` names a flow with a full body in some brief, else the reason it does not."""
    m = SEE_RE.match(str(ref or '').strip())
    if not m:
        return f'`see: {ref}` is not <process>#<flow>'
    proc, fid = m.groups()
    if proc not in BRIEFS:
        return f'`see: {ref}`: no brief handoff/flow-briefs/{proc}.yaml'
    tgt = BRIEFS[proc].get(fid)
    if not isinstance(tgt, dict):
        return f'`see: {ref}`: {proc} has no flow {fid}'
    if 'see' in tgt:
        return f'`see: {ref}` points at another reference; point at the full copy'
    return None


def is_pointer(x):
    return isinstance(x, dict) and 'see' in x and empty(x.get('name')) and empty(x.get('output'))


def check_flow(fid, fl, screens, ops, flows, err, warn):
    if not isinstance(fl, dict):
        err(f'{fid}: not a mapping')
        return {}
    if 'see' in fl:  # a copy kept in the owning process
        extra = set(fl) - {'see', 'note'}
        if extra:
            err(f'{fid}: a `see:` flow carries only `see` and `note` (found {", ".join(sorted(extra))})')
        why = resolve_see(fl['see'])
        if why:
            err(f'{fid}: {why}')
        elif SEE_RE.match(str(fl['see']).strip()).group(2) != fid:
            err(f'{fid}: `see: {fl["see"]}` names a different flow')
        if fid not in flows:
            err(f'{fid}: no such flow id in flows/')
        return {'see': 1}
    if fid not in flows:
        if fl.get('proposed') is True and str(fid).startswith('NEW-'):
            warn(f'{fid}: proposed journey, no flow in flows/ yet')
        else:
            err(f'{fid}: no such flow id in flows/ (mark a new journey `proposed: true` with a NEW- key)')
    for k in REQUIRED:
        if k not in fl:
            err(f'{fid}: missing `{k}`')
        elif k in NON_EMPTY and empty(fl[k]):
            err(f'{fid}: `{k}` is empty')
    for i, inp in enumerate(as_list(fl.get('inputs'))):
        if not isinstance(inp, dict):
            err(f'{fid}: inputs[{i}] is not a mapping')
            continue
        if is_pointer(inp):
            why = resolve_see(inp['see'])
            if why:
                err(f'{fid}: inputs[{i}]: {why}')
            continue
        for k in INPUT_KEYS:
            if empty(inp.get(k)):
                err(f'{fid}: inputs[{i}] ({inp.get("name", "?")}) has no `{k}`')
    for i, out in enumerate(as_list(fl.get('outputs'))):
        if not isinstance(out, dict):
            err(f'{fid}: outputs[{i}] is not a mapping')
            continue
        if is_pointer(out):
            why = resolve_see(out['see'])
            if why:
                err(f'{fid}: outputs[{i}]: {why}')
            continue
        if empty(out.get('name')) and not empty(out.get('output')):
            out = dict(out, name=out['output'])  # `output:` is accepted for the name
        for k in OUTPUT_KEYS:
            if k not in out or (k != 'failure_branches' and empty(out[k])):
                err(f'{fid}: outputs[{i}] ({out.get("name", "?")}) has no `{k}`')
    steps = as_list(fl.get('steps'))
    for i, st in enumerate(steps):
        if not isinstance(st, dict) or empty(st.get('screen')):
            err(f'{fid}: steps[{i}] has no screen')
        elif len(st) < 3:
            err(f'{fid}: steps[{i}] says too little (screen plus what is seen, done and the result)')
    motion = fl.get('motion')
    if isinstance(motion, str) and motion.strip().lower() != 'none':
        err(f'{fid}: motion is a string other than `none`; give a list')
    # references anywhere in the flow
    nops = 0
    for path, key, val in walk(fl):
        if key in ('screen', 'screens'):
            for s in as_list(val):
                if isinstance(s, str):
                    m = SCREEN_RE.match(s)  # "BO-058 Reporting Home" reads as BO-058
                    s = m.group(1) if m else s
                if isinstance(s, str) and s not in screens:
                    err(f'{fid}{path}: screen {s} does not exist')
        if key in ('flow', 'related_flows'):
            for f in as_list(val):
                if isinstance(f, str) and f not in flows:
                    err(f'{fid}{path}: flow {f} does not exist')
        if key is None:
            for c, o in OP_RE.findall(val):
                if c not in ops:
                    continue  # not a contract reference (e.g. a URL fragment)
                nops += 1
                if o not in ops[c]:
                    err(f'{fid}{path}: operation {c}#{o} does not exist')
    return {'inputs': len([x for x in as_list(fl.get('inputs')) if not is_pointer(x)]), 'steps': len(steps),
            'motions': 0 if isinstance(motion, str) else len(as_list(motion)), 'ops': nops,
            'open': len(as_list(fl.get('open')))}


def main(argv):
    files = argv or sorted(glob.glob(os.path.join(ROOT, 'handoff', 'flow-briefs', '*.yaml')))
    if not files:
        print('no flow briefs found')
        return 1
    screens, ops, flows = package()
    for bf in glob.glob(os.path.join(ROOT, 'handoff', 'flow-briefs', '*.yaml')):
        try:
            BRIEFS[os.path.splitext(os.path.basename(bf))[0]] = (load_yaml(bf) or {}).get('flows') or {}
        except yaml.YAMLError:
            pass
    total = 0
    for f in files:
        errors, warnings = [], []
        try:
            doc = load_yaml(f) or {}
        except yaml.YAMLError as e:
            print(f'{f}: YAML error: {e}')
            total += 1
            continue
        if empty(doc.get('process')):
            errors.append('missing top-level `process`')
        fls = doc.get('flows')
        if not isinstance(fls, dict) or not fls:
            errors.append('missing `flows:` mapping keyed by flow id')
            fls = {}
        proc = os.path.splitext(os.path.basename(f))[0]
        for fid, fl in fls.items():
            twins = [p for p, other in BRIEFS.items() if p != proc and isinstance(other.get(fid), dict)
                     and 'see' not in other[fid]]
            if isinstance(fl, dict) and 'see' not in fl and twins:
                errors.append(f'{fid}: also written out in full in {", ".join(sorted(twins))}; keep one copy (the '
                              f'process of the trigger screen) and write `see: <process>#{fid}` in the other')
        sums = {'inputs': 0, 'steps': 0, 'motions': 0, 'ops': 0, 'open': 0, 'see': 0}
        for fid, fl in fls.items():
            c = check_flow(str(fid), fl, screens, ops, flows, errors.append, warnings.append)
            for k in sums:
                sums[k] += c.get(k, 0)
        try:
            shown = os.path.relpath(f, ROOT)
        except ValueError:  # another drive on Windows
            shown = f
        print(f'{shown}: {len(fls)} flows, {sums["inputs"]} inputs, {sums["steps"]} steps, '
              f'{sums["motions"]} motions, {sums["ops"]} operation refs, {sums["open"]} open, '
              f'{sums["see"]} kept in another process; '
              f'{len(errors)} errors, {len(warnings)} warnings')
        for w in warnings:
            print(f'  warning: {w}')
        for e in errors:
            print(f'  ERROR: {e}')
        total += len(errors)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
