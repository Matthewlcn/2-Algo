import os
import tkinter as tk
from tkinter import filedialog, messagebox

from loader import load_dictionary, load_grid
from slot import find_slots
from solver import (
    build_slot_candidates,
    build_solution_grid,
    has_impossible_slot,
    solve_crossword,
)


# Taille d'une case en pixels
CELL_SIZE = 60
CANVAS_PADDING = 4


class CrosswordGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Crossword Solver - 2ALGO")

        # etat de la grille
        self.grid = None
        self.slots = None
        self.words = None
        self.solution_words = None
        self.solved_grid = None
        self.stats = None

        src_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(src_dir)
        self.data_dir = os.path.join(project_dir, "data")

        self._build_ui()

    # construction de l'interface

    def _build_ui(self):
        toolbar = tk.Frame(self.root, padx=12, pady=10)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # ligne 1 : chemin de la grille
        tk.Label(toolbar, text="Grille :", width=14, anchor="e").grid(row=0, column=0, sticky="e", pady=2)
        self.grid_path_var = tk.StringVar(value=os.path.join(self.data_dir, "grid1.txt"))
        tk.Entry(toolbar, textvariable=self.grid_path_var, width=48).grid(row=0, column=1, padx=6, pady=2)
        tk.Button(toolbar, text="Parcourir...", command=self._browse_grid).grid(row=0, column=2, padx=4, pady=2)

        # ligne 2 : chemin du dictionnaire
        tk.Label(toolbar, text="Dictionnaire :", width=14, anchor="e").grid(row=1, column=0, sticky="e", pady=2)
        self.dict_path_var = tk.StringVar(value=os.path.join(self.data_dir, "dict1.txt"))
        tk.Entry(toolbar, textvariable=self.dict_path_var, width=48).grid(row=1, column=1, padx=6, pady=2)
        tk.Button(toolbar, text="Parcourir...", command=self._browse_dict).grid(row=1, column=2, padx=4, pady=2)

        # boutons d'action
        actions = tk.Frame(toolbar)
        actions.grid(row=2, column=0, columnspan=3, pady=(8, 0), sticky="w")
        tk.Button(actions, text="Charger la grille", width=18, command=self._on_load).pack(side=tk.LEFT, padx=4)
        tk.Button(actions, text="Resoudre", width=14, command=self._on_solve).pack(side=tk.LEFT, padx=4)
        tk.Button(actions, text="Reinitialiser", width=14, command=self._on_reset).pack(side=tk.LEFT, padx=4)

        # zone principale : canvas a gauche, infos a droite
        body = tk.Frame(self.root, padx=12, pady=8)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(body, bg="#e8e8e8", width=300, height=300, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=(0, 12))

        side = tk.Frame(body)
        side.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(side, text="Mots places", font=("Arial", 11, "bold")).pack(anchor="w")
        self.words_list = tk.Listbox(side, height=12, width=32, font=("Courier", 10))
        self.words_list.pack(fill=tk.BOTH, expand=True, pady=(2, 8))

        tk.Label(side, text="Statistiques", font=("Arial", 11, "bold")).pack(anchor="w")
        self.stats_text = tk.Text(side, height=5, width=32, font=("Courier", 10), state=tk.DISABLED)
        self.stats_text.pack(fill=tk.X)

        # barre de statut en bas
        self.status_var = tk.StringVar(value="Chargez une grille pour commencer.")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
            relief=tk.SUNKEN,
            padx=6,
            pady=3,
        ).pack(side=tk.BOTTOM, fill=tk.X)

    # boites de dialogue pour choisir les fichiers

    def _browse_grid(self):
        path = filedialog.askopenfilename(
            title="Choisir un fichier de grille",
            initialdir=self.data_dir,
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
        )
        if path:
            self.grid_path_var.set(path)

    def _browse_dict(self):
        path = filedialog.askopenfilename(
            title="Choisir un fichier de dictionnaire",
            initialdir=self.data_dir,
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
        )
        if path:
            self.dict_path_var.set(path)

    # actions des boutons

    def _on_load(self):
        grid_path = self.grid_path_var.get().strip()
        if not grid_path:
            messagebox.showerror("Erreur", "Veuillez choisir un fichier de grille.")
            return

        try:
            self.grid = load_grid(grid_path)
            self.slots = find_slots(self.grid)
        except FileNotFoundError as e:
            messagebox.showerror("Fichier introuvable", str(e))
            return
        except ValueError as e:
            messagebox.showerror("Erreur de donnees", str(e))
            return

        self.solution_words = None
        self.solved_grid = None
        self.stats = None

        self._draw_grid()
        self._refresh_words_list()
        self._refresh_stats()

        rows = len(self.grid)
        cols = len(self.grid[0])
        self.status_var.set(
            "Grille " + str(rows) + "x" + str(cols) + " chargee - "
            + str(len(self.slots)) + " emplacement(s). Cliquez sur Resoudre."
        )

    def _on_solve(self):
        if self.grid is None:
            messagebox.showerror("Erreur", "Veuillez charger une grille d'abord.")
            return

        dict_path = self.dict_path_var.get().strip()
        if not dict_path:
            messagebox.showerror("Erreur", "Veuillez choisir un fichier de dictionnaire.")
            return

        try:
            self.words = load_dictionary(dict_path)
        except FileNotFoundError as e:
            messagebox.showerror("Fichier introuvable", str(e))
            return
        except ValueError as e:
            messagebox.showerror("Erreur de donnees", str(e))
            return

        slot_candidates = build_slot_candidates(self.slots, self.words)
        if has_impossible_slot(slot_candidates):
            messagebox.showwarning(
                "Pas de solution",
                "Aucune solution possible : au moins un emplacement n'a aucun candidat.",
            )
            return

        self.status_var.set("Resolution en cours...")
        self.root.update_idletasks()  

        solution_words, stats = solve_crossword(self.slots, self.words)
        self.stats = stats

        if solution_words is None:
            self._refresh_stats()
            msg = "Aucune solution trouvee : les croisements rendent cette instance impossible."
            self.status_var.set(msg)
            messagebox.showwarning("Pas de solution", msg)
            return

        self.solution_words = solution_words
        self.solved_grid = build_solution_grid(self.grid, self.slots, solution_words)

        self._draw_grid()
        self._refresh_words_list()
        self._refresh_stats()
        self.status_var.set(
            "Resolu ! Appels recursifs : " + str(stats['recursive_calls'])
            + " - Essais : " + str(stats['attempts'])
            + " - Retours arriere : " + str(stats['backtracks']) + "."
        )

    def _on_reset(self):
        self.solution_words = None
        self.solved_grid = None
        self.stats = None
        self._draw_grid()
        self._refresh_words_list()
        self._refresh_stats()
        if self.grid is None:
            self.status_var.set("Chargez une grille pour commencer.")
        else:
            self.status_var.set("Grille reinitialisee.")

    # dessin de la grille

    def _draw_grid(self):
        self.canvas.delete("all")

        if self.grid is None:
            self.canvas.config(width=300, height=300)
            self.canvas.create_text(
                150, 150,
                text="(aucune grille chargee)",
                fill="#808080",
                font=("Arial", 11, "italic"),
            )
            return

        rows = len(self.grid)
        cols = len(self.grid[0])


        canvas_w = cols * CELL_SIZE + 2 * CANVAS_PADDING
        canvas_h = rows * CELL_SIZE + 2 * CANVAS_PADDING
        self.canvas.config(width=canvas_w, height=canvas_h, bg="#ffffff")


        if self.solved_grid is not None:
            display_grid = self.solved_grid
        else:
            display_grid = self.grid

        letter_font = ("Arial", int(CELL_SIZE * 0.45), "normal")

        for row in range(rows):
            for col in range(cols):
                x0 = CANVAS_PADDING + col * CELL_SIZE
                y0 = CANVAS_PADDING + row * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE

                char = display_grid[row][col]
                is_black = (char == "#")

                if is_black:
                    fill = "#000000"
                else:
                    fill = "#ffffff"

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="#000000", width=1)

                if not is_black and char != "_" and char != " ":
                    self.canvas.create_text(
                        (x0 + x1) / 2,
                        (y0 + y1) / 2,
                        text=char,
                        font=letter_font,
                        fill="#000000",
                    )

    def _refresh_words_list(self):
        self.words_list.delete(0, tk.END)

        if self.solution_words is None or self.slots is None:
            return
        
        for i in range(len(self.slots)):
            slot = self.slots[i]
            word = self.solution_words[i]
            direction = slot.direction  # 'H' ou 'V'
            label = (
                str(i + 1).rjust(2) + ". (" + str(slot.start_row) + ","
                + str(slot.start_col) + ") " + direction
                + " len=" + str(slot.length).ljust(2) + " -> " + word
            )
            self.words_list.insert(tk.END, label)

    def _refresh_stats(self):
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete("1.0", tk.END)

        if self.stats is None:
            self.stats_text.insert(tk.END, "(pas encore resolu)")
        else:
            txt = (
                "Appels recursifs : " + str(self.stats['recursive_calls']) + "\n"
                + "Essais           : " + str(self.stats['attempts']) + "\n"
                + "Retours arriere  : " + str(self.stats['backtracks']) + "\n"
            )
            self.stats_text.insert(tk.END, txt)

        self.stats_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    CrosswordGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()