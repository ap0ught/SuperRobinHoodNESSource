# Super Robin Hood ROM images in this tree

Two mapper-71 Super Robin Hood `.nes` images are used here and by [RobinEdit](https://github.com/ap0ught/robinedit): the commercial **Asia** dump and the **PDS rebuild** (`srh-rebuilt.nes`). Both are **65 552** bytes (16-byte header + **64 KiB PRG**, **CHR-RAM**), mapper **71**, vertical mirroring.

RobinEdit’s copy of this note: [`docs/ROMS.md`](https://github.com/ap0ught/robinedit/blob/main/docs/ROMS.md). Cart-vs-rebuild byte gaps: [`journal/03-cart-differences.md`](../journal/03-cart-differences.md).

## Files

| Role | Path(s) in this repo | How produced |
|------|----------------------|--------------|
| Asia dump | `vendor/Super Robin Hood (Asia) (En) (Unl).nes` (canonical); optional root-level duplicate of the same name | Commercial **Asia / En / Unl** cartridge dump — not built here |
| Rebuild | `srh-rebuilt.nes` (prefer [Releases](https://github.com/ap0ught/SuperRobinHoodNESSource/releases/latest)) | `python3 asm/build_srh.py` → assembles `pds_src/src/ROBIN.PRJ` via [ap0ught/pds6502](https://github.com/ap0ught/pds6502) (`asm/pds6502.py` loader), places banks, writes Asia-matching iNES header |

RobinEdit local aliases (gitignored there): `public/asia.nes` ≡ Asia dump; `public/rebuilt.nes` ≡ `srh-rebuilt.nes`.

Related but **different** image: [`prerelease.nes`](https://github.com/ap0ught/SuperRobinHood/tree/master/roms) in [ap0ught/SuperRobinHood](https://github.com/ap0ught/SuperRobinHood) (Wireframe/PDS clean build in that project). CRC/SHA below — not the same as `srh-rebuilt.nes`.

## Fingerprints (headered `.nes`)

| Image | Size | CRC-32 | SHA-256 |
|-------|------|--------|---------|
| Asia (`vendor/…(Asia) (En) (Unl).nes`) | 65552 | `D9114282` | `ae6c7a412732cba05490a4d355b7a619e201583b7f5b99d0148d888293a88076` |
| `srh-rebuilt.nes` | 65552 | `C0E5DBCD` | `0d87e02ab4b0a89d9510feddde32ba8615b165ad429582657347e2f8d8d4998e` |
| SuperRobinHood `prerelease.nes` | 65552 | `44F27107` | `c9882d5415788bc144b7669d27a3ffe42275ab0d1f9aa671d069169dec690582` |

Asia and `srh-rebuilt` share this 16-byte header:

```
4E 45 53 1A  04 00 71 48  00 00 00 07  02 00 00 01
```

- **4** PRG banks (64 KiB), **0** CHR-ROM (CHR-RAM), mapper **71**, vertical mirroring, NES 2.0–style trailer matching the Asia dump.

Same-offset compare Asia ↔ rebuild is ~**40%** (shifts from ZP vs absolute encoding, `flybackvar`, lock/logo path differences, etc.). See [`journal/03-cart-differences.md`](../journal/03-cart-differences.md).

## Build the rebuild

Needs the shared assembler from [ap0ught/pds6502](https://github.com/ap0ught/pds6502) (clone next to this repo as `../pds6502`, or set `PDS6502_HOME`). CI does the same checkout in [`.github/workflows/release-rom.yml`](../.github/workflows/release-rom.yml).

```bash
git clone https://github.com/ap0ught/pds6502.git ../pds6502   # once
python3 asm/build_srh.py
# writes srh-rebuilt.nes and prints per-bank match % vs the Asia dump if present
```

Header constant and bank placement live in `asm/build_srh.py` (`INES_HEADER`, `place()`). Assembler dialect notes: [`journal/01-pds-build-attempt.md`](../journal/01-pds-build-attempt.md), [`journal/02-assembler-from-magician.md`](../journal/02-assembler-from-magician.md).

Do **not** confuse this with `asm/mkrom.py` in sibling projects — that script targets Magician-style MMC3 (128 KiB PRG + CHR-ROM), not Super Robin Hood mapper 71.

## RobinEdit / selftest notes

RobinEdit loads either image: tables are found by **PRG signature**, so Asia file offsets must not be hard-coded. Optional samples:

- Drop dumps into RobinEdit’s `roms/` (preferred empty-screen list), or
- `public/asia.nes` / `public/rebuilt.nes` for quick-load buttons and `make check`.

Selftest (`src/selftest.ts`) on both images: identical object counts `14,8,4,11,29,23,18,31,5,5,4,3,2`; map-4 render **ink** ≈ **277 673** (Asia) vs ≈ **745 472** (rebuild); both must stay ≥ 1000. Higher rebuild ink is normal.

## Which to use

| Goal | Prefer |
|------|--------|
| Match the dumped Asia cart | `vendor/Super Robin Hood (Asia) (En) (Unl).nes` |
| Iterate on assembled `pds_src` | `srh-rebuilt.nes` after `build_srh.py` |
| RobinEdit day-to-day | Either — same layout contract |

## Licensing / copyright caution

- The **Asia dump** is a commercial ROM. Keep redistribution limited to what you are legally allowed to do; treat vendor copies as local reference material.
- **`srh-rebuilt.nes`** is assembled game code from the recovered PDS source. Attribute Wireframe / Oliver Twins material appropriately where those licenses apply; the shipped game remains third-party IP.
- Prefer documenting hashes here over committing new `.nes` blobs into consumer apps such as [robinedit](https://github.com/ap0ught/robinedit) (that repo gitignores `*.nes`).
