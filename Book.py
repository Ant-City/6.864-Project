import os
import cPickle
from nltk.tokenize import sent_tokenize, word_tokenize
import corpusreader

class Book(object):

	def __init__(self,directory_name,path='Books'):
		self.book_path = os.path.join(path,directory_name) + '/'
		self.main_text_path = self.book_path + 'main.txt'
		self.metadata_path = self.book_path + 'meta_data.csv'
		self.title = translate_path(directory_name)
		self.stored_object = translate_to_pickle(self.book_path)
		self.characters = None
		self.mainText = None
		self.populate()
		self.save()

	def getTitle(self):
		return self.title

	def getMainText(self):
		return self.mainText
		

	def getCharacters(self):
		return self.characters

	def populate(self):
		self.characters = corpusreader.getCharactersData(self.metadata_path)
		self.mainText = corpusreader.readText(self.main_text_path)

	def save(self):
		cPickle.dump(self,open(self.stored_object,'wb'))    

	@classmethod
	def getBook(cls,directory_name,path='Books/'):
		book_path = os.path.join(path,directory_name) + '/'
		main_text_path = book_path + 'main.txt'
		stored_object = translate_to_pickle(book_path)
		if os.path.isfile(stored_object):
			print 'loading book object from memory...'
			return cPickle.load(open(stored_object,'rb'))
		else:
			print 'creating new book object..'
			return Book(directory_name,path)

def translate_path(path):
	return ' '.join(path.split('_'))

def translate_to_pickle(path):
	picklefile = 'Book_object.p'
	return path + picklefile


# firstBook = Book.getBook('1984')
