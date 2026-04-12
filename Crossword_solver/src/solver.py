from typing import Dict, List, Optional, Tuple
from slot import Slot


def group_words_by_length(words: List[str]) -> Dict[int, List[str]]:
    words_by_length = {}

    for word in words:
        length = len(word)

        if length not in words_by_length:
            words_by_length[length] = []

        words_by_length[length].append(word)

    return words_by_length


def find_candidates_for_slot(
    slot: Slot,
    words_by_length: Dict[int, List[str]],
) -> List[str]:
    if slot.length not in words_by_length:
        return []

    return words_by_length[slot.length][:]


def build_slot_candidates(slots: List[Slot], words: List[str]) -> List[List[str]]:
    words_by_length = group_words_by_length(words)
    slot_candidates = []

    for slot in slots:
        candidates = find_candidates_for_slot(slot, words_by_length)
        slot_candidates.append(candidates)

    return slot_candidates


def has_impossible_slot(slot_candidates: List[List[str]]) -> bool:
    for candidates in slot_candidates:
        if len(candidates) == 0:
            return True

    return False


def find_intersection(slot1: Slot, slot2: Slot) -> Optional[Tuple[int, int]]:
    cells1 = slot1.cells()
    cells2 = slot2.cells()

    for index1 in range(len(cells1)):
        for index2 in range(len(cells2)):
            if cells1[index1] == cells2[index2]:
                return index1, index2

    return None


def are_words_compatible(slot1: Slot, word1: str, slot2: Slot, word2: str) -> bool:
    intersection = find_intersection(slot1, slot2)

    if intersection is None:
        return True

    index1, index2 = intersection
    return word1[index1] == word2[index2]


def can_assign_word(
    slot_index: int,
    word: str,
    slots: List[Slot],
    assignment: List[Optional[str]],
) -> bool:
    current_slot = slots[slot_index]

    if len(word) != current_slot.length:
        return False

    for other_index in range(len(assignment)):
        other_word = assignment[other_index]

        if other_word is None:
            continue

        other_slot = slots[other_index]

        if not are_words_compatible(current_slot, word, other_slot, other_word):
            return False

    return True


def choose_next_slot(
    assignment: List[Optional[str]],
    domains: List[List[str]],
) -> int:
    best_index = -1
    best_size = -1

    for slot_index in range(len(assignment)):
        if assignment[slot_index] is not None:
            continue

        current_size = len(domains[slot_index])

        if best_index == -1 or current_size < best_size:
            best_index = slot_index
            best_size = current_size

    return best_index


def copy_domains(domains: List[List[str]]) -> List[List[str]]:
    copied = []

    for domain in domains:
        copied.append(domain[:])

    return copied


def forward_check(
    assigned_index: int,
    assigned_word: str,
    slots: List[Slot],
    assignment: List[Optional[str]],
    domains: List[List[str]],
    used_words: set[str],
) -> bool:
    for other_index in range(len(slots)):
        if other_index == assigned_index:
            continue

        if assignment[other_index] is not None:
            continue

        new_domain = []

        for candidate in domains[other_index]:
            if candidate in used_words:
                continue

            if are_words_compatible(
                slots[assigned_index],
                assigned_word,
                slots[other_index],
                candidate,
            ):
                new_domain.append(candidate)

        domains[other_index] = new_domain

        if len(domains[other_index]) == 0:
            return False

    return True


def solve_recursive(
    slots: List[Slot],
    assignment: List[Optional[str]],
    domains: List[List[str]],
    used_words: set[str],
    stats: Dict[str, int],
) -> bool:
    stats["recursive_calls"] += 1

    if all(word is not None for word in assignment):
        return True

    slot_index = choose_next_slot(assignment, domains)

    if slot_index == -1:
        return False

    for word in domains[slot_index]:
        if word in used_words:
            continue

        stats["attempts"] += 1

        if not can_assign_word(slot_index, word, slots, assignment):
            continue

        old_domains = copy_domains(domains)

        assignment[slot_index] = word
        used_words.add(word)
        domains[slot_index] = [word]

        if forward_check(slot_index, word, slots, assignment, domains, used_words):
            if solve_recursive(slots, assignment, domains, used_words, stats):
                return True

        assignment[slot_index] = None
        used_words.remove(word)
        stats["backtracks"] += 1
        domains[:] = old_domains

    return False


def solve_crossword(
    slots: List[Slot],
    words: List[str],
) -> Tuple[Optional[List[str]], Dict[str, int]]:
    initial_domains = build_slot_candidates(slots, words)

    stats = {
        "recursive_calls": 0,
        "attempts": 0,
        "backtracks": 0,
    }

    if has_impossible_slot(initial_domains):
        return None, stats

    assignment: List[Optional[str]] = [None] * len(slots)
    used_words: set[str] = set()
    domains = copy_domains(initial_domains)

    solved = solve_recursive(slots, assignment, domains, used_words, stats)

    if not solved:
        return None, stats

    solution = [word for word in assignment if word is not None]
    return solution, stats


def build_solution_grid(
    grid: List[List[str]],
    slots: List[Slot],
    solution_words: List[str],
) -> List[List[str]]:
    result = []

    for row in grid:
        result.append(row[:])

    for slot_index in range(len(slots)):
        slot = slots[slot_index]
        word = solution_words[slot_index]
        cells = slot.cells()

        for letter_index in range(len(cells)):
            row, col = cells[letter_index]
            result[row][col] = word[letter_index]

    return result