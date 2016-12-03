import os
import cPickle
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import Data.corpusreader as corpusreader
import Data.Book as Book


class BookMatrixV2(object):
	def __init__(self,book,model):
		self.book = book
		self.model = model

	def getMainTextMatrix(self):
		text = self.book.getMainText()
		return self.docToMatrix(text)

	def getCharactersMatrices(self):
		characters_dict = self.book.getCharacters()
		character_vecs = {}
		for char,list_anal in characters_dict.iteritems():
			inner_dict = {}
			for key,text in list_anal.iteritems():
				if text == None:
					continue
				if key != 'relevant_text':
					inner_dict[key] = self.docToMatrix(text)
				else:
					inner_dict[key] = np.array([self.docToMatrix(doc) for doc in text])
			character_vecs[char] = inner_dict
		return character_vecs

	def wordToVector(self,word,dimension=100):
		if word in self.model:
			return self.model[word]
		return np.zeros(dimension)

	def sentenceToMatrix(self,sentence):
		return [self.wordToVector(word) for word in sentence]

	def docToMatrix(self,doc):
		return flattenList([self.sentenceToMatrix(sent) for sent in doc])

	@classmethod
	def getBookMatrix(cls,book_path,embedding_file,rebuild=False):
		book = Book.Book.getBook(book_path,'Books/',rebuild)
		try:
			model = cPickle.load(open(embedding_file,'rb'))
			print 'model loaded...'
		except Exception as e:
			print e
			return None
		return BookMatrixV2(book, model)



def flattenList(multList):
	return np.array([item for sublist in multList for item in sublist])


