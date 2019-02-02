import numpy as np
import tensorflow as tf

from Agent.ACAgent import AC_Network
from Environment.Utils import update_target_graph, discount
from Environment.enviroment import Enviroment


class Worker:
    def __init__(self, name, trainer, model_path, global_episodes, global_rewards):
        self.name = "worker_" + str(name)
        self.number = name
        self.model_path = model_path
        self.trainer = trainer
        self.global_rewards = global_rewards
        self.global_episodes = global_episodes
        self.increment = self.global_episodes.assign_add(1)
        self.episode_rewards = []
        self.episode_lengths = []
        self.episode_mean_values = []

        # Create the local copy of the network and the tensorflow op to copy global paramters to local network
        self.local_AC = AC_Network(self.name, trainer)
        self.update_local_ops = update_target_graph('global', self.name)

        self.sleep_time = 0.028
        self.env = Enviroment()

    def train(self, global_AC, rollout, sess, gamma, bootstrap_value):
        rollout = np.array(rollout)
        observations = rollout[:, 0]
        actions = rollout[:, 1]
        rewards = rollout[:, 2]
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
                     self.local_AC.inputs: np.vstack(observations),
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
                self.env = Enviroment()
                episode_buffer = []
                episode_values = []
                episode_frames = []
                episode_reward = 0
                episode_step_count = 0
                d = False
                m = 0
                # self.env.new_episode()
                rnn_state = self.local_AC.state_init

                while m < len(self.env.listOfFiles):
                    m += 1
                    self.env.prepareNextFile()
                    self.env.currentNumOfTable = 0
                    while self.env.currentNumOfTable < len(self.env.listOfTables):
                        self.env.startTable()
                        self.env.currentNumOfRow = 0
                        while self.env.currentNumOfRow < len(self.env.currentVectors):
                            s = self.env.startRow(m - 1)
                            numOfVectors = 1
                            while numOfVectors < len(self.env.currentVectorRow):
                                # Take an action using probabilities from policy network output.
                                a_dist, v, rnn_state = sess.run(
                                    [self.local_AC.policy, self.local_AC.value, self.local_AC.state_out],
                                    feed_dict={self.local_AC.inputs: [s],
                                               self.local_AC.state_in[0]: rnn_state[0],
                                               self.local_AC.state_in[1]: rnn_state[1]})
                                a = np.random.choice(a_dist[0], p=a_dist[0])
                                a = np.argmax(a_dist == a)

                                r, d, _ = self.env.step(a, m - 1)
                                s1 = self.env.currentVectorRow[numOfVectors]
                                numOfVectors += 1
                                total_steps += 1
                                episode_frames.append(s1)

                                episode_buffer.append([s, a, r, s1, d, v[0, 0]])
                                episode_values.append(v[0, 0])

                                if not numOfVectors < len(self.env.currentVectorRow):
                                    episode_reward += r
                                s = s1
                                total_steps += 1
                                episode_step_count += 1

                                if len(episode_buffer) == 20 and not d:
                                    # Since we don't know what the true final return is, we "bootstrap" from our current
                                    # value estimation.
                                    v1 = sess.run(self.local_AC.value,
                                                  feed_dict={self.local_AC.inputs: [s],
                                                             self.local_AC.state_in[0]: rnn_state[0],
                                                             self.local_AC.state_in[1]: rnn_state[1]})[0, 0]
                                    v_l, p_l, e_l, g_n, v_n, adv = self.train(global_AC, episode_buffer, sess, gamma,
                                                                              v1)
                                    episode_buffer = []
                                    sess.run(self.update_local_ops)
                                if episode_step_count >= max_episode_length - 1 or d == True:
                                    episode_reward += r
                                    break

                self.episode_rewards.append(episode_reward)
                self.episode_lengths.append(episode_step_count)
                self.episode_mean_values.append(np.mean(episode_values))

                # Update the network using the experience buffer at the end of the episode.
                if len(episode_buffer) != 0:
                    v_l, p_l, e_l, g_n, v_n, adv = self.train(global_AC, episode_buffer, sess, gamma, 0.0)

                # Periodically save gifs of episodes, model parameters, and summary statistics.
                if episode_count % 5 == 0 and episode_count != 0:
                    if episode_count % 250 == 0 and self.name == 'worker_0':
                        saver.save(sess, self.model_path + '/model-' + str(episode_count) + '.cptk')
                        print("Saved Model")

                    mean_reward = np.mean(self.episode_rewards[-5:])
                    mean_length = np.mean(self.episode_lengths[-5:])
                    mean_value = np.mean(self.episode_mean_values[-5:])
                    # summary = tf.Summary()
                    print(self.name + " Reward: " + str(float(mean_reward)))
                    print(self.name + " Length: " + str(float(mean_length)))
                    print(self.name + " Value: " + str(float(mean_value)))

                # if self.name == 'worker_0':
                sess.run(self.increment)
                episode_count += 1
