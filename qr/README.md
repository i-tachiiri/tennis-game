# QR コード

`minitomato-qr.png` … ミニトマトのゲームを ひらく QR コード（いんさつ できる カード）
`minitomato-qr-card.html` … その もとの ページ。ひらいて いんさつ しても いい

## さして いる さき

```
https://asobi.tachiiri.com/play/minitomato-sodate
```

あそびばに おいてある ミニトマトの ゲーム。

## つくりなおしかた

```
pip install segno
python3 -c "import segno; segno.make('<URL>', error='h').save('qr.png', scale=10, border=4)"
```

`minitomato-qr-card.html` の なかの QR（インライン SVG）と、いちばん したの
URL を さしかえて、ブラウザで ひらいて スクリーンショットを とる。

## たしかめかた

QR の なかみは、じっさいに よみとって たしかめる。

```
pip install opencv-python-headless
python3 -c "import cv2; print(cv2.QRCodeDetector().detectAndDecode(cv2.imread('minitomato-qr.png'))[0])"
```
