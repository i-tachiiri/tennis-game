# QR コード

`minitomato-qr.png` … ミニトマトのゲームを ひらく QR コード（いんさつ できる カード）
`minitomato-qr-card.html` … その もとの ページ。ひらいて いんさつ しても いい

## いま どこを さして いるか

```
https://claude.ai/code/artifact/9becdf93-cf02-4b1c-9ebc-78e37d15c834
```

これは **アーティファクト**（claude.ai の ページ）。
じぶんの スマホで、claude.ai に ログイン した じょうたい なら そのまま あそべる。
ともだちに わたす ときは、アーティファクトの がめんの「共有」から
リンクを ひらけるように してから わたす こと。

## だれでも あそべる リンクに したい ときは

1. `minitomato-simple.html` を main ブランチに いれる
2. GitHub の Settings → Pages で、main ブランチを こうかいに する
3. `https://i-tachiiri.github.io/tennis-game/minitomato-simple.html` が つかえるように なる
4. その URL で QR を つくりなおす

## つくりなおしかた

```
pip install segno
python3 -c "import segno; segno.make('<URL>', error='h').save('qr.png', scale=10, border=4)"
```

`minitomato-qr-card.html` の QR（インライン SVG）と いちばん したの URL を
さしかえて、ブラウザで ひらいて スクリーンショットを とる。
