# Importation des modules nécessaires
from asciiArtPython import AsciiArtImage
from time import sleep
import cv2
import sys
def capturer_webcam(cap):
    """
    Fonction pour capturer l'image de la webcam et la convertir en art ASCII.
    """
    # Initialisation de la capture vidéo
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la webcam.")
        return

    # Capture d'une image
    ret, frame = cap.read()
    if not ret:
        print("Erreur : Impossible de capturer une image.")
        return

    cv2.imwrite("data/capture_webcam.png", frame)
print("Bienvenue dans le programme d'art ASCII en direct !")
print("Ce programme convertit votre webcam en art ASCII en temps réel. Assurez-vous que votre webcam est connectée et fonctionnelle. Vous pouvez arrêter le programme à tout moment en appuyant sur 'ctrl+C'.")
input("Appuyez sur Entrée pour commencer...")
try:
    cap = cv2.VideoCapture(0)
    # Boucle pour afficher l'art ASCII en temps réel
    while True:
        capturer_webcam(cap)
        sys.stdout.write(str(AsciiArtImage("data/capture_webcam.png",15000)))
        sys.stdout.flush()
        sleep(0.1)  # Pause pour éviter une surcharge CPU
except KeyboardInterrupt:
    print("\nArrêt du programme.")