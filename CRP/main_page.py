import tkinter as tk
from tkinter import ttk
from gui import ContainerRelocationAuto
from gui2 import ContainerRelocationManual


class MainPage:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("Container Relocation Problem")

        main_frame = ttk.Frame(self.main_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title_label = ttk.Label(main_frame, text="Container Relocation Problem", font=("Arial", 18))
        title_label.pack(pady=20)

        manual_button = ttk.Button(main_frame, text="Manually Solve CRP", command=self.start_manual_crp)
        manual_button.pack(pady=10, ipadx=10, ipady=5)

        auto_button = ttk.Button(main_frame, text="Automatically Solve CRP", command=self.start_auto_crp)
        auto_button.pack(pady=10, ipadx=10, ipady=5)

        exit_button = ttk.Button(main_frame, text="Exit", command=self.main_window.quit)
        exit_button.pack(pady=10, ipadx=10, ipady=5)

    def start_manual_crp(self):
        self.main_window.destroy()
        root = tk.Tk()
        app = ContainerRelocationManual(root)
        root.mainloop()

    def start_auto_crp(self):
        self.main_window.destroy()
        root = tk.Tk()
        app = ContainerRelocationAuto(root)
        root.mainloop()

    def start_automatic_simulation(self, app):
        app.start_simulation()
        app.auto_retrieve()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainPage(root)
    root.mainloop()
