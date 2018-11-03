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
            self.Params["InputFile"] = inputFileName

            print(self.Params)

            # Track completion record for output
            self.output = {}

             # Instantiate Instruction Queue
            self.IQ = InstructionQueue(self.Params["Instructions"])
            for i in range(len(self.Params["Instructions"])):
                self.output[i] = [None, None, None, None, None]

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

            # FP ALUs TODO
            self.ALUFPs = []

            # FP Multipliers TODO
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
        """
        Begins the simulation defined by the input file provided at instantiation
        """
        print("Beginning Simulation")

        while self.numRetiredInstructions < len(self.Params["Instructions"]):
            # Try to issue new instructions
            self.issueStage()
            print(self.output)

            # Try to execute ready instructions
            self.executeStage()
            print(self.output)

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

            if(self.cycle == 4):
                break
        self.writeOutput()

        print("Simulation Complete")


    def advanceTime(self):
        """
        Increment the wall time for the system clock and all helper classes
        """
        self.cycle += 1
        for FU in self.ALUIs:
            FU.advanceTime()
        for FU in self.ALUFPs:
            FU.advanceTime()
        for FU in self.MULTFPs:
            FU.advanceTime()


    def updateOutput(self, ID, stage):
        """
        Fills in the current time for the given instruction ID in the given
        output stage

        @param ID An integer representing the instruction to be updated
        @param stage An integer representing the stage to be set to the current
        cycle time
        @return None
        """
        # We store Issue, execute, memory, writeback, commit
        self.output[ID][stage] = self.cycle


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


    def writeOutput(self):
        """
        Write the output file of the results
        """
        fileName = self.Params["InputFile"]
        fileName = fileName[:fileName.find('.')]
        fileName = fileName + "_output.txt"

        with open(fileName, 'w') as outFile:
            # Write the instruction stage tracking
            outFile.write("Instruction Completion Table".ljust(35,'=').rjust(80,'='))
            outFile.write("\n\rID\t IS\t EX\t MEM\t WB\t COM\n\r")
            for inst, stages in self.output.items():
                outFile.write(f"{inst}\t {stages[0]}\t {stages[1]}\t {stages[2]}\t {stages[3]}\t {stages[4]}\n\r")

            # Write the register file
            # write the nonzero sections of memory


    def isTooNew(self, ID):
        """
        Checks if the given instruction has just reached a new stage.

        @param ID An integer representing the instruction ID to check
        @return True if the instruction reached its last non-None stage in
        this cycle, False otherwise.

        This is used to prevent an instruction from executing in the same stage
        in which it was issued.
        """
        # find most recent stage
        stage = 0
        for s in self.output[ID]:
            if s is not None:
                stage = s
            else:
                break
        return stage == self.cycle


    def issueStage(self):
        """
        Attempts to issue the next instruction in the Instruction Queue
        """
        if not self.IQ.empty():
            if not self.ROB.isFull():
                # Peek at PC
                nextName = self.IQ.instructions[self.IQ.next][0]

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
                print(nextInst)
                mapping = self.RAT.getMapping(nextInst[1])
                print("Mapping: ", mapping)

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
                    self.RS_ALUFPs.add(*entry)
                elif(mapping[0] == "MULT.D"):
                    self.RS_MULTFPs.add(*entry)
                else:
                    self.RS_ALUIs.add(*entry)

                # Log the issue in the output dictionary
                self.updateOutput(nextInst[0], 0)


    def executeStage(self):
        """
        For each funcitonal unit, attempts to find an instruction which is
        ready to execute
        """

        # Enumerate a list of ready instructions
        ready_ALUIs = [x for x in self.RS_ALUIs.q if ( (x[4] is not None) and
                                                       (x[5] is not None) and
                                                       (not self.isTooNew(x[0])))]
        ready_ALUFPs = [x for x in self.RS_ALUFPs.q if ( (x[4] is not None) and
                                                         (x[5] is not None) and
                                                         (not self.isTooNew(x[0])))]
        ready_MULTFPs = [x for x in self.RS_MULTFPs.q if ( (x[4] is not None) and
                                                           (x[5] is not None) and
                                                           (not self.isTooNew(x[0])))]
        #ready_LoadStore = []

        # Mark executed instructions for cleanup
        toRemove = []

        # Attempt to issue each instruction on an available unit
        print("Trying to execute ALUI instructions...")
        curPos = 0
        for i, FU in enumerate(self.ALUIs):
            if curPos >= len(ready_ALUIs):
                break
            if not FU.busy():
                FU.execute( ready_ALUIs[curPos][0],
                            ready_ALUIs[curPos][1],
                            ready_ALUIs[curPos][4],
                            ready_ALUIs[curPos][5])
                self.updateOutput(ready_ALUIs[curPos][0], 1)
                toRemove.append(ready_ALUIs[curPos][0])
                curPos += 1

        # TODO uncomment once these classes are done
        #print("Trying to execute ALUFP instructions...")
        #curPos = 0
        #for i, FU in enumerate(self.ALUFPs):
        #    if curPos >= len(ready_ALUFPs):
        #        break
        #    if not FU.busy():
        #        FU.execute( ready_ALUFPs[curPos].q[0],
        #                    ready_ALUFPs[curPos].q[1],
        #                    ready_ALUFPs[curPos].q[4],
        #                    ready_ALUFPs[curPos].q[5])
        #        self.updateOutput(ready_ALUFPs[curPos].q[0], 1)
        #        toRemove.append(ready_ALUIs[curPos][0])
        #        curPos += 1

        # TODO uncomment once these classes are done
        #print("Trying to execute MULTFP instructions...")
        #curPos = 0
        #for i, FU in enumerate(self.MULTFPs):
        #    if curPos >= len(ready_MULTFPs):
        #        break
        #    if not FU.busy():
        #        FU.execute( ready_MULTFPs[curPos].q[0],
        #                    ready_MULTFPs[curPos].q[1],
        #                    ready_MULTFPs[curPos].q[4],
        #                    ready_MULTFPs[curPos].q[5])
        #        self.updateOutput(ready_MULTFPs[curPos].q[0], 1)
        #        toRemove.append(ready_ALUIs[curPos][0])
        #        curPos += 1

        for item in toRemove:
            # Don't check, just blindly call since IDs are unique
            self.RS_ALUIs.remove(item)
            # TODO uncomment once these classes are done
            #self.RS_ALUFPs.remove(item)
            #self.RS_MULTFP.remove(item)


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
        # Check if there are results ready, track the oldest ID seen (the
        # smallest ID number)
        winningFU = None
        oldestInst = 2**30
        for FU in self.ALUIs:
            if FU.isResultReady():
                temp = FU.getResultID()
                if temp < oldestInst:
                    oldestInst = temp
                    winningFU = FU

        # TODO add in same check over the ALUFPs, MULTFPs

        if winningFU is not None:
            # Fetch Result
            result = winningFU.getResult()

            # Update ROB results
            dest = self.ROB.findAndUpdateEntry(*result)

            # Check if the ROB entry matches the RAT entry
            if self.RAT.get(dest) == dest:
                self.ARF.set(dest,result[1])

            # Update writeback cycle
            self.updateOutput(result[0], 3)

        pass


    def commitStage(self):
        # Check if the ROB head is ready, and if so grab the result
        if self.ROB.canCommit():
            result = self.ROB.commit()
            self.updateOutput(result[0], 4)

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
