import calendar
import json
import time
from psychopy import gui

PARAMETERS = {}

def load_parameters_file(file_path):
    with open(file_path, 'r') as f:
        parameters = json.load(f)

    return parameters

def open_dialog(parameters):
    recall_stim_type = get_recall_stim_type_list()
    match_stim_type = get_match_stim_type_list()
    response_type = get_response_type_list()
    defaults = parameters["defaults"]

    dlg = gui.Dlg(title="Aphantasia EEG experiment")
    dlg.addField('participant_id', initial= defaults["participant_id"])

    dlg.addField('recall_stim_type', initial = defaults["recall_stim_type"], choices=recall_stim_type)
    dlg.addField("match_stim_type", initial = defaults["match_stim_type"], choices=match_stim_type)
    dlg.addField('response_type', initial = defaults["response_type"], choices=response_type)

    dlg.addField('nb_stim_total', initial = defaults["nb_stim_total"], choices = [3, 15, 30, 45])
    dlg.addField('nb_stim_per_trial', initial=defaults["nb_stim_per_trial"], choices= [1, 3, 5, 15, 30, 45])
    dlg.addField('nb_parity', initial = defaults["nb_parity"], choices=[0, 1, 2, 3])
    dlg.addField('fullscreen', initial = defaults["fullscreen"], choices=[False, True])
    dlg.addField('color_to_text_filename', initial = defaults["color_to_text_filename"])

    ok_data = dlg.show()

    if dlg.OK:
        return ok_data

def get_recall_stim_type_list():
    return ['color', 'wheelGrey', 'text', None]

def get_match_stim_type_list():
    return [None, "text", "color"]

def get_response_type_list():
    return ['wheel', 'wheelGrey', 'squares', 'text']


def get_session_id(participant_id):
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)

    session_id = f"{participant_id}_{ts}"

    return session_id

def load_parameters(params_from_file={}, params_from_dialog={}):
    global PARAMETERS
    
    session_id = get_session_id(params_from_dialog["participant_id"])
    PARAMETERS = params_from_file | params_from_dialog
    PARAMETERS["session_id"] = session_id
    PARAMETERS.pop('defaults', None)
