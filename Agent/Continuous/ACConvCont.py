import numpy as np
import tensorflow as tf
from tensorflow.contrib import slim

from Agent.Convolutional.ConvolutionaLayer import conv_layer

GLOBAL_NET_SCOPE = 'Global_Net'
UPDATE_GLOBAL_ITER = 10     # sets how often the global net is updated
GAMMA = 0.90                # discount factor
ENTROPY_BETA = 0.01         # entropy factor
LR_A = 0.001               # learning rate for actor
LR_C = 0.001                # learning rate for critic

N_A = 1                      # number of actions
A_BOUND = [-255, 255]


class ACNet(object):
    def __init__(self, scope, sess, feature_size, globalAC=None):
        self.sess = sess
        self.actor_optimizer = tf.train.RMSPropOptimizer(learning_rate=LR_A, name='RMSPropA', decay=0.99, epsilon=0.01)  # optimizer for the actor
        self.critic_optimizer = tf.train.RMSPropOptimizer(learning_rate=LR_C, name='RMSPropC', decay=0.99, epsilon=0.01)  # optimizer for the critic

        if scope == GLOBAL_NET_SCOPE:  # get global network
            with tf.variable_scope(scope):
                self.nodes = tf.placeholder(tf.float32, shape=(None, None, feature_size), name='tree')
                self.children = tf.placeholder(tf.int32, shape=(None, None, None), name='children')

                self.conv = conv_layer(1, 100, self.nodes, self.children, feature_size)
                self.pooling = self.pooling_layer(self.conv)

                self.hidden = slim.fully_connected(self.pooling, 256, activation_fn=tf.nn.tanh, biases_initializer=None)

                self.a_params, self.c_params = self._build_net(scope)[-2:]  # parameters of actor and critic net
        else:  # local net, calculate losses
            with tf.variable_scope(scope):
                self.nodes = tf.placeholder(tf.float32, shape=(None, None, feature_size), name='tree')
                self.children = tf.placeholder(tf.int32, shape=(None, None, None), name='children')

                self.conv = conv_layer(1, 100, self.nodes, self.children, feature_size)
                self.pooling = self.pooling_layer(self.conv)

                self.hidden = slim.fully_connected(self.pooling, 256, activation_fn=tf.nn.tanh, biases_initializer=None)

                self.a_his = tf.placeholder(tf.float32, [None, N_A], 'A')  # action
                self.v_target = tf.placeholder(tf.float32, [None, 1], 'Vtarget')  # v_target value

                mu, sigma, self.v, self.a_params, self.c_params = self._build_net(
                    scope)  # get mu and sigma of estimated action from neural net

                td = tf.subtract(self.v_target, self.v, name='TD_error')
                with tf.name_scope('c_loss'):
                    self.c_loss = tf.reduce_mean(tf.square(td))

                with tf.name_scope('wrap_a_out'):
                    mu, sigma = mu * A_BOUND[1], sigma + 1e-4

                normal_dist = tf.contrib.distributions.Normal(mu, sigma)

                with tf.name_scope('a_loss'):
                    log_prob = normal_dist.log_prob(self.a_his)
                    exp_v = log_prob * td
                    entropy = normal_dist.entropy()  # encourage exploration
                    self.exp_v = ENTROPY_BETA * entropy + exp_v
                    self.a_loss = tf.reduce_mean(-self.exp_v)

                with tf.name_scope('choose_a'):  # use local params to choose action
                    self.A = tf.clip_by_value(tf.squeeze(normal_dist.sample(1), axis=0), A_BOUND[0],
                                              A_BOUND[1])  # sample a action from distribution
                with tf.name_scope('local_grad'):
                    self.a_grads = tf.gradients(self.a_loss,
                                                self.a_params)  # calculate gradients for the network weights
                    self.c_grads = tf.gradients(self.c_loss, self.c_params)

            with tf.name_scope('sync'):  # update local and global network weights
                with tf.name_scope('pull'):
                    self.pull_a_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.a_params, globalAC.a_params)]
                    self.pull_c_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.c_params, globalAC.c_params)]
                with tf.name_scope('push'):
                    self.update_a_op = self.actor_optimizer.apply_gradients(zip(self.a_grads, globalAC.a_params))
                    self.update_c_op = self.critic_optimizer.apply_gradients(zip(self.c_grads, globalAC.c_params))

    def _build_net(self, scope):  # neural network structure of the actor and critic
        w_init = tf.random_normal_initializer(0., .1)
        with tf.variable_scope('actor'):
            l_a = tf.layers.dense(self.hidden, 200, tf.nn.tanh, kernel_initializer=w_init, name='la')
            mu = tf.layers.dense(l_a, N_A, tf.nn.tanh, kernel_initializer=w_init, name='mu')  # estimated action value
            sigma = tf.layers.dense(l_a, N_A, tf.nn.softplus, kernel_initializer=w_init,
                                    name='sigma')  # estimated variance
        with tf.variable_scope('critic'):
            l_c = tf.layers.dense(self.hidden, 200, tf.nn.tanh, kernel_initializer=w_init, name='lc')
            v = tf.layers.dense(l_c, 1, kernel_initializer=w_init, name='v')  # estimated value for state
        a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/actor')
        c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/critic')
        return mu, sigma, v, a_params, c_params

    def update_global(self, feed_dict):  # run by a local
        self.sess.run([self.update_a_op, self.update_c_op], feed_dict)  # local grads applies to global net

    def pull_global(self):  # run by a local
        self.sess.run([self.pull_a_params_op, self.pull_c_params_op])

    def choose_action(self, nodes, children):  # run by a local
        return self.sess.run(self.A, {self.nodes: nodes, self.children: children})[0]

    def pooling_layer(self, nodes):
        """Creates a max dynamic pooling layer from the nodes."""
        with tf.name_scope("pooling"):
            pooled = tf.reduce_max(nodes, axis=1)
            return pooled
