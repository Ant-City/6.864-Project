import os, cPickle, build_dataset
from Data.Book import Book
from Models.SimpleVectorizer import SimpleBookMatrix


def get_book_models(root_dir):
	books = []
	for book_dir_name in os.listdir(root_dir):
		print 'getting book model for '+book_dir_name
		book_obj = Book.getBook(book_dir_name)
		books.append(book_obj)

def get_base_model(root_dir, embedding_file):
	books = []
	for book_dir_name in os.listdir(root_dir):
		print 'getting base model for '+book_dir_name
		book_obj = SimpleBookMatrix.getSimpleVectorizer(book_dir_name, embedding_file)
		books.append(book_obj)
	return books	


#############################
######## Basic Model ########
#############################

# data
root_dir = 'Books/'
saved_file = 'base_model.p'
embedding_file = 'cleaned_embeddings_all_texts.p'
books = get_base_model(root_dir, embedding_file)

# training_df
training_df = build_dataset.build_master_dataframe(books)
with open(saved_file,'wb') as fp:
	cPickle.dump(training_df, fp)  

print training_df


