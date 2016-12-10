import time
import os
import tensorflow as tf
import numpy as np
import Models.NueralModel as nm
import Data.BookPairs as bp
from helper_utils.train_valid_test import get_train_test

LOG_FILE = '/Users/henryaspegren/Dropbox (MIT)/Academics/MIT/Senior Fall (2016)/6.864/Project/6.864-Project/log'
SAVE_DIR = '/Users/henryaspegren/Dropbox (MIT)/Academics/MIT/Senior Fall (2016)/6.864/Project/6.864-Project/saved'


NUM_GRAD_PER_BOOK = 50
CHECKPOINT_EVERY_N_BATCHES = 2

def run_experiment(train_iterator, test_iterator, use_saved_model=False):
  
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

	# start a session
	sess = tf.Session()

	# for logging performance stats as we go
	summary_writer = tf.train.SummaryWriter(LOG_FILE, sess.graph)

	# for saving parameter values
	saver = tf.train.Saver()


	start_time = time.time()

	# holds the total number of examples (with repetition) seen by the network
	step = 0

	# use saved weights rather than re-training
	if use_saved_model:
		print 'using saved weight values rather than training'
		saver.restore(sess, tf.train.latest_checkpoint(SAVE_DIR))
   	else:
   		# initialize variables
		init = tf.global_variables_initializer()

   		# if no saved values need to initialize all variables (randomly)
   		sess.run(init)

		print 'beginning training'
		for batch_count, batch in enumerate(train_iterator):
			text, desc, label = batch
			feed_dict = {text_placeholder: text, desc_placeholder:desc, label_placeholder:label}


			for i in range(NUM_GRAD_PER_BOOK):
				_, loss_value = sess.run([train_op, loss_summary],
		                               feed_dict=feed_dict)

				# count the number of examples
				step += label.shape[0]

				duration = time.time() - start_time

				if step % 500 == 0:
					print('Training | Batch %d: Step %d: loss = %.2f (%.3f sec)' % (batch_count+1, step, loss_value, duration))
			        # # Update the events file.
			        # summary_writer.add_summary(loss_value, step)
			        # summary_writer.flush()

		    # save the model every so often
			if ((batch_count+1) % CHECKPOINT_EVERY_N_BATCHES == 0):
				saver.save(sess, os.path.join(SAVE_DIR,'neural-model'), global_step=step)

		print 'training completed'
		# save the final trained model
		saver.save(sess, os.path.join(SAVE_DIR, 'neural-model'))

	# once it is trained 
	# test it 
	total_correct = 0
	total_incorrect = 0
	for batch_count, batch in enumerate(test_iterator):
		text, desc, label = batch
		feed_dict = {text_placeholder: text, desc_placeholder:desc, label_placeholder:label}

		loss_val, accuracy = sess.run([loss, eval_op],
                               feed_dict=feed_dict)
		duration = time.time() - start_time
		print('Testing | Batch %d: loss = %.2f (%.3f sec)' % (batch_count+1, loss_val, duration))
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

book_pairs: a list of book pair examples (book1, book2) from which to lazily construct examples
embedding_file: a file containing the word embeddings from gensim saved in pickle format
batch_upper: is the upper bound on the batch size
negative_proportion: is the ratio of negative examples / total examples
number_of_epochs: is the number of times the iterator will go through the entire dataset
limit: (for debugging) goes through ONLY that number of examples

"""
class NMFeeder(object):

	def __init__(self, book_pairs, embedding_file='cleaned_embeddings_all_texts.p', 
			limit=None, negative_proportion=0.5, batch_upper=100, number_of_epochs=1):
		self.book_pairs = book_pairs
		self.embedding_file = embedding_file
		self.count = 0
		self.limit = limit
		self.negative_proportion = negative_proportion
		self.batch_upper = batch_upper
		self.number_of_epochs = number_of_epochs

	def __iter__(self):
		for epoch in range(self.number_of_epochs):
			for (book1, book2) in self.book_pairs:
				try:
					# debugging feature
					if self.limit:
						if self.limit <= self.count:
							break
					print 'now using '+book1+' and '+book2+' in epoch:'+str(epoch)
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
######## Nueral Model #######
#############################




# this will return the same train-test partition 
# start with 10k training book pairings
# and 2k test book pairings
# with a 50/50 
train, test = get_train_test(train_count=1000, test_count=200)
train_feeder = NMFeeder(train, limit=2, number_of_epochs=3)
test_feeder = NMFeeder(train, limit=2)
run_experiment(train_feeder, test_feeder, use_saved_model=False)


