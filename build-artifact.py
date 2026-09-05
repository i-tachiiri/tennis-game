# つかいかた: python3 build-artifact.py <artifact用.html> <preview用.html> [pet.html のパス]
import sys, os
SRC = sys.argv[3] if len(sys.argv) > 3 else 'pet.html'
src = open(SRC, encoding='utf-8').read()
for tag in ['<!DOCTYPE html>\n', '<html lang="ja">\n', '<head>\n', '<meta charset="UTF-8">\n',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">\n',
            '</head>\n', '<body>\n', '</body>\n', '</html>\n']:
    src = src.replace(tag, '', 1)
FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;800&display=swap">\n'
src = src.replace('<script src="https://cdn.tailwindcss.com"></script>\n', FONT, 1)
SHIM = """
    /* --- Tailwind で使っていたユーティリティだけを自前で用意 --- */
    * { box-sizing: border-box; }
    .flex { display: flex; }
    .justify-between { justify-content: space-between; }
    .items-center { align-items: center; }
    .grid { display: grid; }
    .grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .grid-cols-5 { grid-template-columns: repeat(5, minmax(0, 1fr)); }
    .grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    .gap-1 { gap: 0.25rem; }
    .gap-2 { gap: 0.5rem; }
    .gap-x-3 { column-gap: 0.75rem; }
    .gap-y-1 { row-gap: 0.25rem; }
    .p-2 { padding: 0.5rem; }
    .p-3 { padding: 0.75rem; }
    .px-1 { padding-left: 0.25rem; padding-right: 0.25rem; }
    .px-3 { padding-left: 0.75rem; padding-right: 0.75rem; }
    .py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
    .mb-1 { margin-bottom: 0.25rem; }
    .mb-2 { margin-bottom: 0.5rem; }
    .mb-3 { margin-bottom: 0.75rem; }
    .mb-4 { margin-bottom: 1rem; }
    .mt-1 { margin-top: 0.25rem; }
    .mt-2 { margin-top: 0.5rem; }
    .mt-3 { margin-top: 0.75rem; }
    .mt-4 { margin-top: 1rem; }
    .my-2 { margin-top: 0.5rem; margin-bottom: 0.5rem; }
    .w-full { width: 100%; }
    .font-bold { font-weight: 800; }
    .text-2xl { font-size: 1.5rem; line-height: 2rem; }
    .text-lg { font-size: 1.125rem; line-height: 1.75rem; }
    .text-sm { font-size: 0.875rem; line-height: 1.35rem; }
    .text-xs { font-size: 0.75rem; line-height: 1.1rem; }
    .leading-6 { line-height: 1.6rem; }
    .text-left { text-align: left; }
    .text-center { text-align: center; }
    .text-amber-700 { color: #b45309; }
    .text-gray-600 { color: #4b5563; }
    .text-gray-500 { color: #6b7280; }
    .border-2 { border-width: 2px; border-style: solid; }
    .border-amber-700 { border-color: #b45309; }
    .rounded-lg { border-radius: 0.5rem; }
    hr { border: none; border-top: 2px dotted #d6c7a8; }
    input { font: inherit; color: inherit; background: #fff; }
    .game-btn:focus-visible, input:focus-visible {
        outline: 3px solid #38bdf8;
        outline-offset: 2px;
    }
    @media (prefers-reduced-motion: reduce) {
        .bar-inner { transition: none; }
    }
"""
src = src.replace("<style>\n", "<style>" + SHIM, 1)
src = src.replace(
    "font-family: 'Hiragino Maru Gothic ProN', 'Arial Rounded MT Bold', 'Arial', sans-serif;",
    "font-family: 'M PLUS Rounded 1c', 'Hiragino Maru Gothic ProN', 'Arial Rounded MT Bold', 'Arial', sans-serif;")
# Artifact 内では vw がホスト幅基準になるため、ボタン文字はコンテナ基準にする
src = src.replace("font-size: clamp(0.72rem, 3.1vw, 0.95rem);", "font-size: clamp(0.72rem, 3.1cqw, 0.95rem);")
src = src.replace("#app {\n        max-width: 480px;", "#app {\n        container-type: inline-size;\n        max-width: 480px;")
open(sys.argv[1], 'w', encoding='utf-8').write(src)
wrapped = '<!doctype html>\n<html>\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<style>*{margin:0;padding:0}</style>\n</head>\n<body>\n' + src + '\n</body>\n</html>\n'
open(sys.argv[2], 'w', encoding='utf-8').write(wrapped)
print('built')
