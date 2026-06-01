import os


class Config:
    """Tüm yapılandırma sınıflarının paylaştığı temel ayarlar."""

    # Güvenlik
    SECRET_KEY = os.environ.get("SECRET_KEY", "gelistirme-icin-gecici-anahtar")
    WTF_CSRF_ENABLED = True

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///substacker.db"
    )

    @staticmethod
    def init_app(app):
        """Alt sınıfların ihtiyaç duyduğunda genişletebileceği init kancası."""
        pass


class DevelopmentConfig(Config):
    """Geliştirme ortamı — debug aktif, SQLite."""

    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Üretim ortamı — debug kapalı."""

    DEBUG = False
    TESTING = False

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        # Üretimde ek güvenlik/logging adımları buraya eklenecek.


class TestingConfig(Config):
    """Test ortamı — bellek içi veritabanı."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False  # Testlerde CSRF'yi devre dışı bırak


# Factory fonksiyonundan isimle seçmek için kullanılan sözlük
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
