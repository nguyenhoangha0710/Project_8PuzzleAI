import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import copy
from collections import deque
import heapq
import time
import pandas as pd
import matplotlib.pyplot as plt
from dfs import *

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry("1400x600")
        self.root.configure(bg="#f0f0f0")
        self.start_state = [[1, 6, 2], [5, 7, 4], [8, 3, 0]]
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.current_state = copy.deepcopy(self.start_state)
        self.running = False
        self.auto_running = False
        self.backtracking_running = False
        
        self.stats = {
            "BFS": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "DFS": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "UCS": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "GBFS": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "A*": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "IDA*": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "HillClim": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "StochasticHC": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "SimAnneal": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "BeamSearch": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "AndOr": {"time": "-", "steps": "-", "cost": "-", "space": "-"}
        }

        # Configure ttk style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=10, font=("Helvetica", 12))
        self.style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), background="#f0f0f0")
        self.style.configure("Grid.TLabel", font=("Helvetica", 16), width=5, anchor="center", background="#ffffff", relief="groove", borderwidth=1)
        self.style.configure("Stats.TLabel", font=("Helvetica", 11), anchor="center", background="#ffffff", relief="groove", borderwidth=1)
        self.style.configure("TCombobox", font=("Helvetica", 12))

        # Create main container
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create sub-frames
        self.board_frame = ttk.Frame(self.main_frame)
        self.algo_frame = ttk.Frame(self.main_frame)
        self.control_frame = ttk.Frame(self.main_frame)
        self.stats_frame = ttk.Frame(self.main_frame)
        self.status_frame = ttk.Frame(self.main_frame)

        # Grid layout for sub-frames
        self.board_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")
        self.algo_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="n")
        self.control_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="n")
        self.stats_frame.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky="nsew")
        self.status_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Board frames (Start, Current, Goal)
        self.start_frame = ttk.LabelFrame(self.board_frame, text="Start State", padding=10)
        self.current_frame = ttk.LabelFrame(self.board_frame, text="Current State", padding=10)
        self.goal_frame = ttk.LabelFrame(self.board_frame, text="Goal State", padding=10)

        self.start_frame.grid(row=0, column=0, padx=20, pady=10)
        self.current_frame.grid(row=0, column=1, padx=20, pady=10)
        self.goal_frame.grid(row=0, column=2, padx=20, pady=10)

        # Calculate the width of the board (3 states) to set the control frame width
        self.board_width = 0
        for frame in (self.start_frame, self.current_frame, self.goal_frame):
            frame.update_idletasks()  # Ensure the frame is rendered to get its size
            self.board_width += frame.winfo_reqwidth()
        self.board_width += 40  # Add padding (20 on each side)

        # Create grids
        self.start_entries = self.create_editable_grid(self.start_frame, self.start_state)
        self.current_labels = self.create_grid(self.current_frame, self.current_state)
        self.goal_labels = self.create_grid(self.goal_frame, self.goal_state)
        
        # Create algorithm selection with Combobox
        algo_label = ttk.Label(self.algo_frame, text="Select Algorithm", style="Header.TLabel")
        algo_label.grid(row=0, column=0, columnspan=3, pady=5)

        self.algo_map = {
            "BFS": bfs, "DFS": dfs, "UCS": ucs, "GBFS": gbfs, "A*": A_start, "IDA*": ida_start,
            "HillClim": SimpleHillClimbing, "StochasticHC": StochasticHillClimbing, "SimAnneal": SimulatedAnnealing,
            "BeamSearch": BeamSearch, "AndOr": and_or_search
        }
        
        self.algo_combobox = ttk.Combobox(self.algo_frame, values=list(self.algo_map.keys()), state="readonly", width=12 , font=("Helvetica", 16))
        self.algo_combobox.grid(row=1, column=0, padx=5, pady=5)
        self.algo_combobox.set("BFS")  # Default selection
        
        ttk.Button(self.algo_frame, text="Run Algorithm", command=self.run_selected_algorithm).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.algo_frame, text="Backtracking", command=self.backtracking).grid(row=1, column=2, padx=5, pady=5)

        # Create control buttons (2 rows)
        control_label = ttk.Label(self.control_frame, text="Controls", style="Header.TLabel")
        control_label.grid(row=0, column=0, columnspan=4, pady=5)
        
        controls = [
            ("Back Step", self.back_step), ("Next Step", self.next_step), ("Auto Run", self.auto_run), ("Stop", self.stop),
            ("Update Start", self.update_start_state), ("Export", self.export_to_file), ("Plot Graph", self.plot_graph)
        ]
        # self.style.configure("Control.TButton", padding=(50,10), font=("Helvetica", 16))
        # Tạo style mới cho nút
        self.style.configure("Custom.TButton",
            borderwidth=1,
            focusthickness=3,
            focuscolor='none',
            font=("Segoe UI", 12),
            padding=6,
        )
        self.style.map("Custom.TButton",
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
        )
        for idx, (name, cmd) in enumerate(controls):
            row = 1 if idx < 4 else 2  # First 4 buttons on row 1, next 3 on row 2
            col = idx % 4
            ttk.Button(self.control_frame, text=name, command=cmd,width=100,style="Custom.TButton").grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # Configure control_frame to match the board width
        self.control_frame.grid_propagate(False)
        self.control_frame.configure(width=500,heigh=200)
        for col in range(4):
            self.control_frame.grid_columnconfigure(col, weight=1)

        # Create stats table
        self.create_stats_table()

        # Status label
        self.status_label = ttk.Label(self.status_frame, text="", font=("Helvetica", 14), background="#f0f0f0")
        self.status_label.grid(row=0, column=0, sticky="ew")

    def create_editable_grid(self, frame, state):
        entries = []
        for i in range(3):
            row = []
            for j in range(3):
                entry = ttk.Entry(frame, width=5, justify="center", font=("Helvetica", 16))
                entry.insert(0, str(state[i][j]) if state[i][j] != 0 else " ")
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.bind("<Return>", lambda event, x=i, y=j: self.move_to_next(x, y))
                entry.bind("<Up>", lambda event, x=i, y=j: self.move_focus(x, y, "U"))
                entry.bind("<Down>", lambda event, x=i, y=j: self.move_focus(x, y, "D"))
                entry.bind("<Left>", lambda event, x=i, y=j: self.move_focus(x, y, "L"))
                entry.bind("<Right>", lambda event, x=i, y=j: self.move_focus(x, y, "R"))
                row.append(entry)
            entries.append(row)
        entries[0][0].focus_set()
        return entries

    def create_grid(self, frame, state):
        labels = []
        for i in range(3):
            row = []
            for j in range(3):
                label = ttk.Label(frame, text=str(state[i][j]) if state[i][j] != 0 else " ",
                                style="Grid.TLabel")
                label.grid(row=i, column=j, padx=2, pady=2)
                row.append(label)
            labels.append(row)
        return labels

    def create_stats_table(self):
        stats_container = ttk.LabelFrame(self.stats_frame, text="Algorithm Statistics", padding=10)
        stats_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.stats_frame.columnconfigure(0, weight=1)
        self.stats_frame.rowconfigure(0, weight=1)

        headers = ["Algorithm", "Time (s)", "Steps", "Cost", "Space"]
        for col, header in enumerate(headers):
            ttk.Label(stats_container, text=header, style="Stats.TLabel", width=12).grid(row=0, column=col, padx=1, pady=1, sticky="nsew")
        
        self.stats_labels = {}
        algorithms = ["BFS", "DFS", "UCS", "GBFS", "A*", "IDA*", "HillClim", "StochasticHC", "SimAnneal", "BeamSearch", "AndOr"]
        for row, algo in enumerate(algorithms, start=1):
            self.stats_labels[algo] = {
                "name": ttk.Label(stats_container, text=algo, style="Stats.TLabel", width=12),
                "time": ttk.Label(stats_container, text="-", style="Stats.TLabel", width=12),
                "steps": ttk.Label(stats_container, text="-", style="Stats.TLabel", width=12),
                "cost": ttk.Label(stats_container, text="-", style="Stats.TLabel", width=12),
                "space": ttk.Label(stats_container, text="-", style="Stats.TLabel", width=12)
            }
            for col, (key, label) in enumerate(self.stats_labels[algo].items()):
                label.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")

    def update_stats(self, algo_name, exec_time, steps, cost, space):
        self.stats[algo_name] = {"time": f"{exec_time:.3f}", "steps": steps, "cost": cost, "space": space}
        self.stats_labels[algo_name]["time"].configure(text=self.stats[algo_name]["time"])
        self.stats_labels[algo_name]["steps"].configure(text=self.stats[algo_name]["steps"])
        self.stats_labels[algo_name]["cost"].configure(text=self.stats[algo_name]["cost"])
        self.stats_labels[algo_name]["space"].configure(text=self.stats[algo_name]["space"])

    def reset_stats(self):
        for algo in self.stats:
            self.stats[algo] = {"time": "-", "steps": "-", "cost": "-", "space": "-"}
            self.stats_labels[algo]["time"].configure(text="-")
            self.stats_labels[algo]["steps"].configure(text="-")
            self.stats_labels[algo]["cost"].configure(text="-")
            self.stats_labels[algo]["space"].configure(text="-")

    def move_to_next(self, x, y):
        next_y = (y + 1) % 3
        next_x = x + (1 if next_y == 0 else 0)
        if next_x < 3:
            self.start_entries[next_x][next_y].focus_set()

    def move_focus(self, x, y, direction):
        moves = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
        dx, dy = moves[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            self.start_entries[new_x][new_y].focus_set()

    def update_start_state(self):
        try:
            new_state = []
            for i in range(3):
                row = []
                for j in range(3):
                    value = self.start_entries[i][j].get().strip()
                    if value == "" or value == " ":
                        value = "0"
                    row.append(int(value))
                new_state.append(row)
            
            flat_state = [num for row in new_state for num in row]
            if sorted(flat_state) != list(range(9)):
                raise ValueError("Must contain exactly one of each number from 0-8")
            self.reset_stats()

            self.start_state = new_state
            self.current_state = copy.deepcopy(self.start_state)
            self.update_grid(self.current_labels, self.current_state)
            self.solution = []
            self.current_step = 0
            self.running = False
            self.auto_running = False
            self.status_label.configure(text="Start state updated")
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e) if str(e) != "" else "Please enter valid numbers (0-8)")
            for i in range(3):
                for j in range(3):
                    self.start_entries[i][j].delete(0, tk.END)
                    self.start_entries[i][j].insert(0, " ")
            self.start_entries[0][0].focus_set()

    def update_grid(self, labels, state):
        for i in range(3):
            for j in range(3):
                labels[i][j].configure(text=str(state[i][j]) if state[i][j] != 0 else " ")

    def run_selected_algorithm(self):
        if self.backtracking_running: 
            self.backtracking_running = False
            self.status_label.configure(text="Backtracking stopped")
            # self.current_state = copy.deepcopy(self.start_state)  # Reset current state
            # self.update_grid(self.current_labels, self.current_state)
        algo_name = self.algo_combobox.get()
        algorithm = self.algo_map.get(algo_name)
        if algorithm:
            self.solve(algorithm, algo_name)
        else:
            messagebox.showerror("Error", "Please select a valid algorithm!")

    def solve(self, algorithm, algo_name):
        self.running = True
        self.current_state = copy.deepcopy(self.start_state)
        self.current_step = 0
        start_time = time.time()
        self.solution, self.cost, max_space = algorithm(self.start_state, self.goal_state)
        exec_time = time.time() - start_time

        self.update_grid(self.current_labels, self.current_state)
        if self.solution:
            steps = len(self.solution)
            self.update_stats(algo_name, exec_time, steps, self.cost, max_space)
            self.status_label.configure(text=f"Step: 0/{len(self.solution)} | Cost: {self.cost}")
        else:
            self.update_stats(algo_name, exec_time, "-", "-", "-")
            self.status_label.configure(text="No solution found!")
            self.running = False

    def next_step(self):
        if self.solution and self.current_step < len(self.solution):
            next_state = move_black(self.current_state, self.solution[self.current_step])
            if next_state is not None:
                self.current_state = next_state
            else:
                print("⚠️ Invalid move, stopping.")
                return

            self.current_step += 1
            self.update_grid(self.current_labels, self.current_state)
            self.status_label.configure(text=f"Step: {self.current_step}/{len(self.solution)} | Cost: {self.cost}")

    def back_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.current_state = copy.deepcopy(self.start_state)
            for i in range(self.current_step):
                self.current_state = move_black(self.current_state, self.solution[i])
            self.update_grid(self.current_labels, self.current_state)
            self.status_label.configure(text=f"Step: {self.current_step}/{len(self.solution)} | Cost: {self.cost}")

    def auto_run(self):
        if not self.auto_running and self.solution and self.current_step < len(self.solution):
            self.auto_running = True
            self.auto_step()

    def auto_step(self):
        if self.auto_running and self.solution and self.current_step < len(self.solution):
            self.next_step()
            self.root.after(1000, self.auto_step)
        else:
            self.auto_running = False
            self.status_label.configure(text=f"Stopped at Step: {self.current_step}/{len(self.solution) if self.solution else 0} | Cost: {self.cost}")

    def stop(self):
        self.auto_running = False
        self.status_label.configure(text="Stopped")

    def backtracking(self):
        self.backtracking_running = True
        values = [1, 2, 4, 3, 7, 6, 8, 5]
        visited = set()
        path = []
        def dfs_BT(depth):
            if not self.backtracking_running:
                return False
            if len(visited) == len(values):
                return True
            for x in values:
                if not self.backtracking_running:  # Check again before proceeding
                    return False
                if x not in visited and (not path or x > path[-1]):
                    path.append(x)
                    visited.add(x)
                    grid_state = [[path[i*3 + j] if i*3 + j < len(path) else 0 for j in range(3)] for i in range(3)]
                    self.update_grid(self.current_labels, grid_state)
                    self.root.update()
                    time.sleep(0.5)
                    if dfs_BT(depth + 1):
                        return True
                    if not self.backtracking_running:
                        return False
                    path.pop()
                    visited.remove(x)
                    grid_state = [[path[i*3 + j] if i*3 + j < len(path) else 0 for j in range(3)] for i in range(3)]
                    self.update_grid(self.current_labels, grid_state)
                    self.root.update()
                    time.sleep(0.5)
            return False
        success = dfs_BT(0)
        if self.backtracking_running: 
            self.backtracking_running = False
            self.status_label.configure(text="Backtracking stopped")
            return (path, len(path)) if success else (None, -1)
        return (None, -1)

    def show_help(self):
        help_text = """
        8-Puzzle Solver Help:
        - Enter the Start State in the left grid.
        - The Goal State is fixed as [1,2,3,4,5,6,7,8,0].
        - Select an algorithm from the dropdown and click "Run Algorithm".
        - Use "Back Step" and "Next Step" to navigate through the solution.
        - "Auto Run" to automatically play the solution.
        - "Stop" to pause Auto Run or Backtracking.
        - "Update Start" to apply changes to the Start State.
        - "Export" to save the solution path to a file.
        - "Plot Graph" to visualize algorithm comparisons.
        - Shortcuts: Enter (Run), Esc (Stop), Space (Next Step).
        """
        messagebox.showinfo("Help", help_text)

    def plot_graph(self):
        try:
            data = []
            for algo, stats in self.stats.items():
                if stats["steps"] != "-":
                    data.append({
                        "Algorithm": algo,
                        "Time (s)": float(stats["time"]),
                        "Steps": int(stats["steps"]),
                        "Cost": int(stats["cost"]),
                        "Space": int(stats["space"])
                    })
            if not data:
                messagebox.showerror("Error", "No valid data to plot!")
                return

            df = pd.DataFrame(data)
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle("Algorithm Comparison", fontsize=16)

            axes[0, 0].bar(df["Algorithm"], df["Time (s)"], color="skyblue")
            axes[0, 0].set_title("Execution Time")
            axes[0, 0].set_ylabel("Time (s)")
            axes[0, 0].tick_params(axis='x', rotation=45)

            axes[0, 1].bar(df["Algorithm"], df["Steps"], color="lightgreen")
            axes[0, 1].set_title("Steps")
            axes[0, 1].set_ylabel("Steps")
            axes[0, 1].tick_params(axis='x', rotation=45)

            axes[1, 0].bar(df["Algorithm"], df["Cost"], color="orange")
            axes[1, 0].set_title("Cost")
            axes[1, 0].set_ylabel("Cost")
            axes[1, 0].tick_params(axis='x', rotation=45)

            axes[1, 1].bar(df["Algorithm"], df["Space"], color="purple")
            axes[1, 1].set_title("Space")
            axes[1, 1].set_ylabel("Space")
            axes[1, 1].tick_params(axis='x', rotation=45)

            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.savefig('algorithm_comparison.png')
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    def export_to_file(self):
        try:
            # Check if there is a solution to export
            if not self.solution:
                messagebox.showerror("Error", "No solution available! Please run an algorithm first.")
                return

            # Get the algorithm name for the file name
            algo_name = self.algo_combobox.get()

            # Create the path data
            path_data = []
            current_state = copy.deepcopy(self.start_state)
            action_map = {"U": "Up", "R": "Right", "D": "Down", "L": "Left"}

            # Add the initial state (Step 0)
            flat_state = ",".join(str(num) for row in current_state for num in row)
            path_data.append({
                "Step": 0,
                "Action": "Start",
                "State": flat_state
            })

            # Generate each step in the path
            for step, action in enumerate(self.solution, 1):
                current_state = move_black(current_state, action)
                if current_state is None:
                    messagebox.showerror("Error", f"Invalid move at step {step}: {action}")
                    return
                flat_state = ",".join(str(num) for row in current_state for num in row)
                path_data.append({
                    "Step": step,
                    "Action": action_map.get(action, action),
                    "State": flat_state
                })

            # Create DataFrame
            df = pd.DataFrame(path_data)

            # Export to Excel with the algorithm name as the default file name
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                initialfile=f"{algo_name}.xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )

            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Export Successful", f"Solution path exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"An error occurred: {str(e)}")
if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()