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
            for byteAddress, value in self.Params["MemInitData"]:
                self.memory.mem_write(byteAddress, value)
            self.memory.dump()

            # Instantiate Branch Unit
            self.branch = BranchUnit()

            # Track retired instruction count globally
            self.numRetiredInstructions = 0

            # Track time as cycles
            self.cycle = 0

            # Track PCnext offset to assist with branching
            self.fetchOffset = 0

            # Track if we are stalled for branch misprediction
            self.branchStalled = False

            # Track mispredicted branch outcomes across ALUIs
            self.mispredictions = []

            # Dumb way to kick out when we are done
            self.done = False

        except FileNotFoundError:
            print("ERROR: Invalid filename, please check the filename and path")
            return None


    def runSimulation(self):
        """
        Begins the simulation defined by the input file provided at instantiation
        """
        print("Beginning Simulation")

        while not self.done:
            print(''.ljust(80,'='))
            print(f" Cycle {self.cycle}".ljust(48, '=').rjust(80,'='))
            print(''.rjust(80,'='))

            # Log state
            #self.dump()
            self.IQ.dump()
            self.ALUIs[0].dump()
            self.RS_ALUIs.dump()
            self.ROB.dump()

            # Try to issue new instructions
            print("ISSUE")
            self.issueStage()

            # Try to execute ready instructions
            print("EXECUTE")
            self.executeStage()

            # Gather and process any branch outcomes
            print("BRANCHCHECK")
            self.checkBranchStage()

            # Try to write back load results
            print("MEMORY")
            self.memoryStage()

            # Try to write back FU results
            print("WRITEBACK")
            self.writebackStage()

            # Try to commit
            print("COMMIT")
            self.commitStage()

            # Advance time
            self.advanceTime()

            if(self.cycle == 8):
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
        if not ID in self.output:
            self.output[ID] = [self.cycle, None, None, None, None]
        else:
            self.output[ID][stage] = self.cycle


    def dumpAll(self):
        for FU in self.ALUIs:
            FU.dump()
        for FU in self.ALUFPs:
            FU.dump()
        for FU in self.MULTFPs:
            FU.dump()

        self.ROB.dump()
        self.ARF.dump()
        self.RAT.dump()
        self.memory.dump()
        self.IQ.dump()


    def writeOutput(self):
        """
        Write the output file of the results
        """
        fileName = self.Params["InputFile"]
        fileName = fileName[:fileName.find('.')]
        fileName = fileName + "_output.txt"

        with open(fileName, 'w') as outFile:
            # Write the instruction stage tracking
            outFile.write("Instruction Completion Table".ljust(48,'=').rjust(80,'='))
            outFile.write("\nID\t| IS\t\t EX\t\t MEM\t\t WB\t\t COM\n")
            for inst, stages in self.output.items():
                outFile.write(f"{inst}\t| {stages[0]}\t\t {stages[1]}\t\t {stages[2]}\t\t {stages[3]}\t\t {stages[4]}\n")
            outFile.write("\n")

            # Write the register file
            outFile.write("Integer ARF".ljust(48, '=').rjust(80,'='))
            outFile.write('\n')
            keys = [f"R{x}" for x in range(32)]
            for i in range(0,len(keys),4):
                outFile.write(f"{keys[i].ljust(3,' ')}: {self.ARF.get(keys[i])}".ljust(20, ' '))
                outFile.write(f"{keys[i+1].ljust(3,' ')}: {self.ARF.get(keys[i+1])}".ljust(20, ' '))
                outFile.write(f"{keys[i+2].ljust(3,' ')}: {self.ARF.get(keys[i+2])}".ljust(20, ' '))
                outFile.write(f"{keys[i+3].ljust(3,' ')}: {self.ARF.get(keys[i+3])}".ljust(20, ' '))
                outFile.write("\n")
            outFile.write("\n")

            outFile.write("Floating Point ARF".ljust(48, '=').rjust(80,'='))
            outFile.write('\n')
            keys = [f"F{x}" for x in range(32)]
            for i in range(0, len(keys),2):
                outFile.write(f"{keys[i].ljust(3,' ')}: {self.ARF.get(keys[i]):.6f}".ljust(40, ' '))
                outFile.write(f"{keys[i+1].ljust(3,' ')}: {self.ARF.get(keys[i+1]):.6f}".ljust(40, ' '))
                outFile.write("\n")
            outFile.write("\n\n")

            # write the nonzero sections of memory
            outFile.write("Memory Unit".ljust(48, '=').rjust(80,'='))
            outFile.write('\n')
            entries = [(str(i),x) for i,x in enumerate(self.memory.memory) if ((x > 0.0) or (x < 0.0)) ]
            newLine = False
            for address, contents in entries:
                outFile.write(f"Word {address.rjust(2,'0')}: {contents:.6f} ".ljust(40,' '))
                if newLine:
                    outFile.write('\n')
                newLine = not newLine
            outFile.write('\n')


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
        stage = None
        for i in range(5):
            stage = self.output[ID][4-i]
            if stage is not None:
                break
        return stage == self.cycle


    def issueStage(self):
        """
        Attempts to issue the next instruction in the Instruction Queue
        """
        if self.IQ.empty(offset=self.fetchOffset):
            print(f"EMPTY IQ, offset={self.fetchOffset}")
            return

        if not self.ROB.isFull():
            # Peek at PC
            nextName = self.IQ.peek(offset=self.fetchOffset)[1]

            print(f"NEXT INST {nextName}")

            # Check that the relevant RS is not full
            # Fetch actual instruction
            if (nextName == "LD") or (nextName == "SD"):
                if not self.memory.q.isFull():
                    nextInst = self.IQ.fetch(offset=self.fetchOffset)
                    self.fetchOffset = 0
                    # TODO Add in memory-specific issue handling here
                return

            elif (nextName == "ADD.D") or (nextName == "SUB.D"):
                if not self.RS_ALUFPs.isFull():
                    nextInst = self.IQ.fetch(offset=self.fetchOffset)
                    self.fetchOffset = 0
                else:
                    return

            elif (nextName == "MULT.D"):
                if not self.RS_MULTFPs.isFull():
                    nextInst = self.IQ.fetch(offset=self.fetchOffset)
                    self.fetchOffset = 0
                else:
                    return

            elif (nextName == "BNE") or (nextName == "BEQ"):
                if not self.RS_ALUIs.isFull():
                    # Store a copy of the RAT
                    canProceed = self.branch.saveRAT(self.IQ.peek(offset=self.fetchOffset)[0], self.RAT.getState())
                    if canProceed:
                        nextInst = self.IQ.fetch(offset=self.fetchOffset)
                        predictTaken = self.branch.predict(nextInst[0])
                        if predictTaken:
                            # update global fetch offset to branch target
                            self.fetchOffset = int(nextInst[1][3])
                            print(f"BRANCH, updating offset to {self.fetchOffset}")
                            # store PC in case of misprediction
                            self.branch.setMispredictTarget(nextInst[0],self.IQ.next)
                        else:
                            self.fetchOffset = 0
                            print(f"BRANCH, updating offset to {self.fetchOffset}")
                            # store target in case of misprediction
                            self.branch.setMispredictTarget(nextInst[0], self.IQ.next + int(nextInst[1][3]))
                else:
                    return
            else:
                if not self.RS_ALUIs.isFull():
                    nextInst = self.IQ.fetch(offset=self.fetchOffset)
                    self.fetchOffset = 0
                    print(f"Fetched ALU inst : {nextInst[1][0]}")
                else:
                    print("ALUIs are full!")
                    return

            print("Next inst: ", nextInst)

            # Add the entry to the ROB
            ROBId = self.ROB.add(nextInst[0],nextInst[1][1])

            # Prepare an entry for the RS
            entry = [nextInst[0], ROBId, nextInst[1][0], None, None, None, None]

            # Check if operands are ready now and update
            # Special case for branches:
            if nextName.startswith('B'):
                operand1 = nextInst[1][1]
                operand2 = nextInst[1][2]
                map1 = self.RAT.get(operand1)
                map2 = self.RAT.get(operand2)
                print(f"Branch: {operand1}, {operand2}")
                if(map1 == operand1):
                    entry[5] = self.ARF.get(operand1)
                else:
                    entry[3] = map1
                if(map2 == operand2):
                    entry[6] = self.ARF.get(operand2)
                else:
                    entry[4] = map2

            else:
                # Update operands per the RAT
                # nextInst  [0, ('ADD', 'R1', 'R2', 'R3')]
                # Mapping ('ADD', 'R1', 'R2', 'R3')
                mapping = self.RAT.getMapping(nextInst[1])
                print("Mapping: ", mapping)

                if mapping[2] == nextInst[1][2]:
                    entry[5] = self.ARF.get(mapping[2])
                else:
                    entry[3] = mapping[2]

                if mapping[3] == nextInst[1][3]:
                    entry[6] = self.ARF.get(mapping[3])
                else:
                    entry[4] = mapping[3]

            # Update RAT
            self.RAT.set(nextInst[1][1], ROBId)
            assert(self.RAT.get(nextInst[1][1]) == ROBId)

            self.RAT.dump()

            # Add the entry to the RS
            if(nextName == "ADD.D"):
                self.RS_ALUFPs.add(*entry)
            elif(nextName == "MULT.D"):
                self.RS_MULTFPs.add(*entry)
            else:
                self.RS_ALUIs.add(*entry)

            print(nextInst)

            # Log the issue in the output dictionary
            self.updateOutput(entry[0], 0)


    def executeStage(self):
        """
        For each funcitonal unit, attempts to find an instruction which is
        ready to execute
        """

        # Enumerate a list of ready instructions
        ready_ALUIs = [x for x in self.RS_ALUIs.q if ( (x[5] is not None) and
                                                       (x[6] is not None) and
                                                       (not x[7]) and
                                                       (not self.isTooNew(x[0])))]
        ready_ALUFPs = [x for x in self.RS_ALUFPs.q if ( (x[5] is not None) and
                                                         (x[6] is not None) and
                                                         (not x[7]) and
                                                         (not self.isTooNew(x[0])))]
        ready_MULTFPs = [x for x in self.RS_MULTFPs.q if ( (x[5] is not None) and
                                                           (x[6] is not None) and
                                                           (not x[7]) and
                                                           (not self.isTooNew(x[0])))]
        #TODO ready_LoadStore = []

        # Mark executed instructions for cleanup
        markAsExecuting = []

        # Attempt to issue each instruction on an available unit
        curPos = 0
        for i, FU in enumerate(self.ALUIs):
            if curPos >= len(ready_ALUIs):
                break
            if not FU.busy():
                FU.execute( ready_ALUIs[curPos][0],
                            ready_ALUIs[curPos][2],
                            int(ready_ALUIs[curPos][5]),
                            int(ready_ALUIs[curPos][6])
                )
                self.updateOutput(ready_ALUIs[curPos][0], 1)
                markAsExecuting.append(ready_ALUIs[curPos][0])
                curPos += 1

        # TODO uncomment once these classes are done
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
        #        markAsExecuting.append(ready_ALUIs[curPos][0])
        #        curPos += 1

        # TODO uncomment once these classes are done
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
        #        markAsExecuting.append(ready_ALUIs[curPos][0])
        #        curPos += 1

        for item in markAsExecuting:
            # Don't check, just blindly call since IDs are unique
            self.RS_ALUIs.markAsExecuting(item)
            # TODO uncomment once these classes are done
            #self.RS_ALUFPs.markAsExecuting(item)
            #self.RS_MULTFP.markAsExecuting(item)


    def checkBranchStage(self):
        """
        Checks to see if the most recent ALUI result is a branch, and if so
        processes the result, and checks for misprediction
        """
        for FU in self.ALUIs:
            if FU.isBranchOutcomePending():
                BID, outcome, _ = FU.getResult()
                prediction = self.branch.predict(BID)
                if outcome != prediction:
                    # signal branch rollback
                    self.mispredictions.append(BID)
                    self.branchStalled = True
                    print(f"BRANCH MISPREDICTION, INSTRUCTION {BID}")

                    # Recover RAT and associated branch instruction ID
                    self.RAT.reg = self.branch.rollBack(BID)

                    # Clear RS for speculative instructions
                    self.RS_ALUIs.purgeAfterMispredict(BID)
                    self.RS_ALUFPs.purgeAfterMispredict(BID)
                    self.RS_MULTFPs.purgeAfterMispredict(BID)

                    # Clear ROB entries after branch
                    self.ROB.purgeAfterMispredict(BID)

                    # Update fetch offset and PC per true branch outcome
                    self.IQ.setPC(self.branch.getMispredictTarget(BID))
                    self.fetchOffset = 0

                    # Update branch outcome in branch unit
                    if prediction:
                        self.branch.update(BID, False)
                    else:
                        self.branch.update(BID, True)

                    # Purge speculations from output
                    dead = [x for x in self.output.keys() if x > BID]
                    for deadEntry in dead:
                        del self.output[deadEntry]

                # Since we pulled the result, handle the ROB bookkeeping
                dest = self.ROB.findAndUpdateEntry(BID, outcome)
                self.RS_ALUIs.remove(BID)


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

            print(f"Writing back {result}")

            # Update ROB results
            dest,name = self.ROB.findAndUpdateEntry(*result[:-1])

            print(f"ROB Destination: {name}")


            # Update Reservation Stations
            self.RS_ALUIs.update(name, result[1])
            self.RS_ALUFPs.update(name, result[1])
            self.RS_MULTFPs.update(name, result[1])

            # TODO update load/stores

            # Free old reservation station(just blindly call)
            self.RS_ALUIs.remove(result[0])
            self.RS_ALUFPs.remove(result[0])
            self.RS_MULTFPs.remove(result[0])

            # Update writeback cycle
            self.updateOutput(result[0], 3)

        pass


    def commitStage(self):
        # Check if the ROB head is ready, and if so grab the result
        resultID = self.ROB.canCommit()
        if resultID is not None:
            # Verify that we didn't write back this cycle
            if not self.isTooNew(resultID):
                print(f"Committing instr. {resultID}")

                # Reference ID, destination, value, doneflag, ROB#
                result = self.ROB.commit()

                print("ROB returned: ",result)

                # Check if the RAT should be updated
                if(self.RAT.get(result[1]) == result[4]):
                    self.RAT.set(result[1], result[1])

                # Update ARF if this is not a branch
                if not isinstance(result[2], bool):
                    self.ARF.set(result[1], result[2])

                # TODO issue store if necessary

                # Retire the instruction
                self.numRetiredInstructions += 1

                # Update commit cycle
                self.updateOutput(resultID, 4)



    def usage():
        """
        Simple helper to print usage information for the entry class
        """
        print("\nUsage:")
        print("\n\t$ python3 Tomasulo.py <testFilePath>\n")


# End Class Tomasulo


# Run simulation by executing this script directly
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("No imput file provided!")
        Tomasulo.usage()
        sys.exit(1)
    myCore = Tomasulo(sys.argv[1])
    myCore.runSimulation()
