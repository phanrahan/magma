'''
MIT License

Copyright (c) 2017 Ayush Saraf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import numpy as np
import tensorflow as tf
from tensorflow.python.framework import ops


def py_func(func, inp, Tout, stateful=True, name=None, grad=None):
    # Need to generate a unique name to avoid duplicates:
    rnd_name = 'PyFuncGrad' + str(np.random.randint(0, 1E+8))
    
    tf.RegisterGradient(rnd_name)(grad)
    g = tf.get_default_graph()
    with g.gradient_override_map({"PyFunc": rnd_name}):
        return tf.py_func(func, inp, Tout, stateful=stateful, name=name)

def binarize_weights(x, name=None):
    """Creates the binarize_weights Op with f as forward pass
    and df as the gradient for the backward pass
    Args:
        x: The input Tensor
        name: the name for the Op
    
    Returns:
        The output tensor
    """
    def f(x):
        alpha = np.abs(x).sum(0).sum(0).sum(0) / x[:,:,:,0].size
        y = np.sign(x)
        y[y == 0] = 1
        return y * alpha

    def df(op, grad):
        x = op.inputs[0]
        print(x)
        n = tf.reduce_prod(tf.shape(x[:,:,:,0])[:3])
        alpha = tf.div(tf.reduce_sum(tf.abs(x), [0, 1, 2]), tf.cast(n, tf.float32))
        ds = tf.multiply(x, tf.cast(tf.less_equal(tf.abs(x), 1), tf.float32))
        return tf.multiply(grad, tf.add(tf.cast(1/n, tf.float32), tf.multiply(alpha, ds)))
        
    with ops.name_scope(name, 'BinarizeWeights', [x]) as name:
        fx = py_func(f, [x], [tf.float32], name=name, grad=df)
        return fx[0]

def binary_activation(x, name=None):
    """Creates the binary_activation Op with f as forward pass
    and fd as the gradient for the backward pass
    Args:
        x: The input Tensor
        name: the name for the Op
    Returns:
        The output tensor
    """
    def f(x):
        y = np.sign(x)
        y[y == 0] = 1
        return y
    
    def df(op, grad):
        x = op.inputs[0]
        alpha = tf.cast(tf.less_equal(tf.abs(x), 1), tf.float32) # alpha = (|x| <= 1) * 1
        return tf.multiply(grad, alpha) # grad * alpha
    
    with ops.name_scope(name, 'BinarizeInputs', [x]) as name:
        fx = py_func(f, [x], [tf.float32], name=name, grad=df)
        return fx[0]

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W, padding='SAME'):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding=padding)

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

def batch_norm_layer(x, name='norm'):
    with tf.name_scope(name) as scope:
        mean, variance = tf.nn.moments(x, axes=[1, 2], keep_dims=True)
        norm = tf.nn.batch_normalization(x, mean, variance, None, None, 1e-5)
        return norm