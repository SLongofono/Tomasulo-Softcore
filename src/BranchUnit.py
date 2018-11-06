# @file         BranchUnit.py
# @authors      Stephen, Yihao

class BranchUnit:
    """
    This helper class works together with the top-level Tomasulo class to
    achieve branch prediction and speculative execution.
    """

    def __init__(self, maxCopies=10):
        """
        Constructor for the BranchUnit class

        @param maxCopies An optional integer representing how many copies
        of the RAT can be stored at any given time.  This effectively limits
        how many layers of branches can be executing under speculation.

        Note that the parameter is related to the recursion depth of the
        system, as it will represent how deeply an execution path can go
        before requiring a base condition branch to be determined.
        """
        self.maxCopies = maxCopies
        # Store copies of the RAT when prompted
        self.RATs = []

        # The branch translation buffer
        self.BTB = {
            "000":True,
            "001":True,
            "010":True,
            "011":True,
            "100":True,
            "101":True,
            "110":True,
            "111":True
        }


    def int2BinStr(self, I):
        """
        Given a non-negative integer value, returns a string representing the 3
        LSBs of the binary representation of that integer.

        @param I An integer value
        @return A string of length 3 representing the lowest 3 bits of the
        binary representation of the given integer

        Note: it is assumed that the integer is positive
        """
        return f"{I:08b}"[-3:]


    def predict(self, ID):
        """
        Given an instruction ID, return the predicted target instruction ID

        @param ID An integer representing the instruciton ID of the
        branch instruction to predict
        @return True if the branch tracker predicts taken, False otherwise

        Note: To mimic the aliasing behavior of branch predictors, we convert
        the instruction IDs to bits and use only the 3 LSBs to address our
        table.  For example, the branch with ID 3 is the third word in the
        instruction queue, which corresponds to the 12th byte, which has binary
        representation "1100", so you would pass in "100" as the address.
        This scheme is prescribed by the rubric.
        """
        return self.BTB[self.int2BinStr(ID)]


    def update(self, ID, taken):
        """
        Given a branch instruction ID, finds it in the BTB and sets its
        predictor to indicate the given target ID

        @param ID An integer representing the instruction ID of the branch to
        update
        @param taken A boolean indicating if the branch was taken
        @return None
        """
        address = self.int2BinStr(ID)
        self.BTB[address] = taken


    def saveRAT(self, ID, RATdict):
        """
        Given the current cycle, the ID of a branch instruction, and a copy of
        the current RAT state, stores the state in the RATs list.

        @param cycle An integer representing the current wall time in cycles
        @param ID An integer representing the instruction ID of the branch
        instruction associated with the RAT state
        @param RATdict A dictionary representing the RAT state

        It is assumed that a copy of the RAT state is passed in rather than a
        direct reference
        """
        if len(self.RATs) < self.maxCopies:
            self.RATs.append((ID, RATdict))
            return True
        return False


    def rollBack(self, ID):
        """
        Given the instruction ID of a mis-predicted branch, retrieve the RAT
        state stored for that branch and purge any RAT states stored after it.

        @param ID An integer representing the instruction ID of the branch
        instruction entry to retrieve
        @return A tuple containing dictionary representing the RAT state just before the
        instruction passed in was encountered

        Note: Assumes that the IDs are unique and in strictly ascending order
        Note: Assumes that the branch has been stored previously
        """
        idx = 0
        for entry in self.RATs:
            if entry[0] == ID:
                break
            else:
                idx += 1

        # Destroy all state that came after the speculation
        self.RATs = self.RATs[:idx+1]

        # Return the state at the time of speculation
        return self.RATS.pop(idx)


    def dump(self):
        """
        Pretty-prints the contents of the branch unit
        """
        print(f"Branch Predictor".ljust(48, '=').rjust(80,'='))
        keys = sorted(self.BTB.keys())
        for i in range(0, len(keys), 4):
            print(f"Address {keys[i]}: {str(self.BTB[keys[i]]).ljust(5, ' ')}".ljust(20, ' '), end='')
            print(f"Address {keys[i+1]}: {str(self.BTB[keys[i+1]]).ljust(5, ' ')}".ljust(20, ' '), end='')
            print(f"Address {keys[i+2]}: {str(self.BTB[keys[i+2]]).ljust(5, ' ')}".ljust(20, ' '), end='')
            print(f"Address {keys[i+3]}: {str(self.BTB[keys[i+3]]).ljust(5, ' ')}".ljust(20, ' '))

        for key, val in self.RATS.items():
            print(f"Branch Instruction {key}:")
            print(val)
        print()


# Testing, run this script directly to execute
if __name__ == "__main__":
    myB = BranchUnit()
    IDS = [3,7,15,16,31,32]
    myB.dump()
    for i in IDS:
        myB.predict(i)
    myB.dump()
    for i in IDS:
        myB.update(i, False)
    myB.dump()

