"""Build the downloadable manual from the same content and images as the website.

Requires reportlab. Run from any directory: python scripts/build-manual.py
"""
import hashlib
import json
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'src/data/manual.json'
DATA = json.loads(SOURCE.read_text(encoding='utf-8'))
OUT = ROOT / 'public/manual/LAFINA-User-Manual.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
W, H = A4
M = 44
INK = colors.HexColor('#0f172a')
MUTED = colors.HexColor('#475569')
INDIGO = colors.HexColor('#4f46e5')
LINE = colors.HexColor('#dce1ec')
SURFACE = colors.HexColor('#f5f6fc')
C = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
C.setTitle(DATA['title'])
C.setAuthor('LAFINA')
C.setSubject('Illustrated Android user manual with linked contents')


def clean(text):
    return text.translate(str.maketrans({'\u2014': ' - ', '\u2013': '-', '\u2011': '-', '\u2019': "'", '\u2018': "'", '\u201c': '"', '\u201d': '"', '\u00b7': '|', '\u2026': '...'}))


def paragraph(text, x, y, width, size=10.5, leading=None, color=INK, bold=False):
    style = ParagraphStyle('body', fontName='Helvetica-Bold' if bold else 'Helvetica', fontSize=size, leading=leading or size * 1.48, textColor=color, alignment=TA_LEFT, spaceAfter=0)
    p = Paragraph(text, style)
    _, height = p.wrap(width, H)
    p.drawOn(C, x, y - height)
    return y - height


def text(text):
    return escape(clean(text))


def rule(y):
    C.setStrokeColor(LINE)
    C.setLineWidth(.6)
    C.line(M, y, W - M, y)


def footer(page):
    rule(40)
    C.setFont('Helvetica', 8)
    C.setFillColor(MUTED)
    C.drawString(M, 25, 'LAFINA User Manual | ' + DATA['edition'])
    C.drawRightString(W - M, 25, str(page))
    if page > 3:
        C.setFillColor(INDIGO)
        C.drawCentredString(W / 2, 25, 'Back to contents')
        C.linkRect('', 'contents', (W / 2 - 45, 20, W / 2 + 45, 35), relative=0, thickness=0)


# Page 1: cover and orientation.
C.setFillColor(INDIGO)
C.rect(0, H - 14, W, 14, fill=1, stroke=0)
paragraph('LAFINA / ANDROID USER GUIDE', M, H - 65, W - 2 * M, 10, color=INDIGO, bold=True)
paragraph('Your day,<br/>with a little guidance.', M, H - 130, W - 2 * M, 33, 39, bold=True)
paragraph('User Manual', M, H - 245, W - 2 * M, 22, color=INDIGO, bold=True)
paragraph(text(DATA['edition']), M, H - 288, W - 2 * M, 11, color=MUTED)
rule(H - 325)
y = paragraph(text(DATA['introduction']), M, H - 350, W - 2 * M, 12, 18)
steps_count = sum(len(c['steps']) for c in DATA['chapters'])
image_count = sum(bool(s.get('image')) for c in DATA['chapters'] for s in c['steps'])
y = paragraph(f"{len(DATA['chapters'])} topics | {steps_count} steps | {image_count} app screenshots", M, y - 22, W - 2 * M, 10, color=INDIGO, bold=True)
y = paragraph('How to use this manual', M, y - 42, W - 2 * M, 13, bold=True)
y = paragraph('Start with Getting started, or use the linked table of contents to jump to a task. Each step explains what to do, what to expect, and any details to check before continuing. Screenshots are illustrative; enter your own information.', M, y - 12, W - 2 * M)
y = paragraph('About this edition', M, y - 28, W - 2 * M, 13, bold=True)
paragraph(text(DATA['scope']), M, y - 12, W - 2 * M, 9.5, color=MUTED)
footer(1)
C.showPage()

# Fixed one-step pages make the PDF contents page numbers exact and reproducible.
page_for = {}
page = 4
for chapter in DATA['chapters']:
    for step in chapter['steps']:
        page_for[f"{chapter['slug']}-{step['id']}"] = page
        page += 1

