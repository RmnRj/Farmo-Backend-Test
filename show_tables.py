import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Farmo.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
tables = cursor.fetchall()
print("\nDatabase Tables:")
for table in tables:
    print(f"  - {table[0]}")
