from color_repr_exp_draw import *
from color_repr_exp_utils import *
import config

def get_stim_list():
    parameters = config.PARAMETERS
    nb_stim_total = parameters["nb_stim_total"]
    nb_stim_per_trial = parameters["nb_stim_per_trial"]

    stimuli = np.arange(0, 360, 360/nb_stim_total)
    np.random.shuffle(stimuli)

    nb_stim = int(len(stimuli)/nb_stim_per_trial)
    stim_list = []

    begin = 0
    end = begin + nb_stim_per_trial
    for i in range(nb_stim):
        stim_list.append(stimuli[begin:end])
        begin = begin + nb_stim_per_trial
        end = end + nb_stim_per_trial
    
    return stim_list

def draw_recall_stim(win, stimulus, color_to_text):
    parameters = config.PARAMETERS
    match parameters['recall_stim_type']:
        case 'color':
            return draw_circle(
                win,
                parameters["circle_size"],
                angle_to_color(stimulus),
                how_long=1.0)

        case 'wheelGrey':
            return draw_color_wheel(
                win,
                mode='stim_spatial',
                hide_wheel = True,
                hide_cursor= True,
                how_long=1.0,
                real=stimulus)

        case 'text':
            draw_text_recall_stim(win, stimulus, color_to_text)

        case _:
            return
        
def draw_parity_task(win, clock, exp, position):
            
    number = np.random.randint(1, 10)
    response = draw_number(win, number, clock, 1.5)
    save_trial_and_next(exp, clock, response, number, 'parity', position)

def get_participant_response_wheel(win, stimulus, color_to_text=None):
    parameters = config.PARAMETERS
    hide_wheel = False
    hide_cursor = False
    response_mode = "feedback"

    # decide if we show wheel and cursor color depending on the task
    if parameters["response_type"] == "wheelGrey":
        hide_wheel = True
        hide_cursor = True

        if parameters['recall_stim_type'] ==  "wheelGrey":
            response_mode = "stim_spatial"

    center_circle_color_angle = None
    if parameters['match_stim_type'] == "color":
        center_circle_color_angle=stimulus

    top_text = None
    if parameters['match_stim_type'] == "text":
        top_text=color_to_text[stimulus]

    response = draw_color_wheel(
        win,
        mode='choice',
        center_circle_color_angle =center_circle_color_angle,
        top_text= top_text,
        hide_wheel = hide_wheel,
        hide_cursor = hide_cursor)

    print(response)
    draw_color_wheel(
        win,
        mode=response_mode,
        how_long=0.5,
        real = stimulus,
        response=response,
        hide_wheel = hide_wheel,
        hide_cursor = hide_cursor)
            
    return response

def get_participant_response(win, stimulus, color_to_text=None):
    parameters = config.PARAMETERS
        
    match parameters['response_type']:
        case 'text':
            with_color = parameters["match_stim_type"] == "color"
            response = draw_text_input(win, with_color, stimulus)
            return response

        case 'squares':
            hues = generate_random_hues(stimulus)
            response = draw_choose_color_rect(
                win,
                hues,
                stimulus,
                parameters['match_stim_type'],
                color_to_text)

            return response

        case 'wheel' | 'wheelGrey':
            response = get_participant_response_wheel(win, stimulus, color_to_text)
            return response

        case _:
            print('response_type not handled')
            return

def launch_trial(win, clock, stimuli, exp, color_to_text=None):
    parameters = config.PARAMETERS
    draw_fixation_cross(win, how_long=0.5)

    for stimulus in stimuli:
        draw_recall_stim(win, stimulus, color_to_text)
        if parameters['recall_stim_type'] is not None:
            draw_empty_screen(win, how_long=0.5)

    for i in range(parameters["nb_parity"]):
        draw_empty_screen(win, how_long=0.5)
        draw_parity_task(win, clock, exp, i)
        draw_empty_screen(win, how_long=0.5)

    if parameters['recall_stim_type'] is not None:
        draw_empty_screen(win, how_long=parameters['maintenance_time'])

    for i, stimulus in enumerate(stimuli):
        print(stimulus)
        response = get_participant_response(win, stimulus, color_to_text)

        draw_empty_screen(win, how_long=0.1)
        save_trial_and_next(exp, clock, response, stimulus, stim_type = 'angle', position = i)
