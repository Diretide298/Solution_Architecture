import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc, sq
root = Path(sys.argv[1])
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
DESC = {
    ('listReports', 'search'): 'Matched case-insensitively as a substring of the report definition\'s `name` or `description`; no wildcards.',
    ('listWaiverTemplateMaster', 'q'): 'Matched case-insensitively as a substring of `waiverName`, `internalDescription` or `customTypeLabel`; no wildcards.',
    ('searchCatalogue', 'q'): 'Keywords matched case-insensitively against the product\'s `name` and `summary`, in the requested language and in English; every word must match.',
}
for (oid, pname), d in DESC.items():
    D = Doc(root / ops[oid]['file'])
    m, end = D.find_op(oid)
    hits = [j for j in range(m, end) if re.match(r'^\s*- name: %s\s*$' % pname, D.text(D.lines[j]))]
    assert len(hits) == 1, (oid, hits)
    j = hits[0]
    ind = D.indent(j) + 2
    D.insert(j + 1, [' ' * ind + 'description: ' + sq(d)])
    D.save()
print('ok')
