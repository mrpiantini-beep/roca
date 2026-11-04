# Agrega la cuadrícula de Instagram en Recursos · Multimedia. Uso: patch_ig.py <dir_sitio>
import sys,os,glob
d=sys.argv[1]; p=os.path.join(d,'index.html'); s=open(p,encoding='utf-8').read()
if 'data-screen-label="Recursos · Instagram"' in s: sys.exit('ya aplicado')
IG='https://www.instagram.com/jjrocaasociados/'
# 1) Marcado: bloque nuevo al final de la sección Multimedia
anchor='''          </article>
        </sc-for>
      </div>
    </div>
  </section>
  <section data-screen-label="Recursos · Alertas"'''
assert s.count(anchor)==1
icon='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"></rect><circle cx="12" cy="12" r="4"></circle><circle cx="17.5" cy="6.5" r="1" fill="currentColor"></circle></svg>'
block='''          </article>
        </sc-for>
      </div>
      <div data-screen-label="Recursos · Instagram" style="display:flex;flex-direction:column;gap:28px;padding:clamp(48px,6vw,88px) 0 clamp(64px,8vw,110px)">
        <div style="display:flex;justify-content:space-between;align-items:end;gap:16px;flex-wrap:wrap;border-top:2px solid #14181F;padding-top:28px">
          <div style="display:flex;flex-direction:column;gap:10px">
            <span style="font-family:var(--roca-mono);font-size:11px;letter-spacing:0.2em;text-transform:uppercase;color:#C60000">Instagram</span>
            <h3 style="margin:0;font-family:var(--roca-serif);font-weight:800;font-size:clamp(30px,3.2vw,48px);line-height:1">Últimas publicaciones</h3>
          </div>
          <a href="IGURL" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;background:#14181F;color:#fff;padding:14px 22px;font-size:11px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase" style-hover="background:#C60000">ICON<span>@jjrocaasociados</span></a>
        </div>
        <sc-if value="{{ igHay }}" hint-placeholder-val="{{ true }}">
          <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(4px,1.2vw,18px)">
            <sc-for list="{{ igPosts }}" as="p" hint-placeholder-count="9">
              <a href="{{ p.url }}" target="_blank" rel="noopener" title="{{ p.alt }}" style="position:relative;display:block;aspect-ratio:1/1;overflow:hidden;background:#ECE6DA" style-hover="opacity:0.86">
                <img src="{{ p.img }}" alt="{{ p.alt }}" loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center">
                <sc-if value="{{ p.video }}" hint-placeholder-val="{{ false }}"><span style="position:absolute;right:10px;top:10px;width:0;height:0;border-top:8px solid transparent;border-bottom:8px solid transparent;border-left:13px solid #fff;filter:drop-shadow(0 1px 3px rgba(0,0,0,0.6))"></span></sc-if>
              </a>
            </sc-for>
          </div>
        </sc-if>
        <sc-if value="{{ igNo }}" hint-placeholder-val="{{ false }}">
          <a href="IGURL" target="_blank" rel="noopener" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;text-align:center;padding:clamp(40px,6vw,80px) 24px;background:#F4F1EB;border:1px solid #E2DDD3;color:#14181F" style-hover="border-color:#C60000">
            <span style="color:#C60000">ICON</span>
            <span style="font-family:var(--roca-serif);font-weight:800;font-size:clamp(22px,2.2vw,30px)">Síganos en Instagram</span>
            <span style="font-size:14px;color:#5B616B">Novedades, eventos y publicaciones de la Firma en @jjrocaasociados</span>
          </a>
        </sc-if>
      </div>
    </div>
  </section>
  <section data-screen-label="Recursos · Alertas"'''.replace('IGURL',IG).replace('ICON',icon)
s=s.replace(anchor,block)
# el bloque Multimedia tenía padding-bottom 0: el nuevo bloque aporta el espacio inferior
# 2) Lógica: cargar ig.json al montar
cdm='  componentDidMount() { '
assert s.count(cdm)==1
s=s.replace(cdm,cdm+"fetch('ig/ig.json', { cache: 'no-cache' }).then(r => r.ok ? r.json() : []).then(j => { if (Array.isArray(j)) this.setState({ ig: j.slice(0, 12), igOk: true }); }).catch(() => this.setState({ igOk: true })); ",1)
ret='''    return {
      setES:'''
assert s.count(ret)==1
s=s.replace(ret,'''    return {
      igPosts: (this.state.ig || []).map(p => ({ url: p.url, img: p.img, alt: p.alt || 'Publicación de Instagram de JJ Roca & Asociados', video: !!p.video })),
      igHay: !!(this.state.ig && this.state.ig.length), igNo: !!this.state.igOk && !(this.state.ig && this.state.ig.length),
      setES:''')
open(p,'w',encoding='utf-8').write(s)
# 3) Traducciones EN
for f in glob.glob(os.path.join(d,'assets','*.js')):
    t=open(f,encoding='utf-8').read()
    if "'MIEMBRO EXCLUSIVO DE GLOBALAW · REPÚBLICA DOMINICANA':" in t and 'var D = {' in t:
        add="  var D = {\n    'Últimas publicaciones': 'Latest posts', 'Síganos en Instagram': 'Follow us on Instagram',\n    'Novedades, eventos y publicaciones de la Firma en @jjrocaasociados': 'News, events and posts from the Firm at @jjrocaasociados',\n    'Publicación de Instagram de JJ Roca & Asociados': 'Instagram post by JJ Roca & Asociados',\n"
        open(f,'w',encoding='utf-8').write(t.replace('  var D = {\n',add,1)); print('i18n',os.path.basename(f))
print('ok')
