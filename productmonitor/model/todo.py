from flask_restful_hal import Link, Resource


class Todo(Resource):
    @staticmethod
    def data(todo):
        return TODOS[todo]

    @staticmethod
    def links(todo):
        return Link('collection', '/todos')
