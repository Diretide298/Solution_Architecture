// A minimal .xlsx reader — enough to pull rows out of a workbook, no more.
//
// An .xlsx is a zip of XML. Node ships the inflate half of that in zlib, so the
// only missing piece is the zip container, which is ~40 lines. That is cheaper
// than a dependency for reading one file the user drops in a folder.

import { inflateRawSync } from 'node:zlib';

const SIG_EOCD = 0x06054b50;
const SIG_CENTRAL = 0x02014b50;

/** name -> uncompressed Buffer, for every entry in the archive. */
function readZip(buf) {
  // the end-of-central-directory record sits in the last 64k, after the comment
  let eocd = -1;
  for (let i = buf.length - 22; i >= Math.max(0, buf.length - 66000); i--) {
    if (buf.readUInt32LE(i) === SIG_EOCD) { eocd = i; break; }
  }
  if (eocd < 0) throw new Error('not a zip archive');

  const count = buf.readUInt16LE(eocd + 10);
  let p = buf.readUInt32LE(eocd + 16);
  const files = new Map();

  for (let i = 0; i < count && p + 46 <= buf.length; i++) {
    if (buf.readUInt32LE(p) !== SIG_CENTRAL) break;
    const method = buf.readUInt16LE(p + 10);
    const compressedSize = buf.readUInt32LE(p + 20);
    const nameLen = buf.readUInt16LE(p + 28);
    const extraLen = buf.readUInt16LE(p + 30);
    const commentLen = buf.readUInt16LE(p + 32);
    const localOffset = buf.readUInt32LE(p + 42);
    const name = buf.toString('utf8', p + 46, p + 46 + nameLen);

    // the central directory's extra field length can differ from the local
    // header's, so the data offset has to come from the local header
    const localNameLen = buf.readUInt16LE(localOffset + 26);
    const localExtraLen = buf.readUInt16LE(localOffset + 28);
    const start = localOffset + 30 + localNameLen + localExtraLen;
    const raw = buf.subarray(start, start + compressedSize);

    try {
      files.set(name, method === 0 ? Buffer.from(raw) : inflateRawSync(raw));
    } catch {
      // a single unreadable entry should not lose the rest of the workbook
    }
    p += 46 + nameLen + extraLen + commentLen;
  }
  return files;
}

const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" };

function decodeXml(text) {
  return text.replace(/&(#x?[0-9a-fA-F]+|[a-z]+);/g, (whole, body) => {
    if (body[0] === '#') {
      const code = body[1] === 'x' ? parseInt(body.slice(2), 16) : parseInt(body.slice(1), 10);
      return Number.isFinite(code) ? String.fromCodePoint(code) : whole;
    }
    return ENTITIES[body] ?? whole;
  });
}

/** Every `<t>` inside an element, concatenated — rich text arrives as runs. */
function textOf(fragment) {
  let out = '';
  const re = /<t[^>]*>([\s\S]*?)<\/t>/g;
  let match;
  while ((match = re.exec(fragment))) out += decodeXml(match[1]);
  return out;
}

function readSharedStrings(xml) {
  const out = [];
  const re = /<si>([\s\S]*?)<\/si>/g;
  let match;
  while ((match = re.exec(xml))) out.push(textOf(match[1]));
  return out;
}

/** "BC7" -> 54. Cells are sparse, so the column has to come from the ref. */
function columnIndex(ref) {
  let n = 0;
  for (const ch of ref) {
    const code = ch.charCodeAt(0);
    if (code < 65 || code > 90) break;
    n = n * 26 + (code - 64);
  }
  return n - 1;
}

const attr = (attrs, name) => attrs.match(new RegExp(`${name}="([^"]*)"`))?.[1] ?? '';

