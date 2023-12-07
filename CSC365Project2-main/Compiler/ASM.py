#---------------------------------------------------
#Stack stuff (Allows pushing and poping onto a stack)
#---------------------------------------------------
stackCounter = 0

class Stack:
    def __init__(self):
        self.stack = [] #blank array to represent

    def push(self, register):
        stackCounter = stackCounter + 1 #To know where things located
        self.stack.append(register)

    def pop(self):
        stackCounter = stackCounter - 1 #To know where things are located
        if len(self.stack) < 1:
            return None
        return self.stack.pop()

    #stack = Stack() #create stack

    #stack.push('eax') #push variable

    #stack.pop()  #pop : output %eax : last in

#Memory:
    #eax = 0001
    #ebx = 0002
    #ecx = 0003
    #edx = 0004
    #a = 0005
    #b = 0006
    #c = 0007
    #x = 0008
    #y = 0009
    #z = 0010
    #line 0 = 0011 -> Increments up for storage

#---------------------------------------------------
#Variables
#---------------------------------------------------
import re

lineCounterM = 0 #count lines for MACHINE CODE
array = []
i = 1

#paths
fileName2 = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\Assembly.txt")
fileName3 = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\Machine.txt")

#---------------------------------------------------
#writeBack Function (Writes to new txt file)
#---------------------------------------------------
tempCounter = 0
machineArr = []

def writeBack (new_line):  #can't just append 1 line apparently
    global lineCounterM, fileName3, tempCounter, machineArr #global, other counter was mistake, too far gone
    lineCounterM = lineCounterM + 1   #increment machine lines as added
    tempCounter = tempCounter + 1

    new_line = str(new_line)

    machineArr.insert(tempCounter, new_line)

    #new line after each write
    new_line = new_line + '\n'

    #reads all lines
    with open(fileName3, 'r') as f:
        lines = f.readlines()

    #modify specific line
    if lineCounterM - 1 < len(lines):
        lines[lineCounterM - 1] = new_line
    else:
        lines.append(new_line)  # Append the new line if the file has fewer lines

    #write all lines back to the file
    with open(fileName3, 'w') as f:
        f.writelines(lines)

    return 0

#-----------------------------------------------------
#issue, its defaulting the last addon to 0000
lineCount = 0
tempC = 0
liability = 0
from betaCompiler import arrayC

