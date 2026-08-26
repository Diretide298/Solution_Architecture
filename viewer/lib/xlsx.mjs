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
