# -*- coding: utf-8 -*-
"""Build a minimal valid EPUB3 from the guide chapters."""
import zipfile, html, re
from pathlib import Path
from markdown import markdown

R = Path(r'D:\SPARK\zcode\朱教授\指南\inner-life-guide-repo')
G = R / 'guide'
OUT = R / "A-Field-Guide-to-Your-Inner-Life.epub"

CHAPTERS = [
    ('00-introduction.md', 'Introduction'),
    ('01-the-inner-life-is-real.md', 'Part I — The inner life is real'),
    ('02-working-with-emotions.md', 'Part II — Working with emotions'),
    ('03-working-with-dreams.md', 'Part III — Working with dreams'),
    ('04-the-house-and-the-people-inside.md', 'Part IV — The house and the people inside'),
    ('05-daily-practice.md', 'Part V — Daily practice and your closest people'),
    ('06-the-edge-of-self-help.md', 'Part VI — The edge of self-help'),
    ('07-sources-and-honesty.md', 'Sources and Honesty'),
]

CSS = """body{font-family:Georgia,serif;line-height:1.6;margin:5%%}
h1{font-size:1.5em}h2{font-size:1.25em;margin-top:1.5em}h3{font-size:1.1em;margin-top:1.2em}
blockquote{border-left:3px solid #999;margin:1em 0;padding:.2em 1em;color:#333}
a{color:#1a0dab}hr{border:none;border-top:1px solid #ccc;margin:2em 0}"""

def to_xhtml(md_text, title):
    # strip nav line
    md_text = re.sub(r'\[← Back to README\]\([^)]*\) · \[Next →\]\([^)]*\)\n', '', md_text)
    # md -> html
    body = markdown(md_text, extensions=['extra'])
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head><meta charset="utf-8"/><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>{body}</body></html>'''

manifest, spine, nav_lis = [], [], []
for i, (fname, title) in enumerate(CHAPTERS, 1):
    md = (G / fname).read_text(encoding='utf-8')
    x = to_xhtml(md, title)
    cid = f'ch{i}'
    (R / '_epub' / f'{cid}.xhtml').parent.mkdir(exist_ok=True)
    (R / '_epub' / f'{cid}.xhtml').write_text(x, encoding='utf-8')
    manifest.append(f'<item id="{cid}" href="{cid}.xhtml" media-type="application/xhtml+xml"/>')
    spine.append(f'<itemref idref="{cid}"/>')
    nav_lis.append(f'<li><a href="{cid}.xhtml">{html.escape(title)}</a></li>')

content_opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en">
<head><meta charset="utf-8"/>
<identifier id="bookid">urn:uuid:6f1e2a3b-7c4d-4e5f-9a8b-0c1d2e3f4a5b</identifier>
<meta name="dcterms:modified" content="2026-10-05T00:00:00Z"/>
<title>A Field Guide to Your Inner Life</title>
<creator>Jinming Shen</creator>
<language>en</language>
</head>
<manifest>
<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="css" href="style.css" media-type="text/css"/>
{''.join(manifest)}
</manifest>
<spine>{''.join(spine)}</spine>
</package>'''

nav = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head><meta charset="utf-8"/><title>Contents</title></head>
<body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>{''.join(nav_lis)}</ol></nav></body></html>'''

container = '''<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'''

OUT.parent.mkdir(exist_ok=True)
if OUT.exists(): OUT.unlink()
with zipfile.ZipFile(OUT, 'w') as z:
    z.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
    z.writestr('META-INF/container.xml', container)
    z.writestr('OEBPS/content.opf', content_opf)
    z.writestr('OEBPS/nav.xhtml', nav)
    z.writestr('OEBPS/style.css', CSS.replace('%%','%'))
    for i, (fname, _) in enumerate(CHAPTERS, 1):
        z.writestr(f'OEBPS/ch{i}.xhtml', (R / '_epub' / f'ch{i}.xhtml').read_text(encoding='utf-8'))
import shutil; shutil.rmtree(R / '_epub', ignore_errors=True)
print('EPUB written:', OUT, OUT.stat().st_size, 'bytes')
