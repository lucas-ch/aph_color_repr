from color_repr_exp_draw import *
from color_repr_exp_utils import *

def launch_trial(win, parameters, clock, stimulus, exp, participant_id, task):
    color_to_text = {}
    if task == "trad_text_to_color":
        file_name_describe = f"{parameters['data_path']}aphantasia_{participant_id}_describe"
        color_to_text = get_color_to_text_dict(file_name_describe)

    if bool(color_to_text): 
        globals()[task](win, parameters, clock, stimulus, exp, color_to_text=color_to_text)
    else:
        globals()[task](win, parameters, clock, stimulus, exp)

def recall_squares(win, parameters, clock, stimulus, exp):
    draw_fixation_cross(win, how_long=0.5)

    draw_circle(
        win,parameters["circle_size"],
        angle_to_color(stimulus, parameters["blue_only"]),
        how_long=1.0)

    draw_empty_screen(win, how_long=2)

    hues = generate_random_hues(stimulus)
    selected = draw_choose_color_rect(win,hues, stimulus)
        
    save_trial_and_next(exp, clock, selected, stimulus)

    draw_empty_screen(win, how_long=0.5)


def recall_parity(win, parameters, clock, stimulus, exp):
    parameters["nb_colors_recall_multi"] = 1
    stimulus = [stimulus]
    recall_multi(win, parameters, clock, stimulus, exp, parity = True)

def recall_simple(win, parameters, clock, stimulus, exp):
    parameters["nb_colors_recall_multi"] = 1
    stimulus = [stimulus]
    recall_multi(win, parameters, clock, stimulus, exp)

def recall_multi(win, parameters, clock, stimulus, exp, parity = False):
    nb_colors = parameters["nb_colors_recall_multi"]

    draw_fixation_cross(win, how_long=0.5)

    for i in range(nb_colors):
        draw_circle(
            win,
            parameters["circle_size"],
            angle_to_color(stimulus[i], parameters["blue_only"]),
            how_long=1.0)
        
        for j in range(parameters["nb_parity"]):
            draw_empty_screen(win, how_long=1.0)
            
            number = np.random.randint(1, 10)
            response = draw_number(win, number, clock, 1.5)
            save_trial_and_next(exp, clock, response[0], number, j)
            
            draw_empty_screen(win, how_long=1.0)

        draw_empty_screen(win, how_long=2.0)

    for i in range(nb_colors):
        selected = draw_color_wheel(
            win,
            parameters["inner_radius"],
            parameters["outer_radius"],
            mode='choice')
        
        draw_color_wheel(
            win,
            parameters["inner_radius"],
            parameters["outer_radius"],
            mode='feedback',
            how_long=0.5,
            response=selected,
            real=stimulus[i])

        save_trial_and_next(exp, clock, selected, stimulus[i], i)

def recall_spatial(win, parameters, clock, stimulus, exp):
    draw_fixation_cross(win, how_long=0.5)
    draw_color_wheel(
        win,
        parameters["inner_radius"],
        parameters["outer_radius"],
        mode='stim_spatial',
        hide = True,
        how_long=1.0,
        real=stimulus)

    draw_empty_screen(win, how_long=2.0)

    selected = draw_color_wheel(
        win,
        parameters["inner_radius"],
        parameters["outer_radius"],
        mode='choice',
        hide = True)
    
    draw_color_wheel(
        win,
        parameters["inner_radius"],
        parameters["outer_radius"],
        mode='stim_spatial',
        hide = True,
        how_long=0.5,
        response=selected,
        real=stimulus)

    save_trial_and_next(exp, clock, selected, stimulus, position = 0)

def match(win, parameters, clock, stimulus, exp, hide=False):
    draw_fixation_cross(win, how_long=0.5)

    selected = draw_color_wheel(
        win,
        parameters["inner_radius"],
        parameters["outer_radius"],
        mode='choice',
        center_circle_color_angle=stimulus,
        hide=hide)
    
    draw_color_wheel(
        win,
        parameters["inner_radius"],
        parameters["outer_radius"],
        mode='feedback',
        how_long=0.5,
        response=selected,
        real=stimulus,
        hide=hide)

    save_trial_and_next(exp, clock, selected, stimulus, position = 0)

def trad_color_to_spatial(clock, stimulus, exp):
    match(clock, stimulus, exp, hide=True)
    
def describe(win, parameters, clock, stimulus, exp):
    draw_fixation_cross(win, how_long=0.5)
    color = angle_to_color(stimulus, parameters["blue_only"])
    
    response = draw_color_with_text_input(win, circle_color=color)
    
    save_trial_and_next(exp, clock, response, stimulus, position = 0)

def trad_text_to_color(win, parameters, clock, stimulus, exp, color_to_text=None):
    draw_fixation_cross(win, how_long=0.5)

    selected = draw_color_wheel(
        win,
        parameters["inner_radius"],
        parameters["outer_radius"],
        mode='choice',
        top_text=color_to_text[stimulus])
    
    draw_color_wheel(
        win,
        parameters["inner_radius"],
        parameters["outer_radius"],
        mode='feedback',
        how_long=0.5,
        response=selected,
        real=stimulus)

    save_trial_and_next(exp, clock, selected, stimulus, position = 0)
