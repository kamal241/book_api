from flask import Blueprint
from flask_restful import Api

from resources.Book import BookResource
from resources.BookList import BookListResource
from resources.ExternalBook import ExternalBookResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(ExternalBookResource, '/external-books', endpoint = 'externam-books')
api.add_resource(BookListResource, '/v1/books', endpoint = 'books')
api.add_resource(BookResource, '/v1/books/<int:id>', endpoint = 'book', methods = ['GET', 'POST', 'PATCH', 'DELETE'])
