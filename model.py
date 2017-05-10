import tflearn
from tflearn.layers.conv import conv_2d
from tflearn.layers.core import input_data, fully_connected, flatten
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import batch_normalization


"""
This is NVIDIAs model with only one channel as input, batch norm after every layer
and two outputs (throttle and turning)
"""
def tflearn_model():
    network = input_data(shape=[None, 200, 66, 1], name='input')
    network = batch_normalization(network, epsilon=0.001)
    network = conv_2d(network, 24, 5, strides=2, activation='relu', padding='valid')
    network = batch_normalization(network)
    network = conv_2d(network, 36, 5, strides=2, activation='relu', padding='valid')
    network = batch_normalization(network)
    network = conv_2d(network, 48, 5, strides=2, activation='relu', padding='valid')
    network = batch_normalization(network)
    network = conv_2d(network, 64, 3, strides=1, activation='relu', padding='valid')
    network = batch_normalization(network)
    network = conv_2d(network, 64, 3, strides=1, activation='relu', padding='valid')
    network = batch_normalization(network)
    network = flatten(network)
    network = fully_connected(network, 1164, activation='relu')
    network = batch_normalization(network)
    network = fully_connected(network, 100, activation='relu')
    network = batch_normalization(network)
    network = fully_connected(network, 50, activation='relu')
    network = batch_normalization(network)
    network = fully_connected(network, 10, activation='relu')
    network = batch_normalization(network)
    network = fully_connected(network, 2, activation='tanh')
    network = regression(network, optimizer='adam', loss='mean_square', name='targets')
    model = tflearn.DNN(network, checkpoint_path='nvidia_model', max_checkpoints=1,
                        tensorboard_verbose=0, tensorboard_dir='tflog')

    return model
