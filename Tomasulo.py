# @file:            Tomasulo.py
# @authors:         Stephen, Yihao

from src.IntegerALU import IntegerALU
from src.ReservationStation import ReservationStation
from src.InstructionQueue import InstructionQueue
from src.ROB import ROB
from src.BranchUnit import BranchUnit
from src.MemoryUnit import MemoryUnit

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
            self.IQ = InstructionQueue(self.Params["Instructions"])

            # Instantiate ROB, RAT, ARF
            self.ROB = ROB(self.Params["ROBEntries"])

            # Instantiate RS for each type of FU
            self.RS_ALUIs = [ReservationStation(self.Params["ALUI"][0]) for i in range(self.Params["ALUI"][-1])]

            # Instantiate FUs
            # Integer ALUs
            self.ALUIs = [IntegerALU(1,1) for i in range(self.Params["ALUI"][-1])]

            # FP ALUs
            self.ALUFPs = []

            # FP Multipliers
            self.MULTFPs = []

            # Instatiate Memory
            self.memory = MemoryUnit()

            # Instantiate Branch Unit
            self.branch = BranchUnit()

            # Track retired instruction count globally
            self.numRetiredInstructions = 0

            # Track time as cycles
            self.cycle = 0

        except FileNotFoundError:
            print("ERROR: Invalid filename, please check the filename and path")
            return None


    def runSimulation(self):

        while self.numRetiredInstructions < len(self.Params["instructions"]):
            # Try to issue new instructions
            self.issueStage()

            # Try to execute ready instructions
            self.executeStage()

            # Try to write back load results
            self.memoryStage()

            # Try to write back FU results
            self.writebackStage()

            # Try to commit
            self.commitStage()

            # Advance time
            self.advanceTime()

            # Log state
            self.dump()

    def advanceTime(self):
        self.cycle += 1
        for FU in self.ALUIs:
            FU.advanceTime()
        for FU in self.ALUFPs:
            FU.advanceTime()
        for FU in self.MULTFPs:
            FU.advanceTime()

    def dump(self):
        for FU in self.ALUIs:
            FU.dump()
        for FU in self.ALUFPs:
            FU.dump()
        for FU in self.MULTFPs:
            FU.dump()

        self.ROB.dump()

        # TODO dump ARF
        # TODO dump RAT
        # TODO dump memory

    def issueStage(self):
        if not self.IQ.empty():
            if not self.ROB.isFull():
                # Peek at PC
                nextInst = self.IQ.q[self.IQ.next][0]

                # Check that at least one RS is not full
                if (nextInst == "LD") or (nextInst == "SD"):
                    idx = self.findIdleRS([self.memory.q])
                    if idx >= 0:
                        nextInst = self.IQ.fetch()

                elif (nextInst == "ADD.D") or (nextInst == "SUB.D"):
                    idx = self.findIdleRS(self.ALUFPs)
                    if idx >= 0:
                        nextInst = self.IQ.fetch()

                elif (nextInst == "MULT.D"):
                    idx = self.findIdleRS(self.MULTFPs)
                    if idx >= 0:
                        nextInst = self.IQ.fetch()

                else:
                    idx = self.findIdleRS(self.ALUIs)
                    if idx >= 0:
                        nextInst = self.IQ.fetch()


                # Fetch instruction
                # Update operands per the RAT
                # Add the entry to the ROB
                # Add the entry to the RS

    def findIdleRS(self, FUList):
        for idx, FU in enumerate(FUList):
            if not FU.busy():
                return idx
        return -1

    def executeStage(self):
        pass

    def memoryStage(self):
        pass

    def writebackStage(self):
        pass

    def commitStage(self):
        # Check if the ROB head is ready, and if so grab the result
        if self.ROB.canCommit():
            result = self.ROB.commit()

            # Check if the RAT needs to be cleared
            # Update the ARF with the result
            # Retire the instruction
            self.numRetiredInstructions += 1

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
    myCore = Tomasulo(sys.argv[1])
    myCore.dump()
