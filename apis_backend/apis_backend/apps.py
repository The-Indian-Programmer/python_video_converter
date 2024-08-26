# apis_backend/apps.py
from django.apps import AppConfig

class MyApiConfig(AppConfig):
    name = 'apis_backend'
    migration_module = 'apis_backend.db.migrations'

