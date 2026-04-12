# crossword_solver/README.txt

CROSSWORD SOLVER

Projet :
Ce programme résout une grille de mots croisés en Python, uniquement dans le terminal.

Structure du projet :
crossword_solver/
├── src/
│   ├── main.py
│   ├── loader.py
│   ├── slot.py
│   └── solver.py
├── data/
│   ├── grid1.txt
│   ├── dict1.txt
│   ├── grid2.txt
│   ├── dict2.txt
│   ├── grid3.txt
│   └── dict3.txt
└── README.txt

Format des fichiers de grille :
- '_' : case blanche
- '#' : case noire

Exemple :
__##
_#_#
___#
#___

Format des fichiers dictionnaire :
- un mot par ligne
- uniquement des lettres
- pas d'espaces
- pas de chiffres

Exemple :
an
in
art
tin
one
net

Principe de résolution :
Le programme :
1. lit la grille et le dictionnaire
2. détecte les emplacements horizontaux et verticaux
3. associe à chaque emplacement les mots de même longueur
4. vérifie les contraintes de croisement
5. cherche une solution par retour arrière (backtracking)

Idée algorithmique :
- chaque emplacement est une variable
- son domaine est l'ensemble des mots candidats
- une contrainte relie deux emplacements qui se croisent
- deux mots sont compatibles si leurs lettres coïncident à l'intersection

Lancement du programme :
Depuis le dossier crossword_solver :

python src/main.py

Le programme demande ensuite :
- le nom du fichier grille
- le nom du fichier dictionnaire

Si on appuie simplement sur Entrée, les fichiers par défaut sont :
- grid1.txt
- dict1.txt

Exemples de tests :
1. grid1.txt + dict1.txt
   Cas avec solution

2. grid2.txt + dict2.txt
   Cas avec solution comme dans l'énoncé 

3. grid3.txt + dict3.txt
   Cas un peu plus grand

Messages possibles :
- "Aucune solution possible : au moins un emplacement n'a aucun candidat."
  => impossible à cause des longueurs disponibles

- "Aucune solution trouvee : les croisements rendent cette instance impossible."
  => chaque emplacement a des candidats, mais aucune combinaison ne respecte toutes les contraintes

Statistiques affichées :
- nombre d'appels récursifs
- nombre d'essais de placement
- nombre de retours arrière

Limites :
- le programme utilise un dictionnaire fixe
- chaque mot du dictionnaire ne peut être utilisé qu'une seule fois
- l'affichage est uniquement textuel dans le terminal
