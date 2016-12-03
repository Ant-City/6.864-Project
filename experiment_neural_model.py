import time
import tensorflow as tf
import numpy as np
import Models.NueralModel as NM


LOG_FILE = '/Users/henryaspegren/Dropbox (MIT)/Academics/MIT/Senior Fall (2016)/6.864/Project/6.864-Project/log'

def run_experiment(train_iterator, test_iterator):
  
  # Tell TensorFlow that the model will be built into the default Graph.
  with tf.Graph().as_default():

  	# first intialize the placeholders
  	text_placeholder, desc_placeholder, label_placeholder = NM.generate_placeholders()

  	# build the graph 
	logits = NM.inference(text_placeholder, desc_placeholder)

	# add the loss to the graph
	loss = NM.loss(logits, label_placeholder)

	# train operation
	train_op = NM.training(loss)

	# evaluation operation
	eval_op = NM.evaluate(logits, label_placeholder)

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
	for batch_count, batch in enumerate(train_iterator):
		text, desc, label = batch
		feed_dict = {text_placeholder: text, desc_placeholder:desc, label_placeholder:label}

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




	# once it is trained 
	# test it 
	total_correct = 0
	total_incorrect = 0
	for batch_count, batch in enumerate(test_iterator):
		text, desc, label = batch
		feed_dict = {text_placeholder: text, desc_placeholder:desc, label_placeholder:label}

		_, accuracy = sess.run([train_op, eval_op],
                               feed_dict=feed_dict)

		correct, incorrect = accuracy
		total_correct += correct
		total_incorrect += incorrect


	print 'final results'
	print 'total correct: '+str(total_correct)
	print 'total incorrect: '+str(total_incorrect)
	print 'accuracy: '+str(float(total_correct)/(total_correct+total_incorrect))





class NMFeeder(object):
	def __init__(self):
		self.count = 0
		self.text = np.random.rand(10, NM.MAX_TEXT_LENGTH, NM.WORD_DIM)
		self.desc = np.random.rand(10, NM.MAX_DESC_LENGTH, NM.WORD_DIM)
		self.label = np.random.rand(10, NM.NUMBER_OF_OUTPUTS)
	def __iter__(self):
		for i in range(10000):
			yield (self.text, self.desc, self.label)







run_experiment(NMFeeder(), NMFeeder())