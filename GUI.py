import tkinter as tk
from tkinter import ttk,messagebox
import copy
from collections import deque
import heapq
import time
from dfs import * 

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry("1200x600")  # Tăng chiều rộng để chứa bảng thống kê
        self.start_state = [[1, 6,2], [5,7, 4], [8, 3, 0]]
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.current_state = copy.deepcopy(self.start_state)
        self.running = False
        self.auto_running=False
        
        self.stats = {
            "BFS": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "DFS": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "UCS": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "GBFS": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "A*": {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "IDA*": {"time": "-", "steps": "-", "cost": "-", "space": "-"},  # Thêm IDA*
            "HillClim" : {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "StochasticHillClimbing" : {"time": "-", "steps": "-", "cost": "-", "space": "-"},
            "BeamSearch" : {"time": "-", "steps": "-", "cost": "-", "space": "-"}
        }
        # Create frames
        self.start_frame = ttk.Frame(root)
        self.current_frame = ttk.Frame(root)
        self.goal_frame = ttk.Frame(root)
        self.button_frame = ttk.Frame(root)
        self.status_frame = ttk.Frame(root)
        self.control_frame = ttk.Frame(root)
        self.stats_frame = ttk.Frame(root)
        # Grid layout
        self.start_frame.grid(row=0, column=0, padx=20, pady=20)
        self.current_frame.grid(row=0, column=1, padx=20, pady=20)
        self.goal_frame.grid(row=0, column=2, padx=20, pady=20)
        self.button_frame.grid(row=1, column=0, columnspan=3, pady=10)
        self.control_frame.grid(row=2, column=0, columnspan=3, pady=10)
        self.status_frame.grid(row=3, column=0, columnspan=3, pady=10)
        self.stats_frame.grid(row=0, column=3, padx=20, pady=20, rowspan=3)  # Bên phải

        # Create grids
        self.start_entries = self.create_editable_grid(self.start_frame, self.start_state, "Start State")
        self.current_labels = self.create_grid(self.current_frame, self.current_state, "Current State")
        self.goal_labels = self.create_grid(self.goal_frame, self.goal_state, "Goal State")
        
        self.create_stats_table()

        # Create buttons
        ttk.Button(self.button_frame, text="BFS", command=lambda: self.solve(bfs,"BFS")).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="DFS", command=lambda: self.solve(dfs,"DFS")).grid(row=0, column=1, padx=5)
        ttk.Button(self.button_frame, text="UCS", command=lambda: self.solve(ucs,"UCS")).grid(row=0, column=2, padx=5)
        ttk.Button(self.button_frame, text="GBFS", command=lambda: self.solve(gbfs,"GBFS")).grid(row=0, column=3, padx=5)
        ttk.Button(self.button_frame, text="A*", command=lambda: self.solve(A_start,"A*")).grid(row=0, column=4, padx=5)
        ttk.Button(self.button_frame, text="IDA*", command=lambda: self.solve(ida_start, "IDA*")).grid(row=0, column=5, padx=5)  
        ttk.Button(self.button_frame, text="HillClim", command=lambda: self.solve(SimpleHillClimbing, "HillClim")).grid(row=2, column=0, padx=5)
        ttk.Button(self.button_frame, text="StochasticHillClimbing", command=lambda: self.solve(StochasticHillClimbing, "StochasticHillClimbing")).grid(row=2, column=1, padx=5)
        ttk.Button(self.button_frame, text="SimulatedAnnealing", command=lambda: self.solve(SimulatedAnnealing, "SimulatedAnnealing")).grid(row=2, column=2, padx=5)
        ttk.Button(self.button_frame, text="BeamSearch", command=lambda: self.solve(BeamSearch, "BeamSearch")).grid(row=2, column=3, padx=5)

        ttk.Button(self.control_frame, text="Back Step", command=self.back_step).grid(row=0, column=0, padx=5)
        ttk.Button(self.control_frame, text="Next Step", command=self.next_step).grid(row=0, column=1, padx=5)
        ttk.Button(self.control_frame, text="Auto Run", command=self.auto_run).grid(row=0, column=2, padx=5)
        ttk.Button(self.control_frame, text="Stop", command=self.stop).grid(row=0, column=3, padx=5)
        ttk.Button(self.control_frame, text="Update Start State", command=self.update_start_state).grid(row=0, column=4, padx=5)

        # Status label
        self.status_label = ttk.Label(self.status_frame, text="",font=("Arial",12))
        self.status_label.grid(row=0, column=0)


    def create_stats_table(self):
        ttk.Label(self.stats_frame, text="Algorithm Stats", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=5, pady=5)
        headers = ["Algorithm", "Time (s)", "Steps", "Cost", "Space"]
        for col, header in enumerate(headers):
            ttk.Label(self.stats_frame, text=header, font=("Arial", 12, "bold"), relief="ridge", width=10, anchor="center").grid(row=1, column=col, padx=1, pady=1)
        
        self.stats_labels = {}
        algorithms = ["BFS", "DFS", "UCS", "GBFS", "A*", "IDA*","HillClim","StochasticHillClimbing","SimulatedAnnealing","BeamSearch"]
        for row, algo in enumerate(algorithms, start=2):
            self.stats_labels[algo] = {
                "name": ttk.Label(self.stats_frame, text=algo, font=("Arial", 12), relief="ridge", width=10, anchor="center"),
                "time": ttk.Label(self.stats_frame, text="-", font=("Arial", 12), relief="ridge", width=10, anchor="center"),
                "steps": ttk.Label(self.stats_frame, text="-", font=("Arial", 12), relief="ridge", width=10, anchor="center"),
                "cost": ttk.Label(self.stats_frame, text="-", font=("Arial", 12), relief="ridge", width=10, anchor="center"),
                "space": ttk.Label(self.stats_frame, text="-", font=("Arial", 12), relief="ridge", width=10, anchor="center")
            }
            self.stats_labels[algo]["name"].grid(row=row, column=0, padx=1, pady=1)
            self.stats_labels[algo]["time"].grid(row=row, column=1, padx=1, pady=1)
            self.stats_labels[algo]["steps"].grid(row=row, column=2, padx=1, pady=1)
            self.stats_labels[algo]["cost"].grid(row=row, column=3, padx=1, pady=1)
            self.stats_labels[algo]["space"].grid(row=row, column=4, padx=1, pady=1)
    
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
    

    def create_editable_grid(self, frame, state, title):
        ttk.Label(frame, text=title, font=("Arial", 10)).grid(row=0, column=0, columnspan=3)
        entries = []
        for i in range(3):
            row = []
            for j in range(3):
                entry = ttk.Entry(frame, width=5, justify="center", font=("Arial", 14))
                entry.insert(0, str(state[i][j]) if state[i][j] != 0 else " ")
                entry.grid(row=i+1, column=j, padx=0, pady=0)
                # Gắn sự kiện phím Enter và các phím mũi tên
                entry.bind("<Return>", lambda event, x=i, y=j: self.move_to_next(x, y))
                entry.bind("<Up>", lambda event, x=i, y=j: self.move_focus(x, y, "U"))
                entry.bind("<Down>", lambda event, x=i, y=j: self.move_focus(x, y, "D"))
                entry.bind("<Left>", lambda event, x=i, y=j: self.move_focus(x, y, "L"))
                entry.bind("<Right>", lambda event, x=i, y=j: self.move_focus(x, y, "R"))
                row.append(entry)
            entries.append(row)
        # Đặt focus vào ô đầu tiên
        entries[0][0].focus_set()
        return entries
    def move_to_next(self, x, y):
        # Di chuyển focus sang ô tiếp theo khi nhấn Enter
        next_y = (y + 1) % 3
        next_x = x + (1 if next_y == 0 else 0)
        if next_x < 3:
            self.start_entries[next_x][next_y].focus_set()

    def move_focus(self, x, y, direction):
        # Di chuyển focus theo phím mũi tên
        moves = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
        dx, dy = moves[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            self.start_entries[new_x][new_y].focus_set()
    def update_start_state(self):
        try:
            # Lấy dữ liệu từ các ô nhập liệu trong Start State
            new_state = []
            for i in range(3):
                row = []
                for j in range(3):
                    value = self.start_entries[i][j].get().strip()
                    if value == "" or value == " ":
                        value = "0"
                    row.append(int(value))
                new_state.append(row)
            
            # Kiểm tra tính hợp lệ
            flat_state = [num for row in new_state for num in row]
            if sorted(flat_state) != list(range(9)):
                raise ValueError("Must contain exactly one of each number from 0-8")
            self.reset_stats()

            # Cập nhật start_state và giao diện
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
                    self.start_entries[i][j].insert(0, " ")  # Đặt lại thành rỗng
            self.start_entries[0][0].focus_set()  # Đặt focus về ô đầu tiên

    def create_grid(self, frame, state, title):
        ttk.Label(frame, text=title).grid(row=0, column=0, columnspan=3)
        labels = []
        for i in range(3):
            row = []
            for j in range(3):
                label = ttk.Label(frame, text=str(state[i][j]) if state[i][j] != 0 else " ",
                                width=5, relief="ridge", anchor="center",font=("Arial",14))
                label.grid(row=i+1, column=j, padx=0, pady=0)
                row.append(label)
            labels.append(row)
        return labels

    def update_grid(self, labels, state):
        for i in range(3):
            for j in range(3):
                labels[i][j].configure(text=str(state[i][j]) if state[i][j] != 0 else " ")

    def solve(self, algorithm,alog_name):
            self.running = True
            self.current_state = copy.deepcopy(self.start_state)
            self.current_step=0
            # do thoi gian thuc thi
            start_time = time.time()
            self.solution,self.cost,max_space =algorithm(self.start_state,self.goal_state)
            exec_time = time.time() - start_time

            self.update_grid(self.current_labels, self.current_state)
            if self.solution:
                steps = len(self.solution)
                self.update_stats(alog_name, exec_time, steps, self.cost, max_space)
                self.status_label.configure(text=f"Step: 0/{len(self.solution)} | Cost: {self.cost}")
            else:
                self.update_stats(alog_name, exec_time, "-", "-", "-")
                self.status_label.configure(text="No solution found!")
                self.status_label.configure(text="No solution found!")
                self.running = False

    def next_step(self): 
        if self.solution and self.current_step<len(self.solution): 
            self.current_state=move_black(self.current_state,self.solution[self.current_step])
            self.current_step+=1
            self.update_grid(self.current_labels,self.current_state)
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
            self.auto_running=True
            self.auto_step()

    def auto_step(self): 
        if self.auto_running and self.solution and self.current_step < len(self.solution): 
            self.next_step()
            self.root.after(1000, self.auto_step)
        else : 
            self.auto_running=False
            self.status_label.configure(text=f"Stopped at Step: {self.current_step}/{len(self.solution) if self.solution else 0} | Cost: {self.cost}")
    def stop(self):
        self.auto_running = False
        self.status_label.configure(text="Stopped")
