import tkinter as tk
from tkinter import ttk
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
# Dijkstra GUI Application
# ---------------------------------------------------------

class DijkstraVisualizer:

    def __init__(self, root):
        """
        Initializes the GUI, maze, labels,
        buttons, calculation table and
        Dijkstra search variables.
        """

        self.root = root
        self.root.title("Dijkstra Maze Visualizer")
        self.root.geometry("1450x720")

        self.cell_size = 85

        # Movement directions:
        # Up, Down, Left, Right
        self.directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        # -------------------------------------------------
        # Main Title
        # -------------------------------------------------

        title = tk.Label(
            root,
            text="Dijkstra's Algorithm - Maze Visualizer",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        # -------------------------------------------------
        # Main Layout
        # -------------------------------------------------

        main_frame = tk.Frame(root)

        main_frame.pack()

        # -------------------------------------------------
        # Maze Canvas
        # -------------------------------------------------

        self.canvas = tk.Canvas(
            main_frame,
            width=GRID_COLS * self.cell_size,
            height=GRID_ROWS * self.cell_size,
            bg="white"
        )

        self.canvas.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        # -------------------------------------------------
        # Information Panel
        # -------------------------------------------------

        info_frame = tk.Frame(main_frame)

        info_frame.grid(
            row=0,
            column=1,
            padx=20,
            sticky="n"
        )

        self.status_label = tk.Label(
            info_frame,
            text="Press Start Dijkstra",
            font=("Arial", 14, "bold"),
            wraplength=300
        )

        self.status_label.pack(
            pady=10
        )

        self.current_label = tk.Label(
            info_frame,
            text="Current Node: None",
            font=("Arial", 12)
        )

        self.current_label.pack(
            pady=5
        )

        self.current_cost_label = tk.Label(
            info_frame,
            text="Current Cost: -",
            font=("Arial", 12)
        )

        self.current_cost_label.pack(
            pady=5
        )

        self.queue_label = tk.Label(
            info_frame,
            text="Priority Queue: []",
            font=("Arial", 10),
            wraplength=300,
            justify="left"
        )

        self.queue_label.pack(
            pady=10
        )

        self.visited_label = tk.Label(
            info_frame,
            text="Explored Nodes: 0",
            font=("Arial", 11)
        )

        self.visited_label.pack(
            pady=5
        )

        self.final_cost_label = tk.Label(
            info_frame,
            text="Minimum Cost: -",
            font=("Arial", 13, "bold")
        )

        self.final_cost_label.pack(
            pady=10
        )

        # -------------------------------------------------
        # Start Button
        # -------------------------------------------------

        self.start_button = tk.Button(
            info_frame,
            text="Start Dijkstra",
            font=("Arial", 12, "bold"),
            width=18,
            command=self.start_dijkstra
        )

        self.start_button.pack(
            pady=5
        )

        # -------------------------------------------------
        # Pause / Resume Button
        # -------------------------------------------------

        self.pause_button = tk.Button(
            info_frame,
            text="Pause",
            font=("Arial", 12),
            width=18,
            command=self.toggle_pause,
            state="disabled"
        )

        self.pause_button.pack(
            pady=5
        )

        # -------------------------------------------------
        # Reset Button
        # -------------------------------------------------

        self.reset_button = tk.Button(
            info_frame,
            text="Reset",
            font=("Arial", 12),
            width=18,
            command=self.reset
        )

        self.reset_button.pack(
            pady=5
        )

        # -------------------------------------------------
        # Legend
        # -------------------------------------------------

        legend = tk.Label(
            info_frame,
            text=(
                "Legend\n\n"
                "Green = Start\n"
                "Red = Goal\n"
                "Black = Obstacle\n"
                "Yellow = Current Node\n"
                "Light Blue = Explored Node\n"
                "Purple = Minimum Cost Path\n"
                "Gray Row = Visited Node"
            ),
            font=("Arial", 11),
            justify="left"
        )

        legend.pack(
            pady=20
        )

        # -------------------------------------------------
        # Dijkstra Calculation Table
        # -------------------------------------------------

        table_frame = tk.Frame(main_frame)

        table_frame.grid(
            row=0,
            column=2,
            padx=20,
            pady=20,
            sticky="n"
        )

        table_title = tk.Label(
            table_frame,
            text="Dijkstra Calculation Table",
            font=("Arial", 13, "bold")
        )

        table_title.pack(
            pady=(0, 10)
        )

        # Create Treeview table
        self.table = ttk.Treeview(
            table_frame,
            columns=(
                "Node",
                "Shortest Path",
                "Previous Node"
            ),
            show="headings",
            height=18
        )

        # Table headings
        self.table.heading(
            "Node",
            text="Node"
        )

        self.table.heading(
            "Shortest Path",
            text="Shortest Path"
        )

        self.table.heading(
            "Previous Node",
            text="Previous Node"
        )

        # Table column sizes
        self.table.column(
            "Node",
            width=100,
            anchor="center"
        )

        self.table.column(
            "Shortest Path",
            width=110,
            anchor="center"
        )

        self.table.column(
            "Previous Node",
            width=120,
            anchor="center"
        )

        # Scrollbar
        table_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=table_scrollbar.set
        )

        self.table.pack(
            side="left"
        )

        table_scrollbar.pack(
            side="right",
            fill="y"
        )

        # Gray style for visited nodes
        self.table.tag_configure(
            "visited",
            background="lightgray"
        )

        # Draw maze
        self.draw_maze()

        # Initialize search data
        self.reset_search_data()


    # ---------------------------------------------------------
    # Reset Search Data
    # ---------------------------------------------------------

    def reset_search_data(self):
        """
        Clears all search-related data.
        """

        # Priority queue stores:
        # (cost, node, path)
        self.priority_queue = []

        # Minimum known cost for each node
        self.best_cost = {}

        # Nodes already explored
        self.explored = set()

        # Final shortest path
        self.final_path = None

        # Running status
        self.running = False

        # Pause status
        self.paused = False

        # Stores previous node for each discovered node
        self.previous_node = {
            START: None
        }

        # Stores Treeview row IDs for each node
        self.table_rows = {}


    # ---------------------------------------------------------
    # Draw Maze
    # ---------------------------------------------------------

    def draw_maze(self):
        """
        Draws the maze with start, goal
        and obstacle nodes.
        """

        self.canvas.delete("all")

        for row in range(GRID_ROWS):

            for col in range(GRID_COLS):

                cell = (
                    row,
                    col
                )

                x1 = col * self.cell_size
                y1 = row * self.cell_size

                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "white"

                if cell in OBSTACLES:

                    color = "black"

                elif cell == START:

                    color = "green"

                elif cell == GOAL:

                    color = "red"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="gray",
                    width=2
                )

                text_color = (
                    "white"
                    if color in [
                        "black",
                        "green",
                        "red"
                    ]
                    else "black"
                )

                self.canvas.create_text(
                    x1 + self.cell_size / 2,
                    y1 + self.cell_size / 2,
                    text=str(cell),
                    font=("Arial", 11, "bold"),
                    fill=text_color
                )


    # ---------------------------------------------------------
    # Get Successors
    # ---------------------------------------------------------

    def get_successors(self, node):
        """
        Returns all valid successor nodes
        from the current node.

        Movement is allowed:
        Up, Down, Left and Right.
        """

        row, col = node

        successors = []

        for dr, dc in self.directions:

            new_row = row + dr
            new_col = col + dc

            new_node = (
                new_row,
                new_col
            )

            if (
                0 <= new_row < GRID_ROWS
                and 0 <= new_col < GRID_COLS
                and new_node not in OBSTACLES
            ):

                successors.append(
                    new_node
                )

        return successors


    # ---------------------------------------------------------
    # Start Dijkstra
    # ---------------------------------------------------------

    def start_dijkstra(self):
        """
        Initializes Dijkstra's algorithm
        and starts the animation.
        """

        if self.running:

            return

        # Clear old table rows
        for row in self.table.get_children():

            self.table.delete(row)

        # Reset data
        self.reset_search_data()

        # Redraw maze
        self.draw_maze()

        # Add start node to priority queue
        heapq.heappush(
            self.priority_queue,
            (
                0,
                START,
                [START]
            )
        )

        # Cost of start node is 0
        self.best_cost = {
            START: 0
        }

        # Previous node for start is None
        self.previous_node = {
            START: None
        }

        self.running = True
        self.paused = False

        self.status_label.config(
            text="Dijkstra Search Started..."
        )

        self.start_button.config(
            state="disabled"
        )

        self.pause_button.config(
            state="normal",
            text="Pause"
        )

        # Start algorithm
        self.dijkstra_step()


    # ---------------------------------------------------------
    # Pause / Resume
    # ---------------------------------------------------------

    def toggle_pause(self):
        """
        Pauses or resumes the Dijkstra search.
        """

        if not self.running:

            return

        # Pause
        if not self.paused:

            self.paused = True

            self.pause_button.config(
                text="Resume"
            )

            self.status_label.config(
                text="Search Paused"
            )

        # Resume
        else:

            self.paused = False

            self.pause_button.config(
                text="Pause"
            )

            self.status_label.config(
                text="Search Resumed"
            )

            self.dijkstra_step()


    # ---------------------------------------------------------
    # Dijkstra Step
    # ---------------------------------------------------------

    def dijkstra_step(self):
        """
        Executes one step of Dijkstra's algorithm.

        The node with the smallest accumulated cost
        is removed from the priority queue.
        """

        # Stop if paused
        if self.paused:

            return

        # No more nodes to explore
        if not self.priority_queue:

            self.running = False

            self.status_label.config(
                text="No path exists."
            )

            self.start_button.config(
                state="normal"
            )

            self.pause_button.config(
                state="disabled"
            )

            return

        # Remove node with minimum cost
        current_cost, current, path = heapq.heappop(
            self.priority_queue
        )

        # Ignore old queue entry if better cost exists
        if current_cost > self.best_cost[current]:

            self.root.after(
                300,
                self.dijkstra_step
            )

            return

        # Mark current node as explored
        self.explored.add(
            current
        )

        # Record the node when it is explored, in priority-queue order
        self.update_calculation_table(
            current,
            current_cost,
            self.previous_node[current]
        )

        # Change table row to gray
        self.mark_table_visited(
            current
        )

        # Update labels
        self.current_label.config(
            text=f"Current Node: {current}"
        )

        self.current_cost_label.config(
            text=f"Current Cost: {current_cost}"
        )

        self.visited_label.config(
            text=f"Explored Nodes: {len(self.explored)}"
        )

        self.status_label.config(
            text=f"Exploring {current}"
        )

        # Update queue display
        self.update_queue_display()

        # Highlight current node
        if (
            current != START
            and current != GOAL
        ):

            self.highlight_cell(
                current,
                "yellow"
            )

        # -------------------------------------------------
        # Goal Test
        # -------------------------------------------------

        if current == GOAL:

            self.final_path = path

            self.running = False

            self.status_label.config(
                text="Goal Reached!"
            )

            self.final_cost_label.config(
                text=f"Minimum Cost: {current_cost}"
            )

            self.pause_button.config(
                state="disabled"
            )

            self.root.after(
                500,
                self.show_final_path
            )

            return

        # -------------------------------------------------
        # Expand Successors
        # -------------------------------------------------

        for neighbor in self.get_successors(
            current
        ):

            # Every movement costs 1
            step_cost = 1

            new_cost = (
                current_cost
                + step_cost
            )

            # If this is the first time the node
            # has been discovered, or if a cheaper
            # path has been found
            if (
                neighbor not in self.best_cost
                or new_cost < self.best_cost[neighbor]
            ):

                # Store shortest known cost
                self.best_cost[
                    neighbor
                ] = new_cost

                # Store previous node
                self.previous_node[
                    neighbor
                ] = current

                # Store updated path
                new_path = (
                    path
                    + [neighbor]
                )

                # Add node to priority queue
                heapq.heappush(
                    self.priority_queue,
                    (
                        new_cost,
                        neighbor,
                        new_path
                    )
                )

        # After exploring, change current node
        # from yellow to light blue
        if (
            current != START
            and current != GOAL
        ):

            self.root.after(
                300,
                lambda node=current:
                self.highlight_cell(
                    node,
                    "lightblue"
                )
            )

        # Continue algorithm
        self.root.after(
            700,
            self.dijkstra_step
        )


    # ---------------------------------------------------------
    # Update Priority Queue
    # ---------------------------------------------------------

    def update_queue_display(self):
        """
        Displays nodes currently in the priority queue
        along with their accumulated cost.
        """

        queue_items = []

        for cost, node, path in sorted(
            self.priority_queue
        ):

            queue_items.append(
                f"{node}: cost {cost}"
            )

        if queue_items:

            queue_text = "\n".join(
                queue_items
            )

        else:

            queue_text = "Empty"

        self.queue_label.config(
            text=(
                "Priority Queue:\n"
                + queue_text
            )
        )


    # ---------------------------------------------------------
    # Update Calculation Table
    # ---------------------------------------------------------

    def update_calculation_table(
        self,
        node,
        shortest_path,
        previous_node
    ):
        """
        Adds a node to the Dijkstra calculation table
        or updates it if the node already exists.

        Columns:
        Node
        Shortest Path
        Previous Node
        """

        node_text = str(
            node
        )

        if previous_node is None:

            previous_text = "None"

        else:

            previous_text = str(
                previous_node
            )

        # Update existing row
        if node in self.table_rows:

            row_id = self.table_rows[
                node
            ]

            self.table.item(
                row_id,
                values=(
                    node_text,
                    shortest_path,
                    previous_text
                )
            )

        # Add new row
        else:

            row_id = self.table.insert(
                "",
                "end",
                values=(
                    node_text,
                    shortest_path,
                    previous_text
                )
            )

            self.table_rows[
                node
            ] = row_id


    # ---------------------------------------------------------
    # Mark Table Row as Visited
    # ---------------------------------------------------------

    def mark_table_visited(
        self,
        node
    ):
        """
        Changes the row colour to gray
        after the node has been visited.
        """

        if node in self.table_rows:

            row_id = self.table_rows[
                node
            ]

            self.table.item(
                row_id,
                tags=(
                    "visited",
                )
            )


    # ---------------------------------------------------------
    # Highlight Cell
    # ---------------------------------------------------------

    def highlight_cell(
        self,
        cell,
        color
    ):
        """
        Changes the colour of a maze cell.
        """

        row, col = cell

        x1 = col * self.cell_size
        y1 = row * self.cell_size

        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Keep start green
        if cell == START:

            color = "green"

        # Keep goal red
        elif cell == GOAL:

            color = "red"

        self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=color,
            outline="gray",
            width=2
        )

        text_color = (
            "white"
            if color in [
                "green",
                "red",
                "purple",
                "black"
            ]
            else "black"
        )

        self.canvas.create_text(
            x1 + self.cell_size / 2,
            y1 + self.cell_size / 2,
            text=str(cell),
            font=("Arial", 11, "bold"),
            fill=text_color
        )


    # ---------------------------------------------------------
    # Show Final Path
    # ---------------------------------------------------------

    def show_final_path(self):
        """
        Displays the minimum-cost path
        using purple cells.
        """

        if not self.final_path:

            return

        for cell in self.final_path:

            if cell == START:

                self.highlight_cell(
                    cell,
                    "green"
                )

            elif cell == GOAL:

                self.highlight_cell(
                    cell,
                    "red"
                )

            else:

                self.highlight_cell(
                    cell,
                    "purple"
                )

        self.status_label.config(
            text=(
                "Minimum Cost Path Found\n\n"
                + str(self.final_path)
            )
        )

        self.start_button.config(
            state="normal"
        )


    # ---------------------------------------------------------
    # Reset GUI
    # ---------------------------------------------------------

    def reset(self):
        """
        Resets the maze, table and all
        Dijkstra search information.
        """

        self.running = False
        self.paused = False

        # Clear table
        for row in self.table.get_children():

            self.table.delete(row)

        # Reset search data
        self.reset_search_data()

        # Redraw maze
        self.draw_maze()

        # Reset labels
        self.status_label.config(
            text="Press Start Dijkstra"
        )

        self.current_label.config(
            text="Current Node: None"
        )

        self.current_cost_label.config(
            text="Current Cost: -"
        )

        self.queue_label.config(
            text="Priority Queue: []"
        )

        self.visited_label.config(
            text="Explored Nodes: 0"
        )

        self.final_cost_label.config(
            text="Minimum Cost: -"
        )

        self.start_button.config(
            state="normal"
        )

        self.pause_button.config(
            state="disabled",
            text="Pause"
        )


# ---------------------------------------------------------
# Start Application
# ---------------------------------------------------------

root = tk.Tk()

app = DijkstraVisualizer(
    root
)

root.mainloop()