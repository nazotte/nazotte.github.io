---
title: 書き順データ(CC BY-SA 3.0)
---

<!-- 下書き(HND-06 §4-4・LG-02・ISS-04)。発注者の確認と承認の前は公開しない。データのファイルは公開のときに config/kanji_strokes_g<N>.json から写す -->

# 書き順データ(CC BY-SA 3.0)

「なぞっておぼえる かんじ1年〜6年」で使っている、漢字の書き順と手本の字形のデータです。
[KanjiVG](https://kanjivg.tagaini.net/)(© Ulrich Apel)のデータを改変して作りました。
改変したこのデータも、元のデータと同じ [クリエイティブ・コモンズ 表示 - 継承 3.0 非移植(CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/deed.ja) で公開します。

## 元のデータ

- KanjiVG (© Ulrich Apel) https://kanjivg.tagaini.net/
- 版: KanjiVG の Git コミット `422b5538595676da918c288a4230cb5e22a1ee7e`
- ライセンス: CC BY-SA 3.0

## 改変した内容

- 小学校で習う漢字(学年別漢字配当表の1,026字)だけを取り出し、学年ごとのファイルに分けた
- 各画の線(SVG のパス)の曲線を細かく点に分け、Ramer-Douglas-Peucker 法で間引いて点の列にした
- 座標を KanjiVG の枠の大きさ(109)で割って 0〜1 にした
- 画の順番(書き順)・画の向き・字の形・画の種類(kvg:type)は変えていない

## ファイル

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
