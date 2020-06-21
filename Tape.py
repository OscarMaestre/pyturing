
class InvalidTapePositionError(Exception):
    pass
class InvalidTapeMovementError(Exception):
    pass

class Tape(object):
    def __init__(self):
        super().__init__()
        self.MAX_ELEMS=1000
        self.tape=list("0"*self.MAX_ELEMS)
        self.current_pos=int(self.MAX_ELEMS/2)
    def set_string(self, tape_string):
        self.tape=list(tape_string)
        self.MAX_ELEMS=len(self.tape)
        self.current_pos=0
    def get_current_pos(self):
        return self.current_pos
    def set_current_pos(self, pos):
        if pos<0:
            raise InvalidTapePositionError("Can't move head to pos<0")
        if pos>=len(self.tape):
            raise InvalidTapePositionError("Can't move head beyond end of tape")
        self.current_pos=pos
    def get_current_symbol(self):
        return self.tape[self.get_current_pos()]
    def write_symbol(self, symbol):
        self.tape[self.get_current_pos()]=symbol
    def move_left(self):
        if self.current_pos==0:
            raise InvalidTapePositionError
        self.current_pos=self.current_pos-1
    def move_right(self):
        if self.current_pos==self.MAX_ELEMS:
            raise InvalidTapePositionError
        self.current_pos=self.current_pos+1

    def move_to(self, string_to):
        if string_to=="R":
            self.move_right()
            return
        if string_to=="L":
            self.move_left()
            return
        raise InvalidTapeMovementError

    def get_tape_string(self):
        return "".join(self.tape)
    
    def __str__(self):
        left        =   self.tape[:self.current_pos]
        head        =   self.tape[self.current_pos]
        right       =   self.tape[self.current_pos+1:]
        str_left    =   "".join(left)
        str_right   =   "".join(right)
        # print("All  :"+self.get_tape_string())
        # print("Pos  :"+str(self.current_pos))
        # print("Head :"+str(head))
        # print("Left :"+str_left)
        # print("Right:"+str_right)
        str_tape    =   str_left + ">"+head+"<"+ str_right
        return str_tape