# Бенчмарк "4 queries" #

## О бенчмарке ##

Данный бенчмарк измеряет время работы 5 библиотек на одних и тех же данных, связанных с базой данных такси. Измерение ведётся на исполнении 4 запросов.

## Описание библиотек ##

### psycopg2 ###
Данная библиотека работает с сервером в pgAdmin и является наиболее популярной для использования с PostgreSQL базами данных. Позволяет работать с базами многопоточно.

Реализация запросов:
  1. Импорт библиотеки (pip install psycopg2 в терминале, затем import psycopg2)
  2. Подключение к серверу
  3. Создание курсора
  4. Выполнение запросов

``` python
import psycopg2
conn = psycopg2.connect(
            host = host, 
            user = user, 
            password = password, 
            database = database
            )

with connection.cursor() as cursor:
################################
cursor.execute(query)
################################
conn.close()
```

### SQLite ###
SQLite - кроссплатформенная библиотека, работающая с файлами ``` .db ```, т.е. локально. Может работать на разных системах и платформах.

Реализация запросов:
1. Импорт библиотеки (как правило install делать без надобности, она часто уже установлена, import sqlite3)
2. Подключение к файлу
4. Выполнение запросов через курсор

```python
import sqlite3
con = sq.connect(pathDB)
cursor = con.cursor()
#################################
cursor.execute(query)
#################################
cursor.close()
if con:
    con.close()
```

### Pandas ###
Pandas -  оптимизированная библиотека, предназначенная для обработки и анализа данных. Позволяет очень легко манипулировать большим объемом данных, что обеспечивает гибкость и скорость работы данной библиотеки.

Реализация запросов:
1. Импорт нужных библиотек и функций (нужен еще и sqlalchemy)
2. Создание движка на основе сервера
3. Выполнение запросов

``` python
import pandas
from sqlalchemy import create_engine
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
#############################
pd.read_sql(query, con=engine)
#############################
engine.dispose()
```

### SQLAlchemy ###
SQLAlchemy - библиотека, позволяющая работать с базами данных при помощи ORM (Object Relational Mapper). Она позволяет работать с ООП (классами) и выполнять запросы не зависимо от SQL - многие SQL запросы реализованы через функции. Хотя и обычные SQL запросы тоже приветствуются и можно пользоваться ими.

Реализация запросов:
1. Подключение библиотеки
2. Создание движка на основе сервера
3. Подключение к серверу через движок
4. Выполнение запросов

``` python
import sqlalchemy
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
connection = engine.connect()
###########################
connection.execute(text(query))
###########################
if connection:
    connection.close()
engine.dispose()
```

### DuckDB ###
DuckDB - самая быстрая библиотека из тестированных, для работы использует файлы `.db` и является реляционной СУБД. Библиотека создана, чтобы работать с большими базами данных с одним потоком. Её не стоит использовать на серверах с множеством обращений за раз.

Реализация запросов:
  1. Импорт библиотеки
  2. Подключение к файлу `.db`
  3. Через курсор выполнить нужные запросы к базе данных

``` python
import duckdb
dck.execute("INSTALL sqlite")
connection = dck.connect(pathDB)
with connection.cursor() as cursor:
##################################
cursor.execute(query)
##################################
if connection:
connection.close()
```

### Инструкция к запуску ###

