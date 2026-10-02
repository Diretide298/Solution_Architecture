#!/usr/bin/env python3
"""Retire the 13 duplicate first-release setup operations the section merges kept (2 October 2026, r2).

**Chinmay, 2 October 2026: "13 dupes would be gone in r2."** The ADM-049 move (CHG-MOV-002) merged the workshop-pack
builders into the venue screens as sections and kept their own writers, because the first-release slice and 13
pushed APP-SETUP-ADM tickets named them (CHG-MOV-008 logged the question). Each duplicates a typed writer the venue
screen already calls:

  setPriceListMaster         ADM-049  -> BO-009 createPriceList / updatePriceList (now carrying the master fields)
  setRateStructure           ADM-051  -> BO-009 setPrices
  createBulkProductCatalogue ADM-121  -> BO-117 importProductCatalogue / commitCatalogueImport
  setPromotionRule           ADM-148  -> BO-010 createPromotion / updatePromotion (ADM-210 declared it too)
  setCouponPromoCode         ADM-159  -> BO-010 createCouponCampaign / generateCouponCodes
  setBuyGetBogo              ADM-169  -> BO-010 createPromotion (Discount buyXGetY)
  setFixedPriceOffer         ADM-172  -> BO-010 createPromotion (Discount, maxApplicationsPerBasket)
  setGiftFreeProduct         ADM-173  -> BO-010 createPromotion (Discount freeItem, rewardProductIds)
  setCrossCategoryPromotion  ADM-174  -> BO-010 createPromotion (PromotionConditions)
  setEligibilityRule         ADM-199  -> BO-010 createPromotion (PromotionConditions)
  setBundleDefinition        ADM-179  -> BO-011 createBundle / updateBundle
  setBundleComponent         ADM-180  -> BO-011 createBundle (BundleComponent)
  setGuestChoiceBuild        ADM-181  -> BO-011 createBundle (BundleChoiceGroup)

This removes the operations from the contracts (approved breaking changes BC-008..BC-020, tag r2), unbinds them from
the screens (each ADM id stays as the anchor of its section), points the board flows' steps at no operation, repoints
the design-note sources to the retired request schema (kept, marked retired) and withdraws the corrections the
retirement made moot. The tickets are retired by tools/op-retire.py (REPLACED, REPLACED_OPS). CHG-CLN-001..003.

    python3 tools/applied/retire-duplicate-setup-ops-2-october.py [--apply]

Run once; a second run finds nothing to retire.
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
P08 = ROOT / "screens" / "P08-venue-back-office.yaml"
NOTES = ROOT / "handoff" / "design-notes"
FLOWS = ROOT / "flows"
CHG = "CHG-CLN-001"
DAY = "2 October 2026"

# op: (contract file, the section screen, the venue screen, its typed writers, the schema the notes cite, BC id)
RETIRE = {
    "setPriceListMaster": ("spine/catalogue", "ADM-049", "BO-009", ["createPriceList", "updatePriceList"],
                           "PriceListMasterConfigurationInput", "BC-008"),
    "setRateStructure": ("spine/catalogue", "ADM-051", "BO-009", ["setPrices"], "RateStructureBuilderInput", "BC-009"),
    "createBulkProductCatalogue": ("spine/catalogue", "ADM-121", "BO-117", ["importProductCatalogue", "commitCatalogueImport"],
                                   "BulkProductCreationCatalogueImportInput", "BC-010"),
    "setPromotionRule": ("satellite/promotions", "ADM-148", "BO-010", ["createPromotion", "updatePromotion"],
                         "PromotionRuleBuilderInput", "BC-011"),
    "setCouponPromoCode": ("satellite/promotions", "ADM-159", "BO-010", ["createCouponCampaign", "generateCouponCodes"],
                           "CouponPromoCodeBuilderInput", "BC-012"),
    "setBuyGetBogo": ("satellite/promotions", "ADM-169", "BO-010", ["createPromotion"], "BuyXGetYBogoRuleBuilderInput",
                      "BC-013"),
    "setFixedPriceOffer": ("satellite/promotions", "ADM-172", "BO-010", ["createPromotion"],
                           "FixedPriceNForXOfferBuilderInput", "BC-014"),
    "setGiftFreeProduct": ("satellite/promotions", "ADM-173", "BO-010", ["createPromotion"],
                           "GiftFreeProductAddedValueOfferBuilderInput", "BC-015"),
    "setCrossCategoryPromotion": ("satellite/promotions", "ADM-174", "BO-010", ["createPromotion"],
                                  "CrossCategoryPromotionBuilderInput", "BC-016"),
    "setEligibilityRule": ("satellite/promotions", "ADM-199", "BO-010", ["createPromotion"], "EligibilityRuleBuilderInput",
                           "BC-017"),
    "setBundleDefinition": ("satellite/promotions", "ADM-179", "BO-011", ["createBundle", "updateBundle"],
                            "BundleDefinitionSetupInput", "BC-018"),
    "setBundleComponent": ("satellite/promotions", "ADM-180", "BO-011", ["createBundle"], "BundleComponentBuilderInput",
                           "BC-019"),
    "setGuestChoiceBuild": ("satellite/promotions", "ADM-181", "BO-011", ["createBundle"],
                            "GuestChoiceBuildYourOwnBundleDesignerInput", "BC-020"),
}
ALSO_DECLARED = {"ADM-210": ["setPromotionRule"]}
VERBS = ("get", "put", "post", "patch", "delete")


def read(path: Path):
    raw = path.read_bytes().decode("utf-8")
    return raw, yaml.load(raw.replace("\r\n", "\n"), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))


def write(path: Path, raw: str, doc) -> None:
    out = yaml.dump(doc, Dumper=yaml.SafeDumper, sort_keys=False, allow_unicode=True, width=100)
    path.write_bytes((out.replace("\n", "\r\n") if "\r\n" in raw else out).encode("utf-8"))


def text(path: Path):
    raw = path.read_bytes().decode("utf-8")
    return raw, "\r\n" in raw, raw.replace("\r\n", "\n").split("\n")


def put(path: Path, crlf: bool, lines: list) -> None:
    body = "\n".join(lines)
    path.write_bytes((body.replace("\n", "\r\n") if crlf else body).encode("utf-8"))


def ind(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def block_end(lines: list, i: int) -> int:
    """The first line after the block that starts at i (by indentation; blank lines belong to it)."""
    n = ind(lines[i])
    j = i + 1
    while j < len(lines) and (not lines[j].strip() or ind(lines[j]) > n):
        j += 1
    return j


# ------------------------------------------------------------------------------------------------ contracts
def retire_in_contract(lines: list, op: str, log: list) -> list:
    at = next((k for k, ln in enumerate(lines) if re.match(rf"^\s+operationId:\s*['\"]?{op}['\"]?\s*$", ln)), None)
    if at is None:
        log.append(f"  {op}: not in the contract (already retired?)")
        return lines
    verb = next(k for k in range(at, -1, -1) if re.match(r"^    (get|put|post|patch|delete):\s*$", lines[k]))
    path = next(k for k in range(verb, -1, -1) if re.match(r"^  /\S*:\s*$", lines[k]))
    pend = block_end(lines, path)
    keys = [lines[k].strip().rstrip(":") for k in range(path + 1, pend) if ind(lines[k]) == 4 and lines[k].strip()]
    others = [k for k in keys if k in VERBS and k != lines[verb].strip().rstrip(":")]
    if others:
        log.append(f"  {op}: {lines[verb].strip()} removed from {lines[path].strip()} (keeps {', '.join(others)})")
        return lines[:verb] + lines[block_end(lines, verb):]
    log.append(f"  {op}: path {lines[path].strip()} removed")
    return lines[:path] + lines[pend:]


def mark_schema(lines: list, name: str, op: str, bc: str) -> list:
    at = next((k for k, ln in enumerate(lines) if ln == f"    {name}:"), None)
    if at is None or any("x-ticvai-retired" in lines[k] for k in range(at, block_end(lines, at))):
        return lines
    note = (f"      x-ticvai-retired: '{op} was removed in r2 ({bc}, {CHG}); no operation takes this shape. Kept "
            "because the design notes and the readiness close-out cite it; the venue screen''s typed writer carries "
            "the record.'")
    return lines[:at + 1] + [note] + lines[at + 1:]


def replace_once(lines: list, old: str, new: str, log: list) -> list:
    body = "\n".join(lines)
    if old not in body:
        log.append(f"  text not found (already edited?): {old[:70]!r}")
        return lines
    return body.replace(old, new, 1).split("\n")


PRICE_LIST_FIELDS = """\
        description:
          type: string
          nullable: true
          description: >-
            **The price list master fields** (data model DM3) are written here since setPriceListMaster was
            retired in r2 (BC-008, CHG-CLN-001); each is optional and means what it means on `PriceList`.
        priceListType:
          type: string
          enum: [standardRetail, venue, attraction, event, membership, group, corporate, b2b, reseller, ota,
                 internal, specialMarket]
        ownerPrincipalId:
          type: string
          format: uuid
          nullable: true
        tags:
          type: array
          items:
            type: string
        legalEntityId:
          type: string
          format: uuid
          nullable: true
        brand:
          type: string
          maxLength: 100
          nullable: true
        businessUnit:
          type: string
          maxLength: 100
          nullable: true
        countryCode:
          type: string
          maxLength: 2
          nullable: true
          pattern: ^[A-Z]{2}$
        marketCode:
          type: string
          maxLength: 40
          nullable: true
        scopeLevel:
          type: string
          enum: [global, country, market, brand, venue, event, businessUnit]
        defaultPriceCategoryId:
          type: string
          format: uuid
          nullable: true
        roundingProfileId:
          type: string
          format: uuid
          nullable: true
        priceResolutionPolicyId:
          type: string
          format: uuid
          nullable: true
        allowOverrides:
          type: boolean
        allowInheritance:
          type: boolean
        allowMultipleCurrencies:
          type: boolean
        allowProductSpecificRates:
          type: boolean"""


def add_price_list_fields(lines: list, log: list) -> list:
    """CreatePriceListRequest and updatePriceList's body take the master fields setPriceListMaster held (additive)."""
    at = next((k for k, ln in enumerate(lines) if ln == "    CreatePriceListRequest:"), None)
    if at is None or any("retired in r2 (BC-008" in lines[k] for k in range(at, block_end(lines, at))):
        log.append("  CreatePriceListRequest already carries the master fields")
        return lines
    end = block_end(lines, at)
    while not lines[end - 1].strip():
        end -= 1
    lines = lines[:end] + PRICE_LIST_FIELDS.split("\n") + lines[end:]
    # updatePriceList's inline body: after `isActive: { type: boolean }` style lines of its properties
    op = next(k for k, ln in enumerate(lines) if re.match(r"^\s+operationId:\s*updatePriceList\s*$", ln))
    props = next(k for k in range(op, len(lines)) if lines[k].strip() == "properties:" and ind(lines[k]) == 14)
    pend = block_end(lines, props)
    while not lines[pend - 1].strip():
        pend -= 1
    extra = [(" " * 8 + x) if x.strip() else x for x in PRICE_LIST_FIELDS.split("\n")]
    lines = lines[:pend] + extra + lines[pend:]
    log.append("  CreatePriceListRequest and updatePriceList take the price list master fields")
    return lines


