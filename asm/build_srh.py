#!/usr/bin/env python3
"""Assemble pds_src/src/ROBIN.PRJ with asm/pds6502.py and write a 64 KiB iNES ROM.

PDS `bank N` downloads every byte assembled since the previous `bank`. Super
Robin Hood is mapper 71: a 16 KiB bank at $8000 and a fixed bank at $C000. The
retail cart is 64 KiB, and the values the game stores (12, 13, 14) select
those 16 KiB banks with the low two bits, so bank 12 lands in the first 16 KiB.
Bytes assembled at $C000-$FFFF are the fixed bank, the last 16 KiB.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pds6502

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "pds_src" / "src"
PROJ = SRC / "ROBIN.PRJ"
OUT = ROOT / "asm" / "out"
RETAIL = ROOT / "Super Robin Hood (Asia) (En) (Unl).nes"

# Retail header: 64 KiB PRG, CHR-RAM, mapper 71, NES 2.0.
INES_HEADER = bytes([
    0x4E, 0x45, 0x53, 0x1A,
    0x04, 0x00, 0x71, 0x48,
    0x00, 0x00, 0x00, 0x07,
    0x02, 0x00, 0x00, 0x01,
])


def project_files() -> list[pathlib.Path]:
    files = []
    for line in PROJ.read_text(errors="replace").splitlines():
        if "FILE" not in line.upper():
            continue
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        raw = parts[-1]
        # A `*` before the path drops the file from the assembly. BANK8 is the
        # overflow dummy and is marked that way.
        if raw.startswith("*"):
            continue
        name = raw.replace("\\", "/").split("/")[-1]
        path = SRC / name
        if not path.is_file():
            print(f"missing {name}", file=sys.stderr)
            continue
        files.append(path)
    return files


def place(segments: list[tuple[int, list[tuple[int, int]]]]) -> bytearray:
    rom = bytearray(64 * 1024)
    for bank, blob in segments:
        for addr, byte in blob:
            if 0xC000 <= addr <= 0xFFFF:
                rom[addr] = byte  # fixed bank is the top of the 64 KiB image
            elif 0x8000 <= addr <= 0xBFFF:
                rom[(bank & 3) * 0x4000 + (addr - 0x8000)] = byte
    return rom


def main() -> int:
    files = project_files()
    print(f"assembling {len(files)} files")
    prg = bytearray(0x20000)
    asm = pds6502.Assembler(prg, SRC, [SRC])
    which = asm.setup_path.name if asm.setup_path else "6502 manual default"
    print(f"byte selectors: option 0,{asm.selector_swap_default} ({which})")
    asm.prescan(files)
    asm.collect_macros(files)
    print(f"macros: {len(asm.macros)}")
    asm.run_all(files, [None] * len(files))

    segments = asm.bank_segments
    print(f"bank segments: {len(segments)}")
    for number, blob in segments:
        if not blob:
            print(f"  bank {number}: empty")
            continue
        lo = min(a for a, _ in blob)
        hi = max(a for a, _ in blob)
        print(f"  bank {number}: {len(blob)} bytes  ${lo:04X}-${hi:04X}")

    rom = place(segments)
    OUT.mkdir(exist_ok=True)
    (OUT / "srh.prg.bin").write_bytes(rom)
    (OUT / "srh.sym").write_text(
        "\n".join(f"{k} = ${v:04X}" for k, v in sorted(asm.sym.items())) + "\n")
    nes = ROOT / "srh-rebuilt.nes"
    nes.write_bytes(INES_HEADER + rom)
    print(f"wrote {nes} ({nes.stat().st_size} bytes), symbols {len(asm.sym)}")

    if RETAIL.is_file():
        retail = RETAIL.read_bytes()[16:16 + 65536]
        same = sum(a == b for a, b in zip(rom, retail))
        print(f"match vs Asia cart: {same}/{len(rom)} ({100 * same / len(rom):.2f}%)")
        for i in range(4):
            a = rom[i * 0x4000:(i + 1) * 0x4000]
            b = retail[i * 0x4000:(i + 1) * 0x4000]
            n = sum(x == y for x, y in zip(a, b))
            print(f"  16 KiB bank {i}: {n}/16384 ({100 * n / 16384:.2f}%)")
    if asm.unresolved:
        print(f"unresolved: {len(asm.unresolved)}")
        for name, where in list(asm.unresolved.items())[:30]:
            print(f"  {name} @ {where}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
