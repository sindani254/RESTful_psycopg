from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList, PostItem


app = Flask(__name__)
app.secret_key = "yule_mguyz"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, '/item/<int:id>')
api.add_resource(ItemList, '/items')
api.add_resource(PostItem, '/item')
api.add_resource(UserRegister, '/signup')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
