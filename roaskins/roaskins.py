#!/usr/bin/python3
import json
import cv2
import numpy as np
import os
import operator
import errno
import random
import re
import importlib.resources
from typing import List
import pkg_resources

class ColorRGB:
    def __init__(self, r : np.uint8, g : np.uint8, b : np.uint8):
        self.r = r
        self.g = g
        self.b = b
    def to_hsv(self):
        img = np.zeros((1,1,3), np.uint8)
        # opencv expects bgr not rgb
        img[:] = (self.b, self.g, self.r)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return ColorHSV(img_hsv[0,0][0], img_hsv[0,0][1], img_hsv[0,0][2])
    def to_cv_tuple(self):
        return (self.b, self.g, self.r)

class ColorHSV:
    def __init__(self, h : np.uint8, s : np.uint8, v : np.uint8):
        self.h = h
        self.s = s
        self.v = v
    def to_rgb():
        img = np.zeros((1,1,3), np.uint8)
        # opencv expects bgr not rgb
        img[:] = (self.h, self.s, self.v)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
        return ColorRGB(img_hsv[0,0][2], img_hsv[0,0][1], img_hsv[0,0][0])
    def to_cv_tuple(self):
        return (self.h, self.s, self.v)

detection_color_hsv = ColorHSV(180/2, 256/2, 256/2)

class Rival:
    def __init__(self, name, aliases, data_dir):
        self.name = name
        self.aliases = aliases
        self.data_dir = data_dir
        self.shades = []
        shade_num = 0
        shade_f = self.data_dir + "/shade_" + str(shade_num) + ".png"
        while os.path.isfile(shade_f):
            print(shade_f)
            shade = cv2.imread(shade_f, cv2.IMREAD_UNCHANGED)
            if shade is None:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), shade_f)
            self.shades.append(shade)
            shade_num += 1
            shade_f = self.data_dir + "/shade_" + str(shade_num) + ".png"
        
        static_f = self.data_dir + "/static.png"
        if os.path.isfile(static_f):
            self.shade_static = cv2.imread(static_f, cv2.IMREAD_UNCHANGED)
            if self.shade_static is None:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), static_f)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), static_f)
        self.shade_num = len(self.shades)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def create_skin_from_colors(self, colors : List[ColorRGB] = []):
        if len(colors) != self.shade_num:
            return
        else:
            return Skin(self, colors)

    def create_skin_from_code(self, code):
        n = int(self.shade_num * 1.5)
        pattern = "^[a-fA-F0-9]{4}(\-[a-fA-F0-9]{4}){" + str(n) +"}$"
        p = re.compile(pattern)
        if not bool(p.match(code)):
            return None
        code_split = code.replace('-', '')
        # split after 2 chars
        colors_hex_list = [code_split[i:i+2] for i in range(0, len(code_split), 2)]
        if len(colors_hex_list) < self.shade_num * 3:
            return None

        colors = []
        checksum = 0
        for i in range(self.shade_num):
            r = int(colors_hex_list[i * 3], 16)
            checksum += (i + 101) * r
            g = int(colors_hex_list[i * 3 + 1], 16)
            checksum += (i + 102) * g
            b = int(colors_hex_list[i * 3 + 2], 16) 
            checksum += (i + 103) * b
            colors.append((r,g,b))
        checksum = checksum % 256
        # check if checksum is present
        if (len(colors_hex_list) > self.shade_num * 3 and \
            # and check it if present
            checksum != int(colors_hex_list[self.shade_num * 3], 16)):
            return None
        return Skin(self, colors)

    def create_random_skin(self):
        colors = []
        for i in range(self.shade_num):
            r = abs(random.randint(0,255))
            g = abs(random.randint(0,255))
            b = abs(random.randint(0,255))
            colors.append(ColorRGB(r, g, b))
        return self.create_skin_from_colors(colors)


