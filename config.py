from sqlalchemy import create_engine, text
import psycopg2
import sqlite3 as sq
import pandas as pd
import duckdb as dck
import pathlib
from pathlib import Path

# Flags to run and number of runs
ATTEMPTS = 20
Psycpog2 = True
SQLite3 = True
Pandas = True
SQLAlchemy = True
DuckDB = True

# Information to connect to PostgreSQL
host = "localhost"  # name of host
port = "5432"  # number of port
user = "postgres"  # name of user
password = "euk721520022201"  # password for PostgreSQL
db_name = "TaxiDB"  # name of database in PostgreSQL

# Information about data
name_table = "TaxiDB" 
nameDBFile = "TaxiDB.db" 
#nameCSVBig = ""
nameCSVTiny = "nyc_yellow_tiny.csv"
folder_with_data = f"C:\pyProjects\Lab3DB_Satykov\data" 

# Additional information
work_path = pathlib.Path.cwd()
#pathCSVBig = Path(work_path, folder_with_data, nameCSVBig)
pathCSVTiny = Path(work_path, folder_with_data, nameCSVTiny)
pathDB = f"{folder_with_data}\{nameDBFile}"
serverPath = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

queries1 = [
    """SELECT "VendorID", COUNT(*)
        FROM "TaxiDB" GROUP BY 1;""",
    """SELECT "passenger_count", AVG("total_amount")
       FROM "TaxiDB" GROUP BY 1;""",
    """SELECT "passenger_count", EXTRACT(year FROM "tpep_pickup_datetime"), COUNT(*)
       FROM "TaxiDB" GROUP BY 1, 2;""",
    """SELECT "passenger_count", EXTRACT(year FROM "tpep_pickup_datetime"), ROUND("trip_distance"), COUNT(*)
       FROM "TaxiDB" GROUP BY 1, 2, 3 ORDER BY 2, 4 DESC;""",
]

queries2 = [
    """SELECT "VendorID", COUNT(*)
        FROM "TaxiDB" GROUP BY 1;""",
    """SELECT "passenger_count", AVG("total_amount")
       FROM "TaxiDB" GROUP BY 1;""",
    """SELECT "passenger_count", STRFTIME('%Y', "tpep_pickup_datetime"), COUNT(*)
       FROM "TaxiDB" GROUP BY 1, 2;""",
    """SELECT "passenger_count", STRFTIME('%Y', "tpep_pickup_datetime"), ROUND("trip_distance"), COUNT(*)
       FROM "TaxiDB" GROUP BY 1, 2, 3 ORDER BY 2, 4 DESC;""",
]