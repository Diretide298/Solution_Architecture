"""List work packages in project 153 created after a given id (read only). Token from TICVAI_OP_TOKEN.

    python tools/op-recent.py 20476
"""
import base64, json, os, sys, urllib.error, urllib.parse, urllib.request

after = int(sys.argv[1])
auth = "Basic " + base64.b64encode(f"apikey:{os.environ['TICVAI_OP_TOKEN']}".encode()).decode()
filters = json.dumps([{"status": {"operator": "*", "values": []}}])
url = ("https://pms.softlabsgroup.in/api/v3/projects/153/work_packages?pageSize=40"
       + "&sortBy=" + urllib.parse.quote('[["id","desc"]]') + "&filters=" + urllib.parse.quote(filters))
try:
    with urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": auth, "User-Agent": "curl/8.0"}), timeout=120) as r:
        rows = json.load(r)["_embedded"]["elements"]
except urllib.error.HTTPError as e:
    sys.exit(f"{e.code}: {e.read().decode(errors='replace')[:400]}")
for w in sorted((w for w in rows if w["id"] > after), key=lambda w: w["id"]):
    parent = (w["_links"].get("parent") or {}).get("href") or ""
    print(w["id"], w["_links"]["type"]["title"], "parent=" + parent.rsplit("/", 1)[-1], w["subject"][:70])
print("newest in project:", max((w["id"] for w in rows), default=None))
