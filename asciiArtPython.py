"""
Cette bibliothèque comprend les fonctions suivantes :
    - depuis_image  : Convertit une image en art ASCII.
    - vers_image : Convertit de l'art ASCII en image.
    - vers_texte : Convertit de l'art ASCII en fichier texte brut.
    - vers_terminal : Affiche de l'art ASCII dans le terminal.
"""
# Importation des bibliothèques nécessaires
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
from tqdm import tqdm
import cv2

# Vérification de la présence du fichier de police FUTRFW.TTF
assert os.path.isfile("FUTRFW.TTF"), "Le fichier de police FUTRFW.TTF est manquant. Veuillez le télécharger depuis https://github.com/pprriieeuurr/ascii-art et le placer dans le même répertoire que ce script."
if not os.path.exists("data"):
    os.mkdir("data")

# Fonction pour les vidéos
def vidéo_vers_images(source:str, fps_max:int=10, taille_frame_maxi:int=7000, noms_images:str="frame")->list:
    """
    Convertit une vidéo en une série d'images.

    Paramètres
    ----------
    source : str
        Chemin vers le fichier vidéo à convertir.
    fps_max : int, optionnel
        Nombre maximum d'images par seconde (par défaut 10).
    taille_frame_maxi : int, optionnel
        Taille maximale de chaque frame en pixels (par défaut 7000).

    Retourne
    --------
    list
        Liste des chemins d'accès aux images extraites de la vidéo.
    """
    # Exportation des frames de la vidéo en images
    vidcap = cv2.VideoCapture(source)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_interval = fps // fps_max if fps > fps_max else 1
    success, image = vidcap.read()
    count = 0
    frame_count = 0
    while success:
        if frame_count % frame_interval == 0:
            cv2.imwrite(f"./data/{noms_images+str(count)}.png", image)
            count = count+1
        success, image = vidcap.read()
        frame_count=frame_count+1
    TMP=vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    vidcap.release()

    return count,round(TMP/fps)
def images_vers_vidéo(liste_paths:list, fps:int, nom_fichier:str)->None:
    """
    Convertit une liste d'images en une vidéo.

    Paramètres
    ----------
    liste_paths : list
        Liste des chemins d'accès aux images à convertir en vidéo.
    fps : int
        Nombre d'images par seconde pour la vidéo.
    nom_fichier : str
        Nom du fichier de sortie pour la vidéo (avec extension, par exemple "output.avi
    
    Ne retourne rien.
    """
    frame = cv2.imread(liste_paths[0])
    height, width, layers = frame.shape
    size = (width, height)
    out = cv2.VideoWriter(nom_fichier, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for image in tqdm(liste_paths):
        img = cv2.imread(image)
        out.write(img)
    out.release()

# Classes de l'art ASCII
class AsciiArtImage:
    """
    Classe pour manipuler l'art ASCII.

    Attributs
    ---------
    self.grille : list
        Liste de caractères utilisés pour représenter les niveaux de gris.
    self.image : PIL.Image
        Image chargée à partir du fichier source.
    self.ascii : list
        Liste de chaînes de caractères représentant les lignes de l'art ASCII.

    Méthodes
    --------
    __init__ :
        Constructeur de la classe AsciiArtImage, initialise l'art ASCII à partir d'une image.
    __str__ :
        Retourne une représentation en chaîne de caractères de l'art ASCII.
    export :
        Exporte l'art ASCII dans un fichier texte ou une image.
    """
    def __init__(self,source:str,taille_maxi:int=10000)->None:
        """
        Initialise une instance de la classe AsciiArt à partir d'un fichier image.

        Paramètres
        ----------
        source : str
            Chemin vers le fichier image à convertir en art ASCII.
        taille_maxi : int, optionnel
            Taille maximale de l'image en pixels (par défaut 10000).
        """
        self.grille = ["#","@","&","$","{","(","=","*",";",":","."," "]
        self.image = Image.open(source).convert("L")
        if self.image.size[0] * self.image.size[1] > taille_maxi:
            self.image = self.image.resize((int(self.image.size[0] * (taille_maxi / (self.image.size[0] * self.image.size[1]))**0.5),int(self.image.size[1] * (taille_maxi / (self.image.size[0] * self.image.size[1]))**0.5)))
        tab_np = np.asarray(self.image)
        self.ascii = []
        for ligne in tab_np:
            chaine = ""
            for valeur in ligne:
                chaine += self.grille[int(valeur/256*len(self.grille))]
            self.ascii.append(chaine)
    def __str__(self)->str:
        """
        Retourne une représentation en chaîne de caractère de l'art ASCII.
        """
        txt = ""
        for i in range(0, len(self.ascii), 2):
            txt += self.ascii[i] + "\n"
        return txt[:-1]
    def exporter(self, nom_fichier:str="mika_export", mode:str="img")->None:
        """
        Export l'art ASCII dans un fichier soit texte, soit image.

        Paramètres
        ----------
        nom_fichier : str
            Nom du fichier de sortie (sans extension).
        mode : str
            Mode d'exportation, soit "img" pour une image au format png, soit "txt" pour un fichier texte brut au format txt (par défaut "img").
        """
        if mode == "txt":
            with open(f"{nom_fichier}.txt", "w", encoding="utf-8") as f:
                f.write(str(self))
        elif mode == "img":
            font = ImageFont.truetype("FUTRFW.TTF", 20)
            largeur = max([len(ligne) for ligne in self.ascii]) * 20
            hauteur = len(self.ascii) * 20
            image = Image.new("L", (largeur, hauteur), color=255)
            draw = ImageDraw.Draw(image)
            for i, ligne in enumerate(self.ascii):
                draw.text((0, i * 20), ligne, fill=0, font=font)
            image.save(f"{nom_fichier}.png")

class AsciiArtVideo:
    """
    Classe pour manipuler l'art ASCII à partir d'une vidéo.
    """
    def __init__(self, source:str, fps_max:int=10, taille_frame_maxi:int=2000,nom:str="mika_frame"):
        """
        Initialise une instance de la classe AsciiArtVideo à partir d'un fichier vidéo.

        Paramètres
        ----------
        source : str
            Chemin vers le fichier vidéo à convertir en art ASCII.
        fps_max : int, optionnel
            Nombre maximum d'images par seconde (par défaut 10).
        taille_frame_maxi : int, optionnel
            Taille maximale de chaque frame en pixels (par défaut 7000).
        nom : str, optionnel
            Nom de base pour les images extraites de la vidéo (par défaut "mika_frame").
        """
        self.source = source
        self.nb_images, self.duree = vidéo_vers_images(source, fps_max, taille_frame_maxi, nom)
        self.images = [AsciiArtImage(f"./data/{nom}{i}.png") for i in tqdm(range(self.nb_images))]
    def exporter(self, nom_fichier:str="mika_video_export")->None:
        """
        Exporte l'art ASCII de chaque image de la vidéo dans un fichier image puis combine les images en une vidéo.
        """
        for i in tqdm(range(self.nb_images), desc="Exportation des images"):
            self.images[i].exporter(f"data/{nom_fichier}{i}")
        images_vers_vidéo([f"data/{nom_fichier}{i}.png" for i in range(self.nb_images)], self.nb_images/self.duree, f"{nom_fichier}.avi")
