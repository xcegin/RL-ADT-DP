import pickle
import time

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

# Set learning parameters
from ADT.Utils.ResolverUtil import getNumOfReasonableNodes
from Agent.Convolutional.GeneratorSamples import batch_samples, gen_samples, Batcher
from Agent.Convolutional.QNetworkAgentConvolutional import Q_Network_Convolutional
from Environment.ExperienceReplay import experience_buffer, updateTargetGraph, updateTarget
from Environment.enviroment import Enviroment

exploration = "boltzmann"  # Exploration method. Choose between: greedy, random, e-greedy, boltzmann, bayesian.
y = 1  # Discount factor.
num_episodes = 100  # Total number of episodes to train network for.
tau = 0.001  # Amount to update target network at each step.
batch_size = 32  # Size of training batch
startE = 1  # Starting chance of random action
endE = 0.01  # Final chance of random action
anneling_steps = 1000  # How many steps of training to reduce startE to endE.
pre_train_steps = 500  # Number of steps used before training updates begin.
num_steps_upd = 10  # How often to perform a training step.
tf.reset_default_graph()

# create lists to contain total rewards and steps per episode
cList = []
cMeans = []
rList = []
episodeList = []
rMeans = []
with open('vectors_cov.pkl', 'rb') as fh:
    embeddings, embed_lookup = pickle.load(fh)
    num_feats = len(embeddings[0])
q_net = Q_Network_Convolutional(num_feats)
target_net = Q_Network_Convolutional(num_feats)

init = tf.global_variables_initializer()
trainables = tf.trainable_variables()
targetOps = updateTargetGraph(trainables, tau)
myBuffer = experience_buffer()

