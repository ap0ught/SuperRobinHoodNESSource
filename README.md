# The Super Robin Hood Info Powerhouse

## What is the purpose of this repo?
This repo is the place where you will find things like the official source code, the ported 6502 version (very heavily a WIP), RAM Maps, actual maps, documentation and PDS assemblers for Super Robin Hood for the NES all in one place.
When opening the RAM Map be sure to view it in raw mode as it doesn't render the best when viewing it regularly :)

## Download the rebuilt ROM

**[Download `srh-rebuilt.nes` from Releases](https://github.com/ap0ught/SuperRobinHoodNESSource/releases/latest)** — assembled from the PDS sources in this repo (mapper 71, 64 KiB PRG + CHR-RAM). Prefer the release asset over any copy checked into the tree.

## Build the ROM from source

Needs Python 3 and the shared assembler from [ap0ught/pds6502](https://github.com/ap0ught/pds6502):

```bash
# clone pds6502 next to this repo, or set PDS6502_HOME
git clone https://github.com/ap0ught/pds6502.git ../pds6502
python3 asm/build_srh.py   # writes ./srh-rebuilt.nes
```

If a retail Asia dump named `Super Robin Hood (Asia) (En) (Unl).nes` is present in the repo root, the script also prints byte-match stats; that dump is **not** required to build.

CI publishes the same artifact on tag push (`v*` / `rom-v*`) or via **Actions → Release rebuilt ROM → Run workflow**. See [`.github/workflows/release-rom.yml`](.github/workflows/release-rom.yml).

## A quickstart to get to wherever you want to go:
* [The official Super Robin Hood Source Code (written in PDS)](https://github.com/ap0ught/SuperRobinHoodNESSource/tree/master/pds_src)
* [The rewritten code ported to cc65 assembly](https://github.com/ap0ught/SuperRobinHoodNESSource/tree/master/rewrite)
* [RobinEdit (map/object editor for mapper-71 carts)](https://github.com/ap0ught/robinedit) — split out of `robinedit/` here; see also [`robinedit/MOVED.md`](robinedit/MOVED.md)
* [RobinEdit journals (04–08)](journal/README.md) — port/ROM-layout notes; also in [ap0ught/robinedit `journals/`](https://github.com/ap0ught/robinedit/tree/main/journals)
* [The Super Robin Hood map consisting of all the levels](https://github.com/ap0ught/SuperRobinHoodNESSource/tree/master/docs/content/map.png)
* [Lua scripts!](https://github.com/ap0ught/SuperRobinHoodNESSource/tree/master/docs/content/lua_scripts)
* [A RAM Map detailing what every variable name is, where it resides in memory and - once the rewrite is finished - hopefully descriptions regarding what the variables do as well](https://github.com/ap0ught/SuperRobinHoodNESSource/tree/master/docs/ram_map.wiki)
* [All the manuals and executables for PDS!](https://github.com/ap0ught/SuperRobinHoodNESSource/tree/master/docs/manuals)
