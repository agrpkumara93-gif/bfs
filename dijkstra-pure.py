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
    Returns all valid neighboring nodes.

    Movement is allowed:
    Up, Down, Left and Right.

    Nodes outside the maze and obstacle nodes
    are not allowed.
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

        # Check whether the new node is inside the maze
        # and is not an obstacle
        if (
            0 <= new_row < GRID_ROWS
            and 0 <= new_col < GRID_COLS
            and new_node not in OBSTACLES
        ):
            successors.append(new_node)

    return successors


# ---------------------------------------------------------
# Dijkstra's Algorithm
# ---------------------------------------------------------

def dijkstra(start, goal):
    """
    Finds the minimum-cost path from the start node
    to the goal node using Dijkstra's Algorithm.
    """

    # Priority queue stores:
    # (total_cost, current_node)
    priority_queue = []

    # Add the start node with cost 0
    heapq.heappush(
        priority_queue,
        (0, start)
    )

    # Stores the minimum known cost to each node
    shortest_cost = {
        start: 0
    }

    # Stores the previous node used to reach each node
    previous_node = {
        start: None
    }

    # Stores visited nodes
    visited = set()

    while priority_queue:

        # Remove the node with the smallest cost
        current_cost, current = heapq.heappop(
            priority_queue
        )

        # Skip the node if it was already visited
        if current in visited:
            continue

        # Mark the node as visited
        visited.add(current)

        print(
            f"Exploring: {current} | Cost: {current_cost}"
        )

        # Check whether the goal has been reached
        if current == goal:
            break

        # Check each valid successor node
        for neighbor in get_successors(current):

            # Every movement has a cost of 1
            step_cost = 1

            # Calculate the new total cost
            new_cost = current_cost + step_cost

            # Update the neighbor if:
            # 1. It has not been discovered before, or
            # 2. A cheaper path has been found
            if (
                neighbor not in shortest_cost
                or new_cost < shortest_cost[neighbor]
            ):

                shortest_cost[neighbor] = new_cost

                previous_node[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (
                        new_cost,
                        neighbor
                    )
                )

    # -----------------------------------------------------
    # If goal was not reached
    # -----------------------------------------------------

    if goal not in shortest_cost:
        return None, None, shortest_cost, previous_node

    # -----------------------------------------------------
    # Reconstruct shortest path
    # -----------------------------------------------------

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = previous_node[current]

    # Path is currently goal -> start,
    # so reverse it
    path.reverse()

    return (
        path,
        shortest_cost[goal],
        shortest_cost,
        previous_node
    )


# ---------------------------------------------------------
# Run Dijkstra
# ---------------------------------------------------------

path, cost, shortest_cost, previous_node = dijkstra(
    START,
    GOAL
)


# ---------------------------------------------------------
# Display Result
# ---------------------------------------------------------

if path:

    print("\nShortest Path:")

    for node in path:
        print(node)

    print(
        "\nTotal Cost:",
        cost
    )

else:

    print(
        "\nNo path exists to the goal."
    )


# ---------------------------------------------------------
# Display Cost Table
# ---------------------------------------------------------

print("\nDijkstra Cost Table")

print(
    f"{'Node':<12}"
    f"{'Shortest Cost':<18}"
    f"{'Previous Node':<15}"
)

print("-" * 45)

for node in shortest_cost:

    print(
        f"{str(node):<12}"
        f"{shortest_cost[node]:<18}"
        f"{str(previous_node[node]):<15}"
    )