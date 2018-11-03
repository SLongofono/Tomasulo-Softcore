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

	def check(self, time):
		'''
		Check if any instruction in the pipeline can be popped
		'''
		output = []
		for i in range(len(self.pipeline)):
			if(self.pipeline[i][1] == time):
				output.append([self.pipeline[i][0], self.pipeline[i][2]])
		return output


class FPMultiplier:
	def __init__(self, latency, bufferLen):
		self.latency = latency
		self.bufferLen = bufferLen									#max buffer length
		self.buffer = []
		self.pipeline = FPALU_pipeline(5)							#set pipeline length as 5
		self.time = 0
		self.activeInstruction = None

	def execute(self, instr_id, instr, op1, op2):
		self.activeInstruction = (instr_id, instr, op1, op2)
		if(instr == 'MUL.d'):
			result = float(op1 * op2)
			schedule = self.time + latency['MUL.d']
			self.pipeline.add(instr_id, schedule, result) 
		else:
		    raise ValueError("Unknown operation [ {} ] in FP.adder, time [ {} ]".format(op, self.time))

	def busy(self):
		return ((self.pipeline.busy()) and (len(self.buffer) < self.bufferLen) ) 	

	def isResultReady(self):
		return len(self.buffer) > 0

	def getResult(self):
		return self.buffer.pop(0)

	def advanceTime(self):
		self.time += 1
		output = self.pipeline.check(self.time) 		
		self.buffer += output
	
	def dump(self):
		print("FP Multiplier".ljust(44, '=').rjust(80,'='))
		print("Time:\t\t\t{}".format(self.time))
		print("Busy:\t\t\t{}".format(self.busy()))
		print("Instruction:\t\t{}".format(self.activeInstruction))
		print("Output Buffer Contents:")
		for item in self.buffer:
			print("\tID:{}, Value:{}".format(item[0],item[1]))
		print()
				
class FPAdder:
	def __init__(self, latency, bufferLen):
		self.latency = latency
		self.bufferLen = bufferLen									#max buffer length
		self.buffer = []
		self.pipeline = FPALU_pipeline(5)						#set pipeline length as 5
		self.time = 0
		self.activeInstruction = None

	def execute(self, instr_id, instr, op1, op2):
		self.activeInstruction = (instr_id, instr, op1, op2)
		if(instr == 'ADD.d'):
			result = float(op1 + op2)
			schedule = self.time + latency['ADD.d']
			self.pipeline.add(instr_id, schedule, result) 
		elif(instr == 'SUB.d'):
			result = float(op1 - op2)
			schedule = self.time + latency['SUB.d']
			self.pipeline.add(instr_id, schedule, result) 
		else:
		    raise ValueError("Unknown operation [ {} ] in FP.adder, time [ {} ]".format(op, self.time))

	def busy(self):
		return self.pipeline.busy() and len(self.buffer) < self.bufferLen 	

	def isResultReady(self):
		return len(self.buffer) > 0

	def getResult(self):
		return self.buffer.pop(0)

	def advanceTime(self):
		self.time += 1
		output = self.pipeline.check(self.time) 		
		self.buffer += output

	def dump(self):
		print("FP Adder".ljust(44, '=').rjust(80,'='))
		print("Time:\t\t\t{}".format(self.time))
		print("Busy:\t\t\t{}".format(self.busy()))
		print("Instruction:\t\t{}".format(self.activeInstruction))
		print("Output Buffer Contents:")
		for item in self.buffer:
			print("\tID:{}, Value:{}".format(item[0],item[1]))
		print()

if __name__ == "__main__":
	t = 0
	latency = {'MUL.d': 5, 'ADD.d': 3, 'SUB.d': 3}
	myALU = FPAdder(latency, 3)
	print(myALU.busy)
	myALU.dump()
	myALU.execute(10,"ADD.d", 33, -1)
	myALU.dump()
	myALU.advanceTime()
	myALU.dump()
	print("Result ready?:{}".format(myALU.isResultReady()))
	myALU.advanceTime()
	myALU.advanceTime()
	myALU.advanceTime()
	print("Result ready?:{}".format(myALU.isResultReady()))
	r = myALU.getResult()
	print(r)
	myALU.dump()


