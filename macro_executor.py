import json
import os
import sys
import time
import keyboard
from functools import partial
from threading import Thread
from tkinter import Frame, Tk, Button


if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
    __location__ = os.path.dirname(sys.executable)
else:
    __location__ = os.path.realpath(os.path.join(os.getcwd(),
                                    os.path.dirname(__file__)))


class Macro(Thread):
    def __init__(self, name, key, delay):
        Thread.__init__(self)
        self.name = name
        self.key = key
        self.delay = delay
        self.running = False
    
    def run(self):
        print("Started macro thread: " + name)
        while True:
            self.press_if_running()
            self.wait_if_running()
    
    def press_if_running(self):
        if self.running:
            keyboard.press_and_release(self.key)

    def wait_if_running(self):
        # Makes the delay number 100 times longer but waits for a hundreth of a second each time.
        # Done to reduce time spent sleeping if it's long and we want to kill the macro early.
        if self.running:
            for i in range(self.delay * 100):
                if self.running is True:
                    time.sleep(0.01)
                else:
                    break


join_paths = os.path.join


def create_template_file(macros_dir):
    template = {
        "name": "template",
        "key": "g",
        "delay": 5
    }
    with open(join_paths(macros_dir, "template.json"), "w+") as fp:
        json.dump(template, fp, indent=4)


def change_state(macro):
    # Toggle the running state externally.
    macro.running = not macro.running
    

if __name__ == "__main__":
    macros_dir = join_paths(__location__, "macros")
    try:
        os.mkdir(macros_dir)
    except OSError:
        # Directory exists already
        pass
    
    macro_files = [fname for fname in os.listdir(macros_dir) if os.path.splitext(fname)[1] == ".json"]
    if len(macro_files) == 0:
        create_template_file(macros_dir)
        exit("No macro files found. Edit the newly placed macro file to use this program.")
    
    root = Tk()
    root.title("ME")
    root.size()
    main_frame = Frame(root)
    main_frame.pack(fill="both")
    
    macros_frame = Frame(main_frame)
    macros_frame.pack(fill="both")
    buttons = []
    macros = []
    for macro_file in macro_files:
        with open(join_paths(macros_dir, macro_file), "r") as fr:
            macro_data = json.load(fr)
            name = macro_data['name']
            key = macro_data['key']
            delay = macro_data['delay']
            macro = Macro(name, key, delay)
            macro.start()
            func = partial(change_state, macro)
            macros.append(macro)
            btn = Button(macros_frame, text=name, command=func)
            btn.pack(padx=5, pady=5, side="left")
            buttons.append(btn)
            
    root.update()
    
    # Makes width = 200 if it's less than that
    width = root.winfo_width() if root.winfo_width() > 200 else 200
    height = root.winfo_height()
    root.minsize(width, height)
    root.mainloop()
