import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from random import shuffle
from pars import *
from rules import TLP, RI, RIL
from json import JSONDecodeError

class Container:
    def __init__(self, position, container_id, reshuffle_index=0, lookahead_cost=0):
        self.position = position
        self.reshuffle_index = reshuffle_index
        self.lookahead_cost = lookahead_cost
        self.id = container_id

class ContainerRelocationAuto:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("Container Relocation Simulation")
        self.setup_ui()
        self.stacks = []
        self.containers = []
        self.selected_container_index = 0
        self.current_rule = None
        self.move_count = 0
        self.wait_time = 2000

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.main_window)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tlp_canvas = tk.Canvas(self.main_frame, bg="#E6E6FA", width=800, height=500)
        self.tlp_canvas.pack(fill=tk.BOTH, expand=True)

        self.control_frame = ttk.Frame(self.main_window)
        self.control_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)

        self.status_var = tk.StringVar()
        self.status_var.set("Status: Ready")
        self.status_bar = ttk.Label(self.main_window, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Label(self.control_frame, text="Select Rule:").grid(row=0, column=0)
        self.rule_var = tk.StringVar()
        self.rule_var.set("TLP")
        self.rule_menu = ttk.OptionMenu(self.control_frame, self.rule_var, "TLP", "TLP", "RI", "RIL")
        self.rule_menu.grid(row=0, column=1)

        ttk.Label(self.control_frame, text="Tiers:").grid(row=0, column=2)
        self.tiers_entry = ttk.Entry(self.control_frame)
        self.tiers_entry.grid(row=0, column=3)
        ttk.Label(self.control_frame, text="Stacks:").grid(row=0, column=4)
        self.stacks_entry = ttk.Entry(self.control_frame)
        self.stacks_entry.grid(row=0, column=5)
        self.start_button = ttk.Button(self.control_frame, text="Start", command=self.start_simulation)
        self.start_button.grid(row=0, column=6)
        #self.next_button = ttk.Button(self.control_frame, text="Next Step", command=self.next_step)
        #self.next_button.grid(row=0, column=7)
        self.load_button = ttk.Button(self.control_frame, text="Load JSON", command=self.load_json)
        self.load_button.grid(row=0, column=8)

        self.menu_button = ttk.Button(self.control_frame, text="Main Page", command=self.go_to_main)
        self.menu_button.grid(row=0, column=10)

        self.move_count_var = tk.StringVar()
        self.move_count_var.set("Moves: 0")
        self.move_count_label = ttk.Label(self.control_frame, textvariable=self.move_count_var)
        self.move_count_label.grid(row=0, column=9)

        self.tlp_canvas.bind("<ButtonPress-1>", lambda event: self.on_click(event))

    def go_to_main(self):
        from main_page import MainPage
        self.main_window.destroy()
        root = tk.Tk()
        app = MainPage(root)
        root.mainloop()

    def start_simulation(self):
        self.move_count = 0
        try:
            tiers = int(self.tiers_entry.get())
            stacks = int(self.stacks_entry.get())
            self.stacks = self.initial_stacks(tiers, stacks)
            self.containers = [container for stack in self.stacks for container in stack]
            self.containers.sort(key=lambda c: c.position)
            self.selected_container_index = 0
            self.current_rule = self.get_selected_rule()
            self.draw_canvas()
            self.status_var.set("Status: Simulation started")
            self.next_step()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values for tiers and stacks.")

    def initial_stacks(self, tiers, stacks):
        all_containers = []
        container_id = 1
        for _ in range(stacks * tiers):
            container = Container(container_id, container_id)
            all_containers.append(container)
            container_id += 1

        shuffle(all_containers)

        stacks_list = [[] for _ in range(stacks)]
        for i, container in enumerate(all_containers):
            stack_index = i % stacks
            stacks_list[stack_index].append(container)

        return stacks_list

    def draw_canvas(self):
        self.tlp_canvas.delete("all")
        self.container_rects = {}
        container_height = 50
        container_width = 50
        bottom_margin = 20

        canvas_height = self.tlp_canvas.winfo_height()
        base_y = canvas_height - bottom_margin - container_height

        for i, stack in enumerate(self.stacks):
            for j, container in enumerate(stack):
                x1 = 50 * i + 10
                y1 = base_y - (j + 1) * container_height
                x2 = x1 + container_width
                y2 = y1 + container_height
                color = "#9400D3" if container.id == self.get_current_container_id() else "#4B0082"
                rect = self.tlp_canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=f"container_{container.id}", outline="black")
                self.tlp_canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=f"{container.position}", fill="white")
                self.container_rects[container.id] = rect

    def get_current_container_id(self):
        if self.selected_container_index < len(self.containers):
            return self.containers[self.selected_container_index].id
        return None

    def next_step(self):
        if self.selected_container_index < len(self.containers):
            container_id = self.get_current_container_id()
            container_to_remove = next((c for stack in self.stacks for c in stack if c.id == container_id), None)
            if container_to_remove:
                self.move_all_above(container_to_remove)
            else:
                self.status_var.set(f"Status: Container {container_id} not found")
        else:
            self.status_var.set(f"Status: No more containers to remove. Total Moves: {self.move_count}")

    def move_all_above(self, target_container):
        target_stack = None
        for stack in self.stacks:
            if target_container in stack:
                target_stack = stack
                break

        if not target_stack:
            return

        index = target_stack.index(target_container)
        containers_above = target_stack[index + 1:] if index + 1 < len(target_stack) else []

        self.status_var.set(f"Moving containers above {target_container.id}")
        self.main_window.update()

        if containers_above:
            container = containers_above.pop()
            best_stack_index = self.find_best_stack(exclude_stack=self.stacks.index(target_stack))
            if best_stack_index is not None:
                self.update_ui(container, best_stack_index, containers_above, target_container)
            else:
                self.status_var.set("Status: No suitable stack available")
        else:
            self.main_window.after(self.wait_time, lambda: self.remove_container(target_container))

    def update_ui(self, container, new_stack_index, containers_above, target_container):
        self.tlp_canvas.itemconfig(self.container_rects[container.id], fill="#FF0000")
        self.main_window.update()

        self.main_window.after(self.wait_time, lambda: self.move_container(container, new_stack_index, containers_above, target_container))

    def move_container(self, container, new_stack_index, containers_above, target_container):
        target_stack = next(stack for stack in self.stacks if container in stack)
        target_stack.remove(container)
        self.stacks[new_stack_index].append(container)
        self.move_count += 1
        self.move_count_var.set(f"Moves: {self.move_count}")
        self.draw_canvas()
        
        if containers_above:
            self.move_all_above(target_container)
        else:
            self.main_window.after(self.wait_time, lambda: self.remove_container(target_container))

    def remove_container(self, container):
        for stack in self.stacks:
            if container in stack:
                self.tlp_canvas.itemconfig(self.container_rects[container.id], fill="#FF0000")
                self.main_window.update()
                self.main_window.after(self.wait_time, lambda: self.finalize_removal(container, stack))
                break

    def finalize_removal(self, container, stack):
        stack.remove(container)
        self.selected_container_index += 1
        self.draw_canvas()
        self.status_var.set(f"Status: Removed container {container.id}.")
        self.main_window.after(self.wait_time, self.next_step)

    def find_best_stack(self, exclude_stack=None):
        min_size = float('inf')
        best_stack_index = None
        for i, stack in enumerate(self.stacks):
            if i != exclude_stack and len(stack) < min_size:
                min_size = len(stack)
                best_stack_index = i
        return best_stack_index

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
                self.start_simulation()
                self.status_var.set("Status: JSON file loaded successfully")
            except (FileNotFoundError, JSONDecodeError):
                messagebox.showerror("Error", "Failed to load JSON file.")

    def get_selected_rule(self):
        rule_name = self.rule_var.get()
        if rule_name == "TLP":
            return TLP
        elif rule_name == "RI":
            return RI
        elif rule_name == "RIL":
            return RIL
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = ContainerRelocationAuto(root)
    root.mainloop()