class Skin:
    def __init__(self, rival : Rival, colors_rgb : List[ColorRGB]):
        if len(colors_rgb) != rival.shade_num:
            raise WRONG_COLORS
        self.colors_rgb = colors_rgb
        self.rival = rival
        self.code = ""
        self.__preview = None


    def get_preview(self):
        if not (self.__preview is None):
            return self.__preview
        # load files
        colors_hsv = list(map(lambda x: x.to_hsv(), self.colors_rgb))

        curr_color = 0
        skin = None
        for shade in self.rival.shades:
            b,g,r,a = cv2.split(shade)
            shade_hsv = cv2.cvtColor(shade, cv2.COLOR_BGR2HSV)
            h,s,v = cv2.split(shade_hsv)
            
            offs = np.subtract(detection_color_hsv.to_cv_tuple(), colors_hsv[curr_color].to_cv_tuple())
            lut_h = np.arange(256, dtype = np.dtype('uint8'))
            lut_v = np.arange(256, dtype = np.dtype('uint8'))
            lut_s = np.arange(256, dtype = np.dtype('uint8'))
            for i in range(256):
                lut_h[i] = np.uint8(max(0, (min(180, (i - offs[0]) % 180))))
                lut_s[i] = np.uint8(max(0, (min(255, (i - offs[1])))))
                lut_v[i] = np.uint8(max(0, (min(255, (i - offs[2])))))
            h = cv2.LUT(h, lut_h)
            s = cv2.LUT(s, lut_s)
            v = cv2.LUT(v, lut_v)

            skin_shade_hsv = cv2.cvtColor(cv2.merge((h,s,v)), cv2.COLOR_HSV2BGR)
            b,g,r = cv2.split(skin_shade_hsv)
            skin_shade = cv2.merge((b,g,r,a))

            curr_color += 1
            if skin is None:   
                skin = skin_shade
            else:
                skin = overlay_images(skin_shade, skin)

            self.__preview = overlay_images(self.rival.shade_static, skin)
        return self.__preview

    def save_preview(self, file_name : str):
        cv2.imwrite(file_name, self.get_preview())
        return

    def show_preview(self):
        cv2.imshow(str(self), self.get_preview())
        cv2.waitKey(0)
        return

    def __str__(self):
        if not self.code:
            counter = 0
            self.code = ""
            checksum = 0
            for i in range(len(self.colors_rgb)):
                for j in range(3):
                    if j == 0:
                        shade = self.colors_rgb[i].r
                    if j == 1:
                        shade = self.colors_rgb[i].g
                    if j == 2:
                        shade = self.colors_rgb[i].b
                    self.code += str('{:02x}'.format(int(shade)))
                    checksum += int(shade) * (i + 101 + j)
                    counter += 1
                    if counter % 2 == 0:
                        self.code += '-'
            # generate checksum
            self.code += str('{:02x}'.format(int(checksum) % 256))
            if counter % 2 == 0:
                self.code += "00"
            self.code = self.code.upper()
        return self.code
    
    def __repr__(self):
        return str(self.rival) + ": " + str(self)

# https://stackoverflow.com/a/59211216
def overlay_images(foreground : np.ndarray, background : np.ndarray):
    # normalize alpha channels from 0-255 to 0-1
    alpha_background = background[:,:,3] / 255.0
    alpha_foreground = foreground[:,:,3] / 255.0

    # set adjusted colors
    for color in range(0, 3):
        background[:,:,color] = alpha_foreground * foreground[:,:,color] + \
            alpha_background * background[:,:,color] * (1 - alpha_foreground)

    # set adjusted alpha and denormalize back to 0-255
    background[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255
    return background


def rival_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'Rival':
        return Rival(obj['name', 'aliases', 'color_num'])
    return obj

def load_rival_from_json(file : str):
    try:
        f = open(file, "r")
        rival = json.loads(f.read())
        f.close()
        return rival
    except OSError:
        print("exception")
        return

_rivals = {}

def rivals():
    if _rivals == {}:
        for filename in os.listdir(os.path.dirname(__file__) + "/data/"):
            rival_dict = load_rival_from_json(os.path.dirname(__file__) + "/data/"+filename+"/rival.json")
            print(rival_dict)
            if rival_dict:
                rival = Rival(rival_dict['name'], rival_dict['aliases'], os.path.dirname(__file__)+"/"+rival_dict['data_dir'])
                _rivals[rival.name] = rival
    return _rivals

if __name__ == "__main__":
    for rival in _rivals.values():
        rival.create_random_skin().show_preview()