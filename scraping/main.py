import os
from dotenv import load_dotenv

import psycopg2
from psycopg2 import sql
from datetime import datetime, date
from dateutil import relativedelta

from utils import bimester, validate_day
from get_week_assignments import new_discuss


current_month = date.today().month
current_year = date.today().year
# e.g bimester = ['julio', 'agosto']

next_bimester = bimester.get_next_bimester(current_month)

if current_month in [10, 12]:
    year = current_year + relativedelta(years=1)
else:
    year = current_year
# e.g year = '2024'


# data = new_discuss.get_week_assignments('2024', ['julio', 'agosto'])
data = new_discuss.get_week_assignments(str(year), next_bimester)

load_dotenv('../../.env')
'''
conn = psycopg2.connect(database=os.getenv('DB_NAME'),
                        host=os.getenv('DB_HOST'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'),
                        port=os.getenv('DB_PORT'))
'''
'''
conn = psycopg2.connect(database='machado-ayfm',
                        host='127.0.0.1',
                        user='user',
                        password='password',
                        port='5432')
'''
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'), # my_postgres_container es un contenedor sincronizado (hecho en la terminal y de borrado automático) #"scraping_postgres_v2" es el container creado a partir de la imagen de este docker-compose
    database=os.getenv('DB_NAME'), # scraping_db es una base de datos vacía para pruebas. machado-ayfm es una base de datos NUEVA que reemplazará a machado-ayfm de proyecto compose de machadostudents hasta el 9302024
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)

# Al conectarse con la bd del proyecto machadostudents
# DB_NAME=machado-ayfm
# DB_USER=user
# DB_PASS=password

cursor = conn.cursor()

# cursor.execute("SELECT * FROM students")
# print(cursor.fetchone())

# WARNING: TO see results here. new_discuss.get_week_Assignments must return weeksprogram_object. Musn't return pretty_weeksprogram_object
# Iter data and make inserts
for week in data["bimestral_program"]:
    
    # Extract thursday date and convert it to DATE format
    date_value = validate_day.thursday_date(week["weekdays"], year)
    

    # Insert reading
    insert_query = sql.SQL(
        "INSERT INTO readings (date, reading) VALUES ({}, {})"
    ).format(
        sql.Literal(date_value),
        sql.Literal(week["reading"])
    )
    cursor.execute(insert_query)

    # Insert president
    insert_query = sql.SQL(
        "INSERT INTO assignments (section, name, date) VALUES ({}, {}, {})"
    ).format(
        sql.Literal("PRESIDENTE"), #This is the key in week object
        sql.Literal(week["president"]), #"Presidente" is the value for "president" key
        sql.Literal(date_value)
    )
    cursor.execute(insert_query)

    for section in week["sections"]:

        for assignment in section["assignments"]:
            # Insert in "Assignments" table
            insert_query = sql.SQL(
                "INSERT INTO assignments (section, name, date) VALUES ({}, {}, {})"
            ).format(
                sql.Literal(section["section"]),
                sql.Literal(assignment),
                sql.Literal(date_value)
            )
            cursor.execute(insert_query)
    
    # Insert final prayer
    insert_query = sql.SQL(
        "INSERT INTO assignments (section, name, date) VALUES ({}, {}, {})"
    ).format(
        sql.Literal("ORACIÓN FINAL"), #This is the key in week object
        sql.Literal(week["final_prayer"]), #"Oración final" is the value for "final_prayer" key
        sql.Literal(date_value)
    )
    cursor.execute(insert_query)

# Confirm changes and close connection
conn.commit()
cursor.close()
conn.close()
