import psycopg2
import time

# Espera a que el servicio de PostgreSQL esté listo
time.sleep(10)

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    host="scraping_postgres_v2", #172.22.0.9
    database="scraping_db",
    user="scraping_user",
    password="scraping_password",
    port="5432"
)

# Función para insertar datos de prueba en la base de datos
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
