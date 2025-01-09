"""
georges :
    verif du gagnant
    demande du nom py et tk
    debut du cheat gon
     
imam : 
    fonctionnement et affichage du score
bilal : 
    image score robot
    boucle des manches
    jointure entre les deux jeux
ibrahim : 
    regle du jeux
    cheat code tkinter
"""
#def pierrFeuilleCiseau():
import random
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
import os

# Liste des coups possibles
listeCoupPossible = {
    "pierre": "p",
    "feuille": "f",
    "ciseaux": "c"
}
# Fonction pour déterminer le gagnant
def gagnant(choixJ1, choixJ2):
    if choixJ1 == choixJ2:
        return "Égalité sur ce round"
    if choixJ1 == "gon":
        return "Personne ne peut battre Gon !"
    
    if choixJ1 == "p" and choixJ2 == "c":
        return "Joueur 1 gagne le round"
    elif choixJ1 == "p" and choixJ2 == "f":
        return "Joueur 2 gagne le round"
    elif choixJ1 == "f" and choixJ2 == "c":
        return "Joueur 2 gagne le round"
    elif choixJ1 == "f" and choixJ2 == "p":
        return "Joueur 1 gagne le round"
    elif choixJ1 == "c" and choixJ2 == "p":
        return "Joueur 2 gagne le round"
    elif choixJ1 == "c" and choixJ2 == "f":
        return "Joueur 1 gagne le round"

# Fonction pour afficher le GIF de victoire
def afficher_gif_victoire():
    # Création d'une nouvelle fenêtre pour afficher le GIF
    win = tk.Toplevel(root)
    win.title("Victoire !")
    win.geometry("300x300")  # Taille de la fenêtre

    # Chargement et affichage du GIF
    gif_image = Image.open(os.path.join(chemin_images, "gonPFC.gif"))
    gif_label = tk.Label(win)
    gif_label.pack()

    # Animation du GIF
    def update_gif(indice):
        frame = gif_image.seek(indice)
        photo = ImageTk.PhotoImage(gif_image)
        gif_label.config(image=photo)
        gif_label.image = photo  # Pour éviter que l'image soit supprimée par le garbage collector
        win.after(100, update_gif, (indice + 1) % gif_image.n_frames)

    update_gif(0)

# Fonction de mise à jour du jeu
def jouer(choixJ1):
    global scoreJoueur1, scoreBot, nombreDeManche
    choixJ2 = random.choice(list(listeCoupPossible.values()))

    # Mise à jour de l'image du choix du Joueur 1
    if choixJ1 == "p":
        choixJoueurImageLabel.config(image=pierreImage)
    elif choixJ1 == "f":
        choixJoueurImageLabel.config(image=feuilleImage)
    elif choixJ1 == "c":
        choixJoueurImageLabel.config(image=ciseauxImage)

    # Mise à jour de l'affichage de l'image correspondant au choix du bot
    if choixJ2 == "p":
        choixBotImageLabel.config(image=pierreImage)
    elif choixJ2 == "f":
        choixBotImageLabel.config(image=feuilleImage)
    elif choixJ2 == "c":
        choixBotImageLabel.config(image=ciseauxImage)

    resultat = gagnant(choixJ1, choixJ2)

    # Gérer le cas spécial pour "Gon"
    if nomJoueur.lower() == "gon":
        scoreJoueur1 = 5
        scoreBot = 0
        nombreDeManche = 1  # Affichage de 1 manche pour le message de victoire
        afficher_gif_victoire()  # Affiche le GIF de victoire
        return  # Sortir de la fonction pour éviter les mises à jour des scores
    
    # Mise à jour des scores
    if resultat == "Joueur 1 gagne le round":
        scoreJoueur1 += 1
    elif resultat == "Joueur 2 gagne le round":
        scoreBot += 1
    
    nombreDeManche += 1
    scoreJoueurLabel.config(text=f"{nomJoueur}: {scoreJoueur1}")  # Mise à jour du score du joueur
    scoreBotLabel.config(text="Bot: {}".format(scoreBot))  # Mise à jour du score du bot

    # Vérification si la partie est terminée
    if scoreJoueur1 + scoreBot == scoreMaxTotal:
        finDePartie()

# Fonction pour finir la partie
def finDePartie():
    if scoreJoueur1 > scoreBot:
        messagebox.showinfo("Fin de partie", f"Félicitations ! {nomJoueur} a gagné en {nombreDeManche} manches !")
    else:
        messagebox.showinfo("Fin de partie", f"Dommage ! L'ordinateur a gagné en {nombreDeManche} manches !")
    
    # Réinitialisation des scores et de la partie
    reset_game()

