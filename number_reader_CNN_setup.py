# okay this thing needs to take the generator that makes close crops of the numbers as training-data
# then feed those into a CNN model that has a (max-phone-number-length)*(possible-choices) number of output nodes

import os
import keras
from keras import optimizers
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from number_reader_training_functions import Close_Up_Image_Batch_Generator
from num_find_training_functions import generate_font_dictionary, shuffle_split_list

printing_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    '-', ' ', '(', ')']

guessing_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ' ', '(', ')']
# other one doesn't recognise brackets... fix that .... have a look at real data and add more relevant ones in...
## also argh this should be listed once not all over the gaff

char_to_index = {ch:i for i,ch in enumerate(guessing_numbers)}
index_to_char = {i:ch for i,ch in enumerate(guessing_numbers)}
end_index = max(index_to_char.keys())+1

num_outputs = 10
print(num_outputs)


bg_pics_dir = "/home/iolie/PycharmProjects/keras__practice/number_checker/lfw_mix"
piclist = []
for dirpath, subdirs, files in os.walk(bg_pics_dir):
    for f in files:
        if f.endswith('.jpg'):
            piclist.append(os.path.join(dirpath, f))


BATCH_SIZE = 128


FONT_DIR = "/usr/share/fonts/truetype"
font_index = generate_font_dictionary(FONT_DIR)
numfonts = max(font_index.keys())


piclist_train, piclist_val = shuffle_split_list(piclist)


training_generator = Close_Up_Image_Batch_Generator(piclist_train, font_index, BATCH_SIZE, printing_numbers, end_index)
validation_generator = Close_Up_Image_Batch_Generator(piclist_val, font_index, BATCH_SIZE, printing_numbers, end_index)

image_size = (50, 400)

model = Sequential()
model.add(Conv2D(64, (3, 3), padding='valid',
                 input_shape= (128, 50, 400, 3)))  #samples, rows, cols, channels
model.add(Activation('relu'))
model.add(Conv2D(64, (2, 2)))
model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# model.add(Conv2D(64, (3, 3), padding='same'))
# model.add(Activation('relu'))
model.add(Conv2D(128, (2, 2)))
model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_outputs))
model.add(Activation('softmax'))

model.add(Activation('sigmoid'))
adam = optimizers.Adam()

model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
checkpointer = keras.callbacks.ModelCheckpoint(filepath='latestweights.hdf5', verbose=1, save_best_only=False)
lowest_loss = 2