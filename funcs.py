from config import *
import os
import sqlalchemy
from time import perf_counter

def load_db():
    df1 = None
    df2 = None
    engine = create_engine(serverPath)
    if db_name not in sqlalchemy.inspect(engine).get_table_names():
        df2 = pd.read_csv(pathCSVTiny)
        df2 = df2.drop(columns=["Airport_fee"])
        df2["tpep_pickup_datetime"] = pd.to_datetime(df2["tpep_pickup_datetime"])
        df2["tpep_dropoff_datetime"] = pd.to_datetime(df2["tpep_dropoff_datetime"])
        df2 = df2.rename(columns={"Unnamed: 0": "ID"})
        df2.to_sql(name_table, engine, if_exists='replace', index=False, chunksize = 1000)
    engine.dispose()

    if not os.path.exists(pathDB):
        df1 = pd.read_csv(pathCSVTiny)
        df1 = df1.drop(columns=["Airport_fee"])
        df1["tpep_pickup_datetime"] = pd.to_datetime(df1["tpep_pickup_datetime"])
        df1["tpep_dropoff_datetime"] = pd.to_datetime(df1["tpep_dropoff_datetime"])
        df1 = df1.rename(columns={"Unnamed: 0": "ID"})
        con = sq.connect(pathDB)
        df1.to_sql(name_table, con, if_exists="replace", index=False, chunksize=1000)
        con.close()

def DuckDBQueries():
    averageTimes = []
    dck.execute("INSTALL sqlite")
    connection = dck.connect(pathDB)
    with connection.cursor() as cursor:
        for query in queries1:
            totalTime = 0
            for _ in range (ATTEMPTS):
                start = perf_counter()
                cursor.execute(query)
                finish = perf_counter()
                totalTime += (finish - start)
            averageTimes.append(totalTime / ATTEMPTS)
    if connection:
        connection.close()
    return averageTimes
def PandasQueries():
    averageTimes = []
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    for query in queries1:
        totalTime = 0
        for _ in range (ATTEMPTS):
            start = perf_counter()
            pd.read_sql(query, con=engine)
            finish = perf_counter()
            totalTime += (finish - start)
        averageTimes.append(totalTime / ATTEMPTS)
    engine.dispose()
    return averageTimes
def Psycopg2Queries():
    averageTimes = []
    connection = psycopg2.connect(
        host = host,
        user = user,
        password = password,
        database = db_name
    )
    with connection.cursor() as cursor:
        for query in queries1:
            totalTime = 0
            for _ in range (ATTEMPTS):
                start = perf_counter()
                cursor.execute(query)
                finish = perf_counter()
                totalTime += (finish - start)
            averageTimes.append(totalTime / ATTEMPTS)
    if connection:
        connection.close()
    return averageTimes
def SQLAlchemyQueries():
    averageTimes = []
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    connection = engine.connect()
    for query in queries1:
        totalTime = 0
        for _ in range (ATTEMPTS):
            start = perf_counter()
            connection.execute(text(query))
            finish = perf_counter()
            totalTime += (finish - start)
        averageTimes.append(totalTime / ATTEMPTS)
    if connection:
        connection.close()
    engine.dispose()
    return averageTimes
def SQLiteQueries():
    averageTimes = []
    con = sq.connect(pathDB)
    cursor = con.cursor()
    for query in queries2:
        totalTime = 0
        for _ in range (ATTEMPTS):
            start = perf_counter()
            cursor.execute(query)
            finish = perf_counter()
            totalTime += (finish - start)
        averageTimes.append(totalTime / ATTEMPTS)
    cursor.close()
    if con:
        con.close()
    return averageTimes