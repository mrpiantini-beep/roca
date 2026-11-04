import re,json,sys
path=sys.argv[1]
s=open(path,encoding='utf-8').read()
if 'roca-mobile-fix' in s: sys.exit('ya aplicado')
m=re.search(r'(<script type="__bundler/template">)(.*?)(</script>)',s,re.S)
raw=m.group(2)
css='''<style id="roca-mobile-fix">
@media (max-width: 900px){
  [style*="max-width: min("],[style*="max-width:min("]{max-width:100% !important}
  header nav{flex:0 0 44px !important;order:5;width:44px;height:40px;overflow:visible !important;cursor:pointer;
    border:1px solid rgba(255,255,255,.4);align-items:center;justify-content:center;
    background:linear-gradient(#fff,#fff) center calc(50% - 6px)/18px 2px no-repeat,
               linear-gradient(#fff,#fff) center/18px 2px no-repeat,
               linear-gradient(#fff,#fff) center calc(50% + 6px)/18px 2px no-repeat}
  header nav > div{display:none !important}
  html.roca-menu header nav{background:linear-gradient(45deg,transparent 45%,#fff 45%,#fff 55%,transparent 55%) center/18px 18px no-repeat,
               linear-gradient(-45deg,transparent 45%,#fff 45%,#fff 55%,transparent 55%) center/18px 18px no-repeat}
  html.roca-menu header nav > div{display:flex !important;flex-direction:column;gap:0 !important;position:absolute;top:100%;left:0;right:0;
    margin:0 !important;padding:8px 20px 20px;background:#07080B;border-top:1px solid rgba(255,255,255,.08);
    font-size:13px !important;white-space:normal !important;z-index:30;box-shadow:0 20px 40px rgba(0,0,0,.5)}
  html.roca-menu header nav > div > a{padding:14px 0 !important;border-bottom:1px solid rgba(255,255,255,.08) !important}
  header nav + button{margin-left:auto !important}
}
@media (max-width: 600px){
  header nav + button{font-size:0 !important;padding:13px 14px !important;gap:0 !important}
  header nav + button + a{padding:12px 14px !important}
}
</style>'''
js='''<script id="roca-mobile-menu">
(function(){
  function onClick(e){
    var h=document.documentElement, nav=e.target.closest&&e.target.closest('header nav');
    if(!nav){h.classList.remove('roca-menu');return;}
    if(window.innerWidth>900)return;
    if(e.target.closest('a')){h.classList.remove('roca-menu');return;}
    e.preventDefault();h.classList.toggle('roca-menu');
  }
  function bind(){
    var h=document.documentElement;
    if(h&&h.getAttribute('data-roca-menu')!=='1'){
      h.setAttribute('data-roca-menu','1');
      document.addEventListener('click',onClick);
    }
  }
  bind();setInterval(bind,500);
  window.addEventListener('resize',function(){if(window.innerWidth>900)document.documentElement.classList.remove('roca-menu');});
})();
</script>'''
def enc(x): return json.dumps(x,ensure_ascii=False)[1:-1].replace('</','<\\u002F')
head='<\\u002Fhead>'; body='<\\u002Fbody>'
assert raw.count(head)>=1 and raw.count(body)>=1, (raw.count(head),raw.count(body))
i=raw.find(head); raw=raw[:i]+enc(css)+enc(js)+raw[i:]
pass
json.loads(raw)
s=s[:m.start(2)]+raw+s[m.end(2):]
open(path,'w',encoding='utf-8').write(s); print('ok')
