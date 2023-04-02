from flask import Flask
from flask_restful_hal import Api, Embedded, Link, Resource

from productmonitor.model.todo import Todo

TODOS = {
    'todo1': {
        'task': 'build an API'
    },
    'todo2': {
        'task': '?????'
    },
    'todo3': {
        'task': 'profit!'
    },
}




class TodoList(Resource):
    @staticmethod
    def data():
        return {'size': len(TODOS)}

    @staticmethod
    def embedded():
        arguments_list = [(todo, ) for todo in sorted(TODOS.keys())]
        return Embedded('items', Todo, *arguments_list)

    @staticmethod
    def links():
        arguments_list = [('/todos/{}'.format(todo), {'title': todo}) for todo in sorted(TODOS.keys())]
        return Link('items', *arguments_list)


# class TodoList(Resource):
#     def pre_hal(self, embed, include_links, todo):
#         self.todos = db.query(...)
#
#     def data(self):
#         return {'size': len(self.todos)}
#
#     def embedded(self):
#         arguments_list = [(todo, ) for todo in sorted(self.todos.keys())]
#         return Embedded('items', Todo, *arguments_list)
#
#     def links(self):
#         arguments_list = [('/todos/{}'.format(todo), {'title': todo}) for todo in sorted(self.todos.keys())]
#         return Link('items', *arguments_list)


app = Flask(__name__)
api = Api(app)
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo>')
app.run(debug=True)