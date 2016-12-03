import cPickle, os
import numpy as np
import tensorflow as tf
import gensim
from Data.Book import Book


WORD_DIM = 100
MAX_DESC_LENGTH = 200
MAX_TEXT_LENGTH = 200
NUM_HIDDEN_RNNS = 55
NUM_HIDDEN_FINAL_NN = 99
NUMBER_OF_OUTPUTS = 2

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
Y = tf.placeholder("float", [None, 2])


# RNN for processing text
with tf.variable_scope("RNN1"):
	x1 = tf.placeholder("float", [None, MAX_TEXT_LENGTH, WORD_DIM])
	cell1 = tf.nn.rnn_cell.BasicRNNCell(num_units=NUM_HIDDEN_RNNS)
	_ , final_state1 = tf.nn.dynamic_rnn(
	    cell=cell1,
	    dtype=tf.float32,
	    inputs=x1)

# RNN for processing description
with tf.variable_scope("RNN2"):
	x2 = tf.placeholder("float", [None, MAX_DESC_LENGTH, WORD_DIM])
	cell2 = tf.nn.rnn_cell.BasicRNNCell(num_units=NUM_HIDDEN_RNNS)
	_ , final_state2 = tf.nn.dynamic_rnn(
	    cell=cell2,
	    dtype=tf.float32,
	    inputs=x2)

X = tf.concat(1, [final_state1, final_state2])


# # NN to combine them
W_hidden = tf.Variable(tf.zeros([NUM_HIDDEN_RNNS*2, NUM_HIDDEN_FINAL_NN]))
b_hidden = tf.Variable(tf.zeros([1, NUM_HIDDEN_FINAL_NN]))


hidden = tf.nn.relu(tf.matmul(X, W_hidden) + b_hidden)


W_readout = tf.Variable(tf.zeros([NUM_HIDDEN_FINAL_NN, NUMBER_OF_OUTPUTS]))
b_readout = tf.Variable(tf.zeros([1, NUMBER_OF_OUTPUTS]))

y = tf.matmul(hidden, W_readout) + b_readout


cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, Y))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(Y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


### getting the data, feeding it in, building graph

firstBook = Book.getBook('1984')
characters =  firstBook.getCharacters()

embedding_model = cPickle.load(open('cleaned_embeddings_all_texts.p','rb'))

X_ = []
for character in characters.keys():
	desc = characters[character]['list']
	vec = text_to_vector(desc, embedding_model).astype(np.float32)
	X_.append(vec)

X_ = np.array(X_)
Y_ = np.zeros((X_.shape[0], 2))
Y_[:, 1] = 1
print Y_


init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

train_accuracy = accuracy.eval(session=sess, feed_dict={x1:X_, x2:X_, Y:Y_})
print 'initial training accruacy '+ str(train_accuracy)
train_step.run(session=sess, feed_dict={x1:X_, x2:X_, Y:Y_})
train_accuracy = accuracy.eval(session=sess, feed_dict={x1:X_, x2:X_, Y:Y_})
print 'final training accruacy '+ str(train_accuracy)
 

 #out = sess.run(correct_prediction, feed_dict={x1:X_, x2:X_, Y:Y_})
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
