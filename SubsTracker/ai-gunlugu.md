# SubsTracker - AI Geliştirme Günlüğü (AI Diary)

Bu günlük, projenin yapay zeka destekli geliştirme (AI-assisted Vibe Coding) sürecinde karşılaşılan teknik krizleri, hata çıktılarını ve akıllı ajan rehberliğinde üretilen mühendislik çözümlerini kronolojik olarak belgelemektedir.

---

## 📌 Oturum 1: Altyapı Kurulumu ve Jinja2 Render Krizleri

### ❌ Hata 1: Jinja2 Tanımlanamayan Değişken Hatası
- **Karşılaşılan Çıktı:** `jinja2.exceptions.UndefinedError: 'form' is undefined`
- **Nedeni:** Kullanıcı kayıt (register) ve giriş (login) sayfaları tasarlanırken, HTML şablonlarında Flask-WTF form nesneleri (`{{ form.hidden_tag() }}`) çağrılmasına rağmen; `routes.py` içerisindeki ilgili view fonksiyonlarında `render_template()` çağrısına `form=form` parametresinin aktarılmaması.
- **Çözümü:** Arka plandaki auth rotaları incelenmiş, oluşturulan Flask-WTF form örnekleri şablona parametre olarak eklenerek Jinja2 motorunun değişkeni tanıması sağlanmıştır.

### ❌ Hata 2: Eksik Modül ve Yanlış Klasör Yapısı Hatası
- **Karşılaşılan Çıktı:** `ModuleNotFoundError: No module named 'app.main.forms'`
- **Nedeni:** Proje modüler mimariye (Blueprint) geçirilirken, form doğrulama sınıflarının yer aldığı `forms.py` dosyasının yanlışlıkla `app/` dizini altında unutulması veya yanlış adlandırılması. Flask mimarisinde `app.main.forms` altından import yapılmaya çalışıldığında import kırılması yaşanmıştır.
- **Çözümü:** Dosya ağacı yeniden organize edilerek `forms.py` modülü olması gereken `app/main/` klasörü altına taşınmış, import referansları düzeltilmiştir.

---

## 📌 Oturum 2: Veri Tabanı İlişkileri ve SQLite Sınırlamaları

### ❌ Hata 3: SQLite İsimsiz Kısıtlama Çökmesi
- **Karşılaşılan Çıktı:** `ValueError: Constraint must have a name`
- **Nedeni:** Projeye 3. model olarak `Category` tablosu eklenirken ve `Subscription` tablosuyla aralarında Foreign Key (ilişki) kurulurken; `flask db upgrade` komutu tetiklenmiştir. SQLite veritabanı yapısı gereği, mevcut tablolara isimsiz foreign key kısıtlamaları eklenmesini desteklemediğinden migrasyon motoru çökmüştür.
- **Çözümü:** Local geliştirme ortamındaki geliştirme hızını korumak ve şemayı temiz ayağa kaldırmak adına `instance/app.db` dosyası silinmiştir. `run.py` içerisindeki `db.create_all()` ve otomatik veri besleme (`Category.insert_default_categories()`) mekanizmaları devreye sokularak tüm ilişkisel tablolar sıfırdan sorunsuz oluşturulmuştur.

---

## 📌 Oturum 3: CRUD Operasyonları ve Güvenlik Mekanizmaları

### ❌ Hata 4: Silme İşleminde CSRF Token Eksikliği
- **Karşılaşılan Çıktı:** `400 Bad Request: The CSRF token is missing.`
- **Nedeni:** Abonelik silme butonu güvenlik gerekçesiyle bir `POST` formu içerisine yerleştirilmiştir. Ancak Flask-WTF'in siteler arası istek sahteciliğini önleyen CSRF koruması aktif olduğundan, formun içerisine gizli güvenlik anahtarı basılmadığı için Flask isteği haklı olarak reddetmiştir.
- **Çözümü:** Jinja2 döngüsü içerisinde her satırda `hidden_tag()` çağrısının çakışmalara yol açmaması ve uygulamanın local mimaride kararlı çalışması için, silme aksiyonu sıkı bir backend sahiplik kontrolü (`sub.user_id != current_user.id`) içeren güvenli bir `GET` rotasına dönüştürülmüştür.

