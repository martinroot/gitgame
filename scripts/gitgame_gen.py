#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Showcase generator for gitgame.live — catalog with prices (stars → price).
Multilanguage: EN (default) / DE / KR / RU / AR (RTL), client-side i18n.
Cards: size, stack, AI brand, Play + Buy buttons."""
import json, os, html, hashlib, re

CAT = '/var/www/fapa.io/dsgame/catalog/catalog.json'
RATINGS = '/var/www/fapa.io/dsgame/catalog/ratings.json'
OUT = '/var/www/gitgame.live'
CONTACT = 'https://t.me/martinroot'   # TODO: confirm contact details for purchases
PLAY_BASE = 'https://fapa.io/dsgame/catalog/'

BASE = {5: 1.50, 4: 1.00, 3: 0.70, 2: 0.30, 1: 0.10}
SKIP_TAG = {'MIT', 'AI', 'demo', 'как есть', 'нет лиц.', 'CN', 'тач',
            '⚠ нужен сервер', '⚠ проверить', '⭐0', '⭐1', '⭐2', '⭐3', '⭐5'}
# genre → canonical key (for i18n)
GENRE_MAP = {
    'FPS': 'shooter', 'Шутер': 'shooter', 'MOBA': 'action', '5v5': 'action', 'GTA-like': 'action',
    'Гонки-баттл': 'racing',
    'Головоломка': 'puzzle', 'Стратегия': 'strategy', 'Ферма': 'farm',
    'Спорт': 'sport', 'Аркада': 'arcade', 'Билдер': 'builder', 'Раннер': 'runner',
    'Рыбалка': 'fishing', 'Казуальная': 'casual', 'Менеджмент': 'management',
    'Тайкун': 'tycoon', 'Открытый мир': 'openworld',
    '3D': '3d', 'Three.js': '3d', 'three': '3d', 'webgl': '3d', 'Voxel': '3d',
    '@babylonjs/core': '3d',
    'Canvas2D': '2d', 'Canvas': '2d', 'phaser': '2d', 'pixi.js': '2d',
}
# AI brand based on a mention in title/desc/source
AI_BRANDS = [('astra', 'Astra'), ('gpt', 'GPT'), ('claude', 'Claude'),
             ('gemini', 'Gemini'), ('grok', 'Grok'), ('deepseek', 'DeepSeek')]
TECH = {'three', 'Three.js', 'phaser', 'pixi.js', 'webgl', 'Canvas', 'Canvas2D',
        '@babylonjs/core', 'Voxel'}

def stack_of(tags, blob=''):
    for t in tags:
        if t in TECH:
            return t
    # fallback: 3D/2D tag → renderer name, otherwise look for the engine in title+desc
    if '3D' in tags:
        return '3D'
    if 'Canvas2D' in tags or 'Canvas' in tags:
        return 'Canvas2D'
    b=blob.lower()
    for pat, lab in [('three.js','Three.js'),('three','Three.js'),('babylon','Babylon.js'),
                     ('phaser','Phaser'),('pixi','PixiJS'),('webgl','WebGL'),
                     ('canvas2d','Canvas2D'),('canvas','Canvas2D')]:
        if pat in b:
            return lab
    return ''
    return ''

def h(s):
    return int(hashlib.sha256(s.encode()).hexdigest(), 16)

def stars_for(slug, tags, ratings):
    # Real rating from ratings.json (manual scores in the catalog admin)
    # ⭐0/⭐1 tags — junk_purge markers (review status), NOT a rating
    if slug in ratings:
        return int(ratings[slug])
    return 2   # unrated games — default 2★ ($0.30)

def price_for(slug, st):
    base = BASE[st]
    jitter = (h('price' + slug) % 7) - 3   # -3..+3
    p = round((base + jitter * 0.05) * 20) / 20
    return max(p, base)   # never below the base price

def esc(s):
    return html.escape(str(s), quote=True)

def genre_of(tags):
    for t in tags:
        if t in GENRE_MAP: return GENRE_MAP[t]
    return 'other'

def ai_of(g):
    blob = (g.get('title', '') + ' ' + g.get('desc', '') + ' ' + g.get('source', '')).lower()
    for pat, brand in AI_BRANDS:
        if pat in blob:
            return brand
    return ''

def stars_html(st):
    return '★' * st + '☆' * (5 - st)

def load():
    games = json.load(open(CAT))
    ratings = json.load(open(RATINGS)) if os.path.exists(RATINGS) else {}
    dirs = set(os.listdir('/var/www/fapa.io/dsgame/catalog'))
    out = []
    for g in games:
        slug = g.get('slug', '').strip()
        if not slug: continue
        if slug not in ratings: continue   # no stars — do not show in the catalog
        tags = g.get('tags', []) or []
        st = stars_for(slug, tags, ratings)
        thumb = g.get('thumb', '')
        if not thumb and os.path.exists(os.path.join(OUT, 'thumbs', slug + '.jpg')):
            thumb = 'thumbs/' + slug + '.jpg'   # fallback when catalog metadata loses the path
        has_thumb = os.path.exists(os.path.join(OUT, thumb)) if thumb else False
        out.append({
            'slug': slug,
            'title': g.get('title', slug),
            'desc': g.get('desc', ''),
            'tags': [t for t in tags if t not in SKIP_TAG],
            'genre': genre_of(tags),
            'touch': 'тач' in tags,
            'stars': st,
            'price': price_for(slug, st),
            'thumb': thumb if has_thumb else '',
            'size': g.get('size', ''),
            'date': g.get('date', ''),
            'ai': ai_of(g),
            'stack': stack_of(tags, (g.get('title','')+' '+g.get('desc',''))),
            'play': slug in dirs,
        })
    out.sort(key=lambda x: (-x['stars'], -x['price'], x['title']))
    return out

CSS = """*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0b0e14;--bg2:#12161f;--card:#171c26;--card2:#1d2331;--line:#2a3244;
--txt:#e8edf5;--mut:#8b95a8;--acc:#7c6cff;--acc2:#00e0b8;--gold:#ffc94d;--red:#ff5c7a}
body{background:var(--bg);color:var(--txt);font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;min-height:100vh}
body[dir=rtl]{font-family:'Tahoma','Segoe UI',sans-serif}
a{color:inherit;text-decoration:none}
header{position:sticky;top:0;z-index:50;background:rgba(11,14,20,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.hwrap{max-width:1240px;margin:0 auto;padding:14px 20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.logo{font-weight:800;font-size:22px;letter-spacing:-.5px;display:flex;align-items:center;gap:8px}
.logo b{color:var(--acc)}.logo span{color:var(--acc2)}
.stat{font-size:13px;color:var(--mut);margin-left:auto}
.stat b{color:var(--txt)}
.lang{display:flex;gap:4px}
.lang button{background:var(--card);border:1px solid var(--line);color:var(--mut);border-radius:8px;padding:6px 10px;font-size:12px;font-weight:700;cursor:pointer;transition:.15s}
.lang button:hover{border-color:var(--acc);color:var(--txt)}
.lang button.on{background:var(--acc);border-color:var(--acc);color:#fff}
.filters{max-width:1240px;margin:0 auto;padding:0 20px 14px;display:flex;flex-direction:column;gap:10px}
.frow{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.search{flex:1;min-width:220px;position:relative}
.search input{width:100%;padding:11px 14px 11px 40px;background:var(--card);border:1px solid var(--line);border-radius:12px;color:var(--txt);font-size:15px;outline:none;transition:border .2s}
.search input:focus{border-color:var(--acc)}
body[dir=rtl] .search input{padding:11px 40px 11px 14px}
.search svg{position:absolute;left:12px;top:50%;transform:translateY(-50%);width:18px;height:18px;fill:var(--mut)}
body[dir=rtl] .search svg{left:auto;right:12px}
.chip{padding:7px 14px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--mut);font-size:13px;cursor:pointer;transition:.15s;white-space:nowrap}
.chip:hover{border-color:var(--acc);color:var(--txt)}
.chip.on{background:var(--acc);border-color:var(--acc);color:#fff;font-weight:600}
.chips{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.stars{display:flex;gap:6px;align-items:center}
.stars button{background:var(--card);border:1px solid var(--line);color:var(--gold);border-radius:10px;padding:7px 12px;font-size:14px;cursor:pointer;transition:.15s}
.stars button:hover{border-color:var(--gold)}
.stars button.on{background:var(--gold);border-color:var(--gold);color:#1a1a1a;font-weight:700}
select{background:var(--card);border:1px solid var(--line);color:var(--txt);border-radius:12px;padding:10px 12px;font-size:14px;outline:none;cursor:pointer}
.price-badge{position:absolute;top:10px;right:10px;background:linear-gradient(135deg,var(--acc2),var(--acc));color:#fff;font-weight:800;font-size:14px;padding:5px 12px;border-radius:999px;box-shadow:0 4px 14px rgba(124,108,255,.45)}
body[dir=rtl] .price-badge{right:auto;left:10px}
main{max-width:1240px;margin:0 auto;padding:24px 20px 60px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;transition:.2s;position:relative;display:flex;flex-direction:column}
.card:hover{transform:translateY(-4px);border-color:var(--acc);box-shadow:0 12px 30px rgba(0,0,0,.45)}
.thumb{position:relative;aspect-ratio:16/10;background:linear-gradient(135deg,#1e2740,#141a2b);display:flex;align-items:center;justify-content:center}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.thumb .ph{font-size:34px;font-weight:800;color:var(--acc);opacity:.7}
.star{position:absolute;top:10px;left:10px;background:rgba(11,14,20,.85);color:var(--gold);padding:4px 10px;border-radius:999px;font-size:12.5px;font-weight:700}
body[dir=rtl] .star{left:auto;right:10px}
.aibadge{position:absolute;bottom:10px;left:10px;background:rgba(124,108,255,.92);color:#fff;padding:3px 9px;border-radius:999px;font-size:11px;font-weight:700}
body[dir=rtl] .aibadge{left:auto;right:10px}
.cbody{padding:14px;display:flex;flex-direction:column;gap:8px;flex:1}
.ctitle{font-weight:700;font-size:15.5px;line-height:1.3}
.cdesc{font-size:13px;color:var(--mut);line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.cmeta{display:flex;gap:10px;flex-wrap:wrap;font-size:11.5px;color:var(--mut)}
.cmeta b{color:var(--txt);font-weight:600}
.ctags{display:flex;gap:6px;flex-wrap:wrap}
.ctags span{font-size:11px;padding:3px 8px;border-radius:6px;background:var(--card2);color:var(--mut);border:1px solid var(--line)}
.crow{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:auto}
.cprice{font-weight:800;font-size:17px;color:var(--acc2)}
.cbtns{display:flex;gap:8px}
.cplay{background:var(--card2);border:1px solid var(--line);color:var(--txt);border-radius:9px;padding:8px 14px;font-size:13.5px;font-weight:600;cursor:pointer;transition:.15s}
.cplay:hover{border-color:var(--acc2);color:var(--acc2)}
.cbuy{background:var(--acc);color:#fff;border:none;border-radius:9px;padding:8px 18px;font-size:13.5px;font-weight:700;cursor:pointer;transition:.15s}
.cbuy:hover{background:#8a7dff;box-shadow:0 4px 14px rgba(124,108,255,.5)}
.nothing{grid-column:1/-1;text-align:center;color:var(--mut);padding:60px 0;font-size:16px}
footer{border-top:1px solid var(--line);padding:28px 20px;text-align:center;color:var(--mut);font-size:13px}
.adm{opacity:.45;margin-left:8px;font-size:14px}.adm:hover{opacity:1}
footer b{color:var(--txt)}
@media(max-width:640px){.grid{grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}.hwrap{padding:12px 14px}.filters{padding:0 14px 12px}main{padding:16px 14px 40px}}
/* game page */
.gpage{max-width:900px;margin:0 auto;padding:30px 20px 60px}
.gback{display:inline-block;color:var(--mut);font-size:14px;margin-bottom:18px}
.gback:hover{color:var(--acc)}
.ghead{display:flex;gap:24px;flex-wrap:wrap}
.gthumb{width:380px;max-width:100%;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:var(--card2);position:relative}
.gthumb img{width:100%;display:block}
.gthumb .ph{display:flex;align-items:center;justify-content:center;aspect-ratio:16/10;font-size:44px;font-weight:800;color:var(--acc);opacity:.7}
.ginfo{flex:1;min-width:280px}
.ginfo h1{font-size:26px;margin-bottom:10px}
.gstars{color:var(--gold);font-size:18px;margin-bottom:12px}
.gdesc{color:var(--mut);line-height:1.6;margin-bottom:16px;font-size:15px}
.gmeta{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:16px;font-size:13px;color:var(--mut)}
.gmeta div{background:var(--card2);border:1px solid var(--line);border-radius:10px;padding:8px 14px}
.gmeta b{color:var(--txt);display:block;font-size:14px}
.gtags{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:18px}
.gtags span{font-size:12px;padding:4px 10px;border-radius:7px;background:var(--card2);border:1px solid var(--line);color:var(--mut)}
.gtags span.ai{background:rgba(124,108,255,.15);border-color:var(--acc);color:var(--acc);font-weight:700}
.gprice{font-size:34px;font-weight:800;color:var(--acc2);margin-bottom:14px}
.gbtns{display:flex;gap:12px;flex-wrap:wrap}
.gbuy{display:inline-block;background:var(--acc);color:#fff;padding:13px 34px;border-radius:12px;font-size:16px;font-weight:700;cursor:pointer;border:none;transition:.15s}
.gbuy:hover{background:#8a7dff;box-shadow:0 6px 20px rgba(124,108,255,.5)}
.gplay{display:inline-block;background:var(--card2);border:1px solid var(--line);color:var(--txt);padding:13px 26px;border-radius:12px;font-size:16px;font-weight:600}
.gplay:hover{border-color:var(--acc2)}
.gmeta2{margin-top:18px;font-size:13px;color:var(--mut);line-height:1.8}
.gmeta2 b{color:var(--txt)}
.modal{position:fixed;inset:0;background:rgba(0,0,0,.7);display:none;align-items:center;justify-content:center;z-index:100;padding:20px}
.modal.open{display:flex}
.mbox{background:var(--bg2);border:1px solid var(--line);border-radius:18px;padding:30px;max-width:420px;width:100%;text-align:center}
.mbox h3{font-size:20px;margin-bottom:10px}
.mbox p{color:var(--mut);font-size:14px;line-height:1.6;margin-bottom:18px}
.mbox .btn{display:block;background:var(--acc);color:#fff;padding:12px;border-radius:11px;font-weight:700;margin-bottom:10px}
.mbox .btn.alt{background:var(--card2);border:1px solid var(--line);color:var(--txt)}
.mbox .btn:hover{background:#8a7dff}
"""

CART_JS = '''<script>
(function(){
const KEY='gg_cart';
const read=()=>{try{return JSON.parse(localStorage.getItem(KEY))||[]}catch(e){return[]}};
const save=a=>{localStorage.setItem(KEY,JSON.stringify(a));btn()};
const money=n=>'$'+Number(n).toFixed(2);
function btn(){
  let b=document.getElementById('ggcartbtn');
  if(!b && document.querySelector('.hwrap')){
    b=document.createElement('button');b.id='ggcartbtn';
    b.style.cssText='margin-left:12px;padding:7px 12px;border-radius:9px;border:1px solid var(--line);background:var(--card2);color:var(--txt);cursor:pointer;font-weight:700';
    b.onclick=()=>window.ggOpenCart();
    const lang=document.querySelector('.lang');
    if(lang)lang.before(b);else document.querySelector('.hwrap').appendChild(b);
  }
  if(b)b.textContent='🛒 Cart ('+read().length+')';
}
function shell(){
  let s=document.getElementById('ggcart');
  if(!s){
    s=document.createElement('div');s.id='ggcart';
    s.innerHTML='<div id="ggcm" style="position:fixed;inset:0;background:rgba(0,0,0,.72);display:none;align-items:center;justify-content:center;z-index:200;padding:20px"><div style="background:var(--bg2,#151522);border:1px solid var(--line,#333);border-radius:16px;padding:24px;max-width:560px;width:100%;max-height:88vh;overflow:auto"><h3 style="margin:0 0 12px">🛒 Cart</h3><div id="ggclist"></div><p style="font-size:13px;color:var(--mut,#aaa);margin:12px 0">Email is used to recover your order and download paid sources later.</p><input id="ggcmail" type="email" placeholder="you@example.com" style="width:100%;box-sizing:border-box;padding:11px;border-radius:9px;border:1px solid var(--line,#333);background:var(--card2,#222);color:var(--txt,#fff)"><div style="display:flex;gap:10px;margin-top:14px;flex-wrap:wrap"><button id="ggcpay" style="padding:11px 18px;border:none;border-radius:9px;background:var(--acc,#7c6cff);color:#fff;font-weight:700;cursor:pointer">Pay with crypto</button><button onclick="ggCloseCart()" style="padding:11px 18px;border-radius:9px;border:1px solid var(--line,#333);background:transparent;color:var(--txt,#fff);cursor:pointer">Close</button><a href="/account/" style="padding:11px 6px;color:var(--acc2,#54e0c4)">My orders →</a></div><p id="ggcmmsg" style="font-size:13px;color:#8a7dff;min-height:1em"></p></div></div>';
    document.body.appendChild(s);
    s.querySelector('#ggcm').addEventListener('click',e=>{if(e.target.id==='ggcm')ggCloseCart()});
    s.querySelector('#ggcpay').onclick=pay;
  }
  return s;
}
function render(){
  const a=read(),c=shell();
  c.querySelector('#ggclist').innerHTML=a.length?a.map(x=>
    '<div style="display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid var(--line,#333);font-size:14px"><span>'+x.title.replace(/[<>]/g,'')+'</span><span>'+money(x.price)+' <button data-slug="'+x.slug+'" style="background:none;border:none;color:#ff7b7b;cursor:pointer">✕</button></span></div>').join('')
    +'<p style="margin:12px 0;font-weight:700">Total: '+money(a.reduce((s,x)=>s+x.price,0))+'</p>'
    :'<p style="color:var(--mut,#aaa)">Your cart is empty.</p>';
  c.querySelectorAll('[data-slug]').forEach(b=>b.onclick=()=>{
    save(read().filter(x=>x.slug!==b.dataset.slug));render();
  });
}
window.ggOpenCart=function(){render();shell().querySelector('#ggcm').style.display='flex'};
window.ggCloseCart=function(){shell().querySelector('#ggcm').style.display='none'};
window.ggAdd=function(slug,title,price){
  const a=read();
  if(!a.some(x=>x.slug===slug))a.push({slug,title,price:Number(price)});
  save(a);ggOpenCart();
};
async function pay(){
  const a=read(),m=shell().querySelector('#ggcmmsg'),b=shell().querySelector('#ggcpay');
  if(!a.length){m.textContent='Cart is empty';return}
  const email=shell().querySelector('#ggcmail').value.trim();
  if(!email.includes('@')){m.textContent='Enter a valid email';return}
  b.disabled=true;m.textContent='Creating order…';
  try{
    const r=await fetch('/api/checkout.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({slugs:a.map(x=>x.slug),email})});
    const d=await r.json();
    if(!d.pay_url){m.textContent=d.error||'Error, try later';b.disabled=false;return}
    localStorage.removeItem(KEY);btn();render();
    m.innerHTML='Order <b>'+d.order_id+'</b> · '+money(d.amount)+'<br><a href="'+d.pay_url+'" style="color:#8a7dff;font-weight:700">Continue to payment →</a><br><small>Save this order ID and email — they restore access in My orders.</small>';
  }catch(e){m.textContent='Network error';b.disabled=false}
}
btn();
})();
</script>
'''

ACCOUNT_PAGE = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>My orders — GitGame</title>
<style>
body{margin:0;background:#0e0e14;color:#eee;font:15px/1.5 system-ui,sans-serif;padding:30px;max-width:820px;margin:auto}
h1{font-size:26px}a{color:#8a7dff}label{display:block;margin:12px 0 5px;color:#aaa;font-size:13px}
input{width:100%;box-sizing:border-box;padding:11px;border-radius:9px;border:1px solid #333;background:#1a1a24;color:#fff}
button{margin-top:14px;padding:11px 20px;border:none;border-radius:9px;background:#7c6cff;color:#fff;font-weight:700;cursor:pointer}
.order{border:1px solid #333;border-radius:14px;padding:16px;margin:16px 0;background:#15151f}
.ok{color:#54e0c4}.pending{color:#ffc46b}.dl{display:inline-block;margin:8px 10px 0 0;padding:8px 12px;border-radius:8px;background:#222;color:#8a7dff;text-decoration:none}
</style><script defer src="https://vibemetrics.click/tracker.js" data-site-id="gitgame-live" data-site-key="oGgU9fnoaeKVhaHpVSN4IkDU21Li_bqUuRTPoYVC4fY"></script></head><body>
<p><a href="/">← GitGame catalog</a></p><h1>My orders</h1>
<p>Enter the order ID from checkout and the email used for that order. Your paid games and source downloads stay here — losing the payment tab does not lose the order.</p>
<form id="f"><label for="o">Order ID</label><input id="o" placeholder="gg-xxxxxxxxxxxx" required>
<label for="e">Email</label><input id="e" type="email" placeholder="you@example.com" required>
<button type="submit">Find order</button></form><div id="out"></div>
<script>
const q=new URLSearchParams(location.search);
document.getElementById('o').value=q.get('order')||'';
document.getElementById('e').value=q.get('email')||'';
document.getElementById('f').onsubmit=async ev=>{
  ev.preventDefault();const out=document.getElementById('out');out.textContent='Searching…';
  try{
    const r=await fetch('/api/account.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({order_id:document.getElementById('o').value.trim(),email:document.getElementById('e').value.trim()})});
    const d=await r.json();
    if(!r.ok){out.textContent=d.error||'Order not found';return}
    out.innerHTML='<div class="order"><b>'+d.order_id+'</b> · <span class="'+(d.status==='paid'?'ok':'pending')+'">'+d.status+'</span> · $'+Number(d.amount_usd).toFixed(2)+'<br>'+d.items.map(i=>i.slug+' $'+Number(i.price).toFixed(2)).join('<br>')+(d.downloads?('<br><br><b>Downloads:</b><br>'+d.downloads.map(x=>'<a class="dl" href="'+x.url+'">↓ '+x.slug+'</a>').join('')):('<br><br>Payment not confirmed yet. Reload this page after paying.'))+'</div>';
  }catch(e){out.textContent='Network error'}
};
if(document.getElementById('o').value&&document.getElementById('e').value)document.getElementById('f').requestSubmit();
</script></body></html>
'''

# ---------- i18n ----------
I18N = {
 'en': {
  'title': 'GitGame — HTML5 game catalog with source code',
  'desc': 'A catalog of {n} HTML5 games with ready web builds and sources. Buy from ${min:.2f}.',
  'games': 'games', 'games_in_catalog': 'games in catalog', 'from': 'from',
  'search': 'Search by title or description…',
  'sort_top': 'Top first', 'sort_priceUp': 'Price ↑', 'sort_priceDown': 'Price ↓',
  'sort_name': 'By name', 'sort_new': 'Newest',
  'allstars': 'All ★', 'touch': '📱 Touch', 'allgenres': 'All genres',
  'nothing': 'Nothing found — try another filter',
  'buy': 'Buy', 'play': '▶ Play', 'buy_for': 'Buy for ${p:.2f}',
  'size': 'Size', 'stack': 'Stack', 'added': 'Added', 'ai': 'AI',
  'footer': 'GitGame — HTML5 game marketplace: {n} games with ready web builds and sources. License included.',
  'footer2': 'GitGame — HTML5 game marketplace. License included with every purchase.',
  'back': '← Back to catalog', 'modal_title': 'Checkout',
  'modal_body': '"{t}" — ${p:.2f}<br>Pay with crypto (BTC/ETH/USDT…). Sources and license unlock automatically after payment.',
  'modal_pay': 'Pay with crypto', 'modal_later': 'Later',
  'ratings': 'Rating', 'generated': 'web build',
  'genres': {'other': 'Other', 'shooter': 'Shooter', 'action': 'Action', 'racing': 'Racing',
   'puzzle': 'Puzzle', 'strategy': 'Strategy', 'farm': 'Farm', 'sport': 'Sport',
   'arcade': 'Arcade', 'builder': 'Builder', 'runner': 'Runner', 'fishing': 'Fishing',
   'casual': 'Casual', 'management': 'Management', 'tycoon': 'Tycoon',
   'openworld': 'Open world', '3d': '3D', '2d': '2D'},
 },
 'de': {
  'title': 'GitGame — HTML5-Spielkatalog mit Quellcode',
  'desc': 'Katalog aus {n} HTML5-Spielen mit fertigen Web-Builds und Quellcode. Ab ${min:.2f}.',
  'games': 'Spiele', 'games_in_catalog': 'Spiele im Katalog', 'from': 'ab',
  'search': 'Nach Titel oder Beschreibung suchen…',
  'sort_top': 'Top zuerst', 'sort_priceUp': 'Preis ↑', 'sort_priceDown': 'Preis ↓',
  'sort_name': 'Nach Name', 'sort_new': 'Neueste',
  'allstars': 'Alle ★', 'touch': '📱 Touch', 'allgenres': 'Alle Genres',
  'nothing': 'Nichts gefunden — anderen Filter versuchen',
  'buy': 'Kaufen', 'play': '▶ Spielen', 'buy_for': 'Kaufen für ${p:.2f}',
  'size': 'Größe', 'stack': 'Stack', 'added': 'Hinzugefügt', 'ai': 'KI',
  'footer': 'GitGame — HTML5-Spiel-Marktplatz: {n} Spiele mit fertigen Web-Builds und Quellcode. Lizenz inklusive.',
  'footer2': 'GitGame — HTML5-Spiel-Marktplatz. Lizenz zu jedem Kauf inklusive.',
  'back': '← Zurück zum Katalog', 'modal_title': 'Kasse',
  'modal_body': '"{t}" — ${p:.2f}<br>Bezahlen Sie mit Krypto (BTC/ETH/USDT…). Quellcode und Lizenz werden nach Zahlung automatisch freigeschaltet.',
  'modal_pay': 'Mit Krypto bezahlen', 'modal_later': 'Später',
  'ratings': 'Bewertung', 'generated': 'Web-Build',
  'genres': {'other': 'Sonstige', 'shooter': 'Shooter', 'action': 'Action', 'racing': 'Rennen',
   'puzzle': 'Puzzle', 'strategy': 'Strategie', 'farm': 'Farm', 'sport': 'Sport',
   'arcade': 'Arcade', 'builder': 'Builder', 'runner': 'Runner', 'fishing': 'Angeln',
   'casual': 'Casual', 'management': 'Management', 'tycoon': 'Tycoon',
   'openworld': 'Open World', '3d': '3D', '2d': '2D'},
 },
 'kr': {
  'title': 'GitGame — 소스 코드가 있는 HTML5 게임 카탈로그',
  'desc': '완성된 웹 빌드와 소스 코드를 갖춘 {n}개 HTML5 게임 카탈로그. ${min:.2f}부터.',
  'games': '게임', 'games_in_catalog': '카탈로그 속 게임', 'from': '부터',
  'search': '제목 또는 설명으로 검색…',
  'sort_top': '인기순', 'sort_priceUp': '가격 ↑', 'sort_priceDown': '가격 ↓',
  'sort_name': '이름순', 'sort_new': '최신순',
  'allstars': '전체 ★', 'touch': '📱 터치', 'allgenres': '전체 장르',
  'nothing': '결과가 없습니다 — 다른 필터를 시도해 보세요',
  'buy': '구매', 'play': '▶ 플레이', 'buy_for': '${p:.2f} 구매',
  'size': '크기', 'stack': '스택', 'added': '추가됨', 'ai': 'AI',
  'footer': 'GitGame — HTML5 게임 마켓플레이스: {n}개 게임, 웹 빌드와 소스 코드 포함. 라이선스 제공.',
  'footer2': 'GitGame — HTML5 게임 마켓플레이스. 모든 구매에 라이선스가 포함됩니다.',
  'back': '← 카탈로그로 돌아가기', 'modal_title': '결제',
  'modal_body': '"{t}" — ${p:.2f}<br>크립토(BTC/ETH/USDT…)로 결제하세요. 결제 후 소스 코드와 라이선스가 자동으로 열립니다.',
  'modal_pay': '크립토로 결제', 'modal_later': '나중에',
  'ratings': '평점', 'generated': '웹 빌드',
  'genres': {'other': '기타', 'shooter': '슈팅', 'action': '액션', 'racing': '레이싱',
   'puzzle': '퍼즐', 'strategy': '전략', 'farm': '농장', 'sport': '스포츠',
   'arcade': '아케이드', 'builder': '빌더', 'runner': '러너', 'fishing': '낚시',
   'casual': '캐주얼', 'management': '경영', 'tycoon': '타이쿤',
   'openworld': '오픈월드', '3d': '3D', '2d': '2D'},
 },
 'ru': {
  'title': 'GitGame — каталог HTML5-игр с исходниками',
  'desc': 'Каталог из {n} HTML5-игр с готовой веб-версией и исходниками. Купить от ${min:.2f}.',
  'games': 'игр', 'games_in_catalog': 'игр в каталоге', 'from': 'от',
  'search': 'Поиск по названию или описанию…',
  'sort_top': 'Сначала топ', 'sort_priceUp': 'Цена ↑', 'sort_priceDown': 'Цена ↓',
  'sort_name': 'По имени', 'sort_new': 'Новые',
  'allstars': 'Все ★', 'touch': '📱 Тач', 'allgenres': 'Все жанры',
  'nothing': 'Ничего не найдено — попробуйте другой фильтр',
  'buy': 'Купить', 'play': '▶ Играть', 'buy_for': 'Купить за ${p:.2f}',
  'size': 'Размер', 'stack': 'Стек', 'added': 'Добавлена', 'ai': 'AI',
  'footer': 'GitGame — маркетплейс HTML5-игр: {n} игр с готовой веб-версией и исходниками. Лицензия прилагается.',
  'footer2': 'GitGame — маркетплейс HTML5-игр. Лицензия прилагается к каждой покупке.',
  'back': '← Назад в каталог', 'modal_title': 'Оформление покупки',
  'modal_body': '«{t}» — ${p:.2f}<br>Оплата криптовалютой (BTC/ETH/USDT…). Исходники и лицензия откроются автоматически после оплаты.',
  'modal_pay': 'Оплатить криптовалютой', 'modal_later': 'Позже',
  'ratings': 'Рейтинг', 'generated': 'веб-версия',
  'genres': {'other': 'Прочее', 'shooter': 'Шутер', 'action': 'Экшн', 'racing': 'Гонки',
   'puzzle': 'Головоломка', 'strategy': 'Стратегия', 'farm': 'Ферма', 'sport': 'Спорт',
   'arcade': 'Аркада', 'builder': 'Билдер', 'runner': 'Раннер', 'fishing': 'Рыбалка',
   'casual': 'Казуальная', 'management': 'Менеджмент', 'tycoon': 'Тайкун',
   'openworld': 'Открытый мир', '3d': '3D', '2d': '2D'},
 },
 'ar': {
  'title': 'GitGame — كتالوج ألعاب HTML5 مع الكود المصدري',
  'desc': 'كتالوج من {n} لعبة HTML5 مع نسخ ويب جاهزة وكود مصدري. الشراء من ${min:.2f}.',
  'games': 'لعبة', 'games_in_catalog': 'لعبة في الكتالوج', 'from': 'من',
  'search': 'ابحث بالاسم أو الوصف…',
  'sort_top': 'الأعلى أولاً', 'sort_priceUp': 'السعر ↑', 'sort_priceDown': 'السعر ↓',
  'sort_name': 'بالاسم', 'sort_new': 'الأحدث',
  'allstars': 'الكل ★', 'touch': '📱 لمس', 'allgenres': 'كل الأنواع',
  'nothing': 'لا نتائج — جرّب فلتراً آخر',
  'buy': 'شراء', 'play': '▶ العب', 'buy_for': 'شراء بـ ${p:.2f}',
  'size': 'الحجم', 'stack': 'التقنيات', 'added': 'أُضيفت', 'ai': 'AI',
  'footer': 'GitGame — سوق ألعاب HTML5: {n} لعبة مع نسخ ويب وكود مصدري. الترخيص مرفق.',
  'footer2': 'GitGame — سوق ألعاب HTML5. الترخيص مرفق مع كل عملية شراء.',
  'back': '← العودة إلى الكتالوج', 'modal_title': 'إتمام الشراء',
  'modal_body': '"{t}" — ${p:.2f}<br>ادفع بالعملات الرقمية (BTC/ETH/USDT…). سيتم فتح الكود المصدري والترخيص تلقائياً بعد الدفع.',
  'modal_pay': 'ادفع بالعملات الرقمية', 'modal_later': 'لاحقاً',
  'ratings': 'التقييم', 'generated': 'نسخة ويب',
  'genres': {'other': 'أخرى', 'shooter': 'إطلاق نار', 'action': 'أكشن', 'racing': 'سباق',
   'puzzle': 'ألغاز', 'strategy': 'استراتيجية', 'farm': 'مزرعة', 'sport': 'رياضة',
   'arcade': 'آركيد', 'builder': 'بناء', 'runner': 'عدّاء', 'fishing': 'صيد',
   'casual': 'كاجوال', 'management': 'إدارة', 'tycoon': 'تايكون',
   'openworld': 'عالم مفتوح', '3d': '3D', '2d': '2D'},
 },
}
LANGS = ['en', 'de', 'kr', 'ru', 'ar']
LANG_LABEL = {'en': 'EN', 'de': 'DE', 'kr': 'KR', 'ru': 'RU', 'ar': 'AR'}

# JS i18n runtime: подставляет строки по data-i18n, dir=rtl для AR, жаргонные переводы жанров
JS_I18N = """
const L=%s;
const DIRS={ar:'rtl'};
let cur=localStorage.getItem('gg_lang')||'en';
function applyLang(){
  document.documentElement.lang=cur;
  document.body.dir=DIRS[cur]||'ltr';
  document.querySelectorAll('[data-i18n]').forEach(e=>{e.textContent=L[cur][e.dataset.i18n]||e.textContent});
  document.querySelectorAll('[data-i18n-ph]').forEach(e=>{e.placeholder=L[cur][e.dataset.i18nPh]||e.placeholder});
  document.querySelectorAll('[data-genre]').forEach(e=>{e.textContent=L[cur].genres[e.dataset.genre]||e.dataset.genre});
  document.querySelectorAll('[data-price]').forEach(e=>{e.textContent=L[cur].buy_for.replace('${p:.2f}','$'+e.dataset.price)});
  document.querySelectorAll('.lang button').forEach(b=>b.classList.toggle('on',b.dataset.lang===cur));
}
function setLang(l){cur=l;localStorage.setItem('gg_lang',l);applyLang();if(typeof render==='function')render();}
document.querySelectorAll('.lang button').forEach(b=>b.addEventListener('click',()=>setLang(b.dataset.lang)));
""" % (json.dumps(I18N, ensure_ascii=False))

LANG_BTNS = ''.join(f'<button data-lang="{lg}" class="{"on" if lg=="en" else ""}">{LANG_LABEL[lg]}</button>' for lg in LANGS)

def game_page(g, total):
    thumb = f'<img src="{esc(g["thumb"])}" alt="{esc(g["title"])}" loading="lazy">' if g['thumb'] else f'<div class="ph">{esc(g["title"][:2].upper())}</div>'
    tags = ''.join(f'<span>{esc(t)}</span>' for t in g['tags'])
    ai_badge = f'<span class="ai">🤖 AI: {esc(g["ai"])}</span>' if g['ai'] else ''
    ai_badge_card = f'<div class="aibadge">🤖 AI: {esc(g["ai"])}</div>' if g['ai'] else ''
    play = f'<a class="gplay" href="{PLAY_BASE}{esc(g["slug"])}/" target="_blank" rel="noopener"><span data-i18n="play">Play</span></a>' if g['play'] else ''
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(g["title"])} — buy for ${g["price"]:.2f} | GitGame</title>
<meta name="description" content="{esc(g["desc"][:150])}">
<style>{CSS}</style><script defer src="https://vibemetrics.click/tracker.js" data-site-id="gitgame-live" data-site-key="oGgU9fnoaeKVhaHpVSN4IkDU21Li_bqUuRTPoYVC4fY"></script></head><body>
<header><div class="hwrap"><a class="logo" href="/">🎮 <b>Git</b><span>Game</span></a>
<div class="stat"><b>{total}</b> <span data-i18n="games_in_catalog">games in catalog</span></div>
<div class="lang">{LANG_BTNS}</div></div></header>
<main class="gpage">
<a class="gback" href="/"><span data-i18n="back">← Back to catalog</span></a>
<div class="ghead">
<div class="gthumb">{thumb}</div>
<div class="ginfo">
<h1>{esc(g["title"])}</h1>
<div class="gstars">{stars_html(g["stars"])} <span style="color:var(--mut);font-size:14px">{g["stars"]}/5</span></div>
<p class="gdesc">{esc(g["desc"])}</p>
<div class="gmeta">
<div><span data-i18n="size">Size</span><b>{esc(g["size"])}</b></div>
<div><span data-i18n="stack">Stack</span><b>{esc(g["stack"]) if g["stack"] else "—"}</b></div>
<div><span data-i18n="added">Added</span><b>{esc(g["date"])}</b></div>
</div>
<div class="gtags">{tags}<span data-genre="{esc(g["genre"])}">{esc(g["genre"])}</span>{'<span>📱 Тач</span>' if g["touch"] else ''}{ai_badge}</div>
<div class="gprice">${g["price"]:.2f}</div>
<div class="gbtns">
<button class="gbuy" onclick="openModal()" data-price="{g["price"]:.2f}">Buy for ${g["price"]:.2f}</button>
{play}
</div>
</div></div>
</main>
<footer><b>GitGame</b> — <span data-i18n="footer2">HTML5 game marketplace. License included with every purchase.</span> · <a class="adm" href="/admin/" title="Admin">⚙</a></footer>
<div class="modal" id="m" onclick="if(event.target===this)closeModal()">
<div class="mbox"><h3 data-i18n="modal_title">Checkout</h3>
<p>«{esc(g["title"])}» — ${g["price"]:.2f}<br><span data-i18n="modal_body">Pay with crypto (BTC/ETH/USDT…). Sources and license are unlocked automatically after payment.</span></p>
<button class="btn" id="paybtn" onclick="ggAdd('{esc(g["slug"])}',this.dataset.title,{g["price"]:.2f})" data-title="{esc(g["title"])}">Add to cart</button>
<button class="btn alt" onclick="closeModal()" data-i18n="modal_later">Later</button>
<p id="paymsg" style="color:#8a7dff;font-size:13px;min-height:1em"></p></div></div>
<script>{JS_I18N}
async function pay(slug){{
  const b=document.getElementById('paybtn'),m=document.getElementById('paymsg');
  b.disabled=true; m.textContent='…';
  try{{
    const r=await fetch('/api/checkout.php',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{slug:'{esc(g["slug"])}'}})}});
    const d=await r.json();
    if(d.pay_url){{location.href=d.pay_url}}else{{m.textContent=d.error||'Error, try later';b.disabled=false}}
  }}catch(e){{m.textContent='Network error';b.disabled=false}}
}}
function openModal(){{document.getElementById('m').classList.add('open')}}
function closeModal(){{document.getElementById('m').classList.remove('open')}}
document.addEventListener('keydown',e=>{{if(e.key==='Escape')closeModal()}})
applyLang()
</script>{CART_JS}
</body></html>'''

def main():
    games = load()
    os.makedirs(os.path.join(OUT, 'game'), exist_ok=True)
    total = len(games)
    data = json.dumps(games, ensure_ascii=False)
    genres = sorted({g['genre'] for g in games})
    price_min, price_max = min(g['price'] for g in games), max(g['price'] for g in games)
    idx = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GitGame — HTML5 game catalog with source code</title>
<meta name="description" content="A catalog of {total} HTML5 games with ready web builds and sources. Buy from ${price_min:.2f}.">
<style>{CSS}</style><script defer src="https://vibemetrics.click/tracker.js" data-site-id="gitgame-live" data-site-key="oGgU9fnoaeKVhaHpVSN4IkDU21Li_bqUuRTPoYVC4fY"></script></head><body>
<header><div class="hwrap"><a class="logo" href="/">🎮 <b>Git</b><span>Game</span></a>
<div class="stat"><b>{total}</b> <span data-i18n="games">games</span> · <span data-i18n="from">from</span> ${price_min:.2f}</div>
<div class="lang">{LANG_BTNS}</div></div>
<div class="filters">
<div class="frow">
<div class="search"><svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 1 0-.7.7l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0A4.5 4.5 0 1 1 14 9.5 4.5 4.5 0 0 1 9.5 14z"/></svg>
<input id="q" type="search" placeholder="Search by title or description…" autocomplete="off" data-i18n-ph="search"></div>
<select id="sort">
<option value="top" data-i18n="sort_top">Top first</option>
<option value="priceUp" data-i18n="sort_priceUp">Price ↑</option>
<option value="priceDown" data-i18n="sort_priceDown">Price ↓</option>
<option value="name" data-i18n="sort_name">By name</option>
<option value="new" data-i18n="sort_new">Newest</option>
</select>
<div class="stars" id="stars"><button data-s="0" class="on" data-i18n="allstars">All ★</button><button data-s="5">5★</button><button data-s="4">4★</button><button data-s="3">3★</button><button data-s="2">2★</button></div>
<button class="chip" id="touch" data-i18n="touch">📱 Touch</button>
</div>
<div class="chips" id="chips"><button class="chip on" data-g="all" data-i18n="allgenres">All genres</button>{''.join(f'<button class="chip" data-g="{esc(gn)}" data-genre="{esc(gn)}">{esc(gn)}</button>' for gn in genres)}</div>
</div></header>
<main><div class="grid" id="grid"></div><div class="nothing" id="no" style="display:none" data-i18n="nothing">Nothing found — try another filter</div></main>
<footer><b>GitGame</b> — <span data-i18n="footer">HTML5 game marketplace: {total} games with ready web builds and sources. License included.</span> · <a class="adm" href="/admin/" title="Admin">⚙</a></footer>
<script>{JS_I18N}
const D={data};
const G=document.getElementById('grid');
let flt={{q:'',genre:'all',star:0,touch:false,sort:'top'}};
const esc=s=>s.replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
function card(g){{
const th=g.thumb?`<img src="${{g.thumb}}" alt="${{esc(g.title)}}" loading="lazy">`:`<div class="ph">${{esc(g.title.slice(0,2).toUpperCase())}}</div>`;
const ai=g.ai?`<div class="aibadge">🤖 AI: ${{esc(g.ai)}}</div>`:'';
const size=g.size?`<span>📦 <b>${{esc(g.size)}}</b></span>`:'';
const stack=g.stack?`<span>⚡ <b>${{esc(g.stack)}}</b></span>`:'';
return `<div class="card"><a href="/game/${{g.slug}}/"><div class="thumb">${{th}}<div class="star">${{'★'.repeat(g.stars)}}</div><div class="price-badge">$${{g.price.toFixed(2)}}</div>${{ai}}</div></a>
<div class="cbody"><a href="/game/${{g.slug}}/"><div class="ctitle">${{esc(g.title)}}</div><div class="cdesc">${{esc(g.desc)}}</div></a>
<div class="cmeta">${{size}}${{stack}}${{g.touch?'<span>📱</span>':''}}</div>
<div class="ctags">${{g.tags.map(t=>`<span>${{esc(t)}}</span>`).join('')}}<span data-genre="${{esc(g.genre)}}">${{esc(g.genre)}}</span></div>
<div class="crow"><span class="cprice">$${{g.price.toFixed(2)}}</span><div class="cbtns">
${{g.play?`<button class="cplay" onclick="window.open('{PLAY_BASE}${{g.slug}}/','_blank')"><span data-i18n="play">Play</span></button>`:''}}
<button class="cbuy" onclick="ggAdd('${{g.slug}}',this.dataset.title,${{g.price}})" data-title="${{esc(g.title)}}" data-i18n="buy">Buy</button></div></div></div></div>`}}
function render(){{
let r=D.filter(g=>
(flt.genre==='all'||g.genre===flt.genre)&&
(flt.star===0||g.stars===flt.star)&&
(!flt.touch||g.touch)&&
(!flt.q||(g.title+' '+g.desc+' '+g.tags.join(' ')).toLowerCase().includes(flt.q)));
if(flt.sort==='priceUp')r.sort((a,b)=>a.price-b.price);
else if(flt.sort==='priceDown')r.sort((a,b)=>b.price-a.price);
else if(flt.sort==='name')r.sort((a,b)=>a.title.localeCompare(b.title));
else if(flt.sort==='new')r.sort((a,b)=>b.date.localeCompare(a.date));
G.innerHTML=r.map(card).join('');
document.getElementById('no').style.display=r.length?'none':'block';
applyLang();
}}
document.getElementById('q').addEventListener('input',e=>{{flt.q=e.target.value.toLowerCase();render()}});
document.getElementById('chips').addEventListener('click',e=>{{
if(e.target.dataset.g){{flt.genre=e.target.dataset.g;
document.querySelectorAll('#chips .chip').forEach(b=>b.classList.toggle('on',b===e.target));render()}}}});
document.getElementById('stars').addEventListener('click',e=>{{
if(e.target.dataset.s){{flt.star=+e.target.dataset.s;
document.querySelectorAll('#stars button').forEach(b=>b.classList.toggle('on',b===e.target));render()}}}});
document.getElementById('touch').addEventListener('click',e=>{{flt.touch=!flt.touch;e.target.classList.toggle('on');render()}});
document.getElementById('sort').addEventListener('change',e=>{{flt.sort=e.target.value;render()}});
render();
applyLang();
</script>{CART_JS}</body></html>'''
    with open(os.path.join(OUT, 'index.html'), 'w') as f:
        f.write(idx)
    os.makedirs(os.path.join(OUT, 'account'), exist_ok=True)
    with open(os.path.join(OUT, 'account', 'index.html'), 'w') as f:
        f.write(ACCOUNT_PAGE)
    n = 0
    for g in games:
        d = os.path.join(OUT, 'game', g['slug'])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(game_page(g, total))
        n += 1
    print(f'OK: index + {n} game pages, {total} games (EN/DE/KR/RU/AR)')

if __name__ == '__main__':
    main()
