# -*- coding: utf-8 -*-
"""data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dU1J93B1i_PkFSvRRGQv_YsknXPDV31q
"""

import numpy as np
import time, math
import tensorflow as tf
import tensorflow.contrib.eager as tfe
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from albumentations import (Compose, Cutout)

def normalize(x):
  """Normalize the values of input image"""
  mean = np.mean(x, axis=(0,1,2))
  std = np.std(x, axis=(0,1,2))
  normalize = lambda x: ((x - mean) / std).astype('float32')
  x = normalize(x)

  return x

def pad4(x):
  """Pad 4 zeros across the edges of input image"""
  pad4 = lambda x: np.pad(x, [(0, 0), (4, 4), (4, 4), (0, 0)], mode='reflect')
  x = pad4(x)

  return x

def Cutout(x_train, y_train, num_images):
  """Function to add cutout augmentation"""
  def Custom_Aug(img):
      seq = Compose([
          Cutout(num_holes=1, p=0.5)], p=1)
  return seq(image=img)['image']

  train_datagen = ImageDataGenerator(preprocessing_function=Custom_Aug)

  train_generator = train_datagen.flow(x_train, y_train, batch_size=num_images)

  x_batch, y_batch = next(train_generator)

  return x_batch, y_batch

def plot_image(x):
  """Function to plot 8 number of images"""
  fig = plt.figure(figsize=(14, 5))

  for i in range(8):
    sub = fig.add_subplot(2, 4, i + 1)
    sub.imshow(x[i,:,:], interpolation='bilinear')

"""TFRecord Classes"""

def _bytes_feature(value):
  """Returns a bytes_list from a string / byte."""

  if isinstance(value, type(tf.constant(0))):
    value = value.numpy()
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
  """Returns an int64_list from a bool / enum / int / uint."""
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def convert_np_to_tf_example(image, label):
    feature_dict = {
        'image': _bytes_feature(image.tostring()),
        'label': _int64_feature(label),
    }

    features = tf.train.Features(feature=feature_dict)
    tf_example = tf.train.Example(features=features)
    protocol_message = tf_example.SerializeToString()

    return protocol_message

def convert_proto_message_to_np(protocol_message):
    feature_dict = {
        'image': tf.io.FixedLenFeature([], tf.string),
        'label': tf.io.FixedLenFeature([], tf.int64)
    }

    parsed_out = tf.io.parse_single_example(serialized=protocol_message,
                                            features=feature_dict)

    image = tf.io.decode_raw(parsed_out['image'], out_type=tf.float32)
    label = parsed_out['label']

    return (image,label)

def reshape_img(X, img_shape):
    img = X[0].numpy()
    label = X[1]
    img = img.reshape(img_shape)
    img_tensor = tf.convert_to_tensor(img)

    return (img_tensor, label)

def convert_np_to_tfrecords(images, labels,
                            batch_size=128,filename=None):

    # Converts a numpy array into TFReocrds

    channels = images.shape[-1]
    width = images.shape[-2]
    height = images.shape[-3]

    img_shape = (height, width, channels)
    if filename == None:
        filename = 'dataset.tfrecords'
    with tf.io.TFRecordWriter(filename) as writer:
        for img,label in zip(images,labels):
            protocol_message = convert_np_to_tf_example(img,label)

            writer.write(protocol_message)

    dataset = tf.data.TFRecordDataset(filename)
    dataset = dataset.map(convert_proto_message_to_np)
    dataset = dataset.map(lambda x, y: (tf.reshape(x,img_shape), y))

    return dataset
