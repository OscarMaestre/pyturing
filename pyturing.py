#!/usr/bin/env python3

import tkinter as tk
from pyturing.Program import Program
from pyturing.Tape import Tape

test_program="""
S0, 0, 1, L, S3;
S0, 1, 0, L, S1;
S1, 0, 1, L, S3;
S1, 1, 0, L, S2;
"""
class GUI(object):
    def __init__(self, root):
        self.root=root
        
        self.program=None
        
        self.stringvartape=tk.StringVar()
        self.stringvartape.set("00000"*10)
        self.stringvarcurrentstate=tk.StringVar()

        self.buildGUI()
        self.tape=Tape()
        self.tape.set_string(self.stringvartape.get())
        self.tape.set_current_pos(10)
        self.update_tape_control()

    def buildGUI(self):
        self.control_tape=tk.Entry(master=self.root, textvariable=self.stringvartape)
        self.control_tape.grid(row=0, column=0, columnspan=12, rowspan=1, sticky="ew")


        self.control_program=tk.Text(master=self.root)
        self.control_program.grid(row=1, column=0, columnspan=9, rowspan=10, sticky="nsew")

        self.control_limit_label=tk.Label(master=self.root, text="No of instructions to run")
        self.control_limit_label.grid(row=1, column=9, sticky="ew")

        
        self.control_instruction_limit=tk.Entry(master=self.root)
        self.control_instruction_limit.grid(row=1, column=10, columnspan=2, sticky="ew")

        self.control_run_one=tk.Button(master=self.root, text="Run 1 instruction", command=self.run_one_pressed)
        self.control_run_one.grid(row=2, column=9, columnspan=3, sticky="nsew")

        self.control_run_all=tk.Button(master=self.root, text="Run all", command=self.run_all_pressed)
        self.control_run_all.grid(row=3, column=9, columnspan=3, sticky="nsew")

        self.control_label_state=tk.Label(master=self.root, text="Current state:")
        self.control_label_state.grid(row=4, column=9, columnspan=3, sticky="nsew")

        self.control_current_symbol_in_tape=tk.Label(master=self.root, text="Current symbol")
        self.control_current_symbol_in_tape.grid(row=5, column=9, columnspan=3, sticky="nswe")
        self.control_warnings=tk.Text(master=self.root)
        self.control_warnings.grid(row=7, column=9, columnspan=3, rowspan=2, sticky="nsew")


        for i in range(0, 9):
            self.root.grid_rowconfigure(i, weight=1)    
        
        for i in range(0, 12):
            self.root.grid_columnconfigure(i, weight=1)

        self.control_program.insert("0.0", test_program)

    def run_one_pressed(self):
        self.append_log("Running one")
        if self.program==None:
            program_text=self.control_program.get("1.0", tk.END)
            

            self.program=Program(self.tape)
            self.program.build(program_text)
        self.run_one_instruction()
        
            

    def highlight_next_instruction_to_run(self):
        if self.program==None:
            return
        next_instruction=self.program.get_next_instruction_to_run()
        program_text=self.control_program.get("1.0", tk.END)
        

    def run_one_instruction(self):
        
        self.program.execute_next_instruction()
        self.update_tape_control()
        self.highlight_next_instruction_to_run()
        
    def update_tape_control(self):
        tape_text=str(self.tape)
        self.stringvartape.set(tape_text)

    def run_all_pressed(self):
        print("Running all")

    def append_log(self, text):
        self.control_warnings.insert(tk.INSERT, text+"\n")


root=tk.Tk()

gui=GUI(root)
root.mainloop()