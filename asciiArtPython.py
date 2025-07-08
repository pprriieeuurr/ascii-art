"""
Cette bibliothèque comprend les fonctions suivantes :
    - depuis_image  : Convertit une image en art ASCII.
    - vers_image : Convertit de l'art ASCII en image.
    - vers_texte : Convertit de l'art ASCII en fichier texte brut.
    - vers_terminal : Affiche de l'art ASCII dans le terminal.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
from tqdm import tqdm

class AsciiArt:
    """
    Classe pour manipuler l'art ASCII.

    Attributs
    ---------

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
            self.image.resize((int(self.image.size[0] * (taille_maxi / (self.image.size[0] * self.image.size[1]))**0.5),
                               int(self.image.size[1] * (taille_maxi / (self.image.size[0] * self.image.size[1]))**0.5)))
        
        tab_np = np.asarray(self.image)
        self.ascii = []
        for lignes in tqdm(tab_np,"Création de l'ascii art. "):
            chaine = ""
            for valeur in lignes:
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
    def export(self, nom_fichier:str="mika_export", mode:str="img")->None:
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
AsciiArt("mika.png").export()