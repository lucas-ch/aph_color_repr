import json
import csv
import numpy as np
from psychopy.tools.colorspacetools import hsv2rgb
import random

def generate_random_hues(hue, n=25, min_distance=2):
    if n > 180 // min_distance:
        raise ValueError("Trop de couleurs demandées pour la contrainte de distance minimale.")

    center = np.random.randint(int(hue - 45), int(hue + 45)) % 360
    candidate_range = list(range(center - 90, center + 90))
    candidate_range = [c % 360 for c in candidate_range]

    selected_hues = [hue % 360]  # inclure la teinte principale
    random.shuffle(candidate_range)

    for candidate in candidate_range:
        if all(min(abs(candidate - h), 360 - abs(candidate - h)) >= min_distance for h in selected_hues):
            selected_hues.append(candidate)
            if len(selected_hues) == n:
                break

    if len(selected_hues) < n:
        raise ValueError("Impossible de générer suffisamment de couleurs respectant la distance minimale.")

    print(hue)
    print(sorted(selected_hues))
    random.shuffle(selected_hues)

    return selected_hues

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

def save_trial_and_next(exp, clock, response, stim, stim_type = 'color_angle', position = 0):
        exp.addData("onset", clock.getTime())
        exp.addData("response", response)
        exp.addData("stim", stim)
        exp.addData("stim_type", stim_type)
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
    
def get_stim_list(parameters, task):
    nb_colors_total = parameters["nb_colors"]
    nb_colors_per_stim = parameters["nb_colors_recall_multi"]

    stimuli = np.arange(0, 360, 360/nb_colors_total)
    np.random.shuffle(stimuli)

    if task == "recall_multi":
        nb_stim = int(len(stimuli)/nb_colors_per_stim)
        stim_list = []

        begin = 0
        end = begin + nb_colors_per_stim
        for i in range(nb_stim):
            stim_list.append(stimuli[begin:end])
            begin = begin + nb_colors_per_stim
            end = end + nb_colors_per_stim
        
    else:
        stim_list = stimuli
    
    return stim_list

def get_color_to_text_dict(file_name_describe):
    color_to_text = {}
    with open(f"{file_name_describe}.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            color = float(row['color_angle'])
            text = row['text']
            color_to_text[color] = text