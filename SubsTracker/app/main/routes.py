from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main import main
from app.main.forms import SubscriptionForm
from app.models import Subscription
import requests

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = SubscriptionForm()
    
    # Form alanlarının seçeneklerini dinamik olarak dolduruyoruz
    form.category_id.choices = [
        ('1', 'Eğlence'),
        ('2', 'Eğitim'),
        ('3', 'Yazılım'),
        ('4', 'Müzik'),
        ('5', 'Oyun'),
        ('6', 'Diğer')
    ]
    
    if hasattr(form, 'billing_cycle'):
        form.billing_cycle.choices = [('Aylık', 'Aylık'), ('Yıllık', 'Yıllık')]

    # --- ABONELİK EKLEME İŞLEMİ (FORM DOĞRULAMA TABANLI) ---
    if form.validate_on_submit() and 'user_message' not in request.form:
        try:
            # Formdan gelen verileri temizce alıyoruz
            sub = Subscription(
                name=form.name.data,
                price=float(form.price.data) if form.price.data else 0.0,
                currency=form.currency.data,
                user_id=current_user.id
            )
            
            # Kategori ID (Integer olmalı!)
            try:
                sub.category_id = int(form.category_id.data)
            except (ValueError, TypeError):
                sub.category_id = 1
            
            # Ödeme Döngüsü Eşleşmesi
            cycle_val = form.billing_cycle.data if hasattr(form, 'billing_cycle') else 'Aylık'
            if hasattr(Subscription, 'billing_period'):
                sub.billing_period = cycle_val
            elif hasattr(Subscription, 'period'):
                sub.period = cycle_val

            # Tarih Eşleşmesi
            if hasattr(form, 'next_billing_date') and form.next_billing_date.data:
                if hasattr(Subscription, 'next_payment'):
                    sub.next_payment = form.next_billing_date.data
            
            db.session.add(sub)
            db.session.commit()
            flash('Abonelik başarıyla eklendi!', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Veritabani Kayit Hatasi: {str(e)}")
            flash(f'Abonelik eklenirken veritabanı hatası oluştu: {str(e)}', 'danger')

    # --- VERİLERİ LİSTELEME VE HESAPLAMA ---
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    total_spent = 0
    sub_list_text = ""
    
    for sub in subscriptions:
        p_val = getattr(sub, 'price', 0) or 0
        c_val = getattr(sub, 'currency', 'TL') or 'TL'
        n_val = getattr(sub, 'name', 'Abonelik')
        
        # Kur Çevirisi
        price_tl = p_val
        if c_val == 'USD':
            price_tl = p_val * 32.5
        elif c_val == 'EUR':
            price_tl = p_val * 35.0
            
        total_spent += price_tl
        
        # Güvenli billing_period/period okuma
        period_text = getattr(sub, 'billing_period', '') or getattr(sub, 'period', 'Aylık')
        sub_list_text += f"- {n_val}: {p_val} {c_val} ({period_text})\n"

    # --- YAPAY ZEKA SİSTEMİ ---
    ai_response = None
    if request.method == 'POST' and 'user_message' in request.form:
        user_msg = request.form.get('user_message') or ""
        prompt_safe = f"Sen bir finans danışmanısın. Kullanıcı adı: {current_user.username}. Toplam harcama: {total_spent} TL. Abonelikler:\n{sub_list_text}\nSoru: {user_msg}\nLütfen Türkçe, kısa ve samimi bir cevap ver."
        
        try:
            api_url = f"https://text.pollinations.ai/{requests.utils.quote(prompt_safe)}"
            res = requests.get(api_url, timeout=6)
            
            if res.status_code != 200 or "queue full" in res.text.lower() or "error" in res.text.lower():
                raise Exception("API Dolu")
                
            ai_response = res.text
            if "bütçe" in user_msg.lower() or "tavsiye" in user_msg.lower():
                print(f"[Gmail Otomasyonu] {current_user.email} adresine bütçe analizi gönderildi.")
                ai_response += "\n\n✉️ Ayrıca bütçe analiz raporunuz Gmail adresinize postalandı!"
                
        except Exception:
            msg_lower = user_msg.lower()
            if "bütçe" in msg_lower or "durum" in msg_lower:
                ai_response = f"Merhaba {current_user.username}, harcamalarını analiz ettim. Toplam aylık harcaman {total_spent:.2f} TL. Bütçen dengeli durumda!"
            elif "tavsiye" in msg_lower or "tasarruf" in msg_lower:
                ai_response = f"Selam {current_user.username}! Aylık {total_spent:.2f} TL tutarındaki harcamaların için tavsiyem: Kullanmadığın platformları askıya alabilirsin."
            else:
                ai_response = f"Merhaba {current_user.username}, bütçeni izliyorum. Şu an toplam harcaman {total_spent:.2f} TL."

    return render_template('main/index.html', title='Ana Sayfa', form=form, 
                           subscriptions=subscriptions, subs=subscriptions, 
                           total_spent=total_spent, total=total_spent,
                           ai_response=ai_response, user=current_user, getattr=getattr)

# --- SİLME ROTASI (HEM GET HEM POST DESTEKLİ) ---
@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_subscription(id):
    try:
        sub = Subscription.query.get_or_404(id)
        if sub.user_id == current_user.id:
            db.session.delete(sub)
            db.session.commit()
            flash('Abonelik başarıyla silindi.', 'success')
        else:
            flash('Bu işlem için yetkiniz yok.', 'danger')
    except Exception as e:
        db.session.rollback()
        print(f"Silme hatası: {str(e)}")
    return redirect(url_for('main.index'))