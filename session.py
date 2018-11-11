import tensorflow as tf
import numpy as np
from numpy.core.tests.test_mem_overlap import xrange

from Agent.ABCAgent import ABCAgent
from Enviroment.enviroment import Enviroment

tf.reset_default_graph() #Clear the Tensorflow graph.

env = Enviroment()

gamma = 0.99

def discount_rewards(r):
    """ take 1D float array of rewards and compute discounted reward """
    discounted_r = np.zeros_like(r)
    running_add = 0
    for t in reversed(xrange(0, r.size)):
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r

myAgent = ABCAgent(lr=1e-2,s_size=4,a_size=2,h_size=8) #Load the agent.

total_episodes = 5000 #Set total number of episodes to train agent on.
max_ep = 999
update_frequency = 5

init = tf.global_variables_initializer()

# Launch the tensorflow graph
with tf.Session() as sess:
    sess.run(init)
    i = 0
    j = 0
    total_reward = []
    total_lenght = []

    gradBuffer = sess.run(tf.trainable_variables())
    for ix, grad in enumerate(gradBuffer):
        gradBuffer[ix] = grad * 0

    while i < len(env.listOfTables):
        env.startTable()
        running_reward = 0
        ep_history = []
        s = env.startRow()
        while j < len(env.currentVectors):
            s = env.startRow()
            numOfVectors = 1
            while numOfVectors < len(env.currentVectorRow):
                a_dist = sess.run(myAgent.output, feed_dict={myAgent.state_in: [s]})
                a = np.random.choice(a_dist[0], p=a_dist[0])
                a = np.argmax(a_dist == a)

                r, d, _ = env.step(a)
                s1 = env.currentVector[numOfVectors]
                numOfVectors += 1

                ep_history.append([s, a, r, s1])
                s = s1
                running_reward += r

                if numOfVectors == len(env.currentVectorRow):
                    d = True

                if d == True:
                    # Update the network.
                    ep_history = np.array(ep_history)
                    ep_history[:, 2] = discount_rewards(ep_history[:, 2])
                    feed_dict = {myAgent.reward_holder: ep_history[:, 2],
                                 myAgent.action_holder: ep_history[:, 1], myAgent.state_in: np.vstack(ep_history[:, 0])}
                    grads = sess.run(myAgent.gradients, feed_dict=feed_dict)
                    for idx, grad in enumerate(grads):
                        gradBuffer[idx] += grad

                    if i % update_frequency == 0 and i != 0:
                        feed_dict = dictionary = dict(zip(myAgent.gradient_holders, gradBuffer))
                        _ = sess.run(myAgent.update_batch, feed_dict=feed_dict)
                        for ix, grad in enumerate(gradBuffer):
                            gradBuffer[ix] = grad * 0

                    total_reward.append(running_reward)
                    total_lenght.append(j)
                    break
