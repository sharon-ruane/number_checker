from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import random

def generate_phone_number(numbers):
    return ''.join(random.choice(numbers) for i in range(random.randint(7, 10)))

r = lambda: random.randint(40,255)
s = lambda: random.randint(20,50)
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','-', ' ']
# this is quite bad use probability to control this later

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

def add_text(thing_getting_drawn_on, width, height, num):
    fnt = ImageFont.truetype(font_index[random.randint(0, numfonts)], s())
    if fnt.getsize(num)[0] <= (width // 2 + 10):
        thing_getting_drawn_on.text((random.randint(0, (width // 2)), random.randint(0, height // 1.3)),
                num, fill=(r(), r(), r(), 255),
                font= fnt)
    else:
        thing_getting_drawn_on.text((random.randint(0, (width // 2)), random.randint(0, height // 1.3)),
        num, fill = (r(), r(), r(), 255),
        font = ImageFont.truetype(font_index[random.randint(0, numfonts)], 20))

def crop_image(im,size):
    w,h=im.size
    w_max,h_max = w-size[0],h-size[1]
    l,d = random.randint(0,w_max+1),random.randint(0,h_max+1)
    return im.crop(box=(l,d,l+size[0],d+size[1]))

def generate_image(images_list, num):
    big_im = Image.open(images_list[random.randint(0, len(images_list)-1)]).convert('RGBA')
    #big_im.show()
    im = crop_image(big_im, size=[230, 230])
    #im.show()
    txt = Image.new('RGBA', im.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    add_text(draw, im.size[0], im.size[1], num)
    out = Image.alpha_composite(im, txt)
    #out.show()
    return out


piclist = []
# for dirpath, subdirs, files in os.walk("/home/iolie/PycharmProjects/keras__practice/Instapics"):
for dirpath, subdirs, files in os.walk("/home/iolie/PycharmProjects/keras__practice/number_checker/lfw_mix"):
    for f in files:
        if f.endswith('.jpg'):
            piclist.append(os.path.join(dirpath, f))
#print(len(piclist))

FONT_DIR = "/usr/share/fonts/truetype"
font_index = generate_font_dictionary(FONT_DIR)
numfonts = max(font_index.keys())

num_pics = 'numpics'
if not os.path.isdir(num_pics):
    os.makedirs(num_pics)

for i in range(0,100000):
    num = str(generate_phone_number())
    new_pic = generate_image(piclist, num).convert("RGB")
    new_pic.save(os.path.join(num_pics, str(num) + ".jpg"), format= 'jpeg')







#im = Image.open("flower.jpg").convert('RGBA')
#app_im = Image.open("/home/iolie/PycharmProjects/thorn/sharon/Minisample/0A0A937C-016C-49E6-A9CA-480292B491BC_3.jpg").convert('RGBA')
#basicfont= ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", s())


# font_index = generate_font_dictionary(FONT_DIR)
# print(font_index[4])
# numfonts = max(font_index.keys())
# print(numfonts)


# txt = Image.new('RGBA', im.size, (255, 255, 255, 0))
# draw = ImageDraw.Draw(txt)
# add_text(draw, im.size[0], im.size[1])
# out = Image.alpha_composite(im, txt)
# out.show()


# print(generate_phone_number())
# print(fonts)
# for font in fonts[]:
#     txt = Image.new('RGBA', im.size, (255, 255, 255, 0))
#     draw = ImageDraw.Draw(txt)
#     if font.endswith("pil"):
#         fnt = ImageFont.load(font, 40)
#     else:
#         fnt = ImageFont.truetype(font, 40)
#     draw.text((10,10), "0123456789", font=fnt) #(255,255,255,255)
#     draw.text((10,60), str(font), font = basicfont)
#     out = Image.alpha_composite(im, txt)
#     out.show()



# basicfont= ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 15)
# font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
#
# im = Image.open("flower.jpg").convert('RGBA')  ## do I need this bit!
#
# txt = Image.new('RGBA', im.size, (255,255,255,0))
# draw = ImageDraw.Draw(txt)
# draw.text((10,10), "Hello", font=font) #(255,255,255,255)
#
# out = Image.alpha_composite(im, txt)
# out.show()

#
# def load_fonts(folder_path):
#     font_char_ims = {}
#     fonts = [f for f in os.listdir(folder_path) if f.endswith('.ttf')]
#     for font in fonts:
#         font_char_ims[font] = dict(make_char_ims(os.path.join(folder_path,
#                                                               font),
#                                                  FONT_HEIGHT))
# return fonts, font_char_ims




# def tile_faces(key, odds):
#     pics_to_display = []
#     for x in os.listdir(os.path.join(image_path, key)):
#         a = os.path.join(image_path, key, x)
#         b = PIL.Image.open(a)
#         pics_to_display.append(b)
#
#     width = pics_to_display[0].width
#     total_width = width * (len(pics_to_display)+2)
#     height = pics_to_display[0].height
#
#     hm = PIL.Image.new('RGB', (width*2, height))
#     hmm = ImageDraw.Draw(hm)
#     hmm.text((20, 70), (str(key + "     " + odds)))
#     pics_to_display.append(hm)
#
#     new_im = PIL.Image.new('RGB', (total_width, height))
#     x_offset = 0
#
#     for im in pics_to_display:
#         new_im.paste(im, (x_offset, 0))
#         x_offset += width
#
#     return(new_im)