def assembler(fileName, i):
    global lineCounterM, array, lineCount, tempC, liability
    with open(fileName, 'r') as g:    #opens file that is going to be converted
        line2 = g.readlines()   #saves whole value to varuable
        line2b = line2[i]   #saves specified line to variable
        line2c = re.split('[, \n]', line2b) #splits line up at whitespaces and ,        {If this doesnt work do 'line2b.split() + line2b.split(',')}
            #need \n, added \n to all lines at somepoint
    if (line2c[0] == "a"):  #Check the varibles
        writeBack('FF 0005')    #FF (Variable) 0000 (Memory Location)

    elif (line2c[0] == "b"):
        writeBack('FF 0006')

    elif (line2c[0] == "c"):
        writeBack('FF 0007')

    elif (line2c[0] == "x"):
        writeBack('FF 0008')

    elif (line2c[0] == "y"):
        writeBack('FF 0009')

    elif (line2c[0] == "z"):
        writeBack('FF 0010')

    elif (line2c[0] == "mov"): #['mov', 'eax', '', 'y', '']
        #this is where I'd add in a check for if a register was changed
        var1 = line2c[1]
        var2 = line2c[3]
    
        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        elif (var1 == "a"):
            var1 = '0005 '
        elif (var1 == "b"):
            var1 = '0006 '
        elif (var1 == "c"):
            var1 = '0007 '
        elif (var1 == "x"):
            var1 = '0008 '
        elif (var1 == "y"):
            var1 = '0009 '
        elif (var1 == "z"):
            var1 = '0010 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        elif (var2 == "a"):
            var2 = '0005 '
        elif (var2 == "b"):
            var2 = '0006 '
        elif (var2 == "c"):
            var2 = '0007 '
        elif (var2 == "x"):
            var2 = '0008 '
        elif (var2 == "y"):
            var2 = '0009 '
        elif (var2 == "z"):
            var2 = '0010 '
        else:
            var2 = '0000 '  #representation for just numbers
            
        var4 = '00 ' + var1 + var2
        writeBack(var4)

    elif (line2c[0] == "add"):  # add xxxx xxxx xxxx : 0 1 2 3
        var1 = line2c[1]
        var2 = line2c[2]
        var3 = line2c[3]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'A ' + var1 + var2 + var3
        writeBack(var4)
       
    elif (line2c[0] == "sub"):
        var1 = line2c[1]
        var2 = line2c[2]
        var3 = line2c[3]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'B ' + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "mult"):
        var1 = line2c[1]
        var2 = line2c[2]
        var3 = line2c[3]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'C ' + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "div"):
        var1 = line2c[1]
        var2 = line2c[2]
        var3 = line2c[3]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'D ' + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "addadd"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'AA ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "addsub"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'AB ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "adddiv"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'AD ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "addmult"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'AC ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "subadd"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'BA ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "subsub"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'BB ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "submult"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'BC ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "subdiv"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'BD '+ var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "multadd"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'CA '+ var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "multsub"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'CB ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "multmult"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'CC ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "multdiv"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'CD ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "divadd"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'DA ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "divsub"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'DB ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "divmult"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'DC ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "divdiv"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var0 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'DD ' + var0 + var1 + var2 + var3
        writeBack(var4)

    elif (line2c[0] == "cmp"): #cmp x, y : 0 1 2
        var1 = line2c[1]
        var2 = line2c[2]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '


        var4 = 'CC ' + var1 + var2
        writeBack(var4)

    elif (line2c[0] == "jmp"):
        var4 = arrayC[tempC]
        tempC = tempC + 1

        var4 = str(var4)
        var4 = 'E0 ' + var4
        writeBack(var4)

    elif (line2c[0] == "jl"):
        var4 = arrayC[tempC]
        tempC = tempC + 1
        
        var4 = str(var4)
        var4 = 'E1 ' + var4
        writeBack(var4)

    elif (line2c[0] == "jle"):
        var4 = arrayC[tempC]
        tempC = tempC + 1
        
        var4 = str(var4)
        var4 = 'E2 ' + var4
        writeBack(var4)

    elif (line2c[0] == "jg"):
        var4 = arrayC[tempC]
        tempC = tempC + 1
        
        var4 = str(var4)
        var4 = 'E3 ' + var4
        writeBack(var4)

    elif (line2c[0] == "jge"):
        var4 = arrayC[tempC]
        tempC = tempC + 1
        
        var4 = str(var4)
        var4 = 'E4 ' + var4
        writeBack(var4)

    elif (line2c[0] == "jne"):
        var4 = arrayC[tempC]
        tempC = tempC + 1
        
        var4 = str(var4)
        var4 = 'E5 ' + var4
        writeBack(var4)

    elif (line2c[0] == "je"):
        var4 = arrayC[tempC]
        tempC = tempC + 1
        
        var4 = str(var4)
        var4 = 'E6 ' + line2c[1]
        writeBack(var4)

    elif (line2c[0] == "push"):
        var1 = line2c[1]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000'   #Might actual cause an error

        var4 = 'FA ' + var1
        writeBack(var4)

    elif (line2c[0] == "pop"):
        var1 = line2c[1]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000'   #Might actual cause an error

        var4 = 'FF' + var1
        writeBack(var4)

    elif (line2c[0].strip() == ""): #checks for blank lines : Don't know if we actually need this
        if (liability == 1):
            liability = liability -1 #idea is that it saves a address after empty space located after a label in ASM
            array.append(lineCounterM)
        writeBack("")

    elif (line2c[0] == "print"): #print \n
        if (line2c[1] == '\n'):
            var4 = '6666'
        elif (line2c[1] == 'a'):
            var4 = '0005'
        elif (line2c[1] == 'b'):
            var4 = '0006'
        elif (line2c[1] == 'c'):
            var4 = '0007'
        elif (line2c[1] == 'x'):
            var4 = '0008'
        elif (line2c[1] == 'y'):
            var4 = '0009'
        elif (line2c[1] == 'z'):
            var4 = '0010'
        else:
            var4 = '0000'

        printVar = 'EE ' + var4
        writeBack(printVar)
        #print (line2c[0])  Done in the compiling

    elif (':' in line2c[0]): #original: line2c[0].endswith == ":"
        writeBack(lineCounterM + 1)

    elif (line2c[0] == 'exit'):
        return 0

    else:
        #error handling
        print("Error at assembler at line ", lineCounterM)
    

    #idea of putting a blank row for csv indication : writeBack('')
    return 0

