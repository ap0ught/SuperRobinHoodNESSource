# What still differs from the Asia cart

Compared `srh-rebuilt.nes` with `vendor/Super Robin Hood (Asia) (En) (Unl).nes` after the music span. The 40% same-offset score is the shifts below: once a byte is inserted or removed, every later byte is scored at the wrong address. Nothing here was edited. Any of it can be left as it is.

## Palette bytes in the map bank

Bank 0 matches apart from 39 bytes, from `gamepallettes` at `$861E` through `showlivescolours`. The source writes `&0e`. The cart stored `$0D`. Both are black. The rest of that 16 KiB bank is the same bytes.

## Zero page where the cart used absolute

An address under `$100` is encoded as zero page, including `sta address7+1`. The cart encodes some of those as absolute, one byte longer. That is the one-byte shift already measured (reset vector `$C283` here, `$C284` on the cart). Forcing those expressions to absolute matched one store and broke the ones the cart really did encode as zero page, so it stayed out.

## `add16toval` of a negative value

`add16toval` takes a short form when `@2<256`:

```
bcc !1
inc high
```

Otherwise it adds the high byte with `adc`. `-sizeofmessage` is `-17`. That is less than 256 as a signed number, so the short form is what we emit. PDS keeps the addend in 16 bits, `$FFEF`, and `$FFEF` is not below 256, so the cart adds the high byte:

```
lda address+1
adc #$FF
sta address+1
```

The only live site is `lidy` in `HISCORE.ROU` (`add16toval address,-sizeofmessage,address`). The bytes agree through `adc #$EF` / `sta address`, then diverge at `$97A0`. The cart's `ovhi2` is two bytes later, so `enbl2`'s `jmp ovhi2` is `$97A7` here and `$97A9` on the cart. The other negative call, `robinxl,-8` in `CONTROL.ROU`, sits under `if testpause=1`, and `testpause` is 0, so it is not in either ROM.

## One `flybackvar` branches to the caller's label

`!` labels belong to the most recent global name. `flybackvar` is:

```
asl flyflag
!1	bit flyflag
	bpl !1
```

`lookingathiscores` calls it and then has its own `!1`. Both are the same symbol, and the later one is the one the branch uses. Our `bpl` at `$9876` is `+11`, which lands on that `ldx #&0d`. The cart's byte is `$FC`, back four bytes onto `bit flyflag`, which is the wait the macro is written as.

The macro is copied twelve times. The other eleven branches are `$FC` in both ROMs. Those globals do not define `!1` again after the call.

## Reset does not run the Taiwan lock

`START.ROU` still has the lock-chip loop: write `$FFF0` / `$FFF1`, burn time in `LOCK2`/`LOCK3`, then thirty `nop`s, then `smiley` and `cm_logo`. That is what we assemble. `start` is `$C283`.

The cart's reset, at `$C284`, is shorter. It clears the PPU and `$4015`, zeroes `cm_flags` (`$07FE`) and `cm_powerup` (`$07FF`), selects bank 12, and jumps through `$C004` into `pastnops`. The lock bytes are still in the cart just after that jump, so they are leftover, not on the reset path. Where we have the thirty `nop`s (`pastlock` at `$C2CC`), the cart copies twenty bytes to `$0600` and jumps there. Those bytes begin `lda #$18` / `sta $9000` / `jmp $FB50`. From `pastnops` onward the two agree again: save `cm_powerup`, call the logo, switch back to bank 12.

## The logo startup is the older copy in the source

Live `CM_LOGO` puts `$97` in Y, checks power-up, downloads characters, then clears zero page and `$0300`. The cart does the clear first, then `ldx #$97` and `cpx`/`stx` the power-up flag, which is the commented-out `CM_LOGO` at the top of `CMLOGO.ROU`. Same first eight bytes (`ldx #0` / `stx $2000` / `stx $2001`), then a different order. That is the source we have, not the assembler.
