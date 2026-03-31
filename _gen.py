# -*- coding: utf-8 -*-
import os

base = r"C:\Users\wangs\.qclaw\workspace\cn2global"
os.makedirs(base, exist_ok=True)

def write_file(name, content):
    path = os.path.join(base, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote: {name} ({len(content)} bytes)")

# ====== JS SHARED DATA ======
country_list = [
    ("🇨🇳", "中国", "China", "+86"),
    ("🇺🇸", "美国", "United States", "+1"),
    ("🇬🇧", "英国", "United Kingdom", "+44"),
    ("🇯🇵", "日本", "Japan", "+81"),
    ("🇰🇷", "韩国", "South Korea", "+82"),
    ("🇩🇪", "德国", "Germany", "+49"),
    ("🇫🇷", "法国", "France", "+33"),
    ("🇦🇺", "澳大利亚", "Australia", "+61"),
    ("🇨🇦", "加拿大", "Canada", "+1"),
    ("🇸🇬", "新加坡", "Singapore", "+65"),
    ("🇲🇾", "马来西亚", "Malaysia", "+60"),
    ("🇹🇭", "泰国", "Thailand", "+66"),
    ("🇻🇳", "越南", "Vietnam", "+84"),
    ("🇮🇩", "印度尼西亚", "Indonesia", "+62"),
    ("🇵🇭", "菲律宾", "Philippines", "+63"),
    ("🇮🇳", "印度", "India", "+91"),
    ("🇧🇷", "巴西", "Brazil", "+55"),
    ("🇲🇽", "墨西哥", "Mexico", "+52"),
    ("🇷🇺", "俄罗斯", "Russia", "+7"),
    ("🇰🇿", "哈萨克斯坦", "Kazakhstan", "+7"),
    ("🇹🇷", "土耳其", "Turkey", "+90"),
    ("🇸🇦", "沙特阿拉伯", "Saudi Arabia", "+966"),
    ("🇦🇪", "阿联酋", "UAE", "+971"),
    ("🇮🇱", "以色列", "Israel", "+972"),
    ("🇳🇱", "荷兰", "Netherlands", "+31"),
    ("🇧🇪", "比利时", "Belgium", "+32"),
    ("🇨🇭", "瑞士", "Switzerland", "+41"),
    ("🇦🇹", "奥地利", "Austria", "+43"),
    ("🇵🇱", "波兰", "Poland", "+48"),
    ("🇮🇹", "意大利", "Italy", "+39"),
    ("🇪🇸", "西班牙", "Spain", "+34"),
    ("🇵🇹", "葡萄牙", "Portugal", "+351"),
    ("🇬🇷", "希腊", "Greece", "+30"),
    ("🇸🇪", "瑞典", "Sweden", "+46"),
    ("🇳🇴", "挪威", "Norway", "+47"),
    ("🇩🇰", "丹麦", "Denmark", "+45"),
    ("🇫🇮", "芬兰", "Finland", "+358"),
    ("🇳🇿", "新西兰", "New Zealand", "+64"),
    ("🇿🇦", "南非", "South Africa", "+27"),
    ("🇳🇬", "尼日利亚", "Nigeria", "+234"),
    ("🇪🇬", "埃及", "Egypt", "+20"),
    ("🇹🇼", "台湾", "Taiwan", "+886"),
    ("🇭🇰", "香港", "Hong Kong", "+852"),
    ("🇲🇴", "澳门", "Macau", "+853"),
    ("🇹🇭", "阿曼", "Oman", "+968"),
    ("🇰🇼", "科威特", "Kuwait", "+965"),
    ("🇶🇦", "卡塔尔", "Qatar", "+974"),
    ("🇧🇭", "巴林", "Bahrain", "+973"),
    ("🇯🇴", "约旦", "Jordan", "+962"),
    ("🇱🇧", "黎巴嫩", "Lebanon", "+961"),
    ("🇵🇰", "巴基斯坦", "Pakistan", "+92"),
    ("🇧🇩", "孟加拉国", "Bangladesh", "+880"),
    ("🇱🇰", "斯里兰卡", "Sri Lanka", "+94"),
    ("🇳🇵", "尼泊尔", "Nepal", "+977"),
    ("🇲🇲", "缅甸", "Myanmar", "+95"),
    ("🇰🇭", "柬埔寨", "Cambodia", "+855"),
    ("🇱🇦", "老挝", "Laos", "+856"),
]

country_options_html = '\n'.join([
    f'    <option value="{code}" data-flag="{flag}">{flag} {zh} ({en}) {code}</option>'
    for flag, zh, en, code in country_list
])

# ====== CSS ======
css = """
        :root {
            --primary: #0066FF;
            --secondary: #00D4FF;
            --accent: #FF6B35;
            --dark: #1a1a2e;
            --light: #f8fafc;
            --gray: #64748b;
            --shadow: 0 4px 20px rgba(0,0,0,0.08);
            --radius: 12px;
            --radius-lg: 16px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', 'Noto Sans SC', sans-serif;
            background: var(--light);
            color: var(--dark);
            line-height: 1.6;
            overflow-x: hidden;
        }
        .navbar {
            position: fixed; top: 0; left: 0; right: 0;
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(20px);
            z-index: 1000; padding: 0 24px; height: 70px;
            display: flex; align-items: center; justify-content: space-between;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .logo { display: flex; align-items: center; gap: 10px; font-size: 24px; font-weight: 700; color: var(--primary); text-decoration: none; }
        .logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, var(--primary), var(--secondary)); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; }
        .nav-links { display: flex; align-items: center; gap: 24px; }
        .nav-links a { text-decoration: none; color: var(--dark); font-weight: 500; transition: color 0.2s; }
        .nav-links a:hover { color: var(--primary); }
        .lang-select { padding: 8px 16px; border: 1px solid #e2e8f0; border-radius: 8px; background: white; font-size: 14px; cursor: pointer; outline: none; }
        .btn-primary { background: var(--primary); color: white; padding: 10px 24px; border-radius: var(--radius); border: none; font-weight: 600; cursor: pointer; transition: all 0.2s; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; }
        .btn-primary:hover { background: #0052cc; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,102,255,0.3); }
        .btn-secondary { background: white; color: var(--primary); border: 2px solid var(--primary); padding: 8px 20px; border-radius: var(--radius); font-weight: 600; cursor: pointer; transition: all 0.2s; text-decoration: none; }
        .btn-secondary:hover { background: var(--primary); color: white; }
        .hero { min-height: 100vh; padding: 120px 24px 80px; background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); position: relative; overflow: hidden; }
        .hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(ellipse at 20% 50%, rgba(0,102,255,0.15) 0%, transparent 50%), radial-gradient(ellipse at 80% 50%, rgba(0,212,255,0.1) 0%, transparent 50%); }
        .hero-content { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; position: relative; z-index: 1; }
        .hero-text h1 { font-size: 56px; font-weight: 700; color: white; line-height: 1.2; margin-bottom: 24px; }
        .hero-text h1 span { background: linear-gradient(135deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .hero-text p { font-size: 18px; color: #94a3b8; margin-bottom: 32px; max-width: 500px; }
        .hero-stats { display: flex; gap: 40px; margin-bottom: 40px; }
        .stat-item { text-align: center; }
        .stat-number { font-size: 36px; font-weight: 700; color: var(--secondary); }
        .stat-label { font-size: 14px; color: #94a3b8; }
        .hero-form { background: white; border-radius: var(--radius-lg); padding: 32px; box-shadow: var(--shadow); }
        .hero-form h3 { margin-bottom: 20px; font-size: 20px; }
        .country-select { width: 100%; padding: 14px 16px; border: 2px solid #e2e8f0; border-radius: var(--radius); font-size: 16px; cursor: pointer; appearance: none; background: white url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2'%3E%3Cpolyline points='6,9 12,15 18,9'%3E%3C/polyline%3E%3C/svg%3E") no-repeat right 16px center; background-size: 20px; }
        .country-select:focus { border-color: var(--primary); outline: none; }
        .globe-container { position: relative; width: 400px; height: 400px; margin: 0 auto; }
        .globe { width: 100%; height: 100%; border-radius: 50%; background: linear-gradient(135deg, rgba(0,102,255,0.3) 0%, rgba(0,212,255,0.2) 100%); position: relative; animation: float 6s ease-in-out infinite; box-shadow: inset -20px -20px 40px rgba(0,0,0,0.3), 0 0 60px rgba(0,102,255,0.3); }
        .globe::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; border-radius: 50%; background: repeating-linear-gradient(0deg, transparent, transparent 40px, rgba(255,255,255,0.1) 40px, rgba(255,255,255,0.1) 41px), repeating-linear-gradient(90deg, transparent, transparent 40px, rgba(255,255,255,0.1) 40px, rgba(255,255,255,0.1) 41px); animation: rotate 20s linear infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .section { padding: 80px 24px; max-width: 1200px; margin: 0 auto; }
        .section-title { text-align: center; font-size: 40px; font-weight: 700; margin-bottom: 16px; }
        .section-subtitle { text-align: center; color: var(--gray); font-size: 18px; margin-bottom: 60px; }
        .warehouse-section { background: white; padding: 80px 24px; }
        .warehouse-tabs { display: flex; justify-content: center; gap: 16px; margin-bottom: 40px; }
        .warehouse-tab { padding: 12px 32px; border: 2px solid #e2e8f0; border-radius: var(--radius); background: white; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
        .warehouse-tab.active { background: var(--primary); color: white; border-color: var(--primary); }
        .warehouse-content { max-width: 1000px; margin: 0 auto; background: #f8fafc; border-radius: var(--radius-lg); padding: 40px; }
        .warehouse-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
        .warehouse-item { background: white; border-radius: var(--radius); padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        .warehouse-label { font-size: 12px; color: var(--gray); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
        .warehouse-value { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
        .warehouse-value span { font-weight: 600; font-size: 15px; word-break: break-all; }
        .copy-btn { background: #f1f5f9; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; color: var(--gray); transition: all 0.2s; white-space: nowrap; margin-left: 12px; }
        .copy-btn:hover { background: var(--primary); color: white; }
        .copy-btn.copied { background: #10b981; color: white; }
        .partners-section { background: #f8fafc; padding: 60px 0; overflow: hidden; }
        .marquee { display: flex; animation: marquee 30s linear infinite; }
        .marquee-content { display: flex; gap: 60px; padding: 0 30px; flex-shrink: 0; }
        .partner-logo { font-size: 24px; font-weight: 700; color: var(--gray); white-space: nowrap; opacity: 0.6; }
        .partner-logo:hover { opacity: 1; }
        @keyframes marquee { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
        .services-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
        .service-card { background: white; border-radius: var(--radius-lg); padding: 32px 24px; text-align: center; box-shadow: var(--shadow); transition: all 0.3s; }
        .service-card:hover { transform: translateY(-8px); box-shadow: 0 12px 40px rgba(0,0,0,0.12); }
        .service-icon { width: 64px; height: 64px; background: linear-gradient(135deg, var(--primary), var(--secondary)); border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 28px; }
        .service-card h3 { font-size: 18px; margin-bottom: 12px; }
        .service-card p { color: var(--gray); font-size: 14px; }
        .process-steps { display: grid; grid-template-columns: repeat(5, 1fr); gap: 24px; position: relative; }
        .process-steps::before { content: ''; position: absolute; top: 40px; left: 10%; right: 10%; height: 2px; background: linear-gradient(90deg, var(--primary), var(--secondary); }
        .step-item { text-align: center; position: relative; }
        .step-number { width: 80px; height: 80px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 28px; font-weight: 700; color: var(--primary); box-shadow: var(--shadow); position: relative; z-index: 1; }
        .step-item h4 { font-size: 16px; margin-bottom: 8px; }
        .step-item p { font-size: 14px; color: var(--gray); }
        .brands-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 24px; }
        .brand-item { background: white; border-radius: var(--radius); padding: 24px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); font-weight: 600; color: var(--gray); }
        .calculator-section { background: linear-gradient(135deg, var(--dark) 0%, #1e293b 100%); padding: 80px 24px; }
        .calculator { max-width: 800px; margin: 0 auto; background: white; border-radius: var(--radius-lg); padding: 40px; }
        .calculator h2 { text-align: center; margin-bottom: 32px; }
        .calc-form { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 32px; }
        .calc-input-group { display: flex; flex-direction: column; gap: 8px; }
        .calc-input-group label { font-size: 14px; font-weight: 500; }
        .calc-input-group select, .calc-input-group input { padding: 12px 16px; border: 2px solid #e2e8f0; border-radius: var(--radius); font-size: 16px; }
        .calc-input-group select:focus, .calc-input-group input:focus { border-color: var(--primary); outline: none; }
        .calc-result { text-align: center; padding: 24px; background: linear-gradient(135deg, var(--primary), var(--secondary)); border-radius: var(--radius); color: white; }
        .calc-result .price { font-size: 48px; font-weight: 700; }
        .calc-result .unit { font-size: 16px; opacity: 0.9; }
        .why-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }
        .why-item { text-align: center; padding: 32px; }
        .why-icon { width: 80px; height: 80px; background: linear-gradient(135deg, rgba(0,102,255,0.1), rgba(0,212,255,0.1)); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 36px; }
        .why-item h3 { font-size: 20px; margin-bottom: 12px; }
        .why-item p { color: var(--gray); }
        .testimonials-section { background: #f8fafc; padding: 80px 24px; }
        .testimonials-slider { max-width: 900px; margin: 0 auto; overflow: hidden; }
        .testimonials-track { display: flex; transition: transform 0.5s ease; }
        .testimonial-card { min-width: 100%; background: white; border-radius: var(--radius-lg); padding: 40px; box-shadow: var(--shadow); }
        .testimonial-text { font-size: 18px; font-style: italic; color: var(--dark); margin-bottom: 24px; line-height: 1.8; }
        .testimonial-author { display: flex; align-items: center; gap: 16px; }
        .author-avatar { width: 56px; height: 56px; background: linear-gradient(135deg, var(--primary), var(--secondary)); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px; font-weight: 700; }
        .author-info h4 { font-size: 16px; }
        .author-info p { font-size: 14px; color: var(--gray); }
        .testimonial-dots { display: flex; justify-content: center; gap: 8px; margin-top: 24px; }
        .dot { width: 10px; height: 10px; border-radius: 50%; background: #cbd5e1; cursor: pointer; transition: all 0.3s; }
        .dot.active { background: var(--primary); width: 30px; border-radius: 5px; }
        .footer { background: var(--dark); color: white; padding: 60px 24px 30px; }
        .footer-content { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; }
        .footer-brand p { color: #94a3b8; margin-top: 16px; font-size: 14px; }
        .footer-col h4 { font-size: 16px; margin-bottom: 20px; }
        .footer-col ul { list-style: none; }
        .footer-col li { margin-bottom: 12px; }
        .footer-col a { color: #94a3b8; text-decoration: none; font-size: 14px; transition: color 0.2s; }
        .footer-col a:hover { color: var(--secondary); }
        .footer-bottom { max-width: 1200px; margin: 40px auto 0; padding-top: 30px; border-top: 1px solid #334155; text-align: center; color: #64748b; font-size: 14px; }
        .cs-widget { position: fixed; bottom: 24px; right: 24px; z-index: 9999; }
        .cs-toggle { width: 56px; height: 56px; background: var(--primary); border-radius: 50%; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 20px rgba(0,102,255,0.4); transition: all 0.3s; }
        .cs-toggle:hover { transform: scale(1.1); }
        .cs-toggle svg { width: 28px; height: 28px; fill: white; }
        .cs-panel { position: absolute; bottom: 70px; right: 0; width: 320px; background: white; border-radius: var(--radius-lg); box-shadow: 0 10px 40px rgba(0,0,0,0.15); opacity: 0; visibility: hidden; transform: translateY(20px); transition: all 0.3s; }
        .cs-panel.open { opacity: 1; visibility: visible; transform: translateY(0); }
        .cs-panel-header { padding: 20px; background: linear-gradient(135deg, var(--primary), var(--secondary)); border-radius: var(--radius-lg) var(--radius-lg) 0 0; color: white; }
        .cs-panel-header h3 { font-size: 18px; }
        .cs-panel-body { padding: 20px; }
        .cs-item { display: flex; align-items: center; gap: 12px; padding: 12px; border-radius: var(--radius); cursor: pointer; transition: background 0.2s; }
        .cs-item:hover { background: #f1f5f9; }
        .cs-item-icon { width: 36px; height: 36px; background: #f1f5f9; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
        .cs-item-text span { display: block; font-size: 12px; color: var(--gray); }
        .cs-item-text strong { font-size: 14px; }
        .cs-footer { padding: 16px 20px; border-top: 1px solid #e2e8f0; font-size: 12px; color: var(--gray); }
        .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 10000; opacity: 0; visibility: hidden; transition: all 0.3s; }
        .modal-overlay.open { opacity: 1; visibility: visible; }
        .modal { background: white; border-radius: var(--radius-lg); width: 90%; max-width: 440px; max-height: 90vh; overflow-y: auto; transform: scale(0.9); transition: transform 0.3s; }
        .modal-overlay.open .modal { transform: scale(1); }
        .modal-header { padding: 24px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; }
        .modal-header h2 { font-size: 20px; }
        .modal-close { background: none; border: none; font-size: 24px; cursor: pointer; color: var(--gray); }
        .modal-body { padding: 24px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; font-size: 14px; font-weight: 500; margin-bottom: 8px; }
        .form-input { width: 100%; padding: 12px 16px; border: 2px solid #e2e8f0; border-radius: var(--radius); font-size: 16px; transition: border-color 0.2s; }
        .form-input:focus { border-color: var(--primary); outline: none; }
        .form-input.error { border-color: #ef4444; }
        .error-message { color: #ef4444; font-size: 12px; margin-top: 6px; }
        .phone-input-group { display: flex; gap: 12px; }
        .phone-input-group .country-select { width: 140px; flex-shrink: 0; }
        .phone-input-group .form-input { flex: 1; }
        .code-btn { background: var(--primary); color: white; border: none; padding: 12px 20px; border-radius: var(--radius); font-weight: 600; cursor: pointer; transition: all 0.2s; }
        .code-btn:disabled { background: #94a3b8; cursor: not-allowed; }
        .code-btn:hover:not(:disabled) { background: #0052cc; }
        .google-btn { width: 100%; background: white; border: 2px solid #e2e8f0; padding: 14px; border-radius: var(--radius); font-size: 16px; font-weight: 500; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 12px; transition: all 0.2s; }
        .google-btn:hover { border-color: var(--gray); background: #f8fafc; }
        .divider { display: flex; align-items: center; gap: 16px; margin: 24px 0; color: var(--gray); font-size: 14px; }
        .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: #e2e8f0; }
        .auth-link { text-align: center; margin-top: 20px; font-size: 14px; color: var(--gray); }
        .auth-link a { color: var(--primary); text-decoration: none; font-weight: 500; }
        .auth-link a:hover { text-decoration: underline; }
        .loading { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255,255,255,0.9); z-index: 10001; align-items: center; justify-content: center; }
        .loading.active { display: flex; }
        .spinner { width: 48px; height: 48px; border: 4px solid #e2e8f0; border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .particles { position: absolute; top: 0; left: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; }
        .particle { position: absolute; width: 4px; height: 4px; background: var(--secondary); border-radius: 50%; opacity: 0.5; animation: particle-float 15s infinite; }
        @keyframes particle-float { 0%, 100% { transform: translateY(0) translateX(0); opacity: 0; } 10% { opacity: 0.5; } 90% { opacity: 0.5; } 100% { transform: translateY(-100vh) translateX(100px); opacity: 0; } }
        @media (max-width: 1024px) {
            .hero-content { grid-template-columns: 1fr; text-align: center; }
            .hero-stats { justify-content: center; }
            .hero-text p { margin: 0 auto 32px; }
            .globe-container { width: 300px; height: 300px; }
            .services-grid { grid-template-columns: repeat(2, 1fr); }
            .process-steps { grid-template-columns: repeat(3, 1fr); }
            .process-steps::before { display: none; }
            .brands-grid { grid-template-columns: repeat(3, 1fr); }
            .why-grid { grid-template-columns: repeat(2, 1fr); }
            .footer-content { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 768px) {
            .nav-links { display: none; }
            .hero-text h1 { font-size: 36px; }
            .hero-stats { flex-direction: column; gap: 20px; }
            .warehouse-grid { grid-template-columns: 1fr; }
            .services-grid { grid-template-columns: 1fr; }
            .process-steps { grid-template-columns: 1fr; }
            .brands-grid { grid-template-columns: repeat(2, 1fr); }
            .calc-form { grid-template-columns: 1fr; }
            .why-grid { grid-template-columns: 1fr; }
            .footer-content { grid-template-columns: 1fr; }
            .cs-panel { width: calc(100vw - 48px); right: -10px; }
        }
"""

# ====== SHARED JS ======
shared_js = """
    const translations = {
        zh: {
            hero_title: '全球电商仓储',
            hero_title2: '一站式物流解决方案',
            hero_desc: 'CN2Global为您提供专业的跨境电商仓储代发货服务，覆盖全球50+国家，支持一件代发、退换货处理、库存管理等全方位解决方案。',
            hero_cta: '立即开始',
            stat_countries: '覆盖国家',
            stat_orders: '日处理订单',
            stat_accuracy: '签收准确率',
            nav_services: '服务', nav_process: '流程', nav_warehouse: '仓库',
            nav_calculator: '价格计算器', nav_contact: '联系我们',
            nav_login: '登录', nav_register: '注册',
            services_title: '我们的服务', services_subtitle: '一站式跨境电商物流解决方案',
            service1_title: '仓储代发', service1_desc: '专业的仓储管理，订单24小时内发货，支持多平台对接',
            service2_title: '国际物流', service2_desc: '覆盖全球50+国家，多种物流渠道可选，全程追踪',
            service3_title: '退换货处理', service3_desc: '本地化退换货服务，降低退货成本，提升客户满意度',
            service4_title: '库存管理', service4_desc: '实时库存同步，智能补货提醒，防止断货超卖',
            service5_title: '定制包装', service5_desc: '支持品牌定制包装，提升开箱体验，增强品牌认知',
            service6_title: '保险服务', service6_desc: '全程物流保险，丢件损件全额赔付，安心托付',
            service7_title: '税务处理', service7_desc: '专业税务顾问，合规清关服务，避免税务风险',
            service8_title: 'API对接', service8_desc: '开放的API接口，支持ERP系统无缝集成',
            process_title: '服务流程', process_subtitle: '简单五步，开启全球销售',
            step1_title: '注册账户', step1_desc: '快速注册，审核通过',
            step2_title: '获取仓库地址', step2_desc: '获取专属仓库地址',
            step3_title: '发送货物', step3_desc: '将货物发至仓库',
            step4_title: '订单处理', step4_desc: '买家下单，自动发货',
            step5_title: '全球送达', step5_desc: '物流追踪，送达全球',
            warehouse_title: '仓库地址', warehouse_subtitle: '将货物发送至以下任一仓库，我们会为您处理后续所有物流',
            warehouse_warehouse: '仓库名称', warehouse_address: '仓库地址',
            warehouse_contact: '联系人', warehouse_phone: '联系电话',
            warehouse_recipient: '收货人', warehouse_postal: '邮编',
            copy: '复制', copied: '已复制',
            brands_title: '热门合作品牌', brands_subtitle: '服务超过1000家跨境电商企业',
            calc_title: '物流价格计算器', calc_subtitle: '输入您的信息，获取即时报价',
            calc_weight: '商品