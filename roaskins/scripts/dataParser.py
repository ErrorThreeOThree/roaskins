#!/usr/bin/python

from sys import *
from cv2 import *
import numpy as np
import os, sys
from operator import sub
from operator import add
import copy
import functools 
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py
import roaskins

thresh = (100, 100, 100)
color = (179/2, 255/2, 255/2)
high = (tuple(map(add,color, thresh)))
low = tuple(map(sub, color, thresh))
high = (255, 255, 254)
low = (0,0,1)
imgs = []
def imgs_keep_common_pixels (a,b):
    img = copy.copy(a)
    rows,cols,depth = img.shape
    for i in range(0, rows):
        for j in range(0, cols):
            if set(a[i,j]) != set(b[i,j]):
                img[i,j] = (0,0,0,0)

    return img

aliases = []

offs = []
if (len(sys.argv) < 2):
    print("usage: datadir")
colornum = 0
data_path = argv[1]
for filename in os.listdir(argv[1]):
    if (filename == "name.txt"):
        fp = open(data_path + filename)
        name = fp.readline().rstrip('\n')
    elif (filename == "aliases.txt"):
        fp = open(data_path + filename)
        for line in fp:
            aliases.append(line.rstrip('\n'))
            line = fp.readline
    if not (filename.startswith("color_") and filename.endswith(".png")):
        continue
    img = imread(data_path + filename, IMREAD_UNCHANGED)
    imgs.append(img)
    b,g,r,a = split(img)
    img_hsv = cvtColor(img, COLOR_BGR2HSV)
    hsv_mask = inRange(img_hsv, low, high)

    mask_inv = bitwise_not(hsv_mask)
    mask = bitwise_and(hsv_mask, a)
    img_color = copy.copy(img_hsv)
    img_color[:] = color
    img_bgr_2 = cvtColor(img_hsv, COLOR_HSV2BGR)
    img_thresh = bitwise_and(img_bgr_2, img_bgr_2, mask=mask)
    b,g,r, = split(img_thresh)
    final = merge((b,g,r,mask))
    imshow("a" + filename, img)
    imwrite(data_path + "/shade_" + str(colornum)+".png", final)

    colornum += 1
result = functools.reduce(imgs_keep_common_pixels, imgs, imgs[0] )
imwrite(data_path + "static.png", result)
imshow("result" + filename, result)
waitKey(0)

#create json representation
rival = skinGenROA.Rival(name, aliases, data_path)
f = open(data_path + "/rival.json", "w+")
f.write('{{\"name\": "{}", "aliases": ["{}"], "color_num": {}, "data_dir": "{}"}}'.format(name, '", "'.join(aliases), colornum, data_path))