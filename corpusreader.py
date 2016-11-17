import os
import gensim
import codecs
from nltk.tokenize import sent_tokenize, word_tokenize


class EntireCorpus(object):

	def __init__(self, book_directory_name):
		self.root_dir = book_directory_name

	def __iter__(self):
		for bookfile_name in os.listdir(self.root_dir):
			bookfile_dir = os.path.join(self.root_dir, bookfile_name)
			if not os.path.isdir(bookfile_dir):
				continue
			for textfile_name in os.listdir(bookfile_dir):
				# only use the .txt files, not the csv metadata)
				if textfile_name[-3:] == "txt":
					textfile = os.path.join(bookfile_dir, textfile_name)
					# this is used to 
					with codecs.open(textfile, mode='r', encoding='utf-8', errors='ignore') as fp:
					 	text = fp.read()
					 	# first split up string into sentences 
					 	sent_tokenize_list = sent_tokenize(text)
					 	for sent in sent_tokenize_list:
					 		# then tokenize
					 		yield word_tokenize(sent)



# corpus_generator = EntireCorpus('Books/')

# model = gensim.models.Word2Vec(corpus_generator, min_count=10)