/** One sheet as an array of string rows, blanks preserved by column position. */
function readSheet(xml, shared) {
  const rows = [];
  const rowRe = /<row([^>]*)>([\s\S]*?)<\/row>/g;
  let rowMatch;

  while ((rowMatch = rowRe.exec(xml))) {
    const cells = [];
    const cellRe = /<c([^>]*?)\/>|<c([^>]*?)>([\s\S]*?)<\/c>/g;
    let cellMatch;

    while ((cellMatch = cellRe.exec(rowMatch[2]))) {
      const attrs = cellMatch[1] ?? cellMatch[2] ?? '';
      const inner = cellMatch[3] ?? '';
      const index = columnIndex(attr(attrs, 'r'));
      const type = attr(attrs, 't');

      let value = '';
      if (type === 'inlineStr') {
        value = textOf(inner);
      } else {
        const v = inner.match(/<v[^>]*>([\s\S]*?)<\/v>/);
        if (v) {
          value = decodeXml(v[1]);
          if (type === 's') value = shared[Number(value)] ?? '';
        }
      }

      if (index >= 0) {
        while (cells.length < index) cells.push('');
        cells[index] = value;
      } else {
        cells.push(value);
      }
    }
    rows.push(cells);
  }
  return rows;
}

/**
 * @returns {Map<string, string[][]>} sheet name -> rows, in workbook order
 */
export function readWorkbook(buffer) {
  const files = readZip(buffer);

  const sharedXml = files.get('xl/sharedStrings.xml');
  const shared = sharedXml ? readSharedStrings(sharedXml.toString('utf8')) : [];

  // workbook.xml names the sheets; the rels map each name to its part
  const workbook = files.get('xl/workbook.xml')?.toString('utf8') ?? '';
  const rels = files.get('xl/_rels/workbook.xml.rels')?.toString('utf8') ?? '';

  const target = new Map();
  const relRe = /<Relationship([^>]*)\/>/g;
  let relMatch;
  while ((relMatch = relRe.exec(rels))) {
    target.set(attr(relMatch[1], 'Id'), attr(relMatch[1], 'Target').replace(/^\/?xl\//, ''));
  }

  const sheets = new Map();
  const sheetRe = /<sheet([^>]*)\/>/g;
  let sheetMatch;
  let ordinal = 0;
  while ((sheetMatch = sheetRe.exec(workbook))) {
    ordinal += 1;
    const name = decodeXml(attr(sheetMatch[1], 'name'));
    const rid = attr(sheetMatch[1], 'r:id') || attr(sheetMatch[1], 'id');
    const part = target.get(rid) ?? `worksheets/sheet${ordinal}.xml`;
    const xml = files.get(`xl/${part}`);
    sheets.set(name, xml ? readSheet(xml.toString('utf8'), shared) : []);
  }
  return sheets;
}

// ── writing ──────────────────────────────────────────────────────────
//
// The other half, by the same argument the top of this file makes for reading:
// `deflateRawSync` is in zlib, so all that is missing is the zip container, and
// writing one is about fifty lines. A dependency to emit six sheets of strings
// would be a larger thing to carry than the code below.
//
// **Inline strings, not a shared-strings table.** A shared table is how Excel
// itself writes a workbook and it is smaller when values repeat; it is also a
// second document that has to stay in step with every cell index in every
// sheet, and getting that wrong produces a file that opens with the right shape
// and the wrong words in it. Here the text is in the cell. The files are larger
// and cannot disagree with themselves.

import { deflateRawSync } from 'node:zlib';

/** CRC-32, which the zip container needs per entry. Table built once. */
const CRC = (() => {
  const table = new Int32Array(256);
  for (let n = 0; n < 256; n += 1) {
    let c = n;
    for (let k = 0; k < 8; k += 1) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c;
  }
  return table;
})();

function crc32(buf) {
  let c = -1;
  for (let i = 0; i < buf.length; i += 1) c = CRC[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ -1) >>> 0;
}

/** A zip of `{name, data}` entries, deflated. No directory entries and no
 *  zip64: a workbook of a few megabytes of XML needs neither. */
function writeZip(entries) {
  const locals = [];
  const central = [];
  let offset = 0;

  for (const { name, data } of entries) {
    const nameBuf = Buffer.from(name, 'utf8');
    const deflated = deflateRawSync(data, { level: 6 });
    const sum = crc32(data);

    const local = Buffer.alloc(30 + nameBuf.length);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4);            // version needed to extract
    local.writeUInt16LE(0, 6);             // flags
    local.writeUInt16LE(8, 8);             // deflate
    local.writeUInt16LE(0, 10);            // time, and below the date: fixed at
    local.writeUInt16LE(0x21, 12);         // 1980-01-01 so two runs over the
    local.writeUInt32LE(sum, 14);          // same data produce the same bytes
    local.writeUInt32LE(deflated.length, 18);
    local.writeUInt32LE(data.length, 22);
    local.writeUInt16LE(nameBuf.length, 26);
    local.writeUInt16LE(0, 28);
    nameBuf.copy(local, 30);

    const entry = Buffer.alloc(46 + nameBuf.length);
    entry.writeUInt32LE(0x02014b50, 0);
    entry.writeUInt16LE(20, 4);
    entry.writeUInt16LE(20, 6);
    entry.writeUInt16LE(0, 8);
    entry.writeUInt16LE(8, 10);
    entry.writeUInt16LE(0, 12);
    entry.writeUInt16LE(0x21, 14);
    entry.writeUInt32LE(sum, 16);
    entry.writeUInt32LE(deflated.length, 20);
    entry.writeUInt32LE(data.length, 24);
    entry.writeUInt16LE(nameBuf.length, 28);
    entry.writeUInt16LE(0, 30);
    entry.writeUInt16LE(0, 32);
    entry.writeUInt16LE(0, 34);
    entry.writeUInt16LE(0, 36);
    entry.writeUInt32LE(0, 38);
    entry.writeUInt32LE(offset, 42);
    nameBuf.copy(entry, 46);

    locals.push(local, deflated);
    central.push(entry);
    offset += local.length + deflated.length;
  }

  const directory = Buffer.concat(central);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0);
  end.writeUInt16LE(entries.length, 8);
  end.writeUInt16LE(entries.length, 10);
  end.writeUInt32LE(directory.length, 12);
  end.writeUInt32LE(offset, 16);
  return Buffer.concat([...locals, directory, end]);
}

