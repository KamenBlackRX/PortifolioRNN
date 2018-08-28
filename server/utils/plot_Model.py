#Generate plot grafics
import numpy as np
import tflearn
import tensorflow as tf
import random
import matplotlib.pyplot as plt
import sys
import nltk
import pickle

def load_model():
    # restore data structures
    data = pickle.load( open( "training_data", "rb" ) )

    global words
    global classes 
    
    words = data['words']
    classes = data['classes']
    train_x = data['train_x']
    train_y = data['train_y']
    
    # reset underlying graph data
    tf.reset_default_graph()
    
    # Build a neural network
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)
       
    # load saved model
    model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
    model.load('./model.tflearn')
    return model

def plot_history(history):
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [1000$]')
    plt.plot(history, np.array(history.history['mean_absolute_error']), 
           label='Train Loss')
    plt.plot(history, np.array(history.history['val_mean_absolute_error']),
           label = 'Val loss')
    plt.legend()
    plt.ylim([0,5])

plot_history(load_model())