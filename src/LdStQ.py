# @file		 LdStQ.py
# @authors	  Yihao

class LdStQ:
	'''
	This class implements a generic load and store queue
	'''
	def __init__(self, size):
		'''
		Constructor for the St queue class

		@param size An integer representing the maximum amount of entries
		for this st queue
		@param buffer A list representing the output buffer
		@param q A list representing the store queue
		'''
		self.size = size
		self.q = []
		self.time = 0
		self.buffer = []

	def isFull(self):
		'''
		Getter to determie if the St queue can accept new entries
		'''
		return len(self.q) == self.size

	def add(self, ID, instr, addr, value, offset):
		'''
		Adds a new entry to the end of the st queue

		@param instr An integar representing the instruction id
		@param addr An integar representing the address to be operated by memory
		@param value An integar representing the memory address storing the value
		@param offset An integar representing the offset of value address
		'''
		self.q.append([ID, instr, addr, value, offset, False])

	def check_forward(addr):
		'''
		Check if there is a forwarding problem while loading
		
		@param addr An integar representing the source address of ld 
		'''
		for i in self.q:
			if i[2] == addr:
				return True
		return False

	def remove(self, ID):
		'''
		Remove the entry in ldstq

		@param ID An integar representing the instruction id
		'''
		for i in len(self.q):
			if self.q[i][0] == ID:
				self.q.pop(i)


	def check(self):
		output = ()
		for i in range(len(self.q)):
			if self.q[i][4] == None:
				return self.q.pop(i)
		return output

	def advanceTime(self):
		self.time += 1
		entry = self.check()
		while(entry != ()):
			self.buffer.append( (entry[0], entry[1], entry[2], entry[3]) )
			entry = self.check()

	def isResultReady(self):
		return len(self.buffer) > 0

	def getResult(self):
		return self.buffer.pop(0)

	def dump(self):
		print("Store queue".ljust(50, '=').rjust(80, '='))
		if(len(self.q) == 0):
			print("\t[ empty ]")
		else:
			for entry in self.q:
				print("{}\t{}\t{}\t{}\t".format(entry[0],entry[1],entry[2],entry[3]))
		print()

if __name__ == "main":
	
