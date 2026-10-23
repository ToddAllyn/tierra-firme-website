#!/usr/bin/env python3
"""Builds the Tierra Firme static site into ../tierra-firme-website."""
import json, os, html

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)
BASE = 'https://tierra-firme.pages.dev'  # switch to https://tierrafirme.com once the domain is attached
SHARE = BASE + '/tierra-firme-share.jpg'

CSS = r"""
:root{color-scheme:light;
  --navy:#061327;--navy-2:#0c2748;--ink:#13212f;--muted:#4e5a67;--muted-2:#8795a3;
  --cream:#f8f2e4;--cream-2:#f0e7d3;--surface:#fffdf8;--border:#e4d9c2;
  --gold:#e9a825;--gold-d:#a86d0c;--gold-l:#f3c76a;--teal:#0d6f5c;--terracotta:#c4552a;--sky:#2b67ad;
  --maxw:1120px}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--cream);color:var(--ink);font-family:'Inter',-apple-system,'Segoe UI',sans-serif;font-size:16.5px;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden}
h1,h2,h3{font-family:'Fraunces',Georgia,serif;font-weight:600;line-height:1.12;letter-spacing:-.01em;margin:0 0 .5em;color:var(--ink);text-wrap:balance}
h1{font-size:clamp(2.5rem,5.4vw,4.4rem)}
h2{font-size:clamp(1.8rem,3.2vw,2.6rem)}
h3{font-size:1.22rem}
p{margin:0 0 1em;color:var(--muted)}
a{color:inherit}
a:focus-visible,button:focus-visible,input:focus-visible,summary:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
.container{max-width:var(--maxw);margin:0 auto;padding:0 clamp(16px,4vw,32px)}
section{padding:clamp(60px,8vw,88px) 0;position:relative}
.alt{background:var(--cream-2)}
.dark{background:var(--navy);color:#fff}
.dark h2,.dark h3{color:#fff}.dark p{color:rgba(255,255,255,.76)}
.eyebrow{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-d);margin-bottom:16px}
.dark .eyebrow,.hero .eyebrow{color:var(--gold)}
.lede{font-size:1.14rem;max-width:660px;line-height:1.62}
.section-head{margin-bottom:40px;max-width:760px}
.text-center{text-align:center}.text-center .lede{margin-inline:auto}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

/* header */
.site-header{position:sticky;top:0;z-index:50;background:rgba(6,19,39,.97);border-bottom:1px solid rgba(255,255,255,.08)}
.nav-wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-block:14px;position:relative}
.brand{display:flex;align-items:center;gap:12px;font-family:'Fraunces',serif;font-weight:600;font-size:1.2rem;color:#fff;text-decoration:none}
.brand-mark{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:50%;border:1.5px solid var(--gold);color:var(--gold);font-size:.8rem;font-weight:700;background:rgba(233,168,37,.08);font-family:'Inter',sans-serif}
.main-nav{display:flex;align-items:center;gap:2px}
.main-nav a{padding:8px 13px;font-size:.92rem;font-weight:500;color:rgba(255,255,255,.84);border-radius:4px;text-decoration:none}
.main-nav a:hover,.main-nav a[aria-current=page]{color:#fff;background:rgba(255,255,255,.08)}
.main-nav a.btn{margin-left:10px;color:var(--navy)}
.nav-toggle{display:none;background:none;border:1px solid rgba(255,255,255,.25);color:#fff;font-size:1.3rem;line-height:1;padding:8px 12px;border-radius:4px;cursor:pointer}
@media (max-width:900px){
  .nav-toggle{display:block}
  .main-nav{display:none;position:absolute;top:100%;right:0;left:0;flex-direction:column;align-items:stretch;gap:2px;background:var(--navy);padding:12px clamp(16px,4vw,32px) 18px;border-bottom:1px solid rgba(255,255,255,.1)}
  .main-nav.open{display:flex}
  .main-nav a.btn{margin:8px 0 0}
}

/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 24px;font-weight:600;font-size:.98rem;border-radius:4px;border:1.5px solid transparent;text-decoration:none;cursor:pointer;font-family:inherit;transition:background .15s,color .15s}
.btn-gold{background:var(--gold);color:var(--navy)}.btn-gold:hover{background:var(--gold-l)}
.btn-outline{border-color:rgba(255,255,255,.5);color:#fff}.btn-outline:hover{background:#fff;color:var(--navy)}
.btn-ink{border-color:var(--ink);color:var(--ink)}.btn-ink:hover{background:var(--ink);color:#fff}
.btn-row{display:flex;flex-wrap:wrap;gap:12px}

/* hero */
.hero{background:radial-gradient(ellipse at 80% 0%,#12355f 0%,var(--navy) 60%);color:#fff;padding:clamp(72px,10vw,120px) 0 clamp(56px,7vw,80px)}
.hero{overflow:hidden}
.hero>.container{position:relative;z-index:2}
.globe{position:absolute;top:50%;right:-80px;transform:translateY(-50%);width:620px;height:620px;background:url("globe.svg") center/contain no-repeat;opacity:.9;z-index:1;pointer-events:none}
@media (max-width:1100px){.globe{right:-220px;opacity:.5}}
@media (max-width:640px){.globe{width:420px;height:420px;right:-200px;top:38%;opacity:.35}}
.hero h1{color:#fff}
.hero .lede{color:rgba(255,255,255,.8)}
.hero-fine{font-size:.86rem;color:rgba(255,255,255,.55);margin-top:18px}
.disciplines{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 22px;padding:0;list-style:none}
.disciplines li{font-size:.78rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;padding:6px 12px;border:1px solid rgba(233,168,37,.45);color:var(--gold-l);border-radius:999px}
.meridian{display:flex;align-items:center;gap:14px;margin-top:48px;max-width:640px;white-space:nowrap;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.6);flex-wrap:wrap}
.meridian .line{flex:1 1 40px;height:1px;background:linear-gradient(90deg,rgba(233,168,37,.1),var(--gold),rgba(233,168,37,.1));min-width:30px}
.meridian .pt{color:var(--gold-l)}
@media (max-width:640px){.meridian .line{display:none}.meridian{flex-direction:column;align-items:flex-start;gap:6px}}

/* cards and grids */
.grid-3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.grid-2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
@media (max-width:900px){.grid-3{grid-template-columns:1fr}}
@media (max-width:760px){.grid-2{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--border);border-radius:4px;padding:28px;min-width:0}
.card p:last-child{margin-bottom:0}
.dark .card{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.14)}
.dark .tag-ground{color:#f08a5d}.dark .tag-build{color:#3cc4a4}.dark .tag-research{color:#7fb0ea}
.card .num{font-family:'Fraunces',serif;font-size:2rem;color:var(--gold-d);line-height:1;margin-bottom:12px}
.bar-ground{border-top:3px solid var(--terracotta)}.bar-build{border-top:3px solid var(--teal)}.bar-research{border-top:3px solid var(--sky)}
.tag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:12px}
.tag-ground{color:var(--terracotta)}.tag-build{color:var(--teal)}.tag-research{color:var(--sky)}
.role{font-size:.9rem;font-weight:600;color:var(--ink);margin:-6px 0 14px}

/* member profile */
.member{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr);gap:clamp(24px,4vw,56px);padding:clamp(28px,4vw,44px) 0;border-top:1px solid var(--border)}
.member:last-child{border-bottom:1px solid var(--border)}
.member h2{font-size:clamp(1.6rem,2.6vw,2.1rem)}
@media (max-width:760px){.member{grid-template-columns:1fr}}

/* ladder */
.ladder{display:flex;flex-direction:column;gap:14px;max-width:820px}
.step{display:grid;grid-template-columns:52px minmax(0,1fr);gap:18px;align-items:start;background:var(--surface);border:1px solid var(--border);border-radius:4px;padding:22px}
.step-mark{width:44px;height:44px;border-radius:50%;background:var(--navy);color:var(--gold);display:flex;align-items:center;justify-content:center;font-weight:700}
.step h3{margin-bottom:6px}
.pill{display:inline-block;font-family:'Inter',sans-serif;font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted-2);margin-left:8px;vertical-align:middle}
.pill.on{color:var(--gold-d)}

/* faq */
.faq{max-width:820px}
.faq details{border-top:1px solid var(--border)}
.faq details:last-child{border-bottom:1px solid var(--border)}
.faq summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:20px;padding:20px 0;font-family:'Fraunces',serif;font-size:1.2rem;font-weight:600;color:var(--ink)}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--gold-d);font-family:'Inter',sans-serif;flex:0 0 auto}
.faq details[open] summary::after{content:"\2212"}
.faq details p{padding-bottom:12px;max-width:70ch}

/* episodes */
.eps{display:flex;flex-direction:column}
.ep{display:grid;grid-template-columns:64px minmax(0,1fr);gap:20px;padding:22px 0;border-top:1px solid var(--border)}
.ep:last-child{border-bottom:1px solid var(--border)}
.ep .n{font-family:'Fraunces',serif;font-size:1.9rem;color:var(--gold-d);line-height:1}
.ep .meta{font-size:.76rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted-2);margin-bottom:4px}
.ep h3{margin-bottom:4px}
.ep p{margin:0}

/* signup */
.signup{display:flex;gap:12px;flex-wrap:wrap;max-width:560px;margin-top:22px}
.signup input{flex:1 1 240px;min-width:0;min-height:48px;padding:0 16px;font:inherit;border:1.5px solid var(--border);border-radius:4px;background:#fff;color:var(--ink)}
.dark .signup input{border-color:rgba(255,255,255,.3)}
.status{min-height:1.6em;margin-top:10px;font-size:.95rem}
.checks{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:12px}
.checks li{padding-left:28px;position:relative;color:var(--muted)}
.checks li::before{content:"";position:absolute;left:0;top:.55em;width:14px;height:8px;border-left:2px solid var(--gold-d);border-bottom:2px solid var(--gold-d);transform:rotate(-45deg)}

.hero-card{background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.16)}
.hero-card h3{color:#fff}.hero-card .checks li{color:rgba(255,255,255,.82)}
.hero .checks li::before{border-color:var(--gold)}
.note{font-size:.9rem;color:var(--muted);max-width:80ch;border-left:3px solid var(--gold);padding-left:16px}

/* footer */
footer{background:var(--navy);color:rgba(255,255,255,.7);padding:44px 0 36px}
.footer-grid{display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;margin-bottom:22px}
.footer-nav{display:flex;flex-wrap:wrap;gap:6px 18px}
.footer-nav a{color:rgba(255,255,255,.8);text-decoration:none;font-size:.92rem}
.footer-nav a:hover{color:var(--gold)}
.legal{font-size:.82rem;color:rgba(255,255,255,.55);max-width:90ch;margin:0 0 10px}
.credit{font-size:.82rem;color:rgba(255,255,255,.55);margin:0}
.credit a{color:rgba(255,255,255,.75)}
"""

