import uuid
from flask import Flask
from flask_restful_hal import Api, Embedded, Link, Resource

from marshmallow import Schema, fields


class Product:
    def __init__(self, name, environments):
        self.product_id = uuid.uuid4()
        self.name = name
        self.environments = environments


class Environment:
    def __init__(self, name, services):
        self.environment_id = uuid.uuid4()
        self.name = name
        self.services = services


class SpringBootService:
    def __init__(self, name, actuatorInfoUrl, gitlabCommitUrlFormatString):
        self.service_id = uuid.uuid4()
        self.name = name
        self.actuatorInfoUrl = actuatorInfoUrl
        self.gitlabCommitUrlFormatString = gitlabCommitUrlFormatString


class SpringBootServiceSchema(Schema):
    service_id = fields.UUID()
    name = fields.Str()
    actuatorInfoUrl = fields.Str()


wiremockActuatorInfo = "http://localhost:8181/spring/boot/actuator"
gitlabFormatString = "https://gitlab.com/yourcompany/yourproject/commit/{commitId}"

PRODUCTS = [
    Product("Product 1", [
        Environment("Product 1 Environment INT",
                    [SpringBootService("Product 1 Environment INT Service 1", wiremockActuatorInfo, gitlabFormatString),
                     SpringBootService("Product 1 Environment INT Service 2", wiremockActuatorInfo,
                                       gitlabFormatString)]),
        Environment("Product 1 Environment STA",
                    [SpringBootService("Product 1 Environment STA Service 1", wiremockActuatorInfo,
                                       gitlabFormatString)])]),
    Product("Product 2",
            [
                Environment("Product 2 Environment DEV",
                            [SpringBootService("Product 2 Environment DEV Service 1", wiremockActuatorInfo,
                                               gitlabFormatString)]),
                Environment("Product 2 Environment INT",
                            [SpringBootService("Product 2 Environment INT Service 1", wiremockActuatorInfo,
                                               gitlabFormatString)]),
                Environment("Product 2 Environment STA",
                            [SpringBootService("Product 2 Environment STA Service 1", wiremockActuatorInfo,
                                               gitlabFormatString)]),
                Environment("Product 2 Environment QA",
                            [SpringBootService("Product 2 Environment QA Service 1", wiremockActuatorInfo,
                                               gitlabFormatString)])
            ]),
    Product("Product 3",
            [Environment("Product 3 Environment DEV",
                         [SpringBootService("Product 3 Environment DEV Service 1", wiremockActuatorInfo,
                                            gitlabFormatString)]),
             Environment("Product 3 Environment QA",
                         [SpringBootService("Product 3 Environment QA Service 1", wiremockActuatorInfo,
                                            gitlabFormatString),
                          SpringBootService("Product 3 Environment QA Service 2", wiremockActuatorInfo,
                                            gitlabFormatString),
                          SpringBootService("Product 3 Environment QA Service 3", wiremockActuatorInfo,
                                            gitlabFormatString),
                          SpringBootService("Product 3 Environment QA Service 4", wiremockActuatorInfo,
                                            gitlabFormatString)])
             ])
]


# Define the ProductResource class
class ProductResource(Resource):
    @staticmethod
    def data(product_id):
        product = next((p for p in PRODUCTS if str(p.product_id) == product_id), None)
        if product:
            return {
                'product_id': str(product.product_id),
                'name': product.name,
                'environments': [{'environment_id': str(env.environment_id), 'name': env.name} for env in
                                 product.environments]
            }
        return {'message': 'Product not found'}, 404

    @staticmethod
    def links(product_id):
        return Link('self', f'/api/products/{product_id}')


class EnvironmentResource(Resource):
    @staticmethod
    def data(product_id, environment_id):

        environments = []
        for product in PRODUCTS:
            environments.extend(product.environments)

        environment = next((e for e in environments if str(e.environment_id) == str(environment_id)), None)
        if environment:
            return {
                'environment_id': str(environment.environment_id),
                'name': environment.name,
                'services': [{'service_id': str(ser.service_id), 'name': ser.name} for ser in environment.services]
            }
        return {'message': 'Environment not found'}, 404

    @staticmethod
    def embedded(product_id, environment_id):
        environments = []
        for product in PRODUCTS:
            environments.extend(product.environments)

        environment = next((e for e in environments if str(e.environment_id) == str(environment_id)), None)
        if environment:
            arguments_list = [{'service_id': str(ser.service_id), 'name': ser.name} for ser in environment.services]
            return Embedded('services', SpringBootServiceResource, *arguments_list)
        return Embedded('services', SpringBootServiceResource)

    @staticmethod
    def links(product_id, environment_id):
        return Link('self', f'/api/products/{product_id}/environments/{environment_id}')


class SpringBootServiceResource(Resource):
    @staticmethod
    def data(product_id, environment_id, service_id):

        services = []
        for product in PRODUCTS:
            for environment in product.environments:
                services.externd(environment.services)

        service = next((s for s in services if str(s.service_id) == str(service_id)), None)
        if service:
            try:
                schema = SpringBootServiceSchema()
                return schema.dump(service)
            except ValidationError as err:
                return err.messages, 400
        return {'message': 'Environment not found'}, 404

    @staticmethod
    def links(product_id, environment_id, service_id):
        return Link('self', f'/api/products/{product_id}/environments/{environment_id}/services/{service_id}')


# Define the ProductsResource class
class ProductsResource(Resource):
    @staticmethod
    def data():
        return {'size': len(PRODUCTS)}

    # @staticmethod
    # def embedded(product_id):
    #     arguments_list = [(product,) for product in PRODUCTS]
    #     return Embedded('items', Product, *arguments_list)

    @staticmethod
    def links():
        arguments_list = [('/api/products/{}'.format(str(product.product_id)), {'name': str(product.name)}) for
                          product in PRODUCTS]
        return Link('items', *arguments_list)


app = Flask(__name__)
api = Api(app)
api.add_resource(ProductsResource, '/api/products')
api.add_resource(ProductResource, '/api/products/<product_id>')
api.add_resource(EnvironmentResource, '/api/products/<product_id>/environments/<environment_id>')
api.add_resource(SpringBootServiceResource,
                 '/api/products/<product_id>/environments/<environment_id>/services/<service_id>')

if __name__ == '__main__':
    app.run(debug=True)
