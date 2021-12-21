import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *

input_shape = (28,28,1)
final_encoder_dim = 2
decoder_input_dim = 4
depth = 5
kernel_size = 3
activation = 'tanh'
dropout = 0.1

def discriminator_vanilla(input_shape, dim, depth, kernel, dropout,activation):
    layers = []
    layers.append(InputLayer(input_shape=input_shape))
    for i in range(1,depth):
        layers.append(Conv2D(16*i,kernel_size=kernel_size))
        layers.append(BatchNormalization())
        layers.append(Activation('relu'))
        layers.append(Dropout(dropout))
    layers.append(Flatten())
    layers.append(Dense(128,activation='relu'))
    layers.append(Dense(dim))
    return Sequential(layers)

encoder_v = discriminator_vanilla(input_shape, final_encoder_dim, depth, kernel_size, dropout,activation)

def generator_vanilla(input_shape, depth, output_shape,kernel,dropout):
    layers = []
    layers.append(InputLayer(input_shape=(input_shape,)))
    layers.append(Dense(784,activation='relu'))
    layers.append(Reshape(target_shape=output_shape))
    for i in range(1,depth):
        layers.append(Conv2DTranspose(16*i,kernel_size=kernel))
        layers.append(BatchNormalization())
        layers.append(Activation('relu'))
        layers.append(Dropout(dropout))
    
    resizer =  lambda name: Lambda(lambda images: tf.image.resize(images, [28,28]), name=name)
    layers.append(resizer('Reshape'))
    layers.append(Conv2DTranspose(1,kernel_size=1,activation=None))
    return Sequential(layers)

def return_decoder():
        encoder_opt = tf.keras.optimizers.Adam()
        decoder_opt = tf.keras.optimizers.Adam()
        decoder_v = generator_vanilla(decoder_input_dim, depth, input_shape,kernel_size,dropout)

        checkpoint_v = tf.train.Checkpoint(generator_optimizer=decoder_opt,discriminator_optimizer=encoder_opt,generator=decoder_v,discriminator=encoder_v)
        latest = tf.train.latest_checkpoint('vanilla_gan/')
        checkpoint_v.restore(latest)
        decoder_v.load_weights = checkpoint_v.discriminator.weights
        return decoder_v