NAV = [('index.html', 'Home'), ('members.html', 'Members'), ('the-show.html', 'The Show'), ('membership.html', 'Membership')]

LEGAL = ("Tierra Firme is educational content and seminars. Nothing here is investment, tax or legal advice, "
         "an offer to sell, or a solicitation of an offer to buy any security or property. Cross-border investing "
         "carries currency, country and tax risk. Each member runs an independent practice; any professional "
         "engagement with a member happens through that member's own firm, separate from Tierra Firme.")

FAQ = [
    ("What is Tierra Firme?",
     "Tierra Firme is a consortium of three practitioners in commercial real estate, business and family capital, and intelligence research. "
     "It produces a free show, research and seminars for people placing capital across borders, starting with Latin America."),
    ("Who is behind Tierra Firme?",
     "Murphy D. Cheatham II (commercial real estate), Shawn Christopher Leamon (business and operations) and Todd Allyn "
     "(intelligence research, Sovereo Intelligence Research). Each runs an independent practice."),
    ("Who is Tierra Firme for?",
     "Individuals, families and family offices in the US, Canada and Europe who want to understand a market abroad before committing capital, "
     "including households priced out of ownership at home and retirees stretching a fixed income."),
    ("Is Tierra Firme free?",
     "The show and the email list are free. Seminars are paid and announced to the list first. A paid membership community is opening soon; join the waitlist for first access."),
    ("What is the Tierra Firme membership?",
     "A paid community opening soon: a structured curriculum on evaluating markets abroad, a members' forum, and live office hours with "
     "Murphy, Shawn and Todd. It is education, not investment advice. The waitlist gets first access."),
    ("Does Tierra Firme sell property or broker deals?",
     "No. Tierra Firme teaches how to evaluate a market and a deal. It does not list property, broker transactions or take fees on what you buy."),
    ("Is anything from Tierra Firme investment advice?",
     "No. Everything Tierra Firme publishes is educational. It is not investment, tax or legal advice. Decisions stay with you and your own advisers."),
    ("What role does Sovereo Intelligence Research play?",
     "Sovereo Intelligence Research is a founding member and leads Tierra Firme research: the macroeconomic, currency and country intelligence "
     "behind each episode and seminar. Sovereo takes no deal fees, advisory fees or carry."),
    ("Where is Tierra Firme based?",
     "Bogotá, Colombia, with members in Dallas and Bogotá. Bogotá holds the central bank, tax authority, notaries and ministries every foreign investor deals with."),
]

