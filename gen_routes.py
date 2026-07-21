#!/usr/bin/env python3
# ローカル実行用：index.html からルート別HTML（title/description/OGP/canonical焼き込み）と
# sitemap.xml / robots.txt / 404.html を生成する。実行後に生成物ごと git push する（Netlifyビルドは使わない＝LEAM HPと同方式）。
# メタ文言は index.html 内の JS `META` と同期させること。
# 手順: index.html を更新 → python3 gen_routes.py → git add -A && git commit && git push
import re
import sys
import datetime

BASE = 'https://tonepalette.com'
RESERVED = ('',)

ROUTES = {
    '/service': {
        't': 'SERVICE｜SNSアカウント運用・インフルエンサーマーケティング｜株式会社TONE PALETTE',
        'd': '戦略設計から企画・制作・運用・分析まで。業界トップのパートナークリエイターとの共同制作で、成果につながるSNS運用を提供します。',
    },
    '/works': {
        't': 'WORKS｜取引実績・事例｜株式会社TONE PALETTE',
        'd': '株式会社TONE PALETTEの取引実績と支援事例をご紹介します。',
    },
    '/company': {
        't': 'COMPANY｜会社概要・メンバー｜株式会社TONE PALETTE',
        'd': '株式会社TONE PALETTEの会社概要・ミッション・メンバーをご紹介します。',
    },
    '/contact': {
        't': 'CONTACT｜お問い合わせ｜株式会社TONE PALETTE',
        'd': 'SNS運用に関するご相談・お見積もり依頼はこちら。最短翌営業日にご返信します。',
    },
}


def sub_once(html, pattern, repl, label):
    out, n = re.subn(pattern, lambda _: repl, html, count=1, flags=re.S)
    if n != 1:
        sys.exit('gen_routes: %s の置換に失敗（マーカー不一致）' % label)
    return out


def stamp(src, path, meta):
    url = BASE + path + '/'
    h = src
    h = sub_once(h, r'<title>.*?</title>', '<title>%s</title>' % meta['t'], path + ' title')
    h = sub_once(h, r'<meta name="description" content="[^"]*">',
                 '<meta name="description" content="%s">' % meta['d'], path + ' description')
    h = sub_once(h, r'<meta property="og:title" content="[^"]*">',
                 '<meta property="og:title" content="%s">' % meta['t'], path + ' og:title')
    h = sub_once(h, r'<meta property="og:description" content="[^"]*">',
                 '<meta property="og:description" content="%s">' % meta['d'], path + ' og:description')
    h = sub_once(h, r'<meta property="og:url" content="[^"]*">',
                 '<meta property="og:url" content="%s">' % url, path + ' og:url')
    h = sub_once(h, r'<link rel="canonical" href="[^"]*">',
                 '<link rel="canonical" href="%s">' % url, path + ' canonical')
    return h


def main():
    import os
    src = open('index.html', encoding='utf-8').read()
    for path, meta in ROUTES.items():
        d = path.strip('/')
        if d in RESERVED:
            sys.exit('gen_routes: 予約ディレクトリへの出力は禁止 ' + repr(d))
        os.makedirs(d, exist_ok=True)
        with open(d + '/index.html', 'w', encoding='utf-8') as f:
            f.write(stamp(src, path, meta))
        print('generated %s/index.html' % d)

    today = datetime.date.today().isoformat()
    urls = [BASE + '/'] + [BASE + p + '/' for p in ROUTES]
    items = '\n'.join(
        '  <url><loc>%s</loc><lastmod>%s</lastmod></url>' % (u, today) for u in urls
    )
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                '%s\n</urlset>\n' % items)
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write('User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % BASE)
    print('generated sitemap.xml (%d urls) / robots.txt' % len(urls))
    import shutil
    shutil.copyfile('index.html', '404.html')
    print('generated 404.html (copy of index.html)')


if __name__ == '__main__':
    main()
