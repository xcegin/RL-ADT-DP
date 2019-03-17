import numpy as np
import tensorflow as tf
from tensorflow.contrib import slim

from Agent.Convolutional.ConvolutionaLayer import conv_layer

GLOBAL_NET_SCOPE = 'Global_Net'
UPDATE_GLOBAL_ITER = 10  # sets how often the global net is updated
GAMMA = 0.90  # discount factor
ENTROPY_BETA = 0.01  # entropy factor
LR_A = 0.001  # learning rate for actor
LR_C = 0.01  # learning rate for critic

N_A = 1  # number of actions
A_BOUND = [-1, 1]


class ACNet(object):
    def __init__(self, scope, sess, feature_size, globalAC=None):
        self.sess = sess
        self.actor_optimizer = tf.train.RMSPropOptimizer(learning_rate=LR_A, name='RMSPropA', decay=0.99,
                                                         epsilon=0.01)  # optimizer for the actor
        self.critic_optimizer = tf.train.RMSPropOptimizer(learning_rate=LR_C, name='RMSPropC', decay=0.99,
                                                          epsilon=0.01)  # optimizer for the critic
        with tf.variable_scope(scope):
            self.nodes = tf.placeholder(tf.float32, shape=(None, None, feature_size), name='tree')
            self.children = tf.placeholder(tf.int32, shape=(None, None, None), name='children')

            self.conv = conv_layer(1, 100, self.nodes, self.children, feature_size)
            self.pooling = self.pooling_layer(self.conv)

            l_ac = slim.fully_connected(self.pooling, 256, activation_fn=tf.nn.tanh, biases_initializer=None)

            self.lstm_cell = tf.nn.rnn_cell.LSTMCell(num_units=256, state_is_tuple=True)
            c_init = np.zeros((1, self.lstm_cell.state_size.c), np.float32)
            h_init = np.zeros((1, self.lstm_cell.state_size.h), np.float32)
            self.state_init = [c_init, h_init]
            c_in = tf.placeholder(tf.float32, [1, self.lstm_cell.state_size.c], name='c_in')
            h_in = tf.placeholder(tf.float32, [1, self.lstm_cell.state_size.h], name='h_in')
            self.state_in = (c_in, h_in)
            rnn_in = tf.expand_dims(l_ac, [0])
            state_in = tf.nn.rnn_cell.LSTMStateTuple(c_in, h_in)
            lstm_outputs, lstm_state = tf.nn.dynamic_rnn(
                self.lstm_cell, rnn_in, initial_state=state_in,
                time_major=False)
            lstm_c, lstm_h = lstm_state
            self.state_out = (lstm_c[:1, :], lstm_h[:1, :])
            rnn_out = tf.reshape(lstm_outputs, [-1, 256])

            w_init = tf.random_normal_initializer(0., .1)

            with tf.variable_scope('actor'):
                self.mu = tf.layers.dense(rnn_out, N_A, tf.nn.tanh, kernel_initializer=w_init, bias_initializer=tf.constant_initializer(0.1),
                                          name='mu')  # estimated action value
                self.sigma = tf.layers.dense(rnn_out, N_A, tf.nn.softplus, kernel_initializer=w_init, bias_initializer=tf.constant_initializer(0.1),
                                             name='sigma')  # estimated variance

            with tf.variable_scope('critic'):
                self.v = tf.layers.dense(rnn_out, 1, kernel_initializer=w_init, name='v')  # estimated value for state

            self.a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope) + tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/actor')
            self.c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope) + tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/critic')

            if scope != GLOBAL_NET_SCOPE:  # get global network
                self.v_target = tf.placeholder(tf.float32, [None, 1], 'Vtarget')
                self.a_his = tf.placeholder(tf.float32, [None, N_A], 'A')

                self.td = tf.subtract(self.v_target, self.v, name='TD_error')
                self.c_loss = tf.reduce_mean(tf.square(self.td))

                self.mu, self.sigma = tf.squeeze(self.mu*1), tf.squeeze(self.sigma + 0.1)

                normal_dist = tf.contrib.distributions.Normal(self.mu, self.sigma)

                log_prob = normal_dist.log_prob(self.a_his)
                exp_v = log_prob * self.td
                entropy = normal_dist.entropy()  # encourage exploration
                self.exp_v = ENTROPY_BETA * entropy + exp_v
                self.a_loss = tf.reduce_mean(-self.exp_v)

                self.A = tf.clip_by_value(tf.squeeze(normal_dist.sample(1), axis=0), A_BOUND[0],
                                          A_BOUND[1])  # sample a action from distribution
                self.a_grads = tf.gradients(self.a_loss,
                                            self.a_params)  # calculate gradients for the network weights
                self.c_grads = tf.gradients(self.c_loss, self.c_params)

                self.pull_a_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.a_params, globalAC.a_params)]
                self.pull_c_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.c_params, globalAC.c_params)]
                self.update_a_op = self.actor_optimizer.apply_gradients(zip(self.a_grads, globalAC.a_params))
                self.update_c_op = self.critic_optimizer.apply_gradients(zip(self.c_grads, globalAC.c_params))

    def update_global(self, feed_dict):  # run by a local
        return self.sess.run([self.update_a_op, self.update_c_op], feed_dict)  # local grads applies to global net

    def pull_global(self):  # run by a local
        self.sess.run([self.pull_a_params_op, self.pull_c_params_op])

    def choose_action(self, nodes, children, rnn_state):  # run by a local
        return self.sess.run([self.A, self.state_out],
                             {self.nodes: nodes, self.children: children, self.state_in[0]: rnn_state[0],
                              self.state_in[1]: rnn_state[1]})

    def pooling_layer(self, nodes):
        """Creates a max dynamic pooling layer from the nodes."""
        with tf.name_scope("pooling"):
            pooled = tf.reduce_max(nodes, axis=1)
            return pooled
