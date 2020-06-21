from Instruction import *

class InvalidProgramError(Exception):
    def __init__(self, str_instruction, line_no, message):
        self.str_instruction=str_instruction
        self.line_no=line_no
        super().__init__(message)
    def get_line_no(self):
        return self.line_no
    def get_invalid_instruction(self):
        return self.line_no

class InvalidInstructionPair(Exception):
    def __init__(self, message, instruction1, instruction2, line_instruction1, line_instruction2):
        self.message=message
        self.instruction1=instruction1
        self.instruction2=instruction2
        self.line_instruction1=line_instruction1
        self.line_instruction2=line_instruction2
        super().__init__(message)

    def get_line_instruction1(self):
        return self.line_instruction1

    def get_line_instruction2(self):
        return self.line_instruction2
    
    def get_instruction1(self):
        return self.instruction1
    
    def get_instruction2(self):
        return self.instruction2
    
        
    def get_invalid_instruction(self):
        return self.line_no

class StopProgram(Exception):
    pass

class Program(object):
    def __init__(self, tape):
        super().__init__()
        self.sentences=[]
        self.tape=tape
    def build(self, str_program):
        lines=str_program.split(";")
        
        self.instructions=[]
        for l in lines:
            if l=="":
                continue
            i=Instruction()
            i.build(l)
            self.instructions.append(i)
        
        self.current_state=self.instructions[0].get_if_in_state()
        self.look_for_errors_in_program()

    def check_contradictory_symbols_to_write(self, i1, i2, pos1, pos2):
        #A instruction pair like this
        # S0, 0, 1, L, S1
        # S0, 0, 0, L, S1
        # is invalid. We can't write 0 and 1 at the same time
        initial_state1=i1.get_if_in_state()
        initial_state2=i2.get_if_in_state()
        
        expected_head1=i1.get_if_head_is()
        expected_head2=i2.get_if_head_is()
        
        symbol_to_write1=i1.get_element_to_write()
        symbol_to_write2=i2.get_element_to_write()

        same_state=(initial_state1==initial_state2)
        same_head=(expected_head1==expected_head2)
        different_symbol_to_write=(symbol_to_write1!=symbol_to_write2)

        if same_state and same_head and different_symbol_to_write:
            error="Found instruction pair with contradictory symbols"
            raise InvalidInstructionPair(error, i1, i2, pos1, pos2)

    def check_contradictory_movements(self, i1, i2, pos1, pos2):
        #A instruction pair like this
        # S0, 0, 0, L, S1
        # S0, 0, 0, R, S1
        # is invalid. We can't move to L and R at the same time
        initial_state1=i1.get_if_in_state()
        initial_state2=i2.get_if_in_state()
        
        expected_head1=i1.get_if_head_is()
        expected_head2=i2.get_if_head_is()
        
        movement1=i1.get_move_to()
        movement2=i2.get_move_to()

        same_state=(initial_state1==initial_state2)
        same_head=(expected_head1==expected_head2)
        different_movements=(movement1!=movement2)

        if same_state and same_head and different_movements:
            error="Found instruction pair with contradictory movements"
            raise InvalidInstructionPair(error, i1, i2, pos1, pos2)

    def check_identical_instructions(self, i1, i2, pos1, pos2):
        #A instruction pair like this
        # S0, 0, 0, L, S1
        # S0, 0, 0, R, S1
        # is invalid. We can't move to L and R at the same time
        initial_state1=i1.get_if_in_state()
        initial_state2=i2.get_if_in_state()
        
        expected_head1=i1.get_if_head_is()
        expected_head2=i2.get_if_head_is()
        
        expected_head1=i1.get_if_head_is()
        expected_head2=i2.get_if_head_is()

        movement1=i1.get_move_to()
        movement2=i2.get_move_to()

        symbol_to_write1=i1.get_element_to_write()
        symbol_to_write2=i2.get_element_to_write()

        new_state1=i1.get_new_state()
        new_state2=i2.get_new_state()

        same_state      =   (initial_state1==initial_state2)
        same_head       =   (expected_head1==expected_head2)
        same_movements  =   (movement1==movement2)
        same_symbols    =   (symbol_to_write1==symbol_to_write2)
        same_states     =   (new_state1==new_state2)

        they_are_identical=(same_state and same_head and same_movements and same_symbols and same_states)

        if they_are_identical:
            error="Found instruction pair identical elements"
            raise InvalidInstructionPair(error, i1, i2, pos1, pos2)

    def look_for_errors_in_program(self):
        program_length=len(self.instructions)
        for pos1 in range(0, program_length):
            for pos2 in range(pos1+1, program_length):
                instruction1=self.instructions[pos1]
                instruction2=self.instructions[pos2]
                #print(str(instruction1)+"<->"+str(instruction2))
                self.check_contradictory_symbols_to_write(
                    instruction1,instruction2, pos1, pos2)
                self.check_contradictory_movements(instruction1,instruction2, pos1, pos2)
                self.check_identical_instructions(instruction1,instruction2, pos1, pos2)

        
    def run(self, max_instructions=1000, log=True):
        for num_instructions_run in range(0, max_instructions):
            tape_before=str(self.tape)
            instruction_to_run=self.get_next_instruction_to_run()
            if log:
                print()
                print("----Step  "+str(num_instructions_run)+"----------")
                print("\tTape before     :"+tape_before)
                print("\tInstruction run :"+str(instruction_to_run))
                self.execute_instruction(instruction_to_run)
                tape_after=str(self.tape)
                print("\tTape after:     :"+tape_after)
                print("----End of step : "+str(num_instructions_run)+"----------")
                print()
            



    def get_next_instruction_to_run(self):
        for pos in range(0, len(self.instructions)):
            instruction=self.instructions[pos]
            right_symbol=(instruction.get_if_head_is()==self.tape.get_current_symbol())
            right_state=(instruction.get_if_in_state()==self.current_state)
            if right_state and right_symbol:
                return instruction
        raise StopProgram

    def get_tape(self):
        return self.tape

    def get_tape_string(self):
        return self.tape.get_tape_string()

    def execute_instruction(self, instruction):
        move_to_symbol      =   instruction.get_move_to()
        symbol_to_write     =   instruction.get_element_to_write()
        
        self.tape.write_symbol(symbol_to_write)
        self.tape.move_to(move_to_symbol)
    
    def execute_next_instruction(self):
        instruction=self.get_next_instruction_to_run()
        self.execute_instruction(instruction)

        
