import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from json import JSONDecodeError
from random import randint, shuffle
from Container import Container
from pars import parse_input

class ContainerRelocationManual:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("Solving Container Relocation Manually")
        self.setup_ui()
        self.stacks_m = []
        self.cont_display_m = {}
        self.selected_cont_m = None
        self.drag_info = {"x": 0, "y": 0, "item": None, "canvas": None, "stack": None}
        self.next_to_retrieve = 1
        self.move_count = 0
        self.max_height = None
        self.retrieval_in_progress = False

    def setup_ui(self):
        self.m_frame = ttk.Frame(self.main_window)
        self.m_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5) 

        self.control_frame = ttk.Frame(self.main_window)
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)

        self.m_canvas = tk.Canvas(self.m_frame, bg="#E6E6FA", width=1000, height=400)
        self.m_canvas.pack(fill=tk.BOTH, expand=True)
        ttk.Label(self.m_frame, text="Solving Container Relocation Manually").pack()

        ttk.Label(self.control_frame, text="Tiers:").grid(row=0, column=0)
        self.tiers_entry = ttk.Entry(self.control_frame)
        self.tiers_entry.grid(row=0, column=1)
        ttk.Label(self.control_frame, text="Stacks:").grid(row=0, column=2)
        self.stacks_entry = ttk.Entry(self.control_frame)
        self.stacks_entry.grid(row=0, column=3)
        self.start_button = ttk.Button(self.control_frame, text="Start", command=self.start_simulation)
        self.start_button.grid(row=0, column=4)
        self.load_button = ttk.Button(self.control_frame, text="Load JSON", command=self.load_json)
        self.load_button.grid(row=0, column=6)

        self.auto_button = ttk.Button(self.control_frame, text="Main Page", command=self.go_to_main)
        self.auto_button.grid(row=0, column=10)

        self.move_count_var = tk.StringVar()
        self.move_count_var.set("Moves: 0")
        self.move_count_label = ttk.Label(self.control_frame, textvariable=self.move_count_var)
        self.move_count_label.grid(row=0, column=7) 

        self.status_var = tk.StringVar()
        self.status_var.set("Status: Ready")
        self.status_bar = ttk.Label(self.main_window, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.m_canvas.bind("<ButtonPress-1>", lambda event: self.on_click(event, self.m_canvas, self.stacks_m, self.cont_display_m, self.selected_cont_m))
        self.m_canvas.bind("<B1-Motion>", self.on_drag)
        self.m_canvas.bind("<ButtonRelease-1>", self.on_drop)
        self.m_canvas.bind("<Motion>", lambda event: self.on_hover(event, self.m_canvas, self.cont_display_m))

    def go_to_main(self):
        from  main_page import MainPage
        self.main_window.destroy()
        root = tk.Tk()
        app = MainPage(root)
        root.mainloop()

    def start_simulation(self):
        self.move_count = 0
        self.next_to_retrieve = 1
        self.selected_cont_m = None
        try:
            tiers = int(self.tiers_entry.get())
            stacks = int(self.stacks_entry.get())
            self.max_height = tiers + tiers // 1.5
            self.stacks_m = self.initial_stacks(tiers, stacks)
            self.simulate_relocation(tiers, stacks)
            self.status_var.set("Status: Simulation started")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values for tiers and stacks.")

    def initial_stacks(self, tiers, stacks):
        all_containers = []
        container_id = 1
        for _ in range(stacks * tiers):
            position = container_id
            reshuffle_index = randint(1, 100)
            lookahead_cost = randint(1, 10)
            container = Container(container_id, position, reshuffle_index, lookahead_cost)
            all_containers.append(container)
            container_id += 1

        shuffle(all_containers)

        stacks_list = [[] for _ in range(stacks)]
        for i, container in enumerate(all_containers):
            stack_index = i % stacks
            stacks_list[stack_index].append(container)

        return stacks_list

    def simulate_relocation(self, tiers, stacks):
        self.draw(self.m_canvas, self.stacks_m, tiers, stacks, self.cont_display_m, self.selected_cont_m)
        self.check_retrieval() 

    global container_rects
    container_rects = []
    def draw(self, canvas, stacks, tiers, stack_count, container_rects, selected_container):
        canvas.delete("all")
        container_rects.clear()

        left_x = 0
        top_y = 700 - 50 * self.max_height
        right_x = 50 * stack_count
        bottom_y = 700

        offset_x = 10
        offset_y = -10

        max_height_y = top_y + offset_y 
        canvas.create_line(left_x + offset_x, max_height_y, right_x + offset_x, max_height_y, fill="black", width=3)

        canvas.create_rectangle(left_x + offset_x, top_y + offset_y, right_x + offset_x, bottom_y + offset_y, outline="black", width=3)

        for i in range(stack_count):
            stack = stacks[i]
            for j, container in enumerate(stack):
                x1, y1 = 50 * i + offset_x, 700 - 50 * (j + 1) + offset_y
                x2, y2 = 50 * (i + 1) + offset_x, 700 - 50 * j + offset_y
                color = "#9400D3" if container == selected_container else "darkgrey"
                rect = canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                text = canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=f"{container.position}", fill="white")
                container_rects[container.id] = (rect, text)


    def relocate_containers(self):
        for stacks, selected_container in [(self.stacks_m, self.selected_cont_m)]:
            if selected_container:
                for stack in stacks:
                    if selected_container in stack:
                        while stack[-1] != selected_container:
                            top_container = stack.pop()
                            empty_stack = self.find_empty_stack(stacks)
                            if empty_stack is not None:
                                stacks[empty_stack].append(top_container)
                                self.move_count += 1 
                                self.move_count_var.set(f"Moves: {self.move_count}") 
                                self.simulate_relocation(int(self.tiers_entry.get()), int(self.stacks_entry.get()))
                                self.main_window.update_idletasks()
                                self.status_var.set(f"Status: Moving container {top_container.id}")
                                self.main_window.update_idletasks()
                                break
                            else:
                                messagebox.showerror("Error", "No available stack with enough space.")
                                return

    def find_empty_stack(self, stacks):
        for i, stack in enumerate(stacks):
            if len(stack) < self.max_height:
                return i
        return None


    def apply_rule(self, rule, stacks, canvas, container_rects, rule_type):
        selected_container = rule(stacks)
        if selected_container:
            rect, text = container_rects[selected_container.id]
            canvas.itemconfig(rect, fill="#B22222")
            if rule_type == "m":
                self.selected_cont_m = selected_container

    def delayed_remove_container(self, container, stacks, canvas, container_rects):
        canvas.after(3000, self.remove_container, container, stacks, canvas, container_rects)

    def remove_container(self, container, stacks, canvas, container_rects):
        for stack in stacks:
            if container in stack:
                stack.remove(container)
                break
        self.simulate_relocation(int(self.tiers_entry.get()), int(self.stacks_entry.get()))

    def on_click(self, event, canvas, stacks, container_rects, selected_container):
        clicked_container_id = None
        for container_id, (rect, text) in container_rects.items():
            if canvas.find_withtag(tk.CURRENT) == (rect,):
                clicked_container_id = container_id
                break

        if clicked_container_id is not None:
            for stack in stacks:
                for container in stack:
                    if container.id == clicked_container_id:
                        if container == stack[-1] and container != selected_container:
                            self.drag_info["item"] = container
                            self.drag_info["canvas"] = canvas
                            self.drag_info["stack"] = stack
                            self.drag_info["x"] = event.x
                            self.drag_info["y"] = event.y
                        return

    def on_drag(self, event):
        if self.drag_info["item"]:
            dx = event.x - self.drag_info["x"]
            dy = event.y - self.drag_info["y"]
            item_rect = self.drag_info["canvas"].find_withtag(tk.CURRENT)
            self.drag_info["canvas"].move(item_rect, dx, dy)
            self.drag_info["x"] = event.x
            self.drag_info["y"] = event.y

    def on_drop(self, event):
        if self.drag_info["item"]:
            stack_index = event.x // 50
            stacks = int(self.stacks_entry.get())
            if 0 <= stack_index < stacks:
                old_stack = self.drag_info["stack"]
                container = self.drag_info["item"]
                if len(self.stacks_m[stack_index]) < self.max_height:
                    old_stack.remove(container)
                    self.stacks_m[stack_index].append(container)
                    self.move_count += 1  
                    self.move_count_var.set(f"Moves: {self.move_count}")
                    self.simulate_relocation(self.max_height, stacks)
                else:
                    messagebox.showwarning("Warning", f"Stack {stack_index+1} is full!")
            self.drag_info = {"x": 0, "y": 0, "item": None, "canvas": None, "stack": None}
            self.check_retrieval()


    def check_retrieval(self):
        if not self.retrieval_in_progress:
            self.retrieval_in_progress = True
            self.process_next_retrieval()

    def process_next_retrieval(self):
        found = False
        for stack in self.stacks_m:
            if stack and stack[-1].id == self.next_to_retrieve:
                self.delayed_remove_container(stack[-1], self.stacks_m, self.m_canvas, self.cont_display_m)
                self.status_var.set(f"Status: Container {self.next_to_retrieve} retrieved")
                self.next_to_retrieve += 1
                found = True
                break
        
        if found:
            self.main_window.update_idletasks()
            self.main_window.after(3000, self.reset_retrieval_in_progress)
        else:
            self.retrieval_in_progress = False

    def reset_retrieval_in_progress(self):
        self.retrieval_in_progress = False
        self.check_retrieval()

    def on_hover(self, event, canvas, container_rects):
        for container_id, (rect, text) in container_rects.items():
            if canvas.find_withtag(tk.CURRENT) == (rect,):
                canvas.itemconfig(rect, fill="#32CD32")
                return
            else:
                canvas.itemconfig(rect, fill="darkgrey")

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                stacks = parse_input(file_path)
                tiers = len(stacks[0]) if stacks else 0
                self.stacks_m = stacks
                self.tiers_entry.delete(0, tk.END)
                self.tiers_entry.insert(0, str(tiers))
                self.stacks_entry.delete(0, tk.END)
                self.stacks_entry.insert(0, str(len(stacks)))
                self.simulate_relocation(tiers, len(stacks))
                self.status_var.set("Status: JSON file loaded successfully")
            except (FileNotFoundError, JSONDecodeError):
                messagebox.showerror("Error", "Failed to load JSON file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContainerRelocationManual(root)
    root.mainloop()
