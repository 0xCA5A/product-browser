# -*- coding: utf-8 -*-

import json
import uuid
from datetime import datetime

from flask import Flask
from flask_restful_hal import Api, Embedded, Link, Resource


class Product:
    def __init__(self, name):
        self.product_id = uuid.uuid4()
        self.name = name


class ProductEncoder(json.JSONEncoder):
    def default(self, obj):
        return {"product_id": obj.product_id.hex, "name": obj.name}


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class Environment:
    def __init__(self, name, product_id):
        self.environment_id = uuid.uuid4()
        self.name = name
        self.product_id = product_id


PRODUCT_1 = Product("BlueMedication")
PRODUCT_1_ENVIRONMENTS = [Environment("INT", PRODUCT_1.product_id), Environment("STA", PRODUCT_1.product_id)]
PRODUCT_2 = Product("Remedi")
PRODUCT_2_ENVIRONMENTS = [Environment("INT", PRODUCT_2.product_id), Environment("STA", PRODUCT_2.product_id)]
PRODUCT_3 = Product("Rezeptanfrage")
PRODUCT_3_ENVIRONMENTS = [Environment("DEV", PRODUCT_3.product_id), Environment("INT", PRODUCT_3.product_id),
                          Environment("STA", PRODUCT_3.product_id), Environment("QA", PRODUCT_3.product_id)]

PRODUCTS = {
    PRODUCT_1: PRODUCT_1_ENVIRONMENTS,
    PRODUCT_2: PRODUCT_2_ENVIRONMENTS,
    PRODUCT_3: PRODUCT_3_ENVIRONMENTS
}


class Todo(Resource):
    @staticmethod
    def data(todo):
        # return TODOS[todo]
        return '{}'


class Random(Resource):
    def get(self):
        return {
            "timestamp": str(datetime.now()),
            "random": str(uuid.uuid4())
        }, 200


class TodoList2(Resource):
    def pre_hal(self, embed, include_links, todo):
        self.todos = PRODUCTS

    def data(self):
        return {'size': len(self.todos)}

    def embedded(self):
        arguments_list = [(todo,) for todo in sorted(self.todos.keys())]
        return Embedded('items', Todo, *arguments_list)

    def links(self):
        arguments_list = [('/todos/{}'.format(todo), {'title': todo}) for todo in sorted(self.todos.keys())]
        return Link('items', *arguments_list)


class Products(Resource):
    @staticmethod
    def data():
        # return {'size': len(PRODUCTS)}
        # return PRODUCTS

        x = json.dumps(PRODUCT_1, cls=ProductEncoder)
        # x = json.dumps(PRODUCT_1)
        # x = json.dumps(PRODUCTS)

        print(x)

        return x

    @staticmethod
    def embedded():
        arguments_list = [(product,) for product in sorted(PRODUCTS.keys())]
        return Embedded('items', Todo, *arguments_list)

    @staticmethod
    def links():
        arguments_list = [('/products/{}'.format(product), {'title': product}) for product in sorted(PRODUCTS.keys())]
        return Link('items', *arguments_list)


app = Flask(__name__)
api = Api(app)
# api.add_resource(Todo, '/todos/<todo>')
api.add_resource(Todo, '/todos/<todo>')
api.add_resource(Products, '/api/products')

api.add_resource(Random, "/randoms")

app.run()
