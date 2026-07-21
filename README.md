# TONE PALETTE Corporate Site

株式会社TONE PALETTE コーポレートサイト（公開予定: https://tonepalette.com/ ※ドメインは要最終確認）

LEAM HP（leam-hp）と同方式: **GitHub → Netlify自動デプロイ（ビルドレス・静的ファイルのみ）**

- `index.html` … サイト本体（1ファイル完結SPA・パス方式ルーティング）**←唯一の編集対象**
- `service/ works/ company/ contact/` … gen_routes.py が index.html から自動生成する複製（ページ別のtitle/OGP/canonical焼き込み済み）。**手で編集しない**
- `gen_routes.py` … 上記の生成スクリプト＋ sitemap.xml / robots.txt / 404.html 生成
- `sync_from_design.py` … デザイン作業用ソース（`../outputs/hp-site-v11/index.html`・hash方式・Artifactプレビュー用）から本番用 index.html を再生成する変換スクリプト。デザイン側で修正した場合はこれで同期
- `_redirects` … 未知パスをトップへ流すSPAフォールバック（実ファイル・実ディレクトリが常に優先）
- `ogp.png` / `favicon-32.png` / `apple-touch-icon.png` / `icon-512.png` … 画像・アイコン

## 更新方法（必ずこの順番）
A. このリポジトリの index.html を直接編集した場合:
1. `python3 gen_routes.py`
2. `git add -A && git commit && git push` → Netlifyが自動デプロイ

B. デザインソース（outputs/hp-site-v11）側で編集した場合:
1. `python3 sync_from_design.py`（本番用index.htmlを再生成）
2. `python3 gen_routes.py`
3. `git add -A && git commit && git push`

⚠️ gen_routes.py を実行し忘れると `/service` 等が古い本文のまま残る。push前に必ず実行。
⚠️ Netlifyのビルドは**使わない**（LEAMでビルド起因の全ページ404事故あり。静的デプロイに固定）。
⚠️ ドメイン設定時、@tonepalette.com のメール保護のため **MXレコードには触らない**（A/CNAMEのみ）。

## URL構造
`/` `/service` `/works` `/company` `/contact`（旧 `#service` 等はサイト内JSで自動転送）

## 公開前チェック（未完了）
- [ ] WORKS事例のダミー数値の実数化 or 削除 🔴
- [ ] ロゴ掲載許諾（GENDA/BanBan/シンコーポ/バイセル/Anker/Typeless/Kling AI）🔴
- [ ] 阿久根氏の写真が本人か確認
- [ ] 公開ドメインの最終確認（tonepalette.com想定）
