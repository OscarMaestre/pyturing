#!/usr/bin/python3

class InvalidInstructionError(Exception):
    pass

class Instruction(object):
    def build(self, str_sentence):
        elements_with_spaces=str_sentence.split(",")
        elements=[elem.strip() for elem in elements_with_spaces]
        
        if len(elements)!=5:
            raise InvalidInstructionError
        self.if_in_state=elements[0]
        if self.if_in_state=="":
            raise InvalidInstructionError
        self.if_head_is=elements[1]
        if self.if_head_is=="":
            raise InvalidInstructionError
        self.element_to_write=elements[2]
        if self.element_to_write=="":
            raise InvalidInstructionError
        self.move_to=elements[3].upper().strip()
        if self.move_to not in ["R", "L"]:
            raise InvalidInstructionError
        self.new_state=elements[4]
        if self.new_state=="":
            raise InvalidInstructionError

    def get_if_in_state(self):
        return self.if_in_state
    def get_if_head_is(self):
        return self.if_head_is
    def get_element_to_write(self):
        return self.element_to_write
    def get_move_to(self):
        return self.move_to
    def get_new_state(self):
        return self.new_state

    def __str__(self):
        str="{0}, {1}, {2}, {3}, {4};".format(
            self.get_if_in_state(),
            self.get_if_head_is(),
            self.get_element_to_write(),
            self.get_move_to(),
            self.get_new_state()
        )

        return str

