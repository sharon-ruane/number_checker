import os
import keras
import pickle
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from number_checker.num_find_training_functions import shuffle_split_list, Image_Batch_Generator, generate_font_dictionary
from PIL import Image


BATCH_SIZE = 128 ## if batch size is not even, entire code breaks and a hole the size of Sweden rips somewhere in the universe
WINDOW_SIZE = (40, 40)
bg_pics_dir = "/home/iolie/PycharmProjects/keras__practice/number_checker/lfw_mix"
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','-', ' ']

FONT_DIR = "/usr/share/fonts/truetype"
font_index = generate_font_dictionary(FONT_DIR)
numfonts = max(font_index.keys())


piclist = []
for dirpath, subdirs, files in os.walk(bg_pics_dir):
    for f in files:
        if f.endswith('.jpg'):
            piclist.append(os.path.join(dirpath, f))

piclist_train, piclist_val = shuffle_split_list(piclist)

print(len(piclist_train))
print(len(piclist_val))


training_generator = Image_Batch_Generator(piclist_train, font_index, BATCH_SIZE, WINDOW_SIZE, numbers)
validation_generator = Image_Batch_Generator(piclist_val, font_index, BATCH_SIZE, WINDOW_SIZE, numbers)


pics, labels = training_generator.next()
# for pic in pics:
#     img = Image.fromarray(pic)
#     img.show()
print(pics.shape)
print(labels.shape)
print(labels)


model = Sequential()
model.add(Conv2D(128, (3, 3), padding='valid',
                 input_shape= (WINDOW_SIZE[1], WINDOW_SIZE[0], 3)))  #samples, rows, cols, channels
model.add(Activation('relu'))
model.add(Conv2D(128, (2, 2)))
model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# model.add(Conv2D(64, (3, 3), padding='same'))
# model.add(Activation('relu'))
model.add(Conv2D(248, (2, 2)))
model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(2))
model.add(Activation('softmax'))
#model.add(Dense(1))
#model.add(Activation('sigmoid'))
adam = optimizers.Adam()

#sgd = keras.optimizers.SGD(lr=0.01, momentum=0.9, decay=0.0, nesterov=True) ## seems a little more keen to converge
# sgd = keras.optimizers.SGD(lr=0.01, momentum=0.9, decay=0.0, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
#model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])
checkpointer = keras.callbacks.ModelCheckpoint(filepath='latestweights.hdf5', verbose=1, save_best_only=False)
lowest_loss = 3

while True:
    callback = model.fit_generator(training_generator, validation_data=validation_generator, steps_per_epoch=1000,
                                   epochs=1, max_queue_size=50, validation_steps=50)
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