def apply_contracts(apply: bool) -> None:
    log: list = []
    for cf in sorted({v[0] for v in RETIRE.values()}):
        path = ROOT / "contracts" / f"{cf}.yaml"
        raw, crlf, lines = text(path)
        for op, (c, sid, tid, typed, schema, bc) in RETIRE.items():
            if c != cf:
                continue
            lines = retire_in_contract(lines, op, log)
            lines = mark_schema(lines, schema, op, bc)
            lines = mark_schema(lines, schema.replace("Input", "View"), op, bc)
        if cf == "spine/catalogue":
            lines = replace_once(
                lines, "Quick actions Create Price List (setPriceListMaster),",
                "Quick actions Create Price List (createPriceList on BO-009; setPriceListMaster retired in r2, BC-008),", log)
            lines = replace_once(
                lines, "Price list master fields (29 September, data model DM3), set with `setPriceListMaster` (ADM-058).",
                "Price list master fields (29 September, data model DM3), set with `createPriceList` and `updatePriceList` "
                "since setPriceListMaster was retired in r2 (BC-008, CHG-CLN-001).", log)
            lines = add_price_list_fields(lines, log)
        else:
            lines = replace_once(
                lines, "gift of `freeItem`, the \"different product\" of a `buyXGetY` (setGiftFreeProduct, setBuyGetBogo).",
                "gift of `freeItem`, the \"different product\" of a `buyXGetY` (createPromotion; the builders "
                "setGiftFreeProduct and setBuyGetBogo were retired in r2, CHG-CLN-001).", log)
            lines = replace_once(
                lines, "an N-for-X offer (setFixedPriceOffer).",
                "an N-for-X offer (createPromotion; setFixedPriceOffer was retired in r2, CHG-CLN-001).", log)
            lines = replace_once(
                lines, "with no promotion of their own, saved by setEligibilityRule) that must also hold.",
                "with no promotion of their own) that must also hold. **Deprecated in r2** (CHG-CLN-001): "
                "setEligibilityRule, which saved library rules, was retired (BC-017), so no operation creates one; "
                "send the conditions inline. Rules already saved still apply.", log)
            lines = replace_once(
                lines, "A rule made in the Promotion Rule Builder (setPromotionRule, `ruleType: benefit`) or\n"
                       "        the Eligibility Rule Builder (setEligibilityRule, `ruleType: eligibility`).",
                "A rule made in the Promotion Rule Builder (`ruleType: benefit`) or the Eligibility Rule\n"
                "        Builder (`ruleType: eligibility`). **No operation writes it since r2**: setPromotionRule and\n"
                "        setEligibilityRule were retired (BC-011, BC-017, CHG-CLN-001) and createPromotion carries\n"
                "        the conditions; the table stays until a forward migration drops it.", log)
        print(f"{cf}.yaml")
        for line in log:
            print(line)
        log.clear()
        if apply:
            put(path, crlf, lines)


