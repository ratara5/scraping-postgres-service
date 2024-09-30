import psycopg2
import time

# Wait for PostgreSQL ready
time.sleep(10)

# Connection to DB configuration
conn = psycopg2.connect(
    host="scraping_postgres_v2",
    database="scraping_db",
    user="scraping_user",
    password="scraping_password",
    port="5432"
)

# Insert test data to database function
def insert_test_data():
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_data (name, value) VALUES ('Raymond', 100)")
    conn.commit()
    cursor.close()

# Ejecuta la función
insert_test_data()

print("Datos insertados con éxito.")

# Cierra la conexión
conn.close()
