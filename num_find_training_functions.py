import os
import numpy as np
import random
import colorsys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# this is quite bad use probability to control this later

def generate_phone_number(nums):
    return ''.join(random.choice(nums) for i in range(random.randint(7, 10)))

def generate_phone_number():
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


def add_text(thing_getting_drawn_on, width, height, numfonts, my_text):
    fnt = ImageFont.truetype(font_index[random.randint(0, numfonts)], random.randint(20,50))
    h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
    r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
    # removed the colour generator so the colours are always bright now!
    if fnt.getsize(num)[0] <= (width // 2 + 10):
        thing_getting_drawn_on.text((random.randint(0, (width // 2)), random.randint(0, height // 1.3)),
                my_text, fill=(r, g, b, 255),
                font= fnt)
    else:
        thing_getting_drawn_on.text((random.randint(0, (width // 2)), random.randint(0, height // 1.3)),
        my_text, fill = (r, g, b, 255),
        font = ImageFont.truetype(font_index[random.randint(0, numfonts)], random.randint(20, 25)))


def crop_image(im,size):
    w,h=im.size
    w_max,h_max = w-size[0],h-size[1]
    l,d = random.randint(0,w_max+1),random.randint(0,h_max+1)
    return im.crop(box=(l,d,l+size[0],d+size[1]))

def gen_train_image(numbers)


    num = str(generate_phone_number())
    big_pre_pic = Image.open(piclist[random.randint(0, len(piclist)-1)]).convert('RGBA')
    cropped_pre_pic = crop_image(big_pre_pic, size=[230, 230])
    txt_im = Image.new('RGBA', cropped_pre_pic.size, (255, 255, 255, 0))
    text_pic = ImageDraw.Draw(txt_im)
    add_text(text_pic, cropped_pre_pic.size[0], cropped_pre_pic.size[1], numfonts, num)
    new_pic = Image.alpha_composite(cropped_pre_pic, txt_im).convert('RGB')
    new_pic.show()

def shuffle_split_list(list):
    training_list = []
    validation_list = []
    for i in range(len(list)):
        if random.randint(0, 3) == 0:
            validation_list.append(i)
        else:
            training_list.append(i)
    return training_list, validation_list