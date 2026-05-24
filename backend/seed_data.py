import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'terrasync_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from ingestion.models import Tenant

User = get_user_model()

def seed():
    # 1. Create Default Tenant
    tenant_name = "Breathe ESG Live"
    tenant, created = Tenant.objects.get_or_create(name=tenant_name)
    if created:
        print(f"Created Tenant: {tenant_name} (ID: {tenant.id})")
    else:
        print(f"Tenant '{tenant_name}' already exists (ID: {tenant.id})")

    # 2. Create Superuser
    username = os.getenv('ADMIN_USERNAME', 'admin')
    email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    password = os.getenv('ADMIN_PASSWORD', 'admin123')

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Created Superuser: {username}")
    else:
        print(f"Superuser '{username}' already exists")

if __name__ == '__main__':
    seed()