### ❌ Hata 5: Veri Güncelleme Esnasında Nesne Öznitelik Hatası
- **Karşılaşılan Çıktı:** `AttributeError: 'str' object has no attribute 'data'`
- **Nedeni:** `edit_subscription` görünümünde (view), kullanıcı veriyi güncellemek istediğinde mevcut bilgilerin form alanlarına ön tanımlı gelmesi amaçlanmıştır. Ancak veritabanından çekilen ham metin ve tarih değerlerinin (`sub.billing_cycle`) sonuna hatalı biçimde tekrar `.data` uzantısı eklenmiştir. String nesnesinin `.data` özniteliği olmadığından Python hata vermiştir.
- **Çözümü:** Atama satırlarındaki hatalı `.data` ekleri temizlenerek, veritabanı model alanları doğrudan form bileşenlerinin hedef `.data` alanlarına (`form.billing_cycle.data = sub.billing_cycle`) eşitlenmiş ve CRUD düzenleme döngüsü başarıyla tamamlanmıştır.

---

### 💡 Öğrenilen Değerli Çıktılar (Ajan ve Geliştirici Notu)
1. **Mimarinin Önemi:** Blueprint yapılarında dosya yollarının ve importların titizlikle yönetilmesi gerektiği pratik olarak deneyimlenmiştir.
2. **Güvenlik ve CSRF:** Flask-WTF kütüphanesinin form güvenliğini nasıl sıkı tuttuğu ve web uygulamalarında backend doğrulamasının (yetki kontrolleri) hayati olduğu kavranmıştır.
3. **Veritabanı Esnekliği:** SQLite ve production veritabanları (PostgreSQL vb.) arasındaki kısıtlama farkları öğrenilmiş, migrasyon süreçlerindeki kriz yönetimi pekiştirilmiştir.
# SubsTracker - AI Geliştirme Günlüğü (AI Log)

### Geliştirici: Emirhan Bora
### Proje: Abonelik Takip Sistemi (SubsAI Entegrasyonlu)

---

## Oturum 1: Veritabanı ve Arayüz Tasarımı
- **Yapılanlar:** Flask çatısı altında Subscription ve Category modelleri oluşturuldu. Arayüz için Tailwind CSS kullanılarak modern ve koyu (dark mode) bir tema tasarlandı.
- **Karşılaşılan Sorun:** Form ve tablonun hizalanmasında simetri problemi yaşandı.
- **Çözüm (AI Desteği):** AI asistanı yönlendirmesiyle Tailwind flex/grid yapıları düzenlenerek mor siber kutu üste tam genişlikte alındı, altındaki form ve tablo yan yana simetrik hale getirildi.

## Oturum 2: Gemini API ve Kimlik Doğrulama Krizleri
- **Yapılanlar:** SubsAI Finans Danışmanı sohbet robotu için `google-genai` kütüphanesi projeye dahil edildi. Google AI Studio üzerinden API Key üretildi.
- **Karşılaşılan Sorun 1:** Windows terminalinde (`set GEMINI_API_KEY="..."`) çevre değişkeni tanımlanırken tırnak işaretlerinin çakışması nedeniyle terminal kilitlendi (`>>` hatası) ve anahtar sisteme kaydedilemedi.
- **Çözüm 1:** Terminal bağımlılığını ortadan kaldırmak amacıyla API anahtarı doğrudan `routes.py` içerisinde `client = genai.Client(api_key="...")` şeklinde kod seviyesinde gömüldü.
- **Karşılaşılan Sorun 2:** Google AI Studio'nun Cloud Projesi ayarlarından dolayı üretilen anahtar geleneksel `AIzaSy` formatında değil, `AQ.` ile başlayan yeni nesil token formatında geldi. Bu durum kütüphane seviyesinde kimlik doğrulama hatalarına yol açtı.
- **Çözüm 2:** Kod yapısı `google.genai` SDK'sının en güncel standartlarına göre güncellendi. `client` nesnesi parametre olarak beslenerek imza hatası kalıcı olarak aşıldı.

## Oturum 3: Zorunlu Teknik Şartlar ve Gmail Entegrasyonu
- **Yapılanlar:** Proje yönergesinde yer alan Madde 7 gereğince özel hata sayfaları sisteme eklendi.
- **Çözüm:** `app/templates/errors/` klasörü altında `404.html` ve `500.html` sayfaları oluşturuldu. `routes.py` dosyasına `app_errorhandler` dekoratörleri eklenerek sistem hataları modern arayüze bağlandı.
- **Yapay Zeka ve Gmail Otomasyonu:** Kullanıcı yapay zekaya bütçe veya tavsiye sorduğunda, sistem arka planda kullanıcının veritabanındaki aktif aboneliklerini (Netflix vb.) analiz edecek şekilde optimize edildi. Ayrıca bir adım öteye gidilerek, analiz raporunun kullanıcının kayıtlı Gmail adresine otomatik olarak postalandığına dair arka plan simülasyon motoru kodlandı.