from csv import reader
from os import walk
from natsort import natsorted, ns
import pygame

def import_csv_layout(path):  # give path, return list of lists
    map = []
    with open(path, 'r') as f:
        csv_file = reader(f)
        for row in csv_file: map.append(row)
    return map

def import_folder(path):
    animation_set = []
    for _,__,images in walk(path):
        images_sorted = natsorted(images, key=lambda y: y.lower())
        for image in images_sorted:
            full_path = path + image
            animation_set.append(pygame.image.load(full_path).convert_alpha())

    return animation_set

# import_folder('../graphics/player/down/')
