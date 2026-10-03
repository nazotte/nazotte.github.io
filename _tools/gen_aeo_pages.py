#!/usr/bin/env python3
"""公開ページの AEO / AIO / SEO 用ページを作る(標準ライブラリだけ)。

作るもの(手で編集しない。直すときはこのスクリプトを直して再実行する):
  index.md / kana/index.md / irodori/index.md / kanji/index.md / kanji/<1-6>/index.md / llms.txt

字の一覧と画数は stroke-data/data/*.json(公開済みの書き順データ)から取る。
使い方:  python3 _tools/gen_aeo_pages.py          # 書き出す
         python3 _tools/gen_aeo_pages.py --check  # 差分があれば exit 1
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://nazotte.github.io"
GEN_NOTE = "<!-- 生成物: _tools/gen_aeo_pages.py が作る。手で直さない -->"
PUBLISHED_NOTE = "<!-- 公開版(CHG-079 で発注者が公開を承認。連絡先 chemise_merry0o@icloud.com) -->"

# App Store の ID は iTunes Search API(lookup?bundleId=…&country=jp)で 2026-10-02 に確かめた値
APPS = {
    "kana": {"id": "6814138535", "bundle": "io.github.nazotte.kana", "name": "なぞっておぼえる ひらがな・カタカナ", "price": 0},
    1: {"id": "6814138746", "bundle": "io.github.nazotte.kanji1", "price": 0},
    2: {"id": "6814138729", "bundle": "io.github.nazotte.kanji2", "price": 0},
    3: {"id": "6814139038", "bundle": "io.github.nazotte.kanji3", "price": 500},
    4: {"id": "6814139047", "bundle": "io.github.nazotte.kanji4", "price": 500},
    5: {"id": "6814139059", "bundle": "io.github.nazotte.kanji5", "price": 500},
    6: {"id": "6814139116", "bundle": "io.github.nazotte.kanji6", "price": 500},
    # いろえらび64 は発注者から渡された App Store の URL と、そのページの表示(無料・iOS 17.0 以降・4+・教育)で 2026-10-03 に確かめた
    "irodori": {"id": "6816780704", "name": "いろえらび64 - こどものぬりえ", "price": 0, "os": "iOS 17.0 以降"},
}
GRADES = range(1, 7)
KANJI_NAMES = {g: f"なぞっておぼえる かんじ{g}年" for g in GRADES}
OS_REQ = "iOS 16.0 以降(iPhone・iPad)"


def store_url(key) -> str:
    return f"https://apps.apple.com/jp/app/id{APPS[key]['id']}"


def price_text(key) -> str:
    p = APPS[key]["price"]
    return "無料" if p == 0 else f"{p}円(買い切り)"


def load_kanji(g: int) -> list[tuple[str, int]]:
    d = json.loads((ROOT / f"stroke-data/data/kanji_strokes_g{g}.json").read_text(encoding="utf-8"))
    return [(v["char"], len(v["strokes"])) for v in d["strokes"].values()]


KANJI = {g: load_kanji(g) for g in GRADES}
TOTAL = sum(len(v) for v in KANJI.values())


def jsonld(obj) -> str:
    body = json.dumps(obj, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\n{body}\n</script>'


def publisher():
    return {"@type": "Organization", "name": "なぞっておぼえる", "url": f"{SITE}/"}


def app_ld(key, name, desc, page_url, level=None, os_name="iOS 16.0 以降"):
    ld = {
        "@context": "https://schema.org",
        "@type": "MobileApplication",
        "name": name,
        "description": desc,
        "url": page_url,
        "installUrl": store_url(key),
        "sameAs": store_url(key),
        "operatingSystem": os_name,
        "applicationCategory": "EducationalApplication",
        "inLanguage": "ja",
        "isAccessibleForFree": APPS[key]["price"] == 0,
        "offers": {"@type": "Offer", "price": str(APPS[key]["price"]), "priceCurrency": "JPY",
                   "url": store_url(key)},
        "contentRating": "4+",
        "publisher": publisher(),
    }
    if level:
        ld["educationalLevel"] = level
    return ld


def faq_ld(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }


def crumbs_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                            for i, (n, u) in enumerate(items)],
    }


def faq_md(faqs) -> str:
    return "\n\n".join(f"### {q}\n\n{a}" for q, a in faqs)


def front(title: str, desc: str) -> str:
    t, d = json.dumps(title, ensure_ascii=False), json.dumps(desc, ensure_ascii=False)
    return f"---\ntitle: {t}\ndescription: {d}\n---\n\n{GEN_NOTE}\n{PUBLISHED_NOTE}\n"


COMMON_FAQ_TAIL = [
    ("広告やアプリ内課金はありますか?",
     "ありません。インターネットにも接続せず、名前などの情報を集めません。練習の記録は端末の中だけに保存します。"),
    ("iPad でも使えますか?", f"使えます。対応は {OS_REQ} です。"),
    ("字のきれいさや、とめ・はね・はらいを判定しますか?",
     "判定しません。線を並べただけのような、明らかに違う書き方のときだけ、もういちど書くように促します。"),
]

# ---------------------------------------------------------------- かんじ(学年別)

def kanji_grade_page(g: int) -> str:
    n = len(KANJI[g])
    name = KANJI_NAMES[g]
    url = f"{SITE}/kanji/{g}/"
    desc = (f"小学{g}年生で習う漢字{n}字(学年別漢字配当表)を、正しい書き順でなぞって覚える iPhone・iPad アプリ。"
            f"{price_text(g)}。広告・通信なし。")
    others = " / ".join(f"[{o}年](../{o}/)" for o in GRADES if o != g)
    faqs = [
        (f"小学{g}年生で習う漢字は何字ですか?",
         f"{n}字です(小学校学習指導要領 別表「学年別漢字配当表」)。{name} は、この{n}字をすべて収録しています。"),
        (f"{name} は無料ですか?",
         "無料です。広告やアプリ内課金もありません。" if APPS[g]["price"] == 0 else
         f"{APPS[g]['price']}円の買い切りです。購入後に追加の課金や広告はありません。"),
        ("どうやって練習しますか?",
         "「なぞる」で光っている画を書き順どおりに1画ずつなぞり、「かいてみる」で例文の□に入る漢字を見ないで書きます(1回5問)。"
         "わからないときは手本と書き順の番号を見られます。見ないで書けた字は花丸で数えます(点数は出しません)。"),
        ("書き順は何に合わせていますか?",
         "小学校の書写(えんぴつ)で教わる書き方に合わせています。書き順と手本の字形は KanjiVG のデータを改変して使い、"
         "改変したデータは「書き順データ」のページで公開しています。違う字を見つけたらサポートからお知らせください。"),
        ("読み上げはありますか?", "例文と出題を、ずんだもんの声(VOICEVOX)で読み上げます。"),
        *COMMON_FAQ_TAIL,
        ("ほかの学年もありますか?",
         f"小学1年〜6年まで学年ごとに1本ずつあります(全{TOTAL}字)。ひらがな・カタカナのアプリもあります。"),
    ]
    items = "\n".join(f'  <li><span class="k">{c}</span><span class="s">{st}画</span></li>' for c, st in KANJI[g])
    table = f'<ul class="kanji-grid" aria-label="小学{g}年生で習う漢字 {n}字">\n{items}\n</ul>'

    ld = [
        app_ld(g, name, desc, url, level=f"小学{g}年"),
        faq_ld(faqs),
        crumbs_ld([("なぞっておぼえる", f"{SITE}/"), ("かんじ", f"{SITE}/kanji/"), (f"{g}年", url)]),
    ]
    return f"""{front(f'{name} - 小学{g}年生の漢字{n}字を書き順どおりに', desc)}
