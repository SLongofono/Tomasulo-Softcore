# @file     FPALU
# @authopipeline  Yihao

class FPALU_pipeline:
	"""
	This class implements the FPAdder pipeline
	"""
	
	def __init__(self, pipelineLen):
		"""
		Constructor for the FPAdder pipeline class.

		@param pipeline An list containing the items in pipeline
		@param maxlen An integar representing the maximum length of the pipeline
		"""
		self.pipeline = []
		self.maxlen = pipelineLen

	def add(self, instr_num, shedule, result):
			self.pipeline.append([instr_num, shedule, result])
	
	def busy(self):
		return len(self.pipeline) == self.maxlen

	def showpip(self):
		return self.pipeline

	def check(self, time):
		'''
		Check if any instruction in the pipeline can be popped
		'''
		output = []
		for i in range(len(self.pipeline)):
			if(self.pipeline[i][1] == time):
				return self.pipeline.pop(i)
		return output


class FPMultiplier:
	def __init__(self, latency, bufferLen, pipelineLen):
		"""
		Constructor for the Multiplier class

		@param latency An dictionary containing the number of cycles required per operation. e.g. {"ADD.D":8, "MULT.D":10}
		@param bufferLen An integer value representing how may results to buffer on output before stalling further inputs
		@param pipelineLen An integer value representing how may instructions to buffer in pipeline
		"""
		self.latency = latency
		self.bufferLen = bufferLen									#max buffer length
		self.buffer = []
		self.pipeline = FPALU_pipeline(pipelineLen)							#set pipeline length as 5
		self.time = 0
		self.activeInstruction = None

	def execute(self, instr_id, instr, op1, op2):
		self.activeInstruction = (instr_id, instr, op1, op2)
		if(instr == 'MULT.D'):
			result = float(op1 * op2)
			schedule = self.time + self.latency['MULT.D']
			self.pipeline.add(instr_id, schedule, result) 
		else:
		    raise ValueError("Unknown operation [ {} ] in FP.adder, time [ {} ]".format(instr, self.time))

	def busy(self):
		return ((self.pipeline.busy()) or (len(self.buffer) == self.bufferLen) ) 	


	def purgeAfterMispredict(self, BID):
		"""
		Removes all currently queued and completed instructions with ID> BID
	
		@param BID An integer representing the instruction ID of the mispredicted branch
		"""
		self.buffer = [x for x in self.buffer if x[0]<= BID ]
		self.pipeline.pipeline = [x for x in self.pipeline.pipeline if x[0]<= BID ]

	def isResultReady(self):
		return len(self.buffer) > 0

	def getResult(self):
		return self.buffer.pop(0)

	def getResultID(self):
		return self.buffer[0][0]

	def advanceTime(self):
		self.time += 1
		output = self.pipeline.check(self.time) 		
		while(output != []):
			self.buffer.append([output[0],output[2]])
			output = self.pipeline.check(self.time) 		
	
	def dump(self):
		print("FP Multiplier".ljust(48, '=').rjust(80,'='))
		print("Time:\t\t\t{}".format(self.time))
		print("Busy:\t\t\t{}".format(self.busy()))
		print("Instruction:\t\t{}".format(self.activeInstruction))
		print("Pipeline:\t\t{}".format(self.pipeline.showpip()))
		print("Output Buffer Contents:")
		for item in self.buffer:
			print("\tID:{}, Value:{}".format(item[0],item[1]))
		print()
				
