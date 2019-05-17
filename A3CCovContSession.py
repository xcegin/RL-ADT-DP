import multiprocessing
import os
import pickle
import threading

import tensorflow as tf

from Agent.Continuous.ACConvCont import ACNet
from Agent.Continuous.ACCovContWorker import ACCovContWorker

GLOBAL_NET_SCOPE = 'Global_Net'

model_path = './model'

tf.reset_default_graph()

if not os.path.exists(model_path):
    os.makedirs(model_path)


if __name__ == "__main__":
    global_rewards = []
    global_episodes = tf.Variable(0, dtype=tf.int32, name='global_episodes', trainable=False)

    sess = tf.Session()

    num_workers = multiprocessing.cpu_count()

    saver = tf.train.Saver(max_to_keep=5)

    with open('vectors_nextDate.pkl', 'rb') as fh:
        embeddings, embed_lookup = pickle.load(fh)
        num_feats = len(embeddings[0])

    with tf.device("/cpu:0"):
        global_ac = ACNet(GLOBAL_NET_SCOPE, sess, num_feats)  # we only need its params
        workers = []
        # Create workers
        for i in range(num_workers):
            workers.append(ACCovContWorker(i, global_ac, sess, global_rewards, global_episodes, model_path))

    coord = tf.train.Coordinator()
    sess.run(tf.global_variables_initializer())

    worker_threads = []
    for worker in workers:  # start workers
        job = lambda: worker.work(sess, coord, saver)
        t = threading.Thread(target=job)
        t.start()
        worker_threads.append(t)
    coord.join(worker_threads)  # wait for termination of workers
