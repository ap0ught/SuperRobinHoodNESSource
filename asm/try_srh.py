import sys, pathlib
sys.path.insert(0, 'asm')
import pds6502

src=pathlib.Path('/tmp/srhclean')
proj=pathlib.Path('/home/cmayfield/code/games/SuperRobinHoodNESSource/pds_src/src/ROBIN.PRJ')
order=[]
for line in proj.read_text(errors='replace').splitlines():
    if 'FILE' in line.upper():
        parts=line.strip().split()
        if len(parts)>=2:
            name=parts[-1].split('\\')[-1]
            order.append(name)

files=[]
for name in order:
    p=src/name
    if p.exists() and (p.suffix.lower() in ('.pds','.rou','.mus') or name in ('SPRITESD.DAT','MAPDATA.DAT')):
        files.append(p)
print('text files in order:', len(files))
for f in files: print(' ', f.name)

prg=bytearray(0x20000)
asm=pds6502.Assembler(prg, src, [src])
asm.collect_macros(files)
try:
    asm.prescan(files)
except Exception as e:
    print('prescan err', type(e).__name__, str(e)[:200])
slots=[None]*len(files)
try:
    asm.run_all(files, slots)
    print('run_all OK')
except Exception as e:
    print('run_all ERR:', type(e).__name__, str(e)[:500])
print('report entries:', len(asm.report))
for r in asm.report[:20]:
    print('  ', r)
