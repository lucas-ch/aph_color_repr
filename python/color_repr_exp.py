from psychopy import visual, core, data

from color_repr_exp_utils import *
from color_repr_exp_exps import *

def launch_exp(ok_data, parameters):
    clock = core.Clock()
    win = visual.Window([800, 800], color=(0, 0, 0), units='pix', fullscr= not parameters["test"])

    task = ok_data['Task']
    participant_id = ok_data['Participant Id:']
    data_path = parameters["data_path"]
    
    stim_list = get_stim_list(parameters, task)

    exp = data.ExperimentHandler(name='aphantasia',
                                    extraInfo={'participant_id': participant_id,
                                                'task': task},
                                    runtimeInfo=None,
                                    originPath=None,
                                    savePickle=False,
                                    saveWideText=True,
                                    dataFileName=f"{data_path}aphantasia_{participant_id}_{task}")
    
    for stimulus in stim_list:
        launch_trial(win, parameters, clock, stimulus, exp, participant_id, task)

def main():
    parameters = load_parameters('parameters.json')
    ok_data = open_dialog() 
    launch_exp(ok_data, parameters)

main()