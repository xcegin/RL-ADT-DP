import pickle
from copy import deepcopy

"""Based on https://github.com/stefanbo92/A3C-Continuous"""

import numpy as np
import tensorflow as tf

from ADT.Utils.ResolverUtil import getNumOfReasonableNodes
from Agent.Continuous.ACConvCont import ACNet
from Agent.Convolutional.GeneratorSamples import Batcher, batch_samples, gen_samples, traverse_tree_in_dfs_inorder
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

# Worker for A3C continous action space
class ACCovContWorker(object):
    def __init__(self, name, globalAC, sess, global_rewards, global_episodes, model_path):
        self.number = str(name)
        self.summary_writer = tf.summary.FileWriter("logs/train_" + str(name))
        self.name = "worker_" + str(name)
        self.global_rewards = global_rewards
        self.global_episodes = global_episodes
        self.increment = self.global_episodes.assign_add(1)

        self.model_path = model_path

        with open('vectors_nextDate.pkl', 'rb') as fh:
            self.embeddings, self.embed_lookup = pickle.load(fh)
            self.num_feats = len(self.embeddings[0])

        self.AC = ACNet(self.name, sess, self.num_feats, globalAC)  # create ACNet for each worker
        self.sess = sess
        self.episode_rewards = []
        self.episode_coverages = []
        self.episode_lengths = []
        self.a_loss = []
        self.c_loss = []

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
                self.batch_rnn_state = rnn_state
                while m < len(self.env.listOfFiles):
                    m += 1
                    self.env.prepareNextFileConv()
                    self.env.currentNumOfTable = 0
                    while self.env.currentNumOfTable < len(self.env.listOfTables):
                        self.env.startTable()
                        self.env.currentNumOfRow = 0
                        for currentRow in self.env.listOfTableVectors[self.env.currentNumOfTable - 1]:
                            nodes, children = traverse_tree_in_dfs_inorder(currentRow, self.embeddings,
                                                                           self.embed_lookup, 0, [], [], -1)
                            gen = yield_some_stuff(nodes, children)
                            batches = list(
                                enumerate(
                                    batch_samples(gen, 1)))
                            iterator = iter(batches)
                            batch = next(iterator, None)
                            if isinstance(batch[0], int):
                                num, batch = batch
                            nodes, children = batch
                            nodes = nodes[0]
                            complexity = getNumOfReasonableNodes(currentRow)
                            # complexity = int(complexity ** (1/3) * (len(self.env.listOfTables[0]) ** (1/3)))
                            complexity = 0
                            if complexity == 0:
                                complexity = 1
                            for i in range(complexity):
                                toBeAppended = deepcopy(nodes)
                                nodes = nodes + toBeAppended
                            epF = 0
                            while epF < len(nodes):
                                s = nodes[epF]
                                a, rnn_state = self.AC.choose_action([s], rnn_state)

                                r,d,c = self.env.step_cov_continuos(a, m - 1)
                                episode_buffer.append([s, a])
                                buffer_r.append(r)
                                # if len(episode_buffer) % (len(self.env.arguments)*totalRows) == 0 and len(episode_buffer) != 0:
                                #     r,d,c,_ = self.env.step_cov_continuos_entire_matrix(self.number)
                                #     temp = 0
                                #     while temp < len(self.env.arguments)*totalRows:
                                #         buffer_r.append(r)
                                #         temp += 1
                                #nextBatch = next(iterator, None)
                                total_step += 1
                                episode_step_count += 1

                                if d or epF + 1 == len(nodes):
                                    # Since we don't know what the true final return is, we "bootstrap" from our current
                                    # value estimation.
                                    if d:
                                        v_s_ = 0  # terminal
                                    else:
                                        v_s_ = self.sess.run(self.AC.v, {self.AC.inputs: [s],
                                                                         self.AC.state_in[0]: rnn_state[0],
                                                                         self.AC.state_in[1]: rnn_state[1]})[0, 0]
                                    buffer_v_target = []

                                    rollout = np.array(episode_buffer)

                                    # self.batcher.pad(rollout[:, 0], self.num_feats)
                                    # self.batcher.init_child()
                                    # self.batcher.pad_child(rollout[:, 1])

                                    for r in buffer_r[::-1]:  # reverse buffer r
                                        v_s_ = r + GAMMA * v_s_
                                        buffer_v_target.append(v_s_)
                                    buffer_v_target.reverse()
                                    buffer_s, buffer_a, buffer_v_target = np.vstack(
                                        rollout[:, 0]), np.vstack(
                                        rollout[:, 1]), np.vstack(
                                        buffer_v_target)
                                    feed_dict = {
                                        self.AC.inputs: buffer_s,
                                        self.AC.a_his: buffer_a,
                                        self.AC.v_target: buffer_v_target,
                                        self.AC.state_in[0]: self.batch_rnn_state[0],
                                        self.AC.state_in[1]: self.batch_rnn_state[1]
                                    }
                                    _, _, self.batch_rnn_state, a_loss, c_loss = self.AC.update_global(
                                        feed_dict)  # actual training step, update global ACNet
                                    self.a_loss.append(a_loss)
                                    self.c_loss.append(c_loss)
                                    buffer_s, buffer_a, buffer_r, buffer_c, buffer_matrix_cov = [], [], [], [], []
                                    episode_buffer = []
                                    self.AC.pull_global()  # get global parameters to local ACNet
                                    # if episode_step_count >= max_episode_length - 1 or d or nextBatch is None:
                                if d or epF + 1 == len(nodes):
                                    episode_reward += r
                                    episode_coverage += c
                                    if self.env.rootTreeAdtNode.name not in self.avgFunctions:
                                        self.avgFunctions[self.env.rootTreeAdtNode.name] = [c]
                                    else:
                                        self.avgFunctions[self.env.rootTreeAdtNode.name].append(c)
                                    break
                                epF += 1

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
                    mean_a_loss = np.mean(self.a_loss[-2:])
                    mean_c_loss = np.mean(self.c_loss[-2:])
                    summary = tf.Summary()
                    summary.value.add(tag='Perf/Reward', simple_value=float(mean_reward))
                    summary.value.add(tag='Perf/Length', simple_value=float(mean_length))
                    summary.value.add(tag='Perf/Coverage', simple_value=float(mean_coverage))
                    summary.value.add(tag='Loss/A_Loss', simple_value=float(mean_a_loss))
                    summary.value.add(tag='Loss/C_loss', simple_value=float(mean_c_loss))
                    for key in self.env.dict_of_max_r.keys():
                        summary.value.add(tag='Max Functions/Max coverage for function: ' + str(key), simple_value=float(self.env.dict_of_max_r[key]))
                    for key in self.avgFunctions.keys():
                        summary.value.add(tag='Avg Functions/Avg coverage for function: ' + str(key), simple_value=float(np.mean(self.avgFunctions[key][-2:])))
                    self.summary_writer.add_summary(summary, episode_count)

                    self.summary_writer.flush()

                    sess.run(self.increment)

def yield_some_stuff(nodes, children):
    n, c = nodes, children
    yield(n,c)
