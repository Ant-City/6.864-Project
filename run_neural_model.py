import time
import os
import tensorflow as tf
import numpy as np
import Models.NueralModel as nm
import Data.BookPairs as bp
from helper_utils.train_valid_test import get_train_test

LOG_FILE = '/Users/henryaspegren/Dropbox (MIT)/Academics/MIT/Senior Fall (2016)/6.864/Project/6.864-Project/log'
SAVE_DIR = '/Users/henryaspegren/Dropbox (MIT)/Academics/MIT/Senior Fall (2016)/6.864/Project/6.864-Project/saved'

def run_experiment(train_iterator, test_iterator):
  
  # Tell TensorFlow that the model will be built into the default Graph.
  with tf.Graph().as_default():

  	# first intialize the placeholders
  	text_placeholder, desc_placeholder, label_placeholder = nm.generate_placeholders()

  	# build the graph 
	logits = nm.inference(text_placeholder, desc_placeholder)

	# add the loss to the graph
	loss = nm.loss(logits, label_placeholder)

	# train operation
	train_op = nm.training(loss)

	# evaluation operation
	eval_op = nm.evaluate(logits, label_placeholder)

	summary = tf.summary.merge_all()

	# initialize variables
	init = tf.global_variables_initializer()

	# create a saver
	saver = tf.train.Saver()

	# start a session
	sess = tf.Session()

	summary_writer = tf.train.SummaryWriter(LOG_FILE, sess.graph)

	sess.run(init)

	start_time = time.time()

	step = 0
	print 'beginning training'
	for batch_count, batch in enumerate(train_iterator):
		text, desc, label = batch
		feed_dict = {text_placeholder: text, desc_placeholder:desc, label_placeholder:label}


		for i in range(1000):
			_, loss_value = sess.run([train_op, loss],
	                               feed_dict=feed_dict)

			# count the number of examples
			step += label.shape[0]

			duration = time.time() - start_time

			if step % 100 == 0:
				print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
		        # Update the events file.
		        summary_str = sess.run(summary, feed_dict=feed_dict)
		        summary_writer.add_summary(summary_str, step)
		        summary_writer.flush()

	    # save the model every 10000 training examples
		if ((step+1) % 10000 == 0):
			saver.save(sess, os.path.join(SAVE_DIR,'neural-model'), global_step=step)

	print 'training completed'

	# save the final trained model
	saver.save(sess, os.path.join(SAVE_DIR, 'neural-model-final'))

	# once it is trained 
	# test it 
	total_correct = 0
	total_incorrect = 0
	for batch_count, batch in enumerate(test_iterator):
		text, desc, label = batch
		feed_dict = {text_placeholder: text, desc_placeholder:desc, label_placeholder:label}

		loss, accuracy = sess.run([loss, eval_op],
                               feed_dict=feed_dict)

		print 'final test loss'
		print loss
		correct, incorrect = accuracy
		total_correct += correct
		total_incorrect += incorrect

	print 'test set results'
	print 'total correct: '+str(total_correct)
	print 'total incorrect: '+str(total_incorrect)
	print 'accuracy: '+str(float(total_correct)/(total_correct+total_incorrect))



"""
This class is a low-memory usage generator for feeding in the books  
to the Nueral Model 
"""
class NMFeeder(object):

	def __init__(self, book_pairs, embedding_file='cleaned_embeddings_all_texts.p', 
			limit=None, negative_proportion=0.5, batch_upper=100):
		self.book_pairs = book_pairs
		self.embedding_file = embedding_file
		self.count = 0
		self.limit = limit
		self.negative_proportion = negative_proportion
		self.batch_upper = batch_upper

	def __iter__(self):
		for (book1, book2) in self.book_pairs:
			try:
				# debugging feature
				if self.limit:
					if self.limit <= self.count:
						break
				print 'now using '+book1+' and '+book2
				# MAX_TEXT_LENGTH and MAX_DESC_LENGTH are hyperparameters
				res = bp.get_batch_for_pair(book1, book2, self.embedding_file, nm.MAX_TEXT_LENGTH, nm.MAX_DESC_LENGTH, 
					batch_upper=self.batch_upper, negative_proportion=self.negative_proportion)
				# this is needed to make sure the numpy arrays have the correct shapes
				text = np.array(res['x_text'].tolist())
				desc = np.array(res['x_desc'].tolist())
				label = np.array(res['Y'].tolist())
				self.count += 1
				yield text, desc, label
			except Exception as e:
				print 'SOMETHING WENT WRONG'
				print e 
				continue




#############################
######## Nueral Model ########
#############################




# this will return the same train-test partition 
# start with 10k training book pairings
# and 2k test book pairings
# with a 50/50 
train, test = get_train_test(train_count=10000, test_count=2000)
train_feeder = NMFeeder(train, limit=1)
test_feeder = NMFeeder(train, limit=1)
run_experiment(train_feeder, test_feeder)


