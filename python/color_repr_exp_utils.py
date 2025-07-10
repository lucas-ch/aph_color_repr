import json
import csv
import numpy as np
from psychopy.tools.colorspacetools import hsv2rgb
import random

import numpy as np
import random
import math
def generate_random_hues(hue, min_distance=2, n=36):
    hue = hue % 360
    inside_center = np.random.randint(hue - 75, hue + 75) % 360
    inside_range = [c % 360 for c in range(inside_center - 45, inside_center + 45)]
    outside_range = [c for c in range(360) if c not in inside_range]

    def select_hues(candidate_range, count, include=None):
        selected = []
        if include is not None and include in candidate_range:
            selected.append(include)
        random.shuffle(candidate_range)
        for candidate in candidate_range:
            if candidate == include:
                continue  # déjà ajouté
            if all(min(abs(candidate - h), 360 - abs(candidate - h)) >= min_distance for h in selected):
                selected.append(candidate)
                if len(selected) == count:
                    break
        return selected

    # Assure que `hue` est inclus dans les teintes "intérieures"
    inside_hues = select_hues(inside_range, math.ceil(n/2), include=hue)
    outside_hues = select_hues(outside_range, math.floor(n/2))

    all_hues = inside_hues + outside_hues
    random.shuffle(all_hues)

    return all_hues

# générer un angle aléatoire entre 0 et 180
def random_angle():
    return np.random.randint(0, 180)

# générer un nombre aléatoire entre 1 inclu et 9 inclu
def random_number():
    return np.random.randint(1, 10)

def angle_to_color(angle):
    hsv_color = [angle, 0.5, 1.0]
    return hsv2rgb(hsv_color)

def load_parameters(file_path):
    with open(file_path, 'r') as f:
        parameters = json.load(f)

    return parameters

def save_trial_and_next(exp, clock, response, stim, stim_type = 'color_angle', position = 0):
        exp.addData("onset", clock.getTime())
        exp.addData("response", response)
        exp.addData("stim", stim)
        exp.addData("sequence_position", position)

        exp.nextEntry()

def get_exp_list():
    exp_list =  [
        "match",
        "recall_simple",
        "recall_parity",
        "recall_multi",
        "recall_squares",
        "recall_spatial",
        "describe",
        "trad_text_to_color",
        "trad_color_to_spatial"
        ]
    
    return exp_list
    
def get_color_to_text_dict(file_name_describe):
    color_to_text = {}
    if file_name_describe is None or file_name_describe == "":
        return {}

    try:
        with open(f"{file_name_describe}.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                color = float(row['stim'])
                text = row['response']
                color_to_text[color] = text            
            return color_to_text
    except:
        return {}

