from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Slot:
    start_row: int
    start_col: int
    direction: str
    length: int

    def cells(self) -> List[Tuple[int, int]]:
        positions = []

        for offset in range(self.length):
            if self.direction == "H":
                positions.append((self.start_row, self.start_col + offset))
            else:
                positions.append((self.start_row + offset, self.start_col))

        return positions

    def __str__(self) -> str:
        return (
            f"Slot(start=({self.start_row}, {self.start_col}), "
            f"direction={self.direction}, length={self.length})"
        )


def is_white_cell(grid: List[List[str]], row: int, col: int) -> bool:
    return grid[row][col] == "_"


def is_horizontal_start(grid: List[List[str]], row: int, col: int) -> bool:
    if not is_white_cell(grid, row, col):
        return False

    if col > 0 and grid[row][col - 1] == "_":
        return False

    if col + 1 >= len(grid[row]) or grid[row][col + 1] == "#":
        return False

    return True


def is_vertical_start(grid: List[List[str]], row: int, col: int) -> bool:
    if not is_white_cell(grid, row, col):
        return False

    if row > 0 and grid[row - 1][col] == "_":
        return False

    if row + 1 >= len(grid) or grid[row + 1][col] == "#":
        return False

    return True


def horizontal_length(grid: List[List[str]], row: int, col: int) -> int:
    length = 0
    current_col = col

    while current_col < len(grid[row]) and grid[row][current_col] == "_":
        length += 1
        current_col += 1

    return length


def vertical_length(grid: List[List[str]], row: int, col: int) -> int:
    length = 0
    current_row = row

    while current_row < len(grid) and grid[current_row][col] == "_":
        length += 1
        current_row += 1

    return length


def find_slots(grid: List[List[str]]) -> List[Slot]:
    slots = []
    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows):
        for col in range(cols):
            if is_horizontal_start(grid, row, col):
                slots.append(
                    Slot(
                        start_row=row,
                        start_col=col,
                        direction="H",
                        length=horizontal_length(grid, row, col),
                    )
                )

            if is_vertical_start(grid, row, col):
                slots.append(
                    Slot(
                        start_row=row,
                        start_col=col,
                        direction="V",
                        length=vertical_length(grid, row, col),
                    )
                )

    return slots
