from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
d=Document('ref.docx')
S={s.name:s for s in d.styles}
INK=RGBColor(0x0F,0x17,0x2A);AC=RGBColor(0x1D,0x4E,0xD8);MUT=RGBColor(0x64,0x74,0x8B);TXT=RGBColor(0x33,0x41,0x55)
def font(st,name='Calibri',size=None,color=None,bold=None):
    f=st.font;f.name=name
    rpr=st.element.get_or_add_rPr();rf=rpr.find(qn('w:rFonts'))
    if rf is None: rf=OxmlElement('w:rFonts');rpr.append(rf)
    for a in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'): rf.set(qn(a),name)
    for a in ('w:asciiTheme','w:hAnsiTheme','w:cstheme','w:eastAsiaTheme'):
        if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
    if size: f.size=Pt(size)
    if color is not None: f.color.rgb=color
    if bold is not None: f.bold=bold
for n in ['Normal','Body Text','First Paragraph','Compact']:
    font(S[n],size=11,color=TXT);pf=S[n].paragraph_format;pf.space_after=Pt(8);pf.line_spacing=1.2
S['Compact'].paragraph_format.space_after=Pt(2);S['Compact'].paragraph_format.line_spacing=1.1
font(S['Title'],size=44,color=INK,bold=True);S['Title'].paragraph_format.space_before=Pt(170);S['Title'].paragraph_format.alignment=0
font(S['Subtitle'],size=20,color=AC);S['Subtitle'].paragraph_format.alignment=0;S['Subtitle'].paragraph_format.space_after=Pt(60)
for n in ['Author','Date']: font(S[n],size=12,color=MUT);S[n].paragraph_format.alignment=0
h1=S['Heading 1'];font(h1,size=24,color=INK,bold=True);h1.paragraph_format.space_before=Pt(0);h1.paragraph_format.space_after=Pt(14);h1.paragraph_format.page_break_before=True
h2=S['Heading 2'];font(h2,size=14,color=AC,bold=True);h2.paragraph_format.space_before=Pt(18);h2.paragraph_format.space_after=Pt(6);h2.paragraph_format.keep_with_next=True
font(S['Heading 3'],size=12,color=INK,bold=True)
for n in ['Image Caption','Caption','Table Caption']:
    font(S[n],size=9.5,color=MUT);S[n].font.italic=False;S[n].paragraph_format.space_after=Pt(16)
S['Captioned Figure'].paragraph_format.keep_with_next=True
bt=S['Block Text'];font(bt,size=11.5,color=INK)
pf=bt.paragraph_format;pf.left_indent=Cm(0.3);pf.right_indent=Cm(0.3);pf.space_before=Pt(8);pf.space_after=Pt(14)
ppr=bt.element.get_or_add_pPr()
for old in ppr.findall(qn('w:pBdr'))+ppr.findall(qn('w:shd')): ppr.remove(old)
bd=OxmlElement('w:pBdr')
for side in ('top','left','bottom','right'):
    e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'24' if side=='left' else '4');e.set(qn('w:space'),'8');e.set(qn('w:color'),'1D4ED8' if side=='left' else 'EFF4FF');bd.append(e)
ppr.append(bd)
sh=OxmlElement('w:shd');sh.set(qn('w:val'),'clear');sh.set(qn('w:color'),'auto');sh.set(qn('w:fill'),'EFF4FF');ppr.append(sh)
font(S['TOC Heading'],size=24,color=INK,bold=True)
S['Hyperlink'].font.color.rgb=AC
sec=d.sections[0];sec.left_margin=sec.right_margin=Cm(2.3);sec.top_margin=sec.bottom_margin=Cm(2.2)
d.save('ref.docx');print('ref ok')
