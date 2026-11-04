import re,json,base64,gzip,sys,os
src,outdir=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def blk(t): return re.search(r'<script type="__bundler/%s">(.*?)</script>'%t,s,re.S).group(1)
man=json.loads(blk('manifest')); ext=json.loads(blk('ext_resources')); t=json.loads(blk('template'))
EXT={'font/woff2':'woff2','image/png':'png','image/jpeg':'jpg','image/webp':'webp','application/javascript':'js','text/javascript':'js','image/svg+xml':'svg','text/css':'css'}
os.makedirs(os.path.join(outdir,'assets'),exist_ok=True)
path={}
for u,v in man.items():
    b=base64.b64decode(v['data']); b=gzip.decompress(b) if v.get('compressed') else b
    name='assets/%s.%s'%(u,EXT[v['mime']]); path[u]=name
    open(os.path.join(outdir,name),'wb').write(b)
for u,p in path.items(): t=t.replace(u,p)
t=re.sub(r'\s+integrity="[^"]*"','',t); t=re.sub(r'\s+crossorigin="[^"]*"','',t)
res={e['id']:path[e['uuid']] for e in ext}
# fuentes latin para precarga
pre=[]
for m in re.finditer(r'/\* latin \*/\s*@font-face\s*\{[^}]*?src:\s*url\("([^"]+)"',t): pre.append(m.group(1))
preload=''.join('<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>\n'%p for p in dict.fromkeys(pre))
favicon='<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 100 100%27%3E%3Crect width=%27100%27 height=%27100%27 fill=%27%23C60000%27/%3E%3Crect x=%2730%27 y=%2730%27 width=%2740%27 height=%2740%27 fill=%27%23fff%27/%3E%3Ctext x=%2750%27 y=%2758%27 font-family=%27Georgia,serif%27 font-weight=%27700%27 font-size=%2722%27 fill=%27%23C60000%27 text-anchor=%27middle%27%3ER%3C/text%3E%3C/svg%3E">\n'
boot='''<title>JJ Roca &amp; Asociados</title>
<meta name="description" content="JJ Roca &amp; Asociados. Firma de abogados en República Dominicana, miembro exclusivo de Globalaw. Desde 1998.">
<meta name="theme-color" content="#07080B">
%s%s<style id="roca-boot">
html,body{background:#07080B;margin:0}
x-dc{display:none!important}
html.roca-loading body{visibility:hidden}
</style>
<script>
window.__resources=%s;
document.documentElement.classList.add('roca-loading');
(function(){
  var t0=Date.now();
  function show(){document.documentElement.classList.remove('roca-loading');}
  function check(){
    var root=document.getElementById('dc-root');
    if(root&&root.querySelector('header')){
      var f=document.fonts&&document.fonts.ready;
      (f?Promise.race([f,new Promise(function(r){setTimeout(r,1500)})]):Promise.resolve()).then(function(){requestAnimationFrame(show)});
      return;
    }
    if(Date.now()-t0>6000)return show();
    setTimeout(check,30);
  }
  check();
})();
</script>
'''%(favicon,preload,json.dumps(res))
i=t.find('<meta name="viewport"'); i=t.find('>',i)+1
t=t[:i]+'\n'+boot+t[i:]
t=t.replace('<html>','<html lang="es">',1)
open(os.path.join(outdir,'index.html'),'w',encoding='utf-8').write(t)
print('index.html',len(t),'assets',len(path),'preload',len(set(pre)))
