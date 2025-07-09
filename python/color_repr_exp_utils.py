import json
import numpy as np
from psychopy.tools.colorspacetools import hsv2rgb

# générer un angle aléatoire entre 0 et 180
def random_angle():
    return np.random.randint(0, 180)

# générer un nombre aléatoire entre 1 inclu et 9 inclu
def random_number():
    return np.random.randint(1, 10)

def angle_to_color(angle, blue_only = False):
    if blue_only:
        angle = (angle * 90)/360 + 180
    hsv_color = [angle, 0.5, 1.0]
    return hsv2rgb(hsv_color)

def load_parameters(file_path):
    with open(file_path, 'r') as f:
        parameters = json.load(f)

    return parameters
