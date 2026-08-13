#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TONE PALETTE コーポレートサイト 本番デプロイ

使い方（このファイルのあるディレクトリで実行）:
    python3 deploy.py "コミットメッセージ"

やっていること:
  1. デザイン正本 ../outputs/hp-site-LIVE/index.html を読む
  2. 本番用の <head>（SEOタグ・OGP・canonical）を付けて index.html / 404.html を生成
  3. git commit → push（GitHub Pages が 1〜2分で https://tonepalette.com/ に反映）

注意:
  - CNAME ファイルは絶対に消さないこと（消すと独自ドメインが外れる）
  - デザインの編集は必ず ../outputs/hp-site-LIVE/index.html 側で行う
    （このリポジトリの index.html は自動生成物。直接編集しても次回上書きされる）
"""
import subprocess
import sys
import os

SRC = '../outputs/hp-site-LIVE/index.html'
BASE = 'https://tonepalette.com'
DESC = ('経営課題から逆算するSNSマーケティング。戦略設計・企画はTONE PALETTEが担い、'
        '制作は業界トップクリエイターとの共同制作で伴走します。')
OLD_TITLE = '<title>TONE PALETTE｜株式会社TONE PALETTE コーポレートサイト（デザイン案 v17＝v13.3ベース改修）</title>'

NEW_HEAD = '''<title>株式会社TONE PALETTE｜SNSマーケティング</title>
<meta name="description" content="%(d)s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TONE PALETTE">
<meta property="og:title" content="株式会社TONE PALETTE｜SNSマーケティング">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="%(b)s/">
<meta property="og:image" content="%(b)s/ogp.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="%(b)s/">
<link rel="icon" sizes="32x32" href="./favicon-32.png">
<link rel="apple-touch-icon" href="./apple-touch-icon.png">''' % {'d': DESC, 'b': BASE}


def build():
    if not os.path.exists(SRC):
        sys.exit('デザイン正本が見つかりません: %s' % SRC)
    s = open(SRC, encoding='utf-8').read()
    if s.count(OLD_TITLE) != 1:
        sys.exit('<title> のマーカーが一致しません。正本のタイトル行を確認してください')
    s = s.replace(OLD_TITLE, NEW_HEAD)
    s = '<!doctype html>\n<html lang="ja">\n<head>\n' + s
    s = s.replace('</style>', '</style>\n</head>\n<body>', 1)
    s = s.rstrip() + '\n</body>\n</html>\n'
    for out in ('index.html', '404.html'):
        open(out, 'w', encoding='utf-8').write(s)
    return len(s)


def main():
    msg = sys.argv[1] if len(sys.argv) > 1 else 'サイト更新'
    size = build()
    print('build: index.html / 404.html を生成しました（%d KB）' % (size // 1024))
    if not os.path.exists('CNAME'):
        open('CNAME', 'w').write('tonepalette.com\n')
        print('CNAME を再作成しました')
    subprocess.run(['git', 'add', '-A'], check=True)
    r = subprocess.run(['git', 'commit', '-m', msg + '\n\nCo-Authored-By: Claude <noreply@anthropic.com>'])
    if r.returncode != 0:
        print('コミットする変更がありません')
        return
    subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], check=False)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print('push 完了 → 1〜2分で https://tonepalette.com/ に反映されます')


if __name__ == '__main__':
    main()
