###
import random
import os
import numpy as np
from PIL import Image
from keras.utils import to_categorical
# really need to make sure this isn't just redundant with my im-char dicts cos I think it is
# if I use it make sure not to be doing weird non-matching conversions

from num_find_training_functions import gen_fake_image, generate_font_dictionary
# okay this thing needs to be a function that outputs close crops of the numbers as a training-data-generator
# and also outputs the label as a numpy array, which fills in leftover spaces with 'blanks'


def Close_Up_Image_Batch_Generator(image_list, font_index, batch_size, printing_numbers, guessing_numbers, end_index):
    # I want an array of images, 3*width*height*batchsize to feed into the data set
    # I also want array of corresponding Y/N values
    print('Spawning...')

    while True:
        selections = []
        labels = []

        while len(selections) < batch_size:
            im, min_x, min_y, max_x, max_y, num = gen_fake_image(image_list, font_index, printing_numbers)
            new_min_x = min_x - random.randint(0, 20)
            new_min_y = min_y - random.randint(0, 20)
            new_max_x = max_x + random.randint(0, 20)
            new_max_y = max_y + random.randint(0, 20)

            if new_min_x > 0 and new_min_y > 0 and new_max_x < im.size[0] and new_max_y < im.size[1]:
                close_up_crop = im.crop(box=(new_min_x, new_min_y, new_max_x, new_max_y))

            else:
                close_up_crop = im.crop([min_x, min_y, max_x, max_y])

            #close_up_crop.show()

            holder = []
            second_holder = []
            for i in num:
                holder.append(i)    # this feels like a silly way to do this....

            char_to_index = {ch: i for i, ch in enumerate(guessing_numbers)}
            for i in range(0, 10):
                if i < len(holder):
                    second_holder.append(char_to_index[holder[i]])
                else:
                    second_holder.append(end_index)


            baseheight = 50
            hpercent = (baseheight / float(close_up_crop.size[1]))
            wsize = int((float(close_up_crop.size[0]) * float(hpercent)))
            close_up_crop_resize = close_up_crop.resize((wsize, baseheight))

            #close_up_crop_resize.show()

            new_im = Image.new('RGB', (baseheight*8, baseheight), (255, 255, 255))

            new_im.paste(close_up_crop_resize, (0,0), mask=None)
            #new_im.show()

            if close_up_crop_resize.size[0] > new_im.size[0]:
                print("shit")
            selections.append(np.asarray(new_im).astype(float)/255)
            labels.append(np.asarray(second_holder))

        selections = np.asarray(selections)
        labels = np.asarray(labels)
        labels_cat = to_categorical(labels)
        yield selections, labels_cat



#
# BATCH_SIZE = 3
# bg_pics_dir = "/home/iolie/PycharmProjects/keras__practice/number_checker/lfw_mix"
#
#
# printing_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
#                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
#                     '-', ' ']
#
# guessing_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ' ']
#
# FONT_DIR = "/usr/share/fonts/truetype"
# font_index = generate_font_dictionary(FONT_DIR)
# numfonts = max(font_index.keys())
#
#
# piclist = []
# for dirpath, subdirs, files in os.walk(bg_pics_dir):
#     for f in files:
#         if f.endswith('.jpg'):
#             piclist.append(os.path.join(dirpath, f))
#
#
# index_to_char = {i: ch for i, ch in enumerate(guessing_numbers)}
# end_index = max(index_to_char.keys())+1
# #
# gen = Close_Up_Image_Batch_Generator(piclist, font_index, BATCH_SIZE, printing_numbers, guessing_numbers, end_index)
# #
# close_ups, nums, nums_cat = gen.next()
#
# print(close_ups.shape)
# print(nums.shape)
# print(nums)
# print(nums_cat.shape)
# print(nums_cat)