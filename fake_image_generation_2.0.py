import os
import random
import colorsys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','-', ' ']
# this is quite bad use probability to control this later

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

    return place_x, place_y, max_x, max_y



def crop_image(im,size):
    w,h=im.size
    w_max,h_max = w-size[0],h-size[1]
    l,d = random.randint(0,w_max+1),random.randint(0,h_max+1)
    return im.crop(box=(l,d,l+size[0],d+size[1]))

#bg_pics_dir = "/home/iolie/PycharmProjects/keras__practice/Instapics"
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


def Generate_Image(model,MAX_LEN,first_char_probs,index_to_char,char_to_index,num_chars,end_index):
    generated = index_to_char[ChooseCharacter(first_char_probs)]
    #print(generated)
    while True:
        input = np.zeros((1, min(len(generated),MAX_LEN), num_chars), dtype=np.bool)  # this is making a BOOLEAN matrix,not sure why it's this shape
        input_index_offset = max(0, len(generated)- MAX_LEN)  #
        for i in range(max(0,len(generated)-MAX_LEN),len(generated)):  # input_index_offset # whaaat?
            input[0, i-input_index_offset, char_to_index[generated[i]]]=1 ## this fills the input matric with the info so far
        prediction = model.predict(input, batch_size=1,verbose=0)
        prediction_b = prediction[0].astype('float64')
        nextindex = ChooseCharacter(prediction_b)
        if nextindex == end_index or len(generated) == 100:  # start -- let rant for longer later!
            return generated
        nextchar = index_to_char[nextindex]
        generated = generated + nextchar



    new_pic.save(os.path.join(num_pics, str(num) + ".jpg"), format='jpeg')