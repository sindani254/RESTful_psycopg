import psycopg2
import psycopg2.extras

db = 'dbname=flask_api user=postgres password=Soen@30010010 host=localhost'


connection = psycopg2.connect(db)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

create_users_table = "CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username text, password text)"
cursor.execute(create_users_table)


create_items_table = "CREATE TABLE IF NOT EXISTS items (id serial PRIMARY KEY, name text, price real)"
cursor.execute(create_items_table)


connection.commit()
connection.close()
