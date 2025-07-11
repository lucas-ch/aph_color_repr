# aph_color_repr

## Tâches psychopy
Dans ce repo, le script python main.py est l'expérience eeg psychopy modifiée pour faire des tâches de comportement flexibles:
Des tâches de recall ou match avec les stimulus suivants:
- color: un rond de couleur
- text: chaine de character correspodant à une couleur
- wheelGrey: un cercle gris marqué d'un emplacement (angle)

A ces stimuli, le participant doit répondre:
- wheel: sélectionner un angle/couleur sur la roue des couleurs
- wheelGrey: sélectionner un angle sur un cercle gris
- squares: sélectionner un carré coloré parmi une grille de couleurs
- text: taper un texte

Par exemple, la tâche la plus courante est d'avoir comme stimulus un rond de couleur que le participant doit placer sur la roue de couleurs par la suite.

Ces tâches peuvent être rendus plus ou moins difficiles par des paramètres dans le fichier parameters.json ou dans la boite de dialogue au lancement du script main.py: longueur de la période entre stimulus et rappel, tâche de parité parasite, nombre de stimuli, nombre de stimuli par trial...

Attention, text peut être séléctionné comme stimulus seulement si le participant à déjà associé un texte aux couleurs lors d'une tâche de rappel color/text auparavant.

## hypothèses
- La tâche de correspondance (match color/wheel ou match color/squares) mesure la qualité de la perception mais n'est pas très sensible: je m'attends à de bons résultats, peu de différences entre participants.
- La tâche de rappel (recall color/wheel) est sensible (perso, je passe d'une erreur moyenne de 4° sur la correspondance à 12° sur le rappel): je m'attends à ce que les aphs fassent moins bien

Je vois 2 grandes stratégies possibles pour les tâches de rappel (y'en a sans doute d'autres, mais j'arrive pas à les imaginer):
- stocker en mémoire de travail l'info de perception (ou une information textuelle qui permet le rappel de la perception?)
- traduire la perception en donnée textuelle/spatiale (du genre vert-jaune ++) et stocker cette information en mémoire de travail

Pour tester la seconde stratégie (celle que je pense utiliser), j'ai fait la tâche dont on avait parlé: 
- décrire les perceptions textuellement, puis utiliser cette description pour retrouver la couleur 
- J'ai aussi fait une tâche où on perçoit la couleur et on doit la placer sur une roue qui ne contient plus que les données spatiales (roue grise).

Sur ces 2 tâches, j'arrive en gros à des performances similaires à la tâche de rappel, ce qui me conforte dans l'idée que j'utilise une stratégie de traduction de perception en donnée textuelle/spatiale.

Les résultats de mes passations sont dans le script R.

## autre info
Pour mesurer la précision d'un rappel, la distance angulaire hsv, c'est peut être pas le plus approprié (on a en général une meilleure perception vers le jaune/orange que vers le violet). Peut être que ce genre de distance peut être utilisé: https://fr.wikipedia.org/wiki/L*u*v*_CIE_1976