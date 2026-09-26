"""Scaffold the frontend starter's apps from the package's app manifests.

The package names its apps by who operates them (ticvai/frontend/*.yaml: guest-app, venue-pos,
venue-management-web, ...) and every screen's implementation.app uses those names. The starter
still had the six generic apps it was created with (backoffice, guest, pos, ...), so 347 findings
in the Block A pull audit (R249, with R031 and R037) were a developer looking for a folder the
package names and the starter does not have.

This makes the starter's apps/ exactly the package's apps, and rewrites the app table in the
starter CLAUDE.md between its markers. Run it after the package adds, renames or removes an app,
then rebuild the setup zip.

    python viewer\\mcp\\setup\\starters\\sync-frontend-apps.py [--package ticvai]
"""
import argparse, json, os, shutil
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
STARTER = os.path.join(HERE, "frontend")
BEGIN, END = "<!-- apps:begin (sync-frontend-apps.py) -->", "<!-- apps:end -->"

ap = argparse.ArgumentParser()
ap.add_argument("--package", default="ticvai")
a = ap.parse_args()
manifests = os.path.join(REPO, a.package, "frontend")

apps = []
for name in sorted(os.listdir(manifests)):
    if not name.endswith(".yaml"):
        continue
    m = yaml.safe_load(open(os.path.join(manifests, name), encoding="utf-8")) or {}
    if not m.get("app"):
        continue
    web = str(m.get("runtime", "")).lower().startswith("reactweb")
    apps.append({"app": m["app"], "operator": m.get("operator", ""), "audience": m.get("audience", ""),
                 "formFactor": m.get("formFactor", ""), "runtime": m.get("runtime", ""),
                 "platform": "web" if web else "react-native", "offline": bool(m.get("offlineCapable")),
                 "platforms": [str(p).split(" ")[0] for p in (m.get("platforms") or [])],
                 "screens": m.get("screenCount")})

apps_dir = os.path.join(STARTER, "apps")
wanted = {x["app"] for x in apps}
for old in os.listdir(apps_dir):
    if old not in wanted:
        shutil.rmtree(os.path.join(apps_dir, old))

for x in apps:
    root = os.path.join(apps_dir, x["app"])
    os.makedirs(os.path.join(root, "src"), exist_ok=True)
    project = {
        "$schema": "../../node_modules/nx/schemas/project-schema.json",
        "name": x["app"],
        "sourceRoot": f"apps/{x['app']}/src",
        "projectType": "application",
        "tags": ["type:app", f"platform:{x['platform']}", f"operator:{x['operator']}",
                 f"offline:{'yes' if x['offline'] else 'no'}"],
        "targets": {
            "lint": {"executor": "nx:run-commands", "options": {"command": "eslint {projectRoot}/src --ext .ts,.tsx"}},
            "test": {"executor": "nx:run-commands", "options": {"command": "vitest run --root {projectRoot} --passWithNoTests"}},
            "typecheck": {"executor": "nx:run-commands", "options": {"command": f"tsc -p apps/{x['app']}/tsconfig.json --noEmit"}},
        },
    }
    json.dump(project, open(os.path.join(root, "project.json"), "w", encoding="utf-8", newline="\n"), indent=2)
    open(os.path.join(root, "project.json"), "a", encoding="utf-8", newline="\n").write("\n")
    open(os.path.join(root, "tsconfig.json"), "w", encoding="utf-8", newline="\n").write(
        '{\n  "extends": "../../tsconfig.base.json",\n  "compilerOptions": { "rootDir": "src", "noEmit": true },\n'
        '  "include": ["src/**/*.ts", "src/**/*.tsx"]\n}\n')
    index = os.path.join(root, "src", "index.ts")
    if not os.path.exists(index):
        open(index, "w", encoding="utf-8", newline="\n").write(
            f"// {x['app']}: {x['audience']} app on {x['formFactor']} ({x['runtime']}), serves {', '.join(x['platforms'])}.\n"
            f"// Screens: `adam_screen` for any screen whose implementation.app is {x['app']}.\n"
            "export {};\n")

rows = ["| App | Runtime | Offline | Serves | Screens |", "|---|---|---|---|---|"]
for x in apps:
    rows.append(f"| `apps/{x['app']}` | {'React web' if x['platform'] == 'web' else 'React Native'} ({x['formFactor']}) | "
                f"{'**yes**' if x['offline'] else 'no'} | {', '.join(x['platforms'])} | {x['screens'] or ''} |")
table = "\n".join([BEGIN,
    "The apps are the package's own (`" + a.package + "/frontend/*.yaml`), named by who operates them. A screen's",
    "`implementation.app` is the folder it goes in; its platform code (P01...) maps to an app here.", "",
    *rows, "",
    "**Adding an app:** the package adds its manifest first; then `python viewer/mcp/setup/starters/sync-frontend-apps.py`",
    "in the ADAM repo scaffolds it here. Do not create an app folder by hand - it would not match the screens.",
    END])

claude = os.path.join(STARTER, "CLAUDE.md")
text = open(claude, encoding="utf-8").read()
if BEGIN in text:
    text = text[:text.index(BEGIN)] + table + text[text.index(END) + len(END):]
else:
    old_rows = [l for l in text.splitlines() if l.startswith("| `apps/")]
    for l in old_rows:
        text = text.replace(l + "\n", "")
    text = text.replace("Import a package as `@ticvai/<name>`", table + "\n\nImport a package as `@ticvai/<name>`", 1)
text = text.replace("React Native apps and a React web app share four packages.",
                    f"{len(apps)} apps (React Native and React web) share four packages.")
open(claude, "w", encoding="utf-8", newline="\n").write(text)

readme = os.path.join(STARTER, "README.md")
r = open(readme, encoding="utf-8").read()
import re
r = re.sub(r"Nx workspace: .*? and four shared packages\.",
           f"Nx workspace: the package's {len(apps)} apps and four shared packages.", r)
open(readme, "w", encoding="utf-8", newline="\n").write(r)
print(f"{len(apps)} apps: " + ", ".join(x["app"] for x in apps))
