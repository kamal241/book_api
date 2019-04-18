from flask import request
from flask_restful import Resource
from Model import db, Book, BookSchema
from flask.ext.restful import abort

book_schema = BookSchema()

class BookResource(Resource):
    def get(self, id):
        book = db.session.query(Book).filter(Book.id == id).first()
        book_data = book_schema.dump(book).data
        if not book:
            return {'status_code' : 404 ,'status': "Book {} doesn't exist".format(id), 'data': []}, 404
        return {'status_code' : 200 ,'status': 'success', 'data': book_data}, 200

    def patch(self, id):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = book_schema.load(json_data)
        if errors:
            return errors, 422
        book = Book.query.filter_by(id=id).first()
        if not book:
            return { 'status_code' : 200, 'status': 'success', 'message':'book does not exist' }, 400
        else:
            name = json_data['name'] if 'name' in json_data else book.name
            isbn = json_data['isbn'] if 'isbn' in json_data else book.isbn
            authors = json_data['authors'] if 'authors' in json_data else book.authors        
            number_of_pages = json_data['number_of_pages'] if 'number_of_pages' in json_data else book.number_of_pages
            publisher = json_data['publisher'] if 'publisher' in json_data else book.publisher
            country = json_data['country'] if 'country' in json_data else book.country
            release_date = json_data['release_date'] if 'release_date' in json_data else book.release_date

            book.name = name
            book.isbn = isbn
            book.authors = authors
            book.publisher = publisher
            book.country = country
            book.release_date = release_date

            db.session.commit()

            result = book_schema.dump(book).data
            message = "The book {} was updated successfully".format(book.name)
            return { 'status_code' : 200, 'status': 'success', 'message': message,'data': [ result ] }, 200

    def delete(self, id):
        book = Book.query.filter_by(id=id).first()        
        if not book:
            return { 'status_code' : 200, 'status': 'success', 'message':'book does not exist' }, 400
        else:            
            message = "The book {} was deleted successfully".format(book.name)            
            db.session.delete(book)
            db.session.commit()
            return { 'status_code' : 204, 'status': 'success', 'message': message,'data': [] }, 200