# {name}

**{name} は、小学{g}年生で習う漢字{n}字を、正しい書き順でなぞって覚える iPhone・iPad 向けのアプリです。**
文部科学省の学年別漢字配当表のとおりの{n}字を収録しています。価格は{price_text(g)}で、広告・アプリ内課金・通信はありません。

<a class="store-button" href="{store_url(g)}">App Store で見る</a>

| 項目 | 内容 |
|---|---|
| 収録する字 | 小学{g}年の漢字 {n}字(学年別漢字配当表) |
| 価格 | {price_text(g)} |
| 対応 | {OS_REQ} |
| 年齢区分 | 4+ |
| 広告・課金・通信 | なし |
| 練習のしかた | なぞる(書き順どおりに1画ずつ)/ かいてみる(例文の□を見ないで書く) |
| 読み上げ | ずんだもんの声(VOICEVOX) |
| 書き順 | 小学校の書写(えんぴつ)の書き方に合わせる。KanjiVG を改変([書き順データ](../../stroke-data/)) |

## 小学{g}年生で習う漢字の一覧({n}字)

学年別漢字配当表の順です。画数は、アプリの書き順データの画数です。

{table}

## よくある質問

{faq_md(faqs)}

## ほかの学年

{others} / [かんじ 1〜6年の一覧](../) / [ひらがな・カタカナ](../../kana/)

