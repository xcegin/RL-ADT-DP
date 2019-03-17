import pickle

import numpy as np
import tensorflow as tf

from ADT.Utils.ResolverUtil import getNumOfReasonableNodes
from Agent.Convolutional.GeneratorSamples import batch_samples, gen_samples, Batcher
from Agent.Convolutional.ACConvAgent import AConv_Network
from Environment.Utils import update_target_graph, discount
from Environment.enviroment import Enviroment


class ACCovWorker:
    def __init__(self, name, trainer, model_path, global_episodes, global_rewards):
        self.name = "worker_" + str(name)
        self.number = name
        self.model_path = model_path
        self.trainer = trainer
        self.global_rewards = global_rewards
        self.global_episodes = global_episodes
        self.increment = self.global_episodes.assign_add(1)
        self.episode_rewards = []
        self.episode_coverages = []
        self.episode_lengths = []
        self.episode_mean_values = []
        self.batcher = Batcher()
        self.summary_writer = tf.summary.FileWriter("logs/train_" + str(self.number))

        with open('vectors_cov.pkl', 'rb') as fh:
            self.embeddings, self.embed_lookup = pickle.load(fh)
            self.num_feats = len(self.embeddings[0])

        # Create the local copy of the network and the tensorflow op to copy global paramters to local network
        self.local_AC = AConv_Network(self.name, trainer, self.num_feats)
        self.update_local_ops = update_target_graph('global', self.name)

        self.sleep_time = 0.028
        self.env = Enviroment()

    def train(self, global_AC, rollout, sess, gamma, bootstrap_value):
        rollout = np.array(rollout)

        self.batcher.pad(rollout[:, 0], self.num_feats)
        self.batcher.init_child()
        self.batcher.pad_child(rollout[:, 1])

        nodes_observations = rollout[:, 0]
        children_observations = rollout[:, 1]
        actions = rollout[:, 2]
        rewards = rollout[:, 3]
        values = rollout[:, 5]

        # Here we take the rewards and values from the rollout, and use them to
        # generate the advantage and discounted returns.
        # The advantage function uses "Generalized Advantage Estimation"
        self.rewards_plus = np.asarray(rewards.tolist() + [bootstrap_value])
        discounted_rewards = discount(self.rewards_plus, gamma)[:-1]
        self.value_plus = np.asarray(values.tolist() + [bootstrap_value])
        advantages = rewards + gamma * self.value_plus[1:] - self.value_plus[:-1]
        advantages = discount(advantages, gamma)

        # Update the global network using gradients from loss
        # Generate network statistics to periodically save
        rnn_state = self.local_AC.state_init
        feed_dict = {self.local_AC.target_v: discounted_rewards,
                     self.local_AC.nodes: np.vstack(nodes_observations),
                     self.local_AC.children: np.vstack(children_observations),
                     self.local_AC.actions: actions,
                     self.local_AC.advantages: advantages,
                     self.local_AC.state_in[0]: rnn_state[0],
                     self.local_AC.state_in[1]: rnn_state[1]}
        v_l, p_l, e_l, g_n, v_n, adv, apl_g = sess.run([self.local_AC.value_loss,
                                                        self.local_AC.policy_loss,
                                                        self.local_AC.entropy,
                                                        self.local_AC.grad_norms,
                                                        self.local_AC.var_norms,
                                                        self.local_AC.adv_sum,
                                                        self.local_AC.apply_grads],
                                                       feed_dict=feed_dict)
        return v_l / len(rollout), p_l / len(rollout), e_l / len(rollout), g_n, v_n, adv / len(rollout)

    def work(self, max_episode_length, gamma, global_AC, sess, coord, saver):
        episode_count = sess.run(self.global_episodes)
        total_steps = 0
        print("Starting worker " + str(self.number))
        with sess.as_default(), sess.graph.as_default():
            while not coord.should_stop():
                sess.run(self.update_local_ops)
                self.env.reset()
                self.batcher = Batcher()
                episode_buffer = []
                episode_values = []
                episode_reward = 0
                episode_coverage = 0
                episode_step_count = 0
                m = 0
                # self.env.new_episode()
                rnn_state = self.local_AC.state_init

                while m < len(self.env.listOfFiles):
                    m += 1
                    self.env.prepareNextFileConvWithCov(self.number)
                    self.env.currentNumOfTable = 0
                    while self.env.currentNumOfTable < len(self.env.listOfTables):
                        self.env.startTable()
                        for currentRow in self.env.listOfTableVectors:
                            numOfTimes = 0
                            d = False
                            self.env.initializeArgumentValuesCov()
                            complexity = getNumOfReasonableNodes(currentRow)
                            complexity = int(complexity ** (1 / 3) * (len(self.env.listOfTables[0]) ** (1 / 3)))
                            # complexity = int(complexity ** (1 / 4))
                            if complexity == 0:
                                complexity = 1
                            total = len(self.env.arguments) * len(self.env.listOfTables[0]) * complexity
                            while numOfTimes < total:  # TODO REPLACE FOR REAL COUNT OF FUNCTION SIZE OR SMS
                                if d:
                                    break
                                # self.env.initializeArgumentValues()
                                batches = list(
                                    enumerate(
                                        batch_samples(gen_samples(currentRow, self.embeddings, self.embed_lookup), 1)))
                                iterator = iter(batches)
                                batch = next(iterator, None)
                                while batch is not None:
                                    # self.env.initializeArgumentValues()
                                    if isinstance(batch[0], int):
                                        num, batch = batch
                                    nodes, children = batch
                                    self.batcher.checkMaxDim(nodes)
                                    a_dist, v, rnn_state = sess.run(
                                        [self.local_AC.policy, self.local_AC.value, self.local_AC.state_out],
                                        feed_dict={self.local_AC.nodes: nodes, self.local_AC.children: children,
                                                   self.local_AC.state_in[0]: rnn_state[0],
                                                   self.local_AC.state_in[1]: rnn_state[1]})
                                    a = np.random.choice(a_dist[0], p=a_dist[0])
                                    a = np.argmax(a_dist == a)

                                    r, d, c, _ = self.env.step_cov(a, self.number, m - 1)
                                    # nextBatch = next(iterator, None)
                                    total_steps += 1
                                    episode_step_count += 1

                                    batch = next(iterator, None)

                                    # batch = nextBatch
                                    episode_buffer.append([nodes, children, a, r, d, v[0, 0]])

                                    if len(episode_buffer) == 10 * (len(
                                            list(self.env.argumentValues.keys())) + 1):  # TODO - really not done?
                                        # Since we don't know what the true final return is, we "bootstrap" from our current
                                        # value estimation.
                                        v1 = sess.run(self.local_AC.value,
                                                      feed_dict={self.local_AC.nodes: nodes,
                                                                 self.local_AC.children: children,
                                                                 self.local_AC.state_in[0]: rnn_state[0],
                                                                 self.local_AC.state_in[1]: rnn_state[1]})[0, 0]
                                        v_l, p_l, e_l, g_n, v_n, adv = self.train(global_AC, episode_buffer, sess,
                                                                                  gamma,
                                                                                  v1)
                                        episode_buffer = []
                                        sess.run(self.update_local_ops)
                                    # if episode_step_count >= max_episode_length - 1 or d or nextBatch is None:
                                    if numOfTimes + 1 == total or d:
                                        episode_reward += r
                                        episode_coverage += c
                                        break
                                numOfTimes += 1

                episode_count += 1
                self.episode_rewards.append(episode_reward)
                self.episode_coverages.append(episode_coverage)
                self.episode_lengths.append(episode_step_count)
                self.episode_mean_values.append(np.mean(episode_values))

                # Update the network using the experience buffer at the end of the episode.
                if len(episode_buffer) != 0:
                    v_l, p_l, e_l, g_n, v_n, adv = self.train(global_AC, episode_buffer, sess, gamma, 0.0)

                # Periodically save gifs of episodes, model parameters, and summary statistics.
                if episode_count % 2 == 0 and episode_count != 0:
                    if episode_count % 100 == 0 and self.name == 'worker_0':
                        saver.save(sess, self.model_path + '/model-' + str(episode_count) + '.cptk')
                        print("Saved Model")

                    mean_reward = np.mean(self.episode_rewards[-2:])
                    mean_length = np.mean(self.episode_lengths[-2:])
                    mean_value = np.mean(self.episode_mean_values[-2:])
                    mean_coverage = np.mean(self.episode_coverages[-2:])
                    summary = tf.Summary()
                    summary.value.add(tag='Perf/Reward', simple_value=float(mean_reward))
                    summary.value.add(tag='Perf/Coverage', simple_value=float(mean_coverage))
                    summary.value.add(tag='Perf/Length', simple_value=float(mean_length))
                    summary.value.add(tag='Perf/Value', simple_value=float(mean_value))
                    summary.value.add(tag='Losses/Value Loss', simple_value=float(v_l))
                    summary.value.add(tag='Losses/Policy Loss', simple_value=float(p_l))
                    summary.value.add(tag='Losses/Entropy', simple_value=float(e_l))
                    summary.value.add(tag='Losses/Advantage', simple_value=float(adv))
                    summary.value.add(tag='Losses/Grad Norm', simple_value=float(g_n))
                    summary.value.add(tag='Losses/Var Norm', simple_value=float(v_n))
                    for key in self.env.dict_of_max_r.keys():
                        summary.value.add(tag='Functions/Max coverage for function: ' + str(key),
                                          simple_value=float(self.env.dict_of_max_r[key]))
                    self.summary_writer.add_summary(summary, episode_count)

                    self.summary_writer.flush()

                    # mean_reward = np.mean(self.episode_rewards[-5:])
                    # mean_length = np.mean(self.episode_lengths[-5:])
                    # mean_value = np.mean(self.episode_mean_values[-5:])
                    # summary = tf.Summary()
                    # print(self.name + " Reward: " + str(float(mean_reward)))
                    # print(self.name + " Length: " + str(float(mean_length)))
                    # print(self.name + " Value: " + str(float(mean_value)))

                # if self.name == 'worker_0':
                sess.run(self.increment)
