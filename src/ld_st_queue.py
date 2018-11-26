# @file         Ld_st_queue.py
# @authors      Yihao

class St_queue:
	'''
	This class implements a generic load queue
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

	def add(self, instr, addr, value, value_tag):
		'''
		Adds a new entry to the end of the st queue

		@param instr An integar representing the instruction id
		@param addr An integar representing the address to be operated by memory
		@param value An integar or float point number to be stored
		@param value_tag A string reprenting the ROB entry tag where the value
		to be stored
		'''
		self.q.append([instr, addr, value, value_tag])

	def remove(self, instr):
		for i in len(self.q):
			if self.q[i][0] == instr:
				self.q.pop(i)

	def update(self, value_tag, value):
		'''
		Given a tag and a value, updates the value operand of any entries 
		with that tag and sets the tag to None

		@param tag A string representing the ROB entry tag to search for and 
		update the value for
		@param value A numeric value used to update the associated value 
		for any tags found under search of the St queue
		'''
		for entry in self.q:
			if entry[3] == tag:
				entry[3] = None
				entry[2] = value

	def check(self):
		output = ()
		for i in range(len(self.q)):
			if self.q[i][3] == None:
				return self.q.pop(i)
		return output

	def advanceTime(self):
		self.time += 1
		entry = self.check()
		while(entry != ()):
			self.buffer.append( (entry[0], entry[1], entry[2]) )
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

	
class Ld_queue:
	'''
	This class implements a generic load queue
	'''
	def __init__(self, size):
		'''
		Conldructor for the Ld queue class

		@param size An integer representing the maximum amount of entries
		for this ld queue
		'''
		self.size = size
		self.q = []
		self.time = 0
		self.buffer = []

	def isFull(self):
		'''
		Getter to determie if the Ld queue can accept new entries
		'''
		return len(self.q) == self.size

	def add(self, instr, addr):
		'''
		Adds a new entry to the end of the ld queue

		@param instr An integar representing the instruction id
		@param addr An integar representing the address to be operated by memory
		'''
		self.q.append([instr, addr])

	def remove(self, instr):
		for i in len(self.q):
			if self.q[i][0] == instr:
				self.q.pop(i)

	def check(self):
		for i in range(len(self.q)):
				return self.q.pop(i)
		return None

	def advanceTime(self):
		self.time += 1
		#TODO: forwarding from a store
		entry = None
		entry = self.check()
		while(entry != None):
			self.buffer.append( (entry[0], entry[1]) )
			entry = self.check()

	def isResultReady(self):
		return len(self.buffer) > 0

	def getResult(self):
		return self.buffer.pop(0)

	def dump(self):
		print("Load queue".ljust(50, '=').rjust(80, '='))
		if(len(self.q) == 0):
			print("\t[ empty ]")
		else:
			for entry in self.q:
				print("{}\t{}\t".format(entry[0],entry[1]))
		print()

if __name__ == "__main__":
	st = St_queue(5)
	ld = Ld_queue(5)
	'''
	ld.add(1,0x20)
	ld.advanceTime()
	print(f"Result ready?:{ld.isResultReady()}")
	ld.add(2,0x30)
	ld.advanceTime()
	ld.add(3,0x20)
	ld.advanceTime()
	ld.dump()
	print(f"Result ready?:{ld.isResultReady()}")
	'''
	st.add(1,0x20,0,None)
	st.advanceTime()
	print(f"Result ready?:{st.isResultReady()}")
	st.add(2,0x30,0,None)
	st.advanceTime()
	st.add(3,0x20,0,None)
	st.advanceTime()
	st.dump()
	print(f"Result ready?:{st.isResultReady()}")
