"""
app/auth/forms.py — Kimlik Doğrulama Formları (Flask-WTF)

Formlar:
  - RegistrationForm : Yeni kullanıcı kaydı
  - LoginForm        : Kullanıcı girişi
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


# =============================================================================
# RegistrationForm — Kayıt Formu
# =============================================================================

class RegistrationForm(FlaskForm):
    """
    Yeni kullanıcı kaydı formu.

    Özel validasyonlar:
      - validate_username : Kullanıcı adının DB'de benzersiz olduğunu kontrol eder.
      - validate_email    : E-posta adresinin DB'de benzersiz olduğunu kontrol eder.
    """

    username = StringField(
        "Kullanıcı Adı",
        validators=[
            DataRequired(message="Kullanıcı adı zorunludur."),
            Length(min=3, max=80, message="Kullanıcı adı 3-80 karakter arasında olmalıdır."),
        ],
    )

    email = EmailField(
        "E-posta Adresi",
        validators=[
            DataRequired(message="E-posta adresi zorunludur."),
            Email(message="Geçerli bir e-posta adresi giriniz."),
        ],
    )

    password = PasswordField(
        "Şifre",
        validators=[
            DataRequired(message="Şifre zorunludur."),
            Length(min=6, message="Şifre en az 6 karakter olmalıdır."),
        ],
    )

    password_confirm = PasswordField(
        "Şifre Tekrar",
        validators=[
            DataRequired(message="Şifre tekrarı zorunludur."),
            EqualTo("password", message="Şifreler eşleşmiyor."),
        ],
    )

    submit = SubmitField("Kayıt Ol")

    # --- Özel DB Validasyonları ---

    def validate_username(self, field: StringField) -> None:
        """
        Girilen kullanıcı adının veritabanında kayıtlı olup olmadığını kontrol eder.
        WTForms bu metodu form doğrulama sırasında otomatik olarak çağırır.
        """
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            raise ValidationError("Bu kullanıcı adı zaten alınmış. Lütfen başka bir ad seçin.")

    def validate_email(self, field: EmailField) -> None:
        """
        Girilen e-posta adresinin veritabanında kayıtlı olup olmadığını kontrol eder.
        WTForms bu metodu form doğrulama sırasında otomatik olarak çağırır.
        """
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError("Bu e-posta adresi zaten kayıtlı. Giriş yapmayı deneyin.")


# =============================================================================
# LoginForm — Giriş Formu
# =============================================================================

class LoginForm(FlaskForm):
    """Mevcut kullanıcı giriş formu."""

    email = EmailField(
        "E-posta Adresi",
        validators=[
            DataRequired(message="E-posta adresi zorunludur."),
            Email(message="Geçerli bir e-posta adresi giriniz."),
        ],
    )

    password = PasswordField(
        "Şifre",
        validators=[
            DataRequired(message="Şifre zorunludur."),
        ],
    )

    remember_me = BooleanField("Beni Hatırla")

    submit = SubmitField("Giriş Yap")
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('E-posta', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Şifreyi Onayla', validators=[DataRequired(), EqualTo('password', message='Şifreler eşleşmeli.')])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanıcı adı zaten alınmış.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu e-posta adresi zaten kayıtlı.')

class LoginForm(FlaskForm):
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember_me = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')