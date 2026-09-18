# Source integrity — two defects found while centralising the packs

> **Owner:** Chinmay · **Written:** 18 September 2026 · **Status:** open, neither fixed
>
> Both were found by accident, while recovering from a bad `--apply` run of `tools/index-packs.py`.
> Neither was caused by it. **Both predate today and both are still live.**

---

## 1. Four reference PDFs are committed broken

`sources/requirements/` holds four packs that **do not parse as PDFs at all** — zero page objects,
no `%%EOF`, no `startxref`. This is not a working-tree problem: the **git blob itself is broken**,
so they were committed in this state and every clone has them.

| file in `requirements/` | blob | the real one in `packs/` |
|---|---|---|
| `F_B_Backend_Structure_Module_Sample_Reference_v1_0.pdf` | **126 KB, 0 pages** | `F&B_Backend_Structure_Module Sample Reference v1.0.pdf` — 3.5 MB, **130 pp** |
| `Retail_Backend_Structure_Module_Reference_v1_0.pdf` | **147 KB, 0 pages** | `Retail_Backend_Structure_Module_Reference_v1.0.pdf` — 4.4 MB, **202 pp** |
| `Resource_Management_Configuration_Reference.pdf` | **182 KB, 0 pages** | `Resource_Management_Configuration_Reference.pdf` — 5.8 MB, **169 pp** |
| `TICVAI_Inventory_and_Procurement_Backend_Structure_Sample_v1_0.pdf` | **183 KB, 0 pages** | 5.2 MB, **175 pp** |

**They are roughly 3% of the real file and they are the rank-2 copy.** `sources/README.md` ranks
`requirements/` as the contracted baseline, so the authoritative copy of four packs is the unusable
one and the working copy is filed as mere reference material.

**This is why they read as separate documents to `index-packs.py`** rather than as duplicates: the
hashes genuinely differ, because one side is a broken truncation of the other. A name-based
deduplicator would have deleted the good copy.

**Fix:** replace the four `requirements/` files with the `packs/` bytes, or delete them and record
the requirement authority against the `packs/` copy in `sources/packs-index.json`. **The second is
the point of the index** — authority is a field now, so the file need not exist twice to carry it.

## 2. `core.autocrlf=true` with no `.gitattributes`

Git is applying line-ending conversion to binary files, because nothing tells it not to:

```
core.autocrlf : true
core.eol      : (unset)
.gitattributes: none, at either the repo root or ticvai/
git check-attr text -- <any>.pdf  ->  text: unspecified
```

**The blobs are pristine.** `ACCREDITATION.pdf` and `Payment_Payment_Orchestration.pdf` in git are
byte-identical to the client's originals in `OneDrive_1_18-9-2026.zip`. **The damage happens on
checkout**, when git writes the working copy back with CRLF applied.

**21 tracked files under `sources/` currently differ from their own blob**, 141,748 bytes added in
total:

| type | files | note |
|---|---|---|
| `.pdf` | **12** | `Retail_Dashboard_Screens_Only.pdf` is +229 bytes against the client's copy |
| `.docx` | **2** | |
| `.json` | 4 | `sources/workshop/pack.json` alone is **+108,742** — harmless, JSON ignores line endings |
| `.md` | 2 | harmless |
| `.url` | 1 | harmless |

**The PDFs still opened in every case tested** — `Retail_Dashboard_Screens_Only.pdf` reports its 6
pages, `%%EOF` and `startxref` intact even while inflated. So this is latent rather than breaking
today. **It stops being latent the moment a byte offset matters**, and a PDF xref table is byte
offsets.

It also makes every integrity check unreliable: a file that round-trips through a checkout no
longer hashes to what the client sent, so *"is this the document they gave us"* cannot be answered
by comparing hashes, which is exactly how the four broken files above went unnoticed.

**Fix:** a `.gitattributes` at the repo root marking binaries, then re-checkout the affected paths.

```
*.pdf  binary
*.docx binary
*.xlsx binary
*.pptx binary
*.png  binary
*.jpg  binary
*.jpeg binary
*.gif  binary
*.zip  binary
```

**Adding it does not repair the working tree** — the files must be re-checked-out afterwards, and
the blobs are correct so nothing needs recommitting.

---

## What the bad `--apply` run taught, for the rewrite

`tools/index-packs.py` read well and wrote badly. The reading discipline was copied from
`index-boards.py`; the writing had no equivalent, and three rules are now obvious:

1. **Scope.** Only `reference`, `workshop` and `board` class documents centralise. `mom`,
   `requirement`, `design` and `rfp` are indexed and never moved — `sources/README.md` ranks them
   and the run flattened 102 files across that ranking.
2. **Refuse on mismatch.** Never delete a source when the destination name exists with different
   bytes. The run skipped the copy, deleted the original, and took five files off disk. **Defect 1
   above is exactly the shape that triggers this** — same name, wildly different content.
3. **Never leave an untracked-only canonical.** If the surviving copy is not committed, it is not a
   canonical, and the cleanup afterwards cannot tell a rescue from a leftover.

**The recovery found things worth keeping**, which is the argument for rule 3. Of 72 untracked
files left after `git checkout`, 59 were provably redundant and **13 were not**, including
`TICVAI_Kickoff_MoM_30Jul2026__2_.docx` at its full size and two design files predating today.
A `git clean -fd` would have destroyed all thirteen.
