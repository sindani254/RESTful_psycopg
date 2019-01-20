import psycopg2
import psycopg2.extras

from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = '@nonymous'
DATABASE_URL = "postgresql://postgres:Soen@30010010@localhost/flask_api"

db = 'dbname=flask_api user=postgres password=Soen@30010010 host=localhost'


def connectToDB():
    connectionString = db
    print(connectionString)
    try:
        return psycopg2.connect(connectionString)
    except Exception as e:
        print("can't connect to database")


@app.route('/users', methods=['GET'])
def get_all_users():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("select * from users")
    except Exception as e:
        return jsonify({"error": "Error executing select"})
    results = cur.fetchall()
    return jsonify({'users list': results})


if __name__ == '__main__':
    app.run(debug=True)
