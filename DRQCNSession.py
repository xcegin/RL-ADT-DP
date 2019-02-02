import pickle

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

# Set learning parameters
from Agent.Convolutional.GeneratorSamples import batch_samples, gen_samples, Batcher
from Agent.Convolutional.RQNetworkAgentConvolutional import RQnetworkConvolutional
from Environment.ExperienceReplay import experience_buffer, updateTargetGraph, updateTarget
from Environment.enviroment import Enviroment

# Setting the training parameters
batch_size = 4  # How many experience traces to use for each training step.
trace_length = 4  # How long each experience trace will be when training
update_freq = 10  # How often to perform a training step.
y = .99  # Discount factor on the target Q-values
startE = 1  # Starting chance of random action
endE = 0.01  # Final chance of random action
anneling_steps = 1000  # How many steps of training to reduce startE to endE.
num_episodes = 25000  # How many episodes of game environment to train network with.
pre_train_steps = 500  # How many steps of random actions before training begins.
load_model = False  # Whether to load a saved model.
path = "./drqn"  # The path to save our model to.
h_size = 100
max_epLength = 100  # The max allowed length of our episode.
time_per_step = 1  # Length of each step used in gif creation
summaryLength = 100  # Number of epidsoes to periodically save for analysis
tau = 0.001

tf.reset_default_graph()

with open('vectors.pkl', 'rb') as fh:
    embeddings, embed_lookup = pickle.load(fh)
    num_feats = len(embeddings[0])

# We define the cells for the primary and target q-networks
cell = tf.nn.rnn_cell.LSTMCell(num_units=h_size, state_is_tuple=True)
cellT = tf.nn.rnn_cell.LSTMCell(num_units=h_size, state_is_tuple=True)
mainQN = RQnetworkConvolutional(h_size, cell, 'main', num_feats)
targetQN = RQnetworkConvolutional(h_size, cellT, 'target', num_feats)

init = tf.global_variables_initializer()
saver = tf.train.Saver(max_to_keep=5)
trainables = tf.trainable_variables()
targetOps = updateTargetGraph(trainables, tau)
myBuffer = experience_buffer()

