// i18n.js - 国际化配置
const translations = {
  zh: {
    // 导航
    nav: {
      home: '首页',
      features: '功能',
      pricing: '价格',
      about: '关于',
      contact: '联系',
      login: '登录',
      register: '注册',
      logout: '退出'
    },
    // 主页
    hero: {
      title: '从青岛出发，连接世界每一个角落',
      subtitle: '在中国购物，我们为您寄送到全球。免费仓库地址、智能集运、专业代购，运费节省高达 80%',
      cta_primary: '立即注册',
      cta_secondary: '了解详情'
    },
    // 注册
    register: {
      title: '创建账户',
      subtitle: '为您的国家/地区创建 CN2Global 账户',
      country: '选择国家/地区',
      phone: '手机号码',
      email: '邮箱地址',
      password: '密码',
      confirm_password: '确认密码',
      agree_terms: '我同意服务条款和隐私政策',
      register_btn: '注册',
      login_link: '已有账户？登录',
      google_login: '使用 Google 登录',
      phone_placeholder: '请输入手机号码',
      password_placeholder: '至少 8 个字符',
      error_phone: '请输入有效的手机号码',
      error_password: '密码至少需要 8 个字符',
      error_email: '请输入有效的邮箱地址',
      success: '注册成功！',
      sending_code: '发送验证码...',
      verify_code: '验证码',
      verify_code_placeholder: '请输入 6 位验证码'
    },
    // 登录
    login: {
      title: '登录账户',
      phone: '手机号码',
      password: '密码',
      login_btn: '登录',
      register_link: '没有账户？注册',
      forgot_password: '忘记密码？',
      google_login: '使用 Google 登录',
      error_phone: '请输入有效的手机号码',
      error_password: '密码不能为空',
      error_invalid: '手机号码或密码错误'
    },
    // 客服
    support: {
      title: '客服支持',
      chat: '在线客服',
      email: '发送邮件',
      phone: '拨打电话',
      faq: '常见问题',
      hours: '工作时间：周一至周五 9:00-18:00'
    },
    // 语言
    language: '语言',
    select_language: '选择语言'
  },
  en: {
    nav: {
      home: 'Home',
      features: 'Features',
      pricing: 'Pricing',
      about: 'About',
      contact: 'Contact',
      login: 'Login',
      register: 'Register',
      logout: 'Logout'
    },
    hero: {
      title: 'Ship from Qingdao to the World',
      subtitle: 'Shop in China, we ship to you globally. Free warehouse address, smart consolidation, professional purchasing. Save up to 80% on shipping.',
      cta_primary: 'Register Now',
      cta_secondary: 'Learn More'
    },
    register: {
      title: 'Create Account',
      subtitle: 'Create a CN2Global account for your country/region',
      country: 'Select Country/Region',
      phone: 'Phone Number',
      email: 'Email Address',
      password: 'Password',
      confirm_password: 'Confirm Password',
      agree_terms: 'I agree to the Terms of Service and Privacy Policy',
      register_btn: 'Register',
      login_link: 'Already have an account? Login',
      google_login: 'Sign up with Google',
      phone_placeholder: 'Enter your phone number',
      password_placeholder: 'At least 8 characters',
      error_phone: 'Please enter a valid phone number',
      error_password: 'Password must be at least 8 characters',
      error_email: 'Please enter a valid email address',
      success: 'Registration successful!',
      sending_code: 'Sending verification code...',
      verify_code: 'Verification Code',
      verify_code_placeholder: 'Enter 6-digit code'
    },
    login: {
      title: 'Login',
      phone: 'Phone Number',
      password: 'Password',
      login_btn: 'Login',
      register_link: 'No account? Register',
      forgot_password: 'Forgot password?',
      google_login: 'Sign in with Google',
      error_phone: 'Please enter a valid phone number',
      error_password: 'Password cannot be empty',
      error_invalid: 'Invalid phone number or password'
    },
    support: {
      title: 'Customer Support',
      chat: 'Live Chat',
      email: 'Send Email',
      phone: 'Call Us',
      faq: 'FAQ',
      hours: 'Hours: Monday-Friday 9:00-18:00'
    },
    language: 'Language',
    select_language: 'Select Language'
  },
  ja: {
    nav: {
      home: 'ホーム',
      features: '機能',
      pricing: '価格',
      about: '概要',
      contact: 'お問い合わせ',
      login: 'ログイン',
      register: '登録',
      logout: 'ログアウト'
    },
    hero: {
      title: '青島から世界へ',
      subtitle: '中国で買い物して、世界中に配送します。無料の倉庫住所、スマート統合、プロの購入。送料を最大80%節約できます。',
      cta_primary: '今すぐ登録',
      cta_secondary: '詳細を見る'
    },
    register: {
      title: 'アカウント作成',
      subtitle: 'あなたの国/地域用の CN2Global アカウントを作成します',
      country: '国/地域を選択',
      phone: '電話番号',
      email: 'メールアドレス',
      password: 'パスワード',
      confirm_password: 'パスワード確認',
      agree_terms: '利用規約とプライバシーポリシーに同意します',
      register_btn: '登録',
      login_link: 'アカウントをお持ちですか？ログイン',
      google_login: 'Google で登録',
      phone_placeholder: '電話番号を入力してください',
      password_placeholder: '8文字以上',
      error_phone: '有効な電話番号を入力してください',
      error_password: 'パスワードは8文字以上である必要があります',
      error_email: '有効なメールアドレスを入力してください',
      success: '登録成功！',
      sending_code: '確認コードを送信中...',
      verify_code: '確認コード',
      verify_code_placeholder: '6桁のコードを入力'
    },
    login: {
      title: 'ログイン',
      phone: '電話番号',
      password: 'パスワード',
      login_btn: 'ログイン',
      register_link: 'アカウントをお持ちでないですか？登録',
      forgot_password: 'パスワードをお忘れですか？',
      google_login: 'Google でログイン',
      error_phone: '有効な電話番号を入力してください',
      error_password: 'パスワードを入力してください',
      error_invalid: '電話番号またはパスワードが無効です'
    },
    support: {
      title: 'カスタマーサポート',
      chat: 'ライブチャット',
      email: 'メール送信',
      phone: '電話する',
      faq: 'よくある質問',
      hours: '営業時間：月〜金 9:00-18:00'
    },
    language: '言語',
    select_language: '言語を選択'
  },
  de: {
    nav: {
      home: 'Startseite',
      features: 'Funktionen',
      pricing: 'Preise',
      about: 'Über uns',
      contact: 'Kontakt',
      login: 'Anmelden',
      register: 'Registrieren',
      logout: 'Abmelden'
    },
    hero: {
      title: 'Von Qingdao in die Welt',
      subtitle: 'Kaufen Sie in China, wir versenden weltweit. Kostenlose Lageradresse, intelligente Konsolidierung, professionelle Einkäufe. Sparen Sie bis zu 80% bei den Versandkosten.',
      cta_primary: 'Jetzt registrieren',
      cta_secondary: 'Mehr erfahren'
    },
    register: {
      title: 'Konto erstellen',
      subtitle: 'Erstellen Sie ein CN2Global-Konto für Ihr Land/Ihre Region',
      country: 'Land/Region wählen',
      phone: 'Telefonnummer',
      email: 'E-Mail-Adresse',
      password: 'Passwort',
      confirm_password: 'Passwort bestätigen',
      agree_terms: 'Ich stimme den Nutzungsbedingungen und der Datenschutzrichtlinie zu',
      register_btn: 'Registrieren',
      login_link: 'Haben Sie bereits ein Konto? Anmelden',
      google_login: 'Mit Google registrieren',
      phone_placeholder: 'Geben Sie Ihre Telefonnummer ein',
      password_placeholder: 'Mindestens 8 Zeichen',
      error_phone: 'Bitte geben Sie eine gültige Telefonnummer ein',
      error_password: 'Das Passwort muss mindestens 8 Zeichen lang sein',
      error_email: 'Bitte geben Sie eine gültige E-Mail-Adresse ein',
      success: 'Registrierung erfolgreich!',
      sending_code: 'Verifizierungscode wird gesendet...',
      verify_code: 'Verifizierungscode',
      verify_code_placeholder: '6-stelligen Code eingeben'
    },
    login: {
      title: 'Anmelden',
      phone: 'Telefonnummer',
      password: 'Passwort',
      login_btn: 'Anmelden',
      register_link: 'Kein Konto? Registrieren',
      forgot_password: 'Passwort vergessen?',
      google_login: 'Mit Google anmelden',
      error_phone: 'Bitte geben Sie eine gültige Telefonnummer ein',
      error_password: 'Passwort darf nicht leer sein',
      error_invalid: 'Ungültige Telefonnummer oder Passwort'
    },
    support: {
      title: 'Kundensupport',
      chat: 'Live-Chat',
      email: 'E-Mail senden',
      phone: 'Anrufen',
      faq: 'Häufig gestellte Fragen',
      hours: 'Öffnungszeiten: Montag-Freitag 9:00-18:00'
    },
    language: 'Sprache',
    select_language: 'Sprache wählen'
  },
  fr: {
    nav: {
      home: 'Accueil',
      features: 'Fonctionnalités',
      pricing: 'Tarifs',
      about: 'À propos',
      contact: 'Contact',
      login: 'Connexion',
      register: 'Inscription',
      logout: 'Déconnexion'
    },
    hero: {
      title: 'De Qingdao au monde',
      subtitle: 'Achetez en Chine, nous livrons dans le monde entier. Adresse d\'entrepôt gratuite, consolidation intelligente, achat professionnel. Économisez jusqu\'à 80% sur les frais d\'expédition.',
      cta_primary: 'S\'inscrire maintenant',
      cta_secondary: 'En savoir plus'
    },
    register: {
      title: 'Créer un compte',
      subtitle: 'Créez un compte CN2Global pour votre pays/région',
      country: 'Sélectionner le pays/la région',
      phone: 'Numéro de téléphone',
      email: 'Adresse e-mail',
      password: 'Mot de passe',
      confirm_password: 'Confirmer le mot de passe',
      agree_terms: 'J\'accepte les conditions d\'utilisation et la politique de confidentialité',
      register_btn: 'S\'inscrire',
      login_link: 'Vous avez déjà un compte ? Connexion',
      google_login: 'S\'inscrire avec Google',
      phone_placeholder: 'Entrez votre numéro de téléphone',
      password_placeholder: 'Au moins 8 caractères',
      error_phone: 'Veuillez entrer un numéro de téléphone valide',
      error_password: 'Le mot de passe doit contenir au moins 8 caractères',
      error_email: 'Veuillez entrer une adresse e-mail valide',
      success: 'Inscription réussie !',
      sending_code: 'Envoi du code de vérification...',
      verify_code: 'Code de vérification',
      verify_code_placeholder: 'Entrez le code à 6 chiffres'
    },
    login: {
      title: 'Connexion',
      phone: 'Numéro de téléphone',
      password: 'Mot de passe',
      login_btn: 'Connexion',
      register_link: 'Pas de compte ? S\'inscrire',
      forgot_password: 'Mot de passe oublié ?',
      google_login: 'Se connecter avec Google',
      error_phone: 'Veuillez entrer un numéro de téléphone valide',
      error_password: 'Le mot de passe ne peut pas être vide',
      error_invalid: 'Numéro de téléphone ou mot de passe invalide'
    },
    support: {
      title: 'Support client',
      chat: 'Chat en direct',
      email: 'Envoyer un e-mail',
      phone: 'Nous appeler',
      faq: 'FAQ',
      hours: 'Heures : lundi-vendredi 9:00-18:00'
    },
    language: 'Langue',
    select_language: 'Sélectionner la langue'
  }
};

