# ペット育成ゲーム `pet.html` 引き継ぎ

（旧: `i-tachiiri/tennis-game` → 新: `tachiiri-org/front-asobi`）

## 0. 最初にこれだけやって（重要）

このゲームは **1つの Artifact に上書き公開し続けている**。
URL が変わると **プレイヤーのセーブデータ（localStorage）が消える**（Artifact ごとに
オリジンが分かれているため）。だから **必ず同じ URL に上書き**すること。

```
Artifact URL: https://claude.ai/code/artifact/2d275b3e-1699-4c98-8eab-90436e21a931
タイトル: もふもふペット育成記
```

新しいセッションでの手順:

1. **先に読む** — `Artifact` ツールを `action: "read"` + この `url` で呼ぶ。
   （一度も read / publish していない Artifact への publish は拒否される）
2. 公開するときは `Artifact` ツールに **`url` をこの URL で渡す**。
   `url` を渡さないと**別の新しい Artifact** ができてしまい、セーブが引き継がれない。
3. `favicon` は再公開時は**渡さない**（既存アイコンが維持される）。

## 1. これは何

- 日本語の、子ども向け「ペット育成ゲーム」。**`pet.html` 1ファイル完結**（約 11,200行 / 610KB）。
- ビルドもフレームワークも無し。`<style>` + `<script>` を直書き、描画は **Canvas 2D の手続き的お絵かき**。
- セーブは `localStorage`、キーは `pet_raising_save_v1`。
- ユーザー（お子さん）が日本語で機能追加をリクエスト → 実装 → Playwright で検証 →
  Artifact を再公開 → commit & push、というのを毎ターン繰り返してきた。

## 2. 開発の約束ごと（これまでのやり方）

毎リクエストで必ずこの順番でやる:

1. `pet.html` を編集（Python スクリプトでアンカー置換するのが安全 → §6）
2. `<script>` を抜き出して `node --check` で構文チェック
3. `build-artifact.py` で Artifact 用 HTML とプレビュー HTML を生成
4. **Playwright + Chromium (headless) で実際に動かして検証**（スクリーンショットも撮る）
5. 同じ URL に Artifact を再公開
6. commit & push

文言はぜんぶ **ひらがな中心のやさしい日本語**（漢字は最小限、分かち書き）。
コード中のコメントも日本語。

## 3. `pet.html` の地図（行番号は 2026-09-05 時点）

| 行 | セクション |
|---|---|
| 232 | `SAVE_KEY = 'pet_raising_save_v1'` / `DAY_SEC = 180`（ゲーム内1日=3分） |
| 1986 | utility（`big()` / `coinText()` / `clamp` など） |
| 2196 | state（`newState()` / `save()` / `load()`＋マイグレーション） |
| 2304 | time progression（`applyTime()`） |
| 2455 | ともだちのペット（`FRIENDS` 8人 / `ROOMIE_LV = 5`） |
| 2914 | キーボードでおしゃべり |
| 3111 | おてつだいロボット |
| 3324 | orders（「〜して」とお願いすると動く） |
| 3589 | actions（`ACTIVITIES` 149種） |
| 4059 | ショップ本体（`SHOP` 10,000品 / `SHOP_PER = 20` ページング） |
| 4176 | 🎲 むげんショップ `INF_TOTAL = 9×10^5000` |
| 4310 | 🍬 おかしやさん `SWEET_TOTAL = 9億` |
| 4430 | 🪑 かぐやさん `FURN_TOTAL = 10兆` |
| 4545 | 🏬 おみせビル（**7棟 109階**、後述） |
| 5212 | 🎁 ぜんぶもらう / 🔁 またかえるようにする |
| 5348 | ちょきんばこ・ぎんこう |
| 5733 | drawing（Canvas 描画 4,600行） |
| 11000 | `DECOR_MAX = 60`（部屋に飾る上限） |
| 11084 | main loop |

`SHOP_CAT` = `room, kitchen, bedroom, yard, wear, health, friend, style, inf, sweet, furn, more`

## 4. いちばん複雑なところ: 🏬 おみせビル（`more` タブ）

**巨大な数の商品を売る**ための仕組み。7棟・109階、最大 `10^1400000` 個。

```
🌈 デパート        9階   10^12 〜 10^19
🗼 タワー         19階   10^2000 〜 10^38000（2000ずつ）
🌍 ワールドモール  50階   10^10000 〜 10^500000（10000ずつ）
🎉 ひろば          3階   10^149 ×3 = ちょうど 3×10^149
🐉 でんせつのしろ  9階   10^600000 〜 10^1400000（100000ずつ）
🎡 ゆうえんち     10階   10^1323 ×10 = ちょうど 10^1324
🐟 すいぞくかん    9階   10^2295 ×9 = ちょうど 9×10^2295
```

### 設計のキモ（ここを壊さないで）

- 各フロアは `{ id, tab, note, mat[], kind[{n,e}], exp }`。
  商品数は **`10^exp`**。`total` を BigInt で持たない（`moreTotal()` で必要時のみ生成）。
- 商品番号は **BigInt ではなく「10進の文字列」のまま**扱う。140万桁でも 60〜200ms で動く。
  - `moAdd(num,k)` / `moSub(num,k)` … 末尾15桁だけ見る（繰り上がり時のみ上位を走査）
  - `moMod(num,m)` / `moDiv(num,d)` … 線形
  - `moDigit(num,place)` … 右から place 桁目（名前・絵文字はここから決まる）
  - `moreCost(num)` … 末尾15桁だけで決める（O(1)）
  - `moPageText(start)` … 先頭19桁と桁数からページ番号表示を作る（O(1)）
  - `moreLast(sh)` … 最終ページ先頭 = `10^exp - 8` = `'9'.repeat(exp-1)+'2'`（計算不要）
  - `moRandom()` … 16桁ずつまとめて乱数文字列を作る
