from collections import deque
import tkinter as tk
from tkinter import messagebox

from bfs_pure import find_bfs_path


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
# BFS GUI Application
# ---------------------------------------------------------

class BFSVisualizer:

    def __init__(self, root):

        self.root = root

        self.root.title("BFS Maze Visualizer")
        self.root.geometry("950x650")

        # Size of each maze cell
        self.cell_size = 80

        # BFS directions:
        # Up, Down, Left, Right
        self.directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = tk.Label(
            root,
            text="Breadth-First Search - Maze Visualizer",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        # -------------------------------------------------
        # Main frame
        # -------------------------------------------------

        main_frame = tk.Frame(root)
        main_frame.pack()

        # -------------------------------------------------
        # Canvas for drawing maze
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
        # Information panel
        # -------------------------------------------------

        info_frame = tk.Frame(
            main_frame,
            width=300
        )

        info_frame.grid(
            row=0,
            column=1,
            sticky="n"
        )

        self.status_label = tk.Label(
            info_frame,
            text="Press Start BFS",
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

        self.queue_label = tk.Label(
            info_frame,
            text="Queue: []",
            font=("Arial", 11),
            wraplength=300,
            justify="left"
        )

        self.queue_label.pack(
            pady=10
        )

        self.visited_label = tk.Label(
            info_frame,
            text="Visited Nodes: 0",
            font=("Arial", 11)
        )

        self.visited_label.pack(
            pady=5
        )

        self.cost_label = tk.Label(
            info_frame,
            text="Path Cost: -",
            font=("Arial", 12, "bold")
        )

        self.cost_label.pack(
            pady=10
        )

        # -------------------------------------------------
        # Buttons
        # -------------------------------------------------

        self.start_button = tk.Button(
            info_frame,
            text="Start BFS",
            font=("Arial", 12, "bold"),
            width=15,
            command=self.start_bfs
        )

        self.start_button.pack(
            pady=10
        )

        self.pause_button = tk.Button(
            info_frame,
            text="Pause",
            font=("Arial", 12),
            width=15,
            command=self.toggle_pause,
            state="disabled"
        )

        self.pause_button.pack(
            pady=5
        )

        self.reset_button = tk.Button(
            info_frame,
            text="Reset",
            font=("Arial", 12),
            width=15,
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
                "Light Blue = Visited\n"
                "Purple = Final Path"
            ),
            justify="left",
            font=("Arial", 11)
        )

        legend.pack(
            pady=20
        )

        # Draw initial maze
        self.draw_maze()

        # Initialize BFS variables
        self.reset_search_data()


    # ---------------------------------------------------------
    # Reset BFS internal data
    # ---------------------------------------------------------

    def reset_search_data(self):

        # Queue stores:
        # (current node, path taken to reach that node)
        self.queue = deque()

        # Store already visited nodes
        self.visited = set()

        # Store currently explored node
        self.current = None

        # Final solution path
        self.final_path = None

        # Reference path computed by the pure BFS implementation
        self.reference_path = find_bfs_path(
            GRID_ROWS,
            GRID_COLS,
            START,
            GOAL,
            OBSTACLES
        )

        # Search running status
        self.running = False
        self.paused = False
        self.step_after_id = None


    # ---------------------------------------------------------
    # Draw complete maze
    # ---------------------------------------------------------

    def draw_maze(self):

        self.canvas.delete("all")

        for r in range(GRID_ROWS):

            for c in range(GRID_COLS):

                cell = (r, c)

                x1 = c * self.cell_size
                y1 = r * self.cell_size

                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Default cell colour
                color = "white"

                # Obstacle
                if cell in OBSTACLES:
                    color = "black"

                # Start node
                elif cell == START:
                    color = "green"

                # Goal node
                elif cell == GOAL:
                    color = "red"

                # Draw rectangle
                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="gray",
                    width=2
                )

                # Display coordinate
                text_color = "white" if cell in OBSTACLES else "black"

                self.canvas.create_text(
                    x1 + self.cell_size / 2,
                    y1 + self.cell_size / 2,
                    text=f"{cell}",
                    font=("Arial", 11, "bold"),
                    fill=text_color
                )


    # ---------------------------------------------------------
    # Start BFS
    # ---------------------------------------------------------

    def start_bfs(self):

        if self.running:
            return

        # Reset everything before new search
        self.reset_search_data()

        self.draw_maze()

        # Add start node to queue
        self.queue.append(
            (START, [START])
        )

        # Mark start as visited
        self.visited.add(
            START
        )

        self.running = True
        self.paused = False

        self.status_label.config(
            text="BFS Search Started..."
        )

        self.start_button.config(
            state="disabled"
        )
        self.pause_button.config(
            text="Pause",
            state="normal"
        )

        # Start animation
        self.bfs_step()


    # ---------------------------------------------------------
    # Execute one BFS step
    # ---------------------------------------------------------

    def bfs_step(self):

        self.step_after_id = None

        if not self.running or self.paused:
            return

        # If queue becomes empty, no solution exists
        if not self.queue:

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

        # BFS removes the first item from queue
        (curr_r, curr_c), path = self.queue.popleft()

        self.current = (
            curr_r,
            curr_c
        )

        # Update GUI information
        self.current_label.config(
            text=f"Current Node: {self.current}"
        )

        self.visited_label.config(
            text=f"Visited Nodes: {len(self.visited)}"
        )

        queue_nodes = [
            item[0]
            for item in self.queue
        ]

        self.queue_label.config(
            text=f"Queue:\n{queue_nodes}"
        )

        # Show current node
        self.highlight_cell(
            self.current,
            "yellow"
        )

        self.status_label.config(
            text=f"Exploring {self.current}"
        )

        # -------------------------------------------------
        # Goal Test
        # -------------------------------------------------

        if self.current == GOAL:

            self.final_path = path

            self.running = False

            self.status_label.config(
                text="Goal Found!"
            )
            self.pause_button.config(
                state="disabled"
            )

            self.cost_label.config(
                text=f"Path Cost: {len(path) - 1}"
            )

            # Show final path after short delay
            self.root.after(
                500,
                self.show_final_path
            )

            return

        # -------------------------------------------------
        # Generate Successor Nodes
        # -------------------------------------------------

        for dr, dc in self.directions:

            nr = curr_r + dr
            nc = curr_c + dc

            neighbor = (
                nr,
                nc
            )

            # Check maze boundary
            if (
                0 <= nr < GRID_ROWS
                and 0 <= nc < GRID_COLS
            ):

                # Ignore obstacles and visited nodes
                if (
                    neighbor not in OBSTACLES
                    and neighbor not in self.visited
                ):

                    # Mark node as visited
                    self.visited.add(
                        neighbor
                    )

                    # Add node and its complete path
                    # to the BFS queue
                    self.queue.append(
                        (
                            neighbor,
                            path + [neighbor]
                        )
                    )

        # Convert previously explored node
        # to visited colour
        if (
            self.current != START
            and self.current != GOAL
        ):

            self.root.after(
                350,
                lambda node=self.current:
                self.highlight_cell(
                    node,
                    "lightblue"
                )
            )

        # Continue BFS after delay
        self.step_after_id = self.root.after(
            700,
            self.bfs_step
        )


    # ---------------------------------------------------------
    # Pause or resume BFS
    # ---------------------------------------------------------

    def toggle_pause(self):

        if not self.running:
            return

        if self.paused:
            self.paused = False
            self.pause_button.config(text="Pause")
            self.status_label.config(text="BFS Search Resumed...")
            self.bfs_step()
            return

        self.paused = True
        self.pause_button.config(text="Resume")
        self.status_label.config(text="BFS Search Paused")

        if self.step_after_id is not None:
            self.root.after_cancel(self.step_after_id)
            self.step_after_id = None


    # ---------------------------------------------------------
    # Highlight one maze cell
    # ---------------------------------------------------------

    def highlight_cell(
        self,
        cell,
        color
    ):

        r, c = cell

        x1 = c * self.cell_size
        y1 = r * self.cell_size

        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Keep start green
        if cell == START:
            color = "green"

        # Keep goal red until final path
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
            if color in ["black", "purple", "red", "green"]
            else "black"
        )

        self.canvas.create_text(
            x1 + self.cell_size / 2,
            y1 + self.cell_size / 2,
            text=f"{cell}",
            font=("Arial", 11, "bold"),
            fill=text_color
        )


    # ---------------------------------------------------------
    # Display the final shortest path
    # ---------------------------------------------------------

    def show_final_path(self):

        if not self.final_path:
            return

        for cell in self.final_path:

            # Keep start and goal their own colours
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
                "Shortest Path Found\n\n"
                f"{self.final_path}"
            )
        )

        self.start_button.config(
            state="normal"
        )


    # ---------------------------------------------------------
    # Reset GUI and search
    # ---------------------------------------------------------

    def reset(self):

        if self.step_after_id is not None:
            self.root.after_cancel(self.step_after_id)
            self.step_after_id = None

        self.running = False
        self.paused = False

        self.reset_search_data()

        self.draw_maze()

        self.status_label.config(
            text="Press Start BFS"
        )

        self.current_label.config(
            text="Current Node: None"
        )

        self.queue_label.config(
            text="Queue: []"
        )

        self.visited_label.config(
            text="Visited Nodes: 0"
        )

        self.cost_label.config(
            text="Path Cost: -"
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

if __name__ == "__main__":
    root = tk.Tk()

    app = BFSVisualizer(root)

    root.mainloop()