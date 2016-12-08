import numpy as np
import tensorflow as tf

# hyper paramaters
WORD_DIM = 100
MAX_TEXT_LENGTH = 4
MAX_DESC_LENGTH = 4
NUM_HIDDEN_RNNS = 100
NUM_HIDDEN_FINAL_NN = 10
NUMBER_OF_OUTPUTS = 2


"""
Builds our architecture using 

text - [batch_size, MAX_TEXT_LENGTH, WORD_DIM]
desc - [batch_size, MAX_DESC_LENGTH, WORD_DIM]

as placeholders

returns 

logits - [batch_size, NUMBER_OF_OUTPUTS]
"""
def inference(text, desc):
	# RNN for processing text
	with tf.variable_scope("RNN1"):
		cell1 = tf.nn.rnn_cell.BasicRNNCell(num_units=NUM_HIDDEN_RNNS)
		_ , final_state1 = tf.nn.dynamic_rnn(
		    cell=cell1,
		    dtype=tf.float32,
		    inputs=text)

	# RNN for processing description
	with tf.variable_scope("RNN2"):
		cell2 = tf.nn.rnn_cell.BasicRNNCell(num_units=NUM_HIDDEN_RNNS)
		_ , final_state2 = tf.nn.dynamic_rnn(
		    cell=cell2,
		    dtype=tf.float32,
		    inputs=desc)

	# Concatenate the outputs
	X = tf.concat(1, [final_state1, final_state2])

	# FeedForward NN to learn final classification
	W_hidden = tf.Variable(tf.truncated_normal([NUM_HIDDEN_RNNS*2, NUM_HIDDEN_FINAL_NN], stddev=0.1), name="W_hidden")
	b_hidden = tf.Variable(tf.constant(0.1, shape=[1, NUM_HIDDEN_FINAL_NN]), name="Bias_hidden")

	hidden = tf.nn.relu(tf.matmul(X, W_hidden) + b_hidden)

	W_readout = tf.Variable(tf.truncated_normal([NUM_HIDDEN_FINAL_NN, NUMBER_OF_OUTPUTS], stddev=0.1), name="W_readout")
	b_readout = tf.Variable(tf.constant(0.1, shape=[1, NUMBER_OF_OUTPUTS]), name="Bias_readout")

	logits = tf.matmul(hidden, W_readout) + b_readout
	return logits

def loss(pred, output):
	cross_entropy = tf.nn.softmax_cross_entropy_with_logits(pred, output, name="cross_entropy")
	loss = tf.reduce_mean(cross_entropy, name="mean_cross_entropy")
	return loss


def evaluate(pred, output):
	correct_prediction = tf.equal(tf.argmax(pred,1), tf.argmax(output,1))
	total_predictions = tf.cast(tf.shape(correct_prediction)[0], tf.float32)
	correct = tf.reduce_sum(tf.cast(correct_prediction, tf.float32))
	incorrect= total_predictions - correct
	return correct, incorrect


def training(loss):
	tf.summary.scalar('loss', loss)
	optimizer = tf.train.AdamOptimizer(1e-4)
	global_step = tf.Variable(0, name='global_step', trainable=False)
	training_step = optimizer.minimize(loss, global_step=global_step)

	return training_step


def generate_placeholders():
	text = tf.placeholder("float", shape=[None, MAX_TEXT_LENGTH, WORD_DIM])
	desc = tf.placeholder("float", shape=[None, MAX_DESC_LENGTH, WORD_DIM])
	label = tf.placeholder("float", shape=[None, NUMBER_OF_OUTPUTS])

	return text, desc, label
