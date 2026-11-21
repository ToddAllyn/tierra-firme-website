#!/usr/bin/env python3
"""Builds the Tierra Firme static site into ../tierra-firme-website."""
import json, os, html, re

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)
BASE = 'https://www.tierrafirme.lat'
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

/* ===== Elite event layer ===== */
:root{--ink-2:#040c1a;--line:rgba(233,168,37,.28)}
section{padding:clamp(48px,6vw,76px) 0}
.section-head{margin-bottom:28px}
.lede{font-size:1.06rem}
.event-bar{background:var(--ink-2);color:rgba(255,255,255,.78);font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;border-bottom:1px solid var(--line)}
.event-bar .container{display:flex;align-items:center;justify-content:center;gap:8px 18px;flex-wrap:wrap;padding-block:9px;text-align:center}
.event-bar b{color:var(--gold-l);font-weight:600}
.event-bar a{color:#fff;text-decoration:none;border-bottom:1px solid var(--gold);padding-bottom:1px}
@media (max-width:640px){.event-bar .eb-long{display:none}.event-bar .container{gap:6px 10px;font-size:.66rem;letter-spacing:.1em}}
.event-bar .pre{color:var(--gold);border:1px solid var(--line);padding:2px 8px;border-radius:999px}
.card{border-radius:2px;transition:transform .2s,border-color .2s,box-shadow .2s}
a.card:hover,.lift:hover{transform:translateY(-3px);box-shadow:0 18px 40px rgba(6,19,39,.18);border-color:var(--gold)}
.dark,.ink{background:var(--navy)}
.ink{background:linear-gradient(180deg,var(--ink-2),var(--navy));color:#fff}
.ink h2,.ink h3{color:#fff}.ink p{color:rgba(255,255,255,.74)}.ink .eyebrow{color:var(--gold)}
.ink .card{background:rgba(255,255,255,.035);border-color:rgba(255,255,255,.12)}
.ink .note{color:rgba(255,255,255,.7)}
.ink .checks li{color:rgba(255,255,255,.8)}
.ink a{color:var(--gold-l)}
/* split hero */
.hero-split{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(24px,4vw,56px);align-items:end}
@media (max-width:980px){.hero-split{grid-template-columns:1fr}}
.photo-hero{min-height:min(88vh,820px)}
.photo-hero>.container{padding-top:clamp(90px,14vh,150px);padding-bottom:clamp(36px,5vw,64px)}
.photo-hero h1{font-size:clamp(2.5rem,5.6vw,5rem)}
.itin-card{background:rgba(4,12,26,.72);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid var(--line);padding:24px 24px 20px;color:#fff;min-width:0}
.itin-card .ic-top{display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:var(--gold-l);margin-bottom:14px}
.itin-card .ic-top .pre{color:var(--gold);border:1px solid var(--line);padding:2px 8px;border-radius:999px}
.ic-city{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:6px 14px;align-items:baseline;padding:14px 0;border-top:1px solid rgba(255,255,255,.12)}
.ic-city .n{font-family:'Fraunces',serif;font-size:2.1rem;line-height:1;color:var(--gold-l)}
.ic-city h3{margin:0;font-size:1.25rem;color:#fff}
.ic-city .d{font-size:.78rem;color:rgba(255,255,255,.6);letter-spacing:.06em;text-align:right}
.ic-city p{grid-column:2/4;margin:0;font-size:.9rem;color:rgba(255,255,255,.72)}
@media (max-width:520px){.ic-city .d{grid-column:2/4;grid-row:2;text-align:left}.ic-city p{grid-row:3}}
.ic-facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid rgba(255,255,255,.12);border-bottom:1px solid rgba(255,255,255,.12);margin:2px 0 16px}
.ic-facts div{padding:12px 0;text-align:center;border-left:1px solid rgba(255,255,255,.1)}
.ic-facts div:first-child{border-left:0}
.ic-facts b{display:block;font-family:'Fraunces',serif;font-weight:500;font-size:1.3rem;color:#fff}
.ic-facts span{font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.55)}
.itin-card .btn{width:100%}
.itin-card .fine{font-size:.74rem;color:rgba(255,255,255,.5);margin:10px 0 0}
/* in-page subnav */
.subnav{position:sticky;top:79px;z-index:40;background:rgba(4,12,26,.96);border-bottom:1px solid var(--line)}
.subnav .container{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;padding-block:6px}
.subnav .container::-webkit-scrollbar{display:none}
.subnav a{flex:none;color:rgba(255,255,255,.78);text-decoration:none;font-size:.82rem;font-weight:500;padding:8px 12px;border-radius:2px;white-space:nowrap}
.subnav a:hover{color:#fff;background:rgba(255,255,255,.06)}
.subnav a.cta{color:var(--navy);background:var(--gold);margin-left:auto;font-weight:600}
[id]{scroll-margin-top:140px}
/* city tiles */
.cities{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
@media (max-width:760px){.cities{grid-template-columns:1fr}}
.city{position:relative;display:block;min-height:clamp(300px,36vw,460px);overflow:hidden;color:#fff;text-decoration:none;background:var(--navy)}
.city img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s}
.city:hover img{transform:scale(1.04)}
.city::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,12,26,.05) 30%,rgba(4,12,26,.92) 100%)}
.city .c-body{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:clamp(18px,3vw,30px)}
.city .c-days{display:inline-block;font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--navy);background:var(--gold);padding:4px 10px;margin-bottom:12px}
.city h3{font-size:clamp(1.8rem,3.2vw,2.6rem);color:#fff;margin:0 0 6px;font-weight:500}
.city p{color:rgba(255,255,255,.8);margin:0;max-width:46ch;font-size:.95rem}
.city .c-credit{position:absolute;top:8px;right:10px;z-index:2;font-size:.62rem;color:rgba(255,255,255,.5)}
.city .c-credit a{color:inherit}
/* itinerary */
.itin{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,2.1fr);gap:18px}
@media (max-width:980px){.itin{grid-template-columns:1fr}}
.itin-col h3.city-h{display:flex;justify-content:space-between;align-items:baseline;gap:10px;font-size:1.5rem;padding-bottom:10px;border-bottom:2px solid var(--gold);margin-bottom:14px}
.itin-col h3.city-h span{font-family:'Inter',sans-serif;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold-d);font-weight:700}
.days{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.itin-col:last-child .days{grid-template-columns:1fr}
@media (max-width:980px){.itin-col:last-child .days{grid-template-columns:repeat(auto-fit,minmax(168px,1fr))}}
.dcard{background:var(--surface);border:1px solid var(--border);border-top:3px solid var(--gold);padding:16px 16px 12px;min-width:0}
.dcard.lane-research{border-top-color:var(--sky)}.dcard.lane-cre{border-top-color:var(--terracotta)}.dcard.lane-capital{border-top-color:var(--teal)}
.dcard .dd{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted-2);font-weight:700}
.dcard h4{font-family:'Fraunces',serif;font-size:1.12rem;margin:4px 0 2px;color:var(--ink);font-weight:600;line-height:1.2}
.dcard .by{font-size:.8rem;color:var(--muted);margin:0 0 8px}
.dcard .by a{color:var(--gold-d)}
.dcard dl{margin:0}
.dcard dt{font-size:.64rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold-d);font-weight:700;margin-top:8px}
.dcard dd{margin:2px 0 0;font-size:.88rem;line-height:1.5;color:var(--muted)}
.prelim{display:flex;gap:12px;align-items:flex-start;background:#fff8e6;border:1px solid #edd9a3;color:#5c4400;padding:12px 16px;font-size:.9rem;margin:0 0 20px}
.prelim b{white-space:nowrap}
/* format strip */
.format{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border:1px solid var(--line)}
.format div{padding:22px 24px;border-left:1px solid var(--line)}
.format div:first-child{border-left:0}
.format .k{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold)}
.format h3{margin:6px 0 6px;font-size:1.25rem}
.format p{margin:0;font-size:.92rem}
@media (max-width:760px){.format{grid-template-columns:1fr}.format div{border-left:0;border-top:1px solid var(--line)}.format div:first-child{border-top:0}}
/* compact faq */
.faq.cols{max-width:none;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 40px}
.faq.cols details:last-child{border-bottom:0}
.faq.cols details{border-bottom:1px solid var(--border);border-top:0}
@media (max-width:860px){.faq.cols{grid-template-columns:1fr}}
.ink .faq summary{color:#fff}.ink .faq details{border-color:rgba(255,255,255,.14)}.ink .faq details p{color:rgba(255,255,255,.72)}
/* stat row */
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.stats div{padding:18px 16px;border-left:1px solid var(--line)}
.stats div:first-child{border-left:0}
.stats b{display:block;font-family:'Fraunces',serif;font-size:clamp(1.5rem,2.6vw,2.1rem);font-weight:500;color:#fff;line-height:1.1}
.stats span{font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.6)}
@media (max-width:760px){.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.stats div:nth-child(3){border-left:0}.stats div:nth-child(n+3){border-top:1px solid var(--line)}}
/* breadcrumb / back bar on inner pages */
.crumbbar{background:#fbf7ee;border-bottom:1px solid var(--border);font-size:.86rem}
.crumbbar .container{display:flex;gap:10px 16px;align-items:center;padding-block:9px;flex-wrap:wrap}
.crumbbar a.back{font-weight:600;color:var(--ink);text-decoration:none;border:1px solid var(--border);background:#fff;padding:6px 14px;border-radius:999px;white-space:nowrap}
.crumbbar a.back:hover{border-color:var(--gold)}
.crumbbar ol{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;color:var(--muted);min-width:0}
.crumbbar li{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:60vw}
.crumbbar li+li::before{content:"/";margin-right:6px;color:var(--muted-2)}
.crumbbar li a{color:var(--muted);text-decoration:none}.crumbbar li a:hover{color:var(--gold-d)}
/* light, refined pages */
.hero-light{background:linear-gradient(180deg,#fbf7ee 0%,#f3ead6 100%);color:var(--ink);padding:clamp(52px,7vw,92px) 0 clamp(44px,6vw,72px);border-bottom:1px solid var(--border)}
.hero-light .eyebrow{color:var(--gold-d)}
.hero-light h1{color:var(--ink);font-weight:500;font-size:clamp(2.4rem,5vw,4.2rem)}
.hero-light .lede{color:var(--muted)}
.hero-light .split{align-items:end}
.panel{display:flex;justify-content:flex-end;padding-left:22px}
.panel a{display:block;margin-left:-22px;transition:transform .2s}
.panel a:hover{transform:translateY(-4px)}
.panel img{display:block;width:clamp(96px,11vw,150px);height:clamp(96px,11vw,150px);border-radius:50%;object-fit:cover;border:4px solid #fff;box-shadow:0 18px 40px rgba(6,19,39,.18)}
@media (max-width:860px){.panel{justify-content:flex-start}}
.profiles{background:#f8f2e4}
.mprofile{display:grid;grid-template-columns:300px minmax(0,1fr);gap:clamp(24px,4vw,56px);align-items:start;background:#fff;border:1px solid var(--border);border-top:3px solid var(--gold);padding:clamp(22px,3vw,40px);box-shadow:0 24px 60px rgba(6,19,39,.07);margin-bottom:24px;scroll-margin-top:110px}
.mprofile.rev{grid-template-columns:minmax(0,1fr) 300px}.mprofile.rev .mp-photo{order:2}
.mp-photo img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:3px}
.mprofile h2{font-size:clamp(1.7rem,2.8vw,2.3rem);font-weight:500;margin:6px 0 4px}
.mprofile .role{margin:0 0 16px}
.mprofile .lane-link{margin-top:6px}
@media (max-width:860px){.mprofile,.mprofile.rev{grid-template-columns:1fr}.mprofile.rev .mp-photo{order:0}.mp-photo img{max-width:300px}}
.pagefoot{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:8px}
/* ===== Motion and imagery layer ===== */
.ph-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}
.photo-hero picture{z-index:0}
.photo-hero::after{z-index:1}
@media (prefers-reduced-motion:reduce){.ph-video{display:none}}
@keyframes rise{from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:none}}
@keyframes kenburns{from{transform:scale(1.0)}to{transform:scale(1.08)}}
.photo-hero .ph-img{animation:kenburns 22s ease-out both}
.photo-hero .kicker,.photo-hero h1,.photo-hero .lede,.photo-hero .btn-row,.photo-hero .hero-fine,.photo-hero .itin-card{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}
.photo-hero h1{animation-delay:.12s}.photo-hero .lede{animation-delay:.24s}.photo-hero .btn-row{animation-delay:.36s}.photo-hero .hero-fine{animation-delay:.46s}.photo-hero .itin-card{animation-delay:.5s}
.photo-hero h1 em{font-style:italic;background:linear-gradient(90deg,#f3c76a,#e9a825 60%,#fff2cc);-webkit-background-clip:text;background-clip:text;color:transparent}
.scroll-cue{position:absolute;left:50%;bottom:18px;z-index:3;transform:translateX(-50%);width:26px;height:42px;border:2px solid rgba(255,255,255,.55);border-radius:14px}
.scroll-cue::after{content:"";position:absolute;left:50%;top:8px;width:4px;height:8px;margin-left:-2px;border-radius:2px;background:#f3c76a;animation:cue 1.8s infinite}
@keyframes cue{0%{opacity:0;transform:translateY(0)}40%{opacity:1}100%{opacity:0;transform:translateY(14px)}}
@media (max-width:980px){.scroll-cue{display:none}}
/* ticker */
.ticker{background:#040c1a;border-top:1px solid var(--line);border-bottom:1px solid var(--line);overflow:hidden;white-space:nowrap}
.ticker .track{display:inline-flex;gap:0;animation:marquee 48s linear infinite;padding-block:14px}
.ticker span{font:500 .82rem Inter,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:rgba(255,255,255,.8);padding:0 26px}
.ticker span b{color:#f3c76a;font-weight:600}
.ticker span::after{content:"\25C6";color:#e9a825;margin-left:52px;font-size:.6rem;vertical-align:middle}
@keyframes marquee{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.ticker .track{animation:none}}
/* reveal on scroll (only when JS is on) */
.js .reveal{opacity:0;transform:translateY(30px);transition:opacity .9s cubic-bezier(.2,.7,.2,1),transform .9s cubic-bezier(.2,.7,.2,1)}
.js .reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.js .reveal{opacity:1;transform:none;transition:none}}
/* mosaic */
.mosaic{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-auto-rows:clamp(150px,17vw,230px);gap:10px}
.mosaic figure{position:relative;overflow:hidden;margin:0;background:var(--navy)}
.mosaic figure.w2{grid-column:span 2}.mosaic figure.h2{grid-row:span 2}
.mosaic img{width:100%;height:100%;object-fit:cover;display:block;transition:transform 1.2s cubic-bezier(.2,.7,.2,1),filter .6s}
.mosaic figure:hover img{transform:scale(1.07);filter:saturate(1.15)}
.mosaic figcaption{position:absolute;left:0;right:0;bottom:0;margin:0;padding:28px 14px 10px;background:linear-gradient(180deg,transparent,rgba(4,12,26,.85));color:#fff;font:500 .82rem Inter,sans-serif;letter-spacing:.04em}
.mosaic figcaption small{display:block;font-size:.66rem;color:rgba(255,255,255,.6);letter-spacing:0;margin-top:2px}
@media (max-width:760px){.mosaic{grid-template-columns:repeat(2,minmax(0,1fr))}.mosaic figure.w2{grid-column:span 2}}
/* full-bleed quote band */
.quote-band{position:relative;padding:clamp(96px,14vw,180px) 0;color:#fff;overflow:hidden;background:#061327}
.quote-band .qb-img{position:absolute;inset:-12% 0;width:100%;height:124%;object-fit:cover;will-change:transform}
.quote-band::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,12,26,.55),rgba(4,12,26,.78))}
.quote-band .container{position:relative;z-index:2;text-align:center}
.quote-band blockquote{margin:0 auto;font:500 clamp(2rem,5vw,4rem)/1.12 Fraunces,serif;max-width:18ch;letter-spacing:-.01em}
.quote-band blockquote em{color:#f3c76a}
.quote-band p{color:rgba(255,255,255,.75);margin-top:18px}
/* card glow */
.ink .card,.dark .card{position:relative}
.dark .card:hover,.ink .card:hover{border-color:rgba(233,168,37,.6);box-shadow:0 0 0 1px rgba(233,168,37,.25),0 30px 60px rgba(0,0,0,.35)}
.stats b{font-variant-numeric:tabular-nums}
.avatar{display:inline-block;width:var(--as,40px);height:var(--as,40px);border-radius:50%;object-fit:cover;border:2px solid #e9a825;background:#061327;vertical-align:middle;flex:none}
.avatars{display:inline-flex;vertical-align:middle}.avatars .avatar{margin-left:-10px;border-color:#fff}.avatars .avatar:first-child{margin-left:0}
.who{display:flex;align-items:center;gap:12px;margin-bottom:12px}.who .tag{margin:0}
.by .avatar{margin-right:8px}
.qa-meta .avatar{margin-right:8px}
.cguide{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(22px,4vw,48px);align-items:start;margin-top:30px;padding-top:30px;border-top:1px solid rgba(255,255,255,.12)}
.cguide.rev{grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr)}.cguide.rev .cg-photo{order:2}
.cg-photo{position:relative;overflow:hidden;min-height:100%}
.cg-photo img{display:block;width:100%;height:100%;min-height:340px;object-fit:cover;transition:transform 1.2s}
.cguide:hover .cg-photo img{transform:scale(1.04)}
.cg-days{position:absolute;left:14px;top:14px;font:600 .7rem Inter,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--navy);background:var(--gold);padding:5px 10px}
.cg-body h3{font-size:clamp(2rem,3.4vw,2.8rem);font-weight:500;margin:0 0 6px;color:#fff}
.cg-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 22px;margin-top:8px}
.cg-block{border-top:2px solid var(--gold);padding-top:10px}
.cg-block .k{font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-l);font-weight:600}
.cg-block p{margin:6px 0 0;font-size:.93rem;line-height:1.6}
.cg-src{font-size:.75rem;color:rgba(255,255,255,.5);margin-top:16px}.cg-src a{color:rgba(255,255,255,.7)}
@media (max-width:900px){.cguide,.cguide.rev{grid-template-columns:1fr}.cguide.rev .cg-photo{order:0}.cg-photo img{min-height:240px}}
@media (max-width:560px){.cg-grid{grid-template-columns:1fr}}
.signup-band{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:clamp(24px,4vw,56px);align-items:center}
@media (max-width:860px){.signup-band{grid-template-columns:1fr}}

/* ---------- wealth palette: ivory, champagne, emerald, gold ---------- */
:root{--cream:#fcf8ef;--cream-2:#f5ecd9;--surface:#fffdf8;--border:#e7d9b9;--gold:#d4a13a;--gold-d:#94680f;--gold-l:#f0cd7c;
  --em:#0c4a37;--em-2:#13684e;--em-3:#1f8a68;--emd:#08362a;--line:rgba(176,130,38,.32);--navy:#0a3a2c;--ink-2:#08362a}
body{background:var(--cream)}
.site-header{background:rgba(8,54,42,.95);border-bottom:1px solid rgba(240,205,124,.28)}
@media (max-width:1080px){.main-nav{background:var(--emd)}}
.event-bar{background:var(--emd)}
.subnav{background:rgba(8,54,42,.96)}
footer{background:linear-gradient(180deg,var(--em),var(--emd))}
.btn-gold{background:linear-gradient(180deg,#e7bb59,#d19a2e);color:#08362a;box-shadow:0 8px 24px rgba(180,130,30,.28)}
.btn-gold:hover{background:linear-gradient(180deg,#f0cd7c,#dcaa45)}
.hero{background:radial-gradient(ellipse at 80% 0%,var(--em-3) 0%,var(--em) 45%,var(--emd) 100%)}
.photo-hero{background:var(--em)}
.photo-hero::after{background:linear-gradient(90deg,rgba(6,40,30,.72) 0%,rgba(6,40,30,.42) 45%,rgba(6,40,30,0) 78%),linear-gradient(180deg,rgba(6,30,24,.35) 0%,rgba(0,0,0,0) 30%,rgba(6,40,30,.45) 72%,rgba(6,40,30,.82) 100%)}
@media (max-width:760px){.photo-hero::after{background:linear-gradient(180deg,rgba(6,40,30,.55) 0%,rgba(6,40,30,.35) 40%,rgba(6,40,30,.75) 75%,rgba(6,40,30,.9) 100%)}}
.itin-card{background:rgba(6,44,33,.55);border-color:rgba(240,205,124,.35)}
.quote-band{background:var(--em)}
.quote-band::after{background:linear-gradient(180deg,rgba(8,54,42,.30),rgba(8,54,42,.62))}
.band-green{background:radial-gradient(ellipse at 15% 0%,var(--em-3),var(--em) 55%,var(--emd))}
.ink{background:linear-gradient(180deg,#fffdf7 0%,#f6eddb 100%);color:var(--ink)}
.ink h2,.ink h3{color:var(--ink)}.ink p{color:var(--muted)}.ink .eyebrow{color:var(--gold-d)}
.ink .card{background:#fff;border-color:var(--border);box-shadow:0 14px 36px rgba(120,90,30,.08)}
.ink .note,.ink .trailer-fine{color:var(--muted)}.ink .checks li{color:var(--ink)}
.ink a{color:var(--em-2)}
.ink .btn-ghost{color:var(--em);border-color:var(--gold)}.ink .btn-ghost:hover{background:var(--em);color:#fff}
.ink .faq summary{color:var(--ink)}.ink .faq details{border-color:var(--border)}.ink .faq details p{color:var(--muted)}
.ink .stats{border-color:var(--border)}.ink .stats div{border-color:var(--border)}
.ink .stats b,.ink .stats b a{color:var(--em)}.ink .stats span{color:var(--muted)}
.ink .format{border-color:var(--border);background:#fff}.ink .format div{border-color:var(--border)}.ink .format .k{color:var(--gold-d)}
.ink .cguide{border-top-color:var(--border)}.ink .cg-body h3{color:var(--ink)}.ink .cg-block{border-top-color:var(--gold)}
.ink .cg-block .k{color:var(--gold-d)}.ink .cg-block p{color:var(--muted)}.ink .cg-src{color:var(--muted-2)}.ink .cg-src a{color:var(--muted)}
.ink figcaption{color:var(--muted-2)}
.ink .city h3{color:#fff}.ink .city p{color:rgba(255,255,255,.88)}.ink .city .c-credit,.ink .city small{color:rgba(255,255,255,.6)}
.dark .card:hover,.ink .card:hover{border-color:var(--gold);box-shadow:0 0 0 1px rgba(212,161,58,.3),0 24px 50px rgba(120,90,30,.16)}
.trailer{background:radial-gradient(ellipse at 50% 0%,#fffdf6 0%,#f7efdc 55%,#efe2c3 100%);color:var(--ink)}
.trailer h2{color:var(--ink)}.trailer .eyebrow{color:var(--gold-d)}.trailer-fine{color:var(--muted)}
.trailer .player{box-shadow:0 40px 90px rgba(60,45,10,.28),0 0 0 1px rgba(212,161,58,.45)}
.ticker{background:var(--em)}

/* ---------- Colombia in frames: interactive gallery ---------- */
.frames-sec{background:linear-gradient(180deg,var(--cream) 0%,#f3e9d2 100%)}
.fr-bar{display:flex;justify-content:space-between;align-items:center;gap:12px 24px;flex-wrap:wrap;margin:0 0 22px}
.fr-tabs{display:flex;flex-wrap:wrap;gap:8px}
.fr-tab{font:600 .78rem Inter,sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:10px 16px;border-radius:999px;border:1px solid var(--border);background:#fff;color:var(--ink);cursor:pointer;display:inline-flex;align-items:center;gap:8px;transition:background .25s,color .25s,border-color .25s,transform .2s}
.fr-tab span{font-size:.68rem;letter-spacing:0;background:var(--cream-2);color:var(--gold-d);border-radius:999px;padding:1px 7px}
.fr-tab:hover{border-color:var(--gold);transform:translateY(-1px)}
.fr-tab[aria-pressed=true]{background:var(--em);color:#fff;border-color:var(--em)}.fr-tab[aria-pressed=true] span{background:rgba(255,255,255,.16);color:var(--gold-l)}
.fr-hint{margin:0;font-size:.82rem;color:var(--muted)}
.fr-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-auto-rows:clamp(180px,19vw,260px);grid-auto-flow:dense;gap:14px}
.fr-item{margin:0;position:relative;min-width:0;opacity:1;transform:none;transition:opacity .45s,transform .45s}
.fr-item.big{grid-column:span 2;grid-row:span 2}.fr-item.wide{grid-column:span 2}.fr-item.tall{grid-row:span 2}
.fr-item.out{opacity:0;transform:scale(.96)}
.fr-item[hidden]{display:none}
.fr-open{all:unset;box-sizing:border-box;position:absolute;inset:0;cursor:zoom-in;overflow:hidden;border-radius:6px;background:var(--em);box-shadow:0 10px 28px rgba(60,45,10,.14)}
.fr-open:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.fr-open img{width:100%;height:100%;object-fit:cover;display:block;transition:transform 1.4s cubic-bezier(.2,.7,.2,1),filter .6s}
.fr-open::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,40,30,0) 45%,rgba(6,40,30,.82) 100%);transition:opacity .4s}
.fr-open:hover img,.fr-open:focus-visible img{transform:scale(1.07);filter:saturate(1.12) brightness(1.04)}
.fr-num{position:absolute;left:14px;top:12px;z-index:2;font:500 .8rem Fraunces,serif;color:#fff;letter-spacing:.06em;text-shadow:0 1px 6px rgba(0,0,0,.4)}
.fr-zoom{position:absolute;right:12px;top:12px;z-index:2;width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:rgba(255,253,248,.88);color:var(--em);font-size:.95rem;opacity:0;transform:scale(.8);transition:opacity .3s,transform .3s}
.fr-open:hover .fr-zoom,.fr-open:focus-visible .fr-zoom{opacity:1;transform:none}
.fr-cap{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:16px 18px 16px;color:#fff;display:block}
.fr-tag{display:inline-block;font:600 .62rem Inter,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:#08362a;background:var(--gold-l);padding:3px 8px;border-radius:2px;margin-bottom:8px}
.fr-cap b{display:block;font:500 clamp(1.05rem,1.6vw,1.35rem)/1.2 Fraunces,serif}
.fr-desc{display:block;font-size:.84rem;line-height:1.45;color:rgba(255,255,255,.85);max-height:0;opacity:0;overflow:hidden;transition:max-height .45s,opacity .45s,margin .45s}
.fr-open:hover .fr-desc,.fr-open:focus-visible .fr-desc{max-height:5em;opacity:1;margin-top:6px}
.fr-item.big .fr-cap b{font-size:clamp(1.4rem,2.4vw,2rem)}.fr-item.big .fr-desc{max-height:5em;opacity:1;margin-top:6px}
@media (hover:none){.fr-desc{max-height:5em;opacity:1;margin-top:6px}.fr-zoom{opacity:1;transform:none}}
@media (max-width:1000px){.fr-grid{grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:clamp(170px,30vw,240px)}}
@media (max-width:560px){.fr-grid{grid-template-columns:1fr;grid-auto-rows:230px}.fr-item.big,.fr-item.wide{grid-column:auto}.fr-item.big,.fr-item.tall{grid-row:span 1}.fr-hint{display:none}}
.fr-box{border:0;padding:0;margin:0;width:100vw;height:100vh;max-width:none;max-height:none;background:transparent;color:#fff;overflow:hidden}
.fr-box::backdrop{background:rgba(5,30,23,.94);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.fr-box[open]{display:flex;align-items:center;justify-content:center;animation:frIn .35s ease}
@keyframes frIn{from{opacity:0}to{opacity:1}}
.fr-box figure{margin:0;display:flex;flex-direction:column;align-items:center;gap:16px;max-width:min(1400px,92vw);padding:64px 0 24px}
.fr-stage{display:flex;align-items:center;justify-content:center}
.fr-stage img{max-width:min(1400px,92vw);max-height:calc(100vh - 210px);width:auto;height:auto;display:block;border-radius:4px;box-shadow:0 30px 80px rgba(0,0,0,.5);transition:opacity .3s,transform .3s}
.fr-stage img.swap{opacity:0;transform:scale(.985)}
.fr-box figcaption{text-align:center;max-width:70ch;padding:0 16px}
.fr-box figcaption b{display:block;font:500 clamp(1.3rem,2.4vw,1.8rem) Fraunces,serif;margin:4px 0}
.fr-box figcaption>span:not(.fr-count){display:block;color:rgba(255,255,255,.8)}
.fr-box figcaption small{display:block;margin-top:8px;color:rgba(255,255,255,.55);font-size:.76rem}.fr-box figcaption small a{color:inherit}
.fr-count{font:600 .7rem Inter,sans-serif;letter-spacing:.22em;color:var(--gold-l)}
.fr-nav,.fr-close{position:absolute;border:1px solid rgba(240,205,124,.5);background:rgba(8,54,42,.6);color:#fff;width:52px;height:52px;border-radius:50%;font-size:1.3rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .2s,transform .2s}
.fr-nav:hover,.fr-close:hover{background:var(--gold);color:#08362a;transform:scale(1.06)}
.fr-nav.prev{left:clamp(10px,2vw,28px);top:50%;margin-top:-26px}.fr-nav.next{right:clamp(10px,2vw,28px);top:50%;margin-top:-26px}
.fr-close{right:clamp(10px,2vw,28px);top:clamp(10px,2vw,22px);width:46px;height:46px;font-size:1.05rem}
@media (max-width:640px){.fr-nav{top:auto;bottom:14px;margin-top:0}.fr-box figure{padding-bottom:84px}}
@media (prefers-reduced-motion:reduce){.fr-item,.fr-open img,.fr-stage img,.fr-desc{transition:none}.fr-box[open]{animation:none}}
"""

NAV = [('index.html', 'Home'), ('colombia-2027.html', 'Colombia 2027'), ('members.html', 'Members'), ('the-show.html', 'The Show'), ('questions.html', 'Questions')]

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
EVENT = dict(name='Tierra Firme Investor Lab', city='Bogotá and Medellín', start='2027-03-07', end='2027-03-12',
             dates='7 to 12 March 2027', short='March 2027')
PRELIM = 'Preliminary. Dates, cities and sessions may change while we put the program together.'

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
    'medellin': dict(base='/img/bogota/medellin-towers', w=(1920, 960), ratio=(1920, 1280),
                     alt='Residential and office towers of Medellín climbing the green slopes of the Aburrá Valley',
                     title='Medellín', author='Mussi Katz', lic='CC0 1.0',
                     lic_url='https://creativecommons.org/publicdomain/zero/1.0/',
                     src='https://commons.wikimedia.org/wiki/File:Colombia_Medellin.jpg'),
    'general': dict(base='/img/bogota/bogota-general-view', w=(1600, 960), ratio=(1600, 1067),
                    alt='Wide view over Bogotá, its high-rise center and the flat savanna beyond',
                    title='Bogotá, general view', author='Raul Cuellar', lic='CC0 1.0',
                    lic_url='https://creativecommons.org/publicdomain/zero/1.0/',
                    src='https://commons.wikimedia.org/wiki/File:Bogota_general_view_2015.jpg'),
}

PHOTOS.update({
    'agora': dict(base='/img/bogota/agora-bogota-convention-center', w=(1920, 960), ratio=(1920, 1234),
                  alt='Ágora Bogotá, the city convention center, a glass and steel building beside the Corferias exhibition grounds',
                  title='Ágora Bogotá convention center', author='Mriobomorales', lic='CC BY-SA 4.0',
                  lic_url='https://creativecommons.org/licenses/by-sa/4.0/',
                  src='https://commons.wikimedia.org/wiki/File:Agora_and_Corferias_event_and_buissines_district.png'),
    'colon': dict(base='/img/bogota/teatro-colon-ceiling', w=(1920, 960), ratio=(1920, 1440),
                  alt='The painted ceiling and crystal chandelier of the Teatro Colón in Bogotá',
                  title='Teatro Colón, Bogotá', author='Ricardoinbaviera', lic='CC BY-SA 3.0',
                  lic_url='https://creativecommons.org/licenses/by-sa/3.0/',
                  src='https://commons.wikimedia.org/wiki/File:Interior_Teatro_Colon_Bogota.jpg'),
    'tequendama': dict(base='/img/bogota/hotel-tequendama', w=(1920, 960), ratio=(1920, 1091),
                       alt='The Hotel Tequendama in Bogotá’s Centro Internacional, seen from Carrera Décima',
                       title='Hotel Tequendama, Centro Internacional, Bogotá', author='Peter Angritt', lic='CC BY-SA 4.0',
                       lic_url='https://creativecommons.org/licenses/by-sa/4.0/',
                       src='https://commons.wikimedia.org/wiki/File:Hotel_Tequendama_-_Vista_desde_Carrera_D%C3%A9cima.jpg'),
})

PHOTOS.update({
    'metro_night': dict(base='/img/medellin/medellin-metrocable-night', w=(1920, 960), ratio=(1920, 1278),
                        alt='Medellín at night seen from the Metrocable, the city lights filling the Aburrá Valley',
                        title='Medellín at night from the Metrocable', author='JoranL', lic='CC BY-SA 4.0',
                        lic_url='https://creativecommons.org/licenses/by-sa/4.0/',
                        src='https://commons.wikimedia.org/wiki/File:Metrocable_in_Medell%C3%ADn_by_night.jpg'),
    'metro_k': dict(base='/img/medellin/medellin-metrocable-line-k', w=(1920, 960), ratio=(1920, 1278),
                    alt='Metrocable Line K cable cars above the hillside neighborhoods of northeast Medellín',
                    title='Metrocable Line K, Medellín', author='Bernard Gagnon', lic='CC BY-SA 4.0',
                    lic_url='https://creativecommons.org/licenses/by-sa/4.0/',
                    src='https://commons.wikimedia.org/wiki/File:L%C3%ADnea_K_(Medell%C3%ADn_Metrocable)_01.jpg'),
    'botero': dict(base='/img/medellin/medellin-plaza-botero', w=(1920, 960), ratio=(1920, 1064),
                   alt='Plaza Botero in central Medellín, with bronze sculptures by Fernando Botero among palm trees',
                   title='Plaza Botero, Medellín', author='Steffen Schmitz', lic='CC BY-SA 4.0',
                   lic_url='https://creativecommons.org/licenses/by-sa/4.0/',
                   src='https://commons.wikimedia.org/wiki/File:Medell%C3%ADn,_Plaza_Botero,_2023-07_CN-01.jpg'),
    'poblado': dict(base='/img/medellin/medellin-el-poblado-night', w=(1920, 960), ratio=(1920, 1280),
                    alt='Apartment towers of El Poblado, Medellín, lit at night among the trees',
                    title='El Poblado at night, Medellín', author='william gil', lic='CC BY 2.0',
                    lic_url='https://creativecommons.org/licenses/by/2.0/',
                    src='https://commons.wikimedia.org/wiki/File:El_poblado,_Medell%C3%ADn.jpg'),
})

def credit(p):
    p = PHOTOS[p]
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

def photo_hero(p, inner, video=None):
    vid = (f'<video class="ph-video" autoplay muted loop playsinline preload="metadata" poster="{video}-poster.webp" aria-hidden="true">'
           f'<source src="{video}.mp4" type="video/mp4"></video>') if video else ''
    cue = '<span class="scroll-cue" aria-hidden="true"></span>' if video else ''
    return (f'<section class="photo-hero"><picture>{img(p, "100vw", "ph-img", eager=True)}</picture>{vid}'
            f'<div class="container">{inner}</div>{cue}<p class="ph-credit">{"Film footage: Pexels. " if video else ""}{credit(p)}</p></section>')

TICKER_ITEMS = ['<b>Bogotá</b> · 3 days', '<b>Medellín</b> · 2 days', '<b>March 2027</b> · preliminary', '<b>Invitation</b> · exclusive group',
                '<b>US$46.0B</b> in deals tracked by Sovereo', '<b>US$3.84B</b> in Colombia alone', 'Boardroom mornings',
                'Verified field visits', 'Cultural evenings', '<b>Three</b> practitioners · three lanes', 'Any currency · solid ground']
def ticker():
    items = ''.join(f'<span>{t}</span>' for t in TICKER_ITEMS)
    return f'<div class="ticker" aria-hidden="true"><div class="track">{items}{items}</div></div>'

FRAMES = [  # (photo, category, title, description, size)
    ('towers', 'bogota', 'Bogotá, below Monserrate', 'Office and residential towers of central Bogotá, with Monserrate and the Eastern Hills behind.', 'big'),
    ('colpatria', 'bogota', 'Torre Colpatria', 'Torre Colpatria lit at night, one of Bogotá’s best-known towers.', 'tall'),
    ('metro_night', 'medellin', 'Medellín after dark', 'The city lights fill the Aburrá Valley, seen from the Metrocable.', 'wide'),
    ('agora', 'landmarks', 'Ágora Bogotá', 'The city’s convention center, beside the Corferias exhibition grounds.', ''),
    ('botero', 'medellin', 'Plaza Botero', 'Central Medellín, with bronze sculptures by Fernando Botero.', ''),
    ('downtown', 'bogota', 'Downtown Bogotá', 'The high-rise center seen from the Torre Colpatria observation deck.', 'wide'),
    ('colon', 'landmarks', 'Teatro Colón', 'The painted ceiling and chandelier of Bogotá’s historic theater.', 'tall'),
    ('medellin', 'medellin', 'The Aburrá Valley', 'Towers of Medellín climbing the green slopes of the valley.', ''),
    ('twilight', 'bogota', 'Bogotá at twilight', 'The city from Monserrate as the lights come on across the savanna.', ''),
    ('metro_k', 'medellin', 'Metrocable Line K', 'Cable cars above the hillside neighborhoods of northeast Medellín.', 'wide'),
    ('tequendama', 'landmarks', 'Hotel Tequendama', 'In the Centro Internacional, Bogotá’s international business district.', ''),
    ('poblado', 'medellin', 'El Poblado', 'Apartment towers of El Poblado, Medellín, lit at night.', ''),
    ('general', 'bogota', 'The savanna', 'Bogotá’s center and the flat high plain beyond.', ''),
]
FRAME_CATS = [('all', 'All'), ('bogota', 'Bogotá'), ('medellin', 'Medellín'), ('landmarks', 'Landmarks')]

def frames_html():
    counts = {c: sum(1 for f in FRAMES if c == 'all' or f[1] == c) for c, _ in FRAME_CATS}
    tabs = ''.join(f'<button type="button" class="fr-tab" data-cat="{c}" aria-pressed="{"true" if c == "all" else "false"}">{n}<span>{counts[c]}</span></button>'
                   for c, n in FRAME_CATS)
    items = []
    for n, (p, cat, title, desc, size) in enumerate(FRAMES, 1):
        x = PHOTOS[p]; big = x['w'][0]
        label = dict(FRAME_CATS)[cat]
        items.append(
            f'<figure class="fr-item {size}" data-cat="{cat}" data-full="{x["base"]}-{big}.webp" data-title="{html.escape(title)}" '
            f'data-desc="{html.escape(desc)}" data-credit="{html.escape(x["author"])}, {x["lic"]}" data-src="{x["src"]}">'
            f'<button type="button" class="fr-open" aria-label="Open {html.escape(title)}">{img(p, "(max-width:640px) 100vw, (max-width:1000px) 50vw, 34vw")}'
            f'<span class="fr-num">{n:02d}</span><span class="fr-zoom" aria-hidden="true">&#x2922;</span>'
            f'<span class="fr-cap"><span class="fr-tag">{label}</span><b>{html.escape(title)}</b><span class="fr-desc">{html.escape(desc)}</span></span></button></figure>')
    return (f'<div class="frames"><div class="fr-bar"><div class="fr-tabs" role="group" aria-label="Filter photographs">{tabs}</div>'
            f'<p class="fr-hint">Tap any frame to open it full screen. Use the arrow keys to move between frames.</p></div>'
            f'<div class="fr-grid">{"".join(items)}</div></div>'
            '<dialog class="fr-box" id="fr-box" aria-label="Photograph viewer"><figure><div class="fr-stage"><img alt="" id="fr-img"></div>'
            '<figcaption><span class="fr-count" id="fr-count"></span><b id="fr-title"></b><span id="fr-desc"></span>'
            '<small>Photo: <a id="fr-credit" rel="noopener" target="_blank"></a>, via Wikimedia Commons</small></figcaption></figure>'
            '<button type="button" class="fr-nav prev" id="fr-prev" aria-label="Previous photograph">&#8592;</button>'
            '<button type="button" class="fr-nav next" id="fr-next" aria-label="Next photograph">&#8594;</button>'
            '<button type="button" class="fr-close" id="fr-close" aria-label="Close" autofocus>&#10005;</button></dialog>')

def quote_band(p, quote, sub, cta=''):
    return (f'<section class="quote-band">{img(p, "100vw", "qb-img")}<div class="container"><blockquote class="reveal">{quote}</blockquote>'
            f'<p class="reveal">{sub}</p>{cta}</div></section>')

def hero_preload(p):
    x = PHOTOS[p]
    big, small = x['w']
    return (f'<link rel="preload" as="image" href="{x["base"]}-{small}.webp" imagesrcset="{x["base"]}-{small}.webp {small}w, '
            f'{x["base"]}-{big}.webp {big}w" imagesizes="100vw" fetchpriority="high">')

def itin_card(cta='colombia-2027.html#invite'):
    return f"""<aside class="itin-card" aria-label="Investor Lab 2027 at a glance">
   <div class="ic-top"><span>Investor Lab 2027</span><span class="pre">Preliminary</span></div>
   <div class="ic-city"><span class="n">3</span><h3>Bogotá</h3><span class="d">Sun 7 to Wed 10 March, morning</span><p>Arrival, then the country, property and business.</p></div>
   <div class="ic-city"><span class="n">2</span><h3>Medellín</h3><span class="d">Wed 10 evening to Fri 12 March</span><p>Field visits and culture, then the decision framework.</p></div>
   <div class="ic-facts"><div><b>6 days</b><span>5 nights</span></div><div><b>Private</b><span>Exclusive group</span></div><div><b>3</b><span>Lanes</span></div></div>
   <a href="{cta}" class="btn btn-gold">Get the information sheet</a>
   <p class="fine">Dates, cities and sessions may change. Newsletter subscribers hear first.</p>
  </aside>"""

def city_tile(p, city, days, text, href):
    x = PHOTOS[p]
    return (f'<a class="city lift" href="{href}">{img(p, "(max-width:760px) 100vw, 50vw")}'
            f'<span class="c-credit">Photo: {html.escape(x["author"])}, {x["lic"]}</span><div class="c-body"><span class="c-days">{days}</span>'
            f'<h3>{city}</h3><p>{text}</p></div></a>')

def cities_html():
    return ('<div class="cities">'
            + city_tile('downtown', 'Bogotá', '3 days · 8 to 10 March, morning', 'The capital, where the rules are made: the central bank, the tax authority, notaries and ministries. Briefings on the country, property and business.', 'colombia-2027.html#itinerary')
            + city_tile('medellin', 'Medellín', '2 days · 10 March evening to 12 March', "Colombia's second-largest city. Arrive Wednesday evening, then verified field visits and the decision framework before you fly home.", 'colombia-2027.html#itinerary')
            + '</div>')

def event_strip():
    return ('<div class="event-strip"><div><b>6 days</b><span>5 nights · 7 to 12 March 2027</span></div><div><b>3 lanes</b><span>Asset · Capital · Country</span></div>'
            '<div><b>Exclusive</b><span>A private group of investors</span></div><div><b><a href="https://www.sovereo.com/deal-record" rel="noopener" style="color:inherit;text-decoration:none">US$46.0B</a></b><span>Business deals tracked by Sovereo</span></div></div>')

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
    ("What is the Investor Lab 2027?",
     "A preliminary six-day, five-night program in Colombia for an exclusive group of investors: three days in Bogotá and two in Medellín, 7 to 12 March 2027. Short boardroom briefings, verified field visits and cultural evenings. "
     "It is a seminar, not a sales event. Details go to newsletter subscribers first."),
    ("Who is Tierra Firme for?",
     "Individuals, families and family offices in the US, Canada and Europe who want to understand a market abroad before committing capital, "
     "including households priced out of ownership at home and retirees stretching a fixed income."),
    ("Is Tierra Firme free?",
     "The show, the sourced answers and the Tierra Firme Newsletter are free. The Investor Lab is a paid seminar, and its details go to newsletter subscribers first."),
    ("What is the Tierra Firme Newsletter?",
     "A free email from Tierra Firme: Investor Lab 2027 updates, short briefings on Colombia and Latin America across property, business and family capital, and country research, plus new answers and episodes. Unsubscribe in one click."),
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
              "<a href=\"https://www.sovereo.com/deal-record\" rel=\"noopener\">Global Deal Record</a> has tracked US$46.0 billion in business "
              "deals so far, including US$3.84 billion in Colombia, each from an official source. "
              "He has been a professor of economics and decision science for over 24 years, and has lived in Bogotá since 2020."),
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

MEMBER_BY_LANE = {m['lane']: m for m in MEMBERS}
def avatar(m, size=40):
    """Small round member photo with a hover title, for inline mentions."""
    return (f'<img class="avatar" src="{m["photo"]}-320.webp" alt="{html.escape(m["name"])}" title="{html.escape(m["name"])}" '
            f'width="{size}" height="{size}" style="--as:{size}px" loading="lazy" decoding="async">') if m.get('photo') else ''
def avatars(size=34):
    return '<span class="avatars">' + ''.join(avatar(m, size) for m in MEMBERS) + '</span>'
def who(lane, text, size=44):
    """Tag line with the member's photo in front of it."""
    return f'<div class="who">{avatar(MEMBER_BY_LANE[lane], size)}<span>{text}</span></div>'

EPISODES = [
    ('All three', 'The World Is Mispriced', 'The founding thesis: prudent capital looks past its home market. Currency, political and structural conditions can make the next asset more reachable abroad, with risks to match.'),
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
    crumbbar = ''
    if crumbs and fname != 'index.html':
        parent = crumbs[-2] if len(crumbs) > 1 else ('', 'Home')
        ph = '/' + parent[0].replace('.html', '') if parent[0] else '/'
        trail = ''.join((f'<li><a href="/{h.replace(".html", "") if h else ""}">{html.escape(n)}</a></li>' if k < len(crumbs) - 1
                         else f'<li aria-current="page">{html.escape(n)}</li>') for k, (h, n) in enumerate(crumbs))
        crumbbar = (f'<nav class="crumbbar" aria-label="Breadcrumb"><div class="container"><a class="back" href="{ph}">&larr; Back to {html.escape(parent[1])}</a>'
                    f'<ol>{trail}</ol></div></nav>')
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
{banner}<div class="event-bar"><div class="container"><span class="pre">Preliminary</span><span><b>Investor Lab 2027</b><span class="eb-long"> · Bogotá 3 days · Medellín 2 days</span> · 7 to 12 March</span><a href="/colombia-2027#invite">Get the information sheet</a></div></div>
<header class="site-header">
 <div class="container nav-wrap">
  <a href="index.html" class="brand"><img src="/img/logo-light.webp" alt="Tierra Firme" width="120" height="56"></a>
  <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="main-nav">&#9776;</button>
  <nav class="main-nav" id="main-nav" aria-label="Main">{nav}<a href="newsletter.html" class="btn btn-gold">Free newsletter</a></nav>
 </div>
</header>
<main>
{crumbbar}
{body}
</main>
<footer>
 <div class="container">
  <div class="footer-grid">
   <a href="index.html" class="brand"><img src="/img/logo-light.webp" alt="Tierra Firme" width="120" height="56"></a>
   <nav class="footer-nav" aria-label="Footer">{''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}<a href="newsletter.html">Newsletter</a><a href="credits.html">Photo credits</a></nav>
  </div>
  <p class="disclaimer">{DISCLAIMER}</p>
  <p class="legal">{LEGAL}</p>
  <p class="credit">&copy; 2026 Tierra Firme. Murphy D. Cheatham II, Shawn Christopher Leamon and Todd Allyn.</p>
 </div>
</footer>
<script>
(function(){{
 var root=document.documentElement;root.classList.add('js');
 var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
 var sel='.section-head,.card,.dcard,.city,.mprofile,.qcard,.faq details,.photo,.day,.step,.facts,.format>div,.stats>div,.signup-band>div,.checks';
 var els=Array.prototype.slice.call(document.querySelectorAll(sel)).filter(function(e){{return !e.closest('.photo-hero')&&!e.closest('.ticker');}});
 els.forEach(function(e,i){{e.classList.add('reveal');var sib=e.parentElement?Array.prototype.indexOf.call(e.parentElement.children,e):0;e.style.transitionDelay=(Math.min(sib,5)*0.08)+'s';}});
 var all=document.querySelectorAll('.reveal');
 if(reduce||!('IntersectionObserver' in window)){{all.forEach(function(e){{e.classList.add('in');}});}}
 else{{var io=new IntersectionObserver(function(es){{es.forEach(function(en){{if(en.isIntersecting){{en.target.classList.add('in');io.unobserve(en.target);}}}});}},{{rootMargin:'0px 0px -8% 0px',threshold:0.08}});all.forEach(function(e){{io.observe(e);}});}}
 /* count-up numbers in stat rows */
 var nums=document.querySelectorAll('.stats b, .ic-facts b');
 var countUp=function(b){{var el=b.querySelector('a')||b;var txt=el.textContent;var m=txt.match(/([0-9]+(?:[.][0-9]+)?)/);if(!m)return;var end=parseFloat(m[1]);var dec=(m[1].split('.')[1]||'').length;var pre=txt.slice(0,m.index),post=txt.slice(m.index+m[1].length);var t0=null;
  var step=function(ts){{if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/1400);var e=1-Math.pow(1-k,3);el.textContent=pre+(end*e).toFixed(dec)+post;if(k<1)requestAnimationFrame(step);}};requestAnimationFrame(step);}};
 if(!reduce&&'IntersectionObserver' in window){{var io2=new IntersectionObserver(function(es){{es.forEach(function(en){{if(en.isIntersecting){{countUp(en.target);io2.unobserve(en.target);}}}});}},{{threshold:0.5}});nums.forEach(function(n){{io2.observe(n);}});}}
 /* gentle parallax on quote bands */
 var bands=document.querySelectorAll('.quote-band .qb-img');
 if(bands.length&&!reduce){{var par=function(){{bands.forEach(function(im){{var r=im.parentElement.getBoundingClientRect();var p=(r.top+r.height/2-innerHeight/2)/innerHeight;im.style.transform='translateY('+(p*-60).toFixed(1)+'px)';}});}};addEventListener('scroll',par,{{passive:true}});par();}}
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

 var fr=document.querySelector('.frames');
 if(fr){{var items=[].slice.call(fr.querySelectorAll('.fr-item')),tabs=[].slice.call(fr.querySelectorAll('.fr-tab')),box=document.getElementById('fr-box'),
   bi=document.getElementById('fr-img'),cur=0,vis=items,x0=null;
  var filter=function(cat){{tabs.forEach(function(t){{t.setAttribute('aria-pressed',t.getAttribute('data-cat')===cat?'true':'false');}});
   items.forEach(function(it){{var on=cat==='all'||it.getAttribute('data-cat')===cat;
    if(on){{it.hidden=false;it.classList.add('out');requestAnimationFrame(function(){{requestAnimationFrame(function(){{it.classList.remove('out');}});}});}}else{{it.hidden=true;}}}});
   vis=items.filter(function(it){{return !it.hidden;}});}};
  tabs.forEach(function(t){{t.addEventListener('click',function(){{filter(t.getAttribute('data-cat'));}});}});
  var show=function(n){{cur=(n+vis.length)%vis.length;var it=vis[cur];bi.classList.add('swap');
   var im=new Image();im.onload=im.onerror=function(){{bi.src=it.getAttribute('data-full');bi.alt=it.querySelector('img').alt;bi.classList.remove('swap');}};im.src=it.getAttribute('data-full');
   document.getElementById('fr-title').textContent=it.getAttribute('data-title');document.getElementById('fr-desc').textContent=it.getAttribute('data-desc');
   var c=document.getElementById('fr-credit');c.textContent=it.getAttribute('data-credit');c.href=it.getAttribute('data-src');
   document.getElementById('fr-count').textContent=(cur+1<10?'0':'')+(cur+1)+' / '+(vis.length<10?'0':'')+vis.length;}};
  items.forEach(function(it){{it.querySelector('.fr-open').addEventListener('click',function(){{var n=vis.indexOf(it);if(!box.showModal){{window.open(it.getAttribute('data-full'));return;}}
   show(n);box.showModal();document.body.style.overflow='hidden';}});}});
  var close=function(){{box.close();}};
  box.addEventListener('close',function(){{document.body.style.overflow='';var it=vis[cur];if(it)it.querySelector('.fr-open').focus();}});
  document.getElementById('fr-close').addEventListener('click',close);
  document.getElementById('fr-prev').addEventListener('click',function(){{show(cur-1);}});
  document.getElementById('fr-next').addEventListener('click',function(){{show(cur+1);}});
  box.addEventListener('click',function(e){{if(e.target===box)close();}});
  box.addEventListener('keydown',function(e){{if(e.key==='ArrowRight'){{show(cur+1);}}else if(e.key==='ArrowLeft'){{show(cur-1);}}}});
  box.addEventListener('pointerdown',function(e){{x0=e.clientX;}});
  box.addEventListener('pointerup',function(e){{if(x0===null)return;var dx=e.clientX-x0;x0=null;if(Math.abs(dx)>50)show(cur+(dx<0?1:-1));}});
 }}
}})();
</script>
</body>
</html>
"""
    out = re.sub(r'href="index\.html(#[^"]*)?"', lambda m: 'href="/' + (m.group(1) or '') + '"', out)
    out = re.sub(r'href="(?!https?:|/|#|mailto:)([a-z0-9/\-]+)\.html(#[^"]*)?"', lambda m: 'href="/' + m.group(1) + (m.group(2) or '') + '"', out)
    return out


def signup_block(dark=True, btn='Get the free newsletter', ok="You're subscribed to the Tierra Firme Newsletter. Investor Lab updates, new research and episodes come to you first.", source='', preset=()):
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
    {portrait(m, 104)}
    <span class="tag tag-{m['key']}">{m['seat']} · {m['area']}</span>
    <h3>{m['name']}</h3>
    <p>{m['show']}</p>
    <a class="lane-link" href="/lanes/{LANE[m['lane']]['slug']}">The {m['area'].lower()} lane &rarr;</a>
   </article>""")
    return '<div class="grid-3">' + ''.join(out) + '</div>'

# ---------- Why Latin America, why Colombia ----------
# Each Colombia point links to a sourced answer page; keep claims to what those pages support.
def why_html(alt=False):
    q = lambda slug, text: f'<a href="/questions/{slug}">{text}</a>'
    return f"""<section{' class="alt"' if alt else ''} id="why">
 <div class="container">
  <div class="section-head">
   <span class="eyebrow">Why Latin America. Why Colombia.</span>
   <h2>The case for looking south, and the rules behind it.</h2>
   <p class="lede">The benefits are real, and so are the risks. Here is what draws buyers from the US, Canada and Europe, with the rule or source behind each point.</p>
  </div>
  <div class="grid-3">
   <article class="card bar-research"><span class="tag tag-research">Latin America</span><h3>Close to home</h3><p>Latin America shares or sits near North American time zones and is a short flight away, so owning or running something there is practical from home.</p></article>
   <article class="card bar-research"><span class="tag tag-research">Latin America</span><h3>Your currency goes further</h3><p>Many local currencies trade cheaply against the dollar, euro and loonie, so the same income or savings can reach further. The rate can also move against you while you hold. {q('how-the-exchange-rate-changes-your-real-estate-return', 'How the exchange rate works')}.</p></article>
   <article class="card bar-research"><span class="tag tag-research">Latin America</span><h3>Markets others overlook</h3><p>Political and structural risk is often priced in, sometimes more than it should be. Research tells the difference. {q('currency-political-and-structural-arbitrage', 'The three arbitrages')}.</p></article>
  </div>
  <div class="grid-2" style="margin-top:28px">
   <div>
    <h3 style="font-size:1.5rem">Why Colombia</h3>
    <ul class="checks">
     <li>Foreigners can own property with the same rights as Colombians. {q('can-foreigners-buy-property-in-colombia', 'Source and detail')}</li>
     <li>A foreign investment registered with Banco de la República carries the right to bring the money home. {q('register-foreign-investment-in-colombia', 'How registration works')}</li>
     <li>Qualifying property can support an investor visa. {q('colombia-investor-visa-through-real-estate', 'Visa rules')}</li>
     <li>Buildings run under a clear legal regime, propiedad horizontal. {q('what-is-propiedad-horizontal-in-colombia', 'What it means for owners')}</li>
     <li>Bogotá runs on UTC-5 all year, the same clock as US Eastern time in winter.</li>
    </ul>
   </div>
   <div>
    <h3 style="font-size:1.5rem">And what to watch</h3>
    <ul class="checks">
     <li>The peso can fall against your home currency while you hold. {q('how-the-exchange-rate-changes-your-real-estate-return', 'Currency risk')}</li>
     <li>Taxes apply when you buy, while you own and when you sell. {q('taxes-foreigners-pay-on-property-in-colombia', 'Taxes for foreigners')}</li>
     <li>Money that arrives informally can be hard to take back out. Register it on the way in.</li>
     <li>Policy changes with each government. {q('how-to-evaluate-a-country-before-investing', 'How to read a country')}</li>
    </ul>
   </div>
  </div>
  <p class="note" style="margin-top:26px">{DISCLAIMER} Rules change; each linked page cites its primary sources.</p>
 </div>
</section>"""

# ---------- index ----------
index_body = f"""
{photo_hero('twilight', f'''
  <div class="hero-split">
   <div>
    <span class="kicker">Tierra Firme<span class="rule"></span>Any currency · Solid ground</span>
    <h1>Read the country <em>before</em> you buy into it.</h1>
    <p class="lede">A consortium of three practitioners in commercial real estate, business and family capital, and research. A private program in Colombia, a free show and sourced answers for people placing capital across borders.</p>
    <div class="btn-row" style="margin-top:26px"><a href="colombia-2027.html#invite" class="btn btn-gold">Get the information sheet</a><a href="colombia-2027.html" class="btn btn-ghost">Investor Lab 2027</a><a href="#trailer" class="btn btn-ghost">&#9654;&nbsp; Watch the film</a></div>
    <p class="hero-fine">{DISCLAIMER} No listings, no sales, no fees on what you buy.</p>
   </div>
   {itin_card()}
  </div>
''', video='/media/hero-loop')}

{ticker()}

<section class="trailer" id="trailer">
 <div class="container">
  <div class="section-head" style="margin-bottom:28px">
   <span class="eyebrow">The film · 3½ minutes</span>
   <h2>Solid ground.</h2>
  </div>
  <div class="player" id="player">
   <video id="tf-trailer" muted playsinline preload="metadata" poster="/media/film-poster.webp" width="1280" height="720" aria-label="Tierra Firme film: Solid Ground">
    <source src="/media/tierra-firme-film.mp4" type="video/mp4">
   </video>
   <button type="button" class="sound" id="tf-sound" aria-label="Turn sound on">&#128266;&nbsp; Sound on</button>
   <button type="button" class="replay" id="tf-replay" aria-label="Replay trailer" hidden>&#8635;&nbsp; Replay</button>
  </div>
  <div class="theater-dim" id="tf-dim" aria-hidden="true"></div>
  <button type="button" class="theater-exit" id="tf-exit">&#10005;&nbsp; Close</button>
  <p class="trailer-fine">3 minutes 38 seconds. Captioned. Why Latin America, why Colombia, why now, and what participants leave with. Footage from Bogotá, Medellín and the Colombian Andes. <a href="credits.html" style="color:inherit">Credits</a>.</p>
 </div>
</section>

<section class="ink">
 <div class="container">
  <div class="section-head" style="max-width:none;display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap">
   <div><span class="eyebrow">Investor Lab 2027 · Preliminary</span><h2 style="margin:0">Bogotá, then Medellín.</h2></div>
   <a href="colombia-2027.html#itinerary" class="btn btn-ghost">Preliminary itinerary &rarr;</a>
  </div>
  {cities_html()}
  <div class="stats" style="margin-top:22px"><div><b>6 days</b><span>5 nights</span></div><div><b>Private</b><span>Exclusive group</span></div><div><b><a href="https://www.sovereo.com/deal-record" rel="noopener" style="color:inherit;text-decoration:none">US$46.0B</a></b><span>Business deals tracked by Sovereo</span></div><div><b><a href="https://www.sovereo.com/deal-record/colombia" rel="noopener" style="color:inherit;text-decoration:none">US$3.84B</a></b><span>In Colombia alone</span></div></div>
  <p class="trailer-fine" style="margin-top:10px">US$46.0 billion in business deals tracked so far by Sovereo, including US$3.84 billion in Colombia. Source: Sovereo Desk, <a href="https://www.sovereo.com/deal-record" rel="noopener">The Global Deal Record</a>.</p>
 </div>
</section>

<section class="frames-sec" id="frames">
 <div class="container">
  <div class="section-head" style="max-width:none;display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap">
   <div><span class="eyebrow">Colombia in frames</span><h2 style="margin:0">Two cities, one journey.</h2></div>
   <p class="lede" style="margin:0;max-width:46ch">Bogotá, where the rules are made, and Medellín, where the valley meets the mountains. Explore the places on the route.</p>
  </div>
  {frames_html()}
 </div>
</section>

<section>
 <div class="container">
  <div class="section-head" style="max-width:none;display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap">
   <div><span class="eyebrow">Three members · Three lanes</span><h2 style="margin:0">Practitioners, not promoters.</h2></div>
   <a href="members.html" class="btn btn-ink">Meet the members</a>
  </div>
  {seat_cards()}
 </div>
</section>

{why_html(alt=True)}


<section>
 <div class="container">
  <div class="section-head" style="max-width:none;display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap">
   <div><span class="eyebrow">Questions investors ask</span><h2 style="margin:0">Sourced answers before you commit.</h2></div>
   <a href="questions.html" class="btn btn-ink">All questions</a>
  </div>
  <div class="qlist">QCARDS</div>
 </div>
</section>

{quote_band('twilight', 'Know the ground <em>before</em> you stand on it.', 'Bogotá and Medellín · March 2027 · Preliminary', '<a href="colombia-2027.html" class="btn btn-gold reveal" style="margin-top:22px">See the Investor Lab</a>')}

<section class="alt">
 <div class="container">
  <div class="section-head"><span class="eyebrow">Straight answers</span><h2>Questions people ask first.</h2></div>
  <div class="faq cols">{''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in FAQ)}</div>
 </div>
</section>

<section class="band-green">
 <div class="container signup-band">
  <div>
   <span class="eyebrow">Investor Lab 2027 · Episodes · Research</span>
   <h2>Know the ground before you stand on it.</h2>
   <p class="lede">Get the Investor Lab information sheet and the free Tierra Firme Newsletter. Subscribers hear about seats, new episodes and research first.</p>
  </div>
  <div>{signup_block(btn='Send me the information sheet', source='home')}</div>
 </div>
</section>
"""

# ---------- members ----------
def _mphoto(m, size=640):
    if not m.get('photo'):
        return portrait(m, 280)
    if size == 640:  # tall profile portrait from the uncropped original
        return f'<img src="{m["photo"]}-portrait.webp" alt="{html.escape(m["name"])}" width="512" height="640" loading="lazy" decoding="async">'
    return f'<img src="{m["photo"]}-{size}.webp" alt="{html.escape(m["name"])}" width="{size}" height="{size}" loading="lazy" decoding="async">'

member_rows = ''.join(f"""
  <article class="mprofile{' rev' if k % 2 else ''}" id="{m['key']}">
   <div class="mp-photo">{_mphoto(m)}</div>
   <div>
    <span class="tag tag-{m['key']}">{m['seat']} · {m['area']}</span>
    <h2>{m['name']}</h2>
    <p class="role">{m['role']}</p>
    <p>{m['bio']}</p>
    <p class="note"><strong>His lane:</strong> {m['show']}</p>
    <a class="lane-link" href="/lanes/{LANE[m['lane']]['slug']}">The {m['area'].lower()} lane &rarr;</a>
   </div>
  </article>""" for k, m in enumerate(MEMBERS))

members_body = f"""
<section class="hero-light">
 <div class="container split">
  <div>
   <span class="eyebrow">The members</span>
   <h1>Three practitioners. Equal seats.</h1>
   <p class="lede">Commercial real estate, business and family capital, and research. Each member runs an independent practice and teaches his own lane, and each view checks the other two.</p>
  </div>
  <div class="panel">{''.join(f'<a href="#{m["key"]}" title="{html.escape(m["name"])}">{_mphoto(m, 320)}</a>' for m in MEMBERS)}</div>
 </div>
</section>
<section class="profiles">
 <div class="container">{member_rows}
 </div>
</section>
<section>
 <div class="container grid-2">
  <div>
   <span class="eyebrow">Why three</span>
   <h2>Experience, access, research.</h2>
   <p>Valuation, operating experience and country research, from three people who work on the ground. Any one view alone misses something the other two catch.</p>
  </div>
  <div>
   <span class="eyebrow">The name</span>
   <h2>Why "Tierra Firme"</h2>
   <p>Tierra firme means solid ground. It was also the historic Spanish name for the South American mainland, a fit for a consortium built between North America and Latin America.</p>
  </div>
 </div>
</section>
<section class="alt">
 <div class="container signup-band">
  <div>
   <span class="eyebrow">Investor Lab 2027 · Preliminary</span>
   <h2>Meet them in Bogotá and Medellín.</h2>
   <p class="lede">Get the information sheet and the free Tierra Firme Newsletter. Subscribers hear about seats and new episodes first.</p>
  </div>
  <div>{signup_block(btn='Send me the information sheet', source='members')}</div>
 </div>
</section>
<section style="padding-top:0">
 <div class="container">
  <p class="note">Members' individual business activities are independent of one another and of Tierra Firme. Tierra Firme does not list property, arrange transactions or take fees on what anyone buys.</p>
  <div class="pagefoot"><a href="/" class="btn btn-ink">&larr; Back to home</a><a href="/colombia-2027" class="btn btn-gold">Investor Lab 2027 &rarr;</a></div>
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
   <article class="card bar-cre">{who('cre', '<span class="tag tag-cre">On location · Murphy · The Asset</span>')}<h3>Ground Truth</h3><p>A real, affordable property abroad on camera, and what the same income would and would not buy at home.</p></article>
   <article class="card bar-capital">{who('capital', '<span class="tag tag-capital">Guest format · Shawn · The Capital</span>')}<h3>Founder's Seat</h3><p>Someone who built a business or first balance sheet abroad: what worked, what it cost and what they would redo.</p></article>
   <article class="card bar-research">{who('research', '<span class="tag tag-research">Every episode · Todd · The Country</span>')}<h3>The Research Close</h3><p>A short close on currency, political and structural conditions and where they are heading.</p></article>
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

newsletter_body = f"""
<section class="hero-light">
 <div class="container signup-band">
  <div>
   <span class="eyebrow">Free · The Tierra Firme Newsletter</span>
   <h1>The Tierra Firme Newsletter.</h1>
   <p class="lede">Short, sourced briefings on Colombia and Latin America from three practitioners, and every Investor Lab 2027 update before anyone else. Free.</p>
   <p class="hero-fine" style="color:var(--muted)">No spam. Unsubscribe in one click. We never sell or share your address.</p>
  </div>
  <div class="card" style="background:#fff;border-top:3px solid var(--gold);box-shadow:0 24px 60px rgba(6,19,39,.08)">
   <h3>Subscribe free</h3>
   {signup_block(btn='Subscribe free', source='newsletter')}
  </div>
 </div>
</section>
<section>
 <div class="container">
  <div class="section-head"><span class="eyebrow">In each issue</span><h2>Three lanes, one read.</h2><p class="lede">Pick the lanes you care about when you subscribe. Every issue is educational and sourced.</p></div>
  <div class="grid-3">
   <article class="card bar-cre">{who('cre', '<span class="tag tag-cre">The Asset · Murphy</span>')}<h3>Property</h3><p>How property is valued, titled and managed in Colombia, and what a buyer from abroad should check before committing.</p></article>
   <article class="card bar-capital">{who('capital', '<span class="tag tag-capital">The Capital · Shawn</span>')}<h3>Business and family capital</h3><p>What it takes to build, run and hold a business across borders, and how families structure what they build.</p></article>
   <article class="card bar-research">{who('research', '<span class="tag tag-research">The Country · Todd</span>')}<h3>Research</h3><p>The currency, policy and deal flow behind the decision, drawing on Sovereo's Global Deal Record.</p></article>
  </div>
 </div>
</section>
<section>
 <div class="container split">
  <div>
   <span class="eyebrow">Sample issue</span>
   <h2>Read Issue No. 1.</h2>
   <p class="lede">Two cities, three lanes: the Investor Lab 2027 plan, US$3.84 billion in Colombian deals so far this year, and a short briefing from each member.</p>
   <div class="btn-row" style="margin-top:20px"><a href="/newsletter/issue-1" class="btn btn-ink">Read the full issue &rarr;</a></div>
  </div>
  <a href="/newsletter/issue-1" class="photo lift" style="display:block;max-height:560px;overflow:hidden;border:1px solid var(--border);border-top:3px solid var(--gold)"><img src="/img/newsletter-issue-1.webp" alt="Preview of Tierra Firme Newsletter Issue No. 1" width="720" height="1300" loading="lazy" decoding="async" style="height:auto"></a>
 </div>
</section>
<section class="alt">
 <div class="container grid-2">
  <div>
   <span class="eyebrow">Also in your inbox</span>
   <ul class="checks">
    <li>Investor Lab 2027 (Bogotá and Medellín): dates, the final itinerary, seats and pricing, first</li>
    <li>New sourced answers on ownership, tax, visas and getting money home</li>
    <li>New episodes and films</li>
   </ul>
  </div>
  <div>
   <span class="eyebrow">What it is not</span>
   <ul class="checks">
    <li>No listings and no offers to buy anything</li>
    <li>No investment, tax or legal advice</li>
    <li>No sharing of your address, ever</li>
   </ul>
  </div>
 </div>
</section>
<section style="padding-top:28px">
 <div class="container"><div class="pagefoot"><a href="/" class="btn btn-ink">&larr; Back to home</a><a href="/colombia-2027" class="btn btn-gold">Investor Lab 2027 &rarr;</a></div></div>
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
# PRELIMINARY. Six days, five nights: 3 days in Bogotá, 2 in Medellín.
# Arrive Bogotá Sunday; Monday, Tuesday and Wednesday morning in Bogotá; fly to Medellín Wednesday afternoon
# (the move may instead be Tuesday); Medellín from Wednesday evening;
# Thursday and Friday in Medellín; depart Friday afternoon or Saturday morning depending on flights.
# Format: short boardroom briefings, verified field visits, cultural evenings.
# Each day: (city, lane id or None, title, weekday, date, [(label, text)]).
PROGRAM = [
    ('Bogotá', None, 'Arrival', 'Sunday', '7 March', [
        ('Day', 'Arrive in Bogotá and settle in at the hotel.'),
        ('Culture', 'Welcome reception.'),
    ]),
    ('Bogotá', 'research', 'The country', 'Monday', '8 March', [
        ('Boardroom', 'Colombia in context: the economy, the political calendar, where policy is heading, and the peso.'),
        ('Field study', 'Bogotá\'s financial and institutional districts.'),
        ('Culture', 'An evening in Bogotá.'),
    ]),
    ('Bogotá', 'cre', 'Property', 'Tuesday', '9 March', [
        ('Boardroom', 'How property is valued, titled and managed in Colombia: propiedad horizontal and tax.'),
        ('Field study', 'Two contrasting Bogotá districts: infrastructure, services and the signals a listing never shows.'),
        ('Culture', 'An evening in Bogotá.'),
    ]),
    ('Bogotá', 'capital', 'Business', 'Wednesday', '10 March · morning', [
        ('Boardroom', 'Building and holding a business: entities, registering foreign investment and getting money home.'),
        ('Field study', 'A Bogotá operator on site, then a short afternoon flight to Medellín. The move may be Tuesday instead.'),
    ]),
    ('Medellín', None, 'Arrival in Medellín', 'Wednesday', '10 March · evening', [
        ('Culture', 'Check in, then an evening in Medellín.'),
    ]),
    ('Medellín', None, 'Commerce on the ground', 'Thursday', '11 March', [
        ('Boardroom', 'Medellín in context: commerce, investment and the city\'s growth.'),
        ('Field study', 'Verified visits to districts, operators and sites across the city.'),
        ('Culture', 'An evening in Medellín.'),
    ]),
    ('Medellín', None, 'The decision', 'Friday', '12 March', [
        ('Boardroom', 'The decision framework: run your own question through it.'),
        ('Field study', 'A final site visit, then departures in the afternoon, or fly out Saturday 13 March.'),
    ]),
]

def _dcard(lane, title, dow, date, slots):
    cls = ''  # days are by topic; speakers are announced separately
    by = '<p class="by">Travel day</p>' if title.startswith('Arrival') else '<p class="by">Boardroom · Field study · Culture</p>'
    dl = ''.join(f'<dt>{t}</dt><dd>{html.escape(d)}</dd>' for t, d in slots)
    return f'<article class="dcard{cls}"><span class="dd">{dow} · {date}</span><h4>{title}</h4>{by}<dl>{dl}</dl></article>'

def program_html():
    cols = []
    for city, label in (('Bogotá', 'Sun 7 to Wed 10 morning'), ('Medellín', 'Wed 10 evening to Fri 12')):
        cards = ''.join(_dcard(*d[1:]) for d in PROGRAM if d[0] == city)
        cols.append(f'<div class="itin-col"><h3 class="city-h">{city}<span>{label}</span></h3><div class="days">{cards}</div></div>')
    return (f'<div class="prelim"><b>Preliminary.</b><span>{PRELIM[13:]} Newsletter subscribers get every update first.</span></div>'
            f'<div class="itin">{"".join(cols)}</div>')

def faculty_html():
    return '<div class="faculty">' + ''.join(f"""<a class="card bar-{m['key']}" href="lanes/{LANE[m['lane']]['slug']}.html">
    {portrait(m, 104)}<span class="tag tag-{m['key']}">{m['seat']} · {m['area']}</span><h3>{m['name']}</h3><p>{m['show']}</p></a>""" for m in MEMBERS) + '</div>'

CITY_GUIDE = [
    dict(name='Bogotá', photo='towers', days='3 days · Sun 7 to Wed 10 March',
         intro='The capital, high on the Andean plateau, where the rules every foreign investor deals with are made.',
         blocks=[
            ('History', 'Founded on 6 August 1538 as Santa Fe de Bogotá, on land of the Muisca people. Capital of the Viceroyalty of New Granada and, since independence, of Colombia. The colonial center, La Candelaria, still sits beside Plaza de Bolívar and the seats of government.'),
            ('Culture', 'A city of museums, universities and Sunday rituals. The Museo del Oro holds one of the great collections of pre-Hispanic goldwork, and every Sunday and holiday the Ciclovía closes major avenues to cars for cyclists and walkers.'),
            ('Business climate', 'Home to the national government, the central bank (Banco de la República), the tax authority and the Colombian stock exchange. Institutional capital is active here: Bancolombia bought five leased buildings at Parque Logístico Calle 80 near Bogotá in 2026, about US$152 million.'),
            ('Places worth seeing', 'Monserrate above the city; La Candelaria and Plaza de Bolívar; the Museo del Oro; Usaquén and its Sunday market; the Parque 93 and Zona T districts in the north.'),
         ],
         sources=[('Museo del Oro, Banco de la República', 'https://www.banrepcultural.org/bogota/museo-del-oro'),
                  ('Ciclovía Bogotana, IDRD', 'https://www.idrd.gov.co/ciclovia-bogotana'),
                  ('Banco de la República', 'https://www.banrep.gov.co'),
                  ('Global Deal Record, Colombia', 'https://www.sovereo.com/deal-record/colombia')]),
    dict(name='Medellín', photo='medellin', days='2 days · Wed 10 evening to Fri 12 March',
         intro="Colombia's second city, in the Aburrá Valley, known as the City of the Eternal Spring for its mild climate year round.",
         blocks=[
            ('History', 'Founded in 1675 in the Aburrá Valley and capital of the department of Antioquia. Long the industrial heart of the country, it rebuilt itself in recent decades around transit, public space and education.'),
            ('Culture', 'Paisa hospitality, the August Feria de las Flores, and the sculptures of Fernando Botero, a son of the city, in Plaza Botero beside the Museo de Antioquia. Hillside neighborhoods such as Comuna 13 tell the story of the city\'s transformation through street art.'),
            ('Business climate', 'Headquarters city for Bancolombia and other major Antioquian companies, with the Ruta N innovation district. In 2013 the Urban Land Institute named Medellín the most innovative city in the world. In 2026 Bancolombia bought Rivana Business Park Torre Sur here, about US$65.6 million.'),
            ('Places worth seeing', 'Plaza Botero and the Museo de Antioquia; Comuna 13; Parque Arví by Metrocable; El Poblado and Provenza; the Metro, opened in 1995, which still anchors the city\'s transit.'),
         ],
         sources=[('Museo de Antioquia', 'https://www.museodeantioquia.co'),
                  ('Metro de Medellín', 'https://www.metrodemedellin.gov.co'),
                  ('Ruta N', 'https://www.rutanmedellin.org'),
                  ('Parque Arví', 'https://parquearvi.org'),
                  ('Global Deal Record, Colombia', 'https://www.sovereo.com/deal-record/colombia')]),
]

def city_guide_html():
    out = []
    for k, c in enumerate(CITY_GUIDE):
        blocks = ''.join(f'<div class="cg-block"><span class="k">{t}</span><p>{html.escape(d)}</p></div>' for t, d in c['blocks'])
        src = ' · '.join(f'<a href="{u}" rel="noopener">{html.escape(n)}</a>' for n, u in c['sources'])
        out.append(f"""<article class="cguide{' rev' if k % 2 else ''}" id="city-{c['name'].lower().replace('á','a').replace('í','i')}">
   <div class="cg-photo">{img(c['photo'], '(max-width:900px) 100vw, 40vw')}<span class="cg-days">{c['days']}</span></div>
   <div class="cg-body">
    <h3>{c['name']}</h3>
    <p class="lede">{html.escape(c['intro'])}</p>
    <div class="cg-grid">{blocks}</div>
    <p class="cg-src">Sources: {src}. {credit(c['photo'])}.</p>
   </div>
  </article>""")
    return ''.join(out)

EVENT_FAQ = [
    ("When and where is the Investor Lab?",
     "Six days and five nights in Colombia: arrive in Bogotá on Sunday 7 March 2027, Bogotá through Wednesday morning, then Medellín from Wednesday evening (the move may be Tuesday instead), departing Friday 12 March in the afternoon or Saturday 13 March in the morning, depending on flights. Hotels are confirmed to registered attendees."),
    ("Is the program final?",
     "No. Everything is preliminary while we put the program together. Dates, cities, sessions and visits may change, and newsletter subscribers hear first."),
    ("Who is it for?",
     "People who earn in dollars, euros or another currency and are weighing property or a business in Colombia, and families thinking about how to hold what they build across borders."),
    ("How large is the group?",
     "Small and exclusive, by design, so every question gets answered."),
    ("Will anyone sell me property or a business?",
     "No. There are no listings, no brokers in the room and no referral fees. Site visits show places, not units for sale. It is education, not advice."),
    ("How do I get the information sheet?",
     "Leave your email on this page. You will receive the information sheet and the free Tierra Firme Newsletter, and subscribers get the final schedule, seat details and pricing before anyone else."),
]

event_body = f"""
{photo_hero('downtown', f'''
  <div class="hero-split">
   <div>
    <span class="kicker">Investor Lab 2027<span class="rule"></span>Bogotá · Medellín · Preliminary</span>
    <h1>Two cities. Six days. <em>Solid ground.</em></h1>
    <p class="lede">A private program in Colombia for an exclusive group of investors placing capital across borders: three days in Bogotá, two in Medellín. Short boardroom briefings, verified field visits and cultural evenings, hosted by Tierra Firme with guest speakers.</p>
    <div class="btn-row" style="margin-top:26px"><a href="#invite" class="btn btn-gold">Get the information sheet</a><a href="#itinerary" class="btn btn-ghost">Preliminary itinerary</a></div>
   </div>
   {itin_card('#invite')}
  </div>
''', video='/media/event-loop')}

{ticker()}

<nav class="subnav" aria-label="On this page"><div class="container">
 <a href="#itinerary">Itinerary</a><a href="#cities">Cities</a><a href="#format">Format</a><a href="#faculty">Hosts</a><a href="#why">Why Colombia</a><a href="#details">Details</a><a href="#faq">FAQ</a><a href="#invite" class="cta">Information sheet</a>
</div></nav>

<section id="itinerary">
 <div class="container">
  <div class="section-head" style="max-width:none;display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap">
   <div><span class="eyebrow">Preliminary itinerary</span><h2 style="margin:0">Bogotá, then Medellín.</h2></div>
   <p style="margin:0;max-width:52ch">Arrive Sunday in Bogotá. Every day from Monday to Friday follows the same rhythm: a short boardroom briefing, a field study and an evening of culture.</p>
  </div>
  {program_html()}
 </div>
</section>

<section class="ink" id="cities">
 <div class="container">
  <div class="section-head"><span class="eyebrow">Two cities</span><h2>The capital and the second city.</h2><p class="lede">History, culture, business climate and the places worth seeing in each.</p></div>
  {cities_html()}
  {city_guide_html()}
 </div>
</section>

<section class="ink" id="format" style="padding-top:0">
 <div class="container">
  <div class="format">
   <div><span class="k">Mornings</span><h3>Boardroom briefings</h3><p>Short, focused sessions: the country, property, business and the decision.</p></div>
   <div><span class="k">Afternoons</span><h3>Verified field visits</h3><p>Districts, operators and sites we have checked, in both cities. Places, not units for sale.</p></div>
   <div><span class="k">Evenings</span><h3>Cultural evenings</h3><p>Colombia beyond the boardroom, with the members and the group.</p></div>
  </div>
 </div>
</section>

<section class="alt">
 <div class="container">
  <div class="section-head"><span class="eyebrow">The setting</span><h2>Quiet rooms, small groups.</h2><p class="lede">Upscale hotels in both cities, a high-floor boardroom and time out in the city. Venues and hotels are confirmed to registered attendees; the photographs show Bogotá, not the venue.</p></div>
  <div class="gallery">
   {fig('agora', 'wide', '(max-width:760px) 100vw, 66vw')}
   <div class="col">{fig('colon', 'wide', '(max-width:760px) 100vw, 33vw')}{fig('tequendama', 'wide', '(max-width:760px) 100vw, 33vw')}</div>
  </div>
 </div>
</section>

<section class="ink" id="faculty">
 <div class="container">
  <div class="section-head"><span class="eyebrow">Hosts</span><h2>Hosted by Tierra Firme.</h2><p class="lede">Guest speakers, including Colombian counsel on property, tax and foreign investment, will be announced to newsletter subscribers.</p></div>
  {faculty_html()}
 </div>
</section>

{why_html(alt=False)}

<section class="alt" id="details">
 <div class="container grid-2" style="align-items:start">
  <div>
   <span class="eyebrow">The details</span>
   <h2>Colombia, March 2027.</h2>
   <dl class="facts">
    <div><dt>Dates</dt><dd>Arrive Sunday 7 March in Bogotá. Depart Friday 12 March afternoon or Saturday 13 March morning from Medellín</dd></div>
    <div><dt>Cities</dt><dd>Bogotá, Sunday to Wednesday morning. Medellín, Wednesday evening to Friday. The move may be Tuesday instead</dd></div>
    <div><dt>Group</dt><dd>Exclusive and kept small, so every question gets answered</dd></div>
    <div><dt>Hotels</dt><dd>Upscale hotels in both cities, confirmed to registered attendees</dd></div>
    <div><dt>Airports</dt><dd>Arrive El Dorado, Bogotá (BOG). Depart José María Córdova, Medellín (MDE)</dd></div>
    <div><dt>Seats and pricing</dt><dd>Sent to newsletter subscribers first</dd></div>
   </dl>
   <p class="note" style="margin-top:18px">{PRELIM}</p>
  </div>
  <div>
   <span class="eyebrow">What you leave with</span>
   <ul class="checks" style="margin-bottom:26px">
    <li>A decision framework, with your own question run through it</li>
    <li>A written Colombia country briefing on the conditions your decision will live in</li>
    <li>Every presentation from the week</li>
   </ul>
   <span class="eyebrow">What this is not</span>
   <ul class="checks">
    <li>No listings: field visits show places, not units for sale</li>
    <li>No brokers in the room and no sales pitches</li>
    <li>No referral fees: we earn nothing from what you buy or where</li>
    <li>Education, not advice: the decision stays yours</li>
   </ul>
  </div>
 </div>
</section>

<section id="faq">
 <div class="container">
  <div class="section-head"><span class="eyebrow">Questions</span><h2>Before you ask.</h2></div>
  <div class="faq cols">{''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in EVENT_FAQ)}</div>
 </div>
</section>

<section class="band-green" id="invite">
 <div class="container signup-band">
  <div>
   <span class="eyebrow">Exclusive group · Bogotá and Medellín · March 2027</span>
   <h2>Get the information sheet.</h2>
   <p class="lede">Leave your email to receive the information sheet and the free Tierra Firme Newsletter. Subscribers get the final itinerary, seat details and pricing first.</p>
   <p class="hero-fine" style="color:rgba(255,255,255,.6)">{DISCLAIMER}</p>
  </div>
  <div>{signup_block(btn='Send me the information sheet', ok="Thank you. You're on the Investor Lab 2027 list; the information sheet and every update come to you first.", source='colombia-2027')}</div>
 </div>
</section>
"""

event_schema = [
    {"@type": "EducationEvent", "@id": BASE + "/colombia-2027#event", "name": "Tierra Firme Investor Lab 2027, Bogotá and Medellín",
     "description": "A six-day educational program in Bogotá and Medellín on commercial real estate, business and family capital, and country research for people placing capital across borders.",
     "startDate": EVENT['start'], "endDate": EVENT['end'], "eventStatus": "https://schema.org/EventScheduled",
     "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
     "location": [{"@type": "Place", "name": "Bogotá (hotel confirmed to registered attendees)",
                   "address": {"@type": "PostalAddress", "addressLocality": "Bogotá", "addressCountry": "CO"}},
                  {"@type": "Place", "name": "Medellín (hotel confirmed to registered attendees)",
                   "address": {"@type": "PostalAddress", "addressLocality": "Medellín", "addressCountry": "CO"}}],
     "image": [BASE + PHOTOS['downtown']['base'] + '-1920.webp'],
     "organizer": {"@id": BASE + "/#org"}, "performer": [{"@type": "Person", "name": m['name']} for m in MEMBERS],
     "inLanguage": "en", "url": BASE + "/colombia-2027"},
    faq_schema(EVENT_FAQ),
]
event_schema[0]["eventStatus"] = "https://schema.org/EventScheduled"

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
    'capital': dict(photo='agora', h1='Build it, run it, hold it.',
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
    day = next(p[1:] for p in PROGRAM if p[1] == l['id'])
    qs = [x for x in QUESTIONS if x['lane'] == l['id']]
    qhtml = ('<div class="qlist">' + ''.join(f'<a class="qcard" href="/questions/{x["slug"]}"><h3>{html.escape(x["q"])}</h3><p>{html.escape(x["short"])}</p></a>' for x in qs) + '</div>') if qs \
        else '<p>Answer pages for this lane are being written. Subscribe to the newsletter to hear when they publish.</p>'
    covers = ''.join(f'<li>{html.escape(x)}</li>' for x in c['covers'])
    body = f"""
{photo_hero(c['photo'], f'''
  <span class="kicker">{l['seat']}<span class="rule"></span>{l['label']} · {l['first']}</span>
  <h1>{c['h1']}</h1>
  <p class="lede">{m['show']}</p>
  <div class="btn-row" style="margin-top:28px"><a href="#join" class="btn btn-gold">Follow this lane</a><a href="/colombia-2027#itinerary" class="btn btn-ghost">Investor Lab 2027</a></div>
''')}
<section>
 <div class="container grid-2" style="align-items:start">
  <div>
   <span class="eyebrow">In {l['first']}'s words</span>
   <p class="quote" style="color:var(--ink);font-size:clamp(1.3rem,2.2vw,1.7rem)">{html.escape(c['voice'])}</p>
   <div class="who" style="margin-top:18px">{avatar(m, 56)}<span class="role" style="margin:0">{m['name']}</span></div>
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
  <p class="lede">Subscribe to the free Tierra Firme Newsletter. Pick the lanes you want to hear about.</p>
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
FILM_CREDITS = [('Juan Castelblanco', 'Andes mountains, Colombia', 'https://www.pexels.com/video/drone-video-of-the-andes-mountains-in-colombia-15747549/'), ('Martina Tomšič', 'Globe', 'https://www.pexels.com/video/close-up-view-of-a-globe-4696463/'), ('Saif Abdulraheem', 'Counting money', 'https://www.pexels.com/video/person-counting-money-4275306/'), ('Alexandr Shorban', 'Clouds from an airplane window', 'https://www.pexels.com/video/clouds-seen-from-airplane-window-10691579/'), ('Juan David Palacio Mesa', 'Bogotá aerials and the Colombian flag', 'https://www.pexels.com/video/bogota-vista-aerea-19593286/'), ('Werner Pfennig', 'Conference room', 'https://www.pexels.com/video/man-speaking-in-conference-room-6951601/'), ('Yunus Terk', 'Modern apartments, aerial', 'https://www.pexels.com/video/stunning-aerial-view-of-modern-luxury-apartments-38235767/'), ('Ron Lach', 'Business owner in a café', 'https://www.pexels.com/video/close-up-video-of-a-woman-holding-a-clipboard-8441634/'), ('Jakub Zerdzicki', 'Financial analyst', 'https://www.pexels.com/video/financial-analyst-calculating-market-trends-38597877/'), ('Camilo Carrò', 'Airplane wing in flight', 'https://www.pexels.com/video/airplane-wing-while-flying-in-the-sky-6472910/'), ('Thirdman', 'Signing a document', 'https://www.pexels.com/video/close-up-video-of-a-person-signing-a-document-8471105/'), ('Julián Armando Santos', 'Plaza de Bolívar and Bogotá walkways', 'https://www.pexels.com/video/historic-plaza-bolivar-in-bogota-colombia-37151628/'), ('Polina Kovaleva', 'Notebook', 'https://www.pexels.com/video/closeup-video-of-writings-on-a-notebook-5546876/'), ('Juan Camilo Trujillo Botero', 'Bogotá at twilight and city aerials', 'https://www.pexels.com/video/aerial-view-of-bogota-at-twilight-40369496/'), ('ME UP', 'Medellín skyline at dusk', 'https://www.pexels.com/video/aerial-view-of-medellin-skyline-at-dusk-40130401/'), ('Vlada Karpovich', 'Business meeting', 'https://www.pexels.com/video/people-having-business-meeting-7552419/'), ('Federico Molina', 'Medellín with mountains', 'https://www.pexels.com/video/aerial-view-of-urban-landscape-with-mountains-40437627/'), ('E CG', 'Salsa, Cali', 'https://www.pexels.com/video/salsa-colorful-shoes-19851286/'), ('Naresh Babu', 'Evening glassware', 'https://www.pexels.com/video/elegant-nighttime-glassware-with-ambient-lighting-37482114/'), ('Mikhail Nilov', 'Professionals reviewing documents', 'https://www.pexels.com/video/professionals-looking-carefully-on-documents-8847933/'), ('Alex Moliski', 'City and mountains at sunset', 'https://www.pexels.com/video/an-aerial-view-of-a-city-and-mountains-at-sunset-26775139/'), ('Julián Armando Santos', 'Sunday ciclovía, Bogotá', 'https://www.pexels.com/video/ciudad-de-bogota-ciclovia-dominical-27097445/'), ('Julián Armando Santos', 'Ciclovía cyclists, Bogotá', 'https://www.pexels.com/video/ciclovias-deporte-bogota-27174461/'), ('Alejo Turola', 'Bogotá towers, drone', 'https://www.pexels.com/video/drone-footage-of-bogota-city-in-colombia-11252085/'), ('luis sebastian zapata ochoa', 'Medellín skyline, aerial', 'https://www.pexels.com/video/aerial-view-of-medellin-s-modern-skyline-31646890/'), ('Jorge Pantaleon', 'Shopping center', 'https://www.pexels.com/video/vibrant-indoor-shopping-mall-scene-captured-35308049/')]
film_rows = ''.join(f'<li><strong>{html.escape(w)}</strong>. {html.escape(a)}, <a href="{u}" rel="noopener">Pexels</a>.</li>' for a, w, u in FILM_CREDITS)
credits_body = f"""
<section class="hero">
 <div class="container">
  <span class="eyebrow">Credits</span>
  <h1>Photo credits.</h1>
  <p class="lede">Photographs of Bogotá are used under the licenses below.</p>
 </div>
</section>
<section>
 <div class="container">
  <ul class="checks">{credit_rows}</ul>
  <p class="note" style="margin-top:28px">Adapted versions of CC BY-SA photographs are shared under the same license. Trailer footage credits are listed with the trailer wherever it is posted.</p>
  <h2 style="margin-top:40px">The film: Solid Ground</h2>
  <p>Narration and music produced with vidIQ. Stock footage from Pexels:</p>
  <ul class="checks">{film_rows}</ul>
 </div>
</section>
"""

PAGES = [
    ('index.html', 'Tierra Firme | Real Estate, Business and Research for Capital Abroad',
     'Tierra Firme is a consortium in commercial real estate, business and intelligence research. A free show, research and seminars for people placing capital across borders, starting with Latin America.',
     index_body, [faq_schema(FAQ), {"@id": BASE + "/colombia-2027#event", "@type": "EducationEvent", "name": "Tierra Firme Investor Lab 2027, Bogotá and Medellín", "startDate": EVENT['start'], "endDate": EVENT['end'], "url": BASE + "/colombia-2027", "location": {"@type": "Place", "name": "Bogotá", "address": {"@type": "PostalAddress", "addressLocality": "Bogotá", "addressCountry": "CO"}}}, {"@type": "VideoObject", "name": "Tierra Firme: Solid Ground",
        "description": "Solid Ground: a short film on Tierra Firme, why Latin America and Colombia, why now, and what participants in the preliminary Investor Lab 2027 in Bogotá and Medellín leave with.",
        "thumbnailUrl": BASE + "/media/film-poster.webp", "contentUrl": BASE + "/media/tierra-firme-film.mp4",
        "uploadDate": "2026-11-21", "duration": "PT3M38S", "inLanguage": "en", "publisher": {"@id": BASE + "/#org"}}], None, 'twilight'),
    ('colombia-2027.html', 'Investor Lab 2027: Bogotá and Medellín | Tierra Firme',
     'Tierra Firme Investor Lab 2027 (preliminary): three days in Bogotá and two in Medellín, 7 to 12 March 2027, for an exclusive group of investors. Commercial real estate, business and family capital, and country research. Education, not advice.',
     event_body, event_schema, [('', 'Home'), ('colombia-2027.html', 'Colombia 2027')], 'downtown'),
    ('credits.html', 'Photo Credits | Tierra Firme', 'Credits and licenses for the photographs used on the Tierra Firme site.',
     credits_body, [], [('', 'Home'), ('credits.html', 'Photo credits')], None),
    ('members.html', 'Members | Tierra Firme',
     'Meet the Tierra Firme members: Murphy D. Cheatham II (commercial real estate, CBRE), Shawn Christopher Leamon (business and family capital, LaGrande Global) and Todd Allyn (research).',
     members_body, [dict(m['person'], **{"memberOf": {"@id": BASE + "/#org"}}) for m in MEMBERS],
     [('', 'Home'), ('members.html', 'Members')], None),
    ('the-show.html', 'The Show | Tierra Firme Season One',
     'Tierra Firme Season One: twelve free episodes on placing capital abroad, from the currency math to a full case study. In English and Spanish.',
     show_body, [show_schema], [('', 'Home'), ('the-show.html', 'The Show')], None),
    ('newsletter.html', 'The Tierra Firme Newsletter | Free',
     'The free Tierra Firme Newsletter: sourced briefings on Colombia and Latin America across property, business and family capital, and research, plus Investor Lab 2027 updates first.',
     newsletter_body, [], [('', 'Home'), ('newsletter.html', 'Newsletter')], None),
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
  <p class="qa-meta"><a class="tag tag-{LANE[x['lane']]['key']}" style="text-decoration:none" href="/lanes/{LANE[x['lane']]['slug']}">{LANE[x['lane']]['seat']} · {LANE[x['lane']]['label']}</a><br>{avatar(MEMBER_BY_LANE['research'], 34)}By Todd Allyn, research lead, Tierra Firme · Updated <time datetime="{UPDATED}">{UPDATED_TEXT}</time></p>
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
  <p class="lede">Subscribe to the free newsletter and reply to any issue. New answers go to subscribers first.</p>
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
for p, pr in ([('', '1.0'), ('colombia-2027', '1.0'), ('members', '0.9'), ('the-show', '0.9'), ('questions', '0.9')]
              + [('lanes/' + l['slug'], '0.8') for l in LANES if l['approved']]
              + [('questions/' + x['slug'], '0.8') for x in QUESTIONS] + [('newsletter', '0.8'), ('newsletter/issue-1', '0.6'), ('credits', '0.3')]):
    sm += f'  <url><loc>{BASE}/{p}</loc><lastmod>2026-11-20</lastmod><priority>{pr}</priority></url>\n'
sm += '</urlset>\n'
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)

llms = f"""# Tierra Firme

> A consortium of three practitioners in commercial real estate, business and family capital, and research. Tierra Firme produces a free show, sourced answers and seminars for people placing capital across borders, starting with Latin America. Based in Dallas and Bogotá; works globally. Educational only: no listings, no transactions, no investment advice.

## Members and lanes
- Murphy D. Cheatham II, The Asset (commercial real estate): Private Clients Director at CBRE, a global role advising private families and high net worth individuals.
- Shawn Christopher Leamon, The Capital (business and family capital): founder and managing partner of LaGrande Global (since 2013), an investment firm managing close to $100 million with a focus on Latin America, and founder and CEO of Cielo.Travel, Bogotá.
- Todd Allyn, The Country (research): leads Tierra Firme research. Founding Director of Sovereo Intelligence Research (https://www.sovereo.com), whose Global Deal Record (https://www.sovereo.com/deal-record) has tracked US$46.0 billion in business deals so far, including US$3.84 billion in Colombia (Sovereo Desk, The Global Deal Record). Professor of economics and decision science for over 24 years. Bogotá.

## Event
- [Tierra Firme Investor Lab 2027]({BASE}/colombia-2027): preliminary. 6 days, 5 nights, 7 to 12 March 2027: 3 days in Bogotá, 2 in Medellín. Exclusive group. Short boardroom briefings, verified field visits, cultural evenings. Education, not advice.

## Pages
- [Home]({BASE}/): what Tierra Firme is, the three lanes, the framework and FAQ.
- [Members]({BASE}/members): full bios of the three members.
- [The Show]({BASE}/the-show): Season One, twelve biweekly episodes in English and Spanish.
- [Newsletter]({BASE}/newsletter): the free Tierra Firme Newsletter. Investor Lab updates, sourced briefings by lane. The only signup on the site.

## Questions investors ask (sourced answers)
""" + ''.join(f"- [{x['q']}]({BASE}/questions/{x['slug']}): {x['short']}\n" for x in QUESTIONS) + f"""
## Notes
- Tierra Firme does not list property, arrange transactions or take fees on what anyone buys.
- Nothing published by Tierra Firme is investment, tax or legal advice.
"""
open(os.path.join(OUT, 'llms.txt'), 'w').write(llms)

redirects = """/the-seats.html /members 301
/the-seats /members 301
/get-the-read.html /newsletter 301
/get-the-read /newsletter 301
/join.html /newsletter 301
/join /newsletter 301
/membership /newsletter 301
/membership.html /newsletter 301
/investor-lab /colombia-2027 301
/bogota-2027 /colombia-2027 301
/bogota-2027.html /colombia-2027 301
/tierra-firme.html / 301
/tierra-firme-episodes.html /the-show 301
/tierra-firme-hosts.html /members 301
/tierra-firme-subscribe.html /newsletter 301
"""
open(os.path.join(OUT, '_redirects'), 'w').write(redirects)

favicon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#061327" stroke="#e9a825" stroke-width="3"/><text x="32" y="40" text-anchor="middle" font-family="Georgia,serif" font-size="22" font-weight="700" fill="#e9a825">TF</text></svg>"""
open(os.path.join(OUT, 'favicon.svg'), 'w').write(favicon)
print('built', sorted(os.listdir(OUT)))
