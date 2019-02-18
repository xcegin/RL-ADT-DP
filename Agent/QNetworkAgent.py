from __future__ import division

import tensorflow as tf
import tensorflow.contrib.slim as slim

class Q_Network:
    def __init__(self):
        # These lines establish the feed-forward part of the network used to choose actions
        self.inputs = tf.placeholder(shape=[None, 8], dtype=tf.float32)
        self.Temp = tf.placeholder(shape=None, dtype=tf.float32)
        self.keep_per = tf.placeholder(shape=None, dtype=tf.float32)

        hidden = slim.fully_connected(self.inputs, 256, activation_fn=tf.nn.tanh, biases_initializer=None)
        hidden = slim.dropout(hidden, self.keep_per)
        self.Q_out = slim.fully_connected(hidden, 7, activation_fn=None, biases_initializer=None)

        self.predict = tf.argmax(self.Q_out, 1)
        self.Q_dist = tf.nn.softmax(self.Q_out / self.Temp)

        # Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.actions = tf.placeholder(shape=[None], dtype=tf.int32)
        self.actions_onehot = tf.one_hot(self.actions, 7, dtype=tf.float32)

        self.Q = tf.reduce_sum(tf.multiply(self.Q_out, self.actions_onehot), reduction_indices=1)

        self.nextQ = tf.placeholder(shape=[None], dtype=tf.float32)
        loss = tf.reduce_sum(tf.square(self.nextQ - self.Q))
        trainer = tf.train.AdamOptimizer(learning_rate=0.001)
        self.updateModel = trainer.minimize(loss)
