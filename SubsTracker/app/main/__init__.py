"""
app/main/__init__.py — Main Blueprint

Ana sayfa, dashboard ve genel route'ları barındırır.
"""

from flask import Blueprint

main = Blueprint("main", __name__)

from app.main import routes  
