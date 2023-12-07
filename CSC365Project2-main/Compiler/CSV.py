
#HLC instruction    |   YMC Address  |   YMC assembly |  YMC encoding | Modified registers | Modified flags
#while y > 0        | XXXX           |  cmp eax, 0    | AB CD 20 XXXX |----                | SF = , OF, ZF, CF 
#                   |                |  Jg xxx

#--------------------------
#reads File, gets line count
#--------------------------
def lineCount(fileName):
    with open(fileName, "r") as file:
        content = file.read()

    #split content by newline characters
    lines = content.split("\n")

    lineAmount = len(lines)
    return lineAmount

#--------------------------------
#'HLC instruction', 'YMC Address', 'YMC assembly', 'YMC Encoding', 'Modified Registers', 'Modified Flags'
# hlcData, assemblyData, machineData, addressArray, modReg, modFlags
def csvCreate(fileName, fileName2, fileName3): #HLC, ASM, Machine
    import csv
    #fileName = 'test.txt'   #Whatever the HLC files name is
    textStop = lineCount(fileName2)    #ASM will be the longest

    # Create arrays : temp for now
    addressArray = ['1000', '1200', '1200', '1200']
    modFlags = ['CF, 0', 'ZF', 'SF', 'OF']
    modReg = ['ax', 'bx', 'dx', 'cx']

    #opens file: HLC file, whatever thats called
    with open(fileName, newline='') as input_file:
        # Create a CSV reader object
        reader = csv.reader(input_file)
        # Read the data into a list of lists
        hlcData = list(reader)

    #opens file: Assembly Code file
    with open(fileName2, newline='') as input_file:
        # Create a CSV reader object
        reader = csv.reader(input_file)
        # Read the data into a list of lists
        assemblyData = list(reader)

    #opens file: Machine Code file
    with open(fileName3, newline='') as input_file:
        # Create a CSV reader object
        reader = csv.reader(input_file)
        # Read the data into a list of lists
        machineData = list(reader)

    #create/open 'output.csv' File
    with open('output.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter='\t')

        #write headers
        writer.writerow(['HLC instruction', 'YMC Address', 'YMC assembly', 'YMC Encoding', 'Modified Registers', 'Modified Flags'])

        #loop to write each row
        for i in range(0, textStop, +1):
            writer.writerow([hlcData[i], assemblyData[i], machineData[i], addressArray[i], modReg[i], modFlags[i]])


    print('Successfully created CSV File')
    return 0



#-------------------------
#for i in range(0, 4, +1): # start, stop, increment : (0, 4, -1 or +1)
     # do something

#------------------------------------------
#idea functions (Probably won't use, but keeping in case)
#------------------------------------------
#unsigned range: 0 to 256
#signed range: -128 to 127



def unsignedSigned(unsigned):
    if unsigned > 127:
        return unsigned - 256
    else:
        return unsigned

def signedUnsigned(signed):
    if signed < 0:
        return signed + 256
    else:
        return signed