for contents_index, chapters in enumerate((DATA['chapters'][:7], DATA['chapters'][7:])):
    if contents_index == 0:
        C.bookmarkPage('contents')
        C.addOutlineEntry('Table of contents', 'contents', level=0)
    y = paragraph('Table of contents' + (' / continued' if contents_index else ''), M, H - 55, W - 2 * M, 23, bold=True)
    y = paragraph('Select a topic or step to jump to its page.', M, y - 12, W - 2 * M, 9, color=MUTED) - 22
    for chapter in chapters:
        index = DATA['chapters'].index(chapter)
        first_key = f"{chapter['slug']}-{chapter['steps'][0]['id']}"
        paragraph(f"{index + 1:02d}  {text(chapter['title'])}", M, y, W - 2 * M - 34, 11, bold=True, color=INDIGO)
        C.setFont('Helvetica-Bold', 10)
        C.setFillColor(INDIGO)
        C.drawRightString(W - M, y - 11, str(page_for[first_key]))
        C.linkRect('', 'chapter-' + chapter['slug'], (M, y - 17, W - M, y + 2), relative=0, thickness=0)
        y -= 24
        for step_index, step in enumerate(chapter['steps']):
            key = f"{chapter['slug']}-{step['id']}"
            top = y
            y = paragraph(f"{step_index + 1}. {text(step['title'])}", M + 18, y, W - 2 * M - 55, 8.6, 12, color=MUTED)
            C.setFont('Helvetica', 8.6)
            C.drawRightString(W - M, top - 9, str(page_for[key]))
            C.linkRect('', key, (M + 18, y - 2, W - M, top + 2), relative=0, thickness=0)
            y -= 4
        y -= 12
    if y < 60:
        raise ValueError('Table of contents overflow; adjust the contents split.')
    footer(contents_index + 2)
    C.showPage()

for chapter_index, chapter in enumerate(DATA['chapters']):
    for step_index, step in enumerate(chapter['steps']):
        key = f"{chapter['slug']}-{step['id']}"
        page = page_for[key]
        C.bookmarkPage(key)
        if step_index == 0:
            C.bookmarkPage('chapter-' + chapter['slug'])
            C.addOutlineEntry(chapter['title'], 'chapter-' + chapter['slug'], level=0)
        C.addOutlineEntry(step['title'], key, level=1)
        paragraph(f"CHAPTER {chapter_index + 1:02d} / {text(chapter['group']).upper()}", M, H - 49, W - 2 * M, 8, color=INDIGO, bold=True)
        y = paragraph(text(chapter['title']), M, H - 72, W - 2 * M, 19, 24, bold=True)
        rule(y - 15)
        y = paragraph(f"STEP {step_index + 1:02d} OF {len(chapter['steps']):02d}", M, y - 34, W - 2 * M, 8, color=INDIGO, bold=True)
        y = paragraph(text(step['title']), M, y - 13, W - 2 * M, 16, 21, bold=True) - 22
        top = y
        image = step.get('image')
        image_width = 198
        width = W - 2 * M - image_width - 25 if image else W - 2 * M
        if step_index == 0:
            y = paragraph('BEFORE YOU BEGIN', M, y, width, 8, color=INDIGO, bold=True)
            y = paragraph(text(chapter['before']), M, y - 7, width, 9, 13, color=MUTED) - 18
        for instruction_index, instruction in enumerate(step['instructions']):
            y = paragraph(f"<b>{instruction_index + 1}.</b>  {text(instruction)}", M, y, width, 10, 14.5) - 13
        y = paragraph('WHAT TO EXPECT', M, y - 3, width, 8, color=INDIGO, bold=True)
        y = paragraph(text(step['result']), M, y - 7, width, 9.5, 14, color=MUTED)
        if step.get('note'):
            y = paragraph('KEEP IN MIND', M, y - 22, width, 8, color=INDIGO, bold=True)
            y = paragraph(text(step['note']), M, y - 7, width, 9, 13, color=MUTED)
        if y < 62:
            raise ValueError(f'Text overflows page {page}: {key} (bottom={y:.1f})')
        if image:
            image_path = ROOT / 'public/manual/screenshots' / image['file']
            reader = ImageReader(str(image_path))
            iw, ih = reader.getSize()
            image_height = image_width * ih / iw
            # Long Home capture is scaled to stay above its caption and footer.
            image_height = min(image_height, top - 115)
            image_width_actual = image_height * iw / ih
            x = W - M - image_width + (image_width - image_width_actual) / 2
            C.drawImage(reader, x, top - image_height, width=image_width_actual, height=image_height)
            C.setStrokeColor(LINE)
            C.rect(x, top - image_height, image_width_actual, image_height, stroke=1, fill=0)
            bottom = paragraph(text(image['caption']), W - M - image_width, top - image_height - 12, image_width, 8, 11, color=MUTED)
            if bottom < 60:
                raise ValueError(f'Image caption overflows page {page}: {key}')
        footer(page)
        C.showPage()

C.save()
metadata = {
    'sourceHash': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'pdfHash': hashlib.sha256(OUT.read_bytes()).hexdigest(),
    'chapters': len(DATA['chapters']), 'steps': steps_count,
    'screenshots': sum(bool(s.get('image')) for c in DATA['chapters'] for s in c['steps']),
    'pages': page,
    'screenshotHashes': {
        s['image']['file']: hashlib.sha256((OUT.parent / 'screenshots' / s['image']['file']).read_bytes()).hexdigest()
        for c in DATA['chapters'] for s in c['steps'] if s.get('image')
    },
}
(OUT.parent / 'manual-meta.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
print(f"Built {OUT.name}: {page} pages with linked contents and chapter/step bookmarks.")