class FPAdder:
	"""
	This class implements a simple floating point adder.

	"""
	def __init__(self, latency, bufferLen,pipelineLen):
		"""
		Constructor for the FPAdder class

		@param latency An dictionary containing the number of cycles required per operation. e.g. {"ADD.D":8}
		@param bufferLen An integer value representing how may results to buffer on output before stalling further inputs
		@param pipelineLen An integer value representing how may instructions to buffer in pipeline
		"""
		self.latency = latency
		self.bufferLen = bufferLen									#max buffer length
		self.buffer = []
		self.pipeline = FPALU_pipeline(pipelineLen)						#set pipeline length as 5
		self.time = 0
		self.activeInstruction = None

	def execute(self, instr_id, instr, op1, op2):
		self.activeInstruction = (instr_id, instr, op1, op2)
		if(instr == 'ADD.D'):
			result = float(op1 + op2)
			schedule = self.time + self.latency['ADD.D']
			self.pipeline.add(instr_id, schedule, result) 
		elif(instr == 'SUB.D'):
			result = float(op1 - op2)
			schedule = self.time + self.latency['SUB.D']
			self.pipeline.add(instr_id, schedule, result) 
		else:
		    raise ValueError("Unknown operation [ {} ] in FP.adder, time [ {} ]".format(instr, self.time))

	def busy(self):
		return ((self.pipeline.busy()) or (len(self.buffer) == self.bufferLen) ) 	

	def purgeAfterMispredict(self, BID):
		"""
		Removes all currently queued and completed instructions with ID> BID

		@param BID An integer representing the instruction ID of the mispredicted branch
		"""
		self.buffer = [x for x in self.buffer if x[0]<= BID ]
		self.pipeline.pipeline = [x for x in self.pipeline.pipeline if x[0]<= BID ]

	def isResultReady(self):
		return len(self.buffer) > 0

	def getResult(self):
		return self.buffer.pop(0)

	def getResultID(self):
		return self.buffer[0][0]

	def advanceTime(self):
		self.time += 1
		output = self.pipeline.check(self.time) 		
		while(output != []):
			self.buffer.append([output[0], output[2]])
			output = self.pipeline.check(self.time) 		
	
	def dump(self):
		print("FP Adder".ljust(48, '=').rjust(80,'='))
		print("Time:\t\t\t{}".format(self.time))
		print("Busy:\t\t\t{}".format(self.busy()))
		print("Instruction:\t\t{}".format(self.activeInstruction))
		print("Pipeline:\t\t{}".format(self.pipeline.showpip()))
		print("Output Buffer Contents:")
		for item in self.buffer:
			print("\tID:{}, Value:{}".format(item[0],item[1]))
		print()


if __name__ == "__main__":
	latency = {"ADD.D":5, "SUB.D":5, "MULT.D":8}
	t = 0
	myAdder = FPAdder(latency,3,3)
	myMultiplier = FPMultiplier(latency,3,3)
	'''
	myAdder.dump()
	myMultiplier.dump()
	myAdder.execute(1,"ADD.D",1.5,1.6)
	myAdder.dump()
	myAdder.advanceTime()
	myAdder.dump()
	myAdder.execute(2,"SUB.D",1.5,1.6)
	myAdder.dump()
	myAdder.advanceTime()
	myAdder.dump()
	myAdder.execute(3,"SUB.D",1.5,1.5)
	myAdder.dump()
	myAdder.advanceTime()
	myAdder.dump()

	print(f"Result ready?:{myAdder.isResultReady()}")
	print(f"Busy?:{myAdder.busy()}")
	myAdder.advanceTime()
	myAdder.advanceTime()
	myAdder.advanceTime()
	myAdder.advanceTime()
	print(f"Result ready?:{myAdder.isResultReady()}")
	print(f"Busy?:{myAdder.busy()}")
	print(myAdder.buffer)
	r = myAdder.getResult()
	print(f"Result is :{r}")
	myAdder.dump()
	'''
	myMultiplier.dump()
	myMultiplier.dump()
	myMultiplier.execute(1,"MULT.D",1.5,1.6)
	myMultiplier.dump()
	myMultiplier.advanceTime()
	myMultiplier.dump()
	myMultiplier.execute(2,"MULT.D",0,1.6)
	myMultiplier.dump()
	myMultiplier.advanceTime()
	myMultiplier.dump()
	myMultiplier.execute(3,"MULT.D",-1,1.5)
	myMultiplier.dump()
	myMultiplier.advanceTime()
	myMultiplier.dump()

	print(f"Result ready?:{myMultiplier.isResultReady()}")
	print(f"Busy?:{myMultiplier.busy()}")
	myMultiplier.advanceTime()
	myMultiplier.advanceTime()
	myMultiplier.advanceTime()
	myMultiplier.advanceTime()
	myMultiplier.advanceTime()
	print(f"Result ready?:{myMultiplier.isResultReady()}")
	print(f"Busy?:{myMultiplier.busy()}")
	print(myMultiplier.buffer)
	r = myMultiplier.getResult()
	print(f"Result is :{r}")
	myMultiplier.dump()

