import sys, os, glob
import docx

SRC = r"D:\Chinmay\adam\ticvai\sources"
OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, "mom"), exist_ok=True)

def docx_text(path):
    d = docx.Document(path)
    out = []
    body = d.element.body
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    for child in body.iterchildren():
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            t = Paragraph(child, d).text.strip()
            if t: out.append(t)
        elif tag == 'tbl':
            tbl = Table(child, d)
            for row in tbl.rows:
                cells = [c.text.strip().replace('\n', ' / ') for c in row.cells]
                # de-dup merged cells
                ded = []
                for c in cells:
                    if not ded or ded[-1] != c: ded.append(c)
                line = " | ".join(ded).strip()
                if line.strip(" |"): out.append("| " + line + " |")
            out.append("")
    return "\n".join(out)

for f in sorted(glob.glob(os.path.join(SRC, "mom", "*.docx"))):
    name = os.path.splitext(os.path.basename(f))[0]
    try:
        txt = docx_text(f)
    except Exception as e:
        print("FAIL", name, e); continue
    dest = os.path.join(OUT, "mom", name + ".txt")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write("SOURCE FILE: " + os.path.basename(f) + "\n\n" + txt)
    print(f"{name}: {len(txt)} chars, {txt.count(chr(10))+1} lines")
