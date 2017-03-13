
# coding: utf-8

# In[1]:

"""
reference paper: http://arxiv.org/pdf/1512.03385.pdf
"""

from collections import namedtuple
from math import sqrt
import os

import tensorflow as tf


# In[18]:

batch_norm = tf.contrib.layers.batch_norm
convolution2d = tf.contrib.layers.convolution2d


# In[19]:

def res_net(x, y, activation=tf.nn.relu):
    """Build a residual network
    Args:
        x: input of the network
        y: output of the network
        activation: activation function to apply after each convolution
    
    Returns:
        predictions and loss tensors.
    """
    BottleneckGroup = namedtuple('BottleneckGroup',
                               ['num_blocks', 'num_filters', 'bottleneck_size'])
    
    groups = [
        BottleneckGroup(3, 128, 32), BottleneckGroup(3, 256, 64),
        BottleneckGroup(3, 512, 128), BottleneckGroup(3, 1024, 256)
    ]
    
    input_shape = x.get_shape().as_list()
    
    if len(input_shape) == 2:
        ndim = int(sqrt(input_shape[1]))
        x = tf.reshape(x, [-1, ndim, ndim, 1])
        
    with tf.variable_scope('conv_layer1'):
        net = convolution2d(
            x, 64, 7, normalizer_fn=batch_norm, activation_fn=activation)
        
    net = tf.nn.max_pool(net, [1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
    
    with tf.variable_scope('conv_layer2'):
        net = convolution2d(net, groups[0].num_filters, 1, padding='VALID')
        
    for group_i, group in enumerate(groups):
        for block_i in range(group.num_blocks):
            name = 'group_%d/block_%d' % (group_i, block_i)
            
            with tf.variable_scope(name + '/conv_in'):
                conv = convolution2d(net, group.bottleneck_size, 1, padding='VALID', 
                                    activation_fn=activation, normalizer_fn=batch_norm)
            with tf.variable_scope(name + 'conv_bottleneck'):
                conv = convolution2d(conv, group.bottleneck_size, 3, padding='SAME',
                                    activation_fn=activation, normalizer_fn=batch_norm)
            with tf.variable_scope(name + '/conv_out'):
                input_dim = net.get_shape()[-1].value
                conv = convolution2d(conv, input_dim, 1, padding='VALID',
                                     activation_fn=activation, normalizer_fn=batch_norm)
            net = conv + net
        
        try:
            next_group = groups[group_i + 1]
            with tf.variable_scope('block_%d/conv_upscale' % group_i):
                net = convolution2d(net, next_group.num_filters, 1, activation_fn=activation,
                                   biases_initializer=None, padding='SAME')
        except IndexError:
            pass
        
    net_shape = net.get_shape().as_list()
    net = tf.nn.avg_pool(net, ksize=[1, net.shape[1], net.shape[2], 1],
                        strides=[1, 1, 1, 1], padding='VALID')
    
    net_shape = net.get_shape().as_list()
    net = tf.reshape(net, [-1, net_shape[1] * net_shape[2] * net_shape[3]])
    
    target = tf.one_hot(y, depth=10, dtype=tf.float32)
    logits = tf.contrib.layers.fully_connected(net, 10, activation_fn=None)
    loss = tf.losses.softmax_cross_entropy(target, logits)
    return tf.nn.softmax(logits), loss
    


# In[20]:

def res_net_mode(x, y):
    prediction, loss = res_net(x, y)
    predicted = tf.argmax(prediction, 1)
    accuracy = tf.equal(predicted, tf.cast(y, tf.int64))
    predictions = {'prob':prediction, 'class':predicted, 'accurcy':accuracy}
    train_op = tf.contrib.layers.optimize_loss(loss, tf.contrib.framework.get_global_step(),
                                              optimizer='Adagrad',
                                              learning_rate=0.001)
    return predictions, loss, train_op


# In[ ]:

def main():
    mnist = tf.contrib.learn.datasets.load_dataset('mnist')
    
    classifier = tf.contrib.learn.Estimator(model_fn=res_net_mode)
    
    tf.logging.set_verbosity(tf.logging.INFO)
    
    classifier.fit(mnist.train.images, mnist.train.labels,
                  batch_size=100, steps=1000)
    
    result = classifier.evaluate(
        x=mnist.test.images, 
        y=mnist.test.labels,
        metrics={'accuracy': tf.contrib.learn.MetricSpec(
                    metrics_fn=tf.contrib.metrics.streaming_accuracy,
                    prediction_key='accuracy')})
    
    score = result['accuracy']
    print('Accuracy: {0:f}'.format(score))
    
if __name__ == '__main__':
    main()


# In[ ]:



