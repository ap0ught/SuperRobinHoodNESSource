import sys, pathlib
sys.path.insert(0,'asm')
import pds6502
src=pathlib.Path('/tmp/srhclean')
proj=pathlib.Path('/home/cmayfield/code/games/SuperRobinHoodNESSource/pds_src/src/ROBIN.PRJ')
order=[]
for line in proj.read_text(errors='replace').splitlines():
    if 'FILE' in line.upper():
        parts=line.strip().split()
        if len(parts)>=2:
            order.append(parts[-1].split('\\')[-1])
files=[]
for n in order:
    p=src/n
    if p.exists() and (p.suffix.lower() in ('.pds','.rou','.mus') or n in ('SPRITESD.DAT','MAPDATA.DAT')):
        files.append(p)
prg=bytearray(0x20000)
asm=pds6502.Assembler(prg, src, [src])
asm.prescan(files)
asm.collect_macros(files)
asm.run_all(files, [None]*len(files))
# dump
out=pathlib.Path('/tmp/srhbuild/out')
out.mkdir(exist_ok=True)
(out/'prg.bin').write_bytes(prg)
print('PRG size:', len(prg))
print('non-zero bytes:', sum(1 for b in prg if b!=0))
# symbols
(out/'srh.sym').write_text('\n'.join(f'{k} = ${v:04X}' for k,v in sorted(asm.sym.items())))
print('symbols:', len(asm.sym))
