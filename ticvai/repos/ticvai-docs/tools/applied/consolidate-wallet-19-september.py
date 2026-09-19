#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give the wallet its operations back.

**`wallet.yaml` held 33 operations and every one was configuration.** The acts — read a
balance, top it up, adjust it, transfer it, freeze it, close it, and the whole gift-card
lifecycle — were 13 of `retail.yaml`'s 37. The rule and the act sat in different
contracts, which is the defect this entire run has been about, living in the middle of
the wallet domain.

Two more come from `games.yaml`: `loadGameCredits` ("Load credits onto a card") is a
top-up, and `adjustGameCard` ("Manually adjust credits or points") is a wallet
adjustment. Both appear in the client's own wallet transaction ledger (Wallet
Configuration Backend Structure, board 3.10) as `Top-Up` and `Manual Adjustment`.

## Why the value is wallet and the gameplay is games

The client's balance-type library is declared in the **wallet** module, not the games
module, and it lists `Ride Credit`, `Attraction Credit` and `Redemption Ticket Credit`
beside `F&B / Meal Credit`, `Retail Credit` and `Parking Credit`. One membership purchase
issues several of them at once:

    Gold Membership -> AED 200 F&B Credit -> 2 Parking Credits -> 3 Ride Credits

**A subscription event issues ride credits.** Had ride credit lived in `games.yaml`, the
subscription module would write into games to grant a membership benefit, and
`getWalletLiability` — which aggregates outstanding value across every credit type —
could not see game value at all.

So 35 of games' 37 operations stay exactly where they are: card lifecycle, readers,
pricing, prize catalogue, entitlements, eligibility, gameplay authorisation. **The card is
a credential, not a wallet** — the client is explicit, blocking a lost card "without
affecting the underlying wallet record" (board 7.7). `GameCard` stays in `games.yaml`.

## Why this moves text and not parsed YAML

`retail.yaml` carries nine section-divider comments and `wallet.yaml` three. A
`safe_load`/`safe_dump` round-trip would silently drop all twelve, and the diff would be
the whole file rather than the fifteen blocks that actually moved. There are no YAML
anchors or aliases in any of the three files — the `&` and `*` in them are `F&B` and
markdown bold — so a line-level move is safe.

**The two games operations re-point from `GameCard` to `Wallet`/`WalletTransaction`.**
Referencing `games.yaml` from `wallet.yaml` would make the wallet depend on games, which
is backwards: games depends on the wallet.

Idempotent — a second run finds nothing to move and says so.
Run with no arguments to preview; `--apply` to write.
"""
import io
import re
import sys

MOVES = [
    ("contracts/satellite/retail.yaml", [
        "/wallets/{walletId}/transfer", "/wallets/{walletId}/suspend",
        "/wallets/{walletId}/reinstate", "/wallets/{walletId}/close",
        "/wallets/{subjectId}", "/wallets/{subjectId}/top-ups",
        "/wallets/{subjectId}/transactions", "/wallets/{subjectId}/adjust",
        "/gift-cards", "/gift-cards/{cardCode}", "/gift-cards/{cardCode}/block",
        "/gift-cards/{giftCardId}/activate", "/gift-cards/{giftCardId}/redeem",
    ], ["Wallet", "WalletTransaction", "WalletTransactionKind", "GiftCard",
        "IssueGiftCardRequest"]),
    ("contracts/satellite/games.yaml", [
        "/game-cards/{cardCode}/load", "/game-cards/{cardCode}/adjust",
    ], []),
]
TARGET = "contracts/satellite/wallet.yaml"

# **`ORDER_CREATE` on a top-up was the permission equivalent of the contract split.**
# WALLET_CONFIGURE/OPERATE/VIEW already exist in contracts/shared/permissions.yaml.
PERMS = {
    "getWallet": "WALLET_VIEW", "listWalletTransactions": "WALLET_VIEW",
    "getGiftCard": "WALLET_VIEW",
    "topUpWallet": "WALLET_OPERATE", "adjustWallet": "WALLET_OPERATE",
    "transferWalletBalance": "WALLET_OPERATE", "suspendWallet": "WALLET_OPERATE",
    "reinstateWallet": "WALLET_OPERATE", "closeWallet": "WALLET_OPERATE",
    "issueGiftCard": "WALLET_OPERATE", "activateGiftCard": "WALLET_OPERATE",
    "redeemGiftCard": "WALLET_OPERATE", "blockGiftCard": "WALLET_OPERATE",
    "loadGameCredits": "WALLET_OPERATE", "adjustGameCard": "WALLET_OPERATE",
}


def read(p):
    return io.open(p, encoding="utf-8").read().split("\n")


def write(p, lines):
    io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))


def block(lines, start, indent):
    """Every line of the mapping that opens at `start`, to the next key at <= indent."""
    end = start + 1
    while end < len(lines):
        l = lines[end]
        if l.strip() and not l.startswith(" " * (indent + 1)):
            break
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    return end


def cut(lines, keys, indent):
    """Remove each key's block; return (remaining lines, {key: block lines})."""
    taken, out, i = {}, [], 0
    want = set(keys)
    while i < len(lines):
        m = re.match(r"^%s(\S.*?):\s*$" % (" " * indent), lines[i])
        key = m.group(1) if m else None
        if key and key.strip("'\"") in want:
            e = block(lines, i, indent)
            taken[key.strip("'\"")] = lines[i:e]
            i = e
            continue
        out.append(lines[i])
        i += 1
    return out, taken


