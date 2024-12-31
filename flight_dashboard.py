# import psycopg2
# from dotenv import load_dotenv
# import os
# import streamlit as st


# load_dotenv()
# # Fetch variables
# # USER = os.getenv("DB_USER")
# # PASSWORD = os.getenv("DB_PASSWORD")
# # HOST = os.getenv("DB_HOST")
# # PORT = os.getenv("DB_PORT")
# # DBNAME = os.getenv("DB_NAME")

# USER = st.secrets["postgresql"]["user"]
# PASSWORD = st.secrets["postgresql"]["password"]
# HOST = st.secrets["postgresql"]["host"]
# PORT = st.secrets["postgresql"]["port"]
# DBNAME = st.secrets["postgresql"]["dbname"]


# # Connect to the database
# class Db:
#     def __init__(self):
#         # server connection to Supabase PostgreSQL
#         try:
#             self.connection = psycopg2.connect(
#                 user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME
#             )
#             self.my_cursor = self.connection.cursor()
#             print("connection successful")
#         except Exception as e:
#             print(f"connection not successful: {e}")

#     def fetch_city_name(self):
#         city = []
#         self.my_cursor.execute(
#             """
#                 SELECT DISTINCT "Destination" FROM "flight-data-3"
#                 UNION
#                 SELECT DISTINCT "Source" FROM "flight-data-3";
#             """
#         )

#         data = self.my_cursor.fetchall()
#         for item in data:
#             city.append(item[0])

#         return city

#     def fetch_all_cities(self, source, destination):
#         if source == destination:
#             return "Source and destination cannot be the same"
#         else:
#             self.my_cursor.execute(
#                 """SELECT "Airline", "Route", "Dep_Time", "Price"
#                    FROM "flight-data-3"
#                    WHERE "Source" = %s AND "Destination" = %s;
#                 """,
#                 (source, destination),
#             )

#         data = self.my_cursor.fetchall()

#         return data

#     def airline_freq(self):
#         airline, freq = [], []
#         self.my_cursor.execute(
#             """SELECT "Airline", COUNT(*)
#                FROM "flight-data-3"
#                GROUP BY "Airline";
#             """
#         )

#         data = self.my_cursor.fetchall()

#         for item in data:
#             airline.append(item[0])
#             freq.append(item[1])

#         return airline, freq
import psycopg2
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
# Fetch variables

USER = st.secrets["postgresql"]["user"]
PASSWORD = st.secrets["postgresql"]["password"]
HOST = st.secrets["postgresql"]["host"]
PORT = st.secrets["postgresql"]["port"]
DBNAME = st.secrets["postgresql"]["dbname"]


