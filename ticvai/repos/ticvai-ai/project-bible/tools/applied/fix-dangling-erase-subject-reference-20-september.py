#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`pii.erase_subject` does not exist, and a whole ADR was written on the assumption that it did.

`ai.yaml`'s `removeIndexEntry` says: *"**The erasure path.** When a subject is erased
(`pii.erase_subject`) or a page is unpublished, its vectors must go too."* The parenthesis is in
`schema.table` form, so it reads as a table — and **`pii` holds `subject`, `subject_contact`,
`subject_document` and `subject_biometric`, and nothing else.**

It is not an operation either. **The erasure path is `deleteGuestAccount`**, in
`contracts/spine/identity.yaml`, which raises an erasure request rather than deleting
immediately, removes PII from the erasable store, leaves ledger entries holding an opaque
subject reference, and fans the request out across cells under ADR-0010.

**ADR-0047 was written this afternoon saying no erase operation existed, citing this sentence as
the evidence.** A dangling reference in prose, naming the mechanism the rest of the package
relies on, read by the next person as proof the mechanism was absent. It has been corrected in
the ADR; this corrects the sentence that caused it.

**Nothing about the operation changes** — only the reference. `removeIndexEntry` is right about
everything else, including the part that matters most: *"deleting from Postgres does not delete
from Qdrant. Nothing cascades between the two stores, which is why this operation exists rather
than being implied."*

**ADR-0047 adds a second caller and it is named here now**, because the same sentence would
otherwise go stale again the moment `archiveSubject` lands: **derived stores purge at archive,
not at erasure.** A knowledge base still answering from an archived profile is an archive that
did not happen.

    python3 tools/applied/fix-dangling-erase-subject-reference-20-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AI = os.path.join(ROOT, "contracts", "satellite", "ai.yaml")

OLD = """      description: '**The erasure path.** When a subject is erased (`pii.erase_subject`) or a page is
        unpublished, its vectors must go too — a knowledge base that keeps answering from a deleted document
        is a deletion that did not happen.
"""

NEW = """      description: '**The erasure path.** When a subject is erased — by `deleteGuestAccount`, the
        guest''s own request, or by `eraseSubject` where it arrived some other way — or a page is
        unpublished, its vectors must go too: a knowledge base that keeps answering from a deleted
        document is a deletion that did not happen.


        **Called at archive as well as at erasure** (ADR-0047). Archived personal data moves to a
        separate instance and is no longer operationally readable, so a knowledge base still
        answering from it is an archive that did not happen — the same rule one stage earlier.


        **This used to cite `pii.erase_subject`, which is not a table and not an operation.** `pii`
        holds `subject`, `subject_contact`, `subject_document` and `subject_biometric`. The dangling
        name was read as evidence that erasure did not exist, and an ADR was drafted on it.
"""


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(AI, encoding="utf-8").read()

    # **The correction names the old reference on purpose**, so "is the string gone" is the
    # wrong test — it failed on this script's own replacement text. The citation is what must
    # go: the parenthesis that reads as a table a reader could go and look for.
    CITATION = "erased (`pii.erase_subject`)"
    if CITATION not in s:
        print("  already applied")
        return 0
    if s.count(OLD) != 1:
        print("  !! description block matched %d times" % s.count(OLD))
        return 1
    s = s.replace(OLD, NEW)
    print("    removeIndexEntry  pii.erase_subject -> deleteGuestAccount, eraseSubject")

    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! would not parse: %s" % str(e)[:200])
        return 1
    text_n = len(re.findall(r"^      operationId:", s, re.M))
    parsed_n = sum(1 for p in (doc.get("paths") or {}).values() for o in (p or {}).values()
                   if isinstance(o, dict) and o.get("operationId"))
    if text_n != parsed_n:
        print("  !! %d operationId lines, %d parsed" % (text_n, parsed_n))
        return 1
    if CITATION in yaml.safe_dump(doc):
        print("  !! the citation survived")
        return 1
    print("    parses · %d operations intact · no dangling reference left" % parsed_n)

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(AI, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> contracts/satellite/ai.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
