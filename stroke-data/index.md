---
title: 書き順データ(CC BY-SA 3.0)
---

<!-- データのファイルは scripts/gen_site_stroke_data.py が作る(手で置かない。社内の記録は落とす) -->

# 書き順データ(CC BY-SA 3.0)

「なぞっておぼえる」のアプリで使っている、書き順のデータです。
[KanjiVG](https://kanjivg.tagaini.net/)(© Ulrich Apel)のデータを改変して作りました。
改変したこのデータも、元のデータと同じ [クリエイティブ・コモンズ 表示 - 継承 3.0 非移植(CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/deed.ja) で公開します。

- [ひらがな・カタカナ](#ひらがなカタカナ)(なぞっておぼえる ひらがな・カタカナ)
- [漢字](#漢字)(なぞっておぼえる かんじ1年〜6年)

## ひらがな・カタカナ

なぞるときに出す書き順の点(書きはじめ・通る点・書きおわり)のデータです。
手本の字そのものは iOS のシステムフォントで描いていて、このデータには入っていません。

### 元のデータ

- KanjiVG (© Ulrich Apel) https://kanjivg.tagaini.net/
- 版: 2026-09-18 に取得した KanjiVG の master。字ごとの元の SVG ファイルの名前と SHA-256 を、データの `source` に書いてあります
- ライセンス: CC BY-SA 3.0

### 改変した内容

- ひらがな・カタカナ(清音。46字ずつ、計92字)だけを取り出した
- 各画の道すじを、字ごとにアプリの手本の字(iOS のシステムフォント)に重ね、手本の字の線の中心をたどるように、書きはじめ・通る点・書きおわりの点を置き直した。点は手本の字に合わせて置いたので、KanjiVG の線の形とは少し違う
- 座標は、一辺を 1 とした正方形のキャンバスの上の位置(0〜1)にした。手本の字は、一辺の 0.7 倍の大きさで中央に描いている
- 画の数・順番・向き(書き順)は変えていない

### ファイル

| 対象 | ファイル | 字数 |
|---|---|---|
| ひらがな・カタカナ | [`kana_strokes.json`](data/kana_strokes.json) | 92 |

## 漢字

漢字の書き順と手本の字形のデータです。

### 元のデータ

- KanjiVG (© Ulrich Apel) https://kanjivg.tagaini.net/
- 版: KanjiVG の Git コミット `422b5538595676da918c288a4230cb5e22a1ee7e`
- ライセンス: CC BY-SA 3.0

### 改変した内容

- 小学校で習う漢字(学年別漢字配当表の1,026字)だけを取り出し、学年ごとのファイルに分けた
- 各画の線(SVG のパス)の曲線を細かく点に分け、Ramer-Douglas-Peucker 法で間引いて点の列にした
- 座標を KanjiVG の枠の大きさ(109)で割って 0〜1 にした
- 画の順番(書き順)・画の向き・字の形・画の種類(kvg:type)は変えていない

### ファイル

| 学年 | ファイル | 字数 |
|---|---|---|
| 1年 | [`kanji_strokes_g1.json`](data/kanji_strokes_g1.json) | 80 |
| 2年 | [`kanji_strokes_g2.json`](data/kanji_strokes_g2.json) | 160 |
| 3年 | [`kanji_strokes_g3.json`](data/kanji_strokes_g3.json) | 200 |
| 4年 | [`kanji_strokes_g4.json`](data/kanji_strokes_g4.json) | 202 |
| 5年 | [`kanji_strokes_g5.json`](data/kanji_strokes_g5.json) | 193 |
| 6年 | [`kanji_strokes_g6.json`](data/kanji_strokes_g6.json) | 191 |

## ライセンス

このページのデータは CC BY-SA 3.0 です。使うときは、KanjiVG(© Ulrich Apel)と、このデータを改変したこと、ライセンス(CC BY-SA 3.0)を表示してください。改変したものを配るときは、同じライセンスにしてください。
