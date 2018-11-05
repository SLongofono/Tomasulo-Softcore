# @file             ARF.py
# @authors          Stephen


class ARF():
    """
    Models a combined floating point and integer Architectural Register File

    Modeled as a separate class so that we can enforce the read-only behavior
    of R0/F0 and so that we can convert values appropriately
    """

    def __init__(self, initVals=None):
        """
        Constructor for the ARF class

        @param initVals An optional list of tuples (string, numeric value)
        that represents the initialization values associated with the string
        name of the registers
        """
        regList = [f"R{x}" for x in range(32)]
        regList.extend([f"F{x}" for x in range(32)])
        vals = [0 for x in range(32)]
        vals.extend([0.0 for x in range(32)])
        self.reg = dict(zip(regList, vals))

        if initVals is not None:
            for a,b in initVals:
                self.reg[a] = b
        if self.reg['R0'] != 0 or self.reg['F0'] != 0.0:
            raise ValueError("Invalid register file initialization: R0, F0 must be zero")


    def get(self, key):
        """
        Getter for register entries

        @param key A string representing the register name to read from
        @return A numeric value representing the contents of the register
        """
        return self.reg[key]


    def set(self, key, value):
        """
        Setter for register entries

        @param key A string representing the register name to be set
        @param value An integer or float representing the value to set
        @return True

        Throws ValueError if key is R0 or F0, these are read-only
        Note: Silently coerces values to the appropriate type for each
        register.  For example, writing 0.1 to an integer register will result
        in int(0.1) = 0 being written.
        """
        if "R0" == key or "F0" == key:
            raise ValueError("R0 and F0 are read-only!")
        if key.startswith("F"):
            self.reg[key] = float(value)
        else:
            self.reg[key] = int(value)
        return True

    def dump(self):
        """
        Pretty-prints the contents of the ARF
        """
        print("Integer ARF".ljust(48, '=').rjust(80,'='))
        keys = [f"R{x}" for x in range(32)]
        for i in range(0,len(keys),4):
            print(f"{keys[i].ljust(3,' ')}: {self.reg[keys[i]]}".ljust(20, ' '), end='')
            print(f"{keys[i+1].ljust(3,' ')}: {self.reg[keys[i+1]]}".ljust(20, ' '), end='')
            print(f"{keys[i+2].ljust(3,' ')}: {self.reg[keys[i+2]]}".ljust(20, ' '), end='')
            print(f"{keys[i+3].ljust(3,' ')}: {self.reg[keys[i+3]]}".ljust(20, ' '))
        print()

        print("Floating Point ARF".ljust(48, '=').rjust(80,'='))
        keys = [f"F{x}" for x in range(32)]
        for i in range(0, len(keys),2):
            print(f"{keys[i].ljust(3,' ')}: {self.reg[keys[i]]:.6f}".ljust(40, ' '), end='')
            print(f"{keys[i+1].ljust(3,' ')}: {self.reg[keys[i+1]]:.6f}".ljust(40, ' '))
        print()

# Test cases, run this script directly to execute
if __name__ == "__main__":
    myVals = [
        ("R1", 13),
        ("R6", -255),
        ("R7", 2**32),
        ("R8", 2**32),
        ("R12", 2**32),
        ("R23", 2**32),
        ("R24", 2**32),
        ("R25", 2**32),
        ("R26", 2**32),
        ("F4", 11/9),
        ("F5", 3.14159),
        ("F13", 12345678.910111213),
        ("F6", 12345.67891011)
    ]
    myARF = ARF(initVals=myVals)
    myARF.dump()
    for x in range(32):
        myARF.get(f"R{x}")
        myARF.get(f"F{x}")
    for x in range(31, 0, -1):
        myARF.set(f"R{x}", 1.1);
        myARF.set(f"F{x}", 1.1);
    myARF.dump()
    try:
        myARF.set("R0", 0)
    except ValueError:
        print("R0 is read only")
    try:
        myARF.set("F0", 0.0)
    except ValueError:
        print("F0 is read only")
