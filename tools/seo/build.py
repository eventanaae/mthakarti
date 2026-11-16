#!/usr/bin/env python3
"""Build static, indexable pages for Google from the lesson data inside index.html.

Input : lessons.json (exported from the live app with tools/seo/export.js)
Output: /lessons/ (grade, subject and lesson pages), /exams/ (exam timetable), sitemap.xml
Every page links into the app (/#grade-subject-id) so students land on the real lesson.
"""
import json, re, os, sys, html, datetime, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = 'https://mthakarti.com'
YEAR = '2026-2027'
TERM = 'الفصل الدراسي الأول'
TODAY = datetime.date.today().isoformat()
data = json.load(open(sys.argv[1], encoding='utf-8'))
data.pop('err', None)

GN = {'g9g': 'الصف التاسع عام', 'g9a': 'الصف التاسع متقدم', 'g11g': 'الصف الحادي عشر عام', 'g11a': 'الصف الحادي عشر متقدم', 'g10g': 'الصف العاشر عام', 'g10a': 'الصف العاشر متقدم', 'g12a': 'الصف الثاني عشر متقدم', 'g12g': 'الصف الثاني عشر عام'}
GS = {'g9g': 'grade-9-general', 'g9a': 'grade-9-advanced', 'g11g': 'grade-11-general', 'g11a': 'grade-11-advanced', 'g10g': 'grade-10-general', 'g10a': 'grade-10-advanced', 'g12a': 'grade-12-advanced', 'g12g': 'grade-12-general'}

e = html.escape


def strip(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s or '')).strip()


CSS = """:root{--bg:#fff8fb;--surface:#fff;--ink:#2a1f2b;--mut:#76667a;--line:#ecdfe8;--pink:#d9467f;--lav:#7b5cc4;--pink-soft:#fde7f0;--sky-soft:#e8f2fd;--sun-soft:#fff4d9}
@media (prefers-color-scheme:dark){:root{--bg:#1b1520;--surface:#251d2b;--ink:#f3eaf2;--mut:#b6a6b8;--line:#3a2f40;--pink:#ff7aa9;--lav:#b39cff;--pink-soft:#3a2231;--sky-soft:#1f2b3a;--sun-soft:#3a3220;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.85 "IBM Plex Sans Arabic",Tahoma,system-ui,sans-serif;direction:rtl}
a{color:var(--lav)}header,main,footer{max-width:820px;margin:0 auto;padding:16px max(16px,env(safe-area-inset-left))}
header{display:flex;justify-content:space-between;align-items:center;gap:10px}header a.logo{font-weight:800;font-size:22px;color:var(--pink);text-decoration:none}
.crumbs{font-size:14px;color:var(--mut)}.crumbs a{color:var(--mut)}h1{font-size:28px;line-height:1.4;margin:.3em 0}h2{font-size:21px;margin:1.4em 0 .4em}
.pill{display:inline-block;background:var(--pink-soft);border-radius:99px;padding:2px 12px;font-size:14px;margin:2px}
.cta{display:block;text-align:center;background:var(--pink);color:#fff;text-decoration:none;font-weight:800;border-radius:16px;padding:14px;margin:18px 0;font-size:18px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:14px 16px;margin:12px 0}
.lfig{margin:16px auto;text-align:center;max-width:640px}.lfig img{max-width:100%;height:auto;border-radius:14px;border:1px solid var(--line);background:#fff}.lfig figcaption{font-size:13.5px;color:var(--mut)}
.m{direction:ltr;unicode-bidi:isolate;display:inline-block;font-family:"Cambria Math","Segoe UI",serif;font-weight:600;color:var(--pink)}
.ex{background:var(--sky-soft);border-radius:14px;padding:10px 12px;margin:8px 0}.trap{background:var(--sun-soft);border-radius:14px;padding:10px 12px;margin:8px 0}.key{background:var(--pink-soft);border-radius:14px;padding:10px 12px;margin:8px 0}
.tbl{width:100%;border-collapse:collapse;font-size:15px}.tbl td,.tbl th{border-bottom:1px solid var(--line);padding:8px;text-align:start}.tw{overflow-x:auto}
.en{direction:ltr;text-align:left}ul.list{padding-inline-start:20px}ul.list li{margin:4px 0}
details{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:10px 14px;margin:8px 0}summary{cursor:pointer;font-weight:700}
.nav{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin:18px 0}footer{color:var(--mut);font-size:14px}"""


