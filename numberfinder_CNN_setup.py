import os
import keras
import pickle
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D

import random
import colorsys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import pandas as pd

BATCH_SIZE = 128
bg_pics_dir = "/home/iolie/PycharmProjects/keras__practice/number_checker/lfw_mix"
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','-', ' ']

piclist = []
for dirpath, subdirs, files in os.walk(bg_pics_dir):
    for f in files:
        if f.endswith('.jpg'):
            piclist.append(os.path.join(dirpath, f))

piclist_train, piclist_val = shuffle_split_list(piclist)
print(len(piclist_train))
print(len(piclist_val))

training_generator = Image_Batch_Generator(piclist_train, BATCH_SIZE)
validation_generator = Image_Batch_Generator(piclist_val, BATCH_SIZE)

samples_per_epoch = GetSamplesPerEpoch(quotes_for_training, BATCH_SIZE)


model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same',
                 input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('softmax'))

adam = optimizers.Adam()
model.compile(loss='binary_crossentropy', optimizer=adam)
checkpointer = keras.callbacks.ModelCheckpoint(filepath='latestweights.hdf5',verbose=1,save_best_only=False)
lowest_loss = 2

while True:
    callback = model.fit_generator(training_generator, validation_data=validation_generator, steps_per_epoch=1000,
                                   epochs=1, max_queue_size=50, validation_steps=100)
    loss = float(callback.history['loss'][0])
    val_loss = float(callback.history['val_loss'][0])
    if loss < lowest_loss - 0.02:
        weightfolder = 'savedmodels_numfinder_1/titletraining_weightsatloss_{0:.2f}'.format(loss)
        if not os.path.isdir(weightfolder):
            os.makedirs(weightfolder)
        print('Saving {}/weights.h5'.format(weightfolder))
        model.save_weights(weightfolder + '/weights.h5')
        open(weightfolder + '/model.json', 'w').write(model.to_json())
        # picklefile = open(weightfolder + '/indices.pickle', 'wb')
        # pickle.dump((char_to_index, index_to_char, first_char_probs), picklefile)  ## what needs to go here??
        # picklefile.close()
        lowest_loss = loss


