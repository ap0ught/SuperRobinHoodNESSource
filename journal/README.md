# Journals

Working notes for Super Robin Hood NES source and the RobinEdit React port.

## Build / assembler (this repo only)

| File | Topic |
|------|--------|
| [01-pds-build-attempt.md](01-pds-build-attempt.md) | PDS assembler port and first `.nes` rebuild attempt |
| [02-assembler-from-magician.md](02-assembler-from-magician.md) | Dialect / bank placement changes vs Magician assembler |
| [03-cart-differences.md](03-cart-differences.md) | Remaining differences vs the Asia cart image |

ROM inventory (Asia dump + `srh-rebuilt.nes` hashes/header/build): **[`docs/ROMS.md`](../docs/ROMS.md)** (mirrored in [robinedit `docs/ROMS.md`](https://github.com/ap0ught/robinedit/blob/main/docs/ROMS.md)).

## RobinEdit / ROM layouts the editor uses

Copied into standalone [ap0ught/robinedit](https://github.com/ap0ught/robinedit) as `journals/` (and mirrored under `robinedit/journals/` here):

| File | Topic |
|------|--------|
| [04-robinedit-react.md](04-robinedit-react.md) | Port overview: EXE → React, ROM map/object layout, feature parity |
| [05-tiles-exe-vs-react.md](05-tiles-exe-vs-react.md) | Metatiles / PP1 / palette: 0.4.4.exe vs canvas path |
| [06-robin-room-spawn.md](06-robin-room-spawn.md) | Room transitions: ±`$D0` Y wrap, ladder shafts, spawn pose |
| [07-map-exits-and-shafts.md](07-map-exits-and-shafts.md) | No exit table — geometry + rim ladders; Exits rail |
| [08-castle-map-numbering.md](08-castle-map-numbering.md) | Map N vs geographic castle overview (`mapheights` + world X) |
| [09-robin-settings-cheatlives.md](09-robin-settings-cheatlives.md) | Robin stats / cheatLives: cart vs dizzy9 vs `patchRobin` |
