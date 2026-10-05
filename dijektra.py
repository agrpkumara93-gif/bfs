import tkinter as tk
from tkinter import messagebox
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
        Initializes the GUI, creates the maze,
        information panel and control buttons.
        """

        self.root = root
        self.root.title("Dijkstra Maze Visualizer")
        self.root.geometry("1100x680")

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
            wraplength=320
        )
        self.status_label.pack(pady=10)

        self.current_label = tk.Label(
            info_frame,
            text="Current Node: None",
            font=("Arial", 12)
        )
        self.current_label.pack(pady=5)

        self.current_cost_label = tk.Label(
            info_frame,
            text="Current Cost: -",
            font=("Arial", 12)
        )
        self.current_cost_label.pack(pady=5)

        self.queue_label = tk.Label(
            info_frame,
            text="Priority Queue: []",
            font=("Arial", 10),
            wraplength=330,
            justify="left"
        )
        self.queue_label.pack(pady=10)

        self.visited_label = tk.Label(
            info_frame,
            text="Explored Nodes: 0",
            font=("Arial", 11)
        )
        self.visited_label.pack(pady=5)

        self.final_cost_label = tk.Label(
            info_frame,
            text="Minimum Cost: -",
            font=("Arial", 13, "bold")
        )
        self.final_cost_label.pack(pady=10)

        # -------------------------------------------------
        # Buttons
        # -------------------------------------------------

        self.start_button = tk.Button(
            info_frame,
            text="Start Dijkstra",
            font=("Arial", 12, "bold"),
            width=18,
            command=self.start_dijkstra
        )
        self.start_button.pack(pady=10)

        self.pause_button = tk.Button(
            info_frame,
            text="Pause",
            font=("Arial", 12),
            width=18,
            command=self.toggle_pause,
            state="disabled"
        )
        self.pause_button.pack(pady=5)

        self.reset_button = tk.Button(
            info_frame,
            text="Reset",
            font=("Arial", 12),
            width=18,
            command=self.reset
        )
        self.reset_button.pack(pady=5)

        # -------------------------------------------------
        # Legend
        # -------------------------------------------------

        legend = tk.Label(
            info_frame,
            text=(
                "Legend\n\n"
                "Green  = Start\n"
                "Red    = Goal\n"
                "Black  = Obstacle\n"
                "Yellow = Current Node\n"
                "Blue   = Explored Node\n"
                "Purple = Minimum Cost Path"
            ),
            font=("Arial", 11),
            justify="left"
        )
        legend.pack(pady=20)

        # Draw initial maze
        self.draw_maze()

        # Initialize search data
        self.reset_search_data()


    # ---------------------------------------------------------
    # Reset internal Dijkstra data
    # ---------------------------------------------------------

    def reset_search_data(self):
        """
        Clears all data used by Dijkstra's algorithm.
        """

        # Priority queue stores:
        # (cost, node, path)
        self.priority_queue = []

        # Stores the minimum known cost to each node
        self.best_cost = {}

        # Stores explored nodes
        self.explored = set()

        # Stores the final path
        self.final_path = None

        # Search status
        self.running = False
        self.paused = False
        self.step_after_id = None


    # ---------------------------------------------------------
    # Draw Maze
    # ---------------------------------------------------------

    def draw_maze(self):
        """
        Draws the maze grid with start, goal
        and obstacle nodes.
        """

        self.canvas.delete("all")

        for row in range(GRID_ROWS):

            for col in range(GRID_COLS):

                cell = (row, col)

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

                text_color = "white" if color in [
                    "black",
                    "green",
                    "red"
                ] else "black"

                self.canvas.create_text(
                    x1 + self.cell_size / 2,
                    y1 + self.cell_size / 2,
                    text=str(cell),
                    font=("Arial", 11, "bold"),
                    fill=text_color
                )


    # ---------------------------------------------------------
    # Get Successor Nodes
    # ---------------------------------------------------------

    def get_successors(self, node):
        """
        Returns all valid successor nodes.

        Movement is allowed:
        Up, Down, Left and Right.

        Obstacles and positions outside
        the maze are ignored.
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
                successors.append(new_node)

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

        self.reset_search_data()
        self.draw_maze()

        # Add start node with cost 0
        heapq.heappush(
            self.priority_queue,
            (
                0,
                START,
                [START]
            )
        )

        # Minimum known cost to start is 0
        self.best_cost = {
            START: 0
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
            text="Pause",
            state="normal"
        )

        # Start search
        self.dijkstra_step()


    # ---------------------------------------------------------
    # Execute One Dijkstra Step
    # ---------------------------------------------------------

    def dijkstra_step(self):
        """
        Executes one step of Dijkstra's algorithm.

        The node with the smallest cost is removed
        from the priority queue and explored.
        """

        self.step_after_id = None

        if not self.running or self.paused:
            return

        # If priority queue is empty,
        # there is no path
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

        # Remove node with smallest cost
        current_cost, current, path = heapq.heappop(
            self.priority_queue
        )

        # Ignore old queue entry if a cheaper
        # path has already been discovered
        if current_cost > self.best_cost[current]:

            self.step_after_id = self.root.after(
                300,
                self.dijkstra_step
            )

            return

        # Mark node as explored
        self.explored.add(current)

        # Update GUI information
        self.current_label.config(
            text=f"Current Node: {current}"
        )

        self.current_cost_label.config(
            text=f"Current Cost: {current_cost}"
        )

        self.visited_label.config(
            text=f"Explored Nodes: {len(self.explored)}"
        )

        self.update_queue_display()

        self.status_label.config(
            text=f"Exploring {current}"
        )

        # Highlight current node
        if current != START and current != GOAL:

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
            self.pause_button.config(
                state="disabled"
            )

            self.final_cost_label.config(
                text=f"Minimum Cost: {current_cost}"
            )

            self.root.after(
                500,
                self.show_final_path
            )

            return

        # -------------------------------------------------
        # Expand Successor Nodes
        # -------------------------------------------------

        for neighbor in self.get_successors(current):

            # Every move costs 1
            step_cost = 1

            new_cost = (
                current_cost
                + step_cost
            )

            # If neighbor has not been discovered,
            # or this route is cheaper
            if (
                neighbor not in self.best_cost
                or new_cost < self.best_cost[neighbor]
            ):

                # Update minimum known cost
                self.best_cost[neighbor] = new_cost

                # Create updated path
                new_path = (
                    path
                    + [neighbor]
                )

                # Add successor to priority queue
                heapq.heappush(
                    self.priority_queue,
                    (
                        new_cost,
                        neighbor,
                        new_path
                    )
                )

        # Change current node to explored color
        if current != START and current != GOAL:

            self.root.after(
                300,
                lambda node=current:
                self.highlight_cell(
                    node,
                    "lightblue"
                )
            )

        # Continue search
        self.step_after_id = self.root.after(
            700,
            self.dijkstra_step
        )


    # ---------------------------------------------------------
    # Pause or resume Dijkstra
    # ---------------------------------------------------------

    def toggle_pause(self):

        if not self.running:
            return

        if self.paused:
            self.paused = False
            self.pause_button.config(text="Pause")
            self.status_label.config(text="Dijkstra Search Resumed...")
            self.dijkstra_step()
            return

        self.paused = True
        self.pause_button.config(text="Resume")
        self.status_label.config(text="Dijkstra Search Paused")

        if self.step_after_id is not None:
            self.root.after_cancel(self.step_after_id)
            self.step_after_id = None


    # ---------------------------------------------------------
    # Display Priority Queue
    # ---------------------------------------------------------

    def update_queue_display(self):
        """
        Displays the contents of the priority queue
        showing both node and accumulated cost.
        """

        queue_items = []

        for cost, node, path in sorted(
            self.priority_queue
        ):

            queue_items.append(
                f"{node}: cost {cost}"
            )

        if queue_items:

            queue_text = "\n".join(queue_items)

        else:

            queue_text = "Empty"

        self.queue_label.config(
            text=(
                "Priority Queue:\n"
                + queue_text
            )
        )


    # ---------------------------------------------------------
    # Highlight Cell
    # ---------------------------------------------------------

    def highlight_cell(self, cell, color):
        """
        Changes the color of a maze cell
        to show search progress.
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

        text_color = "white" if color in [
            "green",
            "red",
            "purple",
            "black"
        ] else "black"

        self.canvas.create_text(
            x1 + self.cell_size / 2,
            y1 + self.cell_size / 2,
            text=str(cell),
            font=("Arial", 11, "bold"),
            fill=text_color
        )


    # ---------------------------------------------------------
    # Show Final Minimum Cost Path
    # ---------------------------------------------------------

    def show_final_path(self):
        """
        Highlights the final minimum-cost path
        discovered by Dijkstra.
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
        Resets the maze and clears all
        Dijkstra search information.
        """

        if self.step_after_id is not None:
            self.root.after_cancel(self.step_after_id)
            self.step_after_id = None

        self.running = False
        self.paused = False

        self.reset_search_data()

        self.draw_maze()

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
            text="Pause",
            state="disabled"
        )


# ---------------------------------------------------------
# Start Application
# ---------------------------------------------------------

root = tk.Tk()

app = DijkstraVisualizer(root)

root.mainloop()