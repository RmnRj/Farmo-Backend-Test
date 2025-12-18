from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
tables = cursor.fetchall()
for table in tables:
    print(table[0])
