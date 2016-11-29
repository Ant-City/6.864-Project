import os, cPickle, build_dataset
from Data.Book import Book
from Models.SimpleVectorizer import SimpleBookMatrix



class Experiment(object):

	def __init__(self, root_dir='Books/'):
		self.root_dir = root_dir

	def __iter__(self):
		for book_dir_name in os.listdir(self.root_dir):
			print 'getting base model for '+book_dir_name
			yield SimpleBookMatrix.getSimpleVectorizer(book_dir_name, 
				'cleaned_embeddings_all_texts.p')


#############################
######## Basic Model ########
#############################

# data
simple_books = Experiment()

# training_df
training_df = build_dataset.build_master_dataframe(simple_books)
with open(saved_file,'wb') as fp:
	cPickle.dump(training_df, fp)  

print training_df