def section_end(lines, header, indent):
    """Index just past the last line of the block introduced by `header`."""
    for i, l in enumerate(lines):
        if l.rstrip() == header:
            return block(lines, i, indent)
    raise SystemExit("could not find %r" % header)


def main():
    apply = "--apply" in sys.argv
    tgt = read(TARGET)
    existing = set(re.findall(r"^  (/\S+):\s*$", "\n".join(tgt), re.M))

    new_paths, new_schemas, moved_ops = [], [], []
    sources = {}
    for src, paths, schemas in MOVES:
        lines = read(src)
        todo = [p for p in paths if p not in existing]
        if not todo:
            print("  %s: nothing to move" % src.split("/")[-1])
            sources[src] = lines
            continue
        rest, got = cut(lines, todo, 2)
        missing = [p for p in todo if p not in got]
        if missing:
            raise SystemExit("path(s) not found in %s: %s" % (src, missing))
        rest, gots = cut(rest, schemas, 4)
        for p in todo:
            new_paths += got[p]
        for s in schemas:
            if s not in gots:
                raise SystemExit("schema %s not found in %s" % (s, src))
            new_schemas += gots[s]
        sources[src] = rest
        for ls in got.values():
            moved_ops += re.findall(r"operationId:\s*(\S+)", "\n".join(ls))
        print("  %-14s -> wallet.yaml : %2d path(s), %d schema(s)"
              % (src.split("/")[-1], len(todo), len(schemas)))

    if not new_paths:
        print("\nnothing to do")
        return

    txt = "\n".join(new_paths)
    # The wallet does not depend on games; games depends on the wallet.
    txt = txt.replace("#/components/schemas/GameCard", "#/components/schemas/Wallet")
    for oid, perm in PERMS.items():
        txt = re.sub(r"(operationId:\s*%s\n(?:.*\n)*?\s*x-ticvai-permission:\s*)\S+" % oid,
                     lambda m: m.group(1) + perm, txt)
    # **The client requires guest self-service top-up**, twice: Game & Ride board 10.5
    # ("Allow customers to add value to their game wallet through an enabled kiosk/channel",
    # worked example AED 100 + AED 25 bonus) and Wallet board 1.2, which lists
    # "Online usage / Mobile-app usage" as per-wallet-type capabilities.
    #
    # **The first cut of this used one regex anchored on `operationId: topUpWallet` and it
    # edited the wrong operation.** `topUpWallet` writes its audience in flow style,
    # `x-ticvai-audience: [staff]`, which a block-list pattern cannot match — so the
    # `(?:.*
)*?` ran past it and added `- guest` to `loadGameCredits` instead. Both do
    # want guest, so the result looked right and was reached by accident. Handle both
    # styles, and only inside the operation's own block.
    for oid in ("topUpWallet", "loadGameCredits"):
        m = re.search(r"operationId:\s*%s
" % oid, txt)
        if not m:
            continue
        head, seg = txt[:m.start()], txt[m.start():m.start() + 900]
        tail = txt[m.start() + 900:]
        if "guest" not in seg.split("summary:")[0]:
            seg = re.sub(r"(x-ticvai-audience:\s*\[)([^\]]*)\]",
                         lambda g: g.group(1) + g.group(2) + ", guest]", seg, count=1)
            seg = re.sub(r"(x-ticvai-audience:
(?:\s+- \S+
)+)",
                         lambda g: g.group(1) + re.match(r"\s*", g.group(1).split("
")[1]).group(0)
                         + "- guest
", seg, count=1)
        if "x-ticvai-guest-callable" not in seg:
            seg = re.sub(r"(x-ticvai-audience:[^
]*
(?:\s+- \S+
)*)",
                         lambda g: g.group(1) + "      x-ticvai-guest-callable: true
",
                         seg, count=1)
        txt = head + seg + tail
    new_paths = txt.split("\n")

    pe = section_end(tgt, "paths:", 0)
    se = section_end(tgt, "  schemas:", 2)
    assert pe < se, "paths must precede components in %s" % TARGET
    out = tgt[:pe] + new_paths + tgt[pe:se] + new_schemas + tgt[se:]

    print("\n  %d operation(s) moved: %s" % (len(moved_ops), ", ".join(sorted(moved_ops))))
    if not apply:
        print("\n  nothing written — pass --apply")
        return
    for src, lines in sources.items():
        write(src, lines)
    write(TARGET, out)
    print("  -> %s and %d source(s)" % (TARGET, len(sources)))


if __name__ == "__main__":
    main()
