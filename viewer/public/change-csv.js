/**
 * The change request CSV, as one column list that both ends agree on.
 *
 * There are two ways to get this file — the button on the changes page, which
 * writes exactly the rows on screen, and Download a date range on the admin
 * page, which asks the service for a range nobody has looked at — and **either
 * one can be filled in and uploaded back**. That only works while the two files
 * are the same file: the same columns, in the same order, with the same
 * headings, so a reader who fills in "our decision" is filling in the column
 * the importer reads whichever button produced the sheet.
 *
 * The verdict export has the same pair and keeps them in step by hand, with a
 * comment on each side saying so. This one does not, because the change request
 * file has twenty-three columns rather than seventeen and three of them are
 * written back — a pair of hand-kept lists that long is a pair that drifts, and
 * the drift shows up as a column shifted by one halfway down somebody's
 * spreadsheet.
 *
 * So the list lives here, on its own, importable by a page and by a check. The
 * service holds its own copy in `_export_changes`, because it is another
 * language and cannot import this one — and `changes-import-check.mjs` asserts
 * the two are identical, which is the part that actually keeps them honest.
 *
 * Nothing in here touches the DOM or the network, so it can be imported by a
 * check running in node.
 */

/**
 * The columns, in order.
 *
 * `id` is the store's own id and is what the importer matches on. `ref` is
 * CR-007, which is what people say out loud — and it is **counted per project**,
 * so two projects both have a CR-007 and it cannot identify a row. It is
 * carried for reading and never read back.
 *
 * The three editable columns sit in the middle, ahead of `problem`. That is the
 * one layout decision here: a problem statement runs to eight thousand
 * characters, and a reader who has to scroll past it to reach the cell they
 * came to fill in is a reader who fills in the wrong row.
 */
export const CHANGE_CSV_HEADER = [
  'id', 'ref', 'raised', 'date', 'project', 'status', 'blocking',
  'side', 'platform',
  'kind', 'artefact', 'title', 'raised by', 'email', 'via', 'ticket',
  'picked by', 'picked on',
  'our decision', 'because', 'reference', 'settled on', 'settled by',
  'problem', 'evidence', 'options', 'recommendation',
];

/** Which side of the house a request is in the queue of. The same two words
 *  the service writes, and the same two `verdict.tag` has always carried. */
export const CHANGE_SIDE_LABEL = { frontend: 'Frontend', backend: 'Backend' };

/** Where a change request stands, as the file spells it. The same four words
 *  the service writes and reads, and the importer takes either spelling. */
export const CHANGE_STATUS_LABEL = {
  open: 'Open', accepted: 'Accepted', rejected: 'Rejected', done: 'Done',
};

/** What each target kind is called in the file, and on the changes page.
 *
 *  The thirteen a change request may be about — the service's CHANGE_KINDS —
 *  and **not the seven a verdict may be about**, which is a different, smaller
 *  vocabulary that calls an operation "APIs". The two are easy to reach for by
 *  mistake because both are "the kinds"; this is the one a CR is filed against.
 */
export const CHANGE_KIND_LABEL = {
  contract: 'Contract', operation: 'Operation', schema: 'Schema',
  table: 'Table', screen: 'Screen', flow: 'Journey', module: 'Module',
  service: 'Service', adr: 'Decision', platform: 'Platform',
  state: 'State model', event: 'Event', other: 'Other',
};

/** The date half of a stored stamp. A slice rather than a parse: every stamp
 *  the service writes is ISO 8601 in UTC, so the first ten characters are the
 *  date and nothing about a timezone can make them something else. */
const day = (value) => (value ?? '').slice(0, 10);

/**
 * One change request — as `/api/changes` hands it over — as a row in that order.
 *
 * `our decision` is **blank while the request is open**, which is the whole of
 * how a blank cell comes to mean "leave this one alone" on the way back. An
 * open request has not been answered, so there is nothing to put there; the
 * `status` column carries the current state for every row including those, so
 * nothing is hidden by it.
 */
export function changeCsvRow(c) {
  const settled = c.status !== 'open';
  return [
    c.rowId,
    c.id,
    c.raisedAt, day(c.raisedAt),
    c.project,
    CHANGE_STATUS_LABEL[c.status] ?? c.status,
    c.blocking ? 'yes' : '',
    // Whose queue. Blank means nobody has said yet, which the page shows as a
    // bucket of its own rather than hiding.
    CHANGE_SIDE_LABEL[c.tag] ?? c.tag ?? '',
    c.platform ?? '',
    CHANGE_KIND_LABEL[c.target?.kind] ?? c.target?.kind ?? '',
    c.target?.id ?? '',
    c.title,
    c.raisedBy ?? '', c.raisedByEmail ?? '',
    c.raisedVia ?? '',
    c.ticket ?? '',
    // Taken on, which is not settled. Blank on an open request older than two
    // days is what the escalation counts.
    c.pickedBy ?? '',
    day(c.pickedAt),
    settled ? (CHANGE_STATUS_LABEL[c.status] ?? c.status) : '',
    c.resolution ?? '',
    c.resolvedRef ?? '',
    day(c.resolvedAt),
    c.resolvedBy ?? '',
    c.problem ?? '', c.evidence ?? '',
    // Pipes rather than commas, because this is one cell in a comma-separated
    // file and a reader who opens it in a text editor should not have to count
    // quotation marks to see where the options end.
    (c.options ?? []).join(' | '),
    c.recommendation ?? '',
  ];
}

/**
 * The whole file, as text.
 *
 * Every field is quoted whether it needs to be or not and an inner quote is
 * doubled — the same CSV the service writes, so a comma inside a `because`
 * lands in the same place whichever button produced the file. The byte order
 * mark is what makes Excel on Windows read the em dashes and curly quotes this
 * package is written in as themselves rather than as mojibake.
 */
export function toChangeCsv(changes) {
  const cell = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
  return '﻿' + [
    CHANGE_CSV_HEADER.join(','),
    ...changes.map((c) => changeCsvRow(c).map(cell).join(',')),
  ].join('\r\n');
}
