import multiprocessing
import os
import pickle
import threading

import tensorflow as tf

from Agent.ACAgent import AC_Network
from Agent.ACWorker import Worker

max_episode_length = 1000
gamma = .99  # discount rate for advantage estimation and reward discounting
load_model = False
model_path = './model'

tf.reset_default_graph()

if not os.path.exists(model_path):
    os.makedirs(model_path)

with open('vectors_calc.pkl', 'rb') as fh:
    embeddings, embed_lookup = pickle.load(fh)
    num_feats = len(embeddings[0])

global_rewards = []
global_episodes = tf.Variable(0, dtype=tf.int32, name='global_episodes', trainable=False)
trainer = tf.train.AdamOptimizer(learning_rate=0.001)
master_network = AC_Network('global', None, num_feats)  # Generate global network
num_workers = multiprocessing.cpu_count()  # Set workers ot number of available CPU threads
workers = []
# Create worker classes
for i in range(num_workers):
    workers.append(Worker(i, trainer, model_path, global_episodes, global_rewards))
saver = tf.train.Saver(max_to_keep=5)

with tf.Session() as sess:
    coord = tf.train.Coordinator()
    if load_model:
        print('Loading Model...')
        ckpt = tf.train.get_checkpoint_state(model_path)
        saver.restore(sess, ckpt.model_checkpoint_path)
    else:
        sess.run(tf.global_variables_initializer())

    worker_threads = []
    for worker in workers:
        worker_work = lambda: worker.work(max_episode_length, gamma, master_network, sess, coord, saver)
        t = threading.Thread(target=worker_work)
        t.start()
        worker_threads.append(t)
    coord.join(worker_threads)
