# asobi-games へ 出すもの

`minitomato-sodate.ts` は **`tachiiri-org/asobi-games` の `src/` に置く** ファイル。
この tennis-game リポジトリでは動かない（あそびば側の `./types` を読むため）。
ここに置いてあるのは、作った物を無くさないための控え。

## 置き方

```
cp minitomato-sodate.ts <asobi-games>/src/minitomato-sodate.ts
cd <asobi-games> && npm install && npm run typecheck
```

## 元になったもの

`minitomato-simple.html`（このリポジトリ）。遊びの中身は変えていない。
変えたのは、あそびばの決まりに合わせた6つ。ファイル頭のコメントに書いてある。

- 保存先を `localStorage` から `ctx.save` に移した
- class / id を `ms-` と `data-*` に付け替えた（あそびば側の画面と名前がぶつからない）
- 画面いっぱいの窓を、置き場所の中の `absolute` に変えた
- 外から CSS を読まない（Google Fonts の読み込みをやめた）
- 収穫のたびに `ctx.onFinish` を呼ぶ
- タイマーを全部ひかえて、後片付けで止める

## 点（ランキング）

**とれた かず × あまさ（とうど）** を四捨五入した数。大きいほど良い。
おせわが丁寧だと数も甘さも上がるので、両方が効く。
あそびば側の一覧表には、この説明で載せてほしい。

## まだ 残っていること

あそびばに出すには `front-asobi` 側の一覧表への登録がいる。
どのゲームを出すかは front が決める決まりなので、こちらだけでは画面に出ない。

## 確かめたこと

- `npm run typecheck`（tsc 5.9.3）… エラー 0
- 一度 JS に落として、ダミーの `ctx` で組み立て → みずやり・ひりょう・ひなた／ひかげ・
  せつめいしょ・保存と読み直し・しゅうかく・後片付け まで通し。エラー 0
- わざと `.card` `.btn` `.hidden` を派手に上書きした画面の中に置いても、見た目は崩れない