# create lists to contain total rewards and steps per episode
rList = []
rMeans = []
episodeList = []
total_steps = 0
with tf.Session() as sess:
    sess.run(init)
    updateTarget(targetOps, sess)
    batcher = Batcher()
    e = startE
    stepDrop = (startE - endE) / anneling_steps
    k = 0
    m = 0
    for k in range(num_episodes):
        env = Enviroment()
        episodeBuffer = []
        rAll = 0
        d = False
        m = 0
        state = (np.zeros([1, h_size]), np.zeros([1, h_size]))
        while m < len(env.listOfFiles):
            m += 1
            env.prepareNextFileConv()
            env.currentNumOfTable = 0
            while env.currentNumOfTable < len(env.listOfTables):
                env.startTable()
                env.currentNumOfRow = 0
                for currentRow in env.listOfTableVectors:
                    for row in currentRow:
                        env.initializeArgumentValues()
                        batches = list(enumerate(batch_samples(gen_samples(row, embeddings, embed_lookup), 1)))
                        iterator = iter(batches)
                        batch = next(iterator, None)
                        while batch is not None:
                            i = 0
                            if isinstance(batch[0], int):
                                num, batch = batch
                            nodes, children = batch
                            batcher.checkMaxDim(nodes)
                            a = None
                            if np.random.rand(1) < e or total_steps < pre_train_steps:
                                state1 = sess.run(mainQN.rnn_state,  # why the fuck is this here if it doesnt do SHIT
                                                  feed_dict={mainQN.nodes: nodes, mainQN.children: children,
                                                             mainQN.trainLength: 1,
                                                             mainQN.state_in: state, mainQN.batch_size: 1})
                                a = env.action_space.sample()
                            else:
                                a, state1 = sess.run([mainQN.predict, mainQN.rnn_state],
                                                     feed_dict={mainQN.nodes: nodes, mainQN.children: children,
                                                                mainQN.trainLength: 1,
                                                                mainQN.state_in: state, mainQN.batch_size: 1})
                                a = a[0]

                            r, d, _ = env.step(a, m - 1)
                            nextBatch = next(iterator, None)
                            if nextBatch is not None:
                                nextNodes, nextChildren = nextBatch
                                batch = nextBatch
                                episodeBuffer.append(np.reshape(np.array([nodes, children, a, r, d]), [1, 5]))
                            if nextBatch is None:
                                episodeBuffer.append(np.reshape(np.array([nodes, children, a, r, d]), [1, 5]))
                                batch = nextBatch

                            if total_steps > pre_train_steps:
                                if e > endE:
                                    e -= stepDrop

                                if total_steps % update_freq == 0:
                                    updateTarget(targetOps, sess)
                                    # Reset the recurrent layer's hidden state
                                    state_train = (np.zeros([batch_size, h_size]), np.zeros([batch_size, h_size]))

                                    #trainBatch = myBuffer.sample_conv(batch_size)
                                    trainBatch = myBuffer.sampleDRQN(batch_size, trace_length)
                                    # Get a random
                                    # batch of experiences.
                                    batcher.pad(trainBatch[:, 0], num_feats)
                                    batcher.init_child()
                                    batcher.pad_child(trainBatch[:, 1])
                                    # Below we perform the Double-DQN update to the target Q-values
                                    Q1 = sess.run(mainQN.predict, feed_dict={
                                        mainQN.nodes: np.vstack(trainBatch[:, 0]),
                                        mainQN.children: np.vstack(trainBatch[:, 1]),
                                        mainQN.trainLength: trace_length, mainQN.state_in: state_train,
                                        mainQN.batch_size: batch_size})
                                    Q2 = sess.run(targetQN.Qout, feed_dict={
                                        targetQN.nodes: np.vstack(trainBatch[:, 0]),
                                        targetQN.children: np.vstack(trainBatch[:, 1]),
                                        targetQN.trainLength: trace_length, targetQN.state_in: state_train,
                                        targetQN.batch_size: batch_size})
                                    end_multiplier = -(trainBatch[:, 4] - 1)
                                    doubleQ = Q2[range(batch_size * trace_length), Q1]
                                    targetQ = trainBatch[:, 3] + (y * doubleQ * end_multiplier)
                                    # Update the network with our target values.
                                    sess.run(mainQN.updateModel,
                                             feed_dict={mainQN.nodes: np.vstack(trainBatch[:, 0]),
                                                        mainQN.children: np.vstack(trainBatch[:, 1]),
                                                        mainQN.targetQ: targetQ,
                                                        mainQN.actions: trainBatch[:, 2],
                                                        mainQN.trainLength: trace_length,
                                                        mainQN.state_in: state_train, mainQN.batch_size: batch_size})

                            state = state1
                            total_steps += 1
                            if nextBatch is None or d:
                                rAll += r
                                break
            # Episode magic here
        bufferArray = np.array(episodeBuffer)
        episodeBuffer = list(zip(bufferArray))
        myBuffer.addRQN(episodeBuffer)
        rList.append(rAll)
        if k % 100 == 0 and k != 0:
            r_mean = np.mean(rList[-100:])
            saver.save(sess, path + '/model-' + str(k/100) + '.cptk')
            print("Saved Model")
            rMeans.append(r_mean)
            episodeList.append((k / 100) + 1)
        if len(rList) % summaryLength == 0 and len(rList) != 0:
            print(total_steps, np.mean(rList[-summaryLength:]), e)
plt.plot(episodeList, rMeans)
plt.title("DRQN E-Greedy")
plt.xlabel('Number of episodes in 100')
plt.ylabel('Accumulated reward')
plt.show()
#print("Percent of successful episodes: " + str(sum(rList) / num_episodes) + "%")
