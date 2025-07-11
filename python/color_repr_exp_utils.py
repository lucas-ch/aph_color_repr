import csv
import numpy as np
from psychopy.tools.colorspacetools import hsv2rgb
import random

import numpy as np
import random
import math

import config

# generate random hues: include selected and favorise colors next to this hue so it is not totally random
def generate_random_hues(hue, min_distance=2, n=36):
    hue = hue % 360
    range_angle = 75
    
    inside_center = np.random.randint(hue - range_angle, hue + range_angle) % 360
    
    inside_range = [c % 360 for c in range(inside_center - range_angle, inside_center + range_angle)]
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
    wheel_size = config.PARAMETERS["wheel_end"] - config.PARAMETERS["wheel_beginning"]
    angle = (angle * wheel_size)/360 + config.PARAMETERS["wheel_beginning"]
    hsv_color = [angle, 0.5, 1.0]
    return hsv2rgb(hsv_color)

def save_trial_and_next(exp, clock, response, stim, stim_type = 'angle', position = 0):
        exp.addData("onset", clock.getTime())
        exp.addData("stim", stim)
        exp.addData("stim_type", stim_type)
        exp.addData("response", response)
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

def get_file_name():
    participant_id = config.PARAMETERS['participant_id']
    recall_stim_type = config.PARAMETERS['recall_stim_type']
    match_stim_type = config.PARAMETERS['match_stim_type']
    response_type = config.PARAMETERS['response_type']

    task_type = 'recall'
    stim_type = recall_stim_type
    if recall_stim_type is None:
        task_type = 'match'
        stim_type = match_stim_type

    filename = f"aphantasia_{participant_id}_{task_type}_{stim_type}_to_{response_type}"
    if (
        config.PARAMETERS['recall_stim_type'] is None and
        config.PARAMETERS['response_type'] == 'text' and
        config.PARAMETERS['match_stim_type'] == 'color'
        ):
        filename = get_participant_describe_file_name()

    return filename

def get_participant_describe_file_name():
    parameters = config.PARAMETERS
    return f"aphantasia_{parameters['participant_id']}_describe_{parameters['nb_stim_total']}_colors_from_{parameters['wheel_beginning']}_to_{parameters['wheel_end']}"

def get_color_to_text_dict():
    data_path = config.PARAMETERS["data_path"]
    describe_file_name = config.PARAMETERS["color_to_text_filename"]

    if describe_file_name == "":
        describe_file_name = get_participant_describe_file_name()

    color_to_text = {}
    if describe_file_name is None or describe_file_name == "":
        return {}

    try:
        with open(f"{data_path}{describe_file_name}.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                color = float(row['stim'])
                text = row['response']
                color_to_text[color] = text

            return color_to_text
    except:
        return {}

