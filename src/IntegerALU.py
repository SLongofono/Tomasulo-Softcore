# @file     IntegerALU
# @authors  Stephen

class IntegerALU:
    """
    This class implements a simple ALU for integer values.

    The class tracks what it is actively executing, and reports time since
    instantiation for debugging purposes.  The latency of each instruction is
    encoded along with the maximum output buffer size at instantiation.  This
    implies that this unit is non-pipelined.
    """


    def __init__(self, latency, bufferLen):
        """
        Constructor for the IntegerALU class

        @param latency An integer value representing the number of cycles
        required per operation
        @param bufferLen An integer value representing how many results to
        buffer on output before stalling further inputs

        """
        self.latency = latency
        self.nextFreeTime = -1
        self.time = 0
        self.activeInstruction = None
        self.result = None
        self.bufferLen = bufferLen
        self.buffer = []


    def busy(self):
        """
        Getter for the busy status of this IntegerALU

        @return True if still busy, False otherwise
        """
        return (self.time < self.nextFreeTime) and (len(self.buffer) < self.bufferLen)


    def execute(self, ID, op, a, b):
        """
        Puts the ALU in an execute state and sets the next free time

        @param op A string representing the operation to perform
        @param ID An integer representing the instruction ID this execution
        represents
        @param a An integer representing the first operand
        @param b An integer representing the second operand
        @return None

        Raises ValueError on bad operation or bad operands
        """
        self.nextFreeTime = self.time + self.latency
        self.activeInstruction = (ID, op, a, b)
        if "ADD" == op or "ADDI" == op:
            self.result = int(a + b)
        elif "SUB" == op:
            self.result = int(a - b)
        elif "BNE" == op:
            self.result = (a!=b)
        elif "BEQ" == op:
            self.result = (a==b)
        else:
            raise ValueError(f"Unknown operation [ {op} ] in integer ALU, time [ {self.time} ]")


    def isResultReady(self):
        """
        Getter determines if a result is waiting to be written back
        """
        return len(self.buffer) > 0


    def getBranchOutcome(self):
        """
        Getter returns the instruction ID of the pending branch outcome and
        whether or not the pending branch outcome is taken

        @return A tuple containing the branch intruction ID and outcome
        pending on this ALUI

        Note: Assumes you have called isBranchOutcomePending to verify that
        the next result in the output buffer is a branch
        """
        return (self.buffer[0][0], self.buffer[0][1])


    def isBranchOutcomePending(self):
        """
        Check if the next result is a branch outcome
        """
        if len(self.buffer) > 0:
            return self.buffer[0][2]
        return False


    def getResult(self):
        """
        Getter for oldest execution result

        @return A list containing the instruction ID, the result, and a
        boolean representing whether this is a branch outcome
        """
        return self.buffer.pop(0)[:-1]


    def getResultID(self):
        """
        Getter for the ID of the head of the output buffer
        """
        return self.buffer[0][0]


    def advanceTime(self):
        """
        Advances the time for this unit and propogates results to output buffer as they complete
        """
        self.time += 1
        if self.time == self.nextFreeTime:
            # If the active instruction has completed, add it to the back of
            # the output queue, and reset the tracking variables
            self.buffer.append( [self.activeInstruction[0], self.result, self.activeInstruction[1].startswith('B')] )
            self.activeInstruction = None
            self.nextFreeTime = -1


    def purgeAfterMispredict(self, BID):
        """
        Removes all currently queued and completed instructions with ID > BID

        @param BID An integer representing the instruction ID of the
        mispredicted branch
        """
        self.buffer = [ x for x in self.buffer if x[0] <= BID ]
        if self.activeInstruction is not None:
            if self.activeInstruction[0] > BID:
                self.activeInstruction = None
                self.nextFreeTime = -1



    def dump(self):
        """
        Pretty-prints the state of the ALU
        """
        print("Integer ALU".ljust(48, '=').rjust(80,'='))
        print(f"Time:\t\t\t{self.time}")
        print(f"Busy:\t\t\t{self.busy()}")
        print(f"Instruction:\t\t{self.activeInstruction}")
        print(f"Next free time:\t\t{self.nextFreeTime}")
        print("Output Buffer Contents:")
        for item in self.buffer:
            print(f"\tID:{item[0]}, Value:{item[1]}")
        print()


if __name__ == "__main__":
    t = 0
    myALU = IntegerALU(2, 3)
    print(myALU.busy)
    myALU.dump()
    myALU.execute(33, "ADD", -1, 51)
    myALU.dump()
    myALU.advanceTime()
    myALU.dump()
    print(f"Result ready?:{myALU.isResultReady()}")
    myALU.advanceTime()
    print(f"Result ready?:{myALU.isResultReady()}")
    r = myALU.getResult()
    print(r)
    myALU.dump()


    # TODO cleanup later
    # NOTE: in order to enforce that results can't be used until te cycle
    # after they finish execution, we need to try to execute first in
    # Tomasulo, and then propogate results to the CDB afterwards.
    # In the context of the FUs, this means first check if busy, then add new
    # instructions to execute, then try to pull from the output buffer.  If we
    # pull from the output buffer first, we risk not getting the CDB buffer
    # and being stuck.
    for i in range(2,11):
        myALU.dump()
        if myALU.busy():
            print(f"Time {i}: ALU busy")
        else:
            print(f"Time {i}: ALU idle")
            myALU.execute(100+i, "ADD", 100, i)
        if myALU.isResultReady() and (0 == i % 4):
            print(f"Retrieved Result {myALU.getResult()}")
        myALU.advanceTime()

