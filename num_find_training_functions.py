import os
import numpy as np
import random
import colorsys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from collections import namedtuple
from keras.utils import to_categorical


# this is quite bad use probability to control this later

def generate_phone_number(numbers):
    return ''.join(random.choice(numbers) for i in range(random.randint(7, 10)))

def generate_font_dictionary(FONT_DIR):
    fonts = []
    for dirpath, subdirs, files in os.walk(FONT_DIR):
        for f in files:
            if f.endswith('.ttf'):
                fonts.append(os.path.join(dirpath, f))

    badfonts = ['/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
                '/usr/share/fonts/truetype/kacst/KacstTitleL.ttf',
                '/usr/share/fonts/truetype/fonts-guru-extra/Saab.ttf',
                '/usr/share/fonts/truetype/kacst/KacstPen.ttf',
                '/usr/share/fonts/truetype/kacst/KacstTitle.ttf',
                '/usr/share/fonts/truetype/kacst/KacstDigital.ttf',
                '/usr/share/fonts/truetype/kacst/KacstNaskh.ttf',
                '/usr/share/fonts/truetype/kacst/KacstLetter.ttf',
                '/usr/share/fonts/truetype/kacst/mry_KacstQurn.ttf',
                '/usr/share/fonts/truetype/kacst/KacstScreen.ttf',
                '/usr/share/fonts/truetype/kacst/KacstArt.ttf',
                '/usr/share/fonts/truetype/kacst/KacstOffice.ttf',
                '/usr/share/fonts/truetype/kacst/KacstPoster.ttf',
                '/usr/share/fonts/truetype/kacst/KacstDecorative.ttf',
                '/usr/share/fonts/truetype/kacst/KacstFarsi.ttf',
                '/usr/share/fonts/truetype/kacst/KacstQurn.ttf',
                '/usr/share/fonts/truetype/kacst/KacstBook.ttf',
                '/usr/share/fonts/truetype/openoffice/opens___.ttf',
                '/usr/share/fonts/truetype/sinhala/lklug.ttf']

    for badfont in badfonts:
        fonts.remove(badfont)

    font_index = {i: f for i, f in enumerate(fonts)}
    return font_index


def add_text(thing_getting_drawn_on, width, height, my_text, font_index):
    fnt = ImageFont.truetype(font_index[random.randint(0, max(font_index.keys()))], random.randint(20,50))
    smallfnt = ImageFont.truetype(font_index[random.randint(0, max(font_index.keys()))], random.randint(10, 20))

    h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
    r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
    # removed the colour generator so the colours are always bright now!
    place_x = random.randint(0, width // 2)
    place_y = random.randint(0, height // 1.3)

    if fnt.getsize(my_text)[0] <= (width // 2 + 10):
        thing_getting_drawn_on.text((place_x, place_y), my_text, fill=(r, g, b, 255), font=fnt)
        max_x = place_x + fnt.getsize(my_text)[0]
        max_y = place_y + fnt.getsize(my_text)[1]
    else:
        thing_getting_drawn_on.text((place_x, place_y), my_text, fill=(r, g, b, 255),
                                    font=smallfnt)
        max_x = place_x + smallfnt.getsize(my_text)[0]
        max_y = place_y + smallfnt.getsize(my_text)[1]

    return place_x, place_y, max_x, max_y


def crop_image(im,size):
    w,h=im.size
    w_max,h_max = w-size[0],h-size[1]
    l,d = random.randint(0,w_max+1),random.randint(0,h_max+1)
    return im.crop(box=(l,d,l+size[0],d+size[1]))

def gen_fake_image(image_list, font_index, numbers):
    num = str(generate_phone_number(numbers))
    big_pre_pic = Image.open(image_list[random.randint(0, len(image_list)-1)]).convert('RGBA')
    cropped_pre_pic = crop_image(big_pre_pic, size=[230, 230])
    txt_im = Image.new('RGBA', cropped_pre_pic.size, (255, 255, 255, 0))
    text_pic = ImageDraw.Draw(txt_im)
    min_x, min_y, max_x, max_y = add_text(text_pic, cropped_pre_pic.size[0], cropped_pre_pic.size[1], num, font_index)
    new_pic = Image.alpha_composite(cropped_pre_pic, txt_im).convert('RGB')
    #new_pic_arr = np.array(new_pic)
    #new_pic.show()
    return new_pic, min_x, min_y, max_x, max_y


def shuffle_split_list(list):
    training_list = []
    validation_list = []
    for i in range(len(list)):
        if random.randint(0, 3) == 0:
            validation_list.append(list[i])
        else:
            training_list.append(list[i])
    return training_list, validation_list

def intersection_area(a, b):  # returns None if rectangles don't intersect
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    #print(dx)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    #print(dy)
    if (dx>=0) and (dy>=0):
        return dx*dy


def Image_Batch_Generator(image_list, font_index, batch_size, WINDOW_SIZE, numbers):
    Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')
    # I want an array of images, 3*width*height*batchsize to feed into the data set
    # I also want array of corresponding Y/N values
    print('Spawning...')

    while True:
        selections = []
        labels = []

        pos_counter = 0
        neg_counter = 0
        while len(selections) < batch_size:
            im, min_x, min_y, max_x, max_y = gen_fake_image(image_list, font_index, numbers)
            font_rectangle = Rectangle(min_x, min_y, max_x, max_y)
            font_area = (max_x - min_x) * (max_y - min_y)

            x_place = 0
            for i in range(0, (im.size[0] // WINDOW_SIZE[0])):
                y_place = 0
                for j in range(0, (im.size[1] // WINDOW_SIZE[1])):
                    mini_pic = im.crop(box=(x_place, y_place, x_place + WINDOW_SIZE[0], y_place + WINDOW_SIZE[1]))
                    window_rectangle = Rectangle(x_place, y_place, x_place + WINDOW_SIZE[0], y_place + WINDOW_SIZE[1])

                    if (intersection_area(window_rectangle, font_rectangle) >= font_area * 0.075) and (pos_counter < batch_size//2):
                        selections.append(np.asarray(mini_pic))
                        labels.append(1)
                        pos_counter += 1

                    elif (intersection_area(window_rectangle, font_rectangle) <= font_area * 0.075) and (neg_counter < batch_size//2):
                        selections.append(np.asarray(mini_pic))
                        labels.append(0)
                        neg_counter += 1

                    y_place += WINDOW_SIZE[1] / 2
                x_place += WINDOW_SIZE[0] / 2

        selections = np.asarray(selections)
        labels = np.asarray(labels)
        labels_cat = to_categorical(labels)  # remove if doing binary_crossentropy and output labels instead

        yield selections, labels_cat



