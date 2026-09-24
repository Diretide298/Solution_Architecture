import sys, os, glob, pdfplumber
OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, "boards"), exist_ok=True)
paths = sorted(glob.glob(r"D:\Chinmay\adam\ticvai\sources\boards\*.pdf"))
paths.append(r"D:\Chinmay\adam\ticvai\sources\requirements\Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf")
for p in paths:
    name = os.path.splitext(os.path.basename(p))[0]
    try:
        with pdfplumber.open(p) as pdf:
            chunks = []
            for i, page in enumerate(pdf.pages, 1):
                t = page.extract_text() or ""
                chunks.append(f"--- page {i} ---\n{t}")
            txt = "\n".join(chunks)
    except Exception as e:
        print("FAIL", name, e); continue
    with open(os.path.join(OUT, "boards", name + ".txt"), "w", encoding="utf-8") as fh:
        fh.write("SOURCE FILE: " + os.path.basename(p) + "\n\n" + txt)
    print(f"{name}: {len(txt)} chars")
