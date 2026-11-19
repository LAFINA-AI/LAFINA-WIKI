"""Create an editable Word manual from the website's canonical content.

Requires python-docx. Run: python scripts/build-manual-docx.py
"""
import hashlib
import json
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Mm, Pt, RGBColor
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'src/data/manual.json'
DATA = json.loads(SOURCE.read_text(encoding='utf-8'))
OUT = ROOT / 'public/manual/LAFINA-User-Manual.docx'
DOC = Document()
DOC.core_properties.title = DATA['title']
DOC.core_properties.subject = 'Illustrated Android user manual'
DOC.core_properties.author = 'LAFINA'
DOC.core_properties.keywords = 'LAFINA, Android, user manual'
DOC.core_properties.comments = ''
BLACK = RGBColor.from_string('000000')
MUTED = RGBColor.from_string('475569')
INDIGO = RGBColor.from_string('4F46E5')


def clean(value):
    return value.translate(str.maketrans({'\u2014': ' - ', '\u2013': '-', '\u2011': '-', '\u2019': "'", '\u2018': "'", '\u201c': '"', '\u201d': '"', '\u00b7': '|', '\u2026': '...'}))


for name in ['Normal', 'Title', 'Subtitle', 'Heading 1', 'Heading 2', 'Heading 3', 'Caption']:
    style = DOC.styles[name]
    style.font.name = 'Arial'
    style.font.color.rgb = BLACK
    style.font.size = Pt(10.5)
    style.paragraph_format.space_after = Pt(8)
    style.paragraph_format.line_spacing = 1.12
for name, size in [('Title', 32), ('Heading 1', 18), ('Heading 2', 14), ('Heading 3', 11)]:
    DOC.styles[name].font.size = Pt(size)
    DOC.styles[name].font.bold = True
    DOC.styles[name].paragraph_format.keep_with_next = True
DOC.styles['Caption'].font.size = Pt(8)
DOC.styles['Caption'].font.color.rgb = MUTED
DOC.styles['Caption'].font.italic = False
DOC.styles['Caption'].paragraph_format.keep_with_next = False


def setup(section, illustrated=False):
    section.page_width, section.page_height = Mm(210), Mm(297)
    section.top_margin, section.bottom_margin = Inches(.65), Inches(.6)
    section.left_margin = section.right_margin = Inches(.65)
    section.header_distance = section.footer_distance = Inches(.28)
    cols = section._sectPr.find(qn('w:cols'))
    for child in list(cols):
        cols.remove(child)
    cols.set(qn('w:num'), '2' if illustrated else '1')
    cols.set(qn('w:equalWidth'), '0' if illustrated else '1')
    if illustrated:
        for width, gap in [(5520, 450), (4064, 0)]:
            col = OxmlElement('w:col')
            col.set(qn('w:w'), str(width))
            col.set(qn('w:space'), str(gap))
            cols.append(col)


def section(illustrated=False):
    result = DOC.add_section(WD_SECTION_START.NEW_PAGE)
    setup(result, illustrated)
    # python-docx's section delimiter is an empty paragraph; keep it compact.
    for p in [DOC.paragraphs[-1]]:
        p.paragraph_format.space_before = p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(1)
        p.add_run().font.size = Pt(1)
    return result


def para(value, style=None, size=None, bold=False, color=None, after=8):
    p = DOC.add_paragraph(style=style)
    p.paragraph_format.space_after = Pt(after)
    r = p.add_run(clean(value))
    if size:
        r.font.size = Pt(size)
    if bold:
        r.bold = True
    if color:
        r.font.color.rgb = color
    return p


bookmark_id = 0


def bookmark(p, name):
    global bookmark_id
    bookmark_id += 1
    start, end = OxmlElement('w:bookmarkStart'), OxmlElement('w:bookmarkEnd')
    start.set(qn('w:id'), str(bookmark_id))
    start.set(qn('w:name'), name)
    end.set(qn('w:id'), str(bookmark_id))
    p._p.insert(0, start)
    p._p.append(end)


def link(p, label, target, size=10, bold=False):
    h = OxmlElement('w:hyperlink')
    h.set(qn('w:anchor'), target)
    h.set(qn('w:history'), '1')
    r, props, t = OxmlElement('w:r'), OxmlElement('w:rPr'), OxmlElement('w:t')
    c, sz = OxmlElement('w:color'), OxmlElement('w:sz')
    c.set(qn('w:val'), '4F46E5')
    sz.set(qn('w:val'), str(int(size * 2)))
    props.extend([c, sz])
    if bold:
        props.append(OxmlElement('w:b'))
    r.append(props)
    t.text = clean(label)
    r.append(t)
    h.append(r)
    p._p.append(h)


def page_field(p):
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'), 'PAGE')
    r, t = OxmlElement('w:r'), OxmlElement('w:t')
    t.text = '1'
    r.append(t)
    field.append(r)
    p._p.append(field)


def page_reference(p, target, page, size):
    p.add_run('\t')
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'), f'PAGEREF {target} \\h')
    r, props, sz, t = OxmlElement('w:r'), OxmlElement('w:rPr'), OxmlElement('w:sz'), OxmlElement('w:t')
    sz.set(qn('w:val'), str(int(size * 2)))
    props.append(sz)
    r.append(props)
    t.text = str(page)
    r.append(t)
    field.append(r)
    p._p.append(field)


setup(DOC.sections[0])
footer = DOC.sections[0].footer.paragraphs[0]
footer.paragraph_format.tab_stops.add_tab_stop(Inches(6.95), WD_TAB_ALIGNMENT.RIGHT)
footer.add_run('LAFINA User Manual | ' + DATA['edition'] + '\t').font.size = Pt(8)
page_field(footer)

