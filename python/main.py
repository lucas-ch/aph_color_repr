from psychopy import visual, core, data

from color_repr_exp_utils import *
from color_repr_exp_exps import *
import calendar;
import time;

def get_session_id(participant_id):
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)

    session_id = f"{participant_id}_{ts}"

    return session_id

def launch_exp(parameters):
    parameters.pop('defaults', None)

    clock = core.Clock()
    win = visual.Window(
        [800, 800],
        color=(0, 0, 0),
        units='pix',
        fullscr= parameters["fullscreen"])

    task = f"from_{parameters['recall_stim_type']}_to_{parameters['response_type']}_with_{parameters['match_stim_type']}"

    participant_id = parameters['participant_id']
    session_id = get_session_id(participant_id)
    data_path = parameters["data_path"]
    
    stim_list = get_stim_list(parameters)
    color_to_text_filename =  f"{data_path}{parameters['color_to_text_filename']}"
    color_to_text = get_color_to_text_dict(color_to_text_filename)

    exp = data.ExperimentHandler(name='aphantasia',
                                    extraInfo={'participant_id': participant_id,
                                               'session_id': session_id,                 
                                                'recall_stim_type': parameters['recall_stim_type'],
                                                'response_type': parameters['response_type'],
                                                'match_stim_type': parameters['match_stim_type'],
                                                'parameters': parameters
                                                },
                                    runtimeInfo=None,
                                    originPath=None,
                                    savePickle=False,
                                    saveWideText=True,
                                    dataFileName=f"{data_path}aphantasia_{session_id}_{task}")
    
    for stimuli in stim_list:
        launch_trial(
            win,
            parameters,
            clock,
            stimuli,
            exp,
            participant_id,
            color_to_text=color_to_text)

def main():
    parameters = load_parameters('parameters.json')
    ok_data = open_dialog(parameters)
    parameters = parameters | ok_data

    launch_exp(parameters)

main()