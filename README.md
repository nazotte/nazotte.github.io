# nazotte.github.io

「なぞっておぼえる」(ひらがな・カタカナ / かんじ1〜6年)と「いろえらび64」の公開ページ・問い合わせ窓口。

## このリポジトリが公開ページの正(2026-10-02〜)

- ページ(トップ・アプリごとのページ・サポート・プライバシーポリシー・英語版)は、**このリポジトリだけ**で直して push する。アプリのリポジトリには写しを置かない
- `index.md`・`kana/`・`kanji/`・`llms.txt` は生成物。`python3 _tools/gen_aeo_pages.py` で作り直す(`--check` で差分を検知)
- 書き順データ(`stroke-data/data/*.json` と `stroke-data/index.md`)は、アプリのリポジトリの `scripts/gen_site_stroke_data.py` が作る。作り直したらここへ写して push する
- 見た目は `_layouts/default.html`・`assets/css/style.scss`。フッターの著作権は `_config.yml` の `copyright_*`(© 2026 Team hetyomokore)
- 公開する前に、手元で組み立てて確かめる(Jekyll。GitHub Pages と同じ github-pages gem)
