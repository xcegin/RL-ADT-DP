import multiprocessing
import pickle
import threading

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from Agent.Continuous.ACConvCont import ACNet
from Agent.Continuous.ACContWorker import Worker

GLOBAL_NET_SCOPE = 'Global_Net'

if __name__ == "__main__":
    global_rewards = []
    global_episodes = tf.Variable(0, dtype=tf.int32, name='global_episodes', trainable=False)

    sess = tf.Session()

    num_workers = multiprocessing.cpu_count()

    with open('vectors.pkl', 'rb') as fh:
        embeddings, embed_lookup = pickle.load(fh)
        num_feats = len(embeddings[0])

    with tf.device("/cpu:0"):
        global_ac = ACNet(GLOBAL_NET_SCOPE, sess, num_feats)  # we only need its params
        workers = []
        # Create workers
        for i in range(num_workers):
            workers.append(Worker(i, global_ac, sess, global_rewards, global_episodes))

    coord = tf.train.Coordinator()
    sess.run(tf.global_variables_initializer())

    worker_threads = []
    for worker in workers:  # start workers
        job = lambda: worker.work(sess, coord)
        t = threading.Thread(target=job)
        t.start()
        worker_threads.append(t)
    coord.join(worker_threads)  # wait for termination of workers

    plt.plot(np.arange(len(global_rewards)), global_rewards)  # plot rewards
    plt.xlabel('step')
    plt.ylabel('total moving reward')
    plt.show()
