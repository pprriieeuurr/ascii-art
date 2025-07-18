# Création d'Ascii Art
Ce projet que j'ai codé avec Python durant l'été 2024 permet de transformer une image, une vidéo ou même votre webcam en [Ascii Art](https://fr.wikipedia.org/wiki/Art_ASCII) (de type _Newskool_).
## Fonctionnement
Pour générer de tels résultats, le programme regarde le taux de blanc de chaque pixel de l'image séparément et choisit le caractère le mieux adapté, selon le tableau suivant :
| Valeur du blanc | Caractère choisi |
|-----------|-----------|
| 0 - 21 | # |
| 22 - 42 | @ |
| 43 - 63 | & |
| 64 - 85 | $ |
| 86 - 106 | { |
| 107 - 127 | ( |
| 128 - 148 | = |
| 149 - 170 | * |
| 171 - 191 | ; |
| 192 - 212 | : |
| 213 - 233 | . |
| 234 - 255 | _espace_ |

## Prérequis
Pour utiliser ce projet, il faut avoir Python et installer (via pip) les bibliothèques ci-dessous :
- tqdm
- numpy
- opencv-python
- pillow
## Installation et configuration
Pour installer et configurer le projet, il faut tout d'abord télécharger le code source de celui-ci.

Ensuite, il faut installer les dépendances dans Python 3 (celles-ci sont détaillées dans **requirements.txt** et ci-dessus).

Maintenant, plusieurs choix s'offrent à vous selon ce que vous voulez faire...
## Utilisation de la WebCam
Un exemple concret de ce que vous pouvez faire avec ce projet est d'afficher votre webcam dans une fenêtre de terminal. Pour ce faire, exécutez simplement le fichier **asciiArtLive.py** avec un pc qui possède une webcam, lisez et admirez.
## Utilisation de asciiArtPython en tant que bibliothèque
### Pour transformer une image
Dans un nouveau fichier Python, écrivez ce qui suit :
```python
# Importation du module
import asciiArtPython as aap

# Utilisation de la classe AsciiArtImage afin de créer et exporter un art ascii
img = aap.AsciiArtImage(input("Nom de l'image : "), 100_000)
img.exporter(mode="txt")

# Afficher l'image dans le terminal
print("Voici votre image :")
print(img)
```
### Pour transformer une vidéo
Dans un nouveau fichier Python, écrivez ce qui suit :
```python
# Importation du module
import asciiArtPython as aap

# Utilisation de la classe AsciiArtVideo afin de créer et exporter un art ascii
vid = aap.AsciiArtVideo(input("Nom de la vidéo : "))
vid.exporter()
```