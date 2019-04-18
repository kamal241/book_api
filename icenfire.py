import requests
import json

class IceNFire(object):
	def __init__(self):
		self.base_url = "https://www.anapioficeandfire.com/api/books"

	def get_book_from_icenfire(self, book_name):
		url = "{}?name={}".format(self.base_url,book_name) 
		response = requests.get(url)
		ext_books = []
		if response.status_code == 200:	
			ext_books = self._filter_response(response.json())
		return ext_books			

	def _filter_response(self, books):
		key_maping = { 'name':'name', 'isbn':'isbn', 'authors':'authors', 'numberOfPages':'number_of_pages', 'publisher':'publisher', 'country':'country', 'released':'release_date' }
		matched_books = []
		for book in books:
			#print book
			ibook = { v : book[k] for k, v in key_maping.items() }
			ibook['release_date'] = ibook['release_date'][:10] # 1996-08-01T00:00:00
			matched_books.append(ibook)
		return matched_books

if __name__ == "__main__":
	icnf = IceNFire()
	mbooks = icnf.get_book_from_icenfire("A Game of Thrones")
	#mbooks = filter_response(books)
	response = {"status_code" : 200, "status": "success", "data" : mbooks}
	print (response)
