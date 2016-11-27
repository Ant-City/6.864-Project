import os
import cPickle
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim
import Book
import corpusreader


class SimpleBookMatrix(object):
	def __init__(self, book, model):
		self.book = book
		self.model = model
	def getMainTextVector(self):
		text = self.book.getMainText()
		return self.docToVector(text)

	def getCharactersMatrix(self):
		characters_dict = self.book.getCharacters()
		character_vecs = {}
		for char,list_anal in characters_dict.iteritems():
			inner_dict = {}
			for key,text in list_anal.iteritems():
				if text == None:
					continue
				inner_dict[key] = self.docToVector(text)
			character_vecs[char] = inner_dict
		return character_vecs

	def wordToVector(self,word,dimension=100):
		if word in self.model:
			return self.model[word]
		return np.zeros(dimension)

	def sentenceToVector(self,sentence):
		vectorized = [self.wordToVector(word) for word in sentence]
		return np.average(vectorized,axis=0)

	def docToVector(self,document):
		vectorized = [self.sentenceToVector(sentence) for sentence in document]
		return np.average(vectorized,axis=0)


	@classmethod
	def getSimpleVectorizer(cls,book_path,embedding_file):
		book = Book.Book.getBook(book_path)
		try:
			model = cPickle.load(open(embedding_file,'rb'))
			print 'model loaded...'
		except Exception as e:
			print e
			return None
		return SimpleBookMatrix(book, model)


# simple = SimpleBookMatrix.getSimpleVectorizer('1984/','all_embeddings.p')
# print simple.getMainTextVector()
# print simple.getCharactersMatrix()