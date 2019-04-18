import psycopg2
import psycopg2.extras
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

db = "dbname='sendit' user='sindani254' password='Soen@30010010' host='localhost'"


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="name field cannot be left blank!"
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="price field cannot be left blank!"
                        )

    @classmethod
    def find_by_id(cls, id):
        connection = psycopg2.connect(db)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "SELECT * FROM items where id=%s"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[1], 'price': row[2]}}
        else:
            return {'message': 'item NOT found'}, 404

    @jwt_required()
    def get(self, id):
        connection = psycopg2.connect(db)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            query = "SELECT * FROM items where id=%s"
            cursor.execute(query, (id,))
        except Exception:
            return {"error msg": "error fetching item details"}, 500
        row = cursor.fetchone()

        if row:
            return {'item': {'name': row[1], 'price': row[2]}}
        return {'message': 'item NOT found'}, 404

    def delete(self, id):
        connection = psycopg2.connect(db)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            query = "DELETE FROM items where id=%s"
            cursor.execute(query, (id,))
        except Exception:
            return {"error msg": "error deleting item"}, 500

        connection.commit()
        connection.close()

        return {'message': 'item deleted'}

    def put(self, id):

        data = Item.parser.parse_args()
        item = self.find_by_id(id)
        updated_item = {'name': data['name'], 'price': data['price']}

        if item is None:
            return {"error message": "item NOT found"}, 404
        else:
            connection = psycopg2.connect(db)
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

            try:
                query = "UPDATE items SET name=%s, price=%s WHERE id=%s"
                cursor.execute(query, (updated_item['name'], updated_item['price'], id))
            except Exception as e:
                return {"update error": "error updating item details"}, 500

            connection.commit()
            connection.close()

            return updated_item


class PostItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="name field cannot be left blank!"
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="price field cannot be left blank!"
                        )

    @classmethod
    def find_by_name(cls, name):
        connection = psycopg2.connect(db)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "SELECT * FROM items where name=%s"
        cursor.execute(query, (name,))
        row = cursor.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[1], 'price': row[2]}}, 200

    @classmethod
    def insert(self, item):
        connection = psycopg2.connect(db)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "INSERT INTO items (name, price) VALUES (%s, %s)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return {'message': 'item inserted successfully'}

    def post(self):
        data = PostItem.parser.parse_args()
        item = {'name': data['name'], 'price': data['price']}

        if self.find_by_name(data['name']):
            return {'message': "item with name '{}' already exists.".format(data['name'])}, 400
        try:
            self.insert(item)
        except Exception as e:
            return {"error msg": e}, 500  # INTERNAL SERVER ERROR

        return item, 201


class ItemList(Resource):
    def get(self):
        items = []

        connection = psycopg2.connect(db)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cursor.execute("SELECT * FROM items ORDER BY id ASC")
            results = cursor.fetchall()
        except Exception as e:
            return {"message": "error fetching items, '{}'".format(e)}, 500

        if results:
            for row in results:
                items.append({'item id': row[0], 'item name': row[1], 'item price': row[2]})
        else:
            return {"error": "0 items found!"}, 404

        return {'items': items}

        connection.close()
