from pony.orm import Database, Required, Json, IntArray
from decouple import config

db = Database()
db.bind(
    provider='postgres', user=config('user'),
    password=config('password'), host='localhost',
    port='32700',
    database=config('database')
)


class Sites(db.Entity):
    name = Required(str, unique=True)
    address = Required(str, unique=True)
    password = Required(str)
    users = Required(IntArray)


class Answers(db.Entity):
    site_name = Required(str)
    data = Required(Json, unique=True)
    typ = Required(str)


db.generate_mapping(create_tables=True)
