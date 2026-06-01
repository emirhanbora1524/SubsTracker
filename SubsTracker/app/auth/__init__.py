"""
app/auth/__init__.py — Auth Blueprint

Kayıt, giriş, çıkış ve şifre sıfırlama route'larını barındırır.
URL ön eki: /auth  (run.py'de tanımlanmıştır)
"""

from flask import Blueprint

auth = Blueprint("auth", __name__)

from app.auth import routes  # noqa: E402, F401
