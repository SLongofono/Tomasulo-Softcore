# @file         RAT.py
# @author       Stephen

class RAT():
    """
    Models a register allocation table for Tomasulo's Algorithm

    This class exists to incorporate helper functions that make the code
    simpler in upstream classes
    """
    def __init__(self):
        """
        Constructor for the RAT class
        """
        self.names = [f"R{x}" for x in range(32)]
        self.names.extend([f"F{x}" for x in range(32)])
        self.reg = dict(zip(self.names, self.names))


    def getMapping(self, inst):
        """
        Given an instruction tuple, returns a tuple with the current mappings
        for each operand in the RAT
        """
        ret = list(inst)
        ret[2] = self.reg[ret[2]]
        ret[3] = self.reg[ret[3]]
        return tuple(ret)


    def get(self, key):
        """
        Getter for the current mapping of the given register name key

        @param key A string representing the name of the register mapping to
        get
        @return None
        """
        return self.reg[key]


    def set(self, key, value):
        """
        Setter for a register mapping

        @param key A string representing the name of the register mapping to update
        @param value A string representing the name of the register to map to
        @return None
        """
        self.reg[key] = value


    def dump(self):
        """
        Pretty-prints the RAT contents
        """
        print("RAT".ljust(40, '=').rjust(80,'='))
        keys = self.names
        for i in range(0, len(keys), 4):
            print(f"{keys[i].ljust(3,' ')}: {self.reg[keys[i]]}".ljust(20,' '), end='')
            print(f"{keys[i+1].ljust(3,' ')}: {self.reg[keys[i+1]]}".ljust(20,' '), end='')
            print(f"{keys[i+2].ljust(3,' ')}: {self.reg[keys[i+2]]}".ljust(20,' '), end='')
            print(f"{keys[i+3].ljust(3,' ')}: {self.reg[keys[i+3]]}".ljust(20,' '))
        print()

if __name__ == "__main__":
    myRAT = RAT()
    myRAT.dump()
