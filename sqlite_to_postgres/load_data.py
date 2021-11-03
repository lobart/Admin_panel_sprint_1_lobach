import io
import sqlite3
import sys
import traceback

import uuid
from dataclasses import dataclass, fields, astuple
from datetime import datetime

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

ClassToTablesNames = { 'FilmWork' : 'film_work',
                       'Genre' : 'genre',
                       'GenreFilmWork' : 'genre_film_work',
                       'Person' : 'person',
                       'PersonFilmWork' : 'person_film_work',
                     }
N = 10


@dataclass
class FilmWork:
    __slots__ = ('id','title', 'description', 'creation_date', 'certificate', 'file_path', 'rating', 'type',
                 'created_at', 'updated_at')
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: datetime.timestamp
    updated_at: datetime.timestamp


@dataclass(frozen=True)
class Genre:
    __slots__ = ('id', 'name', 'description', 'created_at', 'updated_at')
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime.timestamp
    updated_at: datetime.timestamp

@dataclass(frozen=True)
class GenreFilmWork:
    __slots__ = ('id','film_work_id', 'genre_id', 'created_at')
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime.timestamp

@dataclass(frozen=True)
class Person:
    __slots__ = ('id','full_name', 'birth_date', 'created_at', 'updated_at')
    id: uuid.UUID
    full_name: str
    birth_date: str
    created_at: datetime.timestamp
    updated_at: datetime.timestamp


@dataclass(frozen=True)
class PersonFilmWork:
    __slots__ = ('id', 'film_work_id', 'person_id', 'role', 'created_at')
    id: str
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime.timestamp

class SQLiteLoader:
    def __init__(self, connection):
        self.connection = connection
    def load_movies(self):
        movies = dict()
        try:
            cursor = self.connection.cursor()
            movies['film_work'] = []
            movies['genre'] = []
            movies['genre_film_work'] = []
            movies['person'] = []
            movies['person_film_work'] = []

            for row in cursor.execute('SELECT * FROM film_work'):
                movies['film_work'].append(FilmWork(*row))
            for row in cursor.execute('SELECT * FROM genre'):
                movies['genre'].append(Genre(*row))
            for row in cursor.execute('SELECT * FROM genre_film_work'):
                movies['genre_film_work'].append(GenreFilmWork(*row))
            for row in cursor.execute('SELECT * FROM person'):
                movies['person'].append(Person(*row))
            for row in cursor.execute('SELECT * FROM person_film_work'):
                movies['person_film_work'].append(PersonFilmWork(*row))

            return movies
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))



def clean_csv_value(value) -> str:
    if value is None:
        return r'\N'
    return str(value).replace('\n', '\\n')

class PostgresSaver:

    def __init__(self, connection):
        self.connection = connection

    def save_all_data(self, data):
        if len(data) == 0:
            print("Error data is Empty!")
            return
        for k in data:
            self.save_table_data(data[k],k)



    def save_table_data(self, data, column):
            j = 0
            for i in range(len(data)):
                CSV = io.StringIO()
                CSV.write('|'.join(map(clean_csv_value, (
                   astuple(data[i])
                ))) + '\n' )
                CSV.seek(0)
                j = j + 1
                if j == N:
                    with self.connection.cursor() as cursor:
                        try:
                            cursor.copy_from(CSV, column, sep='|', columns=[*data[0].__slots__])
                        except psycopg2.errors.UniqueViolation as er:
                            print("Error when copy_from: %s" % (er))
                            self.connection.rollback()
                    j = 0




def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'postgres', 'password': 1234, 'host': '127.0.0.1', 'port': 5432,
           'options': '-c search_path=content'}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
