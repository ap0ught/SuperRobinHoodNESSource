# Assembler changes after the Magician port

Baseline is `asm/pds6502.py` as committed in `f0d6cb6` (the Magician PDS assembler, already adapted enough to read SRH files). The notes below are the later changes, and why each one exists. Magician's measured dialect was left alone wherever SRH did not contradict it.

## Byte selectors follow option 0

Magician's `option 0,0` means `<` is the low byte and `>` is the high byte. The PDS 6502 manual default is the other way: the arrow points at the byte, so `>$1234` is `$34` and `<$1234` is `$12`. That default is assembler option 0 set to 1 (editor manual 9.2.3, "Swap < and >").

The direction is not hardcoded. `option 0,n` in the source sets it, and `pds_src/src/SETUP.PDS` is read first. `ROBIN.PRJ` is only the file list. The original binary SETUP.PDS is not in the dump; the text file is the one switch the Asia cartridge requires, which is 1. SRH's `times16lo` table is the low bytes of `n*16` under that setting. `move.val` and `ldxy` then store low-then-high and X=low, Y=high.

## `&` is both hex and AND

SRH writes `&8000` for hex and `(@1&32)` for bitwise AND. The lexer treated every `&` as a hex prefix, so an infix AND never parsed. A prefix now happens only when the previous token is an operator or the start of the expression. After a value, `&` is AND.

## `~` is XOR, and `EQU` is equality

`(@1&64~64)` is XOR, same precedence as `^`. `if uuu EQU$100` and `until mwn EQU 1` use `EQU` as `=`. Both show up in the macros and in the conditions, so the expressions were not evaluating.

## `equ`, `if`, and `until` take the rest of the line

`equ` was a one-operand directive, so `dungeonschrs equ * - mapchrsdefs` split on the spaces and the assembler tried to execute `-`. `if showcoins = 1` has the same shape. Those three keywords now consume the remainder of the line.

## Commas can sit on either token

`defb 7,%00000000,     >cmdata0` puts the comma on the previous token, then spaces. The old scanner only continued a list when the next token started with a comma, so the high and low pointer bytes were parsed as new instructions. `defb`, `defw`, and `cbm` are comma lists, same as `db` and `dw`.

## `do`/`loop` and `do`/`until` repeat

They were no-ops. PDS repeats a `do count ... loop` body `count` times, and `do ... until cond` is a post-test loop. The count is evaluated once. Macros go through `process` now, because `move` and the other macros contain those repeats. `free` prints free space and emits nothing. `END` stops the assembly, which is what skips `JUNK` after `ENDCODE`.

## `*` comments and editor bytes

A line whose first non-space character is `*` is a comment (`**** gav's bit ****`). `0x01` and `0x02` are editor block markers, and `0x1A` is the CP/M end of file. They are stripped and the text inside the block is assembled. Leaving `0x1A` in made `MACROS.PDS` fail with an unknown instruction.

## `bank` downloads the previous code

On PDS, `bank N` sends everything assembled since the previous `bank` (or the start) to bank N, then the location counter's output resets and the symbol table stays. The Magician assembler only stored `N` in a slot number and kept writing into one flat buffer.

The last pass of `run_all` records `(address, byte)` pairs. `bank` closes that list. `asm/build_srh.py` places them: `$8000-$BFFF` goes to 16 KiB bank `N & 3` (the game writes 12, 13, and 14; mapper 71 uses the low two bits), and `$C000-$FFFF` is the fixed bank at the top of the 64 KiB image. A branch fixup stores the list it was emitted into, because `bank` moves that list out of the open segment before the branch is resolved.

Each assembly attempt rewinds to a checkpoint. Without that, a discarded pass left its bytes in the download and the next pass appended another copy.

## Counters are restored between passes

`run_file` reassembles a file until symbols settle. `varlim = varlim+n` is a redefinable counter. The second attempt used to continue from the first attempt's final value, so `var` ran twice and overflowed (`GLISS_RATE3`). Counters that existed on entry to the file are put back at the start of every attempt after the first.

## `cbm` is C64 screen code

`cbm` was an alias of `db`, so quoted text was ASCII. The PDS manual's example is `CBM "CAT"` producing `3, 1, $14`. The high score font is at those screen codes: `A` is tile 1, `F` is tile 6, `^` is `$1E`, and space through `?` stay as they are. ASCII `F` (`$46`) drew the wrong tile, which is why the names and the credits were garbage. Numeric operands in a `cbm` line are unchanged.

## What was tried and not kept

Forcing any expression (`address7+1`) to absolute addressing made one `STA` match the cart and moved the reset vector onto `$C284`. It also turned cart zero-page stores into absolute ones (`sta address7+1` is `$85 $2A` on the cart) and dropped the bank 1 match, including `PLAY_MUSIC` landing one byte off. Zero page is still chosen when the value is below `$100`.
