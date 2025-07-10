from color_repr_exp_draw import *
from color_repr_exp_utils import *

def get_stim_list(parameters):
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

def draw_recall_stim(win, stimulus, parameters, color_to_text):
    match parameters['recall_stim_type']:
        case 'color':
            return draw_circle(
                win,
                parameters["circle_size"],
                angle_to_color(stimulus),
                how_long=1.0)

        case 'spatial':
            return draw_color_wheel(
                win,
                parameters["inner_radius"],
                parameters["outer_radius"],
                mode='stim_spatial',
                hide = True,
                how_long=1.0,
                real=stimulus)

        case 'text':
            draw_text_recall_stim(win, stimulus, color_to_text)

        case _:
            return
        
def draw_parity_task(win, clock, exp, position):
            
    number = np.random.randint(1, 10)
    response = draw_number(win, number, clock, 1.5)
    save_trial_and_next(exp, clock, response[0], number, position)

def get_participant_response_wheel(win, parameters, stimulus, color_to_text=None):
    hide_wheel_and_cursor_color = False
    
    if (parameters["match_stim_type"] is not None
            or parameters["recall_stim_type"] == "spatial"):
        hide_wheel_and_cursor_color = True

    center_circle_color_angle = None
    if parameters['match_stim_type'] == "color":
        center_circle_color_angle=stimulus

    top_text = None
    if parameters['match_stim_type'] == "text":
        top_text=color_to_text[stimulus]

    response_mode = "feedback"
    if parameters["recall_stim_type"] == "spatial":
        response_mode = "stim_spatial"

    response = draw_color_wheel(
        win,
        parameters["inner_radius"],
        parameters["outer_radius"],
        mode='choice',
        center_circle_color_angle =center_circle_color_angle,
        top_text= top_text,
        hide = hide_wheel_and_cursor_color)

    draw_color_wheel(
        win,
        parameters["inner_radius"],
        parameters["outer_radius"],
        mode=response_mode,
        how_long=0.5,
        response=response,
        real=stimulus,
        hide = hide_wheel_and_cursor_color)
            
    return response

def get_participant_response(win, parameters, stimulus, color_to_text=None):
        
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

        case 'wheel':
            response = get_participant_response_wheel(win, parameters, stimulus, color_to_text)
            return response

        case _:
            print('response_type not handled')
            return

def launch_trial(win, parameters, clock, stimuli, exp, participant_id, color_to_text=None):
    draw_fixation_cross(win, how_long=0.5)

    for stimulus in stimuli:
        draw_recall_stim(win, stimulus, parameters, color_to_text)
        if parameters['recall_stim_type'] is not None:
            draw_empty_screen(win, how_long=0.5)

    for i in range(parameters["nb_parity"]):
        draw_empty_screen(win, how_long=0.5)
        draw_parity_task(win, clock, exp, i)
        draw_empty_screen(win, how_long=0.5)

    if parameters['recall_stim_type'] is not None:
        draw_empty_screen(win, how_long=parameters['maintenance_time'])

    for i, stimulus in enumerate(stimuli):
        response = get_participant_response(win, parameters, stimulus, color_to_text)

        draw_empty_screen(win, how_long=0.1)
        save_trial_and_next(exp, clock, response, stimulus, i)
