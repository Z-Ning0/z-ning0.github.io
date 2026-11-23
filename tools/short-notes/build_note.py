"""Generate a note and its card into an existing isolated site copy; never publish."""
from argparse import ArgumentParser
from html import escape
from pathlib import Path
import importlib
import json
import re
import sys
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from markdown_it import MarkdownIt

ORIGIN='https://ningcraft.com/'
MD=MarkdownIt('commonmark',{'html':False})
INK='#201e17'; PAPER='#fbfaf6'; QUIET='#625e53'; GOLD='#d9a20c'
FONT=Path('C:/Windows/Fonts')

def markdown(raw):
    # The site blocks arbitrary raw HTML. Only the historical details/summary pair is lifted.
    parts=re.split(r'<details>\s*<summary>([^<>\r\n]+)</summary>\s*(.*?)\s*</details>',raw,flags=re.S)
    if any(re.search(r'</?(?:details|summary)\b',chunk,re.I) for chunk in parts[::3]):
        raise ValueError('unmatched or unsupported details/summary markup')
    rendered=MD.render(parts[0]); details=[]
    for i in range(1,len(parts),3):
        question,inner=parts[i:i+2]; details.append((question,inner))
        rendered+=f'<details><summary>{escape(question)}</summary>\n{MD.render(inner)}</details>\n'+MD.render(parts[i+2])
    return rendered,details

def safe_path(slug):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError('slug must use lowercase letters, digits and hyphens')
    return f'notes/{slug}/'

def clean(s):return re.sub(r'\s+',' ',s).strip()

def card(title, byline, site, excerpt=None):
    im=Image.new('RGB',(1200,630),PAPER);d=ImageDraw.Draw(im)
    d.rectangle((0,0,1199,8),fill=GOLD)
    heavy=lambda n:ImageFont.truetype(str(FONT/'msyhbd.ttc'),n)
    plain=lambda n:ImageFont.truetype(str(FONT/'msyh.ttc'),n)
    mono=ImageFont.truetype(str(FONT/'consola.ttf'),36)
    d.text((82,76),byline,font=heavy(33),fill=QUIET)
    d.line((82,144,1118,144),fill='#d7cfbd',width=2)
    width=535 if excerpt else 1025
    for size in (72,64,56,48,42,36):
        f=heavy(size); rows=[]; row=''
        for ch in title:
            if row and f.getlength(row+ch)>width:rows.append(row);row=''
            row+=ch
        if row:rows.append(row)
        if len(rows)<=3:break
    else:raise ValueError('title is too long for the share image')
    y=212 if len(rows)>1 else 245
    for row in rows:
        d.text((82,y),row,font=f,fill=INK,anchor='lt'); y+=size+22
    if excerpt:
        label, example=excerpt
        d.rectangle((650,179,1118,500),fill='#f2eedf');d.rectangle((650,179,655,500),fill=GOLD)
        d.text((684,211),label,font=heavy(30),fill=QUIET)
        d.line((684,258,1082,258),fill='#d7cfbd',width=2)
        for i,line in enumerate(example.splitlines()):
            if i>=4 or mono.getlength(line)>400:raise ValueError('card example needs at most four short lines')
            d.text((684,279+i*46),line,font=mono,fill=INK,anchor='lt')
    with Image.open(site/'favicon.ico') as logo:
        mark=logo.ico.getimage((48,48)).convert('RGBA');im.paste(mark,(79,535),mark)
    d.text((135,541),'阿柠',font=plain(29),fill=QUIET)
    buf=BytesIO();im.save(buf,format='PNG',optimize=True);return buf.getvalue()

