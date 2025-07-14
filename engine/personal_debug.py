import pygame
import pygame_gui
import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, messagebox

class P_Debug:
    def __init__(self):
        self.outputs = []         #0
        self.engine_bugs = []     #1
        self.slot1 = []           #2
        self.slot2 = []           #3
        self.slot3 = []           #4
        self.slot4 = []           #5

    def view_output(self,num):
        if num == 0:
            print(self.outputs)
        elif num ==9:
            print(self.engine_bugs)
        elif num == 1:
            print(self.slot1)
        elif num == 2:
            print(self.slot2)
        elif num == 3:
            print(self.slot3)
        elif num == 4:
            print(self.slot4)
        else:
            print("Invalid slot number")
   
    def add_engine_bug(self, bug):
        self.engine_bugs.append(bug)

    def add_slot1(self, item):
        self.slot1.append(item)

    def add_slot2(self, item):
        self.slot2.append(item)

    def add_slot3(self, item):
        self.slot3.append(item)

    def add_slot4(self, item):
        self.slot4.append(item)

    def clear_outputs(self):
        self.outputs.clear()

    def clear_engine_bugs(self):
        self.engine_bugs.clear()

    def clear_all_slots(self):
        self.slot1.clear()
        self.slot2.clear()
        self.slot3.clear()
        self.slot4.clear()

    def run_gui_terminal(self):

        pygame.init()
        pygame.display.set_caption('P_Debug Live Terminal')
        window_size = (600, 400)
        window_surface = pygame.display.set_mode(window_size)

        manager = pygame_gui.UIManager(window_size)

        output_box = pygame_gui.elements.UITextBox(
            html_text='Welcome to P_Debug Terminal!',
            relative_rect=pygame.Rect((10, 10), (580, 300)),
            manager=manager
        )

        input_line = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 320), (480, 30)),
            manager=manager
        )

        send_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 320), (90, 30)),
            text='Send',
            manager=manager
        )

        clock = pygame.time.Clock()
        is_running = True

        def append_output(text):
            current = output_box.html_text
            output_box.set_text(current + '<br>' + text)

        while is_running:
            time_delta = clock.tick(30) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == send_button:
                        cmd = input_line.get_text()
                        input_line.set_text('')
                        append_output(f"> {cmd}")
                        try:
                            if cmd.startswith("view "):
                                num = int(cmd.split()[1])
                                if num == 0:
                                    append_output(str(self.outputs))
                                elif num == 9:
                                    append_output(str(self.engine_bugs))
                                elif num == 1:
                                    append_output(str(self.slot1))
                                elif num == 2:
                                    append_output(str(self.slot2))
                                elif num == 3:
                                    append_output(str(self.slot3))
                                elif num == 4:
                                    append_output(str(self.slot4))
                                else:
                                    append_output("Invalid slot number")
                            elif cmd.startswith("addbug "):
                                bug = cmd[7:]
                                self.add_engine_bug(bug)
                                append_output(f"Added bug: {bug}")
                            elif cmd.startswith("add1 "):
                                item = cmd[5:]
                                self.add_slot1(item)
                                append_output(f"Added to slot1: {item}")
                            elif cmd.startswith("add2 "):
                                item = cmd[5:]
                                self.add_slot2(item)
                                append_output(f"Added to slot2: {item}")
                            elif cmd.startswith("add3 "):
                                item = cmd[5:]
                                self.add_slot3(item)
                                append_output(f"Added to slot3: {item}")
                            elif cmd.startswith("add4 "):
                                item = cmd[5:]
                                self.add_slot4(item)
                                append_output(f"Added to slot4: {item}")
                            elif cmd == "clear outputs":
                                self.clear_outputs()
                                append_output("Outputs cleared.")
                            elif cmd == "clear bugs":
                                self.clear_engine_bugs()
                                append_output("Engine bugs cleared.")
                            elif cmd == "clear slots":
                                self.clear_all_slots()
                                append_output("All slots cleared.")
                            elif cmd == "help":
                                append_output("Commands: view [0-4,9], addbug <msg>, add1/2/3/4 <item>, clear outputs, clear bugs, clear slots, help")
                            else:
                                append_output("Unknown command. Type 'help'.")
                        except Exception as e:
                            append_output(f"Error: {e}")

                manager.process_events(event)

            manager.update(time_delta)
            window_surface.fill((30, 30, 30))
            manager.draw_ui(window_surface)
            pygame.display.update()

        pygame.quit()
    def run_tk_terminal(self):
        root = tk.Tk()
        root.title("P_Debug Slot Viewer")
        root.geometry("700x500")

        tab_control = ttk.Notebook(root)

        slots = [
            ("Outputs", self.outputs),
            ("Slot1", self.slot1),
            ("Slot2", self.slot2),
            ("Slot3", self.slot3),
            ("Slot4", self.slot4),
            ("Engine Bugs", self.engine_bugs)
        ]
        text_widgets = {}

        def refresh_tab(name, data):
            text_widgets[name].config(state='normal')
            text_widgets[name].delete(1.0, tk.END)
            for idx, item in enumerate(data):
                text_widgets[name].insert(tk.END, f"{idx+1}: {item}\n")
            text_widgets[name].config(state='disabled')

        def add_item(slot_name, slot_list):
            item = simpledialog.askstring("Add Item", f"Enter item for {slot_name}:")
            if item:
                slot_list.append(item)
                refresh_tab(slot_name, slot_list)

        def clear_slot(slot_name, slot_list):
            if messagebox.askyesno("Clear", f"Clear all items in {slot_name}?"):
                slot_list.clear()
                refresh_tab(slot_name, slot_list)

        for name, data in slots:
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=name)
            frame = ttk.Frame(tab)
            frame.pack(fill='both', expand=True, padx=10, pady=10)

            text = scrolledtext.ScrolledText(frame, height=20, state='disabled')
            text.pack(fill='both', expand=True, side='left')
            text_widgets[name] = text

            btn_frame = ttk.Frame(frame)
            btn_frame.pack(side='right', fill='y', padx=5)

            if name != "Outputs":
                add_btn = ttk.Button(btn_frame, text="Add", command=lambda n=name, d=data: add_item(n, d))
                add_btn.pack(pady=2, fill='x')
                clear_btn = ttk.Button(btn_frame, text="Clear", command=lambda n=name, d=data: clear_slot(n, d))
                clear_btn.pack(pady=2, fill='x')
            else:
                clear_btn = ttk.Button(btn_frame, text="Clear", command=lambda n=name, d=data: clear_slot(n, d))
                clear_btn.pack(pady=2, fill='x')

            refresh_tab(name, data)

        def refresh_all():
            for name, data in slots:
                refresh_tab(name, data)

        menu = tk.Menu(root)
        root.config(menu=menu)
        menu.add_command(label="Refresh All", command=refresh_all)
        menu.add_command(label="Help", command=lambda: messagebox.showinfo("Help",
            "Each tab shows a slot.\nUse Add/Clear buttons to manage items.\nUse Refresh All to update all tabs."))

        tab_control.pack(expand=1, fill='both')
        root.mainloop()

main_debugger_gui_manger = P_Debug()
