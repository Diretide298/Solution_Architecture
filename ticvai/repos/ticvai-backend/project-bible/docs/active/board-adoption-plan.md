# Adopting the client boards — the order of work

**157 screens placed. Two tasks asked about: update the contracts, then regenerate the boards.**

They are not two tasks. **They are one chain with four links, and three of them are already
mostly done.**

---

## The dependency, stated once

`wireframes/BRIEF.md` says it in its own table: **"Screen definitions — `screens/P*.yaml` — this
is the specification."**

**Boards are generated from screens. Screens are validated against contracts. Contracts are the
root.**

```
contracts  →  screens  →  boards
   (1)          (2)         (3)
```

**Deleting the old boards is not a task.** It is what happens when a board is regenerated from a
screen file that changed. A board is a rendering, and nothing else in the package points at one
except the screen that owns it.

**This means the order is forced.** Regenerating boards before the screens change produces a
beautiful drawing of the wrong thing, and updating contracts after the screens means screens
naming operations that do not exist — which `check-screens` refuses, so the mistake is loud rather
than silent.

---

## Link 1 — Contracts. Six operations, not a rebuild.

**The audit found the contracts already carry this work.** 34 of 36 POS board screens resolve to
existing operations. F&B has 50 contracted operations and Retail 35.

**Six things the boards describe that the package cannot do:**

| Operation | Why the board needs it |
|---|---|
| `setOfflinePolicy` | What a workstation may do offline, and the limits |
| `setConnectivityThresholds` | When a device decides it is offline, and when it is back |
| `getWorkstationHealth` | A score a manager can sort by — a heartbeat timestamp is not one |
| `setConfigurationProfile` | The board shows 1,248 workstations across four versions |
| `deployConfigurationProfile` | A deployment with a date, which nothing models |
| `listSerialisedItems` | Retail Board 4 — serialisation past the lot number `StockBatch` carries |

**Plus three fields**: peripheral battery and last-check on `RegisteredDevice`, and a health score
on the workstation.

**Half a day.** And **CF-136 closes with it** — the client's Board 1 names nine peripheral kinds,
which is the device list Dinesh has been asked for since 12 August.

---

## Link 2 — Screens. This is the work.

**79 to P08, 22 to P04, 20 to P06, 10 to a new kitchen platform, 26 to a new analytics platform.**

**Three different kinds of change, and conflating them is what broke the last attempt:**

**Improve** — the board draws a better version of a screen that exists. `BO-045 Menu Management`
and the board's `Menu & Product Command Center` are the same screen; the board specifies it
further. **The screen keeps its id, its flows and its navigation, and gains detail.**

**Add** — 14 screens where the operations exist and nothing calls them. Recipe and BOM, production
planning, the reservation calendar, the waitlist.

**Create a platform** — kitchen and analytics. Both narrow, both justified by a property no
existing platform has: the kitchen must survive the network going down, and analytics is read
rather than operated.

**Do them in that order.** Improving is safest and largest; adding is next; new platforms last,
because a new platform with no screens on it is easy to delete and a new platform with thirty is
not.

**Per section, not per domain.** P08 has eight sections and 79 board screens land across four of
them. **A section is a reviewable unit; a domain is not** — the last attempt tried F&B whole and
created four duplicates because it never looked at what P08 held.

---

## Link 3 — Boards. Regenerate, and the old ones go with it.

**`wireframes/BRIEF.md` is already written for this** — for Claude Code, naming five sources and
the patterns. It says to read `P07 Staff Scanner.dc.html` first as the smallest complete example.

**Regenerate the board for a platform when that platform's screens have changed, and not before.**
Thirteen boards exist; five change. **The other eight are correct and touching them is risk with
no return.**

**`check-wireframes` enforces the join.** A board drawing a screen that no longer exists fails; a
screen naming a board anchor that is not there fails. **The deletion is safe because the checker
refuses to let it be silent.**

---

## Link 4 — Reconcile, which is the link people skip

**Flows and navigation break when screens move.** The last attempt proved it twice: removing four
P08 screens broke five navigation links and two flow steps, and the flow checker caught both.

**After each section:**

- `check-screens` — reachability, entry state, density
- `check-flows` — every step's screen and operation still resolve
- `check-package` — lineage, mirrors, permissions
- `tools/refresh.sh` — derives everything downstream

**And a screen that moves platform keeps its id.** `BO-045` becoming a kitchen screen stays
`BO-045` if it can — **an id that changes is every flow, every board anchor and every traceability
row that cites it.**

---

## What I would actually do first

**Not link 1.** Six operations is half a day and it is not the risk.

**The risk is that 157 screens get adopted before Qossai says which document governs.** The boards
contain functionality the matrix does not, and **every screen built against a board whose status is
undecided is a screen whose requirement cannot be cited at sign-off.**

**One line to Qossai, then link 1 the same afternoon.**

---

## The sequence, if you want it as a list

1. **Ask Qossai which document is the specification.** One line.
2. **Six operations and three fields.** Close CF-136 with the peripheral list.
3. **P08 section by section** — Sell first, it takes the most.
4. **P04, then P06.** Both small and both improvements.
5. **The kitchen platform.** Ten screens, and the four that cannot live anywhere else.
6. **The analytics platform.** 26 board screens collapsing to about ten, with a domain selector.
7. **Regenerate five boards.** The other eight stay.
8. **Re-walk traceability.** 157 screens' worth of new evidence against 3,184 requirement rows.

**Steps 3 to 6 are the project. Everything else is a day.**
