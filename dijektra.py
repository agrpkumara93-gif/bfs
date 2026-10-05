import heapq


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
# Get valid successor nodes
# ---------------------------------------------------------

def get_successors(node):
    """
    Returns all valid successor nodes from the current node.
    Movement is allowed Up, Down, Left and Right.
    Obstacles and positions outside the grid are ignored.
    """

    row, col = node

    directions = [
        (-1, 0),   # Up
        (1, 0),    # Down
        (0, -1),   # Left
        (0, 1)     # Right
    ]

    successors = []

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        new_node = (new_row, new_col)

        if (
            0 <= new_row < GRID_ROWS
            and 0 <= new_col < GRID_COLS
            and new_node not in OBSTACLES
        ):
            successors.append(new_node)

    return successors


# ---------------------------------------------------------
# Dijkstra Search
# ---------------------------------------------------------

def dijkstra(start, goal):
    """
    Finds the minimum-cost path from start to goal
    using Dijkstra's Algorithm.
    """

    # Priority queue stores:
    # (total cost, current node, path)
    priority_queue = []

    heapq.heappush(
        priority_queue,
        (0, start, [start])
    )

    # Stores the lowest known cost for each node
    best_cost = {
        start: 0
    }

    while priority_queue:

        # Remove the node with the smallest total cost
        current_cost, current, path = heapq.heappop(
            priority_queue
        )

        print(
            f"Exploring: {current} | Cost: {current_cost}"
        )

        # Goal test
        if current == goal:

            print("\nGoal reached.")

            return path, current_cost

        # Ignore an old queue entry if a better cost
        # has already been found
        if current_cost > best_cost[current]:
            continue

        # Expand successor nodes
        for neighbor in get_successors(current):

            # Every movement costs 1
            step_cost = 1

            new_cost = current_cost + step_cost

            # If this is the first visit to the node,
            # or a cheaper route has been found
            if (
                neighbor not in best_cost
                or new_cost < best_cost[neighbor]
            ):

                best_cost[neighbor] = new_cost

                new_path = path + [neighbor]

                heapq.heappush(
                    priority_queue,
                    (
                        new_cost,
                        neighbor,
                        new_path
                    )
                )

                print(
                    f"   Added {neighbor} "
                    f"with total cost {new_cost}"
                )

    return None, None


# ---------------------------------------------------------
# Run Dijkstra
# ---------------------------------------------------------

path, cost = dijkstra(
    START,
    GOAL
)


# ---------------------------------------------------------
# Display Result
# ---------------------------------------------------------

if path:

    print("\nMinimum Cost Path:")

    for node in path:
        print(node)

    print("\nTotal Cost:", cost)

else:

    print("No path exists.")