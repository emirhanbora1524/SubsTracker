from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class SubscriptionForm(FlaskForm):
    name = StringField('Platform Adı', validators=[DataRequired(message="Platform adı boş bırakılamaz.")])
    price = FloatField('Ücret', validators=[DataRequired(), NumberRange(min=0, message="Ücret 0'dan küçük olamaz.")])
    currency = SelectField('Para Birimi', choices=[('TL', 'TL ₺'), ('USD', 'USD $'), ('EUR', 'EUR €')])
    billing_cycle = SelectField('Ödeme Döngüsü', choices=[('Aylık', 'Aylık'), ('Yıllık', 'Yıllık')])
    
    
    category_id = SelectField('Kategori', coerce=int, validators=[DataRequired(message="Lütfen bir kategori seçin.")])
    
    next_billing_date = DateField('Sonraki Ödeme Tarihi', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Abonelik Ekle')