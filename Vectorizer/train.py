"""Train the ast2vect network."""
"""Code used from https://github.com/crestonbunch/tbcnn"""

import os

import tensorflow as tf
from tensorflow.contrib.tensorboard.plugins import projector

import Vectorizer.network as network
import Vectorizer.sampling as sampling
from Vectorizer.node_map import NODE_MAP
from Vectorizer.parameters import \
    NUM_FEATURES, LEARN_RATE, BATCH_SIZE, EPOCHS, CHECKPOINT_EVERY, HIDDEN_NODES


def learn_vectors(sample, logdir, num_feats=NUM_FEATURES, epochs=EPOCHS):
    """Learn a vector representation of ADT nodes."""

    # build the inputs and outputs of the network
    net_work = network.embedding_network(batch_size=BATCH_SIZE, num_feats=NUM_FEATURES, hidden_size=HIDDEN_NODES)
    input_node = net_work.inputs
    label_node = net_work.labels
    embed_node = net_work.embeddings
    loss_node = net_work.loss

    # use gradient descent with momentum to minimize the training objective
    train_step = tf.train.GradientDescentOptimizer(LEARN_RATE). \
                    minimize(loss_node)

    tf.summary.scalar('loss', loss_node)
    ### init the graph
    sess = tf.Session()

    with tf.name_scope('saver'):
        saver = tf.train.Saver()
        summaries = tf.summary.merge_all()
        writer = tf.summary.FileWriter(logdir, sess.graph)
        config = projector.ProjectorConfig()
        embedding = config.embeddings.add()
        embedding.tensor_name = embed_node.name
        projector.visualize_embeddings(writer, config)

    sess.run(tf.global_variables_initializer())

    checkfile = os.path.join(logdir, 'ast2vec.ckpt')

    step = 0
    for epoch in range(1, epochs + 1):
        sample_gen = sampling.batch_samples(sample, BATCH_SIZE)
        for batch in sample_gen:
            input_batch, label_batch = batch

            _, summary, embed, err = sess.run(
                [train_step, summaries, embed_node, loss_node],
                feed_dict={
                    input_node: input_batch,
                    label_node: label_batch
                }
            )

            print('Epoch: ', epoch, 'Loss: ', err)
            writer.add_summary(summary, step)
            if step % CHECKPOINT_EVERY == 0:
                # save state so we can resume later
                saver.save(sess, os.path.join(checkfile), step)
                print('Checkpoint saved.')
                # save embeddings
                # pickle.dump((embed, NODE_MAP), embed_file)
            step += 1

    # save embeddings and the mapping
    # saver.save(sess, os.path.join(checkfile), step)
    return (embed, NODE_MAP)