def page(path, title, desc, body, crumbs, jsonld, canonical=None):
    url = SITE + '/' + path
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + '/' + p} for i, (n, p) in enumerate(crumbs)]}
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in [bc] + jsonld)
    cr = ' › '.join(f'<a href="/{p}">{e(n)}</a>' for n, p in crumbs[:-1]) + (' › ' + e(crumbs[-1][0]) if crumbs else '')
    doc = f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{e(canonical or url)}">
<meta property="og:type" content="article"><meta property="og:site_name" content="مذاكرتي"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}"><meta property="og:image" content="{SITE}/icon-512.png"><meta property="og:locale" content="ar_AE">
<link rel="icon" href="/icon-192.png"><meta name="theme-color" content="#ef5d98"><style>{CSS}</style>{lds}</head><body>
<header><a class="logo" href="/">مذاكرتي.</a><a href="/lessons/">📚 كل الدروس</a></header>
<main><nav class="crumbs">{cr}</nav>{body}</main>
<footer><p>مذاكرتي: منصة مذاكرة مجانية سوّتها بنت إماراتية لطلاب الإمارات من صف 9 لين 12. دروس على هيكل امتحانات وزارة التربية والتعليم، وكويز بعد كل درس، ومدرس خصوصي ذكي، ومسابقة أسبوعية.</p>
<p><a href="/lessons/">كل الدروس</a> · <a href="/exam-structure/">هيكل الامتحانات</a> · <a href="/exams/">جدول الامتحانات</a> · <a href="/study-tips/">كيف تذاكر للامتحان</a> · <a href="/about/">من سوّى مذاكرتي؟</a> · <a href="https://www.instagram.com/mthakarti/">إنستغرام</a></p></footer></body></html>"""
    out = os.path.join(ROOT, path, 'index.html') if path.endswith('/') or path == '' else os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(doc)
    return url


def app_link(g, k=None, i=None, camp='lesson'):
    h = '-'.join(str(x) for x in (g, k, i) if x is not None)
    return f'/?utm_source=google&utm_medium=organic&utm_campaign={camp}#{h}'


for d in ('lessons', 'exams', 'exam-structure', 'about'):
    shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)

urls = []
seen = {}  # identical lesson content across grades -> canonical to first
hub = []
for g, gd in data.items():
    gname = GN.get(g) or gd.get('name', g).replace(' · ', ' ')
    gslug = GS.get(g) or ('grade-' + re.sub(r'\D', '', g) + ('-advanced' if g.endswith('a') else '-general'))
    subj_cards = []
    for k, s in gd['subj'].items():
        sname = s['name']
        Q = s.get('Q') or []
        lessons = s['T']
        lcards = []
        for idx, t in enumerate(lessons):
            lid = t['id']
            path = f'lessons/{gslug}/{k}/{lid}/'
            sig = (k, t['t'], len(t['html']))
            canon = seen.get(sig)
            if not canon:
                seen[sig] = SITE + '/' + path
            qs = [q for q in Q if isinstance(q, list) and len(q) >= 7 and q[0] == lid][:3]
            faq = ''.join(f'<details><summary>{q[1]}</summary><p>✅ الجواب: <b>{q[2]}</b></p><p>{q[6]}</p></details>' for q in qs)
            prev = lessons[idx - 1] if idx else None
            nxt = lessons[idx + 1] if idx + 1 < len(lessons) else None
            title = f'{t["t"]} | {sname} {gname} – شرح وأسئلة | مذاكرتي'
            desc = (strip(t['say']) or strip(t['html']))[:155]
            dirattr = ' class="en" dir="ltr"' if s.get('lang') == 'en' else ''
            body = f"""<h1>{e(t['t'])}</h1>