# ------------------------------------------------------------------------------------------------ screens
def comps(s):
    for r in ((s.get("layout") or {}).get("regions") or []):
        for c in (r.get("components") or []):
            yield r, c


def apply_screens(apply: bool) -> None:
    raw, d = read(P08)
    S = {s["id"]: s for s in d["screens"]}
    by_screen = {}
    for op, (c, sid, tid, typed, schema, bc) in RETIRE.items():
        by_screen.setdefault(sid, []).append(op)
    for sid, ops in ALSO_DECLARED.items():
        by_screen.setdefault(sid, []).extend(ops)
    changed = 0
    for sid, ops in by_screen.items():
        s = S[sid]
        before = [a.get("operationId") for a in s.get("apis") or []]
        if not set(ops) & set(before):
            print(f"  {sid}: nothing to unbind")
            continue
        changed += 1
        s["apis"] = [a for a in s.get("apis") or [] if a.get("operationId") not in ops]
        for _, c in comps(s):
            if c.get("operation") in ops:
                op = c.pop("operation")
                if str(c.get("provenance", "")).startswith("contract operation"):
                    c["provenance"] = f"contract operation {op}, retired in r2 ({CHG})"
        for o in s.get("overlays") or []:
            for k in ("confirm", "dismiss"):
                if isinstance(o.get(k), dict) and o[k].get("operation") in ops:
                    o[k].pop("operation")
        for t in (s.get("navigation") or {}).get("transitions") or []:
            if t.get("operation") in ops:
                t.pop("operation")
                t.pop("carries", None)
        if s.get("gaps"):
            s["gaps"] = [g for g in s["gaps"] if not any(o in str(g.get("why")) or o in str(g.get("source"))
                                                         for o in ops)]
            if not s["gaps"]:
                del s["gaps"]
        mine = [o for o in ops if o in RETIRE and RETIRE[o][1] == sid]
        if mine:
            op = mine[0]
            _, _, tid, typed, _, bc = RETIRE[op]
            tname = S[tid]["name"]
            note = (f"**Its own writer is retired in r2** (decided {DAY}, Chinmay: \"13 dupes would be gone in r2\"; "
                    f"{CHG}). `{op}` duplicated {tid} {tname}'s {' and '.join(typed)}, so it is removed from the "
                    f"contract ({bc}) and {tid} saves this record. This id stays the anchor of its section of {tid}: "
                    "nothing on it writes separately.")
            s["apisNote"] = (str(s.get("apisNote") or "") + f" **{DAY} ({CHG}):** {op} retired in r2 ({bc}); "
                             f"{tid} {tname} writes the record with {' and '.join(typed)}.").strip()
            states = s.get("states") or {}
            if not s["apis"]:
                if "emptyNoAccess" in states:
                    states["emptyNoAccess"] = (f"Shown when the caller lacks the permission {tid} {tname} requires; "
                                               "this section has no operation of its own since its writer was "
                                               "retired, so it names that screen's.")
                for k in ("emptyFirstRun",):
                    if "Carries the create action" in str(states.get(k) or ""):
                        states[k] = (f"Nothing saved yet. The create action is {tid}'s ({' and '.join(typed)}); "
                                     "this section offers none of its own.")
        else:
            note = (f"**{', '.join(ops)} unbound in r2** (decided {DAY}; {CHG}): the duplicate writer was removed from "
                    "the contract; this screen keeps its own operation.")
        old = s.get("notes")
        s["notes"] = note + ("\n\n" + old if old else "")
        print(f"  {sid}: unbound {', '.join(o for o in ops if o in before)}; apis now "
              f"{[a.get('operationId') for a in s['apis']]}")
    if apply and changed:
        write(P08, raw, d)