with tf.Session() as sess:
    sess.run(init)
    updateTarget(targetOps, sess)
    e = startE
    batcher = Batcher()
    stepDrop = (startE - endE) / anneling_steps
    total_steps = 0
    k = 0
    m = 0
    for k in range(num_episodes):
        env = Enviroment()
        rAll = 0
        cAll = 0
        d = False
        m = 0
        while m < len(env.listOfFiles):
            m += 1
            env.prepareNextFileConvWithCov()
            env.currentNumOfTable = 0
            while env.currentNumOfTable < len(env.listOfTables):
                env.startTable()
                running_reward = 0
                ep_history = []
                env.currentNumOfRow = 0
                for currentRow in env.listOfTableVectors:
                    numOfTimes = 0
                    d = False
                    env.initializeArgumentValuesCov()
                    complexity = getNumOfReasonableNodes(currentRow)
                    # complexity = int(complexity ** (1/3) * (len(env.listOfTables[0]) ** (1/3)))
                    complexity = int(complexity ** (1 / 4))
                    if complexity == 0:
                        complexity = 1
                    total = len(env.arguments)*len(env.listOfTables[0])*complexity
                    while numOfTimes < total:  # TODO REPLACE FOR REAL COUNT OF FUNCTION SIZE OR SMS
                        if d:
                            break
                        # num_batches = len(env.listOfTableVectors) // 1 + (1 if len(row) % 1 != 0 else 0)
                        batches = list(enumerate(batch_samples(gen_samples(currentRow, embeddings, embed_lookup), 1)))
                        # numOfTimes = int(round(len(batches[0][1][0][0])) ** (1 / 3)) + 1
                        # for x in range(0, numOfTimes*5):
                        #    batches = list(enumerate(batch_samples(gen_samples(row, embeddings, embed_lookup), 1)))
                        iterator = iter(batches)
                        batch = next(iterator, None)
                        while batch is not None:
                            i = 0
                            if isinstance(batch[0], int):
                                num, batch = batch
                            nodes, children = batch
                            batcher.checkMaxDim(nodes)
                            a = None
                            if exploration == "greedy":
                                # Choose an action with the maximum expected value.
                                a, allQ = sess.run([q_net.predict, q_net.Q_out],
                                                   feed_dict={
                                                       q_net.nodes: nodes,
                                                       q_net.children: children,
                                                       q_net.keep_per: 1.0})
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
                                                       feed_dict={
                                                           q_net.nodes: nodes,
                                                           q_net.children: children, q_net.keep_per: 1.0})
                                    a = a[0]
                            if exploration == "boltzmann":
                                # Choose an action probabilistically, with weights relative to the Q-values.
                                Q_d, allQ = sess.run([q_net.Q_dist, q_net.Q_out],
                                                     feed_dict={
                                                         q_net.nodes: nodes,
                                                         q_net.children: children, q_net.Temp: e,
                                                         q_net.keep_per: 1.0})
                                a = np.random.choice(Q_d[0], p=Q_d[0])
                                a = np.argmax(Q_d[0] == a)
                            if exploration == "bayesian":
                                # Choose an action using a sample from a dropout approximation of a bayesian q-network.
                                a, allQ = sess.run([q_net.predict, q_net.Q_out],
                                                   feed_dict={
                                                       q_net.nodes: nodes,
                                                       q_net.children: children, q_net.keep_per: (1 - e) + 0.1})
                                a = a[0]

                            r, d, c, _ = env.step_cov(a, 0, m - 1)
                            nextBatch = next(iterator, None)
                            if nextBatch is not None:
                                nextNodes, nextChildren = nextBatch
                                batch = nextBatch
                                myBuffer.add(
                                    np.reshape(np.array([nodes, children, a, r, d]),
                                               [1, 5]))
                            if nextBatch is None:
                                myBuffer.add(
                                    np.reshape(np.array([nodes, children, a, r, d]), [1, 5]))
                                batch = nextBatch
                            running_reward += r

                            if e > endE and total_steps > pre_train_steps:
                                e -= stepDrop

                            if total_steps > pre_train_steps and total_steps % num_steps_upd == 0:
                                # We use Double-DQN training algorithm
                                # TODO: CHECK BUFFER BATCH SIZES - Should be good
                                trainBatch = myBuffer.sample(batch_size)
                                batcher.pad(trainBatch[:, 0], num_feats)
                                batcher.init_child()
                                batcher.pad_child(trainBatch[:, 1])
                                Q1 = sess.run(q_net.predict,
                                              feed_dict={q_net.nodes: np.vstack(trainBatch[:, 0]),
                                                         q_net.children: np.vstack(trainBatch[:, 1]),
                                                         q_net.keep_per: 1.0})
                                Q2 = sess.run(target_net.Q_out,
                                              feed_dict={target_net.nodes: np.vstack(trainBatch[:, 0]),
                                                         target_net.children: np.vstack(trainBatch[:, 1]),
                                                         target_net.keep_per: 1.0})
                                end_multiplier = -(trainBatch[:, 4] - 1)
                                doubleQ = Q2[range(batch_size), Q1]
                                targetQ = trainBatch[:, 3] + (y * doubleQ * end_multiplier)
                                _ = sess.run(q_net.updateModel,
                                             feed_dict={q_net.nodes: np.vstack(trainBatch[:, 0]),
                                                        q_net.children: np.vstack(trainBatch[:, 1]),
                                                        q_net.nextQ: targetQ,
                                                        q_net.keep_per: 1.0, q_net.actions: trainBatch[:, 2]})
                                updateTarget(targetOps, sess)
                            i += 1
                            total_steps += 1
                            if d or (numOfTimes+1 == total):
                                rAll += r
                                cAll += c
                                break
                        numOfTimes += 1
        rList.append(rAll)
        cList.append(cAll)
        if k % 5 == 0 and k != 0:
            r_mean = np.mean(rList[-5:])
            c_mean = np.mean(cList[-5:])
            if exploration == 'e-greedy':
                print("Mean Reward: " + str(r_mean) + " Total Steps: " + str(total_steps) + " e: " + str(e))
            if exploration == 'boltzmann':
                with open("results.txt", "a") as text_file:
                    text_file.write("Mean Reward: " + str(r_mean) + " Total Steps: " + str(total_steps) + " t: " + str(e) + "\n")
                print("Mean Reward: " + str(r_mean) + " Total Steps: " + str(total_steps) + " t: " + str(e))
            if exploration == 'bayesian':
                print("Mean Reward: " + str(r_mean) + " Total Steps: " + str(total_steps) + " p: " + str(e))
            if exploration == 'random' or exploration == 'greedy':
                print("Mean Reward: " + str(r_mean) + " Total Steps: " + str(total_steps))
            print("Mean Coverage: " + str(c_mean) + " Total Steps: " + str(total_steps))
            with open("results.txt", "a") as text_file:
                text_file.write("Mean Coverage: " + str(c_mean) + " Mean Reward: " + str(r_mean) + " Total Steps: " + str(total_steps) + "\n")
            cMeans.append(c_mean)
            rMeans.append(r_mean)
            episodeList.append((k / 5) + 1)

plt.plot(episodeList, cMeans)
plt.title("Q-learning Boltzmann")
plt.xlabel('Number of episodes in 5')
plt.ylabel('Coverage achieved')
plt.show()
print("Percent of successful episodes: " + str(sum(rList) / num_episodes) + "%")
