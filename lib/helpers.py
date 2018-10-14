# @file:		helpers.py
# @authors:		Stephen

def getParameters(inputFileName):
    """
    Given the full path to an input file, parses out the system parameters,
    intialization values, and instructions into a common data structure.

    @param inputFileName The full system filepath to the input file
    @return A dictionary populated with named system parameters and
    initialization values (as integer lists and lists of tuples)
    """
    with open(inputFileName, 'r') as inFile:
        params = {}

        inFile.readline()
        # Get mandatory inputs
        params['IntegerAdder'] = inFile.readline().split()[2:]
        params['FPAdder'] = inFile.readline().split()[2:]
        params['FPMultiplier'] = inFile.readline().split()[2:]
        params['LoadStoreUnit'] = inFile.readline().split()[2:]
        params['ROBEntries'] = inFile.readline().split()[3]
        params['CDBBufferEntries'] = inFile.readline().split()[4]

        memInitData = []
        regFileInitData = []

        # Determine optional inputs
        x = inFile.readline().strip()
        while len(x) > 1:   # Handle single newline case 0 -> 1
            data = x.split(',')
            if data[0][0].upper() == "M":
                # Case memory initialization inputs
                for entry in data:
                    temp = entry.split('=')
                    addr = int(temp[0][temp[0].find('[')+1:-1])

                    # Always store bytes in case the input is a mix of byte and word addresses
                    if not (addr % 4):
                        addr = 4 * addr

                    try:
                        value = int(temp[1])
                    except ValueError:
                        value = float(temp[1])

                    memInitData.append( (addr,value) )
            else:
                # Case register file initialization inputs
                for entry in data:
                    temp = entry.split('=')
                    print(temp)
                    if temp[0][0].upper() == 'R':
                        regFileInitData.append( (temp[0].upper(),int(temp[1])) )
                    else:
                        regFileInitData.append( (temp[0].upper(),float(temp[1])) )

            x = inFile.readline()
        # End while len...

        params['MemInitData'] = memInitData
        params['RegFileInitData'] = regFileInitData

        # Get and parse instructions
        x = inFile.readline()
        rawInstructions = []
        while len(x) > 0:
            rawInstructions.append(x.upper())
            x = inFile.readline()

        params['Instructions'] = parseInstructions(rawInstructions)

        return params

# Assumes uppercase list of strings input
def parseInstructions(rawInstructions):
    """
    Given a list of uppercase strings, parses the strings into instruction
    tuples.

    @param rawInstructions A list of uppercase strings representing
    instructions from the input file
    @return A list of tuples in a standard format with all pertinent
    information for each instruction
    """
    results = []
    for raw in rawInstructions:
        if raw.startswith('LD') or raw.startswith('SD'):    # case B type
            name = raw[:2]
            temp = raw[3:].strip().split(',')
            reg = temp[0]
            idx = temp[1].find('(')
            offset = int(temp[1][:idx])
            base = temp[1][idx:].strip(')').strip('(')
            results.append( (name, reg, offset, base) )

        elif raw.startswith('B'):                           # case B type
            name = raw[:3]
            temp = raw[3:].strip().split(',')
            results.append( (name, temp[0], temp[1], int(temp[2])) )

        elif raw.startswith('ADDI'):                        # case I type
            name = raw[:4]
            temp = raw[4:].strip().split(',')
            results.append( (name, temp[0], temp[1], int(temp[2])) )

        else:                                               # case R type
            idx = raw.find(' ')
            name = raw[:idx]
            temp = raw[idx:].strip().split(',')
            results.append( (name, temp[0], temp[1], temp[2]) )

    return results


# Helper function tests, run this script directly to execute

if __name__ == "__main__":
    print(parseInstructions(["LD F1,-45(R1)", "SD F2 , 0(R12)", "LD F0,-1(R1)"]))
    print(parseInstructions(["BNE R1 , R1 ,100", "BEQ R0,R2,-12 ", "BEQ R1, R0, -19"]))
    print(parseInstructions(["ADDI R1 , R1 ,100", "ADDI R0,R2,-12 ", "ADDI R1, R0, -19"]))
    print(parseInstructions(["ADD R1 , R1 ,R0", "SUB.D F0,F2,F22 ", "MULT.D F1, F0, F9"]))


