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
# e.g year = 2024


data = new_discuss.get_week_assignments(str(year), next_bimester)

load_dotenv('../../.env')


conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'), # my_postgres_container is a sychronized container (created in terminal and automatized deleted) #"DB_HOST" is created container from image in this docker-compose.yaml
    database=os.getenv('POSTGRES_DB'), # scraping_db is a empty database for test. "DB-NAME" is a NEW database to replace the database for machadostudents compose project at 9302024
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    port=os.getenv('POSTGRES_PORT')
)

cursor = conn.cursor()


# WARNING: To see results here. new_discuss.get_week_assignments must return weeksprogram_object. Musn't return pretty_weeksprogram_object
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
