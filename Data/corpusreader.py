import os
import csv
import gensim
import codecs
import cPickle
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
				# only use the cleaned .txt files, not the csv metadata or uncleaned files
				if len(textfile_name) < 12:
					continue
				if textfile_name[-12:] == "_cleaned.txt":
					textfile = os.path.join(bookfile_dir, textfile_name)
					# this is used to 
					with codecs.open(textfile, mode='r', encoding='utf-8', errors='ignore') as fp:
					 	text = fp.read()
					 	# first split up string into sentences 
					 	sent_tokenize_list = sent_tokenize(text)
					 	for sent in sent_tokenize_list:
					 		# then tokenize
					 		yield word_tokenize(sent)



def getCharactersData(book_path):
	character_data = {}
	with open(book_path,'rb') as csvfile:
		metadata = csv.reader(csvfile,delimiter=',')
		firstline = True
		for character,list_file,analysis_file in metadata:
			if firstline:
				firstline = False
				continue
			character_data[character] = {'list': readText(list_file), 
										'analysis': readText(analysis_file),
										'relevant_text': getRelevantCharacterText(list_file)}
	return character_data

def readText(filename):
	if filename == '':
		return None
	with codecs.open(filename, mode='r', encoding='utf-8', errors='ignore') as fp:
		text = fp.read()
	return textToSentences(text)

def textToSentences(text):
	sent_tokenize_list = sent_tokenize(text)
	return [word_tokenize(sent) for sent in sent_tokenize_list]

def getRelevantCharacterText(textPath):
	filename = translatePathToText(textPath)
	splitter = '___________________________'
	with codecs.open(filename, mode='r', encoding='utf-8', errors='ignore') as fp:
		all_text = fp.read()
	return [textToSentences(text) for text in all_text.split(splitter)]
	

def translatePathToText(characterPath):
	directory = os.path.dirname(characterPath)
	base = os.path.basename(characterPath)
	try:
		character_num = base.split('_')[1]
		int(character_num)
	except Exception as e:
		print e
	new_base = 'character_' + character_num + '_text.txt'
	return os.path.join(directory,new_base)

# corpus_generator = EntireCorpus('Books/')

# model = gensim.models.Word2Vec(corpus_generator, min_count=10)


