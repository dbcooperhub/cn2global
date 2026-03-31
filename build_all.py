# -*- coding: utf-8 -*-
"""CN2Global Complete Website Builder v3 - All pages"""
import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Written: {path} ({len(content)} bytes)")

BASE = r'C:\Users\wangs\.qclaw\workspace\cn2global'
os.makedirs(BASE, exist_ok=True)

# ======== COMPLETE CSS ========
CSS = '''
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
    --primary:#0066FF;--secondary:#00D4FF;--accent:#FF6B35;
    --dark:#1a1a2e;--light:#f8f9fa;--white:#fff;
    --gray-50:#fafafa;--gray-100:#f5f5f5;--gray-200:#e8e8e8;--gray-300:#d0d0d0;
    --gray-400:#999;--gray-500:#666;--gray-600:#333;
    --radius:12px;--radius-lg:16px;
    --shadow:0 4px 20px rgba(0,0,0,.08);--shadow-md:0 4px 20px rgba(0,0,0,.1);--shadow-lg:0 8px 40px rgba(0,0,0,.15);
    --transition:all .3s ease;
    --font:'Inter','Noto Sans SC',-apple-system,BlinkMacSystemFont,sans-serif;
}
html{scroll-behavior:smooth}
body{font-family:var(--font);color:var(--dark);background:var(--white);line-height:1.6;overflow-x:hidden;font-size:16px}
a{text-decoration:none;color:inherit}
button,input,select,textarea{font-family:var(--font)}
img{max-width:100%;display:block}
.container{max-width:1200px;margin:0 auto;padding:0 24px}
.text-center{text-align:center}

/* Scrollbar */
::-webkit-scrollbar{width:8px}
::-webkit-scrollbar-track{background:var(--gray-100)}
::-webkit-scrollbar-thumb{background:var(--primary);border-radius:4px}

/* ======= LANGUAGE SYSTEM ======= */
.lang-zh,.lang-en{display:none}
html[data-lang="zh"] .lang-zh{display:block}
html[data-lang="zh"] .lang-en{display:none}
html[data-lang="en"] .lang-zh{display:none}
html[data-lang="en"] .lang-en{display:block}

/* ======= NAVBAR ======= */
.navbar{
    position:fixed;top:0;left:0;right:0;z-index:1000;
    background:rgba(255,255,255,.97);backdrop-filter:blur(12px);
    border-bottom:1px solid rgba(0,0,0,.05);transition:var(--transition);
}
.navbar.scrolled{box-shadow:0 2px 20px rgba(0,0,0,.08);background:rgba(255,255,255,.99)}
.nav-container{
    max-width:1200px;margin:0 auto;padding:0 24px;
    display:flex;align-items:center;justify-content:space-between;height:70px;
}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;color:var(--primary);transition:var(--transition)}
.logo:hover{transform:scale(1.03)}
.logo-icon{width:36px;height:36px;color:var(--primary)}
.logo-text{background:linear-gradient(135deg,var(--primary),var(--secondary));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-size:22px}
.nav-links{display:flex;gap:32px;flex:1;margin-left:48px}
.nav-links a{font-size:14px;font-weight:500;color:var(--gray-500);transition:var(--transition);position:relative;padding:4px 0}
.nav-links a:hover{color:var(--primary)}
.nav-links a::after{content:'';position:absolute;bottom:0;left:0;width:0;height:2px;background:var(--primary);transition:var(--transition)}
.nav-links a:hover::after{width:100%}
.nav-actions{display:flex;gap:10px;align-items:center}
.btn-outline{
    padding:8px 20px;font-size:14px;font-weight:600;color:var(--primary);
    border:2px solid var(--primary);border-radius:8px;transition:var(--transition);background:transparent;
}
.btn-outline:hover{background:var(--primary);color:#fff}
.btn-primary{
    padding:10px 24px;font-size:14px;font-weight:600;color:#fff;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    border-radius:8px;transition:var(--transition);box-shadow:0 4px 12px rgba(0,102,255,.3);border:none;cursor:pointer;
}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,102,255,.4)}
.lang-switcher{position:relative}
.lang-btn{
    display:flex;align-items:center;gap:6px;padding:7px 14px;
    background:rgba(0,102,255,.08);border:1px solid rgba(0,102,255,.15);
    border-radius:8px;font-size:13px;font-weight:600;color:var(--primary);cursor:pointer;transition:var(--transition);
}
.lang-btn:hover{background:rgba(0,102,255,.15)}
.lang-dropdown{
    display:none;position:absolute;top:calc(100% + 8px);right:0;
    background:#fff;border-radius:var(--radius);box-shadow:var(--shadow-lg);
    overflow:hidden;min-width:160px;z-index:100;
}
.lang-dropdown.show{display:block}
.lang-option{
    display:flex;align-items:center;gap:10px;padding:12px 16px;
    font-size:14px;font-weight:500;cursor:pointer;transition:var(--transition);
}
.lang-option:hover{background:var(--gray-100)}
.lang-option.active{background:rgba(0,102,255,.08);color:var(--primary)}
.mobile-menu-btn{
    display:none;flex-direction:column;gap:5px;width:28px;height:28px;background:none;border:none;cursor:pointer;padding:0;
}
.mobile-menu-btn span{width:100%;height:2px;background:var(--dark);border-radius:2px;transition:var(--transition);display:block}

/* ======= HERO ======= */
.hero{
    margin-top:70px;position:relative;overflow:hidden;
    padding:100px 24px;display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;min-height:85vh;
}
.hero-bg{position:absolute;top:0;left:0;right:0;bottom:0;z-index:0}
.hero-gradient{
    position:absolute;top:0;left:0;right:0;bottom:0;
    background:radial-gradient(ellipse at 30% 50%,rgba(0,102,255,.08) 0%,transparent 60%),
                radial-gradient(ellipse at 70% 50%,rgba(0,212,255,.06) 0%,transparent 60%);
}
.hero-particles{position:absolute;width:100%;height:100%}
.particle{position:absolute;width:3px;height:3px;background:var(--primary);border-radius:50%;opacity:.2;animation:particleFloat 15s ease-in-out infinite}
@keyframes particleFloat{
    0%,100%{transform:translate(0,0);opacity:.2}
    50%{transform:translate(30px,-20px);opacity:.5}
}
.hero-content{position:relative;z-index:1}
.hero-badge{
    display:inline-flex;align-items:center;gap:8px;padding:8px 16px;
    background:rgba(0,102,255,.08);border:1px solid rgba(0,102,255,.2);
    border-radius:24px;font-size:13px;font-weight:600;color:var(--primary);margin-bottom:24px;
    animation:fadeInDown .8s ease;
}
.hero-title{
    font-size:clamp(32px,5vw,56px);font-weight:800;line-height:1.15;margin-bottom:24px;color:var(--dark);
    animation:fadeInDown .8s ease .1s both;
}
.gradient-text{
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero-desc{
    font-size:17px;color:var(--gray-500);margin-bottom:32px;line-height:1.8;max-width:520px;
    animation:fadeInDown .8s ease .2s both;
}
.hero-actions{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:48px;animation:fadeInDown .8s ease .3s both}
.btn-hero-primary{
    display:inline-flex;align-items:center;gap:10px;padding:16px 32px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    color:#fff;border-radius:var(--radius);font-weight:700;font-size:15px;
    transition:var(--transition);box-shadow:0 4px 20px rgba(0,102,255,.35);border:none;cursor:pointer;
}
.btn-hero-primary:hover{transform:translateY(-3px);box-shadow:0 8px 30px rgba(0,102,255,.45)}
.btn-hero-secondary{
    display:inline-flex;align-items:center;gap:10px;padding:16px 32px;
    background:var(--gray-50);color:var(--primary);border-radius:var(--radius);
    font-weight:600;font-size:15px;transition:var(--transition);
    border:1px solid rgba(0,102,255,.2);cursor:pointer;
}
.btn-hero-secondary:hover{background:rgba(0,102,255,.06);transform:translateY(-3px)}
.hero-stats{display:flex;gap:40px;animation:fadeInUp .8s ease .4s both}
.stat-item{display:flex;flex-direction:column;gap:6px}
.stat-num{font-size:32px;font-weight:800;background:linear-gradient(135deg,var(--primary),var(--secondary));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.stat-label{font-size:13px;color:var(--gray-400);font-weight:500}
.stat-div{width:1px;background:var(--gray-200)}

/* Country Selector */
.country-reg{margin-top:32px;animation:fadeInUp .8s ease .35s both}
.country-reg-label{
    display:block;font-size:14px;font-weight:600;color:var(--gray-600);margin-bottom:10px;
}
.country-select-wrap{position:relative;display:inline-block;width:100%;max-width:440px}
.country-select{
    width:100%;padding:14px 48px 14px 16px;border:2px solid rgba(0,102,255,.25);
    border-radius:var(--radius);font-size:14px;font-weight:600;color:var(--dark);
    background:#fff;cursor:pointer;appearance:none;-webkit-appearance:none;
    transition:var(--transition);box-shadow:0 2px 12px rgba(0,102,255,.06);
}
.country-select:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(0,102,255,.12)}
.select-arrow{position:absolute;right:16px;top:50%;transform:translateY(-50%);pointer-events:none;color:var(--primary)}

/* Hero Visual */
.hero-visual{position:relative;z-index:1;display:flex;align-items:center;justify-content:center}
.globe-wrap{position:relative;width:420px;height:420px}
.globe-ring{position:absolute;border:1px solid rgba(0,102,255,.15);border-radius:50%;animation:globeRotate 20s linear infinite}
.ring-1{width:320px;height:320px;top:50px;left:50px;animation-duration:24s}
.ring-2{width:220px;height:220px;top:100px;left:100px;animation-duration:18s;animation-direction:reverse}
.ring-3{width:120px;height:120px;top:150px;left:150px;animation-duration:12s}
@keyframes globeRotate{from{transform:rotate(0)}to{transform:rotate(360deg)}}
.globe-core{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:200px;height:200px;color:var(--primary)}
.globe-svg{width:100%;height:100%}
.pulse-dot{animation:pulse 2s ease-in-out infinite}
.pulse-ring{animation:pulseRing 2s ease-in-out infinite}
@keyframes pulse{0%,100%{r:5;opacity:1}50%{r:7;opacity:.6}}
@keyframes pulseRing{0%{r:8;opacity:1}100%{r:20;opacity:0}}
.floating-card{
    position:absolute;background:#fff;padding:14px 18px;border-radius:14px;
    box-shadow:var(--shadow-md);display:flex;align-items:center;gap:10px;
    font-size:13px;font-weight:600;color:var(--dark);white-space:nowrap;
    animation:cardFloat 4s ease-in-out infinite;box-shadow:0 4px 20px rgba(0,0,0,.1);
}
.card-emoji{font-size:22px}
.card-1{top:30px;left:0;animation-delay:0s}
.card-2{top:50%;right:0;transform:translateY(-50%);animation-delay:1.5s}
.card-3{bottom:30px;left:50%;transform:translateX(-50%);animation-delay:3s}
@keyframes cardFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.card-2{transform:translateY(-50%)}

/* ======= REGISTER MODAL ======= */
.reg-modal-overlay{
    display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);
    z-index:9999;align-items:center;justify-content:center;
}
.reg-modal-overlay.active{display:flex}
.reg-modal{
    background:#fff;border-radius:24px;padding:48px;max-width:520px;width:92%;
    text-align:center;box-shadow:0 24px 80px rgba(0,0,0,.2);animation:modalIn .35s ease;position:relative;
}
@keyframes modalIn{from{opacity:0;transform:scale(.9) translateY(20px)}to{opacity:1;transform:scale(1) translateY(0)}}
.reg-modal-close{
    position:absolute;top:16px;right:16px;width:36px;height:36px;border-radius:50%;
    background:var(--gray-100);border:none;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;transition:var(--transition);
}
.reg-modal-close:hover{background:var(--gray-200)}
.reg-modal-flag{font-size:56px;margin-bottom:16px}
.reg-modal h3{font-size:24px;font-weight:800;color:var(--dark);margin-bottom:10px}
.reg-modal p{font-size:14px;color:var(--gray-500);margin-bottom:28px;line-height:1.7}
.reg-modal-btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.btn-reg-now{
    display:inline-flex;align-items:center;gap:8px;padding:14px 28px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    color:#fff;border-radius:10px;font-weight:700;font-size:15px;border:none;cursor:pointer;transition:var(--transition);
}
.btn-reg-now:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,102,255,.4)}
.btn-reg-later{
    display:inline-flex;align-items:center;gap:8px;padding:14px 28px;
    background:var(--gray-100);color:var(--gray-500);border-radius:10px;
    font-weight:600;font-size:15px;border:none;cursor:pointer;transition:var(--transition);
}
.btn-reg-later:hover{background:var(--gray-200)}

/* ======= WAREHOUSE SECTION ======= */
.warehouse-section{
    padding:80px 24px;background:linear-gradient(135deg,var(--primary) 0%,#0088ee 50%,var(--secondary) 100%);
}
.warehouse-header{text-align:center;margin-bottom:48px}
.warehouse-header h2{font-size:36px;font-weight:800;color:#fff;margin-bottom:12px}
.warehouse-header p{font-size:16px;color:rgba(255,255,255,.82)}
.warehouse-card{
    background:#fff;border-radius:24px;padding:48px;max-width:960px;margin:0 auto;
    box-shadow:0 20px 60px rgba(0,0,0,.2);
}
.warehouse-tabs{
    display:flex;gap:8px;margin-bottom:32px;background:var(--gray-100);
    padding:6px;border-radius:12px;width:fit-content;
}
.warehouse-tab{
    padding:10px 28px;border-radius:8px;font-size:14px;font-weight:700;
    cursor:pointer;border:none;background:transparent;color:var(--gray-500);transition:var(--transition);
}
.warehouse-tab.active{background:linear-gradient(135deg,var(--primary),var(--secondary));color:#fff;box-shadow:0 4px 12px rgba(0,102,255,.3)}
.warehouse-content{display:none}
.warehouse-content.active{display:block}
.address-fields{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.address-field{
    display:flex;align-items:center;padding:16px 18px;background:var(--gray-50);
    border-radius:10px;border:1px solid var(--gray-200);transition:var(--transition);
}
.address-field:hover{border-color:var(--primary);background:rgba(0,102,255,.02)}
.field-label{font-size:13px;font-weight:600;color:var(--gray-400);width:110px;flex-shrink:0}
.field-value{font-size:14px;font-weight:700;color:var(--dark);flex:1}
.copy-btn{
    display:flex;align-items:center;gap:5px;padding:6px 12px;
    background:rgba(0,102,255,.08);border:1px solid rgba(0,102,255,.18);
    border-radius:6px;font-size:12px;font-weight:700;color:var(--primary);
    cursor:pointer;transition:var(--transition);white-space:nowrap;
}
.copy-btn:hover{background:var(--primary);color:#fff;border-color:var(--primary)}
.copy-btn.copied{background:#22c55e!important;border-color:#22c55e!important;color:#fff!important}
.warehouse-cta{margin-top:32px;text-align:center}
.btn-warehouse-cta{
    display:inline-flex;align-items:center;gap:10px;padding:16px 40px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    color:#fff;border-radius:var(--radius);font-weight:700;font-size:16px;
    text-decoration:none;box-shadow:0 4px 20px rgba(0,102,255,.35);transition:var(--transition);
}
.btn-warehouse-cta:hover{transform:translateY(-3px);box-shadow:0 8px 30px rgba(0,102,255,.45)}

/* ======= PARTNERS ======= */
.partners{background:var(--gray-50);padding:40px 0;overflow:hidden;border-top:1px solid var(--gray-200);border-bottom:1px solid var(--gray-200)}
.partners-track{display:flex;animation:partnerScroll 35s linear infinite}
.partners-content{
    display:flex;align-items:center;gap:24px;white-space:nowrap;
    padding:0 24px;font-size:14px;font-weight:500;color:var(--gray-400);flex-shrink:0;
}
.dot{color:var(--gray-300)}
@keyframes partnerScroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.partners-track:hover{animation-play-state:paused}

/* ======= SERVICES ======= */
.services{padding:100px 24px}
.section-header{text-align:center;margin-bottom:60px}
.section-tag{
    display:inline-block;padding:8px 18px;background:rgba(0,102,255,.08);
    border:1px solid rgba(0,102,255,.18);border-radius:24px;
    font-size:12px;font-weight:700;color:var(--primary);text-transform:uppercase;letter-spacing:.8px;margin-bottom:16px;
}
.section-title{font-size:clamp(28px,4vw,42px);font-weight:800;color:var(--dark);margin-bottom:16px}
.section-desc{font-size:16px;color:var(--gray-500);max-width:600px;margin:0 auto;line-height:1.7}
.services-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.service-card{
    padding:36px 28px;background:#fff;border:1px solid var(--gray-200);
    border-radius:var(--radius-lg);transition:var(--transition);position:relative;overflow:hidden;
}
.service-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--primary),var(--secondary));transform:scaleX(0);transform-origin:left;transition:var(--transition)}
.service-card:hover{border-color:var(--primary);box-shadow:var(--shadow-lg);transform:translateY(-8px)}
.service-card:hover::before{transform:scaleX(1)}
.service-card.featured{border:2px solid var(--primary);background:linear-gradient(160deg,rgba(0,102,255,.03) 0%,rgba(0,212,255,.03) 100%);transform:scale(1.02)}
.featured-badge{position:absolute;top:18px;right:18px;padding:6px 12px;background:var(--accent);color:#fff;border-radius:20px;font-size:12px;font-weight:700}
.service-icon{
    width:60px;height:60px;display:flex;align-items:center;justify-content:center;
    background:linear-gradient(135deg,rgba(0,102,255,.1),rgba(0,212,255,.1));
    border-radius:14px;margin-bottom:20px;color:var(--primary);transition:var(--transition);
}
.service-card:hover .service-icon{background:linear-gradient(135deg,var(--primary),var(--secondary));color:#fff;transform:scale(1.1)}
.service-icon svg{width:30px;height:30px}
.service-title{font-size:20px;font-weight:700;color:var(--dark);margin-bottom:12px}
.service-desc{font-size:14px;color:var(--gray-500);line-height:1.8;margin-bottom:20px}
.service-link{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:700;color:var(--primary);transition:var(--transition)}
.service-link:hover{gap:14px}

/* ======= HOW IT WORKS ======= */
.how-it-works{padding:100px 24px;background:var(--gray-50)}
.process-tabs{display:flex;gap:16px;justify-content:center;margin-bottom:60px}
.tab-btn{
    display:flex;align-items:center;gap:10px;padding:12px 24px;
    background:#fff;border:2px solid var(--gray-200);border-radius:12px;
    font-size:15px;font-weight:700;color:var(--gray-500);transition:var(--transition);cursor:pointer;
}
.tab-btn:hover{border-color:var(--primary);color:var(--primary)}
.tab-btn.active{background:linear-gradient(135deg,var(--primary),var(--secondary));border-color:transparent;color:#fff}
.tab-btn svg{width:20px;height:20px}
.process-content{display:none;animation:fadeIn .5s ease}
.process-content.active{display:block}
.process-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;margin-bottom:48px;align-items:flex-start}
.step{position:relative}
.step-num{font-size:52px;font-weight:800;background:linear-gradient(135deg,var(--primary),var(--secondary));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:16px;line-height:1}
.step-icon{width:72px;height:72px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(0,102,255,.1),rgba(0,212,255,.1));border-radius:16px;margin-bottom:20px;color:var(--primary)}
.step-icon svg{width:40px;height:40px}
.step-title{font-size:18px;font-weight:700;color:var(--dark);margin-bottom:10px}
.step-desc{font-size:14px;color:var(--gray-500);line-height:1.8}
.detail-card{background:#fff;border-radius:var(--radius-lg);padding:36px;box-shadow:var(--shadow-md)}
.detail-title{font-size:18px;font-weight:700;color:var(--dark);margin-bottom:24px}
.detail-features{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.detail-feat{display:flex;align-items:flex-start;gap:12px}
.detail-feat svg{width:20px;height:20px;color:var(--primary);flex-shrink:0;margin-top:2px}
.detail-feat span{font-size:14px;color:var(--gray-500);line-height:1.6}

/* ======= BRANDS ======= */
.brands{padding:100px 24px}
.brand-cats{display:flex;gap:10px;justify-content:center;margin-bottom:48px;flex-wrap:wrap}
.cat-btn{
    padding:10px 20px;background:#fff;border:1px solid var(--gray-200);
    border-radius:24px;font-size:13px;font-weight:700;color:var(--gray-500);cursor:pointer;transition:var(--transition);
}
.cat-btn:hover,.cat-btn.active{background:linear-gradient(135deg,var(--primary),var(--secondary));border-color:transparent;color:#fff}
.brands-showcase{margin-bottom:48px}
.brand-row{display:grid;grid-template-columns:repeat(6,1fr);gap:16px;margin-bottom:16px}
.brand-item{transition:var(--transition)}
.brand-item.hidden{display:none}
.brand-card{
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    padding:28px 16px;background:#fff;border:1px solid var(--gray-200);
    border-radius:var(--radius);transition:var(--transition);cursor:pointer;min-height:150px;
}
.brand-card:hover{border-color:var(--primary);box-shadow:var(--shadow-md);transform:translateY(-4px)}
.brand-logo{width:72px;height:72px;display:flex;align-items:center;justify-content:center;margin-bottom:12px;color:var(--primary)}
.brand-logo svg{width:100%;height:100%}
.brand-name{font-size:14px;font-weight:700;color:var(--dark);text-align:center}
.featured-products{background:var(--gray-50);padding:48px;border-radius:var(--radius-lg)}
.products-title{font-size:24px;font-weight:800;color:var(--dark);margin-bottom:8px}
.products-desc{font-size:14px;color:var(--gray-500);margin-bottom:28px}
.products-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.product-card{background:#fff;border-radius:var(--radius);overflow:hidden;transition:var(--transition);box-shadow:var(--shadow)}
.product-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-md)}
.product-img{width:100%;height:150px;background:var(--gray-100);display:flex;align-items:center;justify-content:center;font-size:48px}
.product-info{padding:18px}
.product-cat{display:inline-block;padding:4px 10px;background:rgba(0,102,255,.08);border-radius:6px;font-size:12px;font-weight:700;color:var(--primary);margin-bottom:8px}
.product-name{font-size:15px;font-weight:700;color:var(--dark);margin-bottom:8px}
.product-val,.product-ship{font-size:13px;color:var(--gray-500);margin-bottom:4px}

/* ======= PRICING ======= */
.pricing{padding:100px 24px;background:var(--gray-50)}
.pricing-calc{
    display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-bottom:48px;
    background:#fff;padding:48px;border-radius:var(--radius-lg);box-shadow:var(--shadow-md);
}
.calc-form{display:flex;flex-direction:column;gap:20px}
.form-group{display:flex;flex-direction:column;gap:8px}
.form-label{font-size:14px;font-weight:700;color:var(--dark)}
.form-input,.form-select{
    padding:12px 16px;border:1px solid var(--gray-200);border-radius:8px;
    font-size:14px;color:var(--dark);transition:var(--transition);
}
.form-input:focus,.form-select:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(0,102,255,.1)}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.size-inputs{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.btn-calc{
    display:flex;align-items:center;justify-content:center;gap:10px;padding:14px 32px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    color:#fff;border-radius:8px;font-weight:700;font-size:15px;
    transition:var(--transition);box-shadow:0 4px 12px rgba(0,102,255,.3);border:none;cursor:pointer;margin-top:8px;
}
.btn-calc:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,102,255,.4)}
.calc-result{
    display:flex;align-items:center;justify-content:center;
    background:var(--gray-50);border-radius:12px;min-height:300px;
}
.result-placeholder{text-align:center;color:var(--gray-400)}
.result-placeholder svg{width:48px;height:48px;margin:0 auto 16px;opacity:.4}
.pricing-features{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.pricing-feat{
    display:flex;align-items:center;gap:12px;padding:20px;background:#fff;
    border-radius:var(--radius);box-shadow:var(--shadow);
}
.pricing-feat svg{width:22px;height:22px;color:var(--primary);flex-shrink:0}
.pricing-feat span{font-size:13px;font-weight:700;color:var(--dark)}

/* ======= WHY US ======= */
.why-us{padding:100px 24px}
.features-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.feature-item{
    padding:40px 28px;background:#fff;border:1px solid var(--gray-200);
    border-radius:var(--radius-lg);transition:var(--transition);text-align:center;
}
.feature-item:hover{border-color:var(--primary);box-shadow:var(--shadow-lg);transform:translateY(-8px)}
.feature-icon{
    width:72px;height:72px;display:flex;align-items:center;justify-content:center;
    background:linear-gradient(135deg,rgba(0,102,255,.1),rgba(0,212,255,.1));
    border-radius:16px;margin:0 auto 20px;color:var(--primary);transition:var(--transition);
}
.feature-item:hover .feature-icon{background:linear-gradient(135deg,var(--primary),var(--secondary));color:#fff;transform:scale(1.1)}
.feature-icon svg{width:40px;height:40px}
.feature-title{font-size:18px;font-weight:700;color:var(--dark);margin-bottom:12px}
.feature-desc{font-size:14px;color:var(--gray-500);line-height:1.8}

/* ======= TESTIMONIALS ======= */
.testimonials{padding:100px 24px;background:var(--gray-50)}
.testimonials-slider{overflow:hidden;margin-top:48px}
.testimonials-track{display:flex;gap:24px;animation:testScroll 35s linear infinite}
@keyframes testScroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.testimonials-track:hover{animation-play-state:paused}
.testimonial-card{
    flex-shrink:0;width:340px;padding:28px;background:#fff;
    border-radius:var(--radius-lg);box-shadow:var(--shadow);transition:var(--transition);
}
.testimonial-card:hover{transform:translateY(-6px);box-shadow:var(--shadow-lg)}
.testimonial-rating{display:flex;gap:3px;margin-bottom:14px;font-size:16px}
.testimonial-text{font-size:14px;color:var(--gray-500);line-height:1.8;margin-bottom:18px;font-style:italic}
.testimonial-author{display:flex;align-items:center;gap:12px}
.author-avatar{
    width:44px;height:44px;border-radius:50%;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;
}
.author-name{font-size:14px;font-weight:700;color:var(--dark)}
.author-loc{font-size:12px;color:var(--gray-400)}

/* ======= FOOTER ======= */
footer{background:var(--dark);color:#fff;padding:60px 24px 30px}
.footer-grid{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1.5fr repeat(3,1fr);gap:48px;margin-bottom:40px}
.footer-brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;color:var(--primary);margin-bottom:16px}
.footer-brand .logo-text{background:linear-gradient(135deg,var(--primary),var(--