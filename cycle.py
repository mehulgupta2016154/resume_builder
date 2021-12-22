import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import *
from tensorflow_addons.layers import *
import tensorflow as tf
import numpy as np
import os
from PIL import Image

def preprocess(records):
    images =  records['image']
    images = tf.cast(images, tf.float32)/255.0
    return images

def tf_pipeline(dataset):
    dataset = tf.data.Dataset.from_tensor_slices({'image':dataset})
    dataset = dataset.map(preprocess)
    dataset = dataset.repeat().shuffle(100).batch(16).prefetch(1)
    return dataset

input_dim = (128,128,3)
depth = 4
kernel = 3
n_batch = 16
epochs = 10
steps = round(1500/n_batch)

def discriminator(input_dim,depth,kernel):
    layers = []
    layers.append(Input(shape=input_dim))
    for i in range(1,depth):
            layers.append(Conv2D(16*i,kernel_size=kernel))
            layers.append(InstanceNormalization())
            layers.append(Activation('relu'))
            layers.append(Dropout(0.2))
    layers.append(Conv2D(1,kernel_size=kernel))
    model = Sequential(layers)
    model.compile(loss='mse',optimizer=tf.keras.optimizers.Adam())
    return model

discriminator_A = discriminator(input_dim,depth,kernel)
discriminator_B = discriminator(input_dim,depth,kernel)

def generator(input_dim, depth, kernel):
    layers = []
    layers.append(Input(shape=input_dim))
    for i in range(1,depth):
        layers.append(Conv2D(16*i,kernel_size=kernel))
        layers.append(InstanceNormalization())
        layers.append(Activation('relu'))
        layers.append(Dropout(0.2))
    
    for i in range(1,depth):
        layers.append(Conv2DTranspose(16*i,kernel_size=kernel))
        layers.append(InstanceNormalization())
        layers.append(Activation('relu'))
        layers.append(Dropout(0.2))
    
    resizer =  lambda name: Lambda(lambda images: tf.image.resize(images, [128,128]), name=name)
    layers.append(resizer('Reshape'))
    layers.append(Conv2DTranspose(3,kernel_size=1,activation=None))
    model = Sequential(layers)
    return model

generator_A_B = generator(input_dim,depth,kernel)
generator_B_A = generator(input_dim,depth,kernel)

def composite_model(g1,d,g2,image_dim):
    g1.trainable = True
    g2.trainable = False
    d.trainable = False
    
    #general gan
    input_img = Input(shape=input_dim)
    g1_out = g1(input_img)
    d_out = d(g1_out)
    
    #identity loss
    input_id = Input(shape=input_dim)
    g1_out_id = g1(input_id)
    
    #F-cycle
    g2_out = g2(g1_out)
    
    #B-cycle
    g2_out_id = g2(input_id)
    output_g1 = g1(g2_out_id)
    
    model = Model([input_img,input_id],[d_out, g1_out_id, g2_out, output_g1])
    model.compile(loss=['mse','mae','mae','mae'],loss_weights=[1,5,10,10],optimizer=tf.keras.optimizers.Adam())
    return model

composite_A_B = composite_model(generator_A_B, discriminator_B, generator_B_A, input_dim)
composite_B_A = composite_model(generator_B_A, discriminator_A, generator_A_B, input_dim)

def generate_real(dataset, batch_size,patch_size):
    labels = np.ones((batch_size,patch_size,patch_size,1))
    return dataset,labels

def generate_fake(dataset,g,batch_size,patch_size):
    predicted = g(dataset)
    labels = np.zeros((batch_size,patch_size,patch_size,1))
    return predicted,labels


checkpoint_dir = './cyclegan'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(generator_A_B=generator_A_B, generator_B_A=generator_B_A,discriminator_A=discriminator_A,discriminator_B=discriminator_B,composite_A_B=composite_A_B, composite_B_A=composite_B_A)
manager = tf.train.CheckpointManager(checkpoint, 'cyclegan', max_to_keep=3)
checkpoint.restore(manager.latest_checkpoint)