from typing import List


def read_non_empty_lines(file_path: str) -> List[str]:
    lines = []

    with open(file_path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if line != "":
                lines.append(line)

    return lines


def validate_grid_lines(lines: List[str]) -> None:
    if len(lines) == 0:
        raise ValueError("La grille est vide.")

    expected_length = len(lines[0])

    for line in lines:
        if len(line) != expected_length:
            raise ValueError("Toutes les lignes doivent avoir la même longueur.")

        for char in line:
            if char not in "_#":
                raise ValueError("La grille doit contenir seulement '_' et '#'.")


def load_grid(file_path: str) -> List[List[str]]:
    lines = read_non_empty_lines(file_path)
    validate_grid_lines(lines)
    return [list(line) for line in lines]


def load_dictionary(file_path: str) -> List[str]:
    lines = read_non_empty_lines(file_path)

    words = []
    seen = set()

    for line in lines:
        word = line.lower()

        if word.isalpha() and word not in seen:
            words.append(word)
            seen.add(word)

    if len(words) == 0:
        raise ValueError("Le dictionnaire est vide ou invalide.")

    return words
