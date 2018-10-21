# @file         ROB.py
# @author       Stephen, Yihao

# Local constants to improve readability/debugging
ID = 0
DEST = 1
VALUE = 2
DONEFLAG = 3

class ROB():
    """
    This data type class represents the reorder buffer.

    The class is a wrapper around the standard list type.  It implements
    tracking the head and tail along with the search-and-replace mechanism
    for updating tags with values as they arrive on the CDB.  Note that we
    enforce ordering by our head and tail counters.

    The internal data structure is a list of this format:
    [< instr. ID>, <ARF destination>, <value>, <complete flag>, <stale flag>]

    In order to avoid complications with the circular queue, we initialize with
    a dummy entry marked as stale.
    """
    def __init__(self,size):
        if size < 1:
            raise IndexError(f"ROB initialized with invalid size {size}")
        self.q = [ [-1, "", None, True] for x in range(size)]
        self.size = size
        self.head = 0
        self.tail = 0


    def isFull(self):
        """
        Determines if the ROB is full.

        In this case, full means the head and tail both point to an instruction
        which is not complete.
        """
        return self.head == self.tail and not self.q[self.head][DONEFLAG]


    def findAndUpdateEntry(self, entryID, value):
        """
        Searches the ROB entries for the instruction with the given ID, updates
        its value, and marks it as complete.

        @param entryID An integer representing the instruction entry to find
        @param value An integer or floating point value to populate
        @return True if found and successful, False otherwise
        """

        foundMatch = False
        for entry in self.q:
            if entry[ID] == entryID:
                entry[VALUE] = value
                entry[DONEFLAG] = True
                foundMatch = True
                break

        return foundMatch


    def add(self, entryID, destination):
        """
        Adds an entry to the ROB given an instruction ID and destination
        register.

        @param entryID An integer representing the instruction ID
        @param destination A string representing the destination register in
        the ARF
        @return A string representing the name of the ROB entry created

        Raises IndexError exception if the ROB is considered full

        """
        if self.isFull():
            raise IndexError("The ROB is full!")
        else:
            self.q[self.tail] = [entryID, destination, None, False]
            ret = f"ROB{self.tail}"
            self.tail += 1
            if self.tail == self.size:
                self.tail = 0
            return ret


    def canCommit(self):
        """
        Determines if the oldest instruction is complete and ready to commit
        """
        return self.q[self.head][DONEFLAG] and self.head != self.tail


    def commit(self):
        """
        Retrieve the head of the ROB and advance the head beyond it.

        @return A copy of the ROB entry as a tuple: (ID, destination, value,
        doneflag)
        """
        retVal = self.q[self.head].copy()

        self.head += 1
        if self.head == self.size:
            self.head = 0

        return retVal


    def dump(self):
        """
        Pretty-prints the ROB contents
        """
        print("ROB".ljust(38, '=').rjust(80,'='))
        for i in range(len(self.q)):
            if self.head == i and self.tail == i:
                prefix = "head/tail->"
            elif self.head == i:
                prefix = "head------>"
            elif self.tail == i:
                prefix = "tail------>"
            else:
                prefix = "           "
            print(prefix, self.q[i])
        print()

# Test cases, run this script directly to execute
if __name__ == "__main__":

    # Testing ROB unit
    myRob = ROB(1)
    myRob.dump()
    myRob.add(11, "R1")
    myRob.dump()
    del myRob

    myRob = ROB(5)
    print(myRob.size)
    myRob.dump()
    print("Adding an entry into ", myRob.add(1, "R1"))
    print("Adding an entry into ", myRob.add(2, "R2"))
    print("Adding an entry into ", myRob.add(3, "R3"))
    myRob.dump()
    if myRob.isFull():
        raise Exception('WTF')
    else:
        if myRob.canCommit():
            raise Exception('WTF2')
        else:
            myRob.findAndUpdateEntry(1, 1001)
    myRob.dump()
    print(myRob.findAndUpdateEntry(2, 2002))
    myRob.dump()
    print(myRob.findAndUpdateEntry(3, 3003))
    myRob.dump()
    while(myRob.canCommit()):
        myRob.commit()
        myRob.dump()


