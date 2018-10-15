# @file:            tomasulo.py
# @authors:         Stephen, Yihao

class Tomasulo:
    """
    This class implements the top-level object for the Tomasulo core.

    Given a valid input, the object will be ready to run after instantiation.  Call the runSimulation() method to initiate the simulations.

    @input inputFileName A string representing the full path to the desired input file for simulation.
    @return A valid Tomasulo object with the characteristics described in the input file.  Returns None and throws exceptions if the initiation fails.

    Usage:
    myTomasuloObject = Tomasulo(myInputFileName)
    """

    def __init__(self, inputFileName):
        print("Initialization")
        try:
            from src.helpers import getParameters

            # Validate input and parse instance parameters
            self.Params = getParameters(inputFileName)

            print(self.Params)

            # Instantiate Instruction Queue
            # Instantiate ROB, RS, RAT, ARF
            # Instantiate FUs
            # Instatiate Memory

        except FileNotFoundError:
            print("ERROR: Invalid filename, please check the filename and path")
            return None


    def runSimulation(self):
        pass

    def issueStage(self):
        pass

    def executeStage(self):
        pass

    def memoryStage(self):
        pass

    def writebackStage(self):
        pass

    def commitStage(self):
        pass

    def usage():
        print("\nUsage:")
        print("\n\t$ python3 Tomasulo.py <testFilePath>\n")

# End Class Tomasulo


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("No imput file provided!")
        Tomasulo.usage()
        sys.exit(1)
    myTCore = Tomasulo(sys.argv[1])


