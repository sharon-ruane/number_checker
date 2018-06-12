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
print(end_index)
num_outputs = (len(guessing_numbers) + 1)*10
print(num_outputs)


bg_pics_dir = "/home/iolie/PycharmProjects/keras__practice/number_checker/lfw_mix"
piclist = []
for dirpath, subdirs, files in os.walk(bg_pics_dir):
    for f in files:
        if f.endswith('.jpg'):
            piclist.append(os.path.join(dirpath, f))


BATCH_SIZE = 128
output_shape = ((len(guessing_numbers) + 1), 10)
print(output_shape)


FONT_DIR = "/usr/share/fonts/truetype"
font_index = generate_font_dictionary(FONT_DIR)
numfonts = max(font_index.keys())


piclist_train, piclist_val = shuffle_split_list(piclist)


training_generator = Close_Up_Image_Batch_Generator(piclist_train, font_index, BATCH_SIZE,
                                                    printing_numbers, guessing_numbers, end_index)
validation_generator = Close_Up_Image_Batch_Generator(piclist_val, font_index, BATCH_SIZE,
                                                      printing_numbers, guessing_numbers, end_index)

image_size = (50, 400)

model = Sequential()
model.add(Conv2D(64, (3, 3), padding='valid',
                 input_shape= (50, 400, 3)))  #samples, rows, cols, channels
model.add(Activation('relu'))
model.add(Conv2D(64, (2, 2)))
model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
# model.add(Conv2D(128, (2, 2)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
#model.add(Dense(num_outputs))

from keras.activations import softmax
def softMaxAxis1(x):
    return softmax(x, axis=-1)

model.add(Dense(output_shape, activation=softMaxAxis1))
# model.add(Activation('softmax', axis=-1))
#model.add(Activation('sigmoid'))
adam = optimizers.Adam()

model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
checkpointer = keras.callbacks.ModelCheckpoint(filepath='latestweights.hdf5', verbose=1, save_best_only=False)
lowest_loss = 2


while True:
    callback = model.fit_generator(training_generator, validation_data=validation_generator, steps_per_epoch=1000,
                                   epochs=1, max_queue_size=50, validation_steps=50)
    loss = float(callback.history['loss'][0])
    val_loss = float(callback.history['val_loss'][0])
    if loss < lowest_loss - 0.02:
        weightfolder = 'savedmodels_numreader_1/titletraining_weightsatloss_{0:.2f}'.format(loss)
        if not os.path.isdir(weightfolder):
            os.makedirs(weightfolder)
        print('Saving {}/weights.h5'.format(weightfolder))
        model.save_weights(weightfolder + '/weights.h5')
        open(weightfolder + '/model.json', 'w').write(model.to_json())
        # picklefile = open(weightfolder + '/indices.pickle', 'wb')
        # pickle.dump((char_to_index, index_to_char, first_char_probs), picklefile)  ## what needs to go here??
        # picklefile.close()
        lowest_loss = loss