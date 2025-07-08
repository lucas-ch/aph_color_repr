import json
import serial
import numpy as np
import csv

from psychopy import visual, core, event, gui, data
from psychopy.tools.colorspacetools import hsv2rgb
from psychopy.tools.filetools import fromFile

# FUNCTIONS
# ---------
# générer un angle aléatoire entre 0 et 180
def random_angle():
    return np.random.randint(0, 180)

# générer un nombre aléatoire entre 1 inclu et 9 inclu
def random_number():
    return np.random.randint(1, 10)

def angle_to_color(angle):
    hsv_color = [angle, 0.5, 1.0]
    return hsv2rgb(hsv_color)

def get_donut_vertices(nb_segments, outer_radius, inner_radius):
    vertices = list()
    for angle in range(nb_segments):
        start_angle = np.deg2rad(angle)
        end_angle = np.deg2rad(angle + 1)
        vertices.append([inner_radius * np.cos(start_angle),
            inner_radius * np.sin(start_angle)])
        vertices.append([outer_radius * np.cos(start_angle),
            outer_radius * np.sin(start_angle)])
        vertices.append([outer_radius * np.cos(end_angle),
            outer_radius * np.sin(end_angle)])
        vertices.append([inner_radius * np.cos(end_angle),
            inner_radius * np.sin(end_angle)])
    return vertices

def draw_circle_square(win, square_size, color, how_long=0.250, pos = (0, 0)):
    square = visual.Circle(win, radius=square_size/2.0, fillColor=color, lineColor=None, pos=pos)
    square.draw()
    win.flip()
    core.wait(how_long)

def draw_fixation_cross(win, how_long=0.250):
    fixation = visual.TextStim(win, text='+', height=50, color=(1, 1, 1))
    fixation.draw()
    win.flip()
    core.wait(how_long)

def draw_empty_screen(win, how_long=0.250):
    win.flip()
    core.wait(how_long)

def _draw_cursor(win, angle, cursor, color_circle, mode="choice", hide=False):
    selected_color = angle_to_color(angle)
    if hide:
        selected_color = 'grey'
    cursor.ori = 360 - angle
    # Positionner le cercle de couleur au bout du curseur (1% au-dessus du donut)
    cursor_end_x = (outer_radius + 40) * np.cos(np.deg2rad(angle))
    cursor_end_y = (outer_radius + 40) * np.sin(np.deg2rad(angle))
    color_circle.pos = (cursor_end_x, cursor_end_y)
    color_circle.fillColor = selected_color
    if mode=='feedback':
        color_circle.lineColor = 'darkgrey'
        cursor.lineColor = 'darkgrey'
    cursor.draw()
    color_circle.draw()

def _draw_color_wheel(win, background_grey_circle, background_white_circle, donut_vertices, hide=False):
    background_white_circle.draw()
    background_grey_circle.draw()
    
    for angle in range(nb_segments):
        color = angle_to_color(angle)
        if hide:
            color = 'grey'
        segment = visual.ShapeStim(
            win, vertices=donut_vertices[angle*4:(angle+1)*4],
            fillColor=color, lineWidth=0, interpolate=True
        )
        segment.draw()

def _draw_center_square(win, center_square):
    center_square.draw()

