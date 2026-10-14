"""Line-level edits to the TICVAI contract YAML: find an operation, a response, a schema; insert lines; nothing is
re-serialised, so comments, quoting, CRLF and layout survive."""
import re
from pathlib import Path

VERBS = ('get', 'put', 'post', 'patch', 'delete')


class Doc:
    def __init__(self, path):
        self.path = Path(path)
        raw = self.path.read_bytes().decode('utf-8')
        self.lines = raw.splitlines(keepends=True)
        crlf = sum(1 for l in self.lines if l.endswith('\r\n'))
        self.eol = '\r\n' if crlf > len(self.lines) / 2 else '\n'
        self.dirty = False

    def save(self):
        if self.dirty:
            self.path.write_bytes(''.join(self.lines).encode('utf-8'))

    # --- reading ---------------------------------------------------------------------------------------------
    @staticmethod
    def text(line):
        return line.rstrip('\r\n')

    def indent(self, i):
        s = self.text(self.lines[i])
        return len(s) - len(s.lstrip(' '))

    def blank(self, i):
        s = self.text(self.lines[i]).strip()
        return not s or s.startswith('#')

    def block_end(self, i):
        """First line after i whose indent is <= indent(i) (blank and comment lines never end a block). A list item
        line `- x` at the same indent as its parent key does not end the parent's block when i is a `key:` line
        whose value is that list."""
        ind = self.indent(i)
        head = self.text(self.lines[i]).strip()
        j = i + 1
        while j < len(self.lines):
            if not self.blank(j):
                s = self.text(self.lines[j])
                k = self.indent(j)
                if k < ind:
                    return j
                if k == ind:
                    if s.lstrip().startswith('- ') and head.endswith(':') and not head.startswith('- '):
                        j += 1
                        continue
                    return j
            j += 1
        return len(self.lines)

    def end_trim(self, end):
        """Back over trailing blank lines so an insertion at a block's end sits before the gap."""
        while end > 0 and not self.text(self.lines[end - 1]).strip():
            end -= 1
        return end

    def child(self, i, key, end=None):
        """The direct child line `key:` of the block at line i (or None). key compared after stripping quotes."""
        end = end if end is not None else self.block_end(i)
        ci = self.child_indent(i, end)
        for j in range(i + 1, end):
            if self.blank(j) or self.indent(j) != ci:
                continue
            s = self.text(self.lines[j]).strip()
            m = re.match(r"""^(['"]?)([^'":]+)\1\s*:(\s|$)""", s)
            if m and m.group(2) == str(key):
                return j
        return None

    def child_indent(self, i, end=None):
        end = end if end is not None else self.block_end(i)
        for j in range(i + 1, end):
            if not self.blank(j):
                return self.indent(j)
        return self.indent(i) + 2

    def find_op(self, oid):
        """(method line, end line) of the operation."""
        pat = re.compile(r"""^\s*operationId:\s*['"]?%s['"]?\s*$""" % re.escape(oid))
        for i, l in enumerate(self.lines):
            if pat.match(self.text(l)):
                ind = self.indent(i)
                for j in range(i - 1, -1, -1):
                    if not self.blank(j) and self.indent(j) < ind:
                        s = self.text(self.lines[j]).strip()
                        if s.rstrip(':') in VERBS:
                            return j, self.block_end(j)
                        break
        raise KeyError(oid)

    def find_path_item(self, path):
        for i, l in enumerate(self.lines):
            s = self.text(l)
            if self.indent(i) == 2 and re.match(r"""^\s*(['"]?)%s\1\s*:\s*$""" % re.escape(path), s):
                return i
        return None

    def paths_line(self):
        for i, l in enumerate(self.lines):
            if self.text(l) == 'paths:':
                return i
        raise KeyError('paths')

    def find_schema(self, name):
        comp = None
        for i, l in enumerate(self.lines):
            if self.text(l) == 'components:':
                comp = i
                break
        sch = self.child(comp, 'schemas')
        return self.child(sch, name)

    def response(self, oid, code):
        m, end = self.find_op(oid)
        r = self.child(m, 'responses', end)
        if r is None:
            return None
        return self.child(r, str(code))

    # --- writing ---------------------------------------------------------------------------------------------
    def insert(self, at, texts):
        self.lines[at:at] = [t + self.eol for t in texts]
        self.dirty = True

    def delete(self, a, b):
        del self.lines[a:b]
        self.dirty = True


def sq(s):
    """A YAML single-quoted scalar."""
    return "'" + str(s).replace("'", "''") + "'"