# Connect to the database
class Db:
    def __init__(self):
        # Server connection to Supabase PostgreSQL
        try:
            self.connection = psycopg2.connect(
                user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME
            )
            self.my_cursor = self.connection.cursor()
            print("connection successful")
        except Exception as e:
            print(f"connection not successful: {e}")

    def revenue_insights(self):
        self.my_cursor.execute(
            """
            SELECT "Source", "Destination", 
            CASE 
                WHEN SUM("Price") >= 1000000 THEN CONCAT(ROUND(SUM("Price") / 1000000, 2), 'M')
                WHEN SUM("Price") >= 1000 THEN CONCAT(ROUND(SUM("Price") / 1000, 2), 'K')
                ELSE TO_CHAR(SUM("Price"), 'FM9999999999999.00')  -- Added proper formatting for non-metric numbers
            END AS "Formatted_Revenue"
            FROM "flight-data-3"
            GROUP BY "Source", "Destination"
            ORDER BY SUM("Price") DESC;

            """
        )
        data = self.my_cursor.fetchall()
        return data

    def highest_revenue_airline(self):
        self.my_cursor.execute(
            """
         SELECT "Airline", 
       CASE 
           WHEN SUM("Price") >= 1000000 THEN CONCAT(ROUND(SUM("Price") / 1000000, 2), 'M')
           WHEN SUM("Price") >= 1000 THEN CONCAT(ROUND(SUM("Price") / 1000, 2), 'K')
           ELSE TO_CHAR(SUM("Price"), 'FM9999999999999.00')  -- Proper formatting for non-metric numbers
       END AS "Formatted_Revenue"
       FROM "flight-data-3"
       GROUP BY "Airline"
       ORDER BY SUM("Price") DESC
       LIMIT 5;

            """
        )
        data = self.my_cursor.fetchall()
        return data

    def top_revenue_source_cities(self):
        self.my_cursor.execute(
            """
           SELECT "Source",
       CASE 
           WHEN SUM("Price") >= 1000000 THEN CONCAT(ROUND(SUM("Price") / 1000000, 2), 'M')
           WHEN SUM("Price") >= 1000 THEN CONCAT(ROUND(SUM("Price") / 1000, 2), 'K')
           ELSE TO_CHAR(SUM("Price"), 'FM9999999999999.00')  -- Formatting for non-metric numbers
       END AS "Total_Revenue"
       FROM "flight-data-3"
       WHERE "Price" IS NOT NULL
       GROUP BY "Source"
    

            """
        )
        data = self.my_cursor.fetchall()
        return data

    def top_revenue_destination_cities(self):
        self.my_cursor.execute(
            """
          SELECT "Destination",
       CASE 
           WHEN SUM("Price") >= 1000000 THEN CONCAT(ROUND(SUM("Price") / 1000000, 2), 'M')
           WHEN SUM("Price") >= 1000 THEN CONCAT(ROUND(SUM("Price") / 1000, 2), 'K')
           ELSE TO_CHAR(SUM("Price"), 'FM9999999999999.00')  -- Formatting for non-metric numbers
       END AS "Total_Revenue"
       FROM "flight-data-3"
       GROUP BY "Destination"
            """
        )
        data = self.my_cursor.fetchall()
        return data

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
                """
                SELECT "Airline", "Route", "Dep_Time", "Price"
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
            """
            SELECT "Airline", COUNT(*)
            FROM "flight-data-3"
            GROUP BY "Airline";
            """
        )

        data = self.my_cursor.fetchall()

        for item in data:
            airline.append(item[0])
            freq.append(item[1])

        return airline, freq

    def busiest_routes(self):
        self.my_cursor.execute(
            """
            SELECT "Source", "Destination", COUNT(*) AS Total_flights
            FROM "flight-data-3"
            GROUP BY "Source", "Destination"
            ORDER BY Total_flights DESC;
            """
        )
        data = self.my_cursor.fetchall()

        return data

    def seasonal_trends_monthly(self):
        self.my_cursor.execute(
            """
            SELECT TO_CHAR("Date_of_Journey"::DATE, 'Month') AS "Month", COUNT(*) AS "Total_Flights"
            FROM "flight-data-3"
            WHERE "Date_of_Journey" IS NOT NULL
            GROUP BY TO_CHAR("Date_of_Journey"::DATE, 'Month'),
                     TO_CHAR("Date_of_Journey"::DATE, 'MM')
            ORDER BY TO_CHAR("Date_of_Journey"::DATE, 'MM'); 
            """
        )
        data = self.my_cursor.fetchall()

        return data

    def seasonal_trends_yearly(self):
        self.my_cursor.execute(
            """
            SELECT 
                CASE 
                    WHEN EXTRACT(MONTH FROM TO_DATE("Date_of_Journey", 'YYYY-MM-DD')) IN (12, 1, 2) THEN 'Winter'
                    WHEN EXTRACT(MONTH FROM TO_DATE("Date_of_Journey", 'YYYY-MM-DD')) IN (3, 4, 5) THEN 'Spring'
                    WHEN EXTRACT(MONTH FROM TO_DATE("Date_of_Journey", 'YYYY-MM-DD')) IN (6, 7, 8) THEN 'Summer'
                    ELSE 'Fall' 
                END AS "Season", 
                COUNT(*) AS "Total_Flights"
            FROM "flight-data-3"
            GROUP BY "Season"
            ORDER BY "Total_Flights" DESC;
            """
        )
        data = self.my_cursor.fetchall()

        return data
