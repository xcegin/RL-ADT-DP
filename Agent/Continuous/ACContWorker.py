import pickle

import numpy as np
import tensorflow as tf
from tensorflow.contrib import slim

from Agent.Continuous.ACConvCont import ACNet
from Agent.Convolutional.ConvolutionaLayer import conv_layer
from Agent.Convolutional.GeneratorSamples import Batcher, batch_samples, gen_samples
from Environment.enviroment import Enviroment

OUTPUT_GRAPH = True  # safe logs
RENDER = True  # render one worker
LOG_DIR = './log'  # savelocation for logs
MAX_EP_STEP = 200  # maxumum number of steps per episode
MAX_GLOBAL_EP = 2000  # total number of episodes
GLOBAL_NET_SCOPE = 'Global_Net'
GAMMA = 0.90  # discount factor
ENTROPY_BETA = 0.01  # entropy factor

N_A = 1  # number of actions
A_BOUND = [-1, 1]


class Worker(object):
    def __init__(self, name, globalAC, sess, global_rewards, global_episodes):
        self.summary_writer = tf.summary.FileWriter("logs/train_" + str(name))
        self.name = "worker_" + str(name)
        self.global_rewards = global_rewards
        self.global_episodes = global_episodes
        self.increment = self.global_episodes.assign_add(1)

        with open('vectors.pkl', 'rb') as fh:
            self.embeddings, self.embed_lookup = pickle.load(fh)
            self.num_feats = len(self.embeddings[0])

        self.AC = ACNet(self.name, sess, self.num_feats, globalAC)  # create ACNet for each worker
        self.sess = sess
        self.episode_rewards = []
        self.episode_lengths = []

        self.batcher = Batcher()
        self.env = Enviroment()

    def work(self, sess, coord):
        episode_count = sess.run(self.global_episodes)
        total_step = 1
        buffer_s, buffer_a = [], []
        print("Starting " + str(self.name))
        with sess.as_default(), sess.graph.as_default():
            while not coord.should_stop():
                self.env = Enviroment()
                self.batcher = Batcher()
                episode_buffer = []
                buffer_r = []
                buffer_v_target = []
                episode_reward = 0
                rnn_state = self.AC.state_init
                episode_step_count = 0
                m = 0

                while m < len(self.env.listOfFiles):
                    m += 1
                    self.env.prepareNextFileConv()
                    self.env.currentNumOfTable = 0
                    while self.env.currentNumOfTable < len(self.env.listOfTables):
                        self.env.startTable()
                        self.env.currentNumOfRow = 0
                        for currentRow in self.env.listOfTableVectors:
                            for row in currentRow:
                                # self.env.initializeArgumentValues()
                                batches = list(
                                    enumerate(batch_samples(gen_samples(row, self.embeddings, self.embed_lookup), 1)))
                                iterator = iter(batches)
                                batch = next(iterator, None)
                                k = 0
                                while k < 10:
                                    q = 0
                                    self.env.initializeArgumentValues()
                                    while q < 10 * len(list(self.env.argumentValues.keys())):
                                        # self.env.initializeArgumentValues()
                                        if isinstance(batch[0], int):
                                            num, batch = batch
                                        nodes, children = batch
                                        a, rnn_state = self.AC.choose_action(nodes, children, rnn_state)
                                        self.batcher.checkMaxDim(nodes)

                                        r, d, _ = self.env.step_continuos(a, m - 1)
                                        # nextBatch = next(iterator, None)
                                        buffer_r.append(r)
                                        episode_step_count += 1

                                        # batch = nextBatch
                                        episode_buffer.append([nodes, children, a, r, d])
                                        q += 1
                                        total_step += 1

                                        if len(episode_buffer) == 10 * len(
                                                list(self.env.argumentValues.keys())) or d:  # TODO - really not done?
                                            # Since we don't know what the true final return is, we "bootstrap" from our current
                                            # value estimation.
                                            if d:
                                                v_s_ = 0  # terminal
                                            else:
                                                v_s_ = self.sess.run(self.AC.v, {self.AC.nodes: nodes,
                                                                                 self.AC.children: children,
                                                                                 self.AC.state_in[0]: rnn_state[0],
                                                                                 self.AC.state_in[1]: rnn_state[1]})[0, 0]
                                            buffer_v_target = []

                                            rollout = np.array(episode_buffer)

                                            self.batcher.pad(rollout[:, 0], self.num_feats)
                                            self.batcher.init_child()
                                            self.batcher.pad_child(rollout[:, 1])

                                            for r in buffer_r[::-1]:  # reverse buffer r
                                                v_s_ = r + GAMMA * v_s_
                                                buffer_v_target.append(v_s_)
                                            buffer_v_target.reverse()

                                            buffer_s, buffer_a, buffer_c, buffer_v_target = np.vstack(
                                                rollout[:, 0]), np.vstack(
                                                rollout[:, 2]), np.vstack(rollout[:, 1]), np.vstack(
                                                buffer_v_target)
                                            feed_dict = {
                                                self.AC.nodes: buffer_s,
                                                self.AC.children: buffer_c,
                                                self.AC.a_his: buffer_a,
                                                self.AC.v_target: buffer_v_target,
                                                self.AC.state_in[0]: rnn_state[0],
                                                self.AC.state_in[1]: rnn_state[1]
                                            }
                                            self.AC.update_global(
                                                feed_dict)  # actual training step, update global ACNet
                                            buffer_s, buffer_a, buffer_r, buffer_c = [], [], [], []
                                            episode_buffer = []
                                            self.AC.pull_global()  # get global parameters to local ACNet
                                        # if episode_step_count >= max_episode_length - 1 or d or nextBatch is None:
                                        if q == 10 * len(list(self.env.argumentValues.keys())) or d:
                                            episode_reward += r
                                            break
                                    k += 1

                self.episode_rewards.append(episode_reward)
                self.episode_lengths.append(episode_step_count)

                if episode_count % 3 == 0 and episode_count != 0:
                    # if episode_count % 200 == 0 and self.name == 'worker_0':
                    # saver.save(sess, self.model_path + '/model-' + str(episode_count) + '.cptk')
                    # print("Saved Model")

                    mean_reward = np.mean(self.episode_rewards[-3:])
                    mean_length = np.mean(self.episode_lengths[-3:])
                    summary = tf.Summary()
                    summary.value.add(tag='Perf/Reward', simple_value=float(mean_reward))
                    summary.value.add(tag='Perf/Length', simple_value=float(mean_length))
                    self.summary_writer.add_summary(summary, episode_count)

                    self.summary_writer.flush()

                sess.run(self.increment)
                episode_count += 1