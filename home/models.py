"""
File models.py utama yang hanya mengimport dari submodules.
Ini untuk menjaga kompatibilitas dengan Django.
"""
# Import semua dari models package
from .models import *

# Django memerlukan ini untuk migration system
# Tidak perlu tambah kode lain di sini