import os
import cPickle
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim
import Data.Book as Book
import SimpleVectorizer as SV
import utils

class RelevantTextVectorizer(SV.SimpleBookMatrix):
	"""docstring for RelevantTextVectorizer"""
	def __init__(self, book, model):
		SV.SimpleBookMatrix.__init__(self, book, model)
		
	def getCharactersMatrix(self):
		main_text_vector = self.getMainTextVector()

		characters_dict = self.book.getCharacters()
		character_vecs = {}
		for char,list_anal in characters_dict.iteritems():
			inner_dict = {}
			for key,text in list_anal.iteritems():
				if text == None:
					continue
				if key == 'relevant_text':
					inner_dict[key] = self.docToVector(utils.flattenList(text))
				else:
					inner_dict[key] = self.docToVector(text)
			character_vecs[char] = inner_dict
		return character_vecs

	@classmethod
	def getRelevantTextVectorizer(cls,book_path,embedding_file=None,model=None):
		book = Book.Book.getBook(book_path)
		if model:
			return RelevantTextVectorizer(book,model)
		else:
			try:
				model = cPickle.load(open(embedding_file,'rb'))
				print 'model loaded...'
			except Exception as e:
				print e
				return None
			return RelevantTextVectorizer(book, model)


