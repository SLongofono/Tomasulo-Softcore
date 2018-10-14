# @file:		helpers.py
# @authors:		Stephen

def getParameters(inputFileName):
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
            if data[0][0] == "M":
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
                    if temp[0][0] == 'R':
                        regFileInitData.append( (temp[0],int(temp[1])) )
                    else:
                        regFileInitData.append( (temp[0],float(temp[1])) )

            x = inFile.readline()
        # End while len...

        params['MemInitData'] = memInitData
        params['RegFileInitData'] = regFileInitData

        # Get and parse instructions
        x = inFile.readline()
        rawInstructions = []
        while len(x) > 0:
            rawInstructions.append(x)
            x = inFile.readline()

        params['Instructions'] = parseInstructions(rawInstructions)

        return params

def parseInstructions(rawInstructions):
    pass

