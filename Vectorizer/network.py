"""This creates a network for training a vector embedding of an AST using
a strategy similar to word2vec, but applied to the context of AST's."""

import math
import tensorflow as tf

from Vectorizer.node_map import NODE_MAP
from Vectorizer.parameters import \
    BATCH_SIZE, NUM_FEATURES, HIDDEN_NODES


class embedding_network:
    def __init__(self, batch_size=BATCH_SIZE, num_feats=NUM_FEATURES, hidden_size=HIDDEN_NODES):
        self.inputs = tf.placeholder(tf.int32, shape=[batch_size, ], name='inputs')
        self.labels = tf.placeholder(tf.int32, shape=[batch_size, ], name='labels')

        # embeddings to learn
        self.embeddings = tf.Variable(
            tf.random_uniform([len(NODE_MAP), num_feats]), name='embeddings'
        )

        embed = tf.nn.embedding_lookup(self.embeddings, self.inputs)
        onehot_labels = tf.one_hot(self.labels, len(NODE_MAP), dtype=tf.float32)

        weights = tf.Variable(
            tf.truncated_normal(
                [num_feats, hidden_size], stddev=1.0 / math.sqrt(num_feats)
            ),
            name='weights'
        )

        biases = tf.Variable(
            tf.zeros((hidden_size,)),
            name='biases'
        )

        hidden = tf.tanh(tf.matmul(embed, weights) + biases)

        weights = tf.Variable(
            tf.truncated_normal(
                [hidden_size, len(NODE_MAP)],
                stddev=1.0 / math.sqrt(hidden_size)
            ),
            name='weights'
        )
        biases = tf.Variable(
            tf.zeros((len(NODE_MAP),), name='biases')
        )

        logits = tf.matmul(hidden, weights) + biases

        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(
            labels=onehot_labels, logits=logits, name='cross_entropy'
        )

        self.loss = tf.reduce_mean(cross_entropy, name='cross_entropy_mean')

        #return inputs, labels, embeddings, loss


