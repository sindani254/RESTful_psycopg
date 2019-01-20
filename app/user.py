import psycopg2
import psycopg2.extras
from flask_restful import Resource, reqparse

db = 'dbname=flask_api user=postgres password=Soen@30010010 host=localhost'


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = psycopg2.connect(db)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=%s"
        cursor.execute(query, (username,))
        row = cursor.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = psycopg2.connect(db)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=%s"
        cursor.execute(query, (_id,))
        row = cursor.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username field cannot be left blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password field cannot be left blank"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"error:": "username '{}' already in use!".format(data['username'])}

        connection = psycopg2.connect(db)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (data['username'], data['password'],))

        connection.commit()
        connection.close()

        return {"message": "a/c created successfully"}, 201