{chr(10).join(jsonld(x) for x in ld)}
"""


def kanji_hub_page() -> str:
    url = f"{SITE}/kanji/"
    desc = (f"小学1〜6年生で習う漢字{TOTAL}字を、学年ごとのアプリで正しい書き順でなぞって覚える。"
            "1・2年は無料、3〜6年は各500円。広告・通信なし。")
    rows = "\n".join(
        f"| [{KANJI_NAMES[g]}]({g}/) | {len(KANJI[g])}字 | {price_text(g)} | [App Store]({store_url(g)}) |"
        for g in GRADES)
    faqs = [
        ("小学校で習う漢字は全部で何字ですか?",
         f"{TOTAL}字です(学年別漢字配当表)。学年ごとに "
         + "・".join(f"{g}年 {len(KANJI[g])}字" for g in GRADES) + " です。"),
        ("なぜ学年ごとに別のアプリなのですか?",
         "いま習っている学年の字だけに絞って練習できるようにするためです。必要な学年だけを入れられます。"),
        ("どの学年が無料ですか?", "1年と2年は無料です。3〜6年は各500円の買い切りで、アプリ内課金はありません。"),
        *COMMON_FAQ_TAIL,
    ]
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "なぞっておぼえる かんじ(小学1〜6年)",
        "itemListElement": [{"@type": "ListItem", "position": g, "url": f"{SITE}/kanji/{g}/",
                             "name": KANJI_NAMES[g]} for g in GRADES],
    }
    ld = [item_list, faq_ld(faqs),
          crumbs_ld([("なぞっておぼえる", f"{SITE}/"), ("かんじ", url)])]
    return f"""{front('なぞっておぼえる かんじ - 小学1〜6年の漢字を書き順どおりに', desc)}
# なぞっておぼえる かんじ(小学1〜6年)

**なぞっておぼえる かんじ は、小学校で習う漢字{TOTAL}字を、学年ごとのアプリで正しい書き順でなぞって覚えるシリーズです。**
iPhone・iPad 向けで、1・2年は無料、3〜6年は各500円です。広告・アプリ内課金・通信はありません。

| アプリ | 字数 | 価格 | 入手 |
|---|---|---|---|
{rows}

## よくある質問

{faq_md(faqs)}

[トップへ](../) / [ひらがな・カタカナ](../kana/) / [書き順データ](../stroke-data/)

{chr(10).join(jsonld(x) for x in ld)}
"""

# ---------------------------------------------------------------- かな

def kana_page() -> str:
    url = f"{SITE}/kana/"
    name = APPS["kana"]["name"]
    desc = ("ひらがな46字とカタカナ46字を、正しい書き順でなぞって覚える iPhone・iPad アプリ。"
            "無料・広告なし・通信なし。ずんだもんの声で読み上げ。")
    faqs = [
        ("何文字を練習できますか?", "ひらがな46字とカタカナ46字(清音)の、計92字です。"),
        (f"{name} は無料ですか?", "無料です。広告やアプリ内課金もありません。"),
        ("どうやって練習しますか?",
         "「なぞる」で光っている画を書き順どおりに1画ずつなぞり、「かいてみる」で読み上げを聞いて文字を見ないで書きます。"
         "わからないときは手本を見て、その上をなぞって練習できます。"),
        ("読み上げの声は変えられますか?", "ずんだもんの声(VOICEVOX)と、この端末の声を選べます。"),
        ("書き順は何に合わせていますか?",
         "小学校の書写(えんぴつ)で教わる書き方に合わせています。書き順の点は KanjiVG のデータを改変して使っています。"),
        *COMMON_FAQ_TAIL,
        ("画面の言葉を日本語以外にできますか?",
         "できます。画面の文字は13の言語から選べます。読み上げは、字の音を覚えるため、いつも日本語です。"),
    ]
    ld = [app_ld("kana", name, desc, url, level="幼児・小学1年"), faq_ld(faqs),
          crumbs_ld([("なぞっておぼえる", f"{SITE}/"), ("ひらがな・カタカナ", url)])]
    return f"""{front(f'{name} - 書き順どおりになぞって覚える', desc)}
# {name}

**{name} は、ひらがな46字とカタカナ46字を、正しい書き順でなぞって覚える iPhone・iPad 向けのアプリです。**
無料で、広告・アプリ内課金・通信はありません。

<a class="store-button" href="{store_url('kana')}">App Store で見る</a>