MEMBERS = [
    dict(key='ground', seat='The Ground', area='Commercial real estate', name='Murphy D. Cheatham II', short='Murphy Cheatham',
         role='Private Clients Director, CBRE · Dallas',
         show='The asset: what a property abroad is worth, what your income reaches there, and how to own it without getting burned.',
         bio=("Murphy D. Cheatham II is Private Clients Director at CBRE in Dallas, where he advises private families and high net worth "
              "individuals on commercial real estate. In more than two decades he has sourced and serviced debt and equity, optimized portfolios "
              "and managed properties, led strategic planning on more than $300 million in mixed-use projects in partnership with HDR, and served as "
              "Chief of Housing and Business Development for the City of Shreveport. He holds a B.S. in Accounting from Grambling State University "
              "and a Master of Real Estate Development from Arizona State University, and helped create the real estate partnership between the two schools."),
         person={"@type": "Person", "name": "Murphy D. Cheatham II", "alternateName": "Murphy Cheatham",
                 "jobTitle": "Private Clients Director",
                 "worksFor": {"@type": "Organization", "name": "CBRE", "url": "https://www.cbre.com"},
                 "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Grambling State University"},
                              {"@type": "CollegeOrUniversity", "name": "Arizona State University"}],
                 "sameAs": ["https://www.cbre.com/people/murphy-cheatham"]}),
    dict(key='build', seat='The Build', area='Business and operations', name='Shawn Christopher Leamon', short='Shawn Leamon',
         role='Founder and Managing Partner, LaGrande Global · Founder and CEO, Cielo.Travel · Bogotá',
         show='The operation: the business or income stream you could run on the ground, what it costs to enter and what it takes to run.',
         bio=("Shawn Christopher Leamon is founder and managing partner of LaGrande Global, the investment firm he started in 2013, which manages "
              "close to $100 million across private equity, startups, real estate and public markets, with a focus on Latin America. Before that he "
              "worked in investment banking and wealth management on portfolios of more than $1 billion. He also built and sold a marketing agency, "
              "and is founder and CEO of Cielo.Travel, one of Colombia's largest digital travel networks. Born in Dallas, he has lived in Bogotá since 2023. "
              "He holds degrees in Economics and Philosophy from Dartmouth College and an MBA from IE Business School."),
         person={"@type": "Person", "name": "Shawn Christopher Leamon", "alternateName": "Shawn Leamon",
                 "jobTitle": "Founder and Managing Partner",
                 "worksFor": [{"@type": "Organization", "name": "LaGrande Global", "url": "https://lagrandeglobal.com"},
                              {"@type": "Organization", "name": "Cielo.Travel", "url": "https://cielo.travel"}],
                 "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Dartmouth College"},
                              {"@type": "CollegeOrUniversity", "name": "IE Business School"}],
                 "sameAs": ["https://lagrandeglobal.com/shawn-leamon/", "https://cielo.travel/meet-our-ceo-shawn-christopher-leamon/"]}),
    dict(key='research', seat='The Research', area='Intelligence research', name='Todd Allyn', short='Todd Allyn',
         role='Founding Director, Sovereo Intelligence Research · Former Dean, College of Business, Chancellor University · Bogotá',
         show='The conditions: the macroeconomic, currency and country research that sets your real return, and what changes it.',
         bio=("Todd Allyn leads Tierra Firme research. He is Founding Director of Sovereo Intelligence Research, a systems intelligence firm that "
              "tracks how geopolitics, culture, technopolitics, astropolitics, rare earths and minerals change the options open to investors and families. "
              "Sovereo publishes a daily SITREP, the Sovereo Brief, Country Dossiers and the Decision Forecast, a public record of forecasts made with "
              "stated confidence and scored against what actually happened. Before Sovereo he was Dean of the College of Business at Chancellor "
              "University in Cleveland, where he helped build the Jack Welch Management Institute, and he spent 24 years teaching college economics, "
              "finance and business. He hosted The Todd Allyn Show on iHeartRadio and holds a finance degree and dual master's degrees in finance and "
              "international business from the University of Akron. He has lived in Bogotá since 2020."),
         person={"@type": "Person", "name": "Todd Allyn", "jobTitle": "Founding Director",
                 "worksFor": {"@type": "Organization", "name": "Sovereo Intelligence Research", "url": "https://www.sovereo.com"},
                 "alumniOf": {"@type": "CollegeOrUniversity", "name": "University of Akron"},
                 "hasOccupation": {"@type": "Occupation", "name": "Former Dean, College of Business, Chancellor University"},
                 "sameAs": ["https://www.linkedin.com/in/toddallyn/", "https://www.youtube.com/@sovereointel", "https://www.sovereo.com"]}),
]

