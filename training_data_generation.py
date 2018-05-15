import os
import random
import colorsys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from collections import namedtuple

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')',
           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','-']
# this is quite bad use probability to control this later

def generate_phone_number():
    return ''.join(random.choice(numbers) for i in range(random.randint(7, 14)))

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


def add_text(thing_getting_drawn_on, width, height, numfonts, my_text):
    fnt = ImageFont.truetype(font_index[random.randint(0, numfonts)], random.randint(20,50))
    smallfnt = ImageFont.truetype(font_index[random.randint(0, numfonts)], random.randint(10, 20))
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
        font= smallfnt)
        max_x = place_x + smallfnt.getsize(my_text)[0]
        max_y = place_y + smallfnt.getsize(my_text)[1]

    print(fnt.getsize(my_text))
    return place_x, place_y, max_x, max_y


def crop_image(im,size):
    w,h=im.size
    w_max,h_max = w-size[0],h-size[1]
    l,d = random.randint(0,w_max+1),random.randint(0,h_max+1)
    return im.crop(box=(l,d,l+size[0],d+size[1]))


def intersection_area(a, b):  # returns None if rectangles don't intersect
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    print(dx)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    print(dy)
    if (dx>=0) and (dy>=0):
        return dx*dy


bg_pics_dir = "/home/iolie/PycharmProjects/keras__practice/number_checker/lfw_mix"

piclist = []
for dirpath, subdirs, files in os.walk(bg_pics_dir):
    for f in files:
        if f.endswith('.jpg'):
            piclist.append(os.path.join(dirpath, f))

FONT_DIR = "/usr/share/fonts/truetype"
font_index = generate_font_dictionary(FONT_DIR)
numfonts = max(font_index.keys())

num_pics = 'numpics'
if not os.path.isdir(num_pics):
    os.makedirs(num_pics)

window_pics = 'window_pics'
if not os.path.isdir(window_pics):
    os.makedirs(window_pics)


WINDOW_SIZE = (50, 25)
Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')


for i in range(0, 5):
    num = str(generate_phone_number())
    big_pre_pic = Image.open(piclist[random.randint(0, len(piclist)-1)]).convert('RGBA')
    cropped_pre_pic = crop_image(big_pre_pic, size=[230, 230])
    txt_im = Image.new('RGBA', cropped_pre_pic.size, (255, 255, 255, 0))
    text_pic = ImageDraw.Draw(txt_im)
    min_x, min_y, max_x, max_y = add_text(text_pic, cropped_pre_pic.size[0], cropped_pre_pic.size[1], numfonts, num)
    font_rectangle = Rectangle(min_x, min_y, max_x, max_y)
    font_area = (max_x - min_x)*(max_y-min_y)
    # text_pic.rectangle([min_x, min_y, max_x, max_y], fill = None)
    # print(min_x, min_y, max_x, max_y)
    new_pic = Image.alpha_composite(cropped_pre_pic, txt_im).convert('RGB')
    new_pic.show()

    x_place = 0
    for i in range(0, (cropped_pre_pic.size[0]//WINDOW_SIZE[0])):
        y_place = 0
        for j in range(0, (cropped_pre_pic.size[1]//WINDOW_SIZE[1])):
            mini_pic = new_pic.crop(box=(x_place, y_place, x_place + WINDOW_SIZE[0], y_place + WINDOW_SIZE[1]))
            window_rectangle = Rectangle(x_place, y_place, x_place + WINDOW_SIZE[0], y_place + WINDOW_SIZE[1])

            if intersection_area(window_rectangle,font_rectangle) >= font_area*0.075:
                mini_pic.save(os.path.join(window_pics, str(num) + "_" + str(i) + "_" + str(j) + "_Y" + ".jpg"), format='jpeg')
            else:
                mini_pic.save(os.path.join(window_pics, str(num) + "_" + str(i) + "_" + str(j) + "_N" + ".jpg"), format='jpeg')
            y_place += WINDOW_SIZE[1]/2
        x_place += WINDOW_SIZE[0]/2


    #new_pic.save(os.path.join(num_pics, str(num) + ".jpg"), format='jpeg')