# ------------------------------------------------------------------------------------------------ flows
def apply_flows(apply: bool) -> None:
    """Each step's retired operation leaves its list (an emptied list becomes []); the first step on the section
    screen says where the record is saved now, in its action."""
    pat = re.compile(rf"^(\s*)-\s+({'|'.join(RETIRE)})\s*$")
    for f in sorted(FLOWS.glob("F*.yaml")):
        raw, crlf, lines = text(f)
        if not any(pat.match(ln) for ln in lines):
            continue
        starts = [k for k, ln in enumerate(lines) if re.match(r"^- step:", ln)] + [len(lines)]
        head = lines[:starts[0]]
        out, n, said = list(head), 0, set()
        for a, b in zip(starts, starts[1:]):
            step = lines[a:b]
            screen = next((re.sub(r"^\s*screen:\s*", "", x).strip() for x in step if re.match(r"^\s+screen:", x)), "")
            hit = [pat.match(x).group(2) for x in step if pat.match(x)]
            if hit:
                n += len(hit)
                kept = []
                for i, x in enumerate(step):
                    if pat.match(x):
                        continue
                    kept.append(x)
                for i, x in enumerate(kept):
                    if x.strip() == "operations:" and not (i + 1 < len(kept) and re.match(r"^\s+-\s", kept[i + 1])):
                        kept[i] = x.rstrip() + " []"
                for op in hit:
                    _, sid, tid, typed, _, bc = RETIRE[op]
                    if screen == sid and op not in said:
                        said.add(op)
                        for i, x in enumerate(kept):
                            m = re.match(r"^(\s+action:\s*)(.*)$", x)
                            if m and not m.group(2).startswith(("'", '"', ">", "|")):
                                kept[i] = (m.group(1) + m.group(2).rstrip(".") + f", a section of {tid}, which saves "
                                           f"the record with {' and '.join(typed)} ({op} retired in r2, {CHG})")
                                break
                step = kept
            out.extend(step)
        print(f"  {f.name}: {n} step operation(s) removed")
        if apply:
            put(f, crlf, out)


