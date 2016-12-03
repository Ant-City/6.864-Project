import cPickle, os
import numpy as np
import tensorflow as tf
import gensim
from Data.Book import Book


WORD_DIM = 10
MAX_DESC_LENGTH = 4
MAX_TEXT_LENGTH = 4
NUM_HIDDEN_RNNS = 3
NUM_HIDDEN_FINAL_NN = 2
NUMBER_OF_OUTPUTS = 2

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


## NN to combine them
W_hidden = tf.Variable(tf.truncated_normal([NUM_HIDDEN_RNNS*2, NUM_HIDDEN_FINAL_NN], stddev=0.1), name="W_hidden")
b_hidden = tf.Variable(tf.constant(0.1, shape=[1, NUM_HIDDEN_FINAL_NN]), name="Bias_hidden")


hidden = tf.nn.relu(tf.matmul(X, W_hidden) + b_hidden)


W_readout = tf.Variable(tf.truncated_normal([NUM_HIDDEN_FINAL_NN, NUMBER_OF_OUTPUTS], stddev=0.1), name="W_readout")
b_readout = tf.Variable(tf.constant(0.1, shape=[1, NUMBER_OF_OUTPUTS]), name="Bias_readout")

y = tf.matmul(hidden, W_readout) + b_readout


cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, Y))
train_step = tf.train.AdamOptimizer().minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(Y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


### getting the data, feeding it in, building graph

X_ = np.random.rand(10, MAX_DESC_LENGTH, WORD_DIM)
X_[0:5, ]+= 2
Y_ = np.zeros((X_.shape[0], NUMBER_OF_OUTPUTS))
Y_[0:5, 0] = 1
Y_[5:, 1] = 1

print X_
print Y_

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)


print "PRE-TRAINING"
variables_names =[v.name for v in tf.trainable_variables()]
values = sess.run(variables_names)
for k,v in zip(variables_names, values):
    print(k, v)


train_accuracy = accuracy.eval(session=sess, feed_dict={x1:X_, x2:X_, Y:Y_})
print 'initial training accruacy '+ str(train_accuracy)

train_step.run(session=sess, feed_dict={x1:X_, x2:X_, Y:Y_})
print "POST TRAINING"

variables_names =[v.name for v in tf.trainable_variables()]
values = sess.run(variables_names)
for k,v in zip(variables_names, values):
    print(k, v)

train_accuracy = accuracy.eval(session=sess, feed_dict={x1:X_, x2:X_, Y:Y_})
print 'final training accruacy '+ str(train_accuracy)
 




























# summary_writer = tf.train.SummaryWriter('/Users/henryaspegren/Dropbox (MIT)/Academics/MIT/Senior Fall (2016)/6.864/Project/6.864-Project/log/', sess.graph)


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
