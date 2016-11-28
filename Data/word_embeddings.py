import os
import gensim
import cPickle
from nltk.tokenize import sent_tokenize, word_tokenize
import Data.corpusreader as corpusreader

class WordEmbedding(object):

	def __init__(self, embedding_file, books_path=None):
		self.embedding_file = embedding_file
		self.books_path = books_path
		self.embeddings = None

	def get_embeddings(self):
		if os.path.isfile(self.embedding_file):
			try:
				self.embeddings = cPickle.load(open(self.embedding_file))
			except Exception as e:
				print e
				print 'Could not load pickle file', self.embedding_file
		else: 
			self.embeddings = self.learn_embeddings()
			cPickle.dump(self.embeddings,open(self.embedding_file,'wb'))
		return self.embeddings

	def learn_embeddings(self):
		try:
			print 'Getting sentence iterator for all books..'
			corpus_reader = corpusreader.EntireCorpus(self.books_path)
			print 'creating model for all sentences...'
			# toggle with values here
			model = gensim.models.Word2Vec(corpus_reader, min_count=10)
			return model
		except Exception as e:
			print e
