import csv
import os

import numpy as np
import tensorflow as tf

from Agent.RQNetworkAgent import RQnetwork
from Enviroment.ExperienceReplay import experience_buffer, updateTargetGraph, updateTarget, processState
from Enviroment.enviroment import Enviroment

env = Enviroment()

# Setting the training parameters
batch_size = 4  # How many experience traces to use for each training step.
trace_length = 8  # How long each experience trace will be when training
update_freq = 5  # How often to perform a training step.
y = .99  # Discount factor on the target Q-values
startE = 1  # Starting chance of random action
endE = 0.01  # Final chance of random action
anneling_steps = 10000  # How many steps of training to reduce startE to endE.
num_episodes = 10000  # How many episodes of game environment to train network with.
pre_train_steps = 10000  # How many steps of random actions before training begins.
load_model = False  # Whether to load a saved model.
path = "./drqn"  # The path to save our model to.
h_size = 512  # The size of the final convolutional layer before splitting it into Advantage and Value streams.
max_epLength = 50  # The max allowed length of our episode.
time_per_step = 1  # Length of each step used in gif creation
summaryLength = 100  # Number of epidoes to periodically save for analysis
tau = 0.001

tf.reset_default_graph()
# We define the cells for the primary and target q-networks
cell = tf.contrib.rnn.BasicLSTMCell(num_units=h_size, state_is_tuple=True)
cellT = tf.contrib.rnn.BasicLSTMCell(num_units=h_size, state_is_tuple=True)
mainQN = RQnetwork(h_size, cell, 'main')
targetQN = RQnetwork(h_size, cellT, 'target')

init = tf.global_variables_initializer()

saver = tf.train.Saver(max_to_keep=5)

trainables = tf.trainable_variables()

targetOps = updateTargetGraph(trainables, tau)

myBuffer = experience_buffer()

# Set the rate of random action decrease.
e = startE
stepDrop = (startE - endE) / anneling_steps

# create lists to contain total rewards and steps per episode
jList = []
rList = []
total_steps = 0

# Make a path for our model to be saved in.
if not os.path.exists(path):
    os.makedirs(path)

##Write the first line of the master log-file for the Control Center
with open('./Center/log.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(['Episode', 'Length', 'Reward', 'IMG', 'LOG', 'SAL'])

with tf.Session() as sess:
    if load_model == True:
        print('Loading Model...')
        ckpt = tf.train.get_checkpoint_state(path)
        saver.restore(sess, ckpt.model_checkpoint_path)
    sess.run(init)
    total_steps = 0
    k = 0
    m = 0
    updateTarget(targetOps, sess)  # Set the target network to be equal to the primary network.
    while m < len(env.listOfFiles):
        env.prepareNextFile()
        for k in range(num_episodes):
            episodeBuffer = []
            state = (np.zeros([1, h_size]), np.zeros([1, h_size]))  # Reset the recurrent layer's hidden state
            rAll = 0
            d = False
            i = 0
            while i < len(env.listOfTables):
                env.startTable()
                running_reward = 0  # TODO: check the position of running_reward
                ep_history = []
                j = 0
                while j < len(env.currentVectors):
                    s = env.startRow(m)
                    numOfVectors = 1
                    while numOfVectors < len(env.currentVectorRow):
    for i in range(num_episodes):
        episodeBuffer = []
        # Reset environment and get first new observation
        sP = env.reset()
        s = processState(sP)
        d = False
        rAll = 0
        j = 0
        state = (np.zeros([1, h_size]), np.zeros([1, h_size]))  # Reset the recurrent layer's hidden state
        # The Q-Network
        while j < max_epLength:
            j += 1
            # Choose an action by greedily (with e chance of random action) from the Q-network
            if np.random.rand(1) < e or total_steps < pre_train_steps:
                state1 = sess.run(mainQN.rnn_state,
                                  feed_dict={mainQN.inputs: [s], mainQN.trainLength: 1,
                                             mainQN.state_in: state, mainQN.batch_size: 1})
                a = env.action_space.sample()
            else:
                a, state1 = sess.run([mainQN.predict, mainQN.rnn_state],
                                     feed_dict={mainQN.inputs: [s], mainQN.trainLength: 1,
                                                mainQN.state_in: state, mainQN.batch_size: 1})
                a = a[0]
            r, d, _ = env.step(a,m)
            s1 = env.currentVectorRow[numOfVectors]
            numOfVectors += 1
            #total_steps += 1
            episodeBuffer.append(np.reshape(np.array([s, a, r, s1, d]), [1, 5]))
            if total_steps > pre_train_steps:
                if e > endE:
                    e -= stepDrop

                if total_steps % (update_freq) == 0:
                    updateTarget(targetOps, sess)
                    # Reset the recurrent layer's hidden state
                    state_train = (np.zeros([batch_size, h_size]), np.zeros([batch_size, h_size]))

                    trainBatch = myBuffer.sampleDRQN(batch_size, trace_length)  # Get a random batch of experiences.
                    # Below we perform the Double-DQN update to the target Q-values
                    Q1 = sess.run(mainQN.predict, feed_dict={
                        mainQN.inputs: np.vstack(trainBatch[:, 3]),
                        mainQN.trainLength: trace_length, mainQN.state_in: state_train, mainQN.batch_size: batch_size})
                    Q2 = sess.run(targetQN.Qout, feed_dict={
                        targetQN.inputs: np.vstack(trainBatch[:, 3]),
                        targetQN.trainLength: trace_length, targetQN.state_in: state_train,
                        targetQN.batch_size: batch_size})
                    end_multiplier = -(trainBatch[:, 4] - 1)
                    doubleQ = Q2[range(batch_size * trace_length), Q1]
                    targetQ = trainBatch[:, 2] + (y * doubleQ * end_multiplier)
                    # Update the network with our target values.
                    sess.run(mainQN.updateModel,
                             feed_dict={mainQN.inputs: np.vstack(trainBatch[:, 0]),
                                        mainQN.targetQ: targetQ,
                                        mainQN.actions: trainBatch[:, 1], mainQN.trainLength: trace_length,
                                        mainQN.state_in: state_train, mainQN.batch_size: batch_size})
            rAll += r
            s = s1
            sP = s1P
            state = state1
            if d:
                break

        # Add the episode to the experience buffer
        bufferArray = np.array(episodeBuffer)
        episodeBuffer = list(zip(bufferArray))
        myBuffer.add(episodeBuffer)
        jList.append(j)
        rList.append(rAll)

        # Periodically save the model.
        if i % 1000 == 0 and i != 0:
            saver.save(sess, path + '/model-' + str(i) + '.cptk')
            print("Saved Model")
        if len(rList) % summaryLength == 0 and len(rList) != 0:
            print(total_steps, np.mean(rList[-summaryLength:]), e)
    saver.save(sess, path + '/model-' + str(i) + '.cptk')
