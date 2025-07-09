from color_repr_exp_draw import draw_color_wheel, draw_fixation_cross, draw_empty_screen, draw_circle_square, draw_color_with_text_input
from color_repr_exp_utils import angle_to_color
import numpy as np

def get_stimuli(parameters, task):
    nb_colors_total = parameters["nb_colors"]
    nb_colors_per_stim = parameters["nb_colors_recall_hard"]

    stimuli = np.arange(0, 360, 360/nb_colors_total)
    np.random.shuffle(stimuli)

    if task == "recall_hard":
        nb_stim = int(len(stimuli)/nb_colors_per_stim)
        stim_list = []

        begin = 0
        end = begin + nb_colors_per_stim
        for i in range(nb_stim):
            stim_list.append(stimuli[begin:end])
            begin = begin + nb_colors_per_stim
            end = end + nb_colors_per_stim
        
        return stim_list
    else:
        return stimuli

def exp_recall(win, parameters, clock, stimulus, exp):
    draw_fixation_cross(win, how_long=0.5)
    draw_circle_square(
        win,
        parameters["square_size"],
        angle_to_color(stimulus, parameters["blue_only"]),
        how_long=1.0)
    draw_empty_screen(win, how_long=2.0)

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
        real=stimulus)

    exp.addData("onset", clock.getTime())
    exp.addData("selected", selected)
    exp.addData("color_angle", stimulus)

    exp.nextEntry()


def exp_recall_hard(win, parameters, clock, stimulus, exp):
    nb_colors = parameters["nb_colors_recall_hard"]

    draw_fixation_cross(win, how_long=0.5)

    for i in range(nb_colors):
        draw_circle_square(
            win,
            parameters["square_size"],
            angle_to_color(stimulus[i], parameters["blue_only"]),
            how_long=1.0)
        draw_empty_screen(win, how_long=1.0)

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

        exp.addData("onset", clock.getTime())
        exp.addData("selected", selected)
        exp.addData("color_angle", stimulus[i])

        exp.nextEntry()

def exp_recall_spatial(win, parameters, clock, stimulus, exp):
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

    exp.addData("onset", clock.getTime())
    exp.addData("selected", selected)
    exp.addData("color_angle", stimulus)

    exp.nextEntry()

def exp_match(win, parameters, clock, stimulus, exp, hide=False):
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

    exp.addData("onset", clock.getTime())
    exp.addData("selected", selected)
    exp.addData("color_angle", stimulus)

    exp.nextEntry()

def exp_trad_color_to_spatial(clock, stimulus, exp):
    exp_match(clock, stimulus, exp, hide=True)
    
def exp_describe(win, parameters, clock, stimulus, exp):
    draw_fixation_cross(win, how_long=0.5)
    color = angle_to_color(stimulus, parameters["blue_only"])
    
    response = draw_color_with_text_input(win, circle_color=color)

    exp.addData("onset", clock.getTime())
    exp.addData("text", response)
    exp.addData("color_angle", stimulus)

    exp.nextEntry()


def exp_trad_text_to_color(win, parameters, clock, stimulus, exp, color_to_text=None):
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

    exp.addData("onset", clock.getTime())
    exp.addData("color_angle", stimulus)
    exp.addData("selected", selected)

    exp.nextEntry()