def draw_color_wheel(
        win,
        inner_radius,
        outer_radius,
        nb_segments=360,
        mode='choice',
        how_long=5.0,
        real=None,
        response=None,
        center_circle_color_angle=None,
        top_text=None,
        hide = False):
    donut_vertices = get_donut_vertices(nb_segments, outer_radius, inner_radius)

    cursor = visual.Line(win, start=(inner_radius, 0), end=(outer_radius + 40, 0), lineColor='darkgrey', lineWidth=4)
    color_circle = visual.Circle(win, radius=20, fillColor='darkgrey', lineColor='darkgrey', lineWidth=4)

    # simulate wheel white border
    background_white_circle = visual.Circle(win, radius=outer_radius + 2, fillColor='darkgrey', lineColor='darkgrey')
    background_grey_circle = visual.Circle(win, radius=inner_radius - 2, fillColor='grey', lineColor='grey')

    # Carré gris cliquable au centre
    center_circle_color = 'grey'
    if center_circle_color_angle is not None:
        center_circle_color = angle_to_color(center_circle_color_angle)
    
    center_square = visual.Circle(win, radius=50, fillColor= center_circle_color, lineColor='darkgrey')

    angle = random_angle()

    if mode == 'choice':
        win.clearBuffer()

        _draw_color_wheel(win, background_grey_circle,
            background_white_circle, donut_vertices, hide=hide)
        _draw_cursor(win, angle, cursor, color_circle, hide=hide)
        _draw_center_square(win, center_square)
        
        # Ajoute le texte au-dessus si demandé
        if top_text is not None:
            if len(top_text) > 100:
                top_text = top_text[:100]  # Limiter à 100 caractères
            text_stim = visual.TextStim(win, text=top_text, color='white', height=24,
                                        pos=(0, outer_radius + 130), wrapWidth=1000)
            text_stim.draw()

        win.flip()

        while True:

            # Détecter les clics de souris
            mouse = event.Mouse(win=win)
            if mouse.getPressed()[0]:
                x, y = mouse.getPos()
                angle = np.rad2deg(np.arctan2(y, x))
                # Effacer l'écran et redessiner le donut, le curseur et le cercle de couleur
                win.clearBuffer()
                _draw_color_wheel(win, background_grey_circle,
                    background_white_circle, donut_vertices, hide=hide)
                _draw_cursor(win, angle, cursor, color_circle, hide=hide)
                _draw_center_square(win, center_square)
                                    
                if top_text is not None:
                    text_stim.draw()

                win.flip()

            if mouse.isPressedIn(center_square):
                return None

            if event.getKeys(keyList=['space']):
                return angle

    elif mode == 'feedback':
        # Dessiner le donut, le curseur et le cercle de couleur
        win.clearBuffer()
        _draw_color_wheel(win, background_grey_circle,
            background_white_circle, donut_vertices, hide)
        if response is not None:
            _draw_cursor(win, response, cursor, color_circle)
        _draw_cursor(win, real, cursor, color_circle, mode=mode)
        _draw_center_square(win, center_square)
        win.flip()
        core.wait(how_long)

def load_parameters(file_path):
    with open(file_path, 'r') as f:
        parameters = json.load(f)

    nb_rows = parameters['nb_rows']
    nb_cols = parameters['nb_cols']
    small_square_size = parameters['small_square_size']
    square_size = nb_rows * small_square_size
    gabor_size = parameters['gabor_size']

    nb_segments = parameters['nb_segments']
    outer_radius = parameters['outer_radius']
    inner_radius = parameters['inner_radius']

    big_circle_radius = parameters['big_circle_radius']
    small_circle_radius = parameters['small_circle_radius']

    send_triggers = parameters['send_triggers']
    triggers = parameters['triggers']
    serial_port = parameters['serial_port']

    test = parameters['test']

    return (nb_rows, nb_cols, small_square_size, square_size, gabor_size,
            nb_segments, outer_radius, inner_radius,
            big_circle_radius, small_circle_radius,
            send_triggers, triggers, serial_port, test)
            
def draw_color_with_text_input(win, circle_color='red', circle_pos=(0, 150), circle_radius=50,
                               prompt_text="Décris la couleur :", max_chars=100):

    win.color = 'grey'

    # Eléments visuels
    color_circle = visual.Circle(win, radius=circle_radius, fillColor=circle_color, lineColor=None, pos=circle_pos)
    prompt = visual.TextStim(win, text=prompt_text, color='white', pos=(0, 60), height=24)

    # Texte saisi et curseur
    typed_text = ''
    text_y = -100
    text_stim = visual.TextStim(win, text='', color='white', pos=(0, text_y), height=32)
    cursor = visual.TextStim(win, text='|', color='white', pos=(0, text_y), height=32)

    cursor_visible = True
    last_blink_time = core.getTime()
    blink_interval = 0.5  # secondes

    # Mapping accents clavier AZERTY
    key_map = {
        '2': 'é', '7': 'è', '9': 'ç', '0': 'à', "'": 'ù',
        '`': 'è', 'space': ' ',
    }

    while True:
        # MAJ curseur clignotant
        now = core.getTime()
        if now - last_blink_time >= blink_interval:
            cursor_visible = not cursor_visible
            last_blink_time = now

        # Mise à jour texte
        text_stim.setText(typed_text)

        # Dessin
        win.clearBuffer()
        color_circle.draw()
        prompt.draw()
        text_stim.draw()

        if cursor_visible:
            cursor_x = text_stim.pos[0] + text_stim.boundingBox[0]/2 + 5
            cursor.setPos((cursor_x, text_y))
            cursor.draw()

        win.flip()

        # Attendre un petit moment pour laisser le temps à l'utilisateur
        core.wait(0.05)

        # Récupération des touches
        keys = event.getKeys()

        for key in keys:
            if key in ['return', 'num_enter']:
                return typed_text.strip()
            elif key == 'backspace':
                typed_text = typed_text[:-1]
            elif key == 'escape':
                core.quit()
            elif key in key_map:
                if len(typed_text) < max_chars:
                    typed_text += key_map[key]
            elif len(key) == 1:
                if len(typed_text) < max_chars:
                    typed_text += key