<p><span class="pill">{s.get('icon','📘')} {e(sname)}</span><span class="pill">🎓 {e(gname)}</span>{f'<span class="pill">📌 هيكل الامتحان: {e(t["q"])}</span>' if t.get('q') else ''}</p>
<a class="cta" href="{app_link(g,k,lid)}">🎯 ذاكر الدرس وحل الكويز مجانًا في مذاكرتي</a>
<div{dirattr}>{t['html']}{t.get('deep') or ''}</div>
{f'<h2>اختبر نفسك: أسئلة على {e(t["t"])}</h2>{faq}' if faq else ''}
<a class="cta" href="{app_link(g,k,lid)}">حل كويز الدرس كامل ونافس طلاب مرحلتك 🏆</a>
<div class="nav">{f'<a href="/lessons/{gslug}/{k}/{prev["id"]}/">→ {e(prev["t"])}</a>' if prev else '<span></span>'}<a href="/lessons/{gslug}/{k}/">كل دروس {e(sname)}</a>{f'<a href="/lessons/{gslug}/{k}/{nxt["id"]}/">{e(nxt["t"])} ←</a>' if nxt else ''}</div>"""
            ld = [{"@context": "https://schema.org", "@type": "LearningResource", "name": t['t'], "description": desc, "inLanguage": "ar" if s.get('lang') != 'en' else 'en',
                   "educationalLevel": gname, "about": sname, "isAccessibleForFree": True, "learningResourceType": "Lesson",
                   "provider": {"@type": "EducationalOrganization", "name": "مذاكرتي", "url": SITE}}]
            if qs:
                ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": strip(q[1]), "acceptedAnswer": {"@type": "Answer", "text": strip(q[2]) + '. ' + strip(q[6])}} for q in qs]})
            crumbs = [('مذاكرتي', ''), ('كل الدروس', 'lessons/'), (gname, f'lessons/{gslug}/'), (sname, f'lessons/{gslug}/{k}/'), (t['t'], path)]
            u = page(path, title, desc, body, crumbs, ld, canonical=canon)
            if not canon:
                urls.append(u)
            lcards.append(f'<li><a href="/lessons/{gslug}/{k}/{lid}/">{lid}. {e(t["t"])}</a>{f" <small>({e(t["q"])})</small>" if t.get("q") else ""}</li>')
        # subject page = exam structure + lesson list
        spath = f'lessons/{gslug}/{k}/'
        stitle = f'هيكل امتحان {sname} {gname} {TERM} {YEAR} – شرح كل الدروس وأسئلة | مذاكرتي'
        sdesc = f'كل دروس {sname} لـ{gname} مرتبة على هيكل امتحان وزارة التربية والتعليم ({TERM} {YEAR}): {len(lessons)} درس، و{len(Q)} سؤال، وكويز بعد كل درس. مجانًا.'
        sbody = f"""<h1>{e(sname)}: {e(gname)}</h1><p>{e(sdesc)}</p>
