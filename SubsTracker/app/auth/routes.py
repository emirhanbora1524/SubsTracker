from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import auth
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Hatalı kısım burasıydı, '/' yaparak düzelttik:
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Tebrikler, başarıyla kayıt oldunuz! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Kayıt Ol', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Burayı da güvene aldık:
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Geçersiz e-posta veya şifre.', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = '/'
            
        return redirect(next_page)
    return render_template('auth/login.html', title='Giriş Yap', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect('/')