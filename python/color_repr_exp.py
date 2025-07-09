import numpy as np
import csv

from psychopy import visual, core, gui, data

from color_repr_exp_utils import load_parameters
from color_repr_exp_exps import *

# FUNCTIONS
# ---------
# générer un angle aléatoire entre 0 et 180
# MAIN
# ----

# Load parameters
parameters = load_parameters('parameters.json')

dlg = gui.Dlg(title="Aphantasia EEG experiment")
dlg.addField('Participant Id:', '')
dlg.addField('Task', choices=["match", "recall", "describe", "trad_text_to_color", "trad_color_to_spatial", "recall_spatial", "recall_hard"])
ok_data = dlg.show()

if dlg.OK:
    clock = core.Clock()
    win = visual.Window([800, 800], color=(0, 0, 0), units='pix', fullscr= not parameters["test"])
    task = ok_data['Task']
    
    file_name = f"data/aphantasia_{ok_data['Participant Id:']}_{task}"
    file_name_describe = f"data/aphantasia_{ok_data['Participant Id:']}_describe"

    exp = data.ExperimentHandler(name='aphantasia',
                                 extraInfo={'participant_id': ok_data['Participant Id:'],
                                            'task': ok_data['Task']},
                                 runtimeInfo=None,
                                 originPath=None,
                                 savePickle=False,
                                 saveWideText=True,
                                 dataFileName=f"../data/aphantasia_{ok_data['Participant Id:']}_{task}")
    
    color_to_text = {}
    if task == "trad_text_to_color":
        with open(f"{file_name_describe}.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                color = float(row['color_angle'])
                text = row['text']
                color_to_text[color] = text
    
    stimuli = get_stimuli(parameters, task)

    for stimulus in stimuli:
        if bool(color_to_text): 
            globals()[f"exp_{task}"](win, parameters, clock, stimulus, exp, color_to_text=color_to_text)
        else:
            globals()[f"exp_{task}"](win, parameters, clock, stimulus, exp)

    core.quit()
