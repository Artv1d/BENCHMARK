from config import *
import funcs

funcs.load_db()
if Psycpog2: print('Psycopg2 times:', *funcs.Psycopg2Queries())
if SQLite3: print('SQLite3 times:', *funcs.SQLiteQueries())
if Pandas: print('Pandas times:', *funcs.PandasQueries())
if SQLAlchemy: print('SQLAlchemy times:', *funcs.SQLAlchemyQueries())
if DuckDB: print('DuckDB times:', *funcs.DuckDBQueries())