def compile_note(args):
    raw=args.markdown.read_text(encoding='utf-8-sig')
    lines=raw.splitlines()
    if not lines or not lines[0].startswith('# ') or not lines[0][2:].strip():raise ValueError('Markdown must start with a # title')
    title=lines[0][2:].strip(); content='\n'.join(lines[1:]); url=safe_path(args.slug)
    if not args.output.is_dir():raise ValueError('output must be an existing isolated site directory')
    if not (args.output/'assets/site.css').is_file():raise ValueError('missing base site stylesheet')
    if (args.output/url/'index.html').exists() and not args.replace_existing:
        raise ValueError('note already exists; use --replace-existing only for an intentional revision')
    byline=clean(args.byline)
    if not byline or len(byline)>34:raise ValueError('byline must be 1 to 34 characters')
    rendered,details=markdown(content)
    tokens=MD.parse(content)
    first=next((t.content for t in tokens if t.type=='inline'),title)
    description=clean(re.sub(r'[`*_]','',first))[:145] or title
    feature=None
    if args.experiment:
        if len(details)!=1:raise ValueError('experiment mode requires exactly one question disclosure')
        question,answer=details[0]
        example=next((t.content.rstrip('\n') for t in tokens if t.type=='fence' and t.info.strip()=='text'),None)
        result=next((t.content.rstrip('\n') for t in MD.parse(answer) if t.type=='fence' and t.info.strip()=='text'),None)
        if not example or not result:raise ValueError('experiment mode needs a text sample and a text result inside details')
        feature=dict(url=url,title=title,byline=byline,question=question,example_label=args.example_label,example=example,output=result)
        description=question
    sys.path.insert(0,str(args.generator))
    build_site=importlib.import_module('build_site')
    image_path=url+'share.png'
    header=build_site.head(title+' · 阿柠',description,root='../../',ogtype='article',og=image_path)
    header=header.replace('</head>',f'<meta property="og:image:alt" content="{escape(description)}">\n<style>.note details{{margin:1.25em 0;padding:14px 16px;border:1px solid var(--line)}} .note summary{{cursor:pointer;color:var(--lemon-ink)}} .note details p{{margin:12px 0}} .note pre{{white-space:pre-wrap;overflow-wrap:anywhere}}</style>\n</head>',1)
    body=f'<main><article class="note"><h1>{escape(title)}</h1><div class="byline"><span>{escape(byline)}</span></div><div class="body">\n{rendered}</div></article></main>\n'
    png=card(feature['question'] if feature else title,byline,args.output,(feature['example_label'],feature['example']) if feature else None)
    html=header+body+build_site.foot('../../')
    path=args.output/url;path.mkdir(parents=True,exist_ok=True)
    (path/'index.html').write_text(html,encoding='utf-8',newline='\n');(path/'share.png').write_bytes(png)
    if args.feature_output:
        if not feature:raise ValueError('--feature-output requires --experiment')
        # An explicit file outside the web root; the running site's config is never edited here.
        p=args.feature_output.resolve()
        if p.is_relative_to(args.output.resolve()):raise ValueError('feature output must not be in the public tree')
        p.write_text(json.dumps({'featured':feature},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{url} : index.html + share.png (1200 × 630)'+('; optional feature config exported' if args.feature_output else ''))

if __name__=='__main__':
    cli=ArgumentParser(description=__doc__)
    cli.add_argument('markdown',type=Path);cli.add_argument('--slug',required=True);cli.add_argument('--output',type=Path,required=True)
    cli.add_argument('--generator',type=Path,required=True,help='directory containing build_site.py and site_brand.py')
    cli.add_argument('--byline',default='学习短记');cli.add_argument('--experiment',action='store_true',help='use question and example on card, never include answer')
    cli.add_argument('--example-label',default='目录树');cli.add_argument('--feature-output',type=Path,help='export config to an explicit file outside the output tree')
    cli.add_argument('--replace-existing',action='store_true',help='explicitly allow replacing the existing note in the isolated tree')
    args=cli.parse_args()
    if args.feature_output and (not args.experiment or args.feature_output.resolve().is_relative_to(args.output.resolve())):cli.error('--feature-output requires --experiment and a path outside the output tree')
    try:compile_note(args)
    except (ValueError,OSError) as exc:cli.error(str(exc))
