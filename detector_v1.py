import os
import random
import itertools
import collections
import numpy as np
from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from collections import namedtuple
from keras.models import model_from_json




def im_to_windowbatch(WINDOW_SIZE, image):
    im_size = image.size
    delta_w = im_size[0] % WINDOW_SIZE[0]
    delta_h = im_size[1] % WINDOW_SIZE[1]
    padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2), delta_h - (delta_h // 2))
    new_im = ImageOps.expand(image, padding)
    #new_im.show()
    batch = []
    rects = []
    x_place = 0
    add_rect_im = Image.new('RGBA', new_im.size, (255, 255, 255, 0))
    rect_im = ImageDraw.Draw(add_rect_im)
    for i in range(0, (new_im.size[0] // WINDOW_SIZE[0])*3):
        y_place = 0
        for j in range(0, (new_im.size[1] // WINDOW_SIZE[1])*3):
            bb = x_place, y_place, x_place + WINDOW_SIZE[0], y_place + WINDOW_SIZE[1]
            mini_pic = new_im.crop(box=bb)
            rect_im.rectangle([x_place, y_place, x_place + WINDOW_SIZE[0], y_place + WINDOW_SIZE[1]])

            arr = np.asarray(mini_pic).astype(float) / 255
            slim_arr = arr[:,:,:3]
            batch.append(slim_arr)
            rects.append(np.asarray(bb))

            y_place += WINDOW_SIZE[1] // 3
        x_place += WINDOW_SIZE[0] // 3

    # new_pic = Image.alpha_composite(new_im, add_rect_im).convert('RGB')
    # new_pic.show()

    #print(len(batch)) # 288 in a 230*230 pic
    batch = np.asarray(batch)
    rects = np.asarray(rects)
    # print(batch.shape)
    #print(rects.shape)
    return batch, rects, new_im

#
# def _overlaps(a, b):
#     bbox_tl1, bbox_br1 = a[0], a[3]
#     bbox_tl2, bbox_br2,= b[0], b[3]
#     return (bbox_br1[0] > bbox_tl2[0] and
#             bbox_br2[0] > bbox_tl1[0] and
#             bbox_br1[1] > bbox_tl2[1] and
#             bbox_br2[1] > bbox_tl1[1])
#
# def _group_overlapping_rectangles(hits):
#     matches = [[a[0], a[1], a[2], a[3]] for a in hits]
#     num_groups = 0
#     match_to_group = {}
#     for idx1 in range(len(matches)):
#         for idx2 in range(idx1):
#             if _overlaps(matches[idx1], matches[idx2]):
#                 match_to_group[idx1] = match_to_group[idx2]
#                 break
#         else:
#             match_to_group[idx1] = num_groups
#             num_groups += 1
#
#     groups = collections.defaultdict(list)
#     for ix, group in match_to_group.items():
#         groups[group].append(matches[ix])
#
#     return groups

#
# def post_process(hits):
#     """
#     Take an iterable of matches as returned by `detect` and merge duplicates.
#     Merging consists of two steps:
#       - Finding sets of overlapping rectangles.
#       - Finding the intersection of those sets, along with the code
#         corresponding with the rectangle with the highest presence parameter.
#     """
#     groups = _group_overlapping_rectangles(hits)
#
#     for group_matches in groups.values():
#         mins = np.stack(np.array(m[0]) for m in group_matches)
#         maxs = np.stack(np.array(m[1]) for m in group_matches)
#
#         yield (np.max(mins, axis=0).flatten(),
#                np.min(maxs, axis=0).flatten())







def intersection_area(a, b):  # returns None if rectangles don't intersect
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    #print(dx)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    #print(dy)
    if (dx>=0) and (dy>=0):
        return dx*dy





base_dir = "/home/iolie/PycharmProjects/keras__practice/number_checker/"
data_dir = "data"
model_dir = "savedmodels_numfinder_2/titletraining_weightsatloss_0.17"
os.chdir(base_dir)

json_file = open(os.path.join(model_dir, "model.json"), 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights(os.path.join(model_dir, "weights.h5"))
print("Loaded model from disk")


pics_dir = "/home/iolie/PycharmProjects/keras__practice/number_checker/numpics"
testlist = []
for dirpath, subdirs, files in os.walk(pics_dir):
    for f in files:
        if f.endswith('.jpg'):
            testlist.append(os.path.join(dirpath, f))


im = Image.open(testlist[random.randint(0, len(testlist)-1)]).convert('RGBA')
im.show()

WINDOW_SIZE = (60, 30)
batch, b_boxes, new_im = im_to_windowbatch(WINDOW_SIZE, im)

prediction = model.predict(batch, batch_size=1, verbose=0)
idx = prediction > 0.5
number_hits = b_boxes[idx[:,0],:]

add_rects_image = Image.new('RGBA', new_im.size, (255, 255, 255, 0))
final_rect_im = ImageDraw.Draw(add_rects_image)

for i in number_hits:
    final_rect_im.rectangle([i[0],i[1],i[2],i[3]])
# final_rect_im.rectangle([number_hits[0][0],number_hits[0][1],number_hits[0][2],number_hits[0][3]])  ## single square
new_pic = Image.alpha_composite(new_im, add_rects_image).convert('RGB')
new_pic.show()

Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')
#pairs_of_hits = list(itertools.combinations(range(len(number_hits)), 2))
# many_intersections = []
dict = {}
for x in range(len(number_hits)):
    a = Rectangle(number_hits[x][0], number_hits[x][1],number_hits[x][2],number_hits[x][3])
    counter = 0
    for y in number_hits:
        b = Rectangle(number_hits[x][0], number_hits[x][1],number_hits[x][2],number_hits[x][3])

        if intersection_area(a,b):
            counter += 1

    dict[x] = counter
    # if counter >= 6:
    #     many_intersections.append(number_hits[x])


### I am giving up for now --- need to get the minimal space in image possible to retain the whole number
#### bleh

print(dict)
print(len(number_hits))















#
# WINDOW_SIZE = (60, 30)
# counter = 0
# for i in testlist:
#
#     im = Image.open(i).convert('RGB')
#     # im_change = im.resize(WINDOW_SIZE)
#
#     arr = np.asarray(im).astype(float)/255
#     arr_2 = np.reshape(arr, (1, 30,60, 3))
#     prediction = model.predict(arr_2, batch_size=1, verbose=0)
#     print("*******************************")
#     print(i, prediction)
#     if prediction > 0.5:
#         if "_N" in i:
#             print("OOPS! THIS IS NO --- GUESSED YES", str(i), "_____", str(prediction))
#             counter +=1
#     else:
#         if "_Y" in i:
#             print("OOPS! THIS IS YES --- GUESSED NO", str(i), "_____", str(prediction))
#             counter += 1
#
# print(len(testlist))
# print(counter)