# Fonction pour réinitialiser le jeu
def reset_game():
    global scoreJoueur1, scoreBot, nombreDeManche
    scoreJoueur1 = 0
    scoreBot = 0
    nombreDeManche = 0
    scoreJoueurLabel.config(text=f"{nomJoueur}: 0")  # Réinitialiser le score du joueur
    scoreBotLabel.config(text="Bot: 0")  # Réinitialiser le score du bot
    choixJoueurImageLabel.config(image='')  # Réinitialiser l'image du choix
    choixBotImageLabel.config(image='')  # Réinitialiser l'image du choix du bot

    # Réafficher les boutons de choix si le nom n'est pas "Gon"
    if nomJoueur.lower() != "gon":
        pierreBtn.grid(row=1, column=0)
        feuilleBtn.grid(row=1, column=1)
        ciseauxBtn.grid(row=1, column=2)
    else:
        pierreBtn.grid(row=1, column=0)  # Afficher seulement le bouton Pierre
        feuilleBtn.grid_forget()  # Masquer le bouton Feuille
        ciseauxBtn.grid_forget()  # Masquer le bouton Ciseaux

# Initialisation des variables
scoreMaxTotal = 5
scoreJoueur1 = 0
scoreBot = 0
nombreDeManche = 0

# Demande de saisie du nom du joueur
nomJoueur = askstring("Nom du Joueur", "Entrez votre nom:")  # Saisir le nom du joueur
if nomJoueur is None or nomJoueur == "":
    nomJoueur = "Joueur 1"  # Nom par défaut si aucun nom n'est saisi

# Création de la fenêtre principale
root = tk.Tk()
root.title("Pierre Feuille Ciseaux")

# Chemin relatif vers le dossier images
chemin_images = os.path.join(os.path.dirname(__file__), "images")

# Fonction pour redimensionner les images PNG
def charger_image_png(chemin_image, largeur, hauteur):
    image = Image.open(chemin_image)  # Ouverture de l'image avec Pillow
    image = image.resize((largeur, hauteur), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)  # Conversion pour Tkinter

# Chargement et redimensionnement des images
pierreImage = charger_image_png(os.path.join(chemin_images, "pierre.png"), 100, 100)
feuilleImage = charger_image_png(os.path.join(chemin_images, "feuille.png"), 100, 100)
ciseauxImage = charger_image_png(os.path.join(chemin_images, "ciseaux.png"), 100, 100)

# Création des boutons de choix avec les images redimensionnées
pierreBtn = tk.Button(root, image=pierreImage, command=lambda: jouer("p"), width=100, height=100)
pierreBtn.grid(row=1, column=0, padx=10, pady=10)

feuilleBtn = tk.Button(root, image=feuilleImage, command=lambda: jouer("f"), width=100, height=100)
feuilleBtn.grid(row=1, column=1, padx=10, pady=10)

ciseauxBtn = tk.Button(root, image=ciseauxImage, command=lambda: jouer("c"), width=100, height=100)
ciseauxBtn.grid(row=1, column=2, padx=10, pady=10)

# Label pour VS
vs_label = tk.Label(root, text="VS", font=("Arial", 24), bg="yellow")
vs_label.grid(row=1, column=4, padx=10, pady=10)

# Ajout des boutons pour le Bot (sans commande)
pierreBotBtn = tk.Button(root, image=pierreImage, command=lambda: None, width=100, height=100)  # Sans action
pierreBotBtn.grid(row=1, column=5, padx=10, pady=10)

feuilleBotBtn = tk.Button(root, image=feuilleImage, command=lambda: None, width=100, height=100)  # Sans action
feuilleBotBtn.grid(row=1, column=6, padx=10, pady=10)

ciseauxBotBtn = tk.Button(root, image=ciseauxImage, command=lambda: None, width=100, height=100)  # Sans action
ciseauxBotBtn.grid(row=1, column=7, padx=10, pady=10)

# Labels pour afficher les choix du joueur et du bot
choixJoueurImageLabel = tk.Label(root)
choixJoueurImageLabel.grid(row=2, column=1, pady=10)  # Juste en dessous des boutons

choixBotImageLabel = tk.Label(root)
choixBotImageLabel.grid(row=2, column=6, pady=10)  # Juste en dessous du label du choix du bot

# Frame pour le score du Joueur 1
scoreJoueurFrame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
scoreJoueurFrame.grid(row=5, column=2, padx=10, pady=10)  # Positionne la frame dans la colonne 2
scoreJoueurLabel = tk.Label(scoreJoueurFrame, text=f"{nomJoueur}: {scoreJoueur1}", font=("Arial", 16))
scoreJoueurLabel.pack(padx=10, pady=10)

# Frame pour le score du Bot
scoreBotFrame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
scoreBotFrame.grid(row=5, column=5, padx=10, pady=10)  # Positionne la frame dans la colonne 5
scoreBotLabel = tk.Label(scoreBotFrame, text="Bot: {}".format(scoreBot), font=("Arial", 16))
scoreBotLabel.pack(padx=10, pady=10)

# Conserver les références des images pour éviter qu'elles ne soient supprimées
root.pierreImage = pierreImage
root.feuilleImage = feuilleImage
root.ciseauxImage = ciseauxImage

# Gérer l'affichage des boutons en fonction du nom du joueur
if nomJoueur.lower() == "gon":
    feuilleBtn.grid_forget()  # Masquer le bouton Feuille
    ciseauxBtn.grid_forget()  # Masquer le bouton Ciseaux

# Lancement de la boucle principale de Tkinter
root.mainloop()


