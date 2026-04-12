import os
from loader import load_dictionary, load_grid
from slot import find_slots
from solver import (
    build_slot_candidates,
    build_solution_grid,
    has_impossible_slot,
    solve_crossword,
)


def display_grid(grid: list[list[str]]) -> None:
    for row in grid:
        print("".join(row))


def ask_file_name(message: str, default_name: str) -> str:
    user_input = input(f"{message} [{default_name}] : ").strip()

    if user_input == "":
        return default_name

    return user_input


def build_data_path(project_dir: str, file_name: str) -> str:
    return os.path.join(project_dir, "data", file_name)


def display_slot_summary(slots: list, slot_candidates: list[list[str]]) -> None:
    print("=== EMPLACEMENTS ET CANDIDATS INITIAUX ===")

    for index, slot in enumerate(slots, start=1):
        candidates = slot_candidates[index - 1]

        print(f"{index}. {slot}")
        print(f"   Cases : {slot.cells()}")
        print(f"   Candidats ({len(candidates)}) : {candidates}")
        print()


def display_stats(stats: dict[str, int]) -> None:
    print("=== STATISTIQUES ===")
    print(f"Appels recursifs : {stats['recursive_calls']}")
    print(f"Essais de placement : {stats['attempts']}")
    print(f"Retours arriere : {stats['backtracks']}")
    print()


def main() -> None:
    src_dir = os.path.dirname(__file__)
    project_dir = os.path.dirname(src_dir)

    print("=== CROSSWORD SOLVER ===")
    print("Format grille : '_' = blanc, '#' = noir")
    print()

    grid_file = ask_file_name("Nom du fichier grille", "Entrez un fichier txt")
    dict_file = ask_file_name("Nom du fichier dictionnaire", "Entrez un fichier txt")

    grid_path = build_data_path(project_dir, grid_file)
    dict_path = build_data_path(project_dir, dict_file)

    try:
        grid = load_grid(grid_path)
        words = load_dictionary(dict_path)
        slots = find_slots(grid)
        slot_candidates = build_slot_candidates(slots, words)
    except FileNotFoundError as error:
        print(f"Fichier introuvable : {error}")
        return
    except ValueError as error:
        print(f"Erreur de donnees : {error}")
        return

    print()
    print("=== GRILLE INITIALE ===")
    display_grid(grid)
    print()

    print("=== RESUME ===")
    print(f"Fichier grille : {grid_file}")
    print(f"Fichier dictionnaire : {dict_file}")
    print(f"Dimensions : {len(grid)} x {len(grid[0])}")
    print(f"Nombre de mots dans le dictionnaire : {len(words)}")
    print(f"Nombre d'emplacements : {len(slots)}")
    print()

    display_slot_summary(slots, slot_candidates)

    if has_impossible_slot(slot_candidates):
        print("Aucune solution possible : au moins un emplacement n'a aucun candidat.")
        return

    solution_words, stats = solve_crossword(slots, words)

    if solution_words is None:
        print("Aucune solution trouvee : les croisements rendent cette instance impossible.")
        print()
        display_stats(stats)
        return

    solved_grid = build_solution_grid(grid, slots, solution_words)

    print("=== SOLUTION ===")
    display_grid(solved_grid)
    print()

    print("=== MOTS UTILISES ===")
    for index, word in enumerate(solution_words, start=1):
        print(f"{index}. {word}")
    print()

    display_stats(stats)


if __name__ == "__main__":
    main()