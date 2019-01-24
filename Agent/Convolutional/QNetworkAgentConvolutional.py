from __future__ import division

import tensorflow as tf
import tensorflow.contrib.slim as slim

from Agent.Convolutional.ConvolutionaLayer import conv_layer


class Q_Network_Convolutional:
    def __init__(self, feature_size):
        self.nodes = tf.placeholder(tf.float32, shape=(None, None, feature_size), name='tree')
        self.children = tf.placeholder(tf.int32, shape=(None, None, None), name='children')

        self.conv = conv_layer(1, 100, self.nodes, self.children, feature_size)

        # These lines establish the feed-forward part of the network used to choose actions
        self.Temp = tf.placeholder(shape=None, dtype=tf.float32)
        self.keep_per = tf.placeholder(shape=None, dtype=tf.float32)

        hidden = slim.fully_connected(self.conv, 256, activation_fn=tf.nn.tanh, biases_initializer=None)
        hidden = slim.dropout(hidden, self.keep_per)
        self.Q_out = slim.fully_connected(hidden, 37, activation_fn=None, biases_initializer=None)

        self.predict = tf.argmax(self.Q_out, 1)
        self.Q_dist = tf.nn.softmax(self.Q_out / self.Temp)

        # Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.actions = tf.placeholder(shape=[None], dtype=tf.int32)
        self.actions_onehot = tf.one_hot(self.actions, 37, dtype=tf.float32)

        self.Q = tf.reduce_sum(tf.multiply(self.Q_out, self.actions_onehot), reduction_indices=1)

        self.nextQ = tf.placeholder(shape=[None], dtype=tf.float32)
        loss = tf.reduce_sum(tf.square(self.nextQ - self.Q))
        trainer = tf.train.AdamOptimizer(learning_rate=0.001)
        self.updateModel = trainer.minimize(loss)
