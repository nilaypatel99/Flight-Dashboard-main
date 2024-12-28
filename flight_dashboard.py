import psycopg2
from dotenv import load_dotenv
import os
import streamlit as st


load_dotenv()
# Fetch variables
# USER = os.getenv("DB_USER")
# PASSWORD = os.getenv("DB_PASSWORD")
# HOST = os.getenv("DB_HOST")
# PORT = os.getenv("DB_PORT")
# DBNAME = os.getenv("DB_NAME")

USER = st.secrets["postgresql"]["user"]
PASSWORD = st.secrets["postgresql"]["password"]
HOST = st.secrets["postgresql"]["host"]
PORT = st.secrets["postgresql"]["port"]
DBNAME = st.secrets["postgresql"]["dbname"]


# Connect to the database
class Db:
    def __init__(self):
        # server connection to Supabase PostgreSQL
        try:
            self.connection = psycopg2.connect(
                user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME
            )
            self.my_cursor = self.connection.cursor()
            print("connection successful")
        except Exception as e:
            print(f"connection not successful: {e}")

    def fetch_city_name(self):
        city = []
        self.my_cursor.execute(
            """
SELECT DISTINCT "Destination" FROM "flight-data-3"
UNION
SELECT DISTINCT "Source" FROM "flight-data-3";
"""
        )

        data = self.my_cursor.fetchall()
        for item in data:
            city.append(item[0])

        return city

    def fetch_all_cities(self, source, destination):
        if source == destination:
            return "Source and destination cannot be the same"
        else:
            self.my_cursor.execute(
                """SELECT "Airline", "Route", "Dep_Time", "Price"
FROM "flight-data-3"
WHERE "Source" = %s AND "Destination" = %s;
""",
                (source, destination),
            )

        data = self.my_cursor.fetchall()

        return data

    def airline_freq(self):
        airline, freq = [], []
        self.my_cursor.execute(
            """SELECT "Airline", COUNT(*)
FROM "flight-data-3"
GROUP BY "Airline";
"""
        )

        data = self.my_cursor.fetchall()

        for item in data:
            airline.append(item[0])
            freq.append(item[1])

        return airline, freq
