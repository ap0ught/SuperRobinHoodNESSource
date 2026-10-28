# Attempt to build Super Robin Hood NES source into a .nes

## Progress
Ported magician-nes-re's Python PDS assembler (asm/pds6502.py) to SRH's dialect:
- `&` hex prefix, `defb`/`defw`/`cbm`/`defs` aliases, `do`/`loop`/`list`/`path` no-ops
- macros with dots (`move.val`) and uppercase (`MACRO`)
- banner comments (`*`), control-byte stripping, space-around-commas
- `if` conditions with spaces, branch-base paren fix

## Blocker
Assembly reaches `PRTMESS.ROU:62: beq attrdownrou` -> branch out of range.
Root cause: chained (slot 0) placement instead of proper MMC3 bank slots.
The magician build determines slots by matching against a cartridge dump;
SRH has no reference cartridge in-tree, so placement is undetermined.

## Next steps
- Obtain a Quattro Adventure / Super Robin Hood cartridge dump
- Port build.py's slot-search to SRH's module list
- Or hand-assign banks per ROBIN.PRJ and re-run

## Cartridge found
/extdrive/code/roms/nes/Quattro Adventure (USA) (Unl).nes
- Mapper 232 (Quattro multicart), 16x16KB PRG, CHR-RAM
- Contains 4 games, so SRH's code is a subset; direct byte-match
  against the whole PRG is unreliable for slot placement.

## .nes produced
srh-rebuilt.nes (262160 bytes, Quattro-style header, assembled PRG padded to 256KB)
Branch-out-of-range and chr-symbol warnings remain; not a verified working ROM.