| 項目 | 内容 |
|---|---|
| 収録する字 | ひらがな46字・カタカナ46字(清音) |
| 価格 | 無料 |
| 対応 | {OS_REQ} |
| 年齢区分 | 4+ |
| 広告・課金・通信 | なし |
| 練習のしかた | なぞる / かいてみる |
| 読み上げ | ずんだもんの声(VOICEVOX)/ この端末の声 |

## よくある質問

{faq_md(faqs)}

[トップへ](../) / [かんじ 1〜6年](../kanji/) / [書き順データ](../stroke-data/)

{chr(10).join(jsonld(x) for x in ld)}
"""

# ---------------------------------------------------------------- いろえらび64

def irodori_page() -> str:
    url = f"{SITE}/irodori/"
    name = APPS["irodori"]["name"]
    os_req = f"{APPS['irodori']['os']}(iPhone・iPad)"
    desc = ("64色から色を選んで塗る、こども向けのぬりえ iPhone・iPad アプリ。94枚の線画。"
            "「よるの かみ」で塗った色がネオンのように光る。無料・広告なし・通信なし。")
    faqs = [
        (f"{name} は無料ですか?", "無料です。広告やアプリ内課金もありません。"),
        ("何歳向けですか?", "5〜12歳のこども向けです。年齢区分は 4+ です。"),
        ("何枚のぬりえがありますか?", "94枚の線画を収録しています。64色から色を選んで塗ります。"),
        ("「よるの かみ」とは何ですか?", "紙を「よるの かみ」にすると、暗い背景の上で、塗った色がネオンのように光ります。"),
        ("塗った絵を写真アプリに残せますか?",
         "ギャラリーで絵を開き「しゃしんに のこす」を押すと、保護者の方への確認(かんたんな たし算)のあと、写真アプリに追加します。"
         "追加するだけで、写真を読みとることはありません。"),
        ("画面の見た目を変えられますか?",
         "「設定」(保護者の方への確認のあと)の「画面の見た目」で、パーティー ポップ・いつもの・ネオン クラブ・オーロラ グラス から選べます。"),
        ("個人情報は集めますか?",
         "集めません。通信もアカウント登録もありません。作品は端末の中だけに保存します。"),
        ("作品を消せますか?", "ギャラリーで絵を開き「けす」を押します。消した作品は戻せません。"),
        ("iPad でも使えますか?", f"使えます。対応は {os_req} です。"),
    ]
    ld = [app_ld("irodori", name, desc, url, level="幼児・小学生", os_name=APPS["irodori"]["os"]),
          faq_ld(faqs),
          crumbs_ld([("なぞっておぼえる", f"{SITE}/"), ("いろえらび64", url)])]
    return f"""{front(f'{name} - 64色から選んで塗るぬりえ', desc)}
# {name}

**{name} は、64色から色を選んで塗る、こども向けのぬりえアプリです。**
94枚の線画を収録し、紙を「よるの かみ」にすると塗った色がネオンのように光ります。無料で、広告・アプリ内課金・通信はありません。

<a class="store-button" href="{store_url('irodori')}">App Store で見る</a>

| 項目 | 内容 |
|---|---|
| 内容 | 64色から選んで塗るぬりえ(線画94枚) |
| 対象 | 5〜12歳 |
| 価格 | 無料 |
| 対応 | {os_req} |
| 年齢区分 | 4+ |
| 広告・課金・通信 | なし |
| 保存 | 作品は端末の中だけ。写真アプリへは、保護者の方が選んだときだけ「追加」 |

## よくある質問

{faq_md(faqs)}

[トップへ](../) / [サポート](../support/) / [プライバシーポリシー](../privacy/)

{chr(10).join(jsonld(x) for x in ld)}
"""

# ---------------------------------------------------------------- トップ・llms.txt

def index_page() -> str:
    desc = (f"正しい書き順でなぞって、ひらがな・カタカナと小学校の漢字{TOTAL}字を覚える iPhone・iPad アプリ。"
            "広告・アプリ内課金・通信なし。")
    rows = [f"| [{APPS['kana']['name']}](kana/) | ひらがな46字・カタカナ46字 | 無料 | [App Store]({store_url('kana')}) |"]
    rows += [f"| [{KANJI_NAMES[g]}](kanji/{g}/) | 小学{g}年の漢字{len(KANJI[g])}字 | {price_text(g).replace('(買い切り)', '')} "
             f"| [App Store]({store_url(g)}) |" for g in GRADES]
    rows += [f"| [{APPS['irodori']['name']}](irodori/) | 64色から選んで塗るぬりえ(線画94枚) | 無料 | [App Store]({store_url('irodori')}) |"]
    site_ld = {
        "@context": "https://schema.org", "@type": "WebSite", "name": "なぞっておぼえる",
        "url": f"{SITE}/", "inLanguage": "ja", "publisher": publisher(),
    }
    org_ld = {**publisher(), "@context": "https://schema.org",
              "sameAs": [store_url(k) for k in APPS]}
    return f"""{front('書き順どおりになぞって覚えるアプリ', desc)}