- 商品名 = `MORE_ATT[d5] + MORE_SIZE[d4] + sh.mat[d3%len] + MORE_COL[d2] + MORE_PAT[d1] + sh.kind[d0%len].n`
- **セーブ**: 長い番号をそのまま保存すると重いので、24文字超は
  `moreKey(num)` で `ハッシュ.下6桁.桁数` に圧縮（例 `qx0omy1bv7nmz.115827.1400000`）。
  古いセーブは `load()` で自動的に付け替える。109階ぶん買っても **2KB**。
- 画面の状態は `moreBld`（棟）/ `moreShop`（階）/ `moreStart`（ページ先頭番号の文字列）。

### 「もっと売って」への答え方（これまでの流儀）

- 「もっと」×N と言われたら → **N階建ての新しい棟**を建てる。
- 具体的な数字（例「9のあと0が2295個」）を言われたら →
  **その数ぴったりになる**ように階数と `exp` を決める（例: 10^2295 × 9階 = 9×10^2295）。
  必ず Playwright で `BigInt` と突き合わせて桁数・値が一致することをテストする。
- 全体の総数は最大の階でほぼ決まるので、**「小さい追加は総数を変えない」ことは正直に伝える**。

## 5. お金は BigInt

`state.coins` / `savings` / `bankAcct` / `stats.earned` は **BigInt**。
- `big(v)` で正規化、`coinText(n)` で「万/億/兆/京/…/無量大数」表示、
  72桁超は `1.00×10^500（501けた）` 形式。
- 保存時は JSON replacer で `"123n"` の文字列にし、`load()` の `strip()` で戻す。
- テストコードで `JSON.stringify(state)` すると BigInt で落ちるので `String()`/`coinText()` を使う。

## 6. 編集のコツ（実際にハマった罠）

- **Python でアンカー置換**するのが安全。複数行アンカーは失敗しやすいので
  **1行のユニークな文字列**をアンカーにする。`assert s.count(a)==1` を必ず入れる。
  （assert で落ちれば書き込み前に止まるので、ファイルは壊れない）
- 新しい state キーを足したら **必ず `newState()` と `load()` のマイグレーション両方**に足す。
- `SHOP` に品を足すときは **id の重複**に注意（過去に13件重複させた）。
- 新しいフロアの `id` は **109階すべてで重複しない**こと（`state.more[id]` のキーになる）。

## 7. ビルド＆テスト環境

### ビルドスクリプト（`build-artifact.py`）

`pet.html` から Artifact 用 HTML を作る。やっていること:
- `<!DOCTYPE>` `<html>` `<head>` `<body>` を除去（Artifact 側が包むため）
- Tailwind CDN を **手書き CSS シム**に差し替え（`.grid-cols-1〜5` などを自前定義）
- Google Fonts（M PLUS Rounded 1c）の `<link>` を追加
- `#app` に `container-type: inline-size` を付け、ボタン文字の `3.1vw` → `3.1cqw`
  （Artifact 内では `vw` がホスト幅基準になってしまうため）
- 引数2つ: `python3 build-artifact.py <artifact用.html> <preview用.html>`

**スクリプト本体は別ファイル `build-artifact.py` として一緒に渡す。**
新セッションではリポジトリに置くか、この手順を見て作り直せばよい。

### Playwright

```
/opt/node22/lib/node_modules/playwright/index.mjs
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers （インストール不要）
```

毎回見ている項目:
- `pageerror` が 0件
- `body` に横スクロールが出ていないか（スマホ 420px / デスクトップ両方）
- fps（`requestAnimationFrame` を1秒数える）— **62fps が正常**
- ショップの描画時間、巨大番号でのジャンプ／ページ送り／ランダム／購入の所要 ms
- `save()` → `load()` の往復、`localStorage` のサイズ
- `getAllItems()`（ぜんぶもらう）と `shopReset()`

## 8. 今の状態

- 旧リポジトリ `i-tachiiri/tennis-game`
  - ブランチ `claude/pet-raising-game-lhh5vc`（最新 `6ac24ec`）
  - `main` にも 1回マージ済み（`fbc8166`、ただし🐉しろ・🎡ゆうえんち・🐟すいぞくかんの
    3棟は **main 未マージ**、ブランチにだけある）
  - **最新の完成品はブランチの `pet.html`**。これを新リポジトリに持っていくこと。
- Artifact は上記 URL に最新が公開済み。

## 9. 直近やったこと（新しい順）

1. 🐟 すいぞくかん 9階 = ちょうど 9×10^2295 個
2. 🎡 ゆうえんち 10階 = ちょうど 10^1324 個（ビルが 100階ちょうどに）
3. 🐉 でんせつのしろ 9階（10^1400000 まで）＋ 巨大数の高速化（O(1) 化）
4. 🎉 ひろば 3階 = ちょうど 3×10^149 個
5. 🌍 ワールドモール 50階 ＋ **番号を文字列演算に全面移行**（セーブ 491KB→2KB）

## 10. 未対応・気になっていること

- `main` へのマージは 🐉🎡🐟 の3棟ぶんが未反映。ユーザーが「マージして」と言ったら実施。
- `SHOP` 10,000品のうち `deco` 付きは部屋に飾られるが、表示は `DECOR_MAX = 60` 個まで。
- とても長い番号を大量に買うと `localStorage` が一杯になる可能性 →
  `save()` は失敗を catch し、1回だけ「セーブのばしょが いっぱいみたい」と案内する。
