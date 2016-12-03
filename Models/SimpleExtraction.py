import re, cPickle
import Data.Book as Book
from helper_utils.clean_descriptions import get_all_character_names


class SimpleExtractionModel(object):
	def __init__(self, book, model):
		self.book = book
		self.model = model

	def getMainTextVector(self):
		text = self.book.getMainText()
		return self.docToVector(text)

	def getCharacterTextVector(self, characters_name):
		all_names = get_all_character_names(characters_name)
		# regex is any of the character names
		combined_regex = re.compile(reduce(lambda x, y: x+'|'+y, all_names))
		main_text_sentences = self.book.getMainText()
		relevant_sentences = [sent for sent in main_text_sentences if len(re.findall(combined_regex, sent)) > 0]
		return self.docToVector(relevant_sentences)

	def getCharactersMatrix(self):

		characters_dict = self.book.getCharacters()
		character_vecs = {}

		for char,list_anal in characters_dict.iteritems():
			inner_dict = {}
			for key,text in list_anal.iteritems():
				if text == None:
					continue
				inner_dict[key] = self.docToVector(text)

			inner_dict['relevant_text'] = main_text_vector

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
		return SimpleExtractionModel(book, model)

