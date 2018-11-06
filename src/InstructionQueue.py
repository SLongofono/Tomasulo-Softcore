# @file         InstructionQueue.py
# @authors      Stephen

class InstructionQueue:
    """
    This class models an instruction queue with an incorporated PC
    """

    def __init__(self, instructions):
        """
        Constructor for the InstructionQueue class

        @param instructions A list of tuples with relevant instruction data in
        program order
        """
        self.instructions = instructions
        self.next = 0
        self.nextID = 0


    def fetch(self, offset=0):
        """
        Gets the next instruction to execute

        @param offset An optional integer representing the offset from the
        current PC in units of instructions
        @return A list with the instruction ID, and the instruction data tuple

        This function will by default use the internal PC to determine the
        next instruction to fetch.  When a branch instruction indicates that
        the target should jump forward or back, this offset can be passed in
        to replicate that behavior.
        """
        temp = self.next + offset
        temp2 = self.nextID
        self.nextID += 1
        self.next = temp + 1
        return [ temp2, self.instructions[temp] ]


    def empty(self, offset=0):
        """
        Determines if PC has reached the end of the instruction queue.
        @param offset An optional integer representing the offset from the
        current PC to investigate.
        @return True if PC plus the offset is greater than the instruction
        queue length, false otherwise

        Note: offset is used to handle a corner case where the last
        instruction is a branch.  In this case, the branch offset can be used
        to determine if the program is truly complete or if execution will
        resume elsewhere.
        """
        return (self.next + offset >= len(self.instructions))


    def dump(self):
        """
        Pretty-prints the contents and state of the instruction queue
        """
        print("Instruction Queue".ljust(48, '=').rjust(80,'='))
        print("\tID\t\tInstruction")
        for i, entry in enumerate(self.instructions):
            if i == self.next:
                print(f"PC->\t{i}\t\t{entry}")
            else:
                print(f"\t{i}\t\t{entry}")
        if self.next >= len(self.instructions):
            print("PC->\n")
        print()


    def peek(self, offset=0):
        """
        Retrieve a copy of the next instruction type and its unique ID

        @param offset An optional integer representing the offset from the
        current PC to peek at
        """
        print(f"PEEK at next {self.next} with offset {offset}:{self.instructions[self.next + offset][0]}")
        assert(self.next + offset >= 0)
        return (int(self.nextID), self.instructions[self.next + offset][0])


if __name__ == "__main__":
    insts = [
        ("ADD", "R1", "R2", "R3"),
        ("MULT.D", "F11", "F10", "F25"),
        ("LD", "R4", 255, "R1"),
        ("ADDI", "R5", "R0", 9)
    ]
    myQ = InstructionQueue(insts)
    myQ.dump()
    myQ.fetch()
    myQ.dump()
    myQ.fetch()
    myQ.dump()
    myQ.fetch()
    myQ.dump()
    myQ.fetch(-3)
    myQ.dump()

