from collections import deque


def find_bfs_path(rows, cols, start, goal, obstacles):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    queue = deque([(start, [start])])

    visited = set([start])

    while queue:
        (curr_r, curr_c), path = queue.popleft()

        if (curr_r, curr_c) == goal:
            return path

        for dr, dc in directions:
            nr, nc = curr_r + dr, curr_c + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) not in obstacles and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))

    return None


GRID_ROWS = 5
GRID_COLS = 6

START = (0, 0)
GOAL = (4, 5)

OBSTACLES = {(0, 1), (2, 1), (2, 3), (3, 1), (3, 4), (4, 4)}


def print_maze(rows, cols, start, goal, obstacles, path):
    path_set = set(path) if path else set()

    print(
        "\nMaze Legend: [S] Start | [G] Goal | [X] Blocker | [*] Path | [.] Empty\n")
    for r in range(rows):
        row_str = []
        for c in range(cols):
            cell = (r, c)
            if cell == start:
                row_str.append(" S ")
            elif cell == goal:
                row_str.append(" G ")
            elif cell in obstacles:
                row_str.append(" X ")
            elif cell in path_set:
                row_str.append(" * ")
            else:
                row_str.append(" . ")
        print("".join(row_str))


if __name__ == "__main__":
    bfs_path = find_bfs_path(
        GRID_ROWS, GRID_COLS, START, GOAL, OBSTACLES
    )

    if bfs_path:
        print(
            f"Path found.\nPath: {bfs_path}\nCost: {len(bfs_path) - 1}"
        )
        print_maze(GRID_ROWS, GRID_COLS, START, GOAL, OBSTACLES, bfs_path)
    else:
        print("No path exists to the goal.")
