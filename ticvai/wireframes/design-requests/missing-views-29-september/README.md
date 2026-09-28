# Design request: 8 screens the client prototypes do not show (29 September 2026)

The client approved two prototypes: the POS terminal and the guest web booking (rev 3). Every other screen on
those platforms maps to a view in them. These 8 do not, so they need drawing in the same look.

| Screen | Platform | Style reference |
|---|---|---|
| WEB-014 Pay for a Booking | Guest web | `reference/web/`: checkout and payment step |
| POS-009 Staff Roster | POS | `reference/pos/`: home and the float screen |
| POS-010 Add to Existing Ticket | POS | `reference/pos/`: catalogue, cart and parked carts |
| POS-015 Cash Operations Dashboard | POS | `reference/pos/`: reports and close-out |
| POS-017 Cash In / Cash Out | POS | `reference/pos/`: close-out and the opening float |
| POS-018 Safe Drop & Cash Transfer | POS | `reference/pos/`: close-out |
| POS-019 Shift Templates & Policies | POS | `reference/pos/`: setup |
| POS-024 Outlet Setup | POS | `reference/pos/`: setup |

- `screens.yaml`: what each screen is for, and its states, fields, actions and operations. This is the specification; draw what it says.
- `reference/pos/app.jsx` and `markup.html`: the approved POS terminal source. `outline.txt` lists its views.
- `reference/web/TICVAI Guest Booking v2.dc.html`: the approved web booking, rev 3.
- `frames/`: where the output goes, as one file per screen.

The frame rules are in the prompt. `tools/import-design-frames.py` checks them and refuses a frame that breaks one.