def exp_match(clock, stimulus, exp, hide=False):
    draw_fixation_cross(win, how_long=0.5)

    selected = draw_color_wheel(win, inner_radius, outer_radius, mode='choice', center_circle_color_angle=stimulus, hide=hide)
    draw_color_wheel(win, inner_radius, outer_radius, mode='feedback', how_long=0.5, response=selected, real=stimulus, hide=hide)

    exp.addData("onset", clock.getTime())
    exp.addData("selected", selected)
    exp.addData("color_angle", stimulus)

    exp.nextEntry()

def exp_trad_color_to_spatial(clock, stimulus, exp):
    exp_match(clock, stimulus, exp, hide=True)
    
def exp_recall(clock, stimulus, exp):
    draw_fixation_cross(win, how_long=0.5)
    draw_circle_square(win, square_size, angle_to_color(stimulus), how_long=1.0)
    draw_empty_screen(win, how_long=2.0)

    selected = draw_color_wheel(win, inner_radius, outer_radius, mode='choice')
    draw_color_wheel(win, inner_radius, outer_radius, mode='feedback', how_long=0.5, response=selected, real=stimulus)

    exp.addData("onset", clock.getTime())
    exp.addData("selected", selected)
    exp.addData("color_angle", stimulus)

    exp.nextEntry()

def exp_describe(clock, stimulus, exp):
    draw_fixation_cross(win, how_long=0.5)
    color = angle_to_color(stimulus)
    
    response = draw_color_with_text_input(win, circle_color=color)

    exp.addData("onset", clock.getTime())
    exp.addData("text", response)
    exp.addData("color_angle", stimulus)

    exp.nextEntry()


def exp_trad_text_to_color(clock, stimulus, exp, color_to_text=None):
    draw_fixation_cross(win, how_long=0.5)

    selected = draw_color_wheel(win, inner_radius, outer_radius, mode='choice', top_text=color_to_text[stimulus])
    draw_color_wheel(win, inner_radius, outer_radius, mode='feedback', how_long=0.5, response=selected, real=stimulus)

    exp.addData("onset", clock.getTime())
    exp.addData("color_angle", stimulus)
    exp.addData("selected", selected)

    exp.nextEntry()

# MAIN
# ----

# Load parameters
(nb_rows, nb_cols, small_square_size, square_size, gabor_size,
 nb_segments, outer_radius, inner_radius,
 big_circle_radius, small_circle_radius,
 send_triggers, triggers, serial_port, test) = load_parameters('parameters.json')

dlg = gui.Dlg(title="Aphantasia EEG experiment")
dlg.addField('Participant Id:', '')
dlg.addField('Task', choices=["match", "recall", "describe", "trad_text_to_color", "trad_color_to_spatial"])
ok_data = dlg.show()

fullscreen = not test
nb_color = 4

angle_size = 360/nb_color

if dlg.OK:
    clock = core.Clock()
    win = visual.Window([800, 800], color=(0, 0, 0), units='pix', fullscr=fullscreen)
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
                                 dataFileName=f"data/aphantasia_{ok_data['Participant Id:']}_{task}")
    
    color_to_text = {}
    if task == "trad_text_to_color":
        with open(f"{file_name_describe}.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                color = int(row['color_angle'])
                text = row['text']
                color_to_text[color] = text
    
    stimuli = np.arange(0, 360, angle_size)
    np.random.shuffle(stimuli)

    for stimulus in stimuli:
        if bool(color_to_text): 
            globals()[f"exp_{task}"](clock, stimulus, exp, color_to_text=color_to_text)
        else:
            globals()[f"exp_{task}"](clock, stimulus, exp)

    core.quit()
