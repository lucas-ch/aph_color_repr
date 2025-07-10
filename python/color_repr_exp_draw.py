from psychopy import visual, core, event, gui
import numpy as np
from color_repr_exp_utils import * 
from psychopy.event import Mouse, getKeys

def open_dialog(parameters):
    stim_type = get_stim_type_list()
    response_type = get_response_type_list()
    defaults = parameters["defaults"]

    dlg = gui.Dlg(title="Aphantasia EEG experiment")
    dlg.addField('participant_id', initial= defaults["participant_id"])

    dlg.addField('recall_stim_type', initial = defaults["recall_stim_type"], choices=stim_type)
    dlg.addField('response_type', initial = defaults["response_type"], choices=response_type)
    dlg.addField("match_stim_type", initial = defaults["match_stim_type"], choices=[None, "text", "color"])

    dlg.addField('nb_stim_total', initial = defaults["nb_stim_total"], choices = [3, 15, 45])
    dlg.addField('nb_stim_per_trial', initial=defaults["nb_stim_per_trial"], choices= [1, 3, 5])
    dlg.addField('nb_parity', initial = defaults["nb_parity"], choices=[0, 1, 2, 3])
    dlg.addField('fullscreen', initial = defaults["fullscreen"], choices=[False, True])
    dlg.addField('color_to_text_filename', initial = defaults["color_to_text_filename"])

    ok_data = dlg.show()

    if dlg.OK:
        return ok_data

def get_stim_type_list():
    return ['color', 'spatial', 'text', None]

def get_response_type_list():
    return ['wheel', 'squares', 'text']

def draw_match_stim(win, match_stim_type, stimulus, color_to_text):
    if match_stim_type is not None:
        if match_stim_type == "color":
            color_circle = visual.Circle(
                win,
                radius=50,
                fillColor=angle_to_color(stimulus),
                lineColor=None,
                pos=(0, 325))
            color_circle.draw()
        if match_stim_type == "text":
            text_top = visual.TextStim(
                win,
                text=color_to_text[stimulus],
                color='white',
                pos=(0, 325),
                height=32)
            text_top.draw()

def draw_text_recall_stim(win, stimulus, color_to_text):
    text = visual.TextStim(win, text=color_to_text[stimulus], height=50, color=(1, 1, 1))
    text.draw()
    win.flip()
    core.wait(1.5)

def draw_choose_color_rect(
        win,
        hues,
        stimulus,
        match_stim_type=None,
        color_to_text=None):
    grid_size = 6
    square_size = 80 
    spacing = 15

    positions = []
    for row in range(grid_size):
        for col in range(grid_size):
            x = row * (square_size + spacing) - 230
            y = col * (square_size + spacing) - 250
            positions.append((x, y))

    squares = []
    position_stimulus = None
    for i, hue in enumerate(hues):
        if hue == stimulus:
            position_stimulus = positions[i]

        color_rgb = angle_to_color(hue)
        square = visual.Rect(
                win,
                width=square_size,
                height=square_size,
                pos=positions[i],
                fillColor=color_rgb,
                lineColor=color_rgb
        )
        square.draw()
        squares.append(square)
    
    draw_match_stim(win, match_stim_type, stimulus, color_to_text)
    win.flip()

    while True:
        mouse = event.Mouse(win=win)
        if mouse.getPressed()[0]:
            draw_match_stim(win, match_stim_type, stimulus, color_to_text)

            for i, square in enumerate(squares):
                if square.contains(mouse):
                    color_rgb = angle_to_color(hues[i])
                    square = visual.Rect(
                        win,
                        width=square_size,
                        height=square_size,
                        pos=positions[i],
                        fillColor=color_rgb,
                        lineColor=color_rgb
                        )
                    square.draw()

                    color_rgb = angle_to_color(stimulus)
                    square = visual.Rect(
                        win,
                        width=square_size,
                        height=square_size,
                        pos=position_stimulus,
                        fillColor=color_rgb,
                        lineColor=color_rgb
                        )
                    square.draw()

                    win.flip()
                    core.wait(1)

                    return hues[i]

def draw_number(win, number, clock, how_long=1.0):
    text = visual.TextStim(win, text=f"{number}", height=50, color=(1, 1, 1))
    text.draw()
    win.flip()
    start_time = clock.getTime()
    keys = event.waitKeys(maxWait=how_long, keyList=['f', 'j'], timeStamped=clock)
    if keys is None:
        keys = [['None', clock.getTime()]]
    remaining_time = how_long - (clock.getTime() - start_time)
    if remaining_time > 0:
        core.wait(remaining_time)
    return keys[0]

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

def draw_circle(win, circle_size, color, how_long=0.250, pos = (0, 0)):
    circle = visual.Circle(win, radius=circle_size/2.0, fillColor=color, lineColor=None, pos=pos)
    circle.draw()
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

def _draw_cursor(
        win,
        outer_radius,
        angle,
        cursor,
        color_circle,
        mode="choice",
        hide=False):
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

def _draw_color_wheel(
        win,
        nb_segments,
        background_grey_circle,
        background_white_circle,
        donut_vertices,
        hide=False):
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
    
    if mode == 'stim_spatial':
        win.clearBuffer()
        _draw_color_wheel(
            win,
            nb_segments,
            background_grey_circle,
            background_white_circle,
            donut_vertices, hide=hide)

        _draw_cursor(win, outer_radius, real, cursor, color_circle, mode=mode, hide = hide)
        if response is not None:
            _draw_cursor(win, outer_radius, response, cursor, color_circle, hide=hide)

        _draw_center_square(win, center_square)
        win.flip()
        core.wait(how_long)

    if mode == 'choice':
        win.clearBuffer()

        _draw_color_wheel(
            win,
            nb_segments,
            background_grey_circle,
            background_white_circle,
            donut_vertices,
            hide=hide)

        _draw_cursor(win, outer_radius, angle, cursor, color_circle, hide=hide)
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
                if angle < 0:
                    angle = 360 + angle
                # Effacer l'écran et redessiner le donut, le curseur et le cercle de couleur
                win.clearBuffer()
                _draw_color_wheel(
                    win,
                    nb_segments,
                    background_grey_circle,
                    background_white_circle,
                    donut_vertices,
                    hide=hide)
                
                _draw_cursor(win, outer_radius, angle, cursor, color_circle, hide=hide)
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
        _draw_color_wheel(
            win,
            nb_segments,
            background_grey_circle,
            background_white_circle,
            donut_vertices,
            hide)

        if response is not None:
            _draw_cursor(win, outer_radius, response, cursor, color_circle)
        _draw_cursor(win, outer_radius, real, cursor, color_circle, mode=mode)
        _draw_center_square(win, center_square)
        win.flip()
        core.wait(how_long)
        
def draw_text_input(win, with_color, circle_color='red', circle_pos=(0, 150), circle_radius=50,
                               prompt_text="Décris la couleur :", max_chars=100):

    win.color = 'grey'

    # Eléments visuels
    if with_color:
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

        if with_color:
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

