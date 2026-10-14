"""C-UNTYPED-BODY: name each bare 2xx body. Existing schemas where the action returns its item; small new response
schemas otherwise (persistence none)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc
root = Path(sys.argv[1])
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
by, names = g.schemas()
TARGET = {('broadcastToGuests', '202'): 'GuestBroadcastAccepted', ('cancelMerchandiseReservation', '200'): 'MerchandiseReservation',
          ('collectMerchandiseReservation', '200'): 'MerchandiseReservation', ('disposeShopAndDrop', '200'): 'ShopAndDrop',
          ('exportPartnerInvoice', '200'): 'PartnerInvoiceExport', ('getVenueMapLive', '200'): 'VenueMapLiveState',
          ('replayEvents', '202'): 'WebhookReplayJob', ('skipRolloutCell', '200'): 'RolloutCell'}
NEW = {
    'GuestBroadcastAccepted': [
        "type: object",
        "x-ticvai-persistence: none — response only; the dispatch rows are marketing.message_dispatch",
        "description: '**The broadcast was accepted for sending** (`broadcastToGuests`). Sending runs on; the count is the guests with a live entitlement at the venue when it was accepted.'",
        "required: [broadcastId, kind, acceptedAt, recipientCount]",
        "properties:",
        "  broadcastId: { type: string, format: uuid }",
        "  kind: { type: string, enum: [evacuation, weather, rideClosure, lostChild, operational, allClear] }",
        "  acceptedAt: { type: string, format: date-time }",
        "  recipientCount: { type: integer, minimum: 0 }",
    ],
    'PartnerInvoiceExport': [
        "type: object",
        "x-ticvai-persistence: none — response only; built from the partner's ledger postings for the period",
        "description: '**One partner invoice for one period, in the requested ERP format** (`exportPartnerInvoice`). Idempotent on the period: a second export of the same period returns the same `invoiceNumber` with `isRepeat` true.'",
        "required: [partnerId, periodFrom, periodTo, format, invoiceNumber, fileName, contentType, content, generatedAt, isRepeat]",
        "properties:",
        "  partnerId: { type: string, format: uuid }",
        "  periodFrom: { type: string, format: date }",
        "  periodTo: { type: string, format: date }",
        "  format: { type: string, enum: [sapIdoc, csv, json, ubl] }",
        "  invoiceNumber: { type: string }",
        "  fileName: { type: string }",
        "  contentType: { type: string, description: 'The media type of `content`, e.g. application/xml for sapIdoc and ubl.' }",
        "  content: { type: string, description: 'The export document; base64 when the format is binary.' }",
        "  generatedAt: { type: string, format: date-time }",
        "  isRepeat: { type: boolean, description: 'True when this period was exported before and the same invoice is returned.' }",
    ],
    'VenueMapLiveState': [
        "type: object",
        "x-ticvai-persistence: none — response only; live state over the published map, assembled at read time",
        "description: '**The live operational state on the published map** (`getVenueMapLive`): one entry per point that has a live figure. Changes every few seconds, so it is read apart from the map itself (`getVenueMap`).'",
        "required: [mapId, asOf, points]",
        "properties:",
        "  mapId: { type: string, format: uuid }",
        "  asOf: { type: string, format: date-time }",
        "  points:",
        "    type: array",
        "    items:",
        "      type: object",
        "      required: [pointId]",
        "      properties:",
        "        pointId: { type: string, format: uuid }",
        "        isOpen: { type: boolean, nullable: true }",
        "        waitMinutes: { type: integer, minimum: 0, nullable: true }",
        "        queueLength: { type: integer, minimum: 0, nullable: true }",
        "        occupancyPercent: { type: number, minimum: 0, nullable: true }",
    ],
    'WebhookReplayJob': [
        "type: object",
        "x-ticvai-persistence: none — response only; the replayed deliveries are written as webhook deliveries marked as replays",
        "description: '**A queued replay** (`replayEvents`): the window and event types it re-delivers. Each delivery it makes is marked as a replay in its payload.'",
        "required: [replayId, subscriptionId, from, queuedAt]",
        "properties:",
        "  replayId: { type: string, format: uuid }",
        "  subscriptionId: { type: string, format: uuid }",
        "  from: { type: string, format: date-time }",
        "  to: { type: string, format: date-time, nullable: true }",
        "  eventTypes: { type: array, items: { $ref: '#/components/schemas/WebhookEventType' } }",
        "  queuedAt: { type: string, format: date-time }",
    ],
}
for n in NEW:
    assert n not in names, n
done = set()
for (oid, code), sname in TARGET.items():
    f = ops[oid]
    if sname not in NEW:
        assert (f['contract'], sname) in by, (oid, sname)
    D = Doc(root / f['file'])
    i = D.response(oid, code)
    end = D.block_end(i)
    hit = [j for j in range(i, end) if D.text(D.lines[j]).strip() == 'type: object']
    assert len(hit) == 1, (oid, hit)
    j = hit[0]
    assert D.text(D.lines[j + 1]).strip() == 'additionalProperties: true', oid
    ind = D.indent(j)
    D.delete(j, j + 2)
    D.insert(j, [' ' * ind + f"$ref: '#/components/schemas/{sname}'"])
    if sname in NEW and sname not in done:
        comp = next(k for k, l in enumerate(D.lines) if D.text(l) == 'components:')
        sch = D.child(comp, 'schemas')
        at = D.end_trim(D.block_end(sch))
        ci = D.child_indent(sch)
        D.insert(at, [' ' * ci + sname + ':'] + [' ' * (ci + 2) + l for l in NEW[sname]])
        done.add(sname)
    D.save()
print('ok', len(TARGET))