// 国家代码和区号映射
const countryData = {
  CN: { name: '中国', code: '+86', lang: 'zh' },
  US: { name: 'United States', code: '+1', lang: 'en' },
  GB: { name: 'United Kingdom', code: '+44', lang: 'en' },
  JP: { name: '日本', code: '+81', lang: 'ja' },
  DE: { name: 'Deutschland', code: '+49', lang: 'de' },
  FR: { name: 'France', code: '+33', lang: 'fr' },
  CA: { name: 'Canada', code: '+1', lang: 'en' },
  AU: { name: 'Australia', code: '+61', lang: 'en' },
  SG: { name: 'Singapore', code: '+65', lang: 'en' },
  HK: { name: '香港', code: '+852', lang: 'zh' },
  TW: { name: '台湾', code: '+886', lang: 'zh' },
  KR: { name: '韓国', code: '+82', lang: 'ja' },
  IN: { name: 'India', code: '+91', lang: 'en' },
  BR: { name: 'Brasil', code: '+55', lang: 'en' },
  MX: { name: 'México', code: '+52', lang: 'en' },
  NZ: { name: 'New Zealand', code: '+64', lang: 'en' },
  TH: { name: 'Thailand', code: '+66', lang: 'en' },
  MY: { name: 'Malaysia', code: '+60', lang: 'en' },
  PH: { name: 'Philippines', code: '+63', lang: 'en' },
  VN: { name: 'Vietnam', code: '+84', lang: 'en' }
};

// 获取翻译
function t(key, lang = 'en') {
  const keys = key.split('.');
  let value = translations[lang];
  
  for (let k of keys) {
    if (value && typeof value === 'object') {
      value = value[k];
    } else {
      return key; // 返回 key 如果找不到翻译
    }
  }
  
  return value || key;
}

// 获取用户语言
function getUserLanguage() {
  const saved = localStorage.getItem('language');
  if (saved) return saved;
  
  const browserLang = navigator.language.split('-')[0];
  return translations[browserLang] ? browserLang : 'en';
}

// 设置语言
function setLanguage(lang) {
  localStorage.setItem('language', lang);
  document.documentElement.lang = lang;
  document.documentElement.setAttribute('data-lang', lang);
  
  // 更新所有翻译元素
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    el.textContent = t(key, lang);
  });
  
  // 更新所有占位符
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    el.placeholder = t(key, lang);
  });
}

// 导出
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { translations, countryData, t, getUserLanguage, setLanguage };
}
