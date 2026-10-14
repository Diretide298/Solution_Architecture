import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc
D = Doc(Path(sys.argv[1]) / 'contracts/satellite/fnb.yaml')
si = D.find_schema('UpdateTableReservationRequest')
pi = D.child(D.child(si, 'properties'), 'groupId')
e = D.block_end(pi)
print(''.join(D.lines[pi:e]))
D.delete(pi, e)
D.save()
