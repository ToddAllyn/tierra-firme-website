#!/usr/bin/env python3
"""Builds the Tierra Firme static site into ../tierra-firme-website."""
import json, os, html, re

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
.brand img{display:block;height:52px;width:auto}
.hero-logo{display:block;width:min(360px,70vw);height:auto;margin:0 0 30px}
footer .brand img{height:64px}
.brand-mark{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:50%;border:1.5px solid var(--gold);color:var(--gold);font-size:.8rem;font-weight:700;background:rgba(233,168,37,.08);font-family:'Inter',sans-serif}
.main-nav{display:flex;align-items:center;gap:2px}
.main-nav a{padding:8px 13px;font-size:.92rem;font-weight:500;color:rgba(255,255,255,.84);border-radius:4px;text-decoration:none}
.main-nav a:hover,.main-nav a[aria-current=page]{color:#fff;background:rgba(255,255,255,.08)}
.main-nav a.btn{margin-left:10px;color:var(--navy)}
.nav-toggle{display:none;background:none;border:1px solid rgba(255,255,255,.25);color:#fff;font-size:1.3rem;line-height:1;padding:8px 12px;border-radius:4px;cursor:pointer}
@media (max-width:1080px){
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
.dark .tag-cre{color:#f08a5d}.dark .tag-capital{color:#3cc4a4}.dark .tag-research{color:#7fb0ea}
.card .num{font-family:'Fraunces',serif;font-size:2rem;color:var(--gold-d);line-height:1;margin-bottom:12px}
.bar-cre{border-top:3px solid var(--terracotta)}.bar-capital{border-top:3px solid var(--teal)}.bar-research{border-top:3px solid var(--sky)}
.tag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:12px}
.tag-cre{color:var(--terracotta)}.tag-capital{color:var(--teal)}.tag-research{color:var(--sky)}
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
.signup input[type=email]{flex:1 1 240px;min-width:0;min-height:48px;padding:0 16px;font:inherit;border:1.5px solid var(--border);border-radius:4px;background:#fff;color:var(--ink)}
.dark .signup input[type=email]{border-color:rgba(255,255,255,.3)}
.status{min-height:1.6em;margin-top:10px;font-size:.95rem}
.checks{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:12px}
.checks li{padding-left:28px;position:relative;color:var(--muted)}
.checks li::before{content:"";position:absolute;left:0;top:.55em;width:14px;height:8px;border-left:2px solid var(--gold-d);border-bottom:2px solid var(--gold-d);transform:rotate(-45deg)}

.hero-card{background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.16)}
.hero-card h3{color:#fff}.hero-card .checks li{color:rgba(255,255,255,.82)}
.hero .checks li::before{border-color:var(--gold)}
.trailer{background:radial-gradient(ellipse at 50% 30%,#12355f 0%,#0a1f3d 45%,#061327 80%);color:#fff;padding:clamp(56px,7vw,88px) 0}
.trailer{overflow:hidden}
.trailer h2{color:#fff}.trailer .eyebrow{color:var(--gold)}
.player{position:relative;background:#000;box-shadow:0 40px 120px rgba(0,0,0,.75),0 0 0 1px rgba(233,168,37,.35),0 0 0 8px rgba(0,0,0,.35);border-radius:3px}
.player::before{content:'';position:absolute;inset:-40px -60px;background:radial-gradient(ellipse at 50% 50%,rgba(233,168,37,.10),rgba(0,0,0,0) 60%);z-index:-1}
.trailer .container{position:relative}
.player{max-width:min(100%,calc((100vh - 140px) * 16 / 9));margin:0 auto;scroll-margin-top:96px}
.theater-dim{position:fixed;inset:0;background:rgba(2,6,14,.86);opacity:0;pointer-events:none;transition:opacity .45s;z-index:60}
body.theater .theater-dim{opacity:1;pointer-events:auto}
body.theater .player{z-index:61}
body.theater .site-header{opacity:.15;transition:opacity .45s}
.theater-exit{position:fixed;top:18px;right:18px;z-index:62;display:none;font:600 14px Inter,sans-serif;color:#fff;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:10px 16px;cursor:pointer}
body.theater .theater-exit{display:block}
#trailer{scroll-margin-top:76px}
.player video{display:block;width:100%;height:auto;aspect-ratio:16/9;background:#000;cursor:pointer}
.player .sound,.player .replay{position:absolute;right:18px;bottom:18px;z-index:2;font:600 15px Inter,sans-serif;color:#061327;background:#e9a825;border:0;border-radius:999px;padding:12px 20px;cursor:pointer;box-shadow:0 6px 24px rgba(0,0,0,.5)}
.player .sound:hover,.player .replay:hover{background:#f3c76a}
.player .replay{left:50%;right:auto;bottom:50%;transform:translate(-50%,50%);font-size:18px;padding:16px 28px}
.trailer-fine{margin-top:16px;font-size:.88rem;color:rgba(255,255,255,.55)}
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
.portrait{display:block;width:var(--ps,72px);height:var(--ps,72px);border-radius:50%;object-fit:cover;border:2px solid var(--gold);background:var(--navy);margin-bottom:16px;flex:none}
.monogram{display:flex;align-items:center;justify-content:center;font-family:'Fraunces',serif;font-weight:500;font-size:calc(var(--ps,72px) * .36);letter-spacing:.02em;color:var(--gold-l);background:radial-gradient(circle at 30% 25%,#12355f,var(--navy) 70%)}
.portrait-lg{--ps:min(320px,70vw);margin:0 auto}
.disclaimer{font-size:.9rem;font-weight:600;color:rgba(255,255,255,.85);margin:0 0 8px}

/* event: photo hero */
:root{--green:#123d2c;--green-2:#1c5640;--hair:rgba(233,168,37,.55)}
.photo-hero{position:relative;min-height:min(92vh,880px);display:flex;align-items:flex-end;color:#fff;overflow:hidden;background:var(--navy);padding:0}
.photo-hero picture,.photo-hero .ph-img{position:absolute;inset:0;width:100%;height:100%}
.photo-hero .ph-img{object-fit:cover;object-position:center 60%}
.photo-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,19,39,.82) 0%,rgba(6,19,39,.55) 45%,rgba(6,19,39,.1) 80%),linear-gradient(180deg,rgba(6,19,39,.6) 0%,rgba(6,19,39,.2) 35%,rgba(6,19,39,.8) 75%,rgba(6,19,39,.97) 100%)}
@media (max-width:760px){.photo-hero::after{background:linear-gradient(180deg,rgba(6,19,39,.7) 0%,rgba(6,19,39,.55) 40%,rgba(6,19,39,.88) 75%,rgba(6,19,39,.98) 100%)}}
.photo-hero>.container{position:relative;z-index:2;width:100%;padding-top:clamp(120px,18vh,200px);padding-bottom:clamp(44px,7vw,80px)}
.photo-hero h1{color:#fff;font-size:clamp(2.6rem,6.4vw,5.6rem);font-weight:500;letter-spacing:-.02em;max-width:14ch}
.photo-hero .lede{color:rgba(255,255,255,.86);font-size:clamp(1.05rem,1.6vw,1.25rem)}
.photo-hero .ph-credit{position:absolute;right:12px;bottom:8px;z-index:3;font-size:.68rem;color:rgba(255,255,255,.55);margin:0}
.photo-hero .ph-credit a{color:inherit}
.kicker{display:inline-flex;flex-wrap:wrap;align-items:center;gap:10px 14px;font-size:.74rem;font-weight:600;letter-spacing:.28em;text-transform:uppercase;color:var(--gold-l);margin-bottom:22px}
.kicker .rule{width:44px;height:1px;background:var(--gold)}
.event-strip{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);margin-top:clamp(34px,5vw,56px)}
.event-strip div{padding:18px 18px 16px;border-left:1px solid rgba(233,168,37,.25)}
.event-strip div:first-child{border-left:0;padding-left:0}
.event-strip b{display:block;font-family:'Fraunces',serif;font-weight:500;font-size:clamp(1.5rem,2.6vw,2.2rem);color:#fff;line-height:1.1}
.event-strip span{font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.62)}
@media (max-width:760px){.event-strip{grid-template-columns:repeat(2,minmax(0,1fr))}.event-strip div:nth-child(3){border-left:0;padding-left:0}.event-strip div:nth-child(n+3){border-top:1px solid rgba(233,168,37,.25)}}
.btn-ghost{border-color:var(--hair);color:#fff}.btn-ghost:hover{background:rgba(233,168,37,.12)}

/* editorial bands */
.band-green{background:var(--green);color:#fff}
.band-green h2,.band-green h3{color:#fff}.band-green p{color:rgba(255,255,255,.8)}.band-green .eyebrow{color:var(--gold-l)}
.split{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:clamp(28px,5vw,72px);align-items:center}
.split.rev>figure{order:2}
@media (max-width:860px){.split{grid-template-columns:1fr}.split.rev>figure{order:0}}
figure{margin:0}
.photo{position:relative;overflow:hidden;border-radius:2px;box-shadow:0 30px 80px rgba(6,19,39,.28)}
.photo img{display:block;width:100%;height:100%;object-fit:cover}
.photo.tall{aspect-ratio:4/5}.photo.wide{aspect-ratio:3/2}
figcaption{font-size:.74rem;color:var(--muted-2);margin-top:10px;line-height:1.5}
.dark figcaption,.band-green figcaption{color:rgba(255,255,255,.55)}
figcaption a{color:inherit}
.gallery{display:grid;grid-template-columns:2fr 1fr;gap:18px;align-items:start}
.gallery .col{display:flex;flex-direction:column;gap:18px}
@media (max-width:760px){.gallery{grid-template-columns:1fr}}
.quote{font-family:'Fraunces',serif;font-weight:500;font-size:clamp(1.5rem,2.8vw,2.3rem);line-height:1.3;color:#fff;max-width:28ch;margin:0}

/* program */
.program{display:flex;flex-direction:column;border-top:1px solid var(--border)}
.day{display:grid;grid-template-columns:minmax(0,220px) minmax(0,1fr);gap:clamp(18px,4vw,56px);padding:clamp(26px,4vw,40px) 0;border-bottom:1px solid var(--border)}
.day .when{font-size:.74rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-d)}
.day .when b{display:block;font-family:'Fraunces',serif;font-size:2.4rem;letter-spacing:0;text-transform:none;color:var(--ink);font-weight:500;line-height:1.1;margin:6px 0 4px}
.day h3{font-size:1.6rem;margin-bottom:12px}
.slot{display:grid;grid-template-columns:120px minmax(0,1fr);gap:14px;padding:10px 0;border-top:1px dashed var(--border)}
.slot:first-of-type{border-top:0}
.slot .t{font-size:.76rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted-2);padding-top:3px}
.slot p{margin:0}
@media (max-width:760px){.day{grid-template-columns:1fr}.slot{grid-template-columns:1fr;gap:2px}}
.facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px;border-top:1px solid var(--border);margin:0}
.facts div{padding:18px 0;border-bottom:1px solid var(--border)}
.facts dt{font-size:.72rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--gold-d);margin-bottom:4px}
.facts dd{margin:0;color:var(--ink)}
@media (max-width:640px){.facts{grid-template-columns:1fr}}
.faculty{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
@media (max-width:900px){.faculty{grid-template-columns:1fr}}
a.card{text-decoration:none;display:block}
a.card:hover h3{color:var(--gold-d)}
.dark a.card:hover h3{color:var(--gold-l)}

/* lanes */
.lane-link{display:inline-block;margin-top:14px;font-weight:600;font-size:.92rem;color:var(--gold-d);text-decoration:none}
.dark .lane-link{color:var(--gold-l)}
.draft-banner{background:#fff3cd;color:#5c4400;border-bottom:1px solid #e9cf7a;font-size:.88rem;padding:10px 0;text-align:center}
.lane-chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 26px}
.lane-chips a{font:600 .82rem Inter,sans-serif;letter-spacing:.06em;padding:9px 16px;border-radius:999px;border:1px solid var(--border);background:var(--surface);color:var(--ink);text-decoration:none;cursor:pointer}
.lane-chips a[aria-pressed=true]{background:var(--navy);color:#fff;border-color:var(--navy)}
.qcard .tag{margin-bottom:8px}
.qlane{scroll-margin-top:96px;margin-bottom:34px}
.qlane h2{font-size:1.5rem}

/* signup lanes */
.lanes-pick{flex:1 1 100%;border:0;margin:14px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px 18px;max-width:640px}
.lanes-pick legend{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600;margin-bottom:8px;color:var(--muted);padding:0}
.dark .lanes-pick legend,.hero .lanes-pick legend,.band-green .lanes-pick legend{color:rgba(255,255,255,.7)}
.lanes-pick label{display:inline-flex;align-items:center;gap:8px;font-size:.95rem;cursor:pointer}
.lanes-pick input{width:18px;height:18px;min-height:0;flex:none;margin:0;accent-color:var(--gold)}
.text-center .lanes-pick{justify-content:center}
.signup-wrap{width:100%;max-width:640px}
.text-center .signup-wrap{margin:0 auto}
.text-center .signup{margin-inline:auto}
"""

NAV = [('index.html', 'Home'), ('bogota-2027.html', 'Bogotá 2027'), ('members.html', 'Members'), ('the-show.html', 'The Show'), ('questions.html', 'Questions'), ('membership.html', 'Membership')]

DISCLAIMER = "Educational content. Not investment, tax or legal advice."

# The three lanes. `id` is what the signup form stores in KV; `key` drives CSS colors.
# `approved` stays False until the member signs off on his lane page copy: unapproved pages
# carry a draft banner and a noindex tag, and stay out of the sitemap and llms.txt.
LANES = [
    dict(id='cre', key='cre', slug='commercial-real-estate', label='Commercial real estate', seat='The Asset',
         member='Murphy D. Cheatham II', first='Murphy', approved=False),
    dict(id='capital', key='capital', slug='business-and-family-capital', label='Business and family capital', seat='The Capital',
         member='Shawn Christopher Leamon', first='Shawn', approved=False),
    dict(id='research', key='research', slug='research', label='Research', seat='The Country',
         member='Todd Allyn', first='Todd', approved=False),
]
LANE = {l['id']: l for l in LANES}

# Event: Tierra Firme Investor Lab, Bogotá. Dates and seat count come from the 2027 Investor Lab draft.
EVENT = dict(name='Tierra Firme Investor Lab', city='Bogotá', start='2027-03-07', end='2027-03-12',
             dates='7 to 12 March 2027', short='March 2027', seats=30)

# Photos: Wikimedia Commons. Licenses read on each File: page on 2026-11-20. BY and BY-SA need the credit line.
PHOTOS = {
    'twilight': dict(base='/img/bogota/bogota-twilight-from-monserrate', w=(1920, 960), ratio=(1920, 1080),
                     alt='Bogotá at twilight, seen from Monserrate, city lights spreading toward the savanna',
                     title='Bogotá at twilight from Monserrate', author='Danielcgold', lic='CC BY-SA 4.0',
                     lic_url='https://creativecommons.org/licenses/by-sa/4.0/',
                     src='https://commons.wikimedia.org/wiki/File:Dan-gold-bogota-city-night-montserrate.jpg'),
    'towers': dict(base='/img/bogota/towers-below-monserrate', w=(1920, 960), ratio=(1920, 1280),
                   alt='Office and residential towers of central Bogotá with Monserrate and the Eastern Hills behind',
                   title='Central Bogotá towers below Monserrate', author='Jos Cuevasc', lic='CC BY-SA 4.0',
                   lic_url='https://creativecommons.org/licenses/by-sa/4.0/',
                   src='https://commons.wikimedia.org/wiki/File:Monserrate_y_centro_de_Bogota.jpg'),
    'downtown': dict(base='/img/bogota/downtown-from-torre-colpatria', w=(1920, 960), ratio=(1920, 1440),
                     alt='Downtown Bogotá high-rises seen from the Torre Colpatria observation deck',
                     title='Downtown Bogotá from the Torre Colpatria observation deck', author='Peter Chovanec', lic='CC BY 2.0',
                     lic_url='https://creativecommons.org/licenses/by/2.0/',
                     src='https://commons.wikimedia.org/wiki/File:Bogota_z_Mirador_Torre_Colpatria_(34553345656).jpg'),
    'colpatria': dict(base='/img/bogota/torre-colpatria-night', w=(900, 600), ratio=(900, 1600),
                      alt='Torre Colpatria lit at night in yellow, blue and red, with the city below',
                      title='Torre Colpatria at night', author='ProtoplasmaKid', lic='CC BY-SA 4.0',
                      lic_url='https://creativecommons.org/licenses/by-sa/4.0/',
                      src='https://commons.wikimedia.org/wiki/File:Vista_a%C3%A9rea_Bogot%C3%A1_-_15_-_Torre_Colpatria.jpg'),
    'general': dict(base='/img/bogota/bogota-general-view', w=(1600, 960), ratio=(1600, 1067),
                    alt='Wide view over Bogotá, its high-rise center and the flat savanna beyond',
                    title='Bogotá, general view', author='Raul Cuellar', lic='CC0 1.0',
                    lic_url='https://creativecommons.org/publicdomain/zero/1.0/',
                    src='https://commons.wikimedia.org/wiki/File:Bogota_general_view_2015.jpg'),
}

ILLUSTRATIVE = {
    'ballroom': ('seminar-ballroom', 'An intimate hotel ballroom set for a seminar, rows of upholstered chairs facing a screen, mountains at dusk through tall windows'),
    'lobby': ('hotel-lobby', 'A modern luxury hotel lobby lounge in stone, walnut and brass, with green velvet armchairs'),
    'boardroom': ('boardroom', 'A high-floor boardroom with a long wood table and leather chairs, a city of towers and green mountains beyond the glass'),
    'foyer': ('conference-foyer', 'A bright conference foyer with a navy and gold registration desk and cocktail tables'),
    'library': ('library-lounge', 'A hotel library lounge with dark wood shelves, leather club chairs and a fireplace, city lights at dusk outside'),
}
for k, (f, alt) in ILLUSTRATIVE.items():
    PHOTOS[k] = dict(base='/img/illustrative/' + f, w=(1920, 960), ratio=(1920, 1080), alt=alt + ' (illustrative image)',
                     title='Illustrative image, not the venue', ill=True)

def credit(p):
    p = PHOTOS[p]
    if p.get('ill'):
        return 'Generated illustration for Tierra Firme.'
    return f'Photo: <a href="{p["src"]}" rel="noopener">{html.escape(p["author"])}</a>, <a href="{p["lic_url"]}" rel="noopener">{p["lic"]}</a>, via Wikimedia Commons'

def img(p, sizes='100vw', cls='', eager=False):
    x = PHOTOS[p]
    big, small = x['w']
    w, h = x['ratio']
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="{x["base"]}-{small}.webp" srcset="{x["base"]}-{small}.webp {small}w, {x["base"]}-{big}.webp {big}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{html.escape(x["alt"])}" {load}>')

def fig(p, cls='wide', sizes='(max-width:860px) 100vw, 50vw'):
    return f'<figure><div class="photo {cls}">{img(p, sizes)}</div><figcaption>{html.escape(PHOTOS[p]["title"])}. {credit(p)}</figcaption></figure>'

def photo_hero(p, inner):
    return (f'<section class="photo-hero"><picture>{img(p, "100vw", "ph-img", eager=True)}</picture>'
            f'<div class="container">{inner}</div><p class="ph-credit">{credit(p)}</p></section>')

def hero_preload(p):
    x = PHOTOS[p]
    big, small = x['w']
    return (f'<link rel="preload" as="image" href="{x["base"]}-{small}.webp" imagesrcset="{x["base"]}-{small}.webp {small}w, '
            f'{x["base"]}-{big}.webp {big}w" imagesizes="100vw" fetchpriority="high">')

def event_strip():
    return ('<div class="event-strip"><div><b>6 days</b><span>5 nights · 7 to 12 March 2027</span></div><div><b>3 lanes</b><span>Asset · Capital · Country</span></div>'
            '<div><b>30 seats</b><span>An intimate room</span></div><div><b>0</b><span>Properties for sale</span></div></div>')

LEGAL = ("Tierra Firme is educational content and seminars. Nothing here is investment, tax or legal advice, "
         "an offer to sell, or a solicitation of an offer to buy any security or property. Cross-border investing "
         "carries currency, country and tax risk. Each member runs an independent practice; any professional "
         "engagement with a member happens through that member's own firm, separate from Tierra Firme.")

FAQ = [
    ("What is Tierra Firme?",
     "Tierra Firme is a consortium of three practitioners in commercial real estate, business and family capital, and intelligence research. "
     "It produces a free show, research and seminars for people placing capital across borders, starting with Latin America."),
    ("Who is behind Tierra Firme?",
     "Murphy D. Cheatham II (commercial real estate), Shawn Christopher Leamon (business and family capital) and Todd Allyn "
     "(research). Each runs an independent practice and teaches his own lane."),
    ("What is the Bogotá 2027 Investor Lab?",
     "Six days and five nights in Bogotá, arriving Sunday 7 March 2027 and leaving Friday 12 March, for 30 people: short boardroom briefings each morning, verified field visits in the afternoon and cultural evenings, with three days on Colombian commerce. "
     "It is a seminar, not a sales event. Details go to the waitlist first."),
    ("Who is Tierra Firme for?",
     "Individuals, families and family offices in the US, Canada and Europe who want to understand a market abroad before committing capital, "
     "including households priced out of ownership at home and retirees stretching a fixed income."),
    ("Is Tierra Firme free?",
     "The show and the email list are free. Seminars are paid and announced to the list first. A paid membership community is opening soon; join the waitlist for first access."),
    ("What is the Tierra Firme membership?",
     "A paid community opening soon: a structured curriculum on evaluating markets abroad, a members' forum, and live office hours with "
     "Murphy, Shawn and Todd. It is education, not investment advice. The waitlist gets first access."),
    ("Does Tierra Firme sell property or arrange transactions?",
     "No. Tierra Firme teaches how to read a market before you commit. It does not list property, arrange transactions or take fees on what anyone buys."),
    ("Is anything from Tierra Firme investment advice?",
     "No. Everything Tierra Firme publishes is educational. It is not investment, tax or legal advice. Decisions stay with you and your own advisers."),
    ("Who leads the research?",
     "Todd Allyn leads Tierra Firme research: the economic, currency and country conditions behind each episode and seminar. "
     "Murphy and Shawn each lead their own lanes."),
    ("Where is Tierra Firme based?",
     "Tierra Firme is based in Dallas and Bogotá, and we work globally. The first seminar is in Bogotá, which holds the central bank, tax authority, notaries and ministries every foreign investor deals with."),
]

MEMBERS = [
    dict(key='cre', lane='cre', seat='The Asset', area='Commercial real estate', name='Murphy D. Cheatham II', short='Murphy Cheatham', photo='/img/members/murphy-cheatham', initials='MC',
         role='Private Clients Director, CBRE · Global',
         show='The asset: how property is valued, owned and managed, and what a buyer from abroad should understand before committing.',
         bio=("Murphy D. Cheatham II is Private Clients Director at CBRE, a global role in which he advises private families and high net worth "
              "individuals on commercial real estate. In more than two decades he has sourced and serviced debt and equity, optimized portfolios "
              "and managed properties, led strategic planning on more than $300 million in mixed-use projects in partnership with HDR, and served as "
              "Chief of Housing and Business Development for the City of Shreveport. He holds a B.S. in Accounting from Grambling State University "
              "and a Master of Real Estate Development from Arizona State University, and helped create the real estate partnership between the two schools. "
              "He hosts The Murphy Cheatham Podcast."),
         person={"@type": "Person", "name": "Murphy D. Cheatham II", "alternateName": "Murphy Cheatham", "image": BASE + "/img/members/murphy-cheatham-640.webp",
                 "jobTitle": "Private Clients Director",
                 "worksFor": {"@type": "Organization", "name": "CBRE", "url": "https://www.cbre.com"},
                 "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Grambling State University"},
                              {"@type": "CollegeOrUniversity", "name": "Arizona State University"}],
                 "sameAs": ["https://www.cbre.com/people/murphy-cheatham"]}),
    dict(key='capital', lane='capital', seat='The Capital', area='Business and family capital', name='Shawn Christopher Leamon', short='Shawn Leamon', photo='/img/members/shawn-leamon', initials='SL',
         role='Founder and Managing Partner, LaGrande Global · Founder and CEO, Cielo.Travel · Bogotá',
         show='The capital: how individuals and families build, run and hold a business abroad, what it costs to enter and what it takes to operate.',
         bio=("Shawn Christopher Leamon is founder and managing partner of LaGrande Global, the investment firm he started in 2013, which manages "
              "close to $100 million across private equity, startups, real estate and public markets, with a focus on Latin America. Before that he "
              "worked in investment banking and wealth management on portfolios of more than $1 billion. He also built and sold a marketing agency, "
              "and is founder and CEO of Cielo.Travel, one of Colombia's largest digital travel networks. Born in Dallas, he has lived in Bogotá since 2023. "
              "He holds degrees in Economics and Philosophy from Dartmouth College and an MBA from IE Business School."),
         person={"@type": "Person", "name": "Shawn Christopher Leamon", "alternateName": "Shawn Leamon", "image": BASE + "/img/members/shawn-leamon-640.webp",
                 "jobTitle": "Founder and Managing Partner",
                 "worksFor": [{"@type": "Organization", "name": "LaGrande Global", "url": "https://lagrandeglobal.com"},
                              {"@type": "Organization", "name": "Cielo.Travel", "url": "https://cielo.travel"}],
                 "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Dartmouth College"},
                              {"@type": "CollegeOrUniversity", "name": "IE Business School"}],
                 "sameAs": ["https://lagrandeglobal.com/shawn-leamon/", "https://cielo.travel/meet-our-ceo-shawn-christopher-leamon/"]}),
    dict(key='research', lane='research', seat='The Country', area='Research', name='Todd Allyn', short='Todd Allyn', photo='/img/members/todd-allyn', initials='TA',
         role='Research lead · Founding Director, Sovereo Intelligence Research · Bogotá',
         show='The country: the economic, currency and political conditions that decide what you keep, and the signals that they are changing.',
         bio=("Todd Allyn leads Tierra Firme research. He is Founding Director of Sovereo Intelligence Research, a research company that tracks how "
              "geopolitics, currencies and policy change the options open to families and firms placing capital across borders. Sovereo turns those "
              "conditions into a read a decision-maker can act on: a daily SITREP on what changed, Country Dossiers on the places they are weighing, "
              "and the Decision Forecast, a public record of forecasts scored against what actually happened, so the track record can be checked. Its "
              "<a href=\"https://www.sovereo.com/deal-record\" rel=\"noopener\">Global Deal Record</a> tracks business deals worldwide from official "
              "sources, with US$46 billion in verified deals logged in 2026. He hosted The Todd Allyn Show on iHeartRadio and has lived in Bogotá since 2020."),
         person={"@type": "Person", "name": "Todd Allyn", "jobTitle": "Founding Director", "image": BASE + "/img/members/todd-allyn-640.webp",
                 "worksFor": {"@type": "Organization", "name": "Sovereo Intelligence Research", "url": "https://www.sovereo.com"},
                 "sameAs": ["https://www.linkedin.com/in/toddallyn/", "https://www.youtube.com/@sovereointel", "https://www.sovereo.com"]}),
]

def portrait(m, size=72, cls=''):
    """Member photo when we have one; otherwise a gold monogram until the member sends a photo."""
    if m.get('photo'):
        return (f'<img class="portrait {cls}" style="--ps:{size}px" src="{m["photo"]}-{320 if size <= 160 else 640}.webp" '
                f'width="{size}" height="{size}" alt="{html.escape(m["name"])}" loading="lazy" decoding="async">')
    return f'<div class="portrait monogram {cls}" style="--ps:{size}px" role="img" aria-label="{html.escape(m["name"])}">{m["initials"]}</div>'

EPISODES = [
    ('All three', 'The World Is Mispriced', "The founding thesis: you're not broke, you're in the wrong market. Currency, political and structural conditions put the first rung back within reach abroad."),
    ('Research', 'The Arbitrage, in Numbers', 'The math: how home-currency income and savings change in value the moment they cross the border.'),
    ('Asset', 'Real Assets, Real Prices', 'What entry-level property abroad costs, and how to judge it against being priced out at home.'),
    ('Capital', 'Buy the Business, Not Just the Building', 'Starting or buying a small business abroad, where the cost of entry is within reach and the income is real.'),
    ('Research', 'Strong Dollar, Weak Dollar', 'How the picture changes with your currency, dollar, loonie or euro, when it is strong and when it turns.'),
    ('Research', 'The Currency Trap', 'The other side of the trade: how depreciation eats into what you keep, and how structure can limit the damage.'),
    ('Asset', 'Earning Locally, Bringing It Home', 'How property and business income is earned in another currency, and what it takes to bring the money home.'),
    ('Capital', 'Boots on the Ground', 'Why this cannot be done from a laptop: the teams, trust and presence it takes to operate abroad.'),
    ('Asset', 'Colombia: The Beachhead', 'A market study and an honest look at political risk, up close.'),
    ('All three', 'The Teaching Case', 'A sample property and a sample business, priced, run and stress-tested on camera as a classroom exercise. Illustrative only.'),
    ('Capital', 'Entities, Taxes and Getting Paid', 'Structure in practice: owning as a foreigner, repatriating capital and staying clean with the IRS.'),
    ('Asset', 'The Multinational Balance Sheet', 'Season finale: assets and businesses abroad, assembled into one durable balance sheet.'),
]

def jsonld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + '\n</script>'

def page(fname, title, desc, body, schema_extra=(), crumbs=None, preload=None, noindex=False, banner=''):
    slug = '' if fname == 'index.html' else fname.replace('.html', '')
    url = BASE + '/' + slug
    nav = ''.join(f'<a href="{h}"{" aria-current=page" if h == fname else ""}>{t}</a>' for h, t in NAV)
    if '/' in fname:  # nested pages: make relative nav links root-relative before the rewrite below
        body = re.sub(r'href="(?!https?:|/|#|mailto:)([a-z0-9\-]+\.html)', r'href="/\1', body)
    graph = [
        {"@type": "WebSite", "@id": BASE + "/#website", "name": "Tierra Firme", "url": BASE + "/", "inLanguage": "en",
         "publisher": {"@id": BASE + "/#org"}},
        {"@type": "Organization", "@id": BASE + "/#org", "name": "Tierra Firme", "url": BASE + "/", "logo": BASE + "/img/logo-full.png",
         "description": "A consortium of three practitioners in commercial real estate, business and family capital, and intelligence research, producing a free show, research and seminars on placing capital across borders.",
         "areaServed": ["Worldwide", "Latin America", "Colombia"],
         "knowsAbout": ["Commercial real estate", "Family office", "Foreign investment in Colombia", "Currency risk", "Country risk", "Intelligence research"],
         "member": [m['person'] for m in MEMBERS]},
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc,
         "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BASE + "/#org"}, "dateModified": "2026-11-20"},
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
{'<meta name="robots" content="noindex">' if noindex else ''}<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
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
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap"></noscript>
{preload or '<link rel="preload" as="image" href="/img/logo-light.webp" fetchpriority="high">'}
{jsonld({"@context": "https://schema.org", "@graph": graph})}
<style>{CSS}</style>
</head>
<body>
{banner}<header class="site-header">
 <div class="container nav-wrap">
  <a href="index.html" class="brand"><img src="/img/logo-light.webp" alt="Tierra Firme" width="120" height="56"></a>
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
   <a href="index.html" class="brand"><img src="/img/logo-light.webp" alt="Tierra Firme" width="120" height="56"></a>
   <nav class="footer-nav" aria-label="Footer">{''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}<a href="credits.html">Photo credits</a></nav>
  </div>
  <p class="disclaimer">{DISCLAIMER}</p>
  <p class="legal">{LEGAL}</p>
  <p class="credit">&copy; 2026 Tierra Firme. Murphy D. Cheatham II, Shawn Christopher Leamon and Todd Allyn.</p>
 </div>
</footer>
<script>
(function(){{
 var t=document.querySelector('.nav-toggle'),n=document.getElementById('main-nav');
 if(t&&n){{t.addEventListener('click',function(){{var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');}});}}
 var v=document.getElementById('tf-trailer');
 if(v){{var sb=document.getElementById('tf-sound'),rb=document.getElementById('tf-replay');
  var go=function(){{var p=v.play();if(p&&p.catch)p.catch(function(){{}});}};
  var check=function(){{var r=v.getBoundingClientRect(),h=window.innerHeight||document.documentElement.clientHeight;var vis=Math.max(0,Math.min(r.bottom,h)-Math.max(r.top,0))/Math.max(1,r.height);if(vis>.4){{if(v.paused&&!v.ended)go();}}else if(!v.paused&&vis<.15){{v.pause();leave();}}}};
  ['scroll','resize','load','hashchange'].forEach(function(ev){{window.addEventListener(ev,check,{{passive:true}});}});
  if('IntersectionObserver' in window){{new IntersectionObserver(check,{{threshold:[0,.15,.4,.7]}}).observe(v);}}
  setTimeout(check,300);
  var dim=document.getElementById('tf-dim'),ex=document.getElementById('tf-exit');
  var center=function(){{var r=v.getBoundingClientRect();window.scrollTo({{top:window.pageYOffset+r.top-(window.innerHeight-r.height)/2,behavior:'smooth'}});}};
  var enter=function(){{document.body.classList.add('theater');center();}};
  var leave=function(){{document.body.classList.remove('theater');}};
  dim.addEventListener('click',leave);ex.addEventListener('click',leave);
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')leave();}});
  sb.addEventListener('click',function(){{v.muted=false;v.volume=1;if(v.ended)v.currentTime=0;go();v.controls=true;sb.hidden=true;enter();}});
  v.addEventListener('play',function(){{if(!v.muted)enter();}});
  v.addEventListener('click',function(){{if(v.muted){{sb.click();}}}});
  v.addEventListener('ended',function(){{rb.hidden=false;leave();}});
  rb.addEventListener('click',function(){{rb.hidden=true;v.currentTime=0;go();enter();}});
 }}
 var chips=document.querySelectorAll('[data-lane-filter]');
 if(chips.length){{var show=function(id){{chips.forEach(function(c){{c.setAttribute('aria-pressed',c.getAttribute('data-lane-filter')===id?'true':'false');}});
   document.querySelectorAll('.qlane').forEach(function(sec){{sec.hidden=!(id==='all'||sec.id==='lane-'+id);}});}};
  chips.forEach(function(c){{c.addEventListener('click',function(e){{e.preventDefault();var id=c.getAttribute('data-lane-filter');show(id);history.replaceState(null,'',id==='all'?location.pathname:'#lane-'+id);}});}});
  var h=location.hash.replace('#lane-','');if(h&&document.getElementById('lane-'+h))show(h);}}
 var f=document.getElementById('signup');
 if(f){{var i=f.querySelector('input[type=email]'),s=document.getElementById('signup-status');
  f.addEventListener('submit',function(e){{e.preventDefault();
   if(!i.value||!i.checkValidity()){{s.textContent='Enter a valid email address.';i.focus();return;}}
   var b=f.querySelector('button');b.disabled=true;s.textContent='Sending...';
   fetch('/subscribe',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{email:i.value.trim(),source:f.getAttribute('data-source')||location.pathname,lanes:Array.prototype.map.call(f.querySelectorAll('input[name=lanes]:checked'),function(c){{return c.value;}})}})}})
    .then(function(r){{return r.json().catch(function(){{return {{}};}}).then(function(j){{if(!r.ok||!j.ok)throw new Error(j.error||'');s.textContent=f.getAttribute('data-ok');i.value='';}});}})
    .catch(function(err){{s.textContent=(err&&err.message)||'That did not go through. Try again.';}})
    .then(function(){{b.disabled=false;}});
  }});
 }}
}})();
</script>
</body>
</html>
"""
    out = re.sub(r'href="index\.html(#[^"]*)?"', lambda m: 'href="/' + (m.group(1) or '') + '"', out)
    out = re.sub(r'href="(?!https?:|/|#|mailto:)([a-z0-9/\-]+)\.html(#[^"]*)?"', lambda m: 'href="/' + m.group(1) + (m.group(2) or '') + '"', out)
    return out


def signup_block(dark=True, btn='Join the community', ok="You're on the waitlist. Bogotá 2027 details, new episodes and research come to you first.", source='', preset=()):
    boxes = ''.join(f'<label><input type="checkbox" name="lanes" value="{l["id"]}"{" checked" if l["id"] in preset else ""}> {l["label"]}</label>' for l in LANES)
    return f"""<div class="signup-wrap"><form class="signup" id="signup" novalidate data-ok="{html.escape(ok)}" data-source="{html.escape(source)}">
   <label class="sr" for="tf-email">Email address</label>
   <input id="tf-email" type="email" name="email" autocomplete="email" placeholder="you@email.com" required>
   <button type="submit" class="btn btn-gold">{btn}</button>
   <fieldset class="lanes-pick"><legend>What interests you? Optional</legend>{boxes}</fieldset>
  </form>
  <p class="status" id="signup-status" role="status" aria-live="polite"></p></div>"""

def faq_html(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in items) + '</div>'

def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def seat_cards(link=True):
    out = []
    for m in MEMBERS:
        out.append(f"""<article class="card bar-{m['key']}">
    {portrait(m, 72)}
    <span class="tag tag-{m['key']}">{m['seat']} · {m['area']}</span>
    <h3>{m['name']}</h3>
    <p>{m['show']}</p>
    <a class="lane-link" href="/lanes/{LANE[m['lane']]['slug']}">The {m['area'].lower()} lane &rarr;</a>
   </article>""")
    return '<div class="grid-3">' + ''.join(out) + '</div>'

# ---------- index ----------
index_body = f"""
{photo_hero('twilight', f'''
  <span class="kicker">Tierra Firme Investor Lab<span class="rule"></span>Bogotá · 7 to 12 March 2027</span>
  <h1>Any currency.<br>Solid ground.</h1>
  <p class="lede">A private six-day seminar in Bogotá for people placing capital across borders. Commercial real estate, business and family capital, and country research, taught by the three members of Tierra Firme.</p>
  <div class="btn-row" style="margin-top:30px">
   <a href="bogota-2027.html#invite" class="btn btn-gold">Request an invitation</a>
   <a href="bogota-2027.html" class="btn btn-ghost">See the program</a>
   <a href="#player" class="btn btn-ghost">&#9654;&nbsp; Watch the trailer</a>
  </div>
  {event_strip()}
  <p class="hero-fine">{DISCLAIMER} No listings, no sales, no fees on what you buy.</p>
''')}

<section class="trailer" id="trailer">
 <div class="container">
  <div class="section-head" style="margin-bottom:28px">
   <span class="eyebrow">Official trailer</span>
   <h2>See the gap before the market does.</h2>
  </div>
  <div class="player" id="player">
   <video id="tf-trailer" muted playsinline preload="auto" poster="/media/trailer-poster.webp" width="1920" height="1080" aria-label="Tierra Firme trailer">
    <source src="/media/tierra-firme-trailer.mp4" type="video/mp4">
   </video>
   <button type="button" class="sound" id="tf-sound" aria-label="Turn sound on">&#128266;&nbsp; Sound on</button>
   <button type="button" class="replay" id="tf-replay" aria-label="Replay trailer" hidden>&#8635;&nbsp; Replay</button>
  </div>
  <div class="theater-dim" id="tf-dim" aria-hidden="true"></div>
  <button type="button" class="theater-exit" id="tf-exit">&#10005;&nbsp; Close</button>
  <p class="trailer-fine">1 minute. Footage from Bogotá, Cartagena, Medellín, Lima, Cusco, Montevideo, Santiago, Buenos Aires, Rio de Janeiro, São Paulo, Mexico City, Antigua, Panama City, Santo Domingo and Dallas.</p>
 </div>
</section>

<section>
 <div class="container split">
  {fig('towers', 'tall')}
  <div>
   <span class="eyebrow">Why Bogotá</span>
   <h2>Where the rules are made.</h2>
   <p class="lede">Medellín gets the attention. Bogotá holds the institutions every foreign buyer ends up dealing with: the central bank, the tax authority, the notaries, the law firms and the ministries.</p>
   <p>We meet where the decisions that affect you are made, for six days of short boardroom briefings, verified field visits and cultural evenings.</p>
   <div class="btn-row" style="margin-top:22px"><a href="bogota-2027.html" class="btn btn-ink">The Bogotá 2027 program</a></div>
  </div>
 </div>
</section>

<section class="dark">
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">Three lanes</span>
   <h2>Three practitioners. Three lanes.</h2>
   <p class="lede">Each member teaches his own discipline and runs an independent practice. Every episode, answer and seminar day belongs to a lane, so you can follow the one that fits you.</p>
  </div>
  {seat_cards()}
  <div class="btn-row" style="margin-top:28px"><a href="members.html" class="btn btn-outline">Meet the members</a></div>
 </div>
</section>

<section class="band-green">
 <div class="container split rev">
  {fig('ballroom', 'wide')}
  <div>
   <span class="eyebrow">The room</span>
   <h2>Thirty seats. Every question answered.</h2>
   <p class="lede">The Investor Lab is small on purpose. One table of practitioners, Colombian counsel on property and tax, and a room small enough that nobody leaves with a question unasked.</p>
   <ul class="checks" style="margin-top:18px">
    <li style="color:rgba(255,255,255,.85)">An upscale hotel in north Bogotá, confirmed to registered attendees</li>
    <li style="color:rgba(255,255,255,.85)">Short morning briefings, verified field visits, cultural evenings</li>
    <li style="color:rgba(255,255,255,.85)">A welcome reception on the first evening</li>
   </ul>
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
   <span class="eyebrow">How it works</span>
   <h2>Learn at your own pace.</h2>
   <p class="lede">No hard sell. We would rather you be ready than early.</p>
  </div>
  <div class="ladder">
   <div class="step"><div class="step-mark">1</div><div><h3>Watch the show <span class="pill on">Free</span></h3><p style="margin:0">The thesis, the framework and real stories from the ground, in English and Spanish.</p></div></div>
   <div class="step"><div class="step-mark">2</div><div><h3>Read the answers <span class="pill on">Free</span></h3><p style="margin:0">Sourced answers in each lane, from title and tax to the exchange rate. <a href="questions.html">Browse the questions</a>.</p></div></div>
   <div class="step"><div class="step-mark">3</div><div><h3>Attend the Investor Lab <span class="pill">Bogotá · March 2027</span></h3><p style="margin:0">Six days, three lanes, thirty seats. <a href="bogota-2027.html">See the program</a>.</p></div></div>
   <div class="step"><div class="step-mark">4</div><div><h3>Join the community <span class="pill">Opening soon</span></h3><p style="margin:0">Membership with a structured curriculum, a members' forum and live office hours with all three members. <a href="membership.html">Join the waitlist</a>.</p></div></div>
  </div>
 </div>
</section>

<section>
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">Questions investors ask</span>
   <h2>Sourced answers before you commit.</h2>
   <p class="lede">Short answers on ownership, registration, taxes, the exchange rate and visas, each with the primary sources.</p>
  </div>
  <div class="qlist">QCARDS</div>
  <div class="btn-row" style="margin-top:26px"><a href="questions.html" class="btn btn-ink">All questions</a></div>
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
  <span class="eyebrow">Bogotá 2027 · Episodes · Research</span>
  <h2>Know the ground before you stand on it.</h2>
  <p class="lede">Join the community waitlist. Investor Lab seats, new episodes and research go to the list first.</p>
  {signup_block(source='home')}
 </div>
</section>
"""

# ---------- members ----------
member_rows = ''.join(f"""
  <article class="member" id="{m['key']}">
   <div>
    {portrait(m, 160)}
    <span class="tag tag-{m['key']}">{m['seat']} · {m['area']}</span>
    <h2>{m['name']}</h2>
    <p class="role">{m['role']}</p>
   </div>
   <div>
    <p>{m['bio']}</p>
    <p class="note"><strong>His lane:</strong> {m['show']} <a href="/lanes/{LANE[m['lane']]['slug']}">Read more</a></p>
   </div>
  </article>""" for m in MEMBERS)

members_body = f"""
<section class="hero">
 <div class="container">
  <span class="eyebrow">The members</span>
  <h1>Three practitioners. Equal seats.</h1>
  <p class="lede">Tierra Firme brings together commercial real estate, business and family capital, and research. Each member runs an independent practice and teaches his own lane, and each view checks the other two.</p>
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
  <p class="note">Members' individual business activities are independent of one another and of Tierra Firme. Tierra Firme does not list property, arrange transactions or take fees on what anyone buys.</p>
 </div>
</section>
<section class="dark">
 <div class="container text-center" style="display:flex;flex-direction:column;align-items:center">
  <h2>Get Investor Lab seats and new episodes first.</h2>
  {signup_block(source='members')}
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
   <article class="card bar-cre"><span class="tag tag-cre">On location · Murphy · The Asset</span><h3>Ground Truth</h3><p>A real, affordable property abroad on camera, and what the same income would and would not buy at home.</p></article>
   <article class="card bar-capital"><span class="tag tag-capital">Guest format · Shawn · The Capital</span><h3>Founder's Seat</h3><p>Someone who built a business or first balance sheet abroad: what worked, what it cost and what they would redo.</p></article>
   <article class="card bar-research"><span class="tag tag-research">Every episode · Todd · The Country</span><h3>The Research Close</h3><p>A short close on currency, political and structural conditions and where they are heading.</p></article>
  </div>
  <div class="card" style="margin-top:22px"><span class="tag">Quarterly · All three</span><h3>The Teaching Case</h3><p>A sample property and a sample business, priced, run and stress-tested end to end on camera as a classroom exercise. Illustrative only.</p></div>
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
  {signup_block(btn='Notify me', source='the-show')}
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
   {signup_block(btn='Join the waitlist', ok="You're on the membership waitlist. You'll hear first when doors open.", source='membership')}
   <p class="hero-fine">Waitlist is free and commits you to nothing. Education, not investment advice.</p>
  </div>
  <div class="card hero-card">
   <h3>What members get</h3>
   <ul class="checks">
    <li>A structured curriculum on evaluating a market abroad: currency, political and structural conditions</li>
    <li>Live office hours with Murphy, Shawn and Todd</li>
    <li>A members' forum to compare markets, questions and lessons</li>
    <li>Research led by Todd Allyn, and first seats at the Bogotá Investor Lab</li>
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
   <article class="card bar-cre"><span class="tag tag-cre">The Asset · Murphy</span><h3>Read the property</h3><p>How to judge value, title and management before anyone shows you a unit.</p></article>
   <article class="card bar-capital"><span class="tag tag-capital">The Capital · Shawn</span><h3>Read the business</h3><p>What it costs to enter, run and staff a business on the ground.</p></article>
   <article class="card bar-research"><span class="tag tag-research">The Country · Todd</span><h3>Read the conditions</h3><p>The currency, policy and structural signals that set your real return.</p></article>
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


from questions_data import QUESTIONS, UPDATED, UPDATED_TEXT
# ---------- Bogotá 2027 Investor Lab ----------
# Six days, five nights: arrive Sunday, depart Friday afternoon or Saturday morning depending on flights.
# Format: short boardroom briefings in the morning, verified field visits in the afternoon, cultural evenings.
# Days 3 to 5 (Tuesday to Thursday) are Colombian commerce: short briefings and field work.
# Each day: (lane id or None for a shared day, title, weekday, date, slots).
PROGRAM = [
    (None, 'Arrival', 'Sunday', '7 March', [
        ('Day', 'Arrive in Bogotá and settle in at the hotel in north Bogotá.'),
        ('Evening', 'Welcome reception with the three members.'),
    ]),
    ('research', None, 'Monday', '8 March', [
        ('Boardroom', 'Short briefing: Colombia in context. The economy, the political calendar and where policy is heading.'),
        ('Afternoon', 'The peso. Earning in one currency and owning in another, and how the exchange rate changes what you keep.'),
        ('Evening', 'Cultural evening in Bogotá.'),
    ]),
    ('cre', 'Colombian commerce · Property', 'Tuesday', '9 March', [
        ('Boardroom', 'Short briefing: how property is valued, titled and managed in Colombia, with Colombian counsel on propiedad horizontal and tax.'),
        ('Field visit', 'A verified field visit to two contrasting Bogotá districts: infrastructure, services and the signals a listing never shows.'),
        ('Evening', 'Cultural evening in Bogotá.'),
    ]),
    ('capital', 'Colombian commerce · Business', 'Wednesday', '10 March', [
        ('Boardroom', 'Short briefing: building and holding a business in Colombia, from entities to registering foreign investment and getting money home.'),
        ('Field visit', 'A verified field visit with an operator on site: what it really costs to run a business here.'),
        ('Evening', 'Cultural evening in Bogotá.'),
    ]),
    (None, 'Colombian commerce · Investment', 'Thursday', '11 March', [
        ('Boardroom', 'Short briefing with all three members: Colombian commerce and investment, worked through a sample property and a sample business.'),
        ('Field visit', 'A verified field visit, followed by small-group time with each member on your own questions.'),
        ('Evening', 'Cultural evening in Bogotá.'),
    ]),
    (None, 'The decision', 'Friday', '12 March', [
        ('Boardroom', 'The decision framework. Run your own question through it with the three members.'),
        ('Afternoon', 'Departures, or stay the night and fly out Saturday 13 March, depending on flights.'),
    ]),
]

def program_html():
    out = []
    for lane, title, dow, date, slots in PROGRAM:
        sl = ''.join(f'<div class="slot"><span class="t">{t}</span><p>{html.escape(d)}</p></div>' for t, d in slots)
        if lane:
            l = LANE[lane]
            tag = f'<span class="tag tag-{l["key"]}">{l["seat"]}</span>'
            head = f'<h3>{title or l["label"]}</h3><p style="margin-top:-6px">{l["label"]}, led by {l["member"]}. <a href="lanes/{l["slug"]}.html">About this lane</a></p>'
        else:
            tag = '<span class="tag">Together</span>'
            head = f'<h3>{title}</h3>'
        out.append(f"""<article class="day">
   <div class="when">{dow}<b>{date}</b>{tag}</div>
   <div>{head}{sl}</div>
  </article>""")
    return '<div class="program">' + ''.join(out) + '</div>'

def faculty_html():
    return '<div class="faculty">' + ''.join(f"""<a class="card bar-{m['key']}" href="lanes/{LANE[m['lane']]['slug']}.html">
    {portrait(m, 72)}<span class="tag tag-{m['key']}">{m['seat']} · {m['area']}</span><h3>{m['name']}</h3><p>{m['show']}</p></a>""" for m in MEMBERS) + '</div>'

EVENT_FAQ = [
    ("When and where is the Investor Lab?",
     "Six days and five nights in Bogotá: arrive Sunday 7 March 2027, depart Friday 12 March in the afternoon or Saturday 13 March in the morning, depending on flights. The venue is an upscale hotel in north Bogotá, confirmed to registered attendees."),
    ("Who is it for?",
     "People who earn in dollars, euros or another currency and are weighing property or a small business in Colombia, and families thinking about how to hold what they build across borders."),
    ("How many seats are there?",
     "Thirty. The room is kept small so every question gets answered."),
    ("Will anyone sell me property or a business?",
     "No. There are no listings, no sponsors pitching from the stage and no referral fees. Site visits show places, not units for sale. It is education, not advice."),
    ("How do I get a seat?",
     "Join the waitlist on this page. Seat details and pricing go to the waitlist before anyone else."),
]

event_body = f"""
{photo_hero('downtown', f'''
  <span class="kicker">Investor Lab<span class="rule"></span>Bogotá · {EVENT['dates']}</span>
  <h1>Six days on solid ground.</h1>
  <p class="lede">Read the country before you buy into it. A private seminar in Bogotá for foreign buyers weighing Colombian property or a business: short morning briefings, verified field visits and cultural evenings, a day for each lane.</p>
  <div class="btn-row" style="margin-top:30px">
   <a href="#invite" class="btn btn-gold">Request an invitation</a>
   <a href="#program" class="btn btn-ghost">See the program</a>
  </div>
  {event_strip()}
''')}

<section>
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">The problem</span>
   <h2>Most buyers study the property. The country decides the outcome.</h2>
   <p class="lede">A good apartment in the wrong conditions is a poor decision. Three things move your real result more than the asset does, and most expat events skip all three.</p>
  </div>
  <div class="grid-3">
   <article class="card bar-research"><span class="tag tag-research">Currency</span><h3>Two currencies</h3><p>You earn in one currency and own in another. The peso can add to what you keep or erase it before rent is ever collected.</p></article>
   <article class="card bar-cre"><span class="tag tag-cre">Title and tax</span><h3>Who owns what</h3><p>How title and propiedad horizontal work, what you owe while you hold and what you owe when you sell.</p></article>
   <article class="card bar-capital"><span class="tag tag-capital">Getting money out</span><h3>The way out</h3><p>Registering your investment correctly on the way in, so you can bring the money home on the way out.</p></article>
  </div>
 </div>
</section>

<section class="alt" id="program">
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">The program · Draft</span>
   <h2>Six days. Three lanes.</h2>
   <p class="lede">Boardroom mornings, Colombian commerce and investment in the afternoons, culture in the evenings. Tuesday to Thursday are three days of Colombian commerce: short briefings and field work. Sessions are a draft and may change as each member finalizes his day.</p>
  </div>
  {program_html()}
 </div>
</section>

<section class="dark">
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">The setting</span>
   <h2>A quiet room above Bogotá.</h2>
   <p class="lede">An upscale hotel in north Bogotá, a working session in a high-floor boardroom and two afternoons out in the city.</p>
  </div>
  <div class="gallery">
   {fig('ballroom', 'wide', '(max-width:760px) 100vw, 66vw')}
   <div class="col">{fig('boardroom', 'wide', '(max-width:760px) 100vw, 33vw')}{fig('lobby', 'wide', '(max-width:760px) 100vw, 33vw')}</div>
  </div>
  <p class="trailer-fine" style="margin-top:22px">Interior images are illustrations of the format. The venue is confirmed to registered attendees.</p>
 </div>
</section>

<section>
 <div class="container split">
  <div>
   <span class="eyebrow">The details</span>
   <h2>Bogotá, March 2027.</h2>
   <dl class="facts">
    <div><dt>Dates</dt><dd>6 days, 5 nights: arrive Sunday 7 March, depart Friday 12 March afternoon or Saturday 13 March morning, depending on flights</dd></div>
    <div><dt>Seats</dt><dd>30, so every question gets answered</dd></div>
    <div><dt>Venue</dt><dd>An upscale hotel in north Bogotá, confirmed to registered attendees</dd></div>
    <div><dt>Airport</dt><dd>El Dorado International (BOG)</dd></div>
    <div><dt>Included</dt><dd>All sessions, lunches and coffee, the welcome reception and transport for site visits</dd></div>
    <div><dt>Seats and pricing</dt><dd>Sent to the waitlist first</dd></div>
   </dl>
  </div>
  {fig('colpatria', 'tall', '(max-width:860px) 100vw, 45vw')}
 </div>
</section>

<section class="alt">
 <div class="container grid-2">
  <div>
   <span class="eyebrow">Who it is for</span>
   <h2>Capital, and a question.</h2>
   <ul class="checks">
    <li>You are weighing property or a small business in Colombia.</li>
    <li>You earn in dollars, euros or another currency and want to know what the peso does to you.</li>
    <li>You want to understand the terms before anyone shows you a unit.</li>
    <li>You would rather decide slowly than regret quickly.</li>
   </ul>
  </div>
  <div>
   <span class="eyebrow">What you leave with</span>
   <h2>Tools you keep.</h2>
   <ul class="checks">
    <li>A decision framework, with your own question run through it</li>
    <li>A written Colombia country briefing on the conditions your decision will live in</li>
    <li>Every presentation from the week</li>
   </ul>
  </div>
 </div>
</section>

<section>
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">What this is not</span>
   <h2>Not a sales tour.</h2>
   <p class="lede">Most investor events are funded by the people selling to you. This one is not, so we can tell you what we actually think.</p>
  </div>
  <div class="grid-2" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">
   <article class="card"><h3>No listings</h3><p>Site visits show places, not units for sale.</p></article>
   <article class="card"><h3>No pitches</h3><p>No brokers in the room and no sponsors on the stage.</p></article>
   <article class="card"><h3>No referral fees</h3><p>We earn nothing from what you buy or where.</p></article>
   <article class="card"><h3>Education, not advice</h3><p>We teach you to evaluate. The decision stays yours.</p></article>
  </div>
 </div>
</section>

<section class="alt">
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">Faculty</span>
   <h2>The three members, plus local experts.</h2>
   <p class="lede">Joined by Colombian counsel on property, tax and foreign investment law.</p>
  </div>
  {faculty_html()}
 </div>
</section>

<section>
 <div class="container">
  <div class="section-head"><span class="eyebrow">Questions</span><h2>Before you ask.</h2></div>
  {faq_html(EVENT_FAQ)}
 </div>
</section>

<section class="band-green" id="invite">
 <div class="container text-center" style="display:flex;flex-direction:column;align-items:center">
  <span class="eyebrow">30 seats · Bogotá · March 2027</span>
  <h2>Request an invitation.</h2>
  <p class="lede">Join the waitlist. Seat details and pricing go to the list before public release.</p>
  {signup_block(btn='Request an invitation', ok="Thank you. You're on the Bogotá 2027 waitlist; seat details come to you first.", source='bogota-2027')}
  <p class="hero-fine" style="color:rgba(255,255,255,.6)">{DISCLAIMER}</p>
 </div>
</section>
"""

event_schema = [
    {"@type": "EducationEvent", "@id": BASE + "/bogota-2027#event", "name": "Tierra Firme Investor Lab, Bogotá 2027",
     "description": "A six-day educational seminar in Bogotá on commercial real estate, business and family capital, and country research for people placing capital across borders.",
     "startDate": EVENT['start'], "endDate": EVENT['end'], "eventStatus": "https://schema.org/EventScheduled",
     "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "maximumAttendeeCapacity": EVENT['seats'],
     "location": {"@type": "Place", "name": "North Bogotá (venue confirmed to registered attendees)",
                  "address": {"@type": "PostalAddress", "addressLocality": "Bogotá", "addressCountry": "CO"}},
     "image": [BASE + PHOTOS['downtown']['base'] + '-1920.webp'],
     "organizer": {"@id": BASE + "/#org"}, "performer": [{"@type": "Person", "name": m['name']} for m in MEMBERS],
     "inLanguage": "en", "url": BASE + "/bogota-2027"},
    faq_schema(EVENT_FAQ),
]

# ---------- lane pages ----------
# Copy is a DRAFT in each member's voice. Set approved=True in LANES only after the member signs off.
LANE_COPY = {
    'cre': dict(photo='downtown', h1='Read the property before you buy it.',
        voice=("I have spent my career on the asset side of real estate: what a building is worth, who really owns it and what it costs to run. "
               "Abroad, those questions get harder, not easier. In this lane I teach how to read a property and the market around it before you "
               "commit, so the first conversation you have with a seller is not the first time you have thought about value, title or management."),
        covers=['How commercial and residential property is valued, and what the price is really telling you',
                'Title, propiedad horizontal and what the paperwork shows before you sign',
                'Operating costs and management, and what owners underestimate',
                'Reading a district: infrastructure, services and the signals a listing never shows'],
        show='Ground Truth: a real property on camera, and what the same income would and would not buy at home.',
        extra=''),
    'capital': dict(photo='boardroom', h1='Build it, run it, hold it.',
        voice=("I have built and run businesses in Latin America, and I live in Bogotá. Most people who look at Colombia think about an apartment. "
               "Fewer think about the business that could pay for it, or how a family holds what it builds across two countries. This lane is about "
               "that: what it takes to start or buy a small business here, what it costs to run, and how families hold it over time."),
        covers=['Starting or buying a small business as a foreigner',
                'Entities, registration and banking basics, and getting money home',
                'Hiring, operating and the real cost of being on the ground',
                'How families hold businesses and assets across borders'],
        show="Founder's Seat: someone who built a business abroad on what worked, what it cost and what they would redo.",
        extra='Everything in this lane is education. Nothing here is an offer of, or access to, any investment.'),
    'research': dict(photo='twilight', h1='Read the country first.',
        voice=("I lead the research. Before anyone looks at a property or a business, I want to know what the country is doing: the currency, the "
               "political calendar and the rules that decide what a foreigner can bring home. This lane is the conditions behind every decision, "
               "and the signals that they are changing."),
        covers=['Currency: income in one currency, assets in another',
                'The political and policy cycle, and what it changes',
                'The structural rules: foreign investment registration, tax and repatriation',
                'How to evaluate a country before committing'],
        show='The Research Close: a short close every episode on currency, political and structural conditions.',
        extra=''),
}

def lane_page(l):
    c = LANE_COPY[l['id']]
    m = next(x for x in MEMBERS if x['lane'] == l['id'])
    day = next(p for p in PROGRAM if p[0] == l['id'])
    qs = [x for x in QUESTIONS if x['lane'] == l['id']]
    qhtml = ('<div class="qlist">' + ''.join(f'<a class="qcard" href="/questions/{x["slug"]}"><h3>{html.escape(x["q"])}</h3><p>{html.escape(x["short"])}</p></a>' for x in qs) + '</div>') if qs \
        else '<p>Answer pages for this lane are being written. Join the waitlist to hear when they publish.</p>'
    covers = ''.join(f'<li>{html.escape(x)}</li>' for x in c['covers'])
    body = f"""
{photo_hero(c['photo'], f'''
  <span class="kicker">{l['seat']}<span class="rule"></span>{l['label']} · {l['first']}</span>
  <h1>{c['h1']}</h1>
  <p class="lede">{m['show']}</p>
  <div class="btn-row" style="margin-top:28px"><a href="#join" class="btn btn-gold">Follow this lane</a><a href="/bogota-2027#program" class="btn btn-ghost">{day[2]} {day[3]} at the Investor Lab</a></div>
''')}
<section>
 <div class="container grid-2" style="align-items:start">
  <div>
   <span class="eyebrow">In {l['first']}'s words</span>
   <p class="quote" style="color:var(--ink);font-size:clamp(1.3rem,2.2vw,1.7rem)">{html.escape(c['voice'])}</p>
   <p class="role" style="margin-top:18px">{m['name']}</p>
  </div>
  <div>
   <span class="eyebrow">What this lane covers</span>
   <ul class="checks">{covers}</ul>
   <p class="note" style="margin-top:22px"><strong>On the show:</strong> {html.escape(c['show'])}</p>
   {f'<p class="note">{html.escape(c["extra"])}</p>' if c['extra'] else ''}
  </div>
 </div>
</section>
<section class="alt">
 <div class="container">
  <div class="section-head"><span class="eyebrow">Questions in this lane</span><h2>Sourced answers.</h2></div>
  {qhtml}
 </div>
</section>
<section>
 <div class="container split">
  <div>
   <span class="eyebrow">About {l['first']}</span>
   <h2>{m['name']}</h2>
   <p class="role">{m['role']}</p>
   <p>{m['bio']}</p>
  </div>
  <div>{portrait(m, 320, 'portrait-lg')}</div>
 </div>
</section>
<section class="dark" id="join">
 <div class="container text-center" style="display:flex;flex-direction:column;align-items:center">
  <span class="eyebrow">{l['label']}</span>
  <h2>Follow {l['first']}'s lane.</h2>
  <p class="lede">Join the community waitlist. Pick the lanes you want to hear about.</p>
  {signup_block(source='lane-' + l['id'], preset=(l['id'],))}
 </div>
</section>
"""
    schema = [dict(m['person'], **{"memberOf": {"@id": BASE + "/#org"}})]
    banner = '' if l['approved'] else f'<div class="draft-banner">Draft for review: {l["first"]} has not yet approved this page. Not indexed.</div>'
    return body, schema, banner

# ---------- credits ----------
credit_rows = ''.join(
    f'<li><strong>{html.escape(p["title"])}</strong>. {html.escape(p["author"])}, <a href="{p["lic_url"]}" rel="noopener">{p["lic"]}</a>. '
    f'<a href="{p["src"]}" rel="noopener">Source on Wikimedia Commons</a>. Resized and converted to WebP.</li>'
    for k, p in PHOTOS.items() if not p.get('ill'))
credits_body = f"""
<section class="hero">
 <div class="container">
  <span class="eyebrow">Credits</span>
  <h1>Photo credits.</h1>
  <p class="lede">Photographs of Bogotá are used under the licenses below. Interior images marked "Illustrative" are generated illustrations of the seminar format, not photographs of the venue.</p>
 </div>
</section>
<section>
 <div class="container">
  <ul class="checks">{credit_rows}</ul>
  <p class="note" style="margin-top:28px">Adapted versions of CC BY-SA photographs are shared under the same license. Trailer footage credits are listed with the trailer wherever it is posted.</p>
 </div>
</section>
"""

PAGES = [
    ('index.html', 'Tierra Firme | Real Estate, Business and Research for Capital Abroad',
     'Tierra Firme is a consortium in commercial real estate, business and intelligence research. A free show, research and seminars for people placing capital across borders, starting with Latin America.',
     index_body, [faq_schema(FAQ), {"@id": BASE + "/bogota-2027#event", "@type": "EducationEvent", "name": "Tierra Firme Investor Lab, Bogotá 2027", "startDate": EVENT['start'], "endDate": EVENT['end'], "url": BASE + "/bogota-2027", "location": {"@type": "Place", "name": "Bogotá", "address": {"@type": "PostalAddress", "addressLocality": "Bogotá", "addressCountry": "CO"}}}, {"@type": "VideoObject", "name": "Tierra Firme trailer",
        "description": "Every market has a gap. Tierra Firme, a consortium in commercial real estate, business and intelligence research, on reading the currency, political and structural arbitrage across Latin America before it becomes common knowledge.",
        "thumbnailUrl": BASE + "/media/trailer-poster.webp", "contentUrl": BASE + "/media/tierra-firme-trailer.mp4",
        "uploadDate": "2026-10-23", "duration": "PT1M3S", "inLanguage": "en", "publisher": {"@id": BASE + "/#org"}}], None, 'twilight'),
    ('bogota-2027.html', 'Bogotá 2027 Investor Lab | Tierra Firme · 7 to 12 March 2027',
     'Tierra Firme Investor Lab: six days in Bogotá, 7 to 12 March 2027, for 30 people. Commercial real estate, business and family capital, and country research. Education, not advice.',
     event_body, event_schema, [('', 'Home'), ('bogota-2027.html', 'Bogotá 2027')], 'downtown'),
    ('credits.html', 'Photo Credits | Tierra Firme', 'Credits and licenses for the photographs used on the Tierra Firme site.',
     credits_body, [], [('', 'Home'), ('credits.html', 'Photo credits')], None),
    ('members.html', 'Members | Tierra Firme',
     'Meet the Tierra Firme members: Murphy D. Cheatham II (commercial real estate, CBRE), Shawn Christopher Leamon (business and family capital, LaGrande Global) and Todd Allyn (research).',
     members_body, [dict(m['person'], **{"memberOf": {"@id": BASE + "/#org"}}) for m in MEMBERS],
     [('', 'Home'), ('members.html', 'Members')], None),
    ('the-show.html', 'The Show | Tierra Firme Season One',
     'Tierra Firme Season One: twelve free episodes on placing capital abroad, from the currency math to a full case study. In English and Spanish.',
     show_body, [show_schema], [('', 'Home'), ('the-show.html', 'The Show')], None),
    ('membership.html', 'Membership | Join the Tierra Firme Community',
     'Join the waitlist for the Tierra Firme membership community: a curriculum on evaluating markets abroad, live office hours with the three members, and a members forum.',
     membership_body, [], [('', 'Home'), ('membership.html', 'Membership')], None),
]

for fname, title, desc, body, extra, crumbs, hero in PAGES:
    with open(os.path.join(OUT, fname), 'w') as f:
        f.write(page(fname, title, desc, body, extra, crumbs, preload=hero_preload(hero) if hero else None))

nf = page('404.html', 'Page not found | Tierra Firme', 'That page does not exist.', notfound_body)
nf = nf.replace(f'<link rel="canonical" href="{BASE}/404">', '<meta name="robots" content="noindex">')
with open(os.path.join(OUT, '404.html'), 'w') as f:
    f.write(nf)


# ---------- questions ----------
QMAP = {x['slug']: x for x in QUESTIONS}
AUTHOR = {"@type": "Person", "name": "Todd Allyn", "url": "https://www.linkedin.com/in/toddallyn/",
          "jobTitle": "Founding Director, Sovereo Intelligence Research"}
Q_CSS_EXTRA = """
.qa-answer{font-size:1.2rem;line-height:1.65;color:var(--ink);background:var(--surface);border-left:4px solid var(--gold);padding:22px 26px;margin:0 0 34px;max-width:820px}
.qa-meta{font-size:.88rem;color:var(--muted-2);margin:-6px 0 26px}
.qa h2{font-size:1.55rem;margin-top:34px}
.qa p{max-width:72ch}
.qa-src{font-size:.92rem}.qa-src li{margin-bottom:6px}
.qlist{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
@media(max-width:760px){.qlist{grid-template-columns:1fr}}
.qcard{display:block;text-decoration:none;background:var(--surface);border:1px solid var(--border);border-radius:4px;padding:22px 24px}
.qcard:hover{border-color:var(--gold)}
.qcard h3{margin:0 0 8px;font-size:1.15rem}.qcard p{margin:0;font-size:.95rem}
"""
import html as _h
def q_page(x):
    secs = ''.join(f"<h2>{_h.escape(t)}</h2><p>{_h.escape(b)}</p>" for t, b in x['sections'])
    faqs = ''.join(f"<details><summary>{_h.escape(a)}</summary><p>{_h.escape(b)}</p></details>" for a, b in x['faqs'])
    src = ''.join(f'<li><a href="{u}" rel="noopener">{_h.escape(t)}</a></li>' for t, u in x['sources'])
    rel = ''.join(f'<a class="qcard" href="/questions/{s}"><h3>{_h.escape(QMAP[s]["q"])}</h3><p>{_h.escape(QMAP[s]["short"])}</p></a>' for s in x['related'])
    body = f"""
<section class="hero" style="padding-bottom:56px">
 <div class="container">
  <span class="eyebrow"><a href="/questions" style="color:inherit;text-decoration:none">Questions investors ask</a></span>
  <h1 style="font-size:clamp(2.1rem,4.4vw,3.4rem)">{_h.escape(x['q'])}</h1>
 </div>
</section>
<section class="qa">
 <div class="container">
  <p class="qa-meta"><a class="tag tag-{LANE[x['lane']]['key']}" style="text-decoration:none" href="/lanes/{LANE[x['lane']]['slug']}">{LANE[x['lane']]['seat']} · {LANE[x['lane']]['label']}</a><br>By Todd Allyn, research lead, Tierra Firme · Updated <time datetime="{UPDATED}">{UPDATED_TEXT}</time></p>
  <p class="qa-answer">{_h.escape(x['answer'])}</p>
  {secs}
  <h2>More questions</h2>
  <div class="faq">{faqs}</div>
  {('<h2>Sources</h2><ul class="qa-src">' + src + '</ul>') if src else ''}
  <p class="note" style="margin-top:30px">{DISCLAIMER} Rules and amounts change; confirm with the primary source and a licensed professional before acting.</p>
 </div>
</section>
<section class="alt">
 <div class="container">
  <div class="section-head"><span class="eyebrow">Related</span><h2>Keep reading.</h2></div>
  <div class="qlist">{rel}</div>
 </div>
</section>
<section class="dark">
 <div class="container text-center" style="display:flex;flex-direction:column;align-items:center">
  <span class="eyebrow">Episodes · Research · Seminars</span>
  <h2>Get answers like this first.</h2>
  {signup_block(source='question', preset=(x['lane'],))}
 </div>
</section>
"""
    url = BASE + '/questions/' + x['slug']
    schema = [
        {"@type": "Article", "@id": url + "#article", "headline": x['q'], "description": x['short'], "datePublished": UPDATED,
         "dateModified": UPDATED, "author": AUTHOR, "publisher": {"@id": BASE + "/#org"}, "mainEntityOfPage": url,
         "image": SHARE, "inLanguage": "en", "about": ["Colombia", "Foreign investment", "Real estate"],
         "citation": [u for t, u in x['sources']]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": x['q'], "acceptedAnswer": {"@type": "Answer", "text": x['answer']}}] +
            [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in x['faqs']]},
    ]
    return body, schema

os.makedirs(os.path.join(OUT, 'questions'), exist_ok=True)
for x in QUESTIONS:
    body, schema = q_page(x)
    fname = 'questions/' + x['slug'] + '.html'
    out = page(fname, x['q'] + ' | Tierra Firme', x['short'], body, schema,
               [('', 'Home'), ('questions.html', 'Questions'), (fname, x['q'])])
    out = out.replace('</style>', Q_CSS_EXTRA + '</style>', 1)
    with open(os.path.join(OUT, fname), 'w') as f:
        f.write(out)

def _qcard(x):
    l = LANE[x['lane']]
    return f'<a class="qcard" href="/questions/{x["slug"]}"><span class="tag tag-{l["key"]}">{l["label"]}</span><h3>{_h.escape(x["q"])}</h3><p>{_h.escape(x["short"])}</p></a>'
_chips = '<nav class="lane-chips" aria-label="Filter by lane"><a href="#all" data-lane-filter="all" aria-pressed="true">All lanes</a>' + ''.join(
    f'<a href="#lane-{l["id"]}" data-lane-filter="{l["id"]}" aria-pressed="false">{l["label"]}</a>' for l in LANES) + '</nav>'
hub_cards = _chips + ''.join(
    f'<div class="qlane" id="lane-{l["id"]}"><h2>{l["label"]} <span class="pill">{l["member"]}</span></h2>' +
    (('<div class="qlist">' + ''.join(_qcard(x) for x in QUESTIONS if x['lane'] == l['id']) + '</div>') if any(x['lane'] == l['id'] for x in QUESTIONS)
     else '<p>Answer pages for this lane are being written.</p>') + '</div>' for l in LANES)
hub_body = f"""
<section class="hero">
 <div class="container">
  <span class="eyebrow">Questions investors ask</span>
  <h1>Straight answers, with sources.</h1>
  <p class="lede">Short, sourced answers to the questions people ask before placing capital in Colombia and Latin America, grouped by lane. Each page opens with the answer, then the detail, then the primary sources.</p>
 </div>
</section>
<section>
 <div class="container">{hub_cards}
  <p class="note" style="margin-top:30px">{DISCLAIMER} Updated {UPDATED_TEXT}.</p>
 </div>
</section>
<section class="dark">
 <div class="container text-center" style="display:flex;flex-direction:column;align-items:center">
  <h2>Have a question we have not answered?</h2>
  <p class="lede">Join the waitlist and reply to any email. New answers go to the list first.</p>
  {signup_block(source='questions')}
 </div>
</section>
"""
hub_schema = [{"@type": "ItemList", "name": "Questions investors ask", "itemListElement": [
    {"@type": "ListItem", "position": i + 1, "url": BASE + '/questions/' + x['slug'], "name": x['q']} for i, x in enumerate(QUESTIONS)]},
    {"@type": "CollectionPage", "@id": BASE + "/questions#page", "name": "Questions investors ask", "dateModified": UPDATED}]
hub = page('questions.html', 'Questions Investors Ask About Colombia | Tierra Firme',
           'Sourced answers on buying property in Colombia as a foreigner, foreign investment registration, taxes, the exchange rate, investor visas and propiedad horizontal.',
           hub_body, hub_schema, [('', 'Home'), ('questions.html', 'Questions')])
hub = hub.replace('</style>', Q_CSS_EXTRA + '</style>', 1)
open(os.path.join(OUT, 'questions.html'), 'w').write(hub)

os.makedirs(os.path.join(OUT, 'lanes'), exist_ok=True)
for l in LANES:
    body, schema, banner = lane_page(l)
    fname = 'lanes/' + l['slug'] + '.html'
    out = page(fname, f"{l['label']} with {l['member']} | Tierra Firme", LANE_COPY[l['id']]['voice'][:155].rsplit(' ', 1)[0] + '.',
               body, schema, [('', 'Home'), ('members.html', 'Members'), (fname, l['label'])],
               preload=hero_preload(LANE_COPY[l['id']]['photo']), noindex=not l['approved'], banner=banner)
    out = out.replace('</style>', Q_CSS_EXTRA + '</style>', 1)
    open(os.path.join(OUT, fname), 'w').write(out)
_ix = open(os.path.join(OUT, 'index.html')).read()
_cards = ''.join(_qcard(x) for x in QUESTIONS[:4])
_ix = _ix.replace('QCARDS', _cards).replace('href="questions.html"', 'href="/questions"').replace('</style>', Q_CSS_EXTRA + '</style>', 1)
open(os.path.join(OUT, 'index.html'), 'w').write(_ix)

# ---------- static files ----------
bots = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'anthropic-ai',
        'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Googlebot', 'Applebot', 'Applebot-Extended', 'Bingbot',
        'CCBot', 'meta-externalagent', 'DeepSeekBot', 'Bytespider', 'Amazonbot', 'DuckAssistBot', 'cohere-ai', 'MistralAI-User']
robots = 'User-agent: *\nAllow: /\n\n# Search and AI answer engines are welcome\n' + ''.join(f'User-agent: {b}\nAllow: /\n' for b in bots) + f'\nSitemap: {BASE}/sitemap.xml\n'
open(os.path.join(OUT, 'robots.txt'), 'w').write(robots)

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p, pr in ([('', '1.0'), ('bogota-2027', '1.0'), ('members', '0.9'), ('the-show', '0.9'), ('questions', '0.9')]
              + [('lanes/' + l['slug'], '0.8') for l in LANES if l['approved']]
              + [('questions/' + x['slug'], '0.8') for x in QUESTIONS] + [('membership', '0.8'), ('credits', '0.3')]):
    sm += f'  <url><loc>{BASE}/{p}</loc><lastmod>2026-11-20</lastmod><priority>{pr}</priority></url>\n'
sm += '</urlset>\n'
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)

llms = f"""# Tierra Firme

> A consortium of three practitioners in commercial real estate, business and family capital, and research. Tierra Firme produces a free show, sourced answers and seminars for people placing capital across borders, starting with Latin America. Based in Dallas and Bogotá; works globally. Educational only: no listings, no transactions, no investment advice.

## Members and lanes
- Murphy D. Cheatham II, The Asset (commercial real estate): Private Clients Director at CBRE, a global role advising private families and high net worth individuals.
- Shawn Christopher Leamon, The Capital (business and family capital): founder and managing partner of LaGrande Global (since 2013), an investment firm managing close to $100 million with a focus on Latin America, and founder and CEO of Cielo.Travel, Bogotá.
- Todd Allyn, The Country (research): leads Tierra Firme research. Founding Director of Sovereo Intelligence Research (https://www.sovereo.com), whose Global Deal Record (https://www.sovereo.com/deal-record) tracks business deals worldwide from official sources, with US$46 billion in verified deals logged in 2026. Bogotá.

## Event
- [Tierra Firme Investor Lab, Bogotá 2027]({BASE}/bogota-2027): 6 days, 5 nights, 7 to 12 March 2027 (arrive Sunday, depart Friday afternoon or Saturday morning), Bogotá, 30 seats. A day for each lane. Education, not advice.

## Pages
- [Home]({BASE}/): what Tierra Firme is, the three lanes, the framework and FAQ.
- [Members]({BASE}/members): full bios of the three members.
- [The Show]({BASE}/the-show): Season One, twelve biweekly episodes in English and Spanish.
- [Membership]({BASE}/membership): the community waitlist (curriculum, office hours, forum), opening soon. The only signup on the site.

## Questions investors ask (sourced answers)
""" + ''.join(f"- [{x['q']}]({BASE}/questions/{x['slug']}): {x['short']}\n" for x in QUESTIONS) + f"""
## Notes
- Tierra Firme does not list property, arrange transactions or take fees on what anyone buys.
- Nothing published by Tierra Firme is investment, tax or legal advice.
"""
open(os.path.join(OUT, 'llms.txt'), 'w').write(llms)

redirects = """/the-seats.html /members 301
/the-seats /members 301
/get-the-read.html /membership 301
/get-the-read /membership 301
/join.html /membership 301
/join /membership 301
/investor-lab /bogota-2027 301
/tierra-firme.html / 301
/tierra-firme-episodes.html /the-show 301
/tierra-firme-hosts.html /members 301
/tierra-firme-subscribe.html /membership 301
"""
open(os.path.join(OUT, '_redirects'), 'w').write(redirects)

favicon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#061327" stroke="#e9a825" stroke-width="3"/><text x="32" y="40" text-anchor="middle" font-family="Georgia,serif" font-size="22" font-weight="700" fill="#e9a825">TF</text></svg>"""
open(os.path.join(OUT, 'favicon.svg'), 'w').write(favicon)
print('built', sorted(os.listdir(OUT)))
