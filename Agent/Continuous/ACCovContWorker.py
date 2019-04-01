import pickle

import numpy as np
import tensorflow as tf

from ADT.Utils.ResolverUtil import getNumOfReasonableNodes
from Agent.Continuous.ACConvCont import ACNet
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


class ACCovContWorker(object):
    def __init__(self, name, globalAC, sess, global_rewards, global_episodes, model_path):
        self.number = str(name)
        self.summary_writer = tf.summary.FileWriter("logs/train_" + str(name))
        self.name = "worker_" + str(name)
        self.global_rewards = global_rewards
        self.global_episodes = global_episodes
        self.increment = self.global_episodes.assign_add(1)

        self.model_path = model_path

        with open('vectors_cov.pkl', 'rb') as fh:
            self.embeddings, self.embed_lookup = pickle.load(fh)
            self.num_feats = len(self.embeddings[0])

        self.AC = ACNet(self.name, sess, self.num_feats, globalAC)  # create ACNet for each worker
        self.sess = sess
        self.episode_rewards = []
        self.episode_coverages = []
        self.episode_lengths = []

        self.batcher = Batcher()
        self.env = Enviroment()
        self.avgFunctions = {}

    def getCovVector(self, c):
        if self.env.argumentChangedVal % len(list(self.env.arguments.keys())) == 0 and self.env.argumentChangedVal != 0:
            argColVal = (self.env.argumentColumnValue+1) % len(self.env.listOfTables[0])
            keyOfArg = (self.env.argumentChangedVal+1) % len(list(self.env.arguments.keys()))
        else:
            argColVal = (self.env.argumentColumnValue) % len(self.env.listOfTables[0])
            keyOfArg = (self.env.argumentChangedVal) % len(list(self.env.arguments.keys()))
        return [argColVal, keyOfArg, c]

    def work(self, sess, coord, saver):
        episode_count = sess.run(self.global_episodes)
        total_step = 1
        buffer_s, buffer_a = [], []
        print("Starting " + str(self.name))
        with sess.as_default(), sess.graph.as_default():
            while not coord.should_stop():
                self.env.reset()
                self.batcher = Batcher()
                episode_buffer = []
                buffer_r = []
                buffer_v_target = []
                episode_reward = 0
                episode_coverage = 0
                episode_step_count = 0
                m = 0
                rnn_state = self.AC.state_init

                while m < len(self.env.listOfFiles):
                    m += 1
                    self.env.prepareNextFileConvWithCov(self.number)
                    self.env.currentNumOfTable = 0
                    while self.env.currentNumOfTable < len(self.env.listOfTables):
                        self.env.startTable()
                        self.env.currentNumOfRow = 0
                        for currentRow in self.env.listOfTableVectors:
                            numOfTimes = 0
                            d = False
                            self.env.initializeArgumentValuesCov()
                            complexity = getNumOfReasonableNodes(currentRow)
                            #complexity = int(complexity ** (1/3) * (len(self.env.listOfTables[0]) ** (1/3)))
                            complexity = int(complexity ** (1 / 1))
                            c = 0
                            if complexity == 0:
                                complexity = 1
                            total = len(self.env.arguments) * len(self.env.listOfTables[0]) * complexity
                            while numOfTimes < total:
                                if d:
                                    break
                                # self.env.initializeArgumentValues()
                                batches = list(
                                    enumerate(batch_samples(gen_samples(currentRow, self.embeddings, self.embed_lookup), 1)))
                                iterator = iter(batches)
                                batch = next(iterator, None)
                                while batch is not None:
                                    # self.env.initializeArgumentValues()
                                    if isinstance(batch[0], int):
                                        num, batch = batch
                                    nodes, children = batch
                                    self.batcher.checkMaxDim(nodes)
                                    vectorMatrixWithCov = [self.getCovVector(c)]
                                    a, rnn_state = self.AC.choose_action(nodes, children, rnn_state, vectorMatrixWithCov)

                                    self.env.step_cov_continuos_with_reward(a, self.number)
                                    episode_buffer.append([nodes, children, a, vectorMatrixWithCov])
                                    if len(episode_buffer) % (len(self.env.arguments)*len(self.env.listOfTables[0])) == 0 and len(episode_buffer) != 0:
                                        r,d,c,_ = self.env.step_cov_continuos_entire_matrix(self.number)
                                        temp = 0
                                        while temp < len(self.env.arguments)*len(self.env.listOfTables[0]):
                                            buffer_r.append(r)
                                            temp += 1
                                    # nextBatch = next(iterator, None)
                                    total_step += 1
                                    episode_step_count += 1

                                    batch = next(iterator, None)

                                    if d or numOfTimes + 1 == total:
                                        # Since we don't know what the true final return is, we "bootstrap" from our current
                                        # value estimation.
                                        if d:
                                            v_s_ = 0  # terminal
                                        else:
                                            v_s_ = self.sess.run(self.AC.v, {self.AC.nodes: nodes,
                                                                             self.AC.children: children,
                                                                             self.AC.matrixWithCov: vectorMatrixWithCov,
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
                                        buffer_s, buffer_a, buffer_c, buffer_v_target, buffer_matrix_cov = np.vstack(
                                            rollout[:, 0]), np.vstack(
                                            rollout[:, 2]), np.vstack(rollout[:, 1]), np.vstack(
                                            buffer_v_target), np.vstack(rollout[:, 3])
                                        feed_dict = {
                                            self.AC.nodes: buffer_s,
                                            self.AC.children: buffer_c,
                                            self.AC.a_his: buffer_a,
                                            self.AC.v_target: buffer_v_target,
                                            self.AC.state_in[0]: rnn_state[0],
                                            self.AC.state_in[1]: rnn_state[1],
                                            self.AC.matrixWithCov: buffer_matrix_cov
                                        }
                                        self.AC.update_global(
                                            feed_dict)  # actual training step, update global ACNet
                                        buffer_s, buffer_a, buffer_r, buffer_c, buffer_matrix_cov = [], [], [], [], []
                                        episode_buffer = []
                                        self.AC.pull_global()  # get global parameters to local ACNet
                                    # if episode_step_count >= max_episode_length - 1 or d or nextBatch is None:
                                    if numOfTimes + 1 == total or d:
                                        episode_reward += r
                                        episode_coverage += c
                                        if self.env.rootTreeAdtNode.name not in self.avgFunctions:
                                            self.avgFunctions[self.env.rootTreeAdtNode.name] = [c]
                                        else:
                                            self.avgFunctions[self.env.rootTreeAdtNode.name].append(c)
                                        break
                                numOfTimes += 1
                                print(
                                    "Worker: " + str(self.number) + ", with number of times: " + str(numOfTimes) + ", for file: " + str(m))

                episode_count += 1
                print("Worker: " + str(self.number) + ", with number of episodes: " + str(episode_count))
                self.episode_rewards.append(episode_reward)
                self.episode_coverages.append(episode_coverage)
                self.episode_lengths.append(episode_step_count)

                if episode_count % 2 == 0 and episode_count != 0:
                    if episode_count % 200 == 0 and self.name == 'worker_0':
                        saver.save(sess, self.model_path + '/model-' + str(episode_count) + '.cptk')
                        print("Saved Model")

                    mean_reward = np.mean(self.episode_rewards[-2:])
                    mean_length = np.mean(self.episode_lengths[-2:])
                    mean_coverage = np.mean(self.episode_coverages[-2:])
                    summary = tf.Summary()
                    summary.value.add(tag='Perf/Reward', simple_value=float(mean_reward))
                    summary.value.add(tag='Perf/Length', simple_value=float(mean_length))
                    summary.value.add(tag='Perf/Coverage', simple_value=float(mean_coverage))
                    for key in self.env.dict_of_max_r.keys():
                        summary.value.add(tag='Max Functions/Max coverage for function: ' + str(key), simple_value=float(self.env.dict_of_max_r[key]))
                    for key in self.avgFunctions.keys():
                        summary.value.add(tag='Avg Functions/Avg coverage for function: ' + str(key), simple_value=float(np.mean(self.avgFunctions[key][-2:])))
                    self.summary_writer.add_summary(summary, episode_count)

                    self.summary_writer.flush()

                sess.run(self.increment)
