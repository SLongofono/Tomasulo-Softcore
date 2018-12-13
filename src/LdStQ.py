# @file         LdStQ.py
# @authors      Yihao, Stephen

class LdStQ:
    '''
    This class implements a generic load and store queue
    '''
    def __init__(self, size, latency, MMU):
        '''
        Constructor for the St queue class

        @param size An integer representing the maximum amount of entries
        for this st queue
        @param execute_latency An integer representing the latency in execute stage
        @param number An integer representing the number of LdStQs, which should always be one
        @param buffer A list representing the output buffer
        @param q A list representing the store queue
        @param curInstr An tuple representing the current instruction in the execution stage
        @param MMU A reference to an instance of the MemoryUnit class
        '''
        self.size = size
        self.q = []
        self.time = 0
        self.buffer = []
        self.latency = latency
        self.nextFreeTime = -1
        self.curInstr = None
        self.MMU = MMU


    def busy(self):
        return self.time < self.nextFreeTime


    def executeStage(self, position):
        self.nextFreeTime = self.time + self.latency
        self.curInstr = self.q[position]


    def doForwards(self):
        for i, entry in enumerate(self.q):
            if entry[1] == 'LD' and isinstance(entry[3], int): # if the address of this load is known
                for j in range(i): #find all previous stores
                    idx = len(self.q) - 1 - j
                    # if the instruction is ready and we have a matching address
                    if (self.q[idx][1] == 'SD') and (self.instructionReady(self.q[idx])) and (self.q[idx][3] == entry[3]):
                        # get data from the store and put it directly in the
                        # output buffer
                        self.buffer.append(entry[0], self.q[idx][2])
                        self.q.pop(i)
                        return entry[0]
                    else:
                        return -1
        return -1


    def issueReadyLoad(self):
        for i, entry in enumerate(self.q):
            if entry[1] == 'LD' and self.instructionReady(entry) and not self.MMU.busy() and not entry[6]:
                self.MMU.execute(entry)
                entry[6] = True
                return entry[0]

        return -1


    def issueReadyStore(self):
        for i, entry in enumerate(self.q):
            if entry[1] == 'SD' and self.instructionReady(entry) and not self.MMU.busy() and not entry[6]:
                self.MMU.execute(entry)
                entry[6] = True
                return entry[0]
        return -1


    def checkMMU(self):
        if self.MMU.isResultReady():
            if self.MMU.buffer[0][1] is None:
                print("STORE COMPLETE MMU")
                self.remove(self.MMU.buffer[0][0])
                self.MMU.getResult()
            else:
                print("RETRIEVED A LOAD FROM MMU")
                self.remove(self.MMU.buffer[0][0])
                self.buffer.append(self.MMU.getResult())


    def update(self, tag, value):
        # Reference [ID, instr, rob, register, offset]
        for entry in self.q:
            if entry[2] == tag:
                entry[2] = value
            else:
                print(f"LDSTQ: {entry[2]} doesnt match {tag}")
            if entry[3] == tag:
                entry[3] = value
            else:
                print(f"LDSTQ: {entry[3]} doesnt match {tag}")


    def computeAddress(self, instr):
        for entry in self.q:
            if entry[0] == instr[0]:
                entry[3] = entry[3] + entry[4]
                entry[5] = True


    def isFull(self):
        '''
        Getter to determie if the St queue can accept new entries
        '''
        return (len(self.q) == self.size) or (len(self.buffer) > 0)


    def add(self, ID, instr, robid, value, offset):
        '''
        Adds a new entry to the end of the st queue

        @param instr An integar representing the instruction id
        @param robid An integar representing the ROB id of the target address
        @param value An integar representing the memory address storing the value
        @param offset An integar representing the offset of value address

        Note: the fifth entry indicates whether the byte address has been
        computed yet or not
        Note: the sixth entry indicates whether the instruction is being
        serviced by the MMU
        '''
        self.q.append([ID, instr, robid, value, offset, False, False])


    def instructionReady(self, entry):
        return entry[5] and (entry[1] == 'LD' or isinstance(entry[2], float) )


    def purgeAfterMispredict(self, BID):
        self.q = [x for x in self.q if x[0]<=BID]
        self.buffer = [x for x in self.buffer if x[0]<=BID]


    def advanceTime(self):
        self.time += 1
        if self.time == self.nextFreeTime:
            self.nextFreeTime = -1
            self.computeAddress(self.curInstr)
            self.curInstr = None


    def isResultReady(self):
        return len(self.buffer) > 0


    def remove(self, ID):
        for i, entry in enumerate(self.q):
            if entry[0] == ID:
                self.q.pop(i)
                return


    def getResult(self):
        '''
        Getter of oldest execution result

        @return A tuple containing the instruction ID, and either the loaded
        value if a load instruction, or None if a store instruction
        '''
        return self.buffer.pop(0)


    def getResultID(self):
        '''
        Getter for the ID of the head of the output buffer
        '''
        return self.buffer[0][0]


    def dump(self):
        print("Load/Store queue".ljust(50, '=').rjust(80, '='))
        if(len(self.q) == 0):
            print("\t[ empty ]")
        else:
            for entry in self.q:
                print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6]))
        print()


if __name__ == "__main__":
    myq = LdStQ(3,1)    
    t = 0
    myq.dump()
    myq.add(1,'LD','ROB2',8,8)
    myq.dump()
    myq.execute()
    print("Busy?:{}".format(myq.busy()))
    myq.advanceTime()
    myq.dump()
    print("Busy?:{}".format(myq.busy()))
    myq.checkReady()
    print("Ready?:{}".format(myq.isResultReady()))
    myq.q[0][5] = True
    myq.q[0][6] = True
    myq.update('ROB2',16)
    myq.checkReady()
    myq.dump()
    print("Ready?:{}".format(myq.isResultReady()))
    print("Get result:{}".format(myq.getResult()))
