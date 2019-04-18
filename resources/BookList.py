from flask import request
from flask_restful import Resource
from Model import db, Book, BookSchema

books_schema = BookSchema(many=True)
book_schema = BookSchema()

class BookListResource(Resource):
    def get(self):
        books_data = []
        if 'name' in request.args:
            book_name = request.args.get('name')
            books = Book.query.filter(Book.name.contains(book_name))            
        elif 'country' in request.args:
            book_country = request.args.get('country')
            #books = Book.query.filter_by(country=book_country)
            books = Book.query.filter(Book.country.contains(book_country))
        elif 'publisher' in request.args:
            book_publisher = request.args.get('publisher')
            #books = Book.query.filter_by(publisher=book_publisher)
            books = Book.query.filter(Book.publisher.contains(book_publisher))
        elif 'release_date' in request.args:
            book_release_year = request.args.get('release_date')
            books = Book.query.filter(Book.release_date.contains(book_release_year))
        else:
            books = Book.query.all()
    
        if books:
            books_data = books_schema.dump(books).data
    
        return {'status_code' : 200 ,'status': 'success', 'data': books_data}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = book_schema.load(json_data)
        if errors:
            print (errors)
            return errors, 422
        else:
            try:
                book = Book.query.filter_by(name=data['name']).first()
                if book:
                    return {'message': 'book already exists'}, 400

                book = Book(
                        isbn = json_data['isbn'], 
                        name = json_data['name'],            
                        authors = json_data['authors'], 
                        number_of_pages = json_data['number_of_pages'],
                        publisher = json_data['publisher'],
                        country = json_data['country'],
                        release_date = json_data['release_date']
                        )
                db.session.add(book)
                db.session.commit()
                result = book_schema.dump(book).data
                return {'status_code' : 201, 'status': 'success', 'data': [ result ] }, 201
            except KeyError:
                return {'status_code' : 400, 'status': 'One or more required field missing', 'data': [] }, 400