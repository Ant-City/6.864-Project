import cPickle, os
import numpy as np
import tensorflow as tf
import gensim
from Data.Book import Book




WORD_DIM = 100
MAX_DESC_LENGTH = 200
MAX_TEXT_LENGTH = 200
NUM_HIDDEN = 50

def text_to_vector(list_of_sents, model):
	res = np.zeros((MAX_DESC_LENGTH, WORD_DIM))
	i = 0 
	for sent in list_of_sents:
		for word in sent:
			if word in model:
				res[i] = model[word]
			i+=1
			if i >= MAX_DESC_LENGTH:
				return res
	return res


def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)



# tf Graph input

# RNN for processing text
with tf.variable_scope("RNN1"):
	x1 = tf.placeholder("float", [None, MAX_TEXT_LENGTH, WORD_DIM])
	cell1 = tf.nn.rnn_cell.BasicRNNCell(num_units=NUM_HIDDEN)

	_ , final_state1 = tf.nn.dynamic_rnn(
	    cell=cell1,
	    dtype=tf.float32,
	    inputs=x1)

# RNN for processing description
with tf.variable_scope("RNN2"):
	x2 = tf.placeholder("float", [None, MAX_DESC_LENGTH, WORD_DIM])
	cell2 = tf.nn.rnn_cell.BasicRNNCell(num_units=NUM_HIDDEN)
	_ , final_state2 = tf.nn.dynamic_rnn(
	    cell=cell2,
	    dtype=tf.float32,
	    inputs=x2)

# NN to combine them
W = tf.Variable(tf.zeros([NUM_HIDDEN+NUM_HIDDEN, 2]))
b = tf.Variable(tf.zeros([NUM_HIDDEN+NUM_HIDDEN, 1]))

y = tf.nn.softmax(tf.matmul(x, W) + b)


print [v.name for v in tf.all_variables()]



final_output = (final_state1, final_state2)









firstBook = Book.getBook('1984')
characters =  firstBook.getCharacters()

embedding_model = cPickle.load(open('cleaned_embeddings_all_texts.p','rb'))

X_ = []
for character in characters.keys():
	desc = characters[character]['list']
	vec = text_to_vector(desc, embedding_model).astype(np.float32)
	X_.append(vec)

X_ = np.array(X_)



print 'input'
print X_.shape

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
final_output = sess.run(final_output, feed_dict={x1:X_, x2:X_})
 
# print final_output[0].shape
# print final_output[0]
# print final_output[1].shape
# print final_output[1]





















# X = tf.train.batch(X_tensors, 5, enqueue_many=True,
# 	shapes=[[None, 100] for i in X_tensors], 
# 	dynamic_pad=True,
# 	allow_smaller_final_batch=True)


# res = tf.contrib.learn.run_n({"x": X}, n=1, feed_dict=None)


# print type(res[0]['x'])
# print type(res[0]['x'][0])
# for i in res[0]['x']:
# 	print i.shape

# # Before starting, initialize the variables.  We will 'run' this first.
# init = tf.global_variables_initializer()

# # Launch the graph.
# sess = tf.Session()
# sess.run(init)
