# 🚀 SubsTracker - Akıllı Abonelik Takip Sistemi

Gazi Üniversitesi - TUSAŞ Kazan Meslek Yüksekokulu BLG106 Dönem Projesi kapsamında geliştirilmiş, AI (Yapay Zeka) destekli modern bir abonelik yönetim ve finansal analiz web uygulamasıdır. 

Bu proje, **Flask** altyapısı ve **Tailwind CSS** arayüzü kullanılarak "Vibe Coding" ve AI ajan destekli geliştirme metodolojisiyle mimari edilmiştir.

---

## 🌟 Öne Çıkan Özellikler

- **🔒 Güvenli Kimlik Doğrulama (Auth System):** Kullanıcı kayıt, giriş ve çıkış süreçleri (Flask-Login ve Werkzeug şifreleme altyapısı).
- **📊 Gelişmiş Abonelik Yönetimi (CRUD):** Abonelik adı, fiyatı, para birimi (TL, USD, EUR), faturalandırma periyodu ve bir sonraki ödeme tarihlerinin eklenmesi, düzenlenmesi ve silinmesi.
- **🤖 SubsAI - Akıllı Finans Danışmanı (Gemini Pro Entegrasyonu):** Veritabanındaki aktif abonelikleri (Netflix vb.) ve toplam TL harcamasını canlı olarak analiz eden, kullanıcıya özel bütçe tavsiyeleri sunan yapay zeka motoru.
- **✉️ Otomatik Gmail Geri Bildirim Simülasyonu:** Kullanıcı bütçe analizi talep ettiğinde, sistem arka planda çalışarak detaylı raporun kullanıcının kayıtlı Gmail adresine postalandığını simüle eder.
- **🛡️ Özel Hata Yönetimi:** Standart sunucu hataları yerine uygulamaya özel tasarlanmış modern, koyu temalı `404` ve `500` hata sayfaları.
- **🎨 Modern Siber Koyu Tema (Dark Mode UI):** Tailwind CSS ve Slate/Purple renk paletleri kullanılarak tasarlanmış, tamamen simetrik ve göz yormayan minimalist arayüz.

---

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python / Flask
- **Veritabanı / ORM:** SQLite / Flask-SQLAlchemy
- **Form Yönetimi:** Flask-WTF / WTForms
- **Yapay Zeka:** Google GenAI SDK (Gemini-2.5-Flash)
- **Frontend / Tasarım:** HTML5, Jinja2, Tailwind CSS

---

## 📁 Proje Yapısı

```text
SubsTracker/
│
├── app/
│   ├── main/
│   │   ├── __init__.py
│   │   ├── forms.py     # Abonelik giriş formları
│   │   └── routes.py    # Rotalar, Gemini Motoru & Hata Yakalayıcılar
│   │
│   ├── templates/       # Jinja2 Şablonları
│   │   ├── errors/      # 404 ve 500 Özel Hata Sayfaları
│   │   ├── main/        # Ana sayfa ve düzenleme arayüzleri
│   │   └── base.html    # Ana iskelet yapısı
│   │
│   └── models.py        # User, Subscription ve Category Modelleri
│
├── docs/
│   └── ai-gunlugu.md    # Yapay Zeka Geliştirme Günlüğü
│
├── run.py               # Uygulamayı başlatan ana dosya
└── README.md            # Proje Tanıtım Dokümanı