# @file		 LdStQ.py
# @authors	  Yihao

class LdStQ:
	'''
	This class implements a generic load and store queue
	'''
	def __init__(self, size, latency):
		'''
		Constructor for the St queue class

		@param size An integer representing the maximum amount of entries
		for this st queue
		@param execute_latency An integer representing the latency in execute stage
		@param number An integer representing the number of LdStQs, which should always be one
		@param buffer A list representing the output buffer
		@param q A list representing the store queue
		@param curInstr An tuple representing the current instruction in the execution stage
		'''
		self.size = size
		self.q = []
		self.time = 0
		self.buffer = []
		self.latency = latency
		self.nextFreeTime = -1
		self.curInstr = None

	def busy(self):
		return self.time < self.nextFreeTime 

	def execute(self):
		for x in self.q:
			if x[7] == False:
				self.nextFreeTime = self.time + self.latency
				self.curInstr = x
				break

	def update(self. tag, value):
		for entry in self.q:
			if entry[2] == tag:
				entry[2] = value
			if entry[3] == tag:
				entry[3] = tag
			if not (isinstance(entry[2], str) or isinstance(entry[3], str)):
				entry[8] = True	
		
	def isFull(self):
		'''
		Getter to determie if the St queue can accept new entries
		'''
		return len(self.q) == self.size

	def add(self, ID, instr, robid, value, offset):
		'''
		Adds a new entry to the end of the st queue

		@param instr An integar representing the instruction id
		@param robid An integar representing the ROB id of the target address
		@param value An integar representing the memory address storing the value
		@param offset An integar representing the offset of value address

		x[5] is a flag representing if the value is added by offset
		x[6] is a flag representing if the value is not an address value
		x[7] is a flag representing if this entry has been executed
		x[8] is a flag representing if the ROB tags are substituted by address
		'''
		self.q.append([ID, instr, robid, value, offset, False, False, False, False])

	def purgeAfterMispredict(self, BID):
		self.q = [x for x in self.q if x[0]<=BID]
		self.buffer = [x for x in self.buffer if x[0]<=BID]

	def checkReady(self):
		'''
		check if any LD/SD instruction is ready to enter memory stage
		'''
		for x in self.q:
			if x[5] and x[6] and x[7] and x[8]:
				self.buffer.append((x[0], x[1], x[2], x[3]))

	def advanceTime(self):
		self.time += 1
		if self.time == self.nextFreeTime:
			self.curInstr[7] = True	
			self.nextFreeTime = -1

	def isResultReady(self):
		return len(self.buffer) > 0

	def getResult(self):
		'''
		Getter of oldest execution result

		@return A tuple containing the instruction ID and the load value
		'''
		return self.buffer.pop(0)

	def getResultID(self):
		'''
		Getter for the ID of the head of the output buffer
		'''
		return self.buffer[0][0]

	def dump(self):
		print("Store queue".ljust(50, '=').rjust(80, '='))
		if(len(self.q) == 0):
			print("\t[ empty ]")
		else:
			for entry in self.q:
				print("{}\t{}\t{}\t{}\t".format(entry[0],entry[1],entry[2],entry[3]))
		print()

if __name__ == "main":
	
