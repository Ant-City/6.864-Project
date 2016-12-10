import os
import tensorflow as tf

SAVE_DIR = '/Users/henryaspegren/Dropbox (MIT)/Academics/MIT/Senior Fall (2016)/6.864/Project/6.864-Project/saved'

sess = tf.Session()
new_saver = tf.train.import_meta_graph(os.path.join(SAVE_DIR,'neural-model-final.meta'))
new_saver.restore(sess, tf.train.latest_checkpoint(SAVE_DIR))

print tf.get_collection('MODEL_VARIABLES')
