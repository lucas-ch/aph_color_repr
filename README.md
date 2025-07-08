# aph_color_repr

## Tâches psychopy
Dans ce repo, le script python est l'expérience eeg psychopy modifiée pour faire des tâches de comportement:
- tâche de correspondance (match): le participant perçoit la couleur, il la place sur la roue de couleur pendant la perception
- tâche de rappel (recall): le participant perçoit la couleur pendant 500ms, écran gris pendant 3s, puis place la couleur sur la roue
- tâche de traduction perception vers texte (describe): le participant perçoit la couleur et la décrit par écrit pendant la perception
- tâche de traduction texte vers perception (trad_text_to_color): le participant lis le texte précedemment décrit et place la couleur sur la roue pendant la lecture
- tâche de traduction perception vers spatial (trad_color_to_spatial): le participant perçoit la couleur et la place sur la roue grise pendant la perception

Si tu veux tester les tâches, tu peux changer nb_color. Attention, tu peux pas faire trad_text_to_color si tu n'as pas faire d'abord describe pour le même set de couleurs.

## hypothèses
- La tâche de correspondance mesure la qualité de la perception mais n'est pas très sensible: je m'attends à de bons résultats, peu de différences entre participants.
- La tâche de rappel est sensible (perso, je passe d'une erreur moyenne de 4° sur la correspondance à 12° sur le rappel): je m'attends à ce que les aphs fassent moins bien

Je vois 2 grandes stratégies possibles pour la tâche de rappel (y'en a sans doute d'autres, mais j'arrive pas à les imaginer):
- stocker en mémoire de travail l'info de perception (ou une information textuelle qui permet le rappel de la perception?)
- traduire la perception en donnée textuelle/spatiale (du genre vert-jaune ++) et stocker cette information en mémoire de travail

Pour tester la seconde stratégie (celle que je pense utiliser), j'ai fait la tâche dont on avait parlé: 
- décrire les perceptions textuellement, puis utiliser cette description pour retrouver la couleur 
- J'ai aussi fait une tâche où on perçoit la couleur et on doit la placer sur une roue qui ne contient plus que les données spatiales (roue grise).

Sur ces 2 tâches, j'arrive en gros à des performances similaires à la tâche de rappel, ce qui me conforte dans l'idée que j'utilise une stratégie de traduction de perception en donnée textuelle/spatiale.

Les résultats de mes dernières passations (donc après un entraînement) sont dans le script R.

## autre info
Pour mesurer la précision d'un rappel, la distance angulaire hsv, c'est peut être pas le plus approprié (on a en général une meilleure perception vers le jaune/orange que vers le violet). Peut être que ce genre de distance peut être utilisé: https://fr.wikipedia.org/wiki/L*u*v*_CIE_1976