title = para(DATA['title'], 'Title', after=14)
title.paragraph_format.space_before = Pt(54)
para('Android user guide', 'Subtitle', size=15, after=12)
para(DATA['edition'], size=11, color=MUTED, after=28)
para(DATA['introduction'], size=12, after=22)
steps = sum(len(c['steps']) for c in DATA['chapters'])
images = sum(bool(s.get('image')) for c in DATA['chapters'] for s in c['steps'])
para(f"{len(DATA['chapters'])} topics | {steps} steps | {images} screenshots", color=INDIGO, bold=True, after=30)
para('How to use this manual', 'Heading 2')
para('Start with Getting started or use the linked table of contents to jump to a task. Each step explains what to do, what to expect, and what to check. Screenshots illustrate the Android app; enter your own information.')
para('About this edition', 'Heading 2')
para(DATA['scope'], size=10)

page_for = {}
page = 4
for ci, chapter in enumerate(DATA['chapters']):
    for si, step in enumerate(chapter['steps']):
        page_for[(ci, si)] = page
        page += 1

for toc_index, chapters in enumerate([DATA['chapters'][:7], DATA['chapters'][7:]]):
    section()
    p = para('Table of contents' if toc_index == 0 else 'Table of contents continued', 'Heading 1', after=10)
    if toc_index == 0:
        bookmark(p, 'ManualContents')
    para('Select a topic or step to jump to its page.', size=9, color=MUTED, after=14)
    for chapter in chapters:
        ci = DATA['chapters'].index(chapter)
        p = DOC.add_paragraph()
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.tab_stops.add_tab_stop(Inches(6.9), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        link(p, f"{ci + 1:02d} {chapter['title']}", f'Chapter{ci + 1}', size=10, bold=True)
        page_reference(p, f'Chapter{ci + 1}', page_for[(ci, 0)], 9)
        for si, step in enumerate(chapter['steps']):
            p = DOC.add_paragraph()
            p.paragraph_format.left_indent = Inches(.2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1
            p.paragraph_format.tab_stops.add_tab_stop(Inches(6.7), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
            link(p, f"{si + 1} {step['title']}", f'Step{ci + 1}_{si + 1}', size=8.5)
            page_reference(p, f'Step{ci + 1}_{si + 1}', page_for[(ci, si)], 8.5)

for ci, chapter in enumerate(DATA['chapters']):
    for si, step in enumerate(chapter['steps']):
        image = step.get('image')
        section(bool(image))
        para(f"CHAPTER {ci + 1:02d} | {chapter['group']}", size=8, bold=True, after=10)
        if si == 0:
            p = para(chapter['title'], 'Heading 1', after=13)
            bookmark(p, f'Chapter{ci + 1}')
        else:
            para(chapter['title'], size=15, bold=True, after=13)
        para(f"STEP {si + 1:02d} OF {len(chapter['steps']):02d}", size=8, color=INDIGO, bold=True, after=7)
        p = para(step['title'], 'Heading 2', after=13)
        bookmark(p, f'Step{ci + 1}_{si + 1}')
        if si == 0:
            p = para('Before you begin', bold=True, size=9, after=4)
            p.paragraph_format.keep_with_next = True
            para(chapter['before'], size=9, color=MUTED, after=14)
        for index, instruction in enumerate(step['instructions']):
            p = DOC.add_paragraph()
            p.paragraph_format.left_indent = Inches(.18)
            p.paragraph_format.first_line_indent = Inches(-.18)
            p.add_run(f'{index + 1}. ').bold = True
            p.add_run(clean(instruction))
            p.paragraph_format.space_after = Pt(10)
        p = para('What to expect', bold=True, size=9, after=4)
        p.paragraph_format.keep_with_next = True
        para(step['result'], size=9.5, color=MUTED, after=13)
        if step.get('note'):
            p = para('Keep in mind', bold=True, size=9, after=4)
            p.paragraph_format.keep_with_next = True
            para(step['note'], size=9, color=MUTED, after=13)
        p = DOC.add_paragraph()
        link(p, 'Back to contents', 'ManualContents', size=8)
        if image:
            p = DOC.add_paragraph()
            p.add_run().add_break(WD_BREAK.COLUMN)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = Pt(1)
            p.add_run().font.size = Pt(1)
            p = DOC.add_paragraph()
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_after = Pt(7)
            path = ROOT / 'public/manual/screenshots' / image['file']
            with Image.open(path) as im:
                iw, ih = im.size
            width = min(2.65, 7.65 * iw / ih)
            pic = p.add_run().add_picture(str(path), width=Inches(width))
            pic._inline.docPr.set('descr', image['alt'])
            pic._inline.docPr.set('title', image['caption'])
            para(image['caption'], 'Caption', after=0)

OUT.parent.mkdir(parents=True, exist_ok=True)
# The base Word template can carry a theme rule under Title. Use typography
# and whitespace consistently instead of inheriting paragraph borders.
for root in (DOC.styles.element, DOC.element):
    for border in root.xpath('.//w:pBdr'):
        border.getparent().remove(border)
DOC.save(OUT)
meta = {
    'sourceHash': hashlib.sha256(SOURCE.read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
    'docxHash': hashlib.sha256(OUT.read_bytes()).hexdigest(),
    'chapters': len(DATA['chapters']), 'steps': steps, 'screenshots': images,
    'screenshotHashes': {
        s['image']['file']: hashlib.sha256((OUT.parent / 'screenshots' / s['image']['file']).read_bytes()).hexdigest()
        for c in DATA['chapters'] for s in c['steps'] if s.get('image')
    },
}
(OUT.parent / 'docx-meta.json').write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8')
print(f'Created {OUT.name} with {steps} editable steps, {images} embedded screenshots, and linked contents.')