/** XML text. The five predefined entities, and the control characters XML 1.0
 *  cannot represent at all — package prose has carried a stray one before now,
 *  and a single 0x1a byte makes Excel refuse the whole file rather than that
 *  cell, which is a bug nobody debugs from the symptom. */
function xmlText(value) {
  return String(value)
    .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/** 0 -> "A", 26 -> "AA". */
function columnName(index) {
  let n = index + 1;
  let out = '';
  while (n > 0) {
    const rem = (n - 1) % 26;
    out = String.fromCharCode(65 + rem) + out;
    n = Math.floor((n - rem) / 26);
  }
  return out;
}

// Excel's own ceilings, applied here so the failure is a short sentence rather
// than a file that will not open.
const MAX_SHEET_NAME = 31;
const MAX_CELL = 32767;
const MAX_ROWS = 1048576;

/** Sheet names Excel will accept, and no two the same.
 *
 *  Excel refuses the characters below, refuses an empty name, caps at 31 and
 *  compares case-insensitively. The collision is not hypothetical: "Operations
 *  (contracts)" and "Operations (services)" are the same 31 characters.
 */
function sheetNames(sheets) {
  const used = new Set();
  return sheets.map((sheet, i) => {
    let name = String(sheet.name ?? `Sheet${i + 1}`)
      .replace(/[[\]:*?/\\]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, MAX_SHEET_NAME) || `Sheet${i + 1}`;
    if (used.has(name.toLowerCase())) {
      for (let n = 2; ; n += 1) {
        const suffix = ` ${n}`;
        const tried = name.slice(0, MAX_SHEET_NAME - suffix.length) + suffix;
        if (!used.has(tried.toLowerCase())) { name = tried; break; }
      }
    }
    used.add(name.toLowerCase());
    return name;
  });
}

function sheetXml(sheet) {
  const columns = sheet.columns ?? [];
  const rows = sheet.rows ?? [];
  const all = columns.length ? [columns, ...rows] : rows;
  const body = [];

  all.slice(0, MAX_ROWS).forEach((row, r) => {
    const cells = (row ?? []).map((value, c) => {
      if (value == null || value === '') return '';
      const ref = `${columnName(c)}${r + 1}`;
      // A number stays a number, so a column of counts sorts and adds up. Only
      // a real finite number: an id like 007 or a version like 1.10 is not
      // arithmetic, and Excel would eat the shape of it.
      if (typeof value === 'number' && Number.isFinite(value)) {
        return `<c r="${ref}"><v>${value}</v></c>`;
      }
      const text = xmlText(value).slice(0, MAX_CELL);
      return `<c r="${ref}" t="inlineStr"><is><t xml:space="preserve">${text}</t></is></c>`;
    }).join('');
    body.push(`<row r="${r + 1}">${cells}</row>`);
  });

  // The header row stays put, because a sheet of 230 tables is one you scroll.
  const frozen = columns.length
    ? '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2"'
      + ' activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
    : '';
  const widths = columns.length
    ? `<cols>${columns.map((_, i) => `<col min="${i + 1}" max="${i + 1}"`
      + ` width="${sheet.widths?.[i] ?? 24}" customWidth="1"/>`).join('')}</cols>`
    : '';

  // The used range, stated rather than left to be discovered. Excel copes
  // without it; a streaming reader does not — openpyxl in read_only mode
  // reports max_row as null, and anything sizing a sheet from that gets nothing.
  const wide = all.reduce((n, row) => Math.max(n, (row ?? []).length), 0);
  const deep = Math.min(all.length, MAX_ROWS);
  const dimension = deep
    ? `<dimension ref="A1:${columnName(Math.max(wide, 1) - 1)}${deep}"/>`
    : '';

  return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    + '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
    + `${dimension}${frozen}${widths}<sheetData>${body.join('')}</sheetData></worksheet>`;
}

/**
 * A workbook, as a Buffer.
 *
 * `sheets` is `[{ name, columns, rows, widths }]`: `columns` is the header row
 * and may be left out, `rows` is an array of arrays. Strings and numbers only —
 * anything else is the caller's to stringify, because this module has no idea
 * how a Date or an object should read to a person.
 */
export function writeWorkbook(sheets) {
  const list = (sheets ?? []).filter(Boolean);
  if (!list.length) throw new Error('a workbook needs at least one sheet');
  const names = sheetNames(list);

  const parts = list.map((sheet, i) => ({
    name: `xl/worksheets/sheet${i + 1}.xml`,
    data: Buffer.from(sheetXml(sheet), 'utf8'),
  }));

  const types = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    + '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    + '<Default Extension="xml" ContentType="application/xml"/>'
    + '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
    + list.map((_, i) => `<Override PartName="/xl/worksheets/sheet${i + 1}.xml"`
      + ' ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>').join('')
    + '</Types>';

  const rootRels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    + '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
    + '</Relationships>';

  const workbook = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    + '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    + ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
    + names.map((name, i) => `<sheet name="${xmlText(name)}" sheetId="${i + 1}" r:id="rId${i + 1}"/>`).join('')
    + '</sheets></workbook>';

  const workbookRels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    + names.map((_, i) => `<Relationship Id="rId${i + 1}"`
      + ' Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"'
      + ` Target="worksheets/sheet${i + 1}.xml"/>`).join('')
    + '</Relationships>';

  return writeZip([
    { name: '[Content_Types].xml', data: Buffer.from(types, 'utf8') },
    { name: '_rels/.rels', data: Buffer.from(rootRels, 'utf8') },
    { name: 'xl/workbook.xml', data: Buffer.from(workbook, 'utf8') },
    { name: 'xl/_rels/workbook.xml.rels', data: Buffer.from(workbookRels, 'utf8') },
    ...parts,
  ]);
}
