from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()

class Book(db.Model):
	__tablename__ = 'books'
	id = db.Column(db.Integer, primary_key=True)
	isbn = db.Column(db.String(14))
	name = db.Column(db.String(100))
	authors= db.Column(db.String(500))
	number_of_pages = db.Column(db.Integer)
	publisher = db.Column(db.String(100))
	country = db.Column(db.String(50))
	release_date = db.Column(db.String(10))

	def __init__(self, isbn, name, authors, number_of_pages, publisher, country, release_date):
		self.isbn = isbn
		self.name = name
		self.authors = authors
		self.number_of_pages = number_of_pages
		self.publisher = publisher
		self.country = country
		self.release_date = release_date

class BookSchema(ma.Schema):
	class Meta:
        # Fields to expose
		fields = ('id','name','authors','number_of_pages','publisher','country','release_date')

book_schema = BookSchema()
books_schema = BookSchema(many=True)