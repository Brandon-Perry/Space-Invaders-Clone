import pyglet
import math
import random

def distance(point_1=(0,0), point_2=(0,0)):
    #returns the distance between two points

    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

def angle(point_1=(0,0), point_2=(0,0)):
    return math.atan2(point_2[1] - point_1[1],point_2[0] - point_1[0])