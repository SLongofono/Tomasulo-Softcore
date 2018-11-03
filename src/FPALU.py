# @file     FPAdder
# @authors  Yihao

class FPAdder_waitlist:
	"""
	This class implements the FPAdder waitlist
	"""
	
	def __init__(self, pipelineLen):
		"""
		Constructor for the FPAdder waitlist class.

		@param waitlist An list containing the items in waitlist
		@param maxlen An integar representing the maximum length of the waitlist
		"""
		self.waitlist = []
		self.maxlen = pipelineLen

	def add_list(self, instr_num, shedule, result):
		if(self.getlen < self.maxlen):
			self.waitlist.append([instr_num, shedule, result])
			return True		#True for success
		else:
			return False	#False for fail
	
	def getlen:
		return len(self.waitlist)

	def check_list(self, time):
		'''
		Check if any instruction in the waitlist can be popped
		'''
		output = []
		for i in range(self.getlen):
			if(self.waitlist[i][1] == time):
				output.append([waitlist[i][0], waitlist[i][2]])
		return output


class FPALU:
    """
    This class implements a pipelined FPAdder.

    The class tracks what it is actively executing, and reports time since
    instantiation for debugging purposes.  The latency of each instruction is
    encoded along with the maximum output buffer size at instantiation.  This
    implies that this unit is non-pipelined.
    """

    def __init__(self, latency, pipelineLen, bufferLen, time):
        """
        Constructor for the FPAdder class

        @param latency An integer value representing the number of cycles
        required per FP addition.
		@param pipelineLen An integer value representing the number of pipelines
		in FP adder
		@param parallel An integer value representing the number of pipelines
		that are busy in FP adder
        @param bufferLen An integer value representing how many results to
        buffer on output before stalling further inputs

        @param waitlist A two dimension list stores the result instructions executing 
        in the pipeline and its complete time. For each member, the first parameter
        stands for the time to complete and the second represents the results. e.g.
        waitlist[0][0] = time_to_complete, waitlist[0][1] = result_of_calculation
        """
        self.latency = latency
        self.bufferLen = bufferLen
        self.buffer = []
        self.waitlist = FPAdder_waitlist(pipelineLen)
		self.time = time

	def execute(self, instr_id, instr, op1, op2,  time):
			if(instr == 'MUL'):
				result = float(op1 * op2)
				schedule = time + latency['MUL']
			elif(instr == 'DIV'):
				result = float(op1 / op2)
				schedule = time + latency['DIV']
			elif(instr == 'ADD'):
				result = float(op1 + op2)
				schedule = time + latency['ADD']
			elif(instr == 'SUB'):
				result = float(op1 / op2)
				schedule = time + latency['SUB']

			if(self.waitlist.addlist(instr_id, schedule, result) == FALSE):
				return FALSE	#return busy
			elif:
				return TRUE

    def isResultReady(self):
        """
        Getter determines if a result is waiting to be written back
        """
        return len(self.buffer) > 0

    def getResult(self):
        """
        Getter for oldest execution result

        @return A tuple with the instruction ID followed by the result
        """
        return self.buffer.pop(0)

    def advanceTime(self):
        """
        Advances the time for this unit and propogates results to output buffer as they complete
        """
        self.time += 1
        if self.waitlist.getlen > 0:
        	#if the waitlist is not empty
          	output = check_list(self.time) 		
			self.buffer += output
			if(len(self.buffer) > self.bufferLen):
				print('outrange')
				self.buffer -= output

if __name__ == "__main__":
    time = 0
	latency = {'MUL': 10, 'DIV': 16, 'ADD': 4, 'SUB' : 4}
    myALU = FPALU(latency,5,5,time)
    myALU.execute("ADD",1, 33, -1, 1)
    myALU.advanceTime()
    print(f"Result ready?:{myALU.isResultReady()}")
    myALU.advanceTime()
    print(f"Result ready?:{myALU.isResultReady()}")
    r = myALU.getResult()
    print(r)