EPISODES = [
    ('All three', 'The World Is Mispriced', "The founding thesis: you're not broke, you're in the wrong market. Currency, political and structural conditions put the first rung back within reach abroad."),
    ('Research', 'The Arbitrage, in Numbers', 'The math: how home-currency income and savings change in value the moment they cross the border.'),
    ('Ground', 'Real Assets, Real Prices', 'What entry-level property abroad costs, and how to judge it against being priced out at home.'),
    ('Build', 'Buy the Business, Not Just the Building', 'Starting or buying a small business abroad, where the cost of entry is within reach and the income is real.'),
    ('Research', 'Strong Dollar, Weak Dollar', 'How the picture changes with your currency, dollar, loonie or euro, when it is strong and when it turns.'),
    ('Research', 'The Currency Trap', 'The other side of the trade: how depreciation eats returns, and how structure can limit the damage.'),
    ('Ground', 'Capital In, Yield Out', 'How a modest stake becomes local income, and what it takes to bring the money home.'),
    ('Build', 'Boots on the Ground', 'Why this cannot be done from a laptop: the teams, trust and presence it takes to operate abroad.'),
    ('Ground', 'Colombia: The Beachhead', 'A market study and an honest look at political risk, up close.'),
    ('All three', 'The Case Study', 'A sample deal priced, operated and stress-tested on camera as a teaching case. Not an offer.'),
    ('Build', 'Entities, Taxes and Getting Paid', 'Structure in practice: owning as a foreigner, repatriating capital and staying clean with the IRS.'),
    ('Ground', 'The Multinational Balance Sheet', 'Season finale: assets and businesses abroad, assembled into one durable balance sheet.'),
]

def jsonld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + '\n</script>'

def page(fname, title, desc, body, schema_extra=(), crumbs=None):
    slug = '' if fname == 'index.html' else fname.replace('.html', '')
    url = BASE + '/' + slug
    nav = ''.join(f'<a href="{h}"{" aria-current=page" if h == fname else ""}>{t}</a>' for h, t in NAV)
    graph = [
        {"@type": "WebSite", "@id": BASE + "/#website", "name": "Tierra Firme", "url": BASE + "/", "inLanguage": "en",
         "publisher": {"@id": BASE + "/#org"}},
        {"@type": "Organization", "@id": BASE + "/#org", "name": "Tierra Firme", "url": BASE + "/", "logo": SHARE,
         "description": "A consortium of three practitioners in commercial real estate, business and family capital, and intelligence research, producing a free show, research and seminars on placing capital across borders.",
         "areaServed": ["Colombia", "Latin America"],
         "knowsAbout": ["Commercial real estate", "Family office", "Foreign investment in Colombia", "Currency risk", "Country risk", "Intelligence research"],
         "member": [m['person'] for m in MEMBERS]},
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc,
         "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BASE + "/#org"}, "dateModified": "2026-10-16"},
    ]
    if crumbs:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + '/' + h.replace('.html', '')} for i, (h, n) in enumerate(crumbs)]})
    graph.extend(schema_extra)
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#061327">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Tierra Firme">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SHARE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SHARE}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap">
{jsonld({"@context": "https://schema.org", "@graph": graph})}
<style>{CSS}</style>
</head>
<body>
<header class="site-header">
 <div class="container nav-wrap">
  <a href="index.html" class="brand"><span class="brand-mark" aria-hidden="true">TF</span>Tierra Firme</a>
  <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="main-nav">&#9776;</button>
  <nav class="main-nav" id="main-nav" aria-label="Main">{nav}<a href="membership.html" class="btn btn-gold">Join the community</a></nav>
 </div>
</header>
<main>
{body}
</main>
<footer>
 <div class="container">
  <div class="footer-grid">
   <a href="index.html" class="brand"><span class="brand-mark" aria-hidden="true">TF</span>Tierra Firme</a>
   <nav class="footer-nav" aria-label="Footer">{''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}<a href="join.html">Join the list</a></nav>
  </div>
  <p class="legal">{LEGAL}</p>
  <p class="credit">&copy; 2026 Tierra Firme. Research by <a href="https://www.sovereo.com">Sovereo Intelligence Research</a>. Design by Sovereo Web Works.</p>
 </div>
