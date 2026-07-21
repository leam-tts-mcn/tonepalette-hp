#!/usr/bin/env python3
# デザインソース（outputs/hp-site-v11/index.html・hash方式）→ 本番用 index.html（パス方式）変換
# 実行後は必ず gen_routes.py も実行すること
import sys

SRC = '../outputs/hp-site-v11/index.html'
OUT = 'index.html'
BASE = 'https://tonepalette.com'
DESC = '経営課題から逆算するSNSマーケティング。戦略設計・企画はTONE PALETTEが単体で担い、制作は業界トップクリエイターとの共同制作で伴走します。'

s = open(SRC, encoding='utf-8').read()

def rep(old, new, cnt=1, at_least=False):
    global s
    n = s.count(old)
    ok = (n >= cnt) if at_least else (n == cnt)
    if not ok:
        sys.exit('sync: 置換マーカー不一致 (%d件): %s' % (n, old[:80]))
    s = s.replace(old, new)

old_head = '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TONE PALETTE｜株式会社TONE PALETTE コーポレートサイト（デザイン案 v12）</title>'''
new_head = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>株式会社TONE PALETTE｜SNSマーケティング</title>
<meta name="description" content="%(d)s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TONE PALETTE">
<meta property="og:title" content="株式会社TONE PALETTE｜SNSマーケティング">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="%(b)s/">
<meta property="og:image" content="%(b)s/ogp.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="%(b)s/">
<link rel="icon" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">''' % {'d': DESC, 'b': BASE}
rep(old_head, new_head)
rep('</style>', '</style>\n</head>\n<body>')

for pg in ['service', 'works', 'company', 'contact']:
    rep('href="#%s"' % pg, 'href="/%s"' % pg, 1, at_least=True)
rep('href="#top"', 'href="/"', 1, at_least=True)

rep("if(location.hash!=='#'+p){history.replaceState(null,'','#'+p)}", "applyMeta(p);")

rep('''  var wiping=false;
  function go(p,instant){
    var w=document.getElementById('wipe');''',
'''  var wiping=false;
  var META={
    top:{t:'株式会社TONE PALETTE｜SNSマーケティング',d:'%(d)s'},
    service:{t:'SERVICE｜SNSアカウント運用・インフルエンサーマーケティング｜株式会社TONE PALETTE',d:'戦略設計から企画・制作・運用・分析まで。業界トップのパートナークリエイターとの共同制作で、成果につながるSNS運用を提供します。'},
    works:{t:'WORKS｜取引実績・事例｜株式会社TONE PALETTE',d:'株式会社TONE PALETTEの取引実績と支援事例をご紹介します。'},
    company:{t:'COMPANY｜会社概要・メンバー｜株式会社TONE PALETTE',d:'株式会社TONE PALETTEの会社概要・ミッション・メンバーをご紹介します。'},
    contact:{t:'CONTACT｜お問い合わせ｜株式会社TONE PALETTE',d:'SNS運用に関するご相談・お見積もり依頼はこちら。最短翌営業日にご返信します。'}
  };
  function urlFor(p){return p==='top'?'/':'/'+p}
  function applyMeta(p){
    var m=META[p];if(!m)return;
    document.title=m.t;
    var set=function(sel,attr,v){var el=document.querySelector(sel);if(el)el.setAttribute(attr,v)};
    var url='%(b)s'+(p==='top'?'/':'/'+p+'/');
    set('meta[name="description"]','content',m.d);
    set('meta[property="og:title"]','content',m.t);
    set('meta[property="og:description"]','content',m.d);
    set('meta[property="og:url"]','content',url);
    set('link[rel="canonical"]','href',url);
  }
  function curPage(){
    var h=location.hash||'';
    if(h.length>1){var hp=h.replace(/^#\\/?/,'');if(document.getElementById('p-'+hp))return hp}
    var p=(location.pathname.replace(/\\/+$/,'')||'/');
    p=(p==='/')?'top':p.slice(1);
    return document.getElementById('p-'+p)?p:'top';
  }
  function go(p,instant,fromPop){
    if(!fromPop){
      var u=urlFor(p);var cp=location.pathname.replace(/\\/+$/,'')||'/';
      if(cp!==u){try{history.pushState(null,'',u)}catch(_){/*file://等*/}}
    }
    var w=document.getElementById('wipe');''' % {'d': DESC, 'b': BASE})

rep("window.addEventListener('hashchange',function(){go(location.hash.replace('#','')||'top')});",
'''window.addEventListener('popstate',function(){go(curPage(),false,true)});
  window.addEventListener('hashchange',function(){
    var h=location.hash.replace(/^#\\/?/,'');
    if(h&&document.getElementById('p-'+h)){try{history.replaceState(null,'',urlFor(h))}catch(_){}}
    go(curPage(),false,true);
  });''')

rep("  go(location.hash.replace('#','')||'top',true);",
'''  (function(){var h=location.hash.replace(/^#\\/?/,'');if(h&&document.getElementById('p-'+h)){try{history.replaceState(null,'',urlFor(h))}catch(_){}}})();
  go(curPage(),true,true);''')

s = s.rstrip() + '\n</body>\n</html>\n'
open(OUT, 'w', encoding='utf-8').write(s)
print('sync: index.html regenerated (%d chars)' % len(s))
print('次に必ず: python3 gen_routes.py')
