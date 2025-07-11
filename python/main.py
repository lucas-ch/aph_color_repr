from psychopy import visual, core, data
import config

from color_repr_exp_utils import *
from color_repr_exp_exps import *
import calendar;
import time;

def launch_exp():
    clock = core.Clock()
    win = visual.Window(
        [800, 800],
        color=(0, 0, 0),
        units='pix',
        fullscr= config.PARAMETERS["fullscreen"])

    filename = get_file_name()    
    stim_list = get_stim_list()
    color_to_text = get_color_to_text_dict()

    exp = data.ExperimentHandler(name='aphantasia',
                                    extraInfo={'participant_id': config.PARAMETERS['participant_id'],
                                               'session_id': config.PARAMETERS['session_id'],                 
                                                'recall_stim_type': config.PARAMETERS['recall_stim_type'],
                                                'response_type': config.PARAMETERS['response_type'],
                                                'match_stim_type': config.PARAMETERS['match_stim_type'],
                                                'parameters': config.PARAMETERS
                                                },
                                    runtimeInfo=None,
                                    originPath=None,
                                    savePickle=False,
                                    saveWideText=True,
                                    dataFileName= f"{config.PARAMETERS['data_path']}{filename}")
    
    for stimuli in stim_list:
        launch_trial(
            win,
            clock,
            stimuli,
            exp,
            color_to_text=color_to_text)

def main():
    parameters = config.load_parameters_file('parameters.json')
    ok_data = config.open_dialog(parameters)

    config.load_parameters(parameters, ok_data)

    launch_exp()

if __name__ == "__main__":
    main()