<a class="cta" href="{app_link(g,k,camp='subject')}">ابدأ مذاكرة {e(sname)} مجانًا</a>
<h2>الدروس حسب هيكل الامتحان</h2><ul class="list">{''.join(lcards)}</ul>"""
        urls.append(page(spath, stitle, sdesc, sbody, [('مذاكرتي', ''), ('كل الدروس', 'lessons/'), (gname, f'lessons/{gslug}/'), (sname, spath)],
                         [{"@context": "https://schema.org", "@type": "Course", "name": f'{sname} – {gname}', "description": sdesc, "inLanguage": "ar",
                           "provider": {"@type": "EducationalOrganization", "name": "مذاكرتي", "url": SITE}, "isAccessibleForFree": True}]))
        subj_cards.append(f'<li><a href="/{spath}">{s.get("icon","📘")} {e(sname)}</a> <small>({len(lessons)} درس)</small></li>')
    gpath = f'lessons/{gslug}/'
    gdesc = f'كل مواد {gname} في الإمارات: دروس على هيكل امتحان الوزارة، وكويزات، ومدرس خصوصي ذكي. مجانًا.'
    urls.append(page(gpath, f'دروس {gname} – هيكل الامتحانات وشرح كل المواد {YEAR} | مذاكرتي', gdesc,
                     f'<h1>{e(gname)}</h1><p>{e(gdesc)}</p><a class="cta" href="{app_link(g,camp="grade")}">ابدأ المذاكرة مجانًا</a><h2>المواد</h2><ul class="list">{"".join(subj_cards)}</ul>',
                     [('مذاكرتي', ''), ('كل الدروس', 'lessons/'), (gname, gpath)], []))
    hub.append(f'<li><a href="/{gpath}">🎓 {e(gname)}</a></li>')

hdesc = f'دروس كل المواد لطلاب الإمارات ({", ".join(GN.values())}) على هيكل امتحانات وزارة التربية والتعليم {YEAR}، مع كويزات ومدرس خصوصي ذكي. مجانًا 100%.'
urls.insert(0, page('lessons/', f'كل الدروس – هيكل امتحانات الإمارات {YEAR} | مذاكرتي', hdesc,
                    f'<h1>كل دروس مذاكرتي</h1><p>{e(hdesc)}</p><ul class="list">{"".join(hub)}</ul><p><a href="/exams/">📅 جدول امتحانات نهاية {TERM}</a></p>',
                    [('مذاكرتي', ''), ('كل الدروس', 'lessons/')], []))

# exam timetable page from EXAMS in index.html
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
m = re.search(r'const EXAMS=\{(.*?)\n\};', src, re.S)
rows = ''
if m:
    for g, body in re.findall(r"(\w+):\[(.*?)\]\](?:,|\s*$)", m.group(1), re.S):
        items = re.findall(r"\['(\w+)','([\d-]+)','([^']+)'\]", body + ']')
        names = data.get(g, {}).get('subj', {})
        rows += f'<h2>{e(GN.get(g, g))}</h2><div class="tw"><table class="tbl"><tr><th>المادة</th><th>التاريخ</th><th>الوقت</th></tr>' + ''.join(
            f'<tr><td>{e(names.get(k, {}).get("name", k))}</td><td>{d}</td><td>{e(tm)}</td></tr>' for k, d, tm in items) + '</table></div>'
edesc = f'جدول امتحانات نهاية {TERM} {YEAR} في الإمارات للصف العاشر والثاني عشر (عام ومتقدم)، مع روابط شرح كل مادة على هيكل الامتحان.'
urls.append(page('exams/', f'جدول امتحانات نهاية {TERM} {YEAR} الإمارات – العاشر والثاني عشر | مذاكرتي', edesc,
                 f'<h1>جدول امتحانات نهاية {TERM} {YEAR}</h1><p>{e(edesc)}</p>{rows}<a class="cta" href="/?utm_source=google&utm_medium=organic&utm_campaign=exams#exams">🔔 فعّل تذكير الامتحانات وذاكر مجانًا</a><p><a href="/lessons/">📚 شرح كل المواد</a></p>',
                 [('مذاكرتي', ''), ('جدول الامتحانات', 'exams/')], []))


# exam-structure hub: every subject of every grade with its structure references
hs = ''
for g, gd in data.items():
    gname = GN.get(g) or gd.get('name', g)
    gslug = GS.get(g) or g
    items = ''
    for k, s in gd['subj'].items():
        refs = [t.get('q') for t in s['T'] if t.get('q')]
        items += f'<li><a href="/lessons/{gslug}/{k}/">{s.get("icon","📘")} هيكل امتحان {e(s["name"])}</a> <small>({len(s["T"])} درس{"، " + str(len(refs)) + " بند من الهيكل" if refs else ""})</small></li>'
    hs += f'<h2>{e(gname)}</h2><ul class="list">{items}</ul>'
hdesc2 = f'هياكل امتحانات وزارة التربية والتعليم في الإمارات {TERM} {YEAR} لكل المواد، من صف 9 لين 12 عام ومتقدم، مع شرح كل بند في الهيكل وأسئلة عليه. مجانًا.'
urls.append(page('exam-structure/', f'هيكل امتحانات الإمارات {TERM} {YEAR} – كل المواد صف 9-12 | مذاكرتي', hdesc2,
                 f'<h1>هيكل امتحانات {TERM} {YEAR}</h1><p>{e(hdesc2)}</p><a class="cta" href="/?utm_source=google&utm_medium=organic&utm_campaign=structure">ذاكر على الهيكل مجانًا</a>{hs}<p><a href="/exams/">📅 جدول الامتحانات</a></p>',
                 [('مذاكرتي', ''), ('هيكل الامتحانات', 'exam-structure/')], []))

# about page (trust: who made it and why)
adesc = 'مذاكرتي منصة مذاكرة مجانية سوّتها بنت إماراتية عشان تساعد طلاب الإمارات من صف 9 لين 12: دروس على هيكل الامتحان، وكويزات، ومدرس خصوصي ذكي، ومسابقة كل أسبوع.'
urls.append(page('about/', 'من سوّى مذاكرتي؟ منصة مجانية من بنت إماراتية لطلاب الإمارات | مذاكرتي', adesc,
                 f"""<h1>من سوّى مذاكرتي؟</h1>