# ------------------------------------------------------------------------------------------------ design notes
def apply_notes(apply: bool) -> None:
    sources = {}
    for op, (c, sid, tid, typed, schema, bc) in RETIRE.items():
        sources[f"contracts/{c}.yaml#{op}"] = f"contracts/{c}.yaml#/components/schemas/{schema}"
    screens = {v[1] for v in RETIRE.values()}
    for f in sorted(NOTES.glob("*.yaml")):
        raw, crlf, lines = text(f)
        if not any(k in raw for k in sources):
            continue
        cur, out, changed = None, [], 0
        k = 0
        while k < len(lines):
            ln = lines[k]
            m = re.match(r"^  ([A-Z]{2,4}-\d{3,4}):\s*$", ln)
            if m:
                cur = m.group(1)
            if cur in screens and re.match(r"^    - what:", ln):
                e = block_end(lines, k) if False else k + 1
                while e < len(lines) and lines[e].strip() and ind(lines[e]) > 4 and not re.match(r"^    - ", lines[e]):
                    e += 1
                item = lines[k:e]
                body = "\n".join(item)
                if any(src in body for src in sources) and "status: logged" in body:
                    status = "fixed" if "duplicat" in body.lower() or "second" in body.lower() else "withdrawn"
                    item = [x.replace("status: logged", f"status: {status}") for x in item]
                    item = [re.sub(r"^(\s+by:\s*)CHG-[A-Z]+-\d+\s*$", rf"\g<1>{CHG}", x) for x in item]
                    changed += 1
                out.extend(item)
                k = e
                continue
            out.append(ln)
            k += 1
        body = "\n".join(out)
        n = 0
        for old, new in sources.items():
            n += body.count(old)
            body = re.sub(re.escape(old) + r"(?![A-Za-z])", new, body)
        print(f"  {f.relative_to(ROOT).as_posix()}: {changed} correction(s) closed, {n} source(s) repointed")
        if apply:
            put(f, crlf, body.split("\n"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    apply_contracts(a.apply)
    apply_screens(a.apply)
    apply_flows(a.apply)
    apply_notes(a.apply)
    print("applied" if a.apply else "dry run: --apply writes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
