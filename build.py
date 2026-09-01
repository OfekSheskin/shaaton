#!/usr/bin/env python3
"""Wrap the artifact fragment (index.html) into a standalone page at docs/index.html.

index.html is authored for the Claude Artifact runtime, which supplies the
<!doctype>/<head>/<body> skeleton at publish time. GitHub Pages does not, so this
lifts the <title> and the font <link> into a real <head> and adds the viewport,
social-preview and reset rules the runtime would otherwise have provided.
Single source of truth: edit index.html, run this, push.
"""
import io, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://ofeksheskin.github.io/shaaton/"

src = io.open(os.path.join(HERE, "index.html"), encoding="utf-8").read()

title = re.search(r"<title>(.*?)</title>", src).group(1)
fonts = re.findall(r'^<link rel="(?:preconnect|stylesheet)"[^>]*>$', src, re.M)

body = src
body = re.sub(r"^<title>.*?</title>\n", "", body, count=1, flags=re.M)
for tag in fonts:
    body = body.replace(tag + "\n", "", 1)

head = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="בונה מערכות שעות בעברית: סינון לפי קבוצת לימוד, בלוקים בגודל אמיתי לפי אורך השיעור, עריכה בגרירה וייצוא ליומן.">
<meta name="theme-color" content="#0B6B63" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0D1015" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:title" content="{title} — מערכת שעות שאפשר לקרוא">
<meta property="og:description" content="מסננת לקבוצה שלך, מציגה כל שיעור בגובה האמיתי שלו ומחשבת את ההפסקות לבד. עריכה בגרירה, ייצוא ליומן, הדפסה.">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}preview.png">
<meta property="og:locale" content="he_IL">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>%F0%9F%97%93%EF%B8%8F</text></svg>">
{chr(10).join(fonts)}
<style>
  :root{{color-scheme:light dark}}
  html,body{{margin:0}}
  body{{font:14px system-ui,sans-serif}}
  img{{max-width:100%}}
</style>
</head>
<body>
"""

out = os.path.join(HERE, "docs")
os.makedirs(out, exist_ok=True)
io.open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(head + body + "\n</body>\n</html>\n")

preview = os.path.join(HERE, "site", "preview.png")
if os.path.exists(preview):
    shutil.copyfile(preview, os.path.join(out, "preview.png"))

io.open(os.path.join(out, ".nojekyll"), "w").write("")
print("built docs/index.html  (%d KB)" % (os.path.getsize(os.path.join(out, "index.html")) // 1024))