<p>مذاكرتي سوّتها <b>بنت إماراتية</b> عشان تساعد طلاب الإمارات. كانت المذاكرة من ملفات وقروبات مبعثرة، وما تدري وش المهم في الامتحان. فجمعت كل شي في مكان واحد، مرتب على <b>هيكل امتحان وزارة التربية والتعليم</b>، و<b>مجاني 100%</b>.</p>
<h2>وش تلقى في مذاكرتي؟</h2><ul class="list"><li>📚 دروس ومراجعات لكل المواد، من صف 9 لين 12، عام ومتقدم.</li><li>✅ كويز بعد كل درس، وامتحانات تجريبية.</li><li>🤖 مدرس خصوصي ذكي يرد على أسئلتك.</li><li>🏆 مسابقة كل أسبوع مع طلاب مرحلتك في كل الإمارات.</li><li>🔔 تذكير بالامتحانات وجدولها.</li></ul>
<a class="cta" href="/?utm_source=google&utm_medium=organic&utm_campaign=about">ابدأ مجانًا</a>
<p>تابعونا على إنستغرام: <a href="https://www.instagram.com/mthakarti/">@mthakarti</a></p>""",
                 [('مذاكرتي', ''), ('من نحن', 'about/')],
                 [{"@context": "https://schema.org", "@type": "AboutPage", "name": "من سوّى مذاكرتي؟", "description": adesc,
                   "about": {"@type": "EducationalOrganization", "name": "مذاكرتي", "url": SITE, "sameAs": ["https://www.instagram.com/mthakarti/"]}}]))

# hand-written content pages (not generated here; keep them in the sitemap)
urls.append(f'{SITE}/study-tips/')

# sitemap
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', f'<url><loc>{SITE}/</loc><lastmod>{TODAY}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>']
sm += [f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls]
sm.append('</urlset>')
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(sm))
print('pages', len(urls) + 1, 'canonical-dupes', sum(1 for _ in seen) and None)
