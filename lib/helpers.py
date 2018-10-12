# @file:		helpers.py
# @authors:		Stephen

def getParameters(inputFileName):
    with open(inputFileName, 'r') as inFile:
        
        params = {}

        inFile.readline()
        # Get mandatory inputs
        params['IntegerAdder'] = inFile.readline().split()[2:]
        params['FPAdder'] = inFile.readline().split()[2:]
        params['LoadStoreUnit'] = inFile.readline().split()[2:]
        params['ROBEntries'] = inFile.readline().split()[3]
        params['CDBBufferEntries'] = inFile.readline().split()[4]

        # Determine optional inputs
        x = inFile.readline()
        while len(x) > 0:
            data = x.split(',')
            if data[0][0] == "M":
                # Case memory initialization inputs
                memInitData = []
                for entry in data:
                    temp = data.split('=')
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
                pass

        # Get and parse instructions
        x = inFile.readline()
        rawInstructions = []
        while len(x) > 0:
            rawInstructions.append(x)

        params['Instructions'] = parseInstructions(rawInstructions)

def parseInstructions(rawInstructions):
    pass

