# @file         ReservationStation.py
# @authors      Stephen

#private constants for readability
ID = 0
DEST = 1
OPERATION = 2
TAG_I = 3
TAG_J = 4
VALUE_I = 5
VALUE_J = 6
EXECUTING = 7

class ReservationStation:
    """
    This class implements a generic reservation station
    """

    def __init__(self, size, name):
        """
        Constructor for the RS class

        @param size An integer representing the maximum amount of entries for
        this reservation station
        @param name A string used to identify this RS in the dump() output
        """
        self.size = size
        self.name = name
        self.q = []


    def isFull(self):
        """
        Getter to determine if the RS can accept new entries
        """
        return len(self.q) == self.size


    def add(self, instructionID, dest, op, Qi, Qj, Vi, Vj):
        """
        Adds a new entry to the end of the RS

        @param instructionID An integer representing the unqiue instruction ID
        @param op A string representing the instruction data tuple
        @param Qi A string representing the ROB entry tag that this
        instruction's first operand will come from
        @param Qj A string representing the ROB entry tag that this
        instruction's second operand will come from
        @param Vi A numeric value representing the value of this instruction's
        first operand
        @param Vj A numeric value representing the value of this instruction's
        second operand.

        We use the convention that unknown parameters are passed as None.
        Note that it is assumed that exactly one of Qi, Vi is None and exactly
        one of Qj, Vj is None at any given time.

        Note also that since we do not wish to track which of the many FUs may
        be executing any given instruction, we include a flag at the end to
        designate those that are being executed.
        """
        self.q.append( [instructionID, dest, op, Qi, Qj, Vi, Vj, False] )


    def markAsExecuting(self, instructionID):
        """
        Marks the instruction with the given ID as executing so that it is not
        erroneously executed again.

        @param instructionID An integer representing the instruction which
        should be marked as executing
        """
        for entry in self.q:
            if entry[ID] == instructionID:
                entry[EXECUTING] = True


    def remove(self, instructionID):
        """
        Given a valid instruction ID, removes the associated entry from the RS

        @param instructionID An integer representing the unique instruction ID
        """
        for i, entry in enumerate(self.q):
            if entry[ID] == instructionID:
                self.q.pop(i)
                return True
        return False

    def purgeAfterMispredict(self, instructionID):
        """
        Given an instruction ID, removes all entries with newer instruction
        IDs (greater in value, since they are strictly increasing)

        @param instructionID An integer representing the mispredicted branch
        instruction ID
        @return None
        """
        dead = [ i for i, entry in enumerate(self.q) if entry[ID] > instructionID  ]
        self.q = [ entry for i, entry in enumerate(self.q) if not i in dead ]


    def update(self, tag, value):
        """
        Given a tag and a value, updates the value operand of any entries with
        that tag and sets the tag to None

        @param tag A string represnting the ROB entry tag to search for and
        update the value for
        @param value A numeric value used to update the associated value for
        any tags found under search of the RS

        Note that we enforce the convention that exactly one of Qi, Vj will be
        None and exactly one of Qj, Vj will be None at any given time.
        """
        for entry in self.q:
            if entry[TAG_I] == tag:
                print(f"INSTR {entry[ID]} FOUND TAG {tag}")
                entry[TAG_I] = None
                entry[VALUE_I] = value
            else:
                print(f"NO MATCH TAG {tag}")
            if entry[TAG_J] == tag:
                print(f"INSTR {entry[ID]} FOUND TAG {tag}")
                entry[TAG_J] = None
                entry[VALUE_J] = value
            else:
                print(f"NO MATCH TAG {tag}")


    def dump(self):
        """
        Pretty-prints the RS contents
        """
        print(f"RS {self.name}".ljust(48, '=').rjust(80, '='))
        print("Index\tID\tDest\tOperation\tQi\tQj\tVi\tVj")
        if len(self.q) < 1:
            print("\t[ empty ]")
	#I think here should be an else
        for idx, entry in enumerate(self.q):
            print(f"{idx}\t{entry[ID]}\t{entry[DEST]}\t{entry[OPERATION]}\t\t{entry[TAG_I]}\t{entry[TAG_J]}\t{entry[VALUE_I]}\t{entry[VALUE_J]}")
        print()


# Test cases, run this script directly to execute
if __name__ == "__main__":
    myRS = ReservationStation(5)
    myRS.dump()
    i = 0
    while not myRS.isFull():
        print("Adding entry...")
        myRS.add(i, "ADDI", f"ROB{i}", None, None, 12)
        myRS.dump()
        i += 1

    print("RS is full!")
    for j in range(i):
        idx = i - 1 - j
        print(f"Updating ROB{idx}...")
        myRS.update(f"ROB{idx}", idx+100)
        myRS.dump()

    for j in range(i):
        print(f"Removing ID {j}...")
        myRS.remove(j)
        myRS.dump()


