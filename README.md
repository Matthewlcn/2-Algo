# Crossword Solver

Projet de 2ALGO - résolution d'une grille de mots croisés en Python.

Le programme peut être lancé en mode terminal ou via une interface graphique Tkinter.

## Auteurs

- Kadvael Caudal
- Matthew Li-Ching-Ng
- Joachim Collot

## Prérequis

- Python 3.8 ou plus
- Tkinter (normalement inclus avec Python, sinon `sudo apt install python3-tk` sous Linux)

Aucune bibliothèque externe n'est nécessaire.

## Structure du projet

```
crossword_solver/
├── src/
│   ├── main.py       # point d'entrée terminal
│   ├── gui.py        # interface graphique (bonus)
│   ├── loader.py     # chargement grille + dictionnaire
│   ├── slot.py       # détection des emplacements
│   └── solver.py     # résolution par backtracking
├── data/
│   ├── grid1.txt
│   ├── dict1.txt
│   ├── grid2.txt
│   ├── dict2.txt
│   ├── grid3.txt
│   └── dict3.txt
└── README.md
```

## Format des fichiers

### Grille

- `_` : case blanche
- `#` : case noire

Exemple :

```
__##
_#_#
___#
#___
```

### Dictionnaire

- un mot par ligne
- uniquement des lettres
- pas d'espaces ni de chiffres

Exemple :

```
an
in
art
tin
one
net
```

## Principe de résolution

Le programme :

1. lit la grille et le dictionnaire
2. détecte les emplacements horizontaux et verticaux
3. associe à chaque emplacement les mots de même longueur
4. vérifie les contraintes de croisement
5. cherche une solution par retour arrière (backtracking)

### Idée algorithmique

- chaque emplacement est une variable
- son domaine est l'ensemble des mots candidats
- une contrainte relie deux emplacements qui se croisent
- deux mots sont compatibles si leurs lettres coïncident à l'intersection

## Utilisation

### Mode terminal

Depuis le dossier `crossword_solver` :

```
python src/main.py
```

Le programme demande ensuite :
- le nom du fichier grille
- le nom du fichier dictionnaire

Si on appuie simplement sur Entrée, les fichiers par défaut sont utilisés :
- `grid1.txt`
- `dict1.txt`

### Mode graphique (bonus)

Depuis le dossier `crossword_solver` :

```
python src/gui.py
```

La fenêtre Tkinter permet de :
- choisir un fichier de grille et un fichier de dictionnaire (boutons "Parcourir")
- afficher la grille vide (cases blanches / cases noires)
- lancer la résolution et afficher la grille remplie
- consulter la liste des mots placés et les statistiques du solveur

## Exemples de tests


grid1.txt + dict1.txt       cas simple avec solution
grid2.txt + dict2.txt       cas de l'énoncé
grid3.txt + dict3.txt       cas un peu plus grand

## Messages possibles

- **"Aucune solution possible : au moins un emplacement n'a aucun candidat."**
  → impossible à cause des longueurs disponibles dans le dictionnaire.

- **"Aucune solution trouvee : les croisements rendent cette instance impossible."**
  → chaque emplacement a bien des candidats, mais aucune combinaison ne respecte toutes les contraintes de croisement.

## Statistiques affichées

Après résolution, le programme affiche :

- le nombre d'appels récursifs
- le nombre d'essais de placement
- le nombre de retours arrière

Ces valeurs permettent de comparer la difficulté des différentes grilles.

## Limites

- le programme utilise un dictionnaire fixe (pas de génération automatique)
- chaque mot du dictionnaire ne peut être utilisé qu'une seule fois dans une grille
- l'affichage terminal (`main.py`) reste purement textuel ; la GUI (`gui.py`) fournit la visualisation graphique du bonus