В файле "config.py" поменять значения переменных `host` (имя хоста в pgadmin), `user` (имя пользователя в pgadmin), `password` (пароль от пользователя в pgadmin), `db_name` (название базы данных в pgadmin), `port` (порт в pgadmin, по умолчанию 5432), `name_table` (имя таблицы в базах данных), `pathDB` (путь к файлу `.db`. Если файл не существует, то он создастся, если существует, то останется таким же), `bigCsvPath` (путь к большому файлу с расширением `.csv`), `pathCSVTiny` (путь к маленькому файлу с расширением `.csv`). По умолчанию создается файл .db и таблица в pgAdmin на маленьком файле. При запуске программы база данных в pgadmin (PostgreSQL) уже должна существовать.
Выбор запуска библиотек для теста происходит через соответствующие переменные, изменяя их значение на `True` (запускать) или `False` (не запускать).
Через интерпретатор запускать файл `main.py`, используя версию python 3.10.0.
Все материалы работы можно посмотреть на [гугл диске] (https://drive.google.com/drive/folders/1reglmy0N92TyGp4_F_4WD3aFxswICEaX)

## Впечатления от библиотек ##

### psycopg2 ###

Работа с библиотекой не вызвала трудностей. При вводе в Интернете "psycopg2" превой же ссылкой предлагается сайт с документацией данной библеотеки и примерами корректного использования. Всё четко и понятно. Это библиотека, позволяющая легко и быстро выполнять различные действия в Python или pgAdmin. При этом, загрузка в `Postgres` происходит достаточно долго по сравнению с работой `SQLite`. Требует предварительной настройки.

### SQLite ###

Самая медленная библиотека по результатам тестов. Синтаксис практически не отличается от некоторых других библиотек таких как psycopg2 и DuckDB. При работе с библиотекой возникла проблема в создании запроса, а именно: библиотека не понимала функции `EXTRACT`, из-за чего в запросах 3 и 4 пришлось заменить данную функцию на `STRFTIME`. Запросы в других библиотеках:
``` SQL
SELECT "passenger_count", EXTRACT(year FROM "tpep_pickup_datetime"), COUNT(*)
    FROM "TaxiDB" GROUP BY 1, 2;
```
``` SQL 
SELECT "passenger_count", EXTRACT(year FROM "tpep_pickup_datetime"), ROUND("trip_distance"), COUNT(*)
    FROM "TaxiDB" GROUP BY 1, 2, 3 ORDER BY 2, 4 DESC;
```
Запросы в `sqlite3`:
``` SQL
SELECT "passenger_count", STRFTIME('%Y', "tpep_pickup_datetime"), COUNT(*)
    FROM "TaxiDB" GROUP BY 1, 2;
```
``` SQL
SELECT "passenger_count", STRFTIME('%Y', "tpep_pickup_datetime"), ROUND("trip_distance"), COUNT(*)
    FROM "TaxiDB" GROUP BY 1, 2, 3 ORDER BY 2, 4 DESC;
```

### Pandas ###

Проблем при использовании не возникло. 

### SQLAlchemy ###

При использовании этой библиотеки проблем не возникло, в документации все описано.

### DuckDB ###

При ее использовании возникло несколько трудностей. Прежде всего, библиотека не устанавливалась падая с ошибкой на этапе загрузки. Эту проблему удалось решить, перейдя на версию `python` 3.10.0 с 3.12.0. После установки появилась новая проблема. Нужно было установить расширение "sqlite", ошибка в терминале подсказывала, что стоит попробовать написать ```INSTALL sqlite```, но куда именно было непонятно. Оказалось, нужно было просто сделать duckdb.execute("INSTALL sqlite") перед подключением. Самая быстрая библиотека по итогу исследования.


## Сравнение времени работы библиотек ##
![Графики сравнения времени](https://github.com/Artv1d/BENCHMARK/blob/main/diagram.png)

Дольше всех отрабатывал Sqlite3, а быстрее Duckdb. 4 запрос оказался самым долгим и потратил достаточно времени у всех библиотек. 

</br>Скорость выполнения запросов в различных библиотеках может зависеть от нескольких факторов:

* **_</ins>Тип базы данных:</ins>_**
</br>Некоторые библиотеки могут быть оптимизированы для работы с определенными типами баз данных. Например, `DuckDB` специализируется на аналитических запросах, поэтому показывает высокую производительность при выполнении сложных аналитических запросов. В то время как библиотеки, такие как `Psycopg2` и `SQLAlchemy`, являются более универсальными, что может повлиять на скорость выполнения запросов в зависимости от конкретной базы данных.

* **_</ins>Объем входных данных:</ins>_**
</br>Скорость выполнения запросов также зависит от объема данных, но, к сожалению в силу технических причин в моей работе реализована работа только с меньшей базой данных.

* **_</ins>Оптимизация запросов:</ins>_**
</br>Эффективность выполнения запросов может зависеть от того, насколько хорошо запросы оптимизированы. Например, использование индексов, правильная структура таблиц и грамотные запросы могут существенно повлиять на скорость выполнения запросов.

* **_</ins>Уровень оптимизации и сложности библиотеки:</ins>_**
</br>Некоторые библиотеки могут быть более оптимизированы и эффективны в своей работе, в то время как другие могут предлагать больше функций, что сказывается на скорости выполнения запросов.
