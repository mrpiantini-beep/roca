# Foto del panel de perfil en formato 4:5 centrada. Uso: 3_patch_perfil.py <dir_sitio>
import sys,os
p=os.path.join(sys.argv[1],'index.html'); s=open(p,encoding='utf-8').read()
old='<div style="position:relative;aspect-ratio:4/3;flex:none;background:#DDD8CE"><image-slot id="{{ pf.img }}" placeholder="{{ pf.ph }}" style="width:100%;height:100%"></image-slot>'
new='<div style="position:relative;flex:none;background:#DDD8CE;display:flex;justify-content:center;padding:28px 0 0"><div style="width:min(340px,72%);aspect-ratio:4/5;flex:none;box-shadow:0 18px 40px rgba(20,24,31,0.18)"><image-slot id="{{ pf.img }}" placeholder="{{ pf.ph }}" style="width:100%;height:100%"></image-slot></div>'
if new in s: sys.exit('ya aplicado')
assert s.count(old)==1, 'no se encontró el marcado del perfil'
open(p,'w',encoding='utf-8').write(s.replace(old,new)); print('perfil ok')
