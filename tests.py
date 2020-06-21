#!/usr/bin/python3

import unittest
import os.path
from pyturing.Program import *
from pyturing.Instruction import *
from pyturing.Tape import *


class TestInstruction(unittest.TestCase):
    def test_num_elements(self):
        str_instruction="S0, 0, 1, L, S4"
        instruction=Instruction()
        instruction.build(str_instruction)
        self.assertEqual(instruction.get_if_in_state(), "S0")
        self.assertEqual(instruction.get_if_head_is(), "0")
        self.assertEqual(instruction.get_element_to_write(), "1")
        self.assertEqual(instruction.get_new_state(), "S4")
    
    def test_num_elements_with_spaces(self):
        str_instruction="S0, 1, 0,    R       ,S1"
        instruction=Instruction()
        instruction.build(str_instruction)
        self.assertEqual(instruction.get_if_in_state(), "S0")
        self.assertEqual(instruction.get_if_head_is(), "1")
        self.assertEqual(instruction.get_element_to_write(), "0")
        self.assertEqual(instruction.get_move_to(), "R")
        self.assertEqual(instruction.get_new_state(), "S1")
    
    def test_exception_1(self):
        str_instruction1="S0, 1, 0     R      ,L"
        instruction=Instruction()
        with self.assertRaises(InvalidInstructionError):
            instruction.build(str_instruction1)
    
    def test_exception_2(self):
        str_instruction2="S0, 1, 0           ,"
        instruction=Instruction()
        with self.assertRaises(InvalidInstructionError):
            instruction.build(str_instruction2)
    
    def test_exception_3(self):
        str_instruction3="S0, 1,            ,S0"
        instruction=Instruction()
        with self.assertRaises(InvalidInstructionError):
            instruction.build(str_instruction3)
    
    def test_exception_4(self):
        str_instruction3="S0, ,            ,S0"
        instruction=Instruction()
        with self.assertRaises(InvalidInstructionError):
            instruction.build(str_instruction3)


    def test_tape1(self):
        tape=Tape()
        tape.set_string("0101")
        str_tape=str(tape)
        self.assertEqual(">0<101", str_tape)
    
    def test_tape_with_move_right(self):
        tape=Tape()
        tape.set_string("0101")
        tape.move_right()
        str_tape=str(tape)
        self.assertEqual("0>1<01", str_tape)

    def test_tape_with_move_left(self):
        tape=Tape()
        tape.set_string("0101")
        tape.set_current_pos(3)
        tape.move_left()
        str_tape=str(tape)
        self.assertEqual("01>0<1", str_tape)

    def test_program1(self):
        tape=Tape()
        tape.set_string("0101")
        str_program="S0, 0, 1, R, S0;S0, 1, 0, L, S0"
        program=Program(tape)
        program.build(str_program)
        program.execute_next_instruction()
        
        self.assertEqual(program.get_tape_string(), "1101")

        program.execute_next_instruction()
        self.assertEqual(program.get_tape_string(), "1001")
        
        with self.assertRaises(InvalidTapePositionError):
            program.execute_next_instruction()

    def test_program_error_different_symbols_to_write(self):
        tape=Tape()
        tape.set_string("0101")
        str_program="S0, 0, 1, R, S0;S0, 0, 0, L, S0"
        with self.assertRaises(InvalidInstructionPair):
            program=Program(tape)
            program.build(str_program)

    def test_program_error_different_movements(self):
        tape=Tape()
        tape.set_string("0101")
        str_program="S0, 0, 1, R, S0;S0, 0, 1, L, S0"
        with self.assertRaises(InvalidInstructionPair):
            program=Program(tape)
            program.build(str_program)

    def test_program_error_identical_instructions(self):
        tape=Tape()
        tape.set_string("0101")
        str_program="S0, 0, 1, R, S0;S1, 0, 1, L, S0;S0, 0, 1, R, S0"
        trozos=str_program.split(";")
        
        with self.assertRaises(InvalidInstructionPair):
            program=Program(tape)
            program.build(str_program)

    def test_program_with_log1(self):
        tape=Tape()
        tape.set_string("0101")
        str_program="S0, 0, 1, R, S0;S0, 1, 0, L, S2"
        program=Program(tape)
        program.build(str_program)
        with self.assertRaises(StopProgram):    
            program.run(log=False)

    def test_load_external_program(self):
        filepath=os.path.join("examples", "increment_number.txt")
        tape=Tape()
        tape.set_string("000111")
        for i in range(0, 5):
            tape.move_right()
        program=Program(tape)
        program.load_file_program(filepath)
        program.run()


    
if __name__ == "__main__":
    unittest.main()