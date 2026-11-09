import sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
d=Document(sys.argv[1])
def shade(cell,fill):
    tcPr=cell._tc.get_or_add_tcPr()
    for o in tcPr.findall(qn('w:shd')): tcPr.remove(o)
    sh=OxmlElement('w:shd');sh.set(qn('w:val'),'clear');sh.set(qn('w:color'),'auto');sh.set(qn('w:fill'),fill);tcPr.append(sh)
def margins(cell):
    tcPr=cell._tc.get_or_add_tcPr();m=OxmlElement('w:tcMar')
    for side,v in (('top',70),('bottom',70),('left',100),('right',100)):
        e=OxmlElement('w:'+side);e.set(qn('w:w'),str(v));e.set(qn('w:type'),'dxa');m.append(e)
    tcPr.append(m)
for t in d.tables:
    tblPr=t._tbl.tblPr
    for o in tblPr.findall(qn('w:tblBorders')): tblPr.remove(o)
    b=OxmlElement('w:tblBorders')
    for side in ('top','bottom','insideH'):
        e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'CBD5E1');b.append(e)
    for side in ('left','right','insideV'):
        e=OxmlElement('w:'+side);e.set(qn('w:val'),'nil');b.append(e)
    tblPr.append(b)
    w=tblPr.find(qn('w:tblW'))
    if w is None: w=OxmlElement('w:tblW');tblPr.append(w)
    w.set(qn('w:w'),'5000');w.set(qn('w:type'),'pct')
    for i,row in enumerate(t.rows):
        for c in row.cells:
            margins(c)
            if i==0: shade(c,'0F172A')
            elif i%2==0: shade(c,'F8FAFC')
            for p in c.paragraphs:
                p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1.1
                for r in p.runs:
                    r.font.size=Pt(9.5)
                    if i==0: r.font.color.rgb=RGBColor(255,255,255);r.font.bold=True
        if i==0:
            trPr=row._tr.get_or_add_trPr();h=OxmlElement('w:tblHeader');trPr.append(h)
        trPr=row._tr.get_or_add_trPr();cs=OxmlElement('w:cantSplit');trPr.append(cs)
# footer page numbers
sec=d.sections[0];p=sec.footer.paragraphs[0] if sec.footer.paragraphs else sec.footer.add_paragraph()
p.alignment=2
r=p.add_run('KINO · Roadmap, estrategia y presupuesto · ');r.font.size=Pt(8.5);r.font.color.rgb=RGBColor(0x64,0x74,0x8B)
r=p.add_run();r.font.size=Pt(8.5)
for tag,txt in (('begin',None),(None,'PAGE'),('end',None)):
    if tag:
        f=OxmlElement('w:fldChar');f.set(qn('w:fldCharType'),tag);r._r.append(f)
    else:
        it=OxmlElement('w:instrText');it.set(qn('xml:space'),'preserve');it.text=txt;r._r.append(it)
d.save(sys.argv[1]);print('post ok',len(d.tables))
