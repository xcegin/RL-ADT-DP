import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Set learning parameters
from Agent.QNetworkAgent import Q_Network
from Environment.ExperienceReplay import experience_buffer, updateTargetGraph, updateTarget
from Environment.enviroment import Enviroment


exploration = "boltzmann"  # Exploration method. Choose between: greedy, random, e-greedy, boltzmann, bayesian.
y = .99  # Discount factor.
num_episodes = 5000  # Total number of episodes to train network for.
tau = 0.001  # Amount to update target network at each step.
batch_size = 64  # Size of training batch
startE = 1  # Starting chance of random action
endE = 0.01  # Final chance of random action
anneling_steps = 200000  # How many steps of training to reduce startE to endE.
pre_train_steps = 50000  # Number of steps used before training updates begin.
num_steps_upd = 5  # How often to perform a training step.
tf.reset_default_graph()

q_net = Q_Network()
target_net = Q_Network()

init = tf.initialize_all_variables()
trainables = tf.trainable_variables()
targetOps = updateTargetGraph(trainables, tau)
myBuffer = experience_buffer()

# create lists to contain total rewards and steps per episode
jList = []
jMeans = []
rList = []
episodeList = []
rMeans = []
with tf.Session() as sess:
    sess.run(init)
    updateTarget(targetOps, sess)
    e = startE
    stepDrop = (startE - endE) / anneling_steps
    total_steps = 0
    k = 0
    m = 0
    for k in range(num_episodes):
        env = Enviroment()
        rAll = 0
        d = False
        m = 0
        while m < len(env.listOfFiles):
            m += 1
            env.prepareNextFile()
            env.currentNumOfTable = 0
            while env.currentNumOfTable < len(env.listOfTables):
                env.startTable()
                running_reward = 0  # TODO: check the position of running_reward
                ep_history = []
                env.currentNumOfRow = 0
                while env.currentNumOfRow < len(env.currentVectors):
                    s = env.startRow(m - 1)
                    numOfVectors = 1
                    while numOfVectors < len(env.currentVectorRow):
                        a = None
                        if exploration == "greedy":
                            # Choose an action with the maximum expected value.
                            a, allQ = sess.run([q_net.predict, q_net.Q_out],
                                               feed_dict={q_net.inputs: [s], q_net.keep_per: 1.0})
                            a = a[0]
                        if exploration == "random":
                            # Choose an action randomly.
                            a = env.action_space.sample()
                        if exploration == "e-greedy":
                            # Choose an action by greedily (with e chance of random action) from the Q-network
                            if np.random.rand(1) < e or total_steps < pre_train_steps:
                                a = env.action_space.sample()
                            else:
                                a, allQ = sess.run([q_net.predict, q_net.Q_out],
                                                   feed_dict={q_net.inputs: [s], q_net.keep_per: 1.0})
                                a = a[0]
                        if exploration == "boltzmann":
                            # Choose an action probabilistically, with weights relative to the Q-values.
                            Q_d, allQ = sess.run([q_net.Q_dist, q_net.Q_out],
                                                 feed_dict={q_net.inputs: [s], q_net.Temp: e, q_net.keep_per: 1.0})
                            a = np.random.choice(Q_d[0], p=Q_d[0])
                            a = np.argmax(Q_d[0] == a)
                        if exploration == "bayesian":
                            # Choose an action using a sample from a dropout approximation of a bayesian q-network.
                            a, allQ = sess.run([q_net.predict, q_net.Q_out],
                                               feed_dict={q_net.inputs: [s], q_net.keep_per: (1 - e) + 0.1})
                            a = a[0]

                        r, d, _ = env.step(a, m - 1)
                        s1 = env.currentVectorRow[numOfVectors]
                        numOfVectors += 1

                        myBuffer.add(np.reshape(np.array([s, a, r, s1, d]), [1, 5]))
                        running_reward += r

                        if e > endE and total_steps > pre_train_steps:
                            e -= stepDrop

                        if total_steps > pre_train_steps and total_steps % num_steps_upd == 0:
                            # We use Double-DQN training algorithm
                            trainBatch = myBuffer.sample(batch_size)
                            Q1 = sess.run(q_net.predict,
                                          feed_dict={q_net.inputs: np.vstack(trainBatch[:, 3]), q_net.keep_per: 1.0})
                            Q2 = sess.run(target_net.Q_out,
                                          feed_dict={target_net.inputs: np.vstack(trainBatch[:, 3]),
                                                     target_net.keep_per: 1.0})
                            end_multiplier = -(trainBatch[:, 4] - 1)
                            doubleQ = Q2[range(batch_size), Q1]
                            targetQ = trainBatch[:, 2] + (y * doubleQ * end_multiplier)
                            _ = sess.run(q_net.updateModel,
                                         feed_dict={q_net.inputs: np.vstack(trainBatch[:, 0]), q_net.nextQ: targetQ,
                                                    q_net.keep_per: 1.0, q_net.actions: trainBatch[:, 1]})
                            updateTarget(targetOps, sess)
                        if not numOfVectors < len(env.currentVectorRow):
                            rAll += r
                        s = s1
                        total_steps += 1
                        if d:
                            rAll += r
                            break
        rList.append(rAll)
        if k % 100 == 0 and k != 0:
            r_mean = np.mean(rList[-100:])
            if exploration == 'e-greedy':
                print("Mean Reward: " + str(r_mean) + " Total Steps: " + str(total_steps) + " e: " + str(e))
            if exploration == 'boltzmann':
                print("Mean Reward: " + str(r_mean) + " Total Steps: " + str(total_steps) + " t: " + str(e))
            if exploration == 'bayesian':
                print("Mean Reward: " + str(r_mean) + " Total Steps: " + str(total_steps) + " p: " + str(e))
            if exploration == 'random' or exploration == 'greedy':
                print("Mean Reward: " + str(r_mean) + " Total Steps: " + str(total_steps))
            rMeans.append(r_mean)
            episodeList.append((k / 100) + 1)

plt.plot(episodeList, rMeans)
plt.title("Q-learning Boltzmann")
plt.xlabel('Number of episodes in 100')
plt.ylabel('Accumulated reward')
plt.show()
print("Percent of successful episodes: " + str(sum(rList) / num_episodes) + "%")
