"""
app/__init__.py — Application Factory

create_app(config_name) fonksiyonu ile Flask uygulaması oluşturulur.
Tüm Flask eklentileri burada başlatılır ve blueprint'ler kayıt edilir.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from config import config_by_name

# ---------------------------------------------------------------------------
# Eklenti nesneleri — uygulamaya bağlanmadan önce "boş" olarak oluşturulur
# ---------------------------------------------------------------------------
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_name: str = "default") -> Flask:
    """
    Application Factory.

    Args:
        config_name: 'development' | 'production' | 'testing' | 'default'

    Returns:
        Yapılandırılmış Flask uygulama nesnesi.
    """
    app = Flask(__name__)

    # --- Yapılandırma yükle ---
    app.config.from_object(config_by_name[config_name])
    config_by_name[config_name].init_app(app)

    # --- Eklentileri başlat ---
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # LoginManager ayarları
    login_manager.login_view = "auth.login"          # Giriş sayfasının endpoint'i
    login_manager.login_message_category = "warning"  # Flash mesaj kategorisi

    # --- Blueprint'leri kayıt et ---
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    # --- Modelleri içe aktar (Flask-Migrate'in tabloları görmesi için) ---
    from app import models  # noqa: F401
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    return app
