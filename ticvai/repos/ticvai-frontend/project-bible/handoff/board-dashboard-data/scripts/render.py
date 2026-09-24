import pdfplumber, os, sys
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
files = [
 "FB_Dashboard_Screens_v1_0.pdf",
 "Inventory_Procurement_Dashboard_Screens.pdf",
 "Retail_Dashboard_Screens_Only.pdf",
 "TICVAI_POS_Frontline_Dashboard_Screens_Reference_v1_0.pdf",
 "TICVAI_Resource_Management_All_Screens_v1_0.pdf",
 "TICVAI_Ticket_Types_Dashboard_Screens_High_Resolution.pdf",
]
short = {
 "FB_Dashboard_Screens_v1_0.pdf": "FB",
 "Inventory_Procurement_Dashboard_Screens.pdf": "INVPROC",
 "Retail_Dashboard_Screens_Only.pdf": "RETAIL",
 "TICVAI_POS_Frontline_Dashboard_Screens_Reference_v1_0.pdf": "POSFRONT",
 "TICVAI_Resource_Management_All_Screens_v1_0.pdf": "RESMGMT",
 "TICVAI_Ticket_Types_Dashboard_Screens_High_Resolution.pdf": "TICKETTYPES",
}
for f in files:
    p = os.path.join(r"D:\Chinmay\adam\ticvai\sources\boards", f)
    s = short[f]
    with pdfplumber.open(p) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            dest = os.path.join(OUT, f"{s}-p{i:02d}.png")
            page.to_image(resolution=170).save(dest)
            print(f"{os.path.basename(dest)}  {os.path.getsize(dest)//1024} KB")
