from __future__ import annotations
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)  # Netflix, Spotify vs.
    price = db.Column(db.Float, nullable=False)      # 149.99 gibi
    currency = db.Column(db.String(10), default='TL')# TL, USD, EUR
    billing_cycle = db.Column(db.String(20), default='Aylık') # Aylık / Yıllık
    next_billing_date = db.Column(db.Date, nullable=False) # Sonraki ödeme tarihi
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # Kullanıcı ile ilişki kuruyoruz
    user = db.relationship('User', backref=db.backref('subscriptions', lazy=True))

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Kategori ile abonelikler arasındaki ilişki
    subscriptions = db.relationship('Subscription', backref='category', lazy=True)

    @staticmethod
    def insert_default_categories():
        # İlk başta sistemde hazır bulunacak kategoriler
        default_categories = ['Eğlence', 'Eğitim', 'Yazılım/Araçlar', 'Sağlık/Spor', 'Diğer']
        for name in default_categories:
            category = Category.query.filter_by(name=name).first()
            if category is None:
                category = Category(name=name)
                db.session.add(category)
        db.session.commit()        