import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Farmo.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;')
print("All tables dropped successfully")
