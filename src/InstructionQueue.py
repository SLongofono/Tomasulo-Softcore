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
        self.next += (1 + offset)
        return [ temp2, self.instructions[temp] ]


    def empty(self):
        """
        Determines if PC has reached the end of the instruction queue.

        @return True if PC is greater than the instruction queue length, false
        otherwise
        """
        return self.next == len(self.instructions)


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
        print()


    def peek(self):
        """
        Retrieve a copy of the next instruction type and its unique ID
        """
        return (int(self.nextID), self.instructions[self.next][0])


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

