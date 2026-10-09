# ---------------------------------------------------------
# Maze Configuration
# ---------------------------------------------------------

GRID_ROWS = 5
GRID_COLS = 6

START = (0, 0)
GOAL = (4, 5)

OBSTACLES = {
    (0, 1),
    (2, 1),
    (2, 3),
    (3, 1),
    (3, 4),
    (4, 4)
}


# ---------------------------------------------------------
# Create Knowledge Base
# ---------------------------------------------------------

free_nodes = set()

for row in range(GRID_ROWS):

    for col in range(GRID_COLS):

        node = (row, col)

        if node not in OBSTACLES:
            free_nodes.add(node)


# ---------------------------------------------------------
# Get Adjacent Nodes
# ---------------------------------------------------------

def get_adjacent_nodes(node):
    """
    Returns all nodes that are directly adjacent
    to the current node.

    Allowed directions:
    Up, Down, Left, Right
    """

    row, col = node

    directions = [
        (-1, 0),   # Up
        (1, 0),    # Down
        (0, -1),   # Left
        (0, 1)     # Right
    ]

    adjacent_nodes = []

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if (
            0 <= new_row < GRID_ROWS
            and 0 <= new_col < GRID_COLS
        ):
            adjacent_nodes.append(
                (new_row, new_col)
            )

    return adjacent_nodes


# ---------------------------------------------------------
# Forward Chaining using GMP
# ---------------------------------------------------------

def forward_chaining():
    """
    Applies Forward Chaining using
    Generalized Modus Ponens.

    Rule:

    At(X) AND Adjacent(X,Y) AND Free(Y)
    -> At(Y)
    """

    # Initial fact
    reachable = {
        START
    }

    # Stores how each node was reached
    parent = {
        START: None
    }

    step = 1

    print("Initial Knowledge Base")
    print("----------------------")
    print(f"At{START}")
    print(f"Goal{GOAL}")

    print("\nStarting Forward Chaining...\n")

    # Continue while new facts are being derived
    changed = True

    while changed:

        changed = False

        # Copy current reachable facts
        current_reachable = list(
            reachable
        )

        for current in current_reachable:

            for neighbor in get_adjacent_nodes(
                current
            ):

                # -------------------------------------------------
                # Check GMP Rule
                #
                # At(current)
                # AND Adjacent(current, neighbor)
                # AND Free(neighbor)
                # -> At(neighbor)
                # -------------------------------------------------

                if (
                    neighbor in free_nodes
                    and neighbor not in reachable
                ):

                    print(
                        f"Step {step}"
                    )

                    print(
                        f"Premise 1: At{current} = True"
                    )

                    print(
                        f"Premise 2: "
                        f"Adjacent({current}, {neighbor}) = True"
                    )

                    print(
                        f"Premise 3: "
                        f"Free{neighbor} = True"
                    )

                    print(
                        "Apply Rule:"
                    )

                    print(
                        "At(X) AND Adjacent(X,Y) "
                        "AND Free(Y) -> At(Y)"
                    )

                    print(
                        f"Inferred Fact: At{neighbor}"
                    )

                    print(
                        "-" * 55
                    )

                    # Add new inferred fact
                    reachable.add(
                        neighbor
                    )

                    # Store parent node
                    parent[
                        neighbor
                    ] = current

                    changed = True

                    step += 1

                    # -------------------------------------------------
                    # Goal Test
                    # -------------------------------------------------

                    if neighbor == GOAL:

                        print(
                            f"\nGoal fact At{GOAL} has been derived."
                        )

                        print(
                            f"Goal{GOAL} is already known."
                        )

                        print(
                            "\nApplying Goal Rule:"
                        )

                        print(
                            "At(X) AND Goal(X) "
                            "-> OutOfMaze"
                        )

                        print(
                            "\nInferred Fact:"
                        )

                        print(
                            "OutOfMaze = True"
                        )

                        return (
                            reachable,
                            parent,
                            True
                        )

    return (
        reachable,
        parent,
        False
    )


# ---------------------------------------------------------
# Reconstruct Path
# ---------------------------------------------------------

def reconstruct_path(
    parent,
    goal
):
    """
    Reconstructs the path from
    the goal back to the start.
    """

    if goal not in parent:
        return None

    path = []

    current = goal

    while current is not None:

        path.append(
            current
        )

        current = parent[
            current
        ]

    path.reverse()

    return path


# ---------------------------------------------------------
# Run Forward Chaining
# ---------------------------------------------------------

reachable, parent, goal_reached = forward_chaining()


# ---------------------------------------------------------
# Display Final Result
# ---------------------------------------------------------

if goal_reached:

    path = reconstruct_path(
        parent,
        GOAL
    )

    print(
        "\nFinal Path:"
    )

    for node in path:

        print(
            node
        )

    print(
        "\nPath Cost:",
        len(path) - 1
    )

    print(
        "\nSuccess Criteria:"
    )

    print(
        "OutOfMaze = True"
    )

else:

    print(
        "\nGoal could not be derived."
    )