</footer>
<script>
(function(){{
 var t=document.querySelector('.nav-toggle'),n=document.getElementById('main-nav');
 if(t&&n){{t.addEventListener('click',function(){{var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');}});}}
 var f=document.getElementById('signup');
 if(f){{var i=f.querySelector('input[type=email]'),s=document.getElementById('signup-status');
  f.addEventListener('submit',function(e){{e.preventDefault();
   if(!i.value||!i.checkValidity()){{s.textContent='Enter a valid email address.';i.focus();return;}}
   var b=f.querySelector('button');b.disabled=true;s.textContent='Sending...';
   fetch('/subscribe',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{email:i.value.trim(),source:location.pathname}})}})
    .then(function(r){{return r.json().catch(function(){{return {{}};}}).then(function(j){{if(!r.ok||!j.ok)throw new Error(j.error||'');s.textContent=f.getAttribute('data-ok');f.reset();}});}})
    .catch(function(err){{s.textContent=(err&&err.message)||'That did not go through. Try again.';}})
    .then(function(){{b.disabled=false;}});
  }});
 }}
}})();
</script>
</body>
</html>
"""
    for a, b in [('href="index.html"', 'href="/"'), ('href="members.html"', 'href="/members"'), ('href="the-show.html"', 'href="/the-show"'), ('href="join.html"', 'href="/join"'), ('href="membership.html"', 'href="/membership"')]:
        out = out.replace(a, b)
    return out


def signup_block(dark=True, btn='Join the list', ok="You're on the list. New episodes, research and seminar dates come to you first."):
    return f"""<form class="signup" id="signup" novalidate data-ok="{html.escape(ok)}">
   <label class="sr" for="tf-email">Email address</label>
   <input id="tf-email" type="email" name="email" autocomplete="email" placeholder="you@email.com" required>
   <button type="submit" class="btn btn-gold">{btn}</button>
  </form>
  <p class="status" id="signup-status" role="status" aria-live="polite"></p>"""

def faq_html(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in items) + '</div>'

def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def seat_cards(link=True):
    out = []
    for m in MEMBERS:
        out.append(f"""<article class="card bar-{m['key']}">
    <span class="tag tag-{m['key']}">{m['seat']} · {m['area']}</span>
    <h3>{m['name']}</h3>
    <p>{m['show']}</p>
   </article>""")
    return '<div class="grid-3">' + ''.join(out) + '</div>'

# ---------- index ----------
index_body = f"""
<section class="hero">
 <div class="globe" aria-hidden="true"></div>
 <div class="container">
  <ul class="disciplines" aria-label="Disciplines"><li>Commercial real estate</li><li>Business and family capital</li><li>Intelligence research</li></ul>
  <h1>Any currency.<br>Solid ground.</h1>
  <p class="lede">Tierra Firme is a consortium of three practitioners in real estate, business and research. We produce a free show, research and seminars for people placing capital across borders, starting with Latin America.</p>
  <div class="btn-row" style="margin-top:28px">
   <a href="membership.html" class="btn btn-gold">Join the community</a>
   <a href="join.html" class="btn btn-outline">Get the free list</a>
  </div>
  <p class="hero-fine">Education, not advice. No listings, no deals, no fees on what you buy.</p>
  <div class="meridian" aria-hidden="true"><span class="pt">Dallas · 32.78°N</span><span class="line"></span><span>Home to solid ground</span><span class="line"></span><span class="pt">Latin America</span></div>
 </div>
</section>

<section>
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">What Tierra Firme is</span>
   <h2>Three disciplines at one table.</h2>
   <p class="lede">A sound property in the wrong conditions is a bad investment. Most advice covers the asset or the money, rarely the country. Tierra Firme puts all three views in the same room so each one checks the others.</p>
  </div>
  <div class="grid-3">
   <article class="card bar-ground"><span class="tag tag-ground">The asset</span><h3>Commercial real estate</h3><p>How property is sourced, financed, valued and managed, and what that means for a buyer entering a new market.</p></article>
   <article class="card bar-build"><span class="tag tag-build">The capital</span><h3>Business and family capital</h3><p>How individuals, families and family offices build, run and hold assets and businesses abroad.</p></article>
   <article class="card bar-research"><span class="tag tag-research">The country</span><h3>Intelligence research</h3><p>The economic, currency and political conditions that set your real return, and the signals that they are changing.</p></article>
  </div>
 </div>
</section>

<section class="alt">
 <div class="container grid-2" style="align-items:start">
  <div>
   <span class="eyebrow">The thesis</span>
   <h2>You're not broke. You're in the wrong market.</h2>
  </div>
  <div>
   <p class="lede" style="margin-bottom:18px">Across the US, Canada and Europe, the entry point to owning something has moved out of reach: a first home, a rental, a small business. That holds even for people with solid incomes who did everything right.</p>
   <p>But "out of reach" is local. Whether you are stretching a fixed income into retirement or still earning and ready to build a first real asset, the same savings can buy more abroad. Three forces explain why, and each carries its own risk.</p>
  </div>
 </div>
</section>

<section>
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">The framework</span>
   <h2>Three arbitrages, three risks.</h2>
   <p class="lede">Every gap that makes a market cheaper is also a reason to be careful. We teach both sides.</p>
  </div>
  <div class="grid-3">
   <article class="card"><div class="num">1</div><h3>Currency</h3><p>Your dollar, loonie or euro goes further abroad. It can also lose ground while you hold, so the exchange rate is part of your return.</p></article>
   <article class="card"><div class="num">2</div><h3>Political</h3><p>Markets others avoid often price in more risk than exists. Sometimes they price in less. Research tells the difference.</p></article>
   <article class="card"><div class="num">3</div><h3>Structural</h3><p>How a foreigner owns and operates: entities, title, tax and getting money home. These rules decide what you actually keep.</p></article>
  </div>
 </div>
</section>

<section class="dark">
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">The members</span>
   <h2>Three practitioners. Equal seats.</h2>
   <p class="lede">Each member runs an independent practice. Every episode and seminar moves through the same three views.</p>
  </div>
  {seat_cards()}
  <div class="btn-row" style="margin-top:28px"><a href="members.html" class="btn btn-outline">Read the full bios</a></div>
 </div>
</section>

<section>
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">How it works</span>
   <h2>Learn at your own pace.</h2>
   <p class="lede">No hard sell. We would rather you be ready than early.</p>
  </div>
  <div class="ladder">
   <div class="step"><div class="step-mark">1</div><div><h3>Watch the show <span class="pill on">Free</span></h3><p style="margin:0">The thesis, the framework and real stories from the ground, in English and Spanish.</p></div></div>
   <div class="step"><div class="step-mark">2</div><div><h3>Read the research <span class="pill on">Free</span></h3><p style="margin:0">A regular research note on currency, political and structural conditions, led by Sovereo Intelligence Research.</p></div></div>
   <div class="step"><div class="step-mark">3</div><div><h3>Attend a seminar <span class="pill">Dates to the list first</span></h3><p style="margin:0">Small-format sessions in Bogotá with lectures, case studies and time on the ground.</p></div></div>
   <div class="step"><div class="step-mark">4</div><div><h3>Join the community <span class="pill">Opening soon</span></h3><p style="margin:0">Membership with a structured curriculum, a members' forum and live office hours with all three members. <a href="membership.html">Join the waitlist</a>.</p></div></div>
  </div>
 </div>
</section>

<section class="alt">
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">Straight answers</span>
   <h2>Questions people ask first.</h2>
  </div>
  {faq_html(FAQ)}
 </div>
</section>

<section class="dark">
 <div class="container text-center" style="display:flex;flex-direction:column;align-items:center">
  <span class="eyebrow">Episodes · Research · Seminars</span>
  <h2>Know the ground before you stand on it.</h2>
  <p class="lede">Join the list. New episodes, research and seminar dates go to the list first.</p>
  {signup_block()}
 </div>
</section>
"""

# ---------- members ----------
member_rows = ''.join(f"""
  <article class="member" id="{m['key']}">
   <div>
    <span class="tag tag-{m['key']}">{m['seat']} · {m['area']}</span>
    <h2>{m['name']}</h2>
    <p class="role">{m['role']}</p>
   </div>
   <div>
    <p>{m['bio']}</p>
    <p class="note"><strong>On the show:</strong> {m['show']}</p>
   </div>
  </article>""" for m in MEMBERS)

members_body = f"""
<section class="hero">
 <div class="container">
  <span class="eyebrow">The members</span>
  <h1>Three practitioners. Equal seats.</h1>
  <p class="lede">Tierra Firme brings together commercial real estate, business and operations, and intelligence research. Each member runs an independent practice, and each view checks the other two.</p>
 </div>
</section>
<section>
 <div class="container">{member_rows}
 </div>
</section>
<section class="alt">
 <div class="container grid-2">
  <div>
   <span class="eyebrow">Why three</span>
   <h2>Experience, access, research.</h2>
   <p>Valuation, operating experience and country research, from three people who work on the ground. Any one view alone misses something the other two catch.</p>
  </div>
  <div>
   <span class="eyebrow">The name</span>
   <h2>Why "Tierra Firme"</h2>
   <p>Tierra firme means solid ground. It was also the historic Spanish name for the South American mainland, a fit for a consortium built between North America and Latin America. Every episode is also produced in Spanish under the Despacho line.</p>
  </div>
 </div>
</section>
<section>
 <div class="container">
  <p class="note">Members' individual business activities are independent of one another and of Tierra Firme. Sovereo Intelligence Research provides research to Tierra Firme and takes no deal fees, advisory fees or carry.</p>
 </div>
</section>
<section class="dark">
 <div class="container text-center" style="display:flex;flex-direction:column;align-items:center">
  <h2>Get new episodes and seminar dates first.</h2>
  {signup_block()}
 </div>
</section>
"""

# ---------- show ----------
ep_rows = ''.join(f"""
   <article class="ep"><div class="n">{i+1:02d}</div><div><div class="meta">{seat}</div><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div></article>""" for i, (seat, t, d) in enumerate(EPISODES))

show_schema = {"@type": "PodcastSeries", "@id": BASE + "/the-show#series", "name": "Tierra Firme",
               "url": BASE + "/the-show", "inLanguage": ["en", "es"], "genre": ["Investing", "Business", "Economics"],
               "description": "A free show from the Tierra Firme consortium on placing capital across borders, through real estate, business and country research.",
               "publisher": {"@id": BASE + "/#org"},
               "actor": [{"@type": "Person", "name": m['name']} for m in MEMBERS]}

show_body = f"""
<section class="hero">
 <div class="container">
  <span class="eyebrow">The show · Season One</span>
  <h1>From the sidelines to a balance sheet abroad.</h1>
  <p class="lede">Twelve biweekly episodes from the thesis, to the math, to a full case study. Free, in English and Spanish, on audio and video.</p>
 </div>
</section>
<section>
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">Recurring segments</span>
   <h2>Formats that outlive any single season.</h2>
  </div>
  <div class="grid-3">
   <article class="card bar-ground"><span class="tag tag-ground">On location · Murphy</span><h3>Ground Truth</h3><p>A real, affordable property abroad on camera, and what the same income would and would not buy at home.</p></article>
   <article class="card bar-build"><span class="tag tag-build">Guest format · Shawn</span><h3>Founder's Seat</h3><p>Someone who built a business or first balance sheet abroad: what worked, what it cost and what they would redo.</p></article>
   <article class="card bar-research"><span class="tag tag-research">Every episode · Todd</span><h3>The Research Close</h3><p>A short close on currency, political and structural conditions and where they are heading.</p></article>
  </div>
  <div class="card" style="margin-top:22px"><span class="tag">Quarterly · All three</span><h3>The Case Study</h3><p>One sample deal priced, operated and stress-tested end to end on camera, as a teaching case. Not an offer.</p></div>
 </div>
</section>
<section class="alt">
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">Episode guide</span>
   <h2>Season One</h2>
   <p class="lede">Biweekly, about 42 minutes, on podcast platforms and YouTube.</p>
  </div>
  <div class="eps">{ep_rows}
  </div>
 </div>
</section>
<section>
 <div class="container grid-2">
  <div>
   <span class="eyebrow">Who it is for</span>
   <h2>Two audiences, one question.</h2>
   <ul class="checks">
    <li>Adults near or in retirement stretching a fixed income further abroad.</li>
    <li>Earners with portable income building a first real asset abroad.</li>
    <li>Families and family offices weighing Latin America for the first time.</li>
   </ul>
  </div>
  <div>
   <span class="eyebrow">How it runs</span>
   <h2>Filmed where it happens.</h2>
   <ul class="checks">
    <li>Filmed in a US studio and in market in Colombia, with the asset and the operator on camera.</li>
    <li>Despacho: every episode cut again in Spanish for bilingual audiences across the Americas.</li>
    <li>Short clips in English and Spanish for YouTube Shorts, Reels, TikTok and LinkedIn.</li>
   </ul>
  </div>
 </div>
</section>
<section class="dark">
 <div class="container text-center" style="display:flex;flex-direction:column;align-items:center">
  <span class="eyebrow">Don't miss an episode</span>
  <h2>Get notified when each episode goes live.</h2>
  {signup_block(btn='Notify me')}
 </div>
</section>
"""

# ---------- join ----------
join_body = f"""
<section class="hero">
 <div class="container grid-2" style="align-items:start">
  <div>
   <span class="eyebrow">Free list</span>
   <h1>Join the list.</h1>
   <p class="lede">New episodes, research notes and seminar dates, in your inbox first. Free, and it stays free.</p>
   {signup_block()}
   <p class="hero-fine">No spam. Unsubscribe in one click.</p>
  </div>
  <div class="card hero-card">
   <h3>What you get</h3>
   <ul class="checks">
    <li>A note when each new episode goes live</li>
    <li>Research on currency, political and structural conditions, led by Sovereo Intelligence Research</li>
    <li>First access to seminar dates in Bogotá</li>
    <li>No listings, no deals, no solicitation</li>
   </ul>
  </div>
 </div>
</section>
<section>
 <div class="container">
  <p class="note">The Tierra Firme list is separate from any member's own mailing list. We do not sell or share your address.</p>
 </div>
</section>
"""

membership_body = f"""
<section class="hero">
 <div class="container grid-2" style="align-items:start">
  <div>
   <span class="eyebrow">Membership · Opening soon</span>
   <h1>Join the community.</h1>
   <p class="lede">A members' community for people serious about placing capital in Latin America. Learn the framework, ask the three members directly, and compare notes with others doing the same work.</p>
   {signup_block(btn='Join the waitlist', ok="You're on the membership waitlist. You'll hear first when doors open.")}
   <p class="hero-fine">Waitlist is free and commits you to nothing. Education, not investment advice.</p>
  </div>
  <div class="card hero-card">
   <h3>What members get</h3>
   <ul class="checks">
    <li>A structured curriculum on evaluating a market abroad: currency, political and structural conditions</li>
    <li>Live office hours with Murphy, Shawn and Todd</li>
    <li>A members' forum to compare markets, questions and lessons</li>
    <li>Research from Sovereo Intelligence Research, and first seats at seminars in Bogotá</li>
   </ul>
  </div>
 </div>
</section>
<section>
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">How it fits</span>
   <h2>The next step after the show.</h2>
   <p class="lede">The show and the list stay free. Membership is for people who want structure, direct access to the three members and a room of peers.</p>
  </div>
  <div class="grid-3">
   <article class="card bar-ground"><span class="tag tag-ground">The asset</span><h3>Read the property</h3><p>How to judge value, title and management before anyone shows you a unit.</p></article>
   <article class="card bar-build"><span class="tag tag-build">The operation</span><h3>Read the business</h3><p>What it costs to enter, run and staff a business on the ground.</p></article>
   <article class="card bar-research"><span class="tag tag-research">The country</span><h3>Read the conditions</h3><p>The currency, policy and structural signals that set your real return.</p></article>
  </div>
 </div>
</section>
<section>
 <div class="container">
  <p class="note">Membership is educational. Tierra Firme does not list property, broker transactions or provide investment, tax or legal advice.</p>
 </div>
</section>
"""

notfound_body = """
<section class="hero" style="min-height:60vh">
 <div class="container">
  <span class="eyebrow">404</span>
  <h1>Off solid ground.</h1>
  <p class="lede">That page does not exist. Start from the home page.</p>
  <div class="btn-row" style="margin-top:24px"><a href="/" class="btn btn-gold">Go home</a></div>
 </div>
</section>
"""

PAGES = [
    ('index.html', 'Tierra Firme | Real Estate, Business and Research for Capital Abroad',
     'Tierra Firme is a consortium in commercial real estate, business and intelligence research. A free show, research and seminars for people placing capital across borders, starting with Latin America.',
     index_body, [faq_schema(FAQ)], None),
    ('members.html', 'Members | Tierra Firme',
     'Meet the Tierra Firme members: Murphy D. Cheatham II (commercial real estate, CBRE), Shawn Christopher Leamon (business and operations) and Todd Allyn (intelligence research, Sovereo).',
     members_body, [dict(m['person'], **{"memberOf": {"@id": BASE + "/#org"}}) for m in MEMBERS],
     [('', 'Home'), ('members.html', 'Members')]),
    ('the-show.html', 'The Show | Tierra Firme Season One',
     'Tierra Firme Season One: twelve free episodes on placing capital abroad, from the currency math to a full case study. In English and Spanish.',
     show_body, [show_schema], [('', 'Home'), ('the-show.html', 'The Show')]),
    ('membership.html', 'Membership | Join the Tierra Firme Community',
     'Join the waitlist for the Tierra Firme membership community: a curriculum on evaluating markets abroad, live office hours with the three members, and a members forum.',
     membership_body, [], [('', 'Home'), ('membership.html', 'Membership')]),
    ('join.html', 'Join the List | Tierra Firme',
     'Join the free Tierra Firme list for new episodes, research on currency and country conditions, and first access to seminar dates in Bogotá.',
     join_body, [], [('', 'Home'), ('join.html', 'Join the list')]),
]

for fname, title, desc, body, extra, crumbs in PAGES:
    with open(os.path.join(OUT, fname), 'w') as f:
        f.write(page(fname, title, desc, body, extra, crumbs))

nf = page('404.html', 'Page not found | Tierra Firme', 'That page does not exist.', notfound_body)
nf = nf.replace('<link rel="canonical" href="https://tierrafirme.com/404.html">', '<meta name="robots" content="noindex">')
with open(os.path.join(OUT, '404.html'), 'w') as f:
    f.write(nf)

# ---------- static files ----------
bots = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'anthropic-ai',
        'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Googlebot', 'Applebot', 'Applebot-Extended', 'Bingbot',
        'CCBot', 'meta-externalagent', 'DeepSeekBot', 'Bytespider', 'Amazonbot', 'DuckAssistBot', 'cohere-ai', 'MistralAI-User']
robots = 'User-agent: *\nAllow: /\n\n# Search and AI answer engines are welcome\n' + ''.join(f'User-agent: {b}\nAllow: /\n' for b in bots) + f'\nSitemap: {BASE}/sitemap.xml\n'
open(os.path.join(OUT, 'robots.txt'), 'w').write(robots)

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p, pr in [('', '1.0'), ('members', '0.9'), ('the-show', '0.9'), ('membership', '0.8'), ('join', '0.7')]:
    sm += f'  <url><loc>{BASE}/{p}</loc><lastmod>2026-10-16</lastmod><priority>{pr}</priority></url>\n'
sm += '</urlset>\n'
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)

llms = f"""# Tierra Firme

> A consortium of three practitioners in commercial real estate, business and family capital, and intelligence research. Tierra Firme produces a free show, research and seminars for people placing capital across borders, starting with Latin America. Based in Bogotá, Colombia. Educational only: no listings, no brokered deals, no investment advice.

## Members
- Murphy D. Cheatham II, The Ground (commercial real estate): Private Clients Director at CBRE, Dallas, advising private families and high net worth individuals.
- Shawn Christopher Leamon, The Build (business and operations): founder and managing partner of LaGrande Global (since 2013) and founder and CEO of Cielo.Travel, Bogotá.
- Todd Allyn, The Research (intelligence research): Founding Director of Sovereo Intelligence Research (https://www.sovereo.com), former Dean of the College of Business at Chancellor University. Leads Tierra Firme research.

## Pages
- [Home]({BASE}/): what Tierra Firme is, the framework and FAQ.
- [Members]({BASE}/members): full bios of the three members.
- [The Show]({BASE}/the-show): Season One, twelve biweekly episodes in English and Spanish.
- [Membership]({BASE}/membership): waitlist for the paid community (curriculum, office hours, forum), opening soon.
- [Join the list]({BASE}/join): free list for episodes, research and seminar dates.

## Notes
- Sovereo Intelligence Research provides research to Tierra Firme and takes no deal fees, advisory fees or carry.
- Nothing published by Tierra Firme is investment, tax or legal advice.
"""
open(os.path.join(OUT, 'llms.txt'), 'w').write(llms)

redirects = """/the-seats.html /members 301
/the-seats /members 301
/get-the-read.html /join 301
/get-the-read /join 301
/tierra-firme.html / 301
/tierra-firme-episodes.html /the-show 301
/tierra-firme-hosts.html /members 301
/tierra-firme-subscribe.html /join 301
"""
open(os.path.join(OUT, '_redirects'), 'w').write(redirects)

favicon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#061327" stroke="#e9a825" stroke-width="3"/><text x="32" y="40" text-anchor="middle" font-family="Georgia,serif" font-size="22" font-weight="700" fill="#e9a825">TF</text></svg>"""
open(os.path.join(OUT, 'favicon.svg'), 'w').write(favicon)
print('built', sorted(os.listdir(OUT)))
