#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CN2Global Complete Static Website Generator"""

def gen_index():
    css = """*{margin:0;padding:0;box-sizing:border-box}
:root{--blue:#0066FF;--cyan:#00D4FF;--orange:#FF6B35;--dark:#1a1a2e;--g50:#fafafa;--g100:#f5f5f5;--g200:#e8e8e8;--g300:#d0d0d0;--g400:#999;--g500:#666;--white:#fff;--r:12px;--r2:16px;--shadow:0 4px 20px rgba(0,0,0,.08);--shadow2:0 8px 40px rgba(0,0,0,.14);--t:all .3s ease;--font:'Inter','Noto Sans SC',sans-serif}
html{scroll-behavior:smooth}
body{font-family:var(--font);color:var(--dark);background:var(--white);line-height:1.6;font-size:16px;overflow-x:hidden}
a{text-decoration:none;color:inherit}
button,input,select{font-family:var(--font)}
img{max-width:100%;display:block}
.container{max-width:1200px;margin:0 auto;padding:0 24px}
.text-center{text-align:center}
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:var(--g100)}
::-webkit-scrollbar-thumb{background:var(--blue);border-radius:3px}
[lang-zh],[lang-en],[lang-ko]{display:none}
html[data-lang="zh"] [lang-zh]{display:block}
html[data-lang="zh"] [lang-en]{display:none}
html[data-lang="zh"] [lang-ko]{display:none}
html[data-lang="en"] [lang-zh]{display:none}
html[data-lang="en"] [lang-en]{display:block}
html[data-lang="en"] [lang-ko]{display:none}
html[data-lang="ko"] [lang-zh],[html][data-lang="ko"] [lang-en]{display:none}
html[data-lang="ko"] [lang-ko]{display:block}
.navbar{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(255,255,255,.97);backdrop-filter:blur(12px);border-bottom:1px solid rgba(0,0,0,.05);transition:var(--t)}
.navbar.scrolled{box-shadow:var(--shadow);background:#fff}
.nav{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:70px}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px}
.logo-text{background:linear-gradient(135deg,var(--blue),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-size:22px}
.nav-links{display:flex;gap:32px;flex:1;margin-left:40px}
.nav-links a{font-size:14px;font-weight:500;color:var(--g500);transition:var(--t);position:relative}
.nav-links a:hover{color:var(--blue)}
.nav-links a::after{content:'';position:absolute;bottom:-4px;left:0;width:0;height:2px;background:var(--blue);transition:var(--t)}
.nav-links a:hover::after{width:100%}
.nav-actions{display:flex;gap:10px;align-items:center}
.btn-o{padding:8px 20px;font-size:14px;font-weight:600;color:var(--blue);border:2px solid var(--blue);border-radius:8px;transition:var(--t);background:transparent;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center}
.btn-o:hover{background:var(--blue);color:#fff}
.btn-p{padding:10px 24px;font-size:14px;font-weight:600;color:#fff;background:linear-gradient(135deg,var(--blue),var(--cyan));border-radius:8px;transition:var(--t);box-shadow:0 4px 12px rgba(0,102,255,.3);border:none;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:8px}
.btn-p:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,102,255,.4)}
.lang-wrap{position:relative}
.lang-btn{display:flex;align-items:center;gap:6px;padding:7px 14px;background:rgba(0,102,255,.08);border:1px solid rgba(0,102,255,.15);border-radius:8px;font-size:13px;font-weight:600;color:var(--blue);cursor:pointer;transition:var(--t)}
.lang-btn:hover{background:rgba(0,102,255,.15)}
.lang-drop{display:none;position:absolute;top:calc(100% + 8px);right:0;background:#fff;border-radius:var(--r);box-shadow:var(--shadow2);overflow:hidden;min-width:160px;z-index:100}
.lang-drop.show{display:block}
.lang-opt{display:flex;align-items:center;gap:10px;padding:12px 16px;font-size:14px;font-weight:500;cursor:pointer;transition:var(--t)}
.lang-opt:hover{background:var(--g100)}
.lang-opt.active{background:rgba(0,102,255,.08);color:var(--blue)}
.m-btn{display:none;flex-direction:column;gap:5px;width:28px;background:none;border:none;cursor:pointer;padding:0}
.m-btn span{width:100%;height:2px;background:var(--dark);border-radius:2px;transition:var(--t)}
.hero{margin-top:70px;position:relative;overflow:hidden;padding:100px 24px;display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;min-height:88vh}
.hero-bg{position:absolute;inset:0;z-index:0}
.hero-gradient{position:absolute;inset:0;background:radial-gradient(ellipse at 30% 50%,rgba(0,102,255,.07) 0%,transparent 60%),radial-gradient(ellipse at 70% 50%,rgba(0,212,255,.05) 0%,transparent 60%)}
.hero-particles{position:absolute;width:100%;height:100%}
.particle{position:absolute;width:3px;height:3px;background:var(--blue);border-radius:50%;opacity:.18;animation:pf 15s ease-in-out infinite}
@keyframes pf{0%,100%{transform:translate(0,0);opacity:.18}50%{transform:translate(40px,-25px);opacity:.45}}
.hero-content{position:relative;z-index:1}
.hero-badge{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;background:rgba(0,102,255,.08);border:1px solid rgba(0,102,255,.2);border-radius:24px;font-size:13px;font-weight:600;color:var(--blue);margin-bottom:24px;animation:fa .8s ease}
@keyframes fa{from{opacity:0;transform:translateY(-20px)}to{opacity:1;transform:translateY(0)}}
.hero-title{font-size:clamp(32px,5vw,56px);font-weight:800;line-height:1.15;margin-bottom:24px;animation:fa .8s ease .1s both}
.gt{background:linear-gradient(135deg,var(--blue),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-desc{font-size:17px;color:var(--g500);margin-bottom:32px;line-height:1.8;max-width:520px;animation:fa .8s ease .2s both}
.hero-actions{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:48px;animation:fa .8s ease .3s both}
.btn-h1{display:inline-flex;align-items:center;gap:10px;padding:16px 32px;background:linear-gradient(135deg,var(--blue),var(--cyan));color:#fff;border-radius:var(--r);font-weight:700;font-size:15px;transition:var(--t);box-shadow:0 4px 20px rgba(0,102,255,.35);border:none;cursor:pointer}
.btn-h1:hover{transform:translateY(-3px);box-shadow:0 8px 30px rgba(0,102,255,.45)}
.btn-h2{display:inline-flex;align-items:center;gap:10px;padding:16px 32px;background:var(--g50);color:var(--blue);border-radius:var(--r);font-weight:600;font-size:15px;transition:var(--t);border:1px solid rgba(0,102,255,.2);cursor:pointer}
.btn-h2:hover{background:rgba(0,102,255,.06);transform:translateY(-3px)}
.hero-stats{display:flex;gap:40px;animation:fa .8s ease .4s both}
.stat-item{display:flex;flex-direction:column;gap:6px}
.stat-num{font-size:32px;font-weight:800;background:linear-gradient(135deg,var(--blue),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.stat-label{font-size:13px;color:var(--g400);font-weight:500}
.stat-div{width:1px;background:var(--g200)}
.country-reg{margin-top:32px;animation:fa .8s ease .35s both}
.country-reg-label{display:block;font-size:14px;font-weight:600;color:var(--g500);margin-bottom:10px}
.country-wrap{position:relative;display:inline-block;width:100%;max-width:440px}
.country-select{width:100%;padding:14px 48px 14px 16px;border:2px solid rgba(0,102,255,.25);border-radius:var(--r);font-size:14px;font-weight:600;color:var(--dark);background:#fff;cursor:pointer;appearance:none;-webkit-appearance:none;transition:var(--t);box-shadow:0 2px 12px rgba(0,102,255,.06)}
.country-select:focus{outline:none;border-color:var(--blue);box-shadow:0 0 0 3px rgba(0,102,255,.1)}
.select-arrow{position:absolute;right:16px;top:50%;transform:translateY(-50%);pointer-events:none;color:var(--blue)}
.hero-visual{position:relative;z-index:1;display:flex;align-items:center;justify-content:center}
.globe-wrap{position:relative;width:420px;height:420px}
.globe-ring{position:absolute;border:1px solid rgba(0,102,255,.12);border-radius:50%;animation:gr 22s linear infinite}
.ring1{width:320px;height:320px;top:50px;left:50px;animation-duration:26s}
.ring2{width:220px;height:220px;top:100px;left:100px;animation-duration:18s;animation-direction:reverse}
.ring3{width:120px;height:120px;top:150px;left:150px;animation-duration:12s}
@keyframes gr{from{transform:rotate(0)}to{transform:rotate(360deg)}}
.globe-core{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:200px;height:200px;color:var(--blue)}
.globe-svg{width:100%;height:100%}
.pd{animation:pd 2s ease-in-out infinite}
.pr{animation:pr 2s ease-in-out infinite}
@keyframes pd{0%,100%{r:5;opacity:1}50%{r:7;opacity:.5}}
@keyframes pr{0%{r:8;opacity:1}100%{r:20;opacity:0}}
.fc{position:absolute;background:#fff;padding:14px 18px;border-radius:14px;box-shadow:var(--shadow);display:flex;align-items:center;gap:10px;font-size:13px;font-weight:600;color:var(--dark);white-space:nowrap;animation:cf 4s ease-in-out infinite}
@keyframes cf{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.fc1{top:30px;left:0;animation-delay:0s}
.fc2{top:50%;right:0;transform:translateY(-50%);animation-delay:1.5s}
.fc3{bottom:30px;left:50%;transform:translateX(-50%);animation-delay:3s}
.fc2{transform:translateY(-50%)}
.fc-emoji{font-size:22px}
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;align-items:center;justify-content:center}
.modal-overlay.active{display:flex}
.modal{background:#fff;border-radius:24px;padding:48px;max-width:520px;width:92%;text-align:center;box-shadow:0 24px 80px rgba(0,0,0,.2);animation:mi .35s ease;position:relative}
@keyframes mi{from{opacity:0;transform:scale(.9) translateY(20px)}to{opacity:1;transform:scale(1) translateY(0)}}
.modal-close{position:absolute;top:16px;right:16px;width:36px;height:36px;border-radius:50%;background:var(--g100);border:none;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;transition:var(--t)}
.modal-close:hover{background:var(--g200)}
.modal-flag{font-size:56px;margin-bottom:16px}
.modal h3{font-size:24px;font-weight:800;color:var(--dark);margin-bottom:10px}
.modal p{font-size:14px;color:var(--g500);margin-bottom:28px;line-height:1.7}
.modal-btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.btn-now{display:inline-flex;align-items:center;gap:8px;padding:14px 28px;background:linear-gradient(135deg,var(--blue),var(--cyan));color:#fff;border-radius:10px;font-weight:700;font-size:15px;border:none;cursor:pointer;transition:var(--t)}
.btn-now:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,102,255,.4)}
.btn-later{display:inline-flex;align-items:center;gap:8px;padding:14px 28px;background:var(--g100);color:var(--g500);border-radius:10px;font-weight:600;font-size:15px;border:none;cursor:pointer;transition:var(--t)}
.btn-later:hover{background:var(--g200)}
.wh-section{padding:80px 24px;background:linear-gradient(135deg,var(--blue) 0%,#0088ee 50%,var(--cyan) 100%)}
.wh-header{text-align:center;margin-bottom:48px}
.wh-header h2{font-size:36px;font-weight:800;color:#fff;margin-bottom:12px}
.wh-header p{font-size:16px;color:rgba(255,255,255,.82)}
.wh-card{background:#fff;border-radius:24px;padding:48px;max-width:960px;margin:0 auto;box-shadow:0 20px 60px rgba(0,0,0,.2)}
.wh-tabs{display:flex;gap:8px;margin-bottom:32px;background:var(--g100);padding:6px;border-radius:12px;width:fit-content}
.wh-tab{padding:10px 28px;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;border:none;background:transparent;color:var(--g500);transition:var(--t)}
.wh-tab.active{background:linear-gradient(135deg,var(--blue),var(--cyan));color:#fff;box-shadow:0 4px 12px rgba(0,102,255,.3)}
.wh-content{display:none}
.wh-content.active{display:block}
.addr-fields{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.addr-field{display:flex;align-items:center;padding:16px 18px;background:var(--g50);border-radius:10px;border:1px solid var(--g200);transition:var(--t)}
.addr-field:hover{border-color:var(--blue);background:rgba(0,102,255,.02)}
.field-label{font-size:13px;font-weight:600;color:var(--g400);width:110px;flex-shrink:0}
.field-value{font-size:14px;font-weight:700;color:var(--dark);flex:1}
.copy-btn{display:flex;align-items:center;gap:5px;padding:6px 12px;background:rgba(0,102,255,.08);border:1px solid rgba(0,102,255,.18);border-radius:6px;font-size:12px;font-weight:700;color:var(--blue);cursor:pointer;transition:var(--t);white-space:nowrap}
.copy-btn:hover{background:var(--blue);color:#fff;border-color:var(--blue)}
.copy-btn.copied{background:#22c55e!important;border-color:#22c55e!important;color:#fff!important}
.wh-cta{margin-top:32px;text-align:center}
.btn-wh-cta{display:inline-flex;align-items:center;gap:10px;padding:16px 40px;background:linear-gradient(135deg,var(--blue),var(--cyan));color:#fff;border-radius:var(--r);font-weight:700;font-size:16px;text-decoration:none;box-shadow:0 4px 20px rgba(0,102,255,.35);transition:var(--t)}
.btn-wh-cta:hover{transform:translateY(-3px);box-shadow:0 8px 30px rgba(0,102,255,.45)}
.partners{background:var(--g50);padding:40px 0;overflow:hidden;border-top:1px solid var(--g200);border-bottom:1px solid var(--g200)}
.partners-track{display:flex;animation:ps 35s linear infinite}
.partners-content{display:flex;align-items:center;gap:24px;white-space:nowrap;padding:0 24px;font-size:14px;font-weight:500;color:var(--g400);flex-shrink:0}
@keyframes ps{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.partners-track:hover{animation-play-state:paused}
.section{padding:100px 24px}
.section-alt{background:var(--g50)}
.section-header{text-align:center;margin-bottom:60px}
.section-tag{display:inline-block;padding:8px 18px;background:rgba(0,102,255,.08);border:1px solid rgba(0,102,255,.18);border-radius:24px;font-size:12px;font-weight:700;color:var(--blue);text-transform:uppercase;letter-spacing:.8px;margin-bottom:16px}
.section-title{font-size:clamp(28px,4vw,42px);font-weight:800;color:var(--dark);margin-bottom:16px}
.section-desc{font-size:16px;color:var(--g500);max-width:600px;margin:0 auto;line-height:1.7}
.services-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.service-card{padding:36px 28px;background:#fff;border:1px solid var(--g200);border-radius:var(--r2);transition:var(--t);position:relative;overflow:hidden}
.service-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--blue),var(--cyan));transform:scaleX(0);transform-origin:left;transition:var(--t)}
.service-card:hover{border-color:var(--blue);box-shadow:var(--shadow2);transform:translateY(-8px)}
.service-card:hover::before{transform:scaleX(1)}
.service-card.featured{border:2px solid var(--blue);background:linear-gradient(160deg,rgba(0,102,255,.03) 0%,rgba(0,212,255,.03) 100%);transform:scale(1.02)}
.fb{position:absolute;top:18px;right:18px;padding:6px 12px;background:var(--orange);color:#fff;border-radius:20px;font-size:12px;font-weight:700}
.si{width:60px;height:60px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(0,102,255,.1),rgba(0,212,255,.1));border-radius:14px;margin-bottom:20px;color:var(--blue);transition:var(--t)}
.service-card:hover .si{background:linear-gradient(135deg,var(--blue),var(--cyan));color:#fff;transform:scale(1.1)}
.si svg{width:30px;height:30px}
.service-title{font-size:20px;font-weight:700;color:var(--dark);margin-bottom:12px}
.service-desc{font-size:14px;color:var(--g500);line-height:1.8;margin-bottom:20px}
.service-link{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:700;color:var(--blue);transition:var(--t)}
.service-link:hover{gap:14px}
.process-tabs{display:flex;gap:16px;justify-content:center;margin-bottom:60px}
.tab-btn{display:flex;align-items:center;gap:10px;padding:12px 24px;background:#fff;border:2px solid var(--g200);border-radius:12px;font-size:15px;font-weight:700;color:var(--g500);transition:var(--t);cursor:pointer}
.tab-btn:hover{border-color:var(--blue);color:var(--blue)}
.tab-btn.active{background:linear-gradient(135deg,var(--blue),var(--cyan));border-color:transparent;color:#fff}
.tab-btn svg{width:20px;height:20px}
.process-content{display:none;animation:fa .5s ease}
.process-content.active{display:block}
.process-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;margin-bottom:48px;align-items:flex-start}
.step{position:relative}
.step-num{font-size:52px;font-weight:800;background:linear-gradient(135deg,var(--blue),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:16px;line-height:1}
.step-icon{width:72px;height:72px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(0,102,255,.1),rgba(0,212,255,.1));border-radius:16px;margin-bottom:20px;color:var(--blue)}
.step-icon svg{width:40px;height:40px}
.step-title{font-size:18px;font-weight:700;color:var(--dark);margin-bottom:10px}
.step-desc{font-size:14px;color:var(--g500);line-height:1.8}
.detail-card{background:#fff;border-radius:var(--r2);padding:36px;box-shadow:var(--shadow)}
.detail-title{font-size:18px;font-weight:700;color:var(--dark);margin-bottom:24px}
.detail-features{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.detail-feat{display:flex;align-items:flex-start;gap:12px}
.detail-feat svg{width:20px;height:20px;color:var(--blue);flex-shrink:0;margin-top:2px}
.detail-feat span{font-size:14px;color:var(--g500);line-height:1.6}
.brand-cats{display:flex;gap:10px;justify-content:center;margin-bottom:48px;flex-wrap:wrap}
.cat-btn{padding:10px 20px;background:#fff;border:1px solid var(--g200);border-radius:24px;font-size:13px;font-weight:700;color:var(--g500);cursor:pointer;transition:var(--t)}
.cat-btn:hover,.cat-btn.active{background:linear-gradient(135deg,var(--blue),var(--cyan));border-color:transparent;color:#fff}
.brands-showcase{margin-bottom:48px}
.brand-row{display:grid;grid-template-columns:repeat(6,1fr);gap:16px;margin-bottom:16px}
.brand-item{transition:var(--t)}
.brand-item.hidden{display:none}
.brand-card{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:28px 16px;background:#fff;border:1px solid var(--g200);border-radius:var(--r);transition:var(--t);cursor:pointer;min-height:150px}
.brand-card:hover{border-color:var(--blue);box-shadow:var(--shadow);transform:translateY(-4px)}
.brand-logo{width:72px;height:72px;display:flex;align-items:center;justify-content:center;margin-bottom:12px;color:var(--blue)}
.brand-logo svg{width:100%;height:100%}
.brand-name{font-size:14px;font-weight:700;color:var(--dark);text-align:center}
.featured-products{background:var(--g50);padding:48px;border-radius:var(--r2)}
.products-title{font-size:24px;font-weight:800;color:var(--dark);margin-bottom:8px}
.products-desc{font-size:14px;color:var(--g500);margin-bottom:28px}
.products-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.product-card{background:#fff;border-radius:var(--r);overflow:hidden;transition:var(--t);box-shadow:var(--shadow)}
.product-card:hover{transform:translateY(-4px);box-shadow:var(--shadow2)}
.product-img{width:100%;height:150px;background:var(--g100);display:flex;align-items:center;justify-content:center;font-size:48px}
.product-info{padding:18px}
.product-cat{display:inline-block;padding:4px 10px;background:rgba(0,102,255,.08);border-radius:6px;font-size:12px;font-weight:700;color:var(--blue);margin-bottom:8px}
.product-name{font-size:15px;font-weight:700;color:var(--dark);margin-bottom:8px}
.product-val,.product-ship{font-size:13px;color:var(--g500);margin-bottom:4px}
.pricing-calc{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-bottom:48px;background:#fff;padding:48px;border-radius:var(--r2);box-shadow:var(--shadow)}
.calc-form{display:flex;flex-direction:column;gap:20px}
.form-group{display:flex;flex-direction:column;gap:8px}
.form-label{font-size:14px;font-weight:700;color:var(--dark)}
.form-input,.form-select{padding:12px 16px;border:1px solid var(--g200);border-radius:8px;font-size:14px;color:var(--dark);transition:var(--t)}
.form-input:focus,.form-select:focus{outline:none;border-color:var(--blue);box-shadow:0 0 0 3px rgba(0,102,255,.1)}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.size-inputs{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.btn-calc{display:flex;align-items:center;justify-content:center;gap:10px;padding:14px 32px;background:linear-gradient(135deg,var(--blue),var(--cyan));color:#fff;border-radius:8px;font-weight:700;font-size:15px;transition:var(--t);box-shadow:0 4px 12px rgba(0,102,255,.3);border:none;cursor:pointer;margin-top:8px}
.btn-calc:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,102,255,.4)}
.calc-result{display:flex;align-items:center;justify-content:center;background:var(--g50);border-radius:12px;min-height:300px}
.result-placeholder{text-align:center;color:var(--g400)}
.result-placeholder svg{width:48px;height:48px;margin:0 auto 16px;opacity:.4}
.pricing-features{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.pricing-feat{display:flex;align-items:center;gap:12px;padding:20px;background:#fff;border-radius:var(--r);box-shadow:var(--shadow)}
.pricing-feat svg{width:22px;height:22px;color:var(--blue);flex-shrink:0}
.pricing-feat span{font-size:13px;font-weight:700;color:var(--dark)}
.features-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.feature-item{padding:40px 28px;background:#fff;border:1px solid var(--g200);border-radius:var(--r2);transition:var(--t);text-align:center}
.feature-item:hover{border-color:var(--blue);box-shadow:var(--shadow2);transform:translateY(-8px)}
.feature-icon{width:72px;height:72px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(0,102,255,.1),rgba(0,212,255,.1));border-radius:16px;margin:0 auto 20px;color:var(--blue);transition:var(--t)}
.feature-item:hover .feature-icon{background:linear-gradient(135deg,var(--blue),var(--cyan));color:#fff;transform:scale(1.1)}
.feature-icon svg{width:40px;height:40px}
.feature-title{font-size:18px;font-weight:700;color:var(--dark);margin-bottom:12px}
.feature-desc{font-size:14px;color:var(--g500);line-height:1.8}
.testimonials-slider{overflow:hidden;margin-top:48px}
.testimonials-track{display:flex;gap:24px;animation:ts 35s linear infinite}
@keyframes ts{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.testimonials-track:hover{animation-play-state:paused}
.testimonial-card{flex-shrink:0;width:340px;padding:28px;background:#fff;border-radius:var(--r2);box-shadow:var(--shadow);transition:var(--t)}
.testimonial-card:hover{transform:translateY(-6px);box-shadow:var(--shadow2)}
.testimonial-rating{display:flex;gap:3px;margin-bottom:14px;font-size:16px}
.testimonial-text{font-size:14px;color:var(--g500);line-height:1.8;margin-bottom:18px;font-style:italic}
.testimonial-author{display:flex;align-items:center;gap:12px}
.author-avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--blue),var(--cyan));color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px}
.author-name{font-size:14px;font-weight:700;color:var(--dark)}
.author-loc{font-size:12px;color:var(--g400)}
footer{background:var(--dark);color:#fff;padding:60px 24px 30px}
.footer-grid{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1.5fr repeat(3,1fr);gap:48px;margin-bottom:40px}
.footer-brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;margin-bottom:16px}
.footer-brand .logo-text{background:linear-gradient(135deg,var(--blue),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-size:22px}
.footer-desc{font-size:14px;color:rgba(255,255,255,.6);line-height:1.8;margin-bottom:16px}
.footer-contact p{font-size:14px;color:rgba(255,255,255,.6);margin-bottom:8px}
.footer-section h4{font-size:16px;font-weight:700;margin-bottom:20px}
.footer-section ul{list-style:none}
.footer-section li{margin-bottom:12px}
.footer-section a{font-size:14px;color:rgba(255,255,255,.6);transition:var(--t)}
.footer-section a:hover{color:var(--blue)}
.footer-bottom{max-width:1200px;margin:0 auto;padding-top:30px;border-top:1px solid rgba(255,255,255,.1);display:flex;justify-content:space-between;align-items:center;font-size:13px;color:rgba(255,255,255,.45)}
.support-widget{position:fixed;bottom:30px;right:30px;z-index:9998}
.support-btn{width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,var(--blue),var(--cyan));border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px rgba(0,102,255,.4);transition:var(--t);position:relative}
.support-btn::before{content:'';position:absolute;width:100%;height:100%;border-radius:50%;background:rgba(0,102,255,.3);animation:sp 2s ease-in-out infinite}
@keyframes sp{0%{transform:scale(1);opacity:.8}100%{transform:scale(1.8);opacity:0}}
.support-btn:hover{transform:scale(1.1)}
.support-btn svg{width:28px;height:28px;color:#fff;position:relative;z-index:1}
.support-panel{display:none;position:absolute;bottom:75px;right:0;width:300px;background:#fff;border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,.15);overflow:hidden;animation:fa .3s ease}
.support-panel.active{display:block}
.support-header{background:linear-gradient(135deg,var(--blue),var(--cyan));padding:20px;color:#fff}
.support-header h4{font-size:16px;font-weight:700;margin-bottom:4px}
.support-header p{font-size:12px;opacity:.85}
.support-channels{padding:12px}
.support-channel{display:flex;align-items:center;gap:14px;padding:12px 14px;border-radius:10px;cursor:pointer;transition:var(--t);text-decoration:none;color:inherit}
.support-channel:hover{background:var(--g100)}
.support-channel-icon{width:42px;height:42px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0}
.support-channel-name{font-size:13px;font-weight:700;color:var(--dark)}
.support-channel-value{font-size:12px;color:var(--g400);margin-top:2px}
.support-footer{padding:14px 20px;background:var(--g100);border-top:1px solid var(--g200);font-size:12px;color:var(--g400);text-align:center}
@media(max-width:768px){
.hide-m{display:none!important}
.navbar{height:60px}
.nav{height:60px}
.nav-links{display:none}
.m-btn{display:flex}
.hero{grid-template-columns:1fr;padding:80px 24px 60px;gap:40px;min-height:auto}
.hero-visual{display:none}
.hero-title{font-size:28px}
.services-grid{grid-template-columns:1fr}
.process-steps{grid-template-columns:1fr}
.step-connector{display:none}
.detail-features{grid-template-columns:1fr}
.brand-row{grid-template-columns:repeat(3,1fr)}
.products-grid{grid-template-columns:1fr}
.pr