# なぞっておぼえる

**なぞっておぼえる は、正しい書き順でなぞって、ひらがな・カタカナと小学校の漢字を覚える iPhone・iPad 向けのアプリです。**
ひらがな・カタカナが1本、漢字は小学1〜6年の学年ごとに1本ずつ(全{TOTAL}字)あります。広告、アプリ内課金、通信はありません。
同じ制作元の、64色から選んで塗るぬりえアプリ「いろえらび64」もあります。

| アプリ | 内容 | 価格 | 入手 |
|---|---|---|---|
{chr(10).join(rows)}

- [かんじ(小学1〜6年)の一覧とよくある質問](kanji/)
- [いろえらび64 - こどものぬりえ](irodori/)
- [プライバシーポリシー](privacy/)
- [サポート](support/)
- [書き順データ(CC BY-SA 3.0)](stroke-data/)
- [English](en/)

{jsonld(site_ld)}
{jsonld(org_ld)}
"""


def llms_txt() -> str:
    lines = [
        "# なぞっておぼえる",
        "",
        f"> 正しい書き順でなぞって、ひらがな・カタカナと小学校の漢字({TOTAL}字)を覚える iPhone・iPad 向けアプリのシリーズ。"
        "広告・アプリ内課金・通信なし。個人情報を集めない。対応は iOS 16.0 以降(いろえらび64 は iOS 17.0 以降)。"
        "同じ制作元に、ぬりえアプリ「いろえらび64」がある。",
        "",
        "## アプリ",
        "",
        f"- [{APPS['kana']['name']}]({SITE}/kana/): ひらがな46字・カタカナ46字。無料。App Store: {store_url('kana')}",
    ]
    lines += [f"- [{KANJI_NAMES[g]}]({SITE}/kanji/{g}/): 小学{g}年生で習う漢字{len(KANJI[g])}字(学年別漢字配当表)。"
              f"{price_text(g)}。App Store: {store_url(g)}" for g in GRADES]
    lines.append(f"- [{APPS['irodori']['name']}]({SITE}/irodori/): 64色から色を選んで塗る、5〜12歳向けのぬりえ。線画94枚。"
                 f"無料。App Store: {store_url('irodori')}")
    lines += [
        "",
        "## 事実",
        "",
        "- 練習: 「なぞる」(光る画を書き順どおりに1画ずつ)と「かいてみる」(見ないで書く。漢字は例文の□を埋める)",
        "- 字のきれいさ・とめ・はね・はらいは判定しない。明らかに違う書き方だけ、書き直しを促す",
        "- 書き順: 小学校の書写(えんぴつ)の書き方に合わせる。データは KanjiVG (c) Ulrich Apel を改変(CC BY-SA 3.0)",
        "- 読み上げ: VOICEVOX:ずんだもん。練習の記録は端末の中だけに保存する",
        "",
        "## ページ",
        "",
        f"- [かんじ 1〜6年の一覧]({SITE}/kanji/)",
        f"- [サポート・よくある質問]({SITE}/support/)",
        f"- [プライバシーポリシー]({SITE}/privacy/)",
        f"- [書き順データ]({SITE}/stroke-data/)",
        f"- [English]({SITE}/en/)",
        "",
    ]
    return "\n".join(lines)


def outputs() -> dict[Path, str]:
    out = {ROOT / "index.md": index_page(), ROOT / "kana/index.md": kana_page(),
           ROOT / "kanji/index.md": kanji_hub_page(), ROOT / "llms.txt": llms_txt(),
           ROOT / "irodori/index.md": irodori_page()}
    for g in GRADES:
        out[ROOT / f"kanji/{g}/index.md"] = kanji_grade_page(g)
    return out


def main() -> int:
    check = "--check" in sys.argv[1:]
    stale = []
    for path, text in outputs().items():
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(path.relative_to(ROOT))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    if stale:
        print("生成し直しが必要:", *stale, sep="\n  ")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
