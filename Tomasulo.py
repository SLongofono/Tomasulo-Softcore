# @file:            Tomasulo.py
# @authors:         Stephen, Yihao

# Subclasses
from src.IntegerALU import IntegerALU
from src.ReservationStation import ReservationStation
from src.InstructionQueue import InstructionQueue
from src.ROB import ROB
from src.BranchUnit import BranchUnit
from src.MemoryUnit import MemoryUnit
from src.RAT import RAT
from src.ARF import ARF

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
            self.ARF = ARF(initVals = self.Params["RegFileInitData"] if len(self.Params["RegFileInitData"])>0 else None)
            self.RAT = RAT()

            # Instantiate RS for each type of FU with the specific size
            self.RS_ALUIs = ReservationStation(self.Params["ALUI"][0])
            self.RS_ALUFPs = ReservationStation(self.Params["ALUFP"][0])
            self.RS_MULTFPs = ReservationStation(self.Params["MULTFP"][0])


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
        self.ARF.dump()
        self.RAT.dump()
        # TODO dump memory


    def issueStage(self):
        """
        Attempts to issue the next instruction in the Instruction Queue
        """
        if not self.IQ.empty():
            if not self.ROB.isFull():
                # Peek at PC
                nextName = self.IQ.q[self.IQ.next][0]

                # Check that the relevant RS is not full
                # Fetch actual instruction
                if (nextName == "LD") or (nextName == "SD"):
                    if not self.memory.q.isFull():
                        nextInst = self.IQ.fetch()
                        # TODO Add in memory-specific issue handling here
                    return

                elif (nextName == "ADD.D") or (nextName == "SUB.D"):
                    if not self.RS_ALUFPs.isFull():
                        nextInst = self.IQ.fetch()
                    else:
                        return

                elif (nextName == "MULT.D"):
                    if not self.RS_MULTFPs.isFull():
                        nextInst = self.IQ.fetch()
                    else:
                        return

                else:
                    if not self.RS_ALUIs.isFull():
                        nextInst = self.IQ.fetch()
                    else:
                        return

                # Update operands per the RAT
                mapping = self.RAT.getMapping(nextInst[1])

                # Add the entry to the ROB
                ROBId = self.ROB.add(nextInst[0],nextInst[1][1])

                # Prepare an entry for the RS
                entry = [nextInst[0], nextInst[1][0], None, None, None, None]

                # Check if operands are ready now and update
                if mapping[1] == nextInst[1][1]:
                    entry[4] = self.ARF.get(mapping[1])
                else:
                    entry[2] = mapping[1]

                if mapping[2] == nextInst[1][2]:
                    entry[5] = self.ARF.get(mapping[2])
                else:
                    entry[3] = mapping[2]

                # Add the entry to the RS
                if(mapping[0] == "ADD.D"):
                    self.RS_ALUFPs.add(entry)
                elif(mapping[0] == "MULT.D"):
                    self.RS_MULTFPs.add(entry)
                else:
                    self.RS_ALUIs[idx].add(entry)


    def executeStage(self):
        """
        For each funcitonal unit, attempts to find an instruction which is
        ready to execute
        """

        # Enumerate a list of ready instructions
        ready_ALUIs = [x for x in self.RS_ALUIs.q if ((x[4] is not None) and (x[5] is not None))]
        ready_ALUFPs = [x for x in self.RS_ALUFPs.q if ((x[4] is not None) and (x[5] is not None))]
        ready_MULTFPs = [x for x in self.RS_MULTFPs.q if ((x[4] is not None) and (x[5] is not None))]
        #ready_LoadStore = []

        # Attempt to issue each instruction on an available unit
        print("Trying to execute ALUI instructions...")
        curPos = 0
        for i, FU in enumerate(self.ALUIs):
            if curPos >= len(ready_ALUIs):
                break
            if not FU.busy():
                FU.execute( ready_ALUIs[curPos].q[1],
                            ready_ALUIs[curPos].q[0],
                            ready_ALUIs[curPos].q[4],
                            ready_ALUIs[curPos].q[5])
                curPos += 1

        print("Trying to execute ALUFP instructions...")
        curPos = 0
        for i, FU in enumerate(self.ALUFPs):
            if curPos >= len(ready_ALUFPs):
                break
            if not FU.busy():
                FU.execute( ready_ALUFPs[curPos].q[1],
                            ready_ALUFPs[curPos].q[0],
                            ready_ALUFPs[curPos].q[4],
                            ready_ALUFPs[curPos].q[5])
                curPos += 1

        print("Trying to execute MULTFP instructions...")
        curPos = 0
        for i, FU in enumerate(self.MULTFPs):
            if curPos >= len(ready_MULTFPs):
                break
            if not FU.busy():
                FU.execute( ready_MULTFPs[curPos].q[1],
                            ready_MULTFPs[curPos].q[0],
                            ready_MULTFPs[curPos].q[4],
                            ready_MULTFPs[curPos].q[5])
                curPos += 1


    def memoryStage(self):
        """
        Cues the memory module to perform any queued LD instructions and
        update its output buffer
        """
        pass

    def writebackStage(self):
        """
        Check functional units for ready results, and pick one to write back.

        Any result written back will update reservations stations and ROB,
        potentially the ARF.
        """
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
        """
        Simple helper to print usage information for the entry class
        """
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
    myCore.runSimulation()
