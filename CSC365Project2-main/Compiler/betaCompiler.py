#-----------------------------------------------------------------------------------------------------
#NOTES:
#-----------------------------------------------------------------------------------------------------
#If a varible was signed or unsigned. Would i need to have a manual check for if its outside of that number range so that it gives an error message?



#-----------------------------------------------------------------------------------------------------
#variables/imports
#-----------------------------------------------------------------------------------------------------
import re
import ASM
import CSV


#dummy variable
lineCounterASM = '' #their are 389 uses of this function, that I'll clean up later

fileName = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\HighLevelCode.txt")
fileName2 = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\Assembly.txt")

#variables
i = 0
lineCounterASMR = 0 #for the ASM
whileCheck = 'false'
ifCheck = 'false'
elseCheck = 'false'
indentCheck = 'false'
whileStatement = ''
whileLine = 0

arrayAlign = 0  #place holder number to help align things in the csv file

#arrays
modReg = []         #register updates
modFlags = []       #flag updates
YMCArr = []         #keeps track of address's

#forr csv, might be easier to just put everything in arrays, depending on function it'd change the spaceing, then feed arrays to csv function
#ignore spacing, just use as indication
#have it write as its beign read, or run sepearte later
HLCArr = []
ASMArr = []
MachArr = []


#only positive                  Range: 0 to 255  (unsigned)
a = 0
b = 0
c = 0

#both positive and negative     Range: -128 to 127  (Signed)
x = 0
y = 0
z = 0

#registers
eax = 0
ebx = 0
ecx = 0
edx = 0

#placeHolder registers (to check for changes)
eax2 = 0
ebx2 = 0
ecx2 = 0
edx2 = 0

#-----------------------------------------------------
#writeASM fucntion (for HLC to ASM)
#-----------------------------------------------------
def writeASM (new_line):    
    global lineCounterASMR, fileName2, arrayAlign, ASMArr      #to many statements already include the other import
    lineCounterASMR = lineCounterASMR + 1  # increments the line for each time its added to for ASM
    arrayAlign = arrayAlign + 1
    
    ASMArr.insert(arrayAlign, new_line)

    #new line after each write
    new_line = new_line + '\n'

    if (indentCheck == 'true'):
        new_line = '\t' + new_line

    # Read all lines
    with open(fileName2, 'r') as f:
        lines = f.readlines()

    # Modify the specific line
    if lineCounterASMR - 1 < len(lines): 
        lines[lineCounterASMR - 1] = new_line   
    else:
        lines.append(new_line)  # Append the new line if the file has fewer lines

    # Write all lines back to the file
    with open(fileName2, 'w') as f:
        f.writelines(lines)

    return 0

#-----------------------------------------------------------------------------------------------------
#register updates
#-----------------------------------------------------------------------------------------------------
#stores its own backup registers after each line and compares. if something was changed, it will show on the csv file

def regCheck ():
    regChanges = ''   #reset before check
    global eax2, ebx2, ecx2, edx2, eax, ebx, ecx, edx   #gets from global, all changes made will stay

    if (eax != eax2):
       regChanges = regChanges + ' eax '
       eax2 = eax
    if (ebx != ebx2):
       regChanges = regChanges + ' ebx '
       ebx2 = ebx
    if (ecx != ecx2):
       regChanges = regChanges + ' ecx '
       ecx2 = ecx
    if (edx != edx2):
       regChanges = regChanges + ' edx '
       edx2 = edx
    
    return regChanges

#-----------------------------------------------------------------------------------------------------
#indent printer (prints, to different text file the conversion, but doesn't acutally process them)
#-----------------------------------------------------------------------------------------------------
def justPrint(placeHolder):
    global elseCheck
    temp = len(placeHolder)
    #might need to split placeholder in here?

    if (temp == 4): #b = 3 : 0 1 2
        var4 = 'mov ' + placeHolder[0] + ', ' + placeHolder[2]
        writeASM(var4)

    elif (temp == 6): #y = a + b : 0 1 2 3 4 
        var4 = 'mov eax, ' + placeHolder[2]
        writeASM(var4)
        var4 = 'mov ebx, ' + placeHolder[4]
        writeASM(var4)

        if (placeHolder[3] == '+'):
            var4 = 'add eax eax ebx'
        elif (placeHolder[3] == '-'):
            var4 = 'sub eax eax ebx'
        elif (placeHolder[3] == '*'):
            var4 = 'mult eax eax ebx'
        elif (placeHolder[3] == '/'):
            var4 = 'div eax eax ebx'
        else:
            print('NoPrint: Error Temp5')

        writeASM(var4)
        var4 = 'mov ' + placeHolder[0] + ', eax'
        writeASM(var4)

    elif (temp == 8): #y = a + b - c : 0 1 2 3 4 5 6 
        var4 = 'mov eax, ' + placeHolder[2]
        writeASM(var4)
        var4 = 'mov ebx, ' + placeHolder[4]
        writeASM(var4)
        var4 = 'mov ebc, ' + placeHolder[6]
        writeASM(var4)
        
        if (placeHolder[3] == '+'):
            p1 = 'add'
        elif (placeHolder[3] == '-'):
            p1 = 'sub'
        elif (placeHolder[3] == '*'):
            p1 = 'mult'
        elif (placeHolder[3] == '/'):
            p1 = 'div'
        else:
            print('NoPrint: Error Temp7: 3')

        if (placeHolder[5] == '+'):
            p2 = 'add'
        elif (placeHolder[5] == '-'):
            p2 = 'sub'
        elif (placeHolder[5] == '*'):
            p2 = 'mult'
        elif (placeHolder[5] == '/'):
            p2 = 'div'
        else:
            print('NoPrint: Error Temp7: 5')
        
        temp2 = p1 + p2

        var4 = temp2 + ' eax eax ebx ecx'
        writeASM(var4)

        var4 = 'mov ' + placeHolder[0] + ', eax'
        writeASM(var4)

    else:
        print('justPrint: Temp Error')

    #clumps up what each action does
    writeASM('\t')
    return 0

#-----------------------------------------------------------------------------------------------------
#YMC Addressing
#-----------------------------------------------------------------------------------------------------
#starts at 0011

def YMCAddress():
    global YMCArr, lineCounterASMR
    var4 = lineCounterASMR + 11
    YMCArr.append(var4)

    return 0

#-----------------------------------------------------------------------------------------------------
#flags
#-----------------------------------------------------------------------------------------------------
#make a function to be ran after each step for the flags to be updated
#reset at beginning of function, output to csv file
#maybe make seperate file
overflowF = False
zeroF = False
carryF = False #only true, when a signed/unsigned is borrowed (goes out of range, but is in differnt range): like 1011 is 8 4 2 1 : for signed its -8 4 2 1
signF = False
flagArr = []


#checks most significant bit : true = 1 and false = 0
def checkSign(n):
    return bool(n & 0x80)

def flagCarrier():
    global overflowF, zeroF, carryF, signF, flagArr
    #overFlow = set when signed value overflows
    #carry = set with unsigned values overflows out
    #zero = arithmetic result = 0
    #sign = 1 in most sognificant bit

    #for math: eax stores the result so just check that


    var4 = ''   #initialize to makes sure its clear
    
    if (carryF == True):
        carryF = False
        var4 = var4 + ' CF '

    if (signF == True):
        signF = False
        var4 = var4 + ' SF '

    if (overflowF == True):
        overflowF = False
        var4 = var4 + ' OF '
    
    if (zeroF == True):
        zeroF = False
        var4 = var4 + ' ZF '

    #flagArr.append(var4)


    return var4

#-----------------------------------------------------------------------------------------------------
#math function (This sucked)
#-----------------------------------------------------------------------------------------------------
#Do not make me move all those lines over by a indent space
def mathStuff(placeHolder): #do I need to import the variables and registers
    global a, b, c, x, y, z, eax, ebx, ecx, edx, zeroF, carryF, overflowF,signF   #gets from global, all changes made will stay
    temp = len(placeHolder)

    #['a', '=', '3', ''] = 4
    #['b', '=', '15', '+', 'a', ''] = 6
    #['b', '=', '15', '+', 'a', '/', '2', ''] = 8

    if (temp == 4): # b = 3 or b = a : 0 1 2
        #this is where the zero flag will go
        if (placeHolder[0] == 'a'):
            if (placeHolder[2] == 'a'):
                eax = a
                a = eax
                writeASM('mov eax, a')
                writeASM('mov a, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                a = eax
                writeASM('mov eax, b')
                writeASM('mov a, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                a = eax
                writeASM('mov eax, c')
                writeASM('mov a, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                a = eax
                writeASM('mov eax, x')
                writeASM('mov a, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                a = eax
                writeASM('mov eax, y')
                writeASM('mov a, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                a = eax
                writeASM('mov eax, z')
                writeASM('mov a, eax')

            else:
                eax = placeHolder[2]
                a = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov a, eax')

        elif (placeHolder[0] == 'b'):
            if (placeHolder[2] == 'a'):
                eax = a
                b = eax
                writeASM('mov eax, a')
                writeASM('mov b, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                b = eax
                writeASM('mov eax, b')
                writeASM('mov b, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                b = eax
                writeASM('mov eax, c')
                writeASM('mov b, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                b = eax
                writeASM('mov eax, x')
                writeASM('mov b, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                b = eax
                writeASM('mov eax, y')
                writeASM('mov b, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                b = eax
                writeASM('mov eax, z')
                writeASM('mov b, eax')

            else:
                eax = placeHolder[2]
                b = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov b, eax')

        elif (placeHolder[0] == 'c'):
            if (placeHolder[2] == 'a'):
                eax = a
                c = eax
                writeASM('mov eax, a')
                writeASM('mov c, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                c = eax
                writeASM('mov eax, b')
                writeASM('mov c, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                c = eax
                writeASM('mov eax, c')
                writeASM('mov c, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                c = eax
                writeASM('mov eax, x')
                writeASM('mov c, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                c = eax
                writeASM('mov eax, y')
                writeASM('mov c, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                c = eax
                writeASM('mov eax, z')
                writeASM('mov c, eax')

            else:
                eax = placeHolder[2]
                c = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov c, eax')

        elif (placeHolder[0] == 'x'):
            if (placeHolder[2] == 'a'):
                eax = a
                x = eax
                writeASM('mov eax, a')
                writeASM('mov x, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                x = eax
                writeASM('mov eax, b')
                writeASM('mov x, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                x = eax
                writeASM('mov eax, c')
                writeASM('mov x, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                x = eax
                writeASM('mov eax, x')
                writeASM('mov x, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                x = eax
                writeASM('mov eax, y')
                writeASM('mov x, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                x = eax
                writeASM('mov eax, z')
                writeASM('mov x, eax')

            else:
                eax = placeHolder[2]
                x = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov x, eax')

        elif (placeHolder[0] == 'y'):
            if (placeHolder[2] == 'a'):
                eax = a
                y = eax
                writeASM('mov eax, a')
                writeASM('mov y, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                y = eax
                writeASM('mov eax, b')
                writeASM('mov y, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                y = eax
                writeASM('mov eax, c')
                writeASM('mov y, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                y = eax
                writeASM('mov eax, x')
                writeASM('mov y, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                y = eax
                writeASM('mov eax, y')
                writeASM('mov y, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                y = eax
                writeASM('mov eax, z')
                writeASM('mov y, eax')

            else:
                eax = placeHolder[2]
                y = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov y, eax')

        elif (placeHolder[0] == 'z'):
            if (placeHolder[2] == 'a'):
                eax = a
                z = eax
                writeASM('mov eax, a')
                writeASM('mov z, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                z = eax
                writeASM('mov eax, b')
                writeASM('mov z, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                z = eax
                writeASM('mov eax, c')
                writeASM('mov z, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                z = eax
                writeASM('mov eax, x')
                writeASM('mov z, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                z = eax
                writeASM('mov eax, y')
                writeASM('mov z, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                z = eax
                writeASM('mov eax, z')
                writeASM('mov z, eax')

            else:
                eax = placeHolder[2]
                z = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov z, eax')

        else:
            print('Compiler: Error for temp3 in abc')

    elif (temp == 6): #basic math : 0 1 2 3 4 : y = a + b
        #move varible to register eax
        if (placeHolder[2] == 'a'): 
            eax = a
            writeASM('mov eax, a')
        elif (placeHolder[2] == 'b'):
            eax = b
            writeASM('mov eax, b')
        elif (placeHolder[2] == 'c'):
            eax = c
            writeASM('mov eax, c')
        elif (placeHolder[2] == 'x'):
            eax = x
            writeASM('mov eax, x')
        elif (placeHolder[2] == 'y'):
            eax = y
            writeASM('mov eax, y') 
        elif (placeHolder[2] == 'z'):
            eax = z
            writeASM('mov eax, z')
        else:
            eax = placeHolder[2]
            var4 = 'mov eax, ' + placeHolder[2]
            writeASM(var4)

        #move varible to register ebx
        if (placeHolder[4] == 'a'):
            ebx = a
            writeASM('mov ebx, a')
        elif (placeHolder[4] == 'b'):
            ebx = b
            writeASM('mov ebx, b')
        elif (placeHolder[4] == 'c'):
            ebx = c
            writeASM('mov ebx, c')
        elif (placeHolder[4] == 'x'):
            ebx = x
            writeASM('mov ebx, x')
        elif (placeHolder[4] == 'y'):
            ebx = y
            writeASM('mov ebx, y')
        elif (placeHolder[4] == 'z'):
            ebx = c
            writeASM('mov ebx, z')
        else:
            ebx = placeHolder[4]
            var4 = 'mov ebx, ' + placeHolder[4]
            writeASM(var4)

        #above else statments take in the placeholders to the varibales
        eax = int(eax)
        ebx = int(ebx)
        ecx = int(ecx)
        edx = int(edx)

        #does arithmetic and writes to txt assembly conversion
        if (placeHolder[0] == 'a'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                a = eax
                writeASM('add eax eax ebx')
                writeASM('mov a, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                a = eax
                writeASM('sub eax eax ebx')
                writeASM('mov a, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                a = eax
                writeASM('mult eax eax ebx')
                writeASM('mov a, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                a = eax
                writeASM('div eax eax ebx')
                writeASM('mov a, eax')

            else:
                print('Compiler: Error for Operator type in abc')
                
        elif (placeHolder[0] == 'b'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                b = eax
                writeASM('add eax eax ebx')
                writeASM('mov b, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                b = eax
                writeASM('sub eax eax ebx')
                writeASM('mov b, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                b = eax
                writeASM('mult eax eax ebx')
                writeASM('mov b, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                b = eax
                writeASM('div eax eax ebx')
                writeASM('mov b, eax')

            else:
                print('Compiler: Error for Operator type in abc')                

        elif (placeHolder[0] == 'c'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                c = eax
                writeASM('add eax eax ebx')
                writeASM('mov c, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                c = eax
                writeASM('sub eax eax ebx')
                writeASM('mov c, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                c = eax
                writeASM('mult eax eax ebx')
                writeASM('mov c, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                c = eax
                writeASM('div eax eax ebx')
                writeASM('mov c, eax')

            else:
                print('Compiler: Error for Operator type in abc')   

        elif (placeHolder[0] == 'x'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                x = eax
                writeASM('add eax eax ebx')
                writeASM('mov x, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                x = eax
                writeASM('sub eax eax ebx')
                writeASM('mov x, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                x = eax
                writeASM('mult eax eax ebx')
                writeASM('mov x, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                x = eax
                writeASM('div eax eax ebx')
                writeASM('mov x, eax')

            else:
                print('Compiler: Error for Operator type in abc')            

        elif (placeHolder[0] == 'y'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                y = eax
                writeASM('add eax eax ebx')
                writeASM('mov y, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                y = eax
                writeASM('sub eax eax ebx')
                writeASM('mov y, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                y = eax
                writeASM('mult eax eax ebx')
                writeASM('mov y, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                y = eax
                writeASM('div eax eax ebx')
                writeASM('mov y, eax')

            else:
                print('Compiler: Error for Operator type in abc')

        elif (placeHolder[0] == 'z'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                z = eax
                writeASM('add eax eax ebx')
                writeASM('mov z, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                z = eax
                writeASM('sub eax eax ebx')
                writeASM('mov z, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                z = eax
                writeASM('mult eax eax ebx')
                writeASM('mov z, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                z = eax
                writeASM('div eax eax ebx')
                writeASM('mov z, eax')

            else:
                print('Compiler: Error for Operator type in abc')

        else:
            print ('Compiler: Error at temp5 abc')

    elif (temp == 8): #2 types for the math : Y = X + Z + 3 : 0 1 2 3 4 5 6
        #move varible to register eax
        if (placeHolder[2] == 'a'): 
            eax = a
            writeASM('mov eax, a')
        elif (placeHolder[2] == 'b'):
            eax = b
            writeASM('mov eax, b')
        elif (placeHolder[2] == 'c'):
            eax = c
            writeASM('mov eax, c')
        elif (placeHolder[2] == 'x'):
            eax = x
            writeASM('mov eax, x')
        elif (placeHolder[2] == 'y'):
            eax = y
            writeASM('mov eax, y') 
        elif (placeHolder[2] == 'z'):
            eax = z
            writeASM('mov eax, z')
        else:
            eax = placeHolder[2]
            var4 = 'mov eax, ' + placeHolder[2]
            writeASM(var4)

        #move varible to register ebx
        if (placeHolder[4] == 'a'):
            ebx = a
            writeASM('mov ebx, a')
        elif (placeHolder[4] == 'b'):
            ebx = b
            writeASM('mov ebx, b')
        elif (placeHolder[4] == 'c'):
            ebx = c
            writeASM('mov ebx, c')
        elif (placeHolder[4] == 'x'):
            ebx = x
            writeASM('mov ebx, x')
        elif (placeHolder[4] == 'y'):
            ebx = y
            writeASM('mov ebx, y')
        elif (placeHolder[4] == 'z'):
            ebx = c
            writeASM('mov ebx, z')
        else:
            ebx = placeHolder[4]
            var4 = 'mov ebx, ' + placeHolder[4]
            writeASM(var4)
    
        #move varible to register ecx
        if (placeHolder[6] == 'a'):
            ecx = a
            writeASM('mov ecx, a')
        elif (placeHolder[6] == 'b'):
            ecx = b
            writeASM('mov ecx, b')
        elif (placeHolder[6] == 'c'):
            ecx = c
            writeASM('mov ecx, c')
        elif (placeHolder[6] == 'x'):
            ecx = x
            writeASM('mov ecx, x')
        elif (placeHolder[6] == 'y'):
            ecx = y
            writeASM('mov ecx, y')
        elif (placeHolder[6] == 'z'):
            ecx = c
            writeASM('mov ecx, z')
        else:
            ecx = placeHolder[6]
            var4 = 'mov ecx, ' + placeHolder[6]
            writeASM(var4)       
    
        #above else statments take in the placeholders to the varibales
        eax = int(eax)
        ebx = int(ebx)
        ecx = int(ecx)
        edx = int(edx)

        #does double arithmetic and converts to assembly
        if (placeHolder[0] == 'a'): # Y = X + Z + 3 : 0 1 2 3 4 5 6
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    a = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    a = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    a = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    a = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    a = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    a = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    a = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    a = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    a = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    a = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    a = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    a = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    a = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    a = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    a = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    a = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic parta')

        elif (placeHolder[0] == 'b'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    b = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    b = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    b = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    b = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    b = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    b = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    b = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    b = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    b = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    b = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    b = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    b = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    b = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    b = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    b = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    b = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partb')

        elif (placeHolder[0] == 'c'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    c = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    c = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    c = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    c = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    c = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    c = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    c = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    c = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    c = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    c = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    c = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    c = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    c = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    c = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    c = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    c = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partc')

        elif (placeHolder[0] == 'x'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    x = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    x = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    x = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    x = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov x, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    x = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    x = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    x = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    x = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    x = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    x = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    x = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    x = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov x, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    x = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    x = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    x = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    x = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov x, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partx')

        elif (placeHolder[0] == 'y'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    y = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    y = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    y = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    y = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    y = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    y = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    y = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    y = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    y = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    y = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    y = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    y = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    y = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    y = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    y = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    y = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic party')

        elif (placeHolder[0] == 'z'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    z = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    z = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    z = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    z = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    z = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    z = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    z = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    z = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    z = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    z = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    z = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    z = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    z = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    z = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    z = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    z = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partz')

        else:
            print('Compiler: Error in temp7')

    else:
        print("MathStuff: Temp Length is not right")

    #zero flag is set here : all results go through eax so
    if (eax == 0): 
        zeroF = True

    eax = int(eax)
    signF = checkSign(eax)
    #unsigned: a b c : 0 to 255 : carry flag
    #signed: x y z : -128 to 127 : overflow flag
    #they wrap around
    #Checks if any variables overflowed or carry after done 

    a = int(a)
    b = int(b)
    c = int(c)
    x = int(x)
    y = int(y)
    z = int(z)

    if (a < 0):
        a = a + 255
        carryF = True

    elif (a > 255):
        a = a - 255
        carryF = True

    if (b < 0):
        b = b + 255
        carryF = True

    elif (b > 255):
        b = b - 255
        carryF = True

    if (c < 0):
        c = c + 255
        carryF = True

    elif (c > 255):
        c = c - 255
        carryF = True
    
    if (x < -128):
        x = x + 255
        overflowF = True

    elif (x > 127):
        x = x - 255
        overflowF = True

    if (y < -128):
        y = y + 255
        overflowF = True

    elif (y > 127):
        y = y - 255
        overflowF = True

    if (z < -128):
        z = z + 255
        overflowF = True

    elif (z > 127):
        z = z - 255
        overflowF = True


    #clumps up what each action does
    writeASM('\t')
    return 0

#-----------------------------------------------------------------------------------------------------
#indent checker 
#-----------------------------------------------------------------------------------------------------
def checkIndent(filename, line_number):
    global indentCheck
    with open(filename, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == line_number and line.startswith('\t'):
                indentCheck = 'true'
                
            else:
                indentCheck = 'false'
    return 0

#-----------------------------------------------------------------------------------------------------
#parser
#-----------------------------------------------------------------------------------------------------
arrayC = []
liability = 0
placeHolder = ''

def betaParser (i):
    global a, b, c, x, y, z, whileCheck, lineCounterASMR, whileASMR, whileLine, ifCheck, eax, ebx, ecx, edx, fileName, whileStatement, arrayAlign
    global HLCArr, modFlags, modReg, arrayC, liability, placeHolder

    with open(fileName, 'r') as file:
        content = file.readlines()#reads all lines
        line2 = content[i] #gets line
        placeHolder = re.split('[ \n]', line2)  #splits line into words : just a space, this is meant more for more than one split type though

    #arrays to organize CSV file
    #HLCArr[arrayAlign] = line2 #might be better to use placeHolder
    HLCArr.insert(arrayAlign, line2)
    fF = flagCarrier()
    flagArr.insert(arrayAlign, fF)
    rR = regCheck() 
    modReg.insert(arrayAlign, rR)
    #asm array in write asm
    #also need YMC Address
    #also add machine code to ASM file

    #checks for \t in placeHolder[0]
    if '\t' in placeHolder[0]:
        placeHolder[0] = placeHolder[0].replace('\t', '')

    #statement to check if statment and else statments
    if (ifCheck == 'else' and elseCheck == 'false'):    #for if if statment was not good
        justPrint()
        return 0

    if (placeHolder[0] == "unsigned"):  #the varibles are consisnt with naming right?
        temp = len(placeHolder)

        if (temp == 3):
            var4 = placeHolder[1] + ' dd $'
            writeASM(var4)

        elif (temp == 4):
            var4 = placeHolder[1] + ' dd $'
            writeASM(var4)
            var4 = placeHolder[2] + ' dd $'
            writeASM(var4)
        elif (temp == 5):
            var4 = placeHolder[1] + ' dd $'
            writeASM(var4)
            var4 = placeHolder[2] + ' dd $'
            writeASM(var4)
            print(placeHolder)
            var4 = placeHolder[3] + ' dd $'
            writeASM(var4)
        else:
            print('Compiler: Temp error in unsigned/signed')
        writeASM('\t')

    elif (placeHolder[0] == "signed"):
        temp = len(placeHolder)

        if (temp == 3):
            var4 = placeHolder[1] + ' dd $'
            writeASM(var4)

        elif (temp == 4):
            var4 = placeHolder[1] + ' dd $'
            writeASM(var4)
            var4 = placeHolder[2] + ' dd $'
            writeASM(var4)
        elif (temp == 5):
            var4 = placeHolder[1] + ' dd $'
            writeASM(var4)
            var4 = placeHolder[2] + ' dd $'
            writeASM(var4)
            print(placeHolder)
            var4 = placeHolder[3] + ' dd $'
            writeASM(var4)
        else:
            print('Compiler: Temp error in unsigned/signed')
        writeASM('\t')

    elif (placeHolder[0].strip() == ""): #checks for blank lines : Don't know if we actually need this
        if (liability == 1):
            arrayC.append(lineCounterASMR)
            liability = liability - 1
        writeASM("")

    elif (placeHolder[0] == "print"):   #also needs to be added to the assemlby conversion : print y : 0 1
        if (placeHolder[1] == 'a'):
            print(a)
            writeASM('print a')
        elif (placeHolder[1] == 'b'):
            print(b)
            writeASM('print b')
        elif (placeHolder[1] == 'c'):
            print(c)
            writeASM('print c')
        elif (placeHolder[1] == 'x'):
            print(x)
            writeASM('print x')
        elif (placeHolder[1] == 'y'):
            print(y)
            writeASM('print y')
        elif (placeHolder[1] == 'z'):
            print(z)
            writeASM('print z')
        elif (placeHolder[1] == '\n'):
            print('\n')
            writeASM('print \n')
        elif (placeHolder[1] == '\\n'): #sometimes it adds a \
            print('\n')
            writeASM('print \n')
        else:
            var4 = 'print ' + placeHolder[1]
            writeASM(var4)
            print(var4)
        
    elif (placeHolder[0] == "if"): #Ex. y = 12 or y <= 3 : 1 2 3
        #check for type: <, >, <=, >=, =, !=

        #prints statement to assembly.txt
        var4 = 'cmp ' + placeHolder[1] + ', ' + placeHolder[3]
        writeASM(var4)

        if (placeHolder[2] == '<'):
            var4 = 'jl if'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter
        elif (placeHolder[2] == '>'):
            var4 = 'jg if'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter
        elif (placeHolder[2] == '<='):
            var4 = 'jle if'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter
        elif (placeHolder[2] == '>='):
            var4 = 'jge if'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter
        elif (placeHolder[2] == '!='):
            var4 = 'jne if'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter
        elif (placeHolder[2] == '='):
            var4 = 'je if' 
            writeASM(var4)  #can put at end of if statement to make shorter
        #else:
        var4 = 'jmp else'
        writeASM(var4)  #can put at end of if statement to make shorter

        writeASM('')
        writeASM('if:')

        #help specify address's
        arrayC.append(lineCounterASMR)
        liability = liability + 1

        #conflicts of varibles: type any
        a = int(a)
        b = int(b)
        c = int(c)
        x = int(x)
        y = int(y)
        z = int(z)

        #if Check will go to 'true' or 'false' depends on statement
        if (placeHolder[1] == 'a'): # while y > 0 : 0 1 2 3
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (a > a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (a > b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (a > c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (a > x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (a > y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (a > z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (a > int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (a < a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (a < b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (a < c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (a < x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (a < y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (a < z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (a < int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (a >= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (a >= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (a >= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (a >= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (a >= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (a >= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (a >= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (a <= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (a <= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (a <= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (a <= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (a <= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (a <= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (a <= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (a == a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (a == b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (a == c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (a == x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (a == y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (a == z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (a == int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (a != a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (a != b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (a != c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (a != x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (a != y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (a != z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (a != int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            else:
                print('Error in If statements')
            
        elif (placeHolder[1] == 'b'):
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (b > a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (b > b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (b > c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (b > x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (b > y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (b > z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (b > int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (b < a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (b < b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (b < c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (b < x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (b < y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (b < z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (b < int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (b >= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (b >= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (b >= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (b >= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (b >= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (b >= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (b >= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (b <= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (b <= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (b <= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (b <= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (b <= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (b <= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (b <= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (b == a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (b == b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (b == c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (b == x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (b == y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (b == z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (b == int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (b != a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (b != b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (b != c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (b != x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (b != y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (b != z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (b != int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            else:
                print('Error in If statements')
                
        elif (placeHolder[1] == 'c'):
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (c > a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (c > b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (c > c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (c > x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (c > y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (c > z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (c > int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (c < a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (c < b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (c < c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (c < x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (c < y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (c < z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (c < int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (c >= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (c >= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (c >= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (c >= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (c >= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (c >= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (c >= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (c <= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (c <= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (c <= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (c <= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (c <= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (c <= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (c <= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (c == a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (c == b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (c == c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (c == x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (c == y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (c == z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (c == int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (c != a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (c != b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (c != c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (c != x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (c != y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (c != z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (c != int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'x'):
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (x > a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (x > b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (x > c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (x > x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (x > y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (x > z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (x > int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (x < a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (x < b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (x < c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (x < x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (x < y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (x < z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (x < int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (x >= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (x >= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (x >= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (x >= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (x >= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (x >= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (x >= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (x <= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (x <= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (x <= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (x <= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (x <= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (x <= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (x <= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (x == a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (x == b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (x == c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (x == x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (x == y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (x == z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (x == int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (x != a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (x != b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (x != c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (x != x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (x != y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (x != z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (x != int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'y'):
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (y > a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (y > b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (y > c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (y > x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (y > y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (y > z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (y > int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (y < a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (y < b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (y < c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (y < x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (y < y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (y < z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (y < int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (y >= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (y >= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (y >= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (y >= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (y >= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (y >= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (y >= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (y <= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (y <= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (y <= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (y <= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (y <= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (y <= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (y <= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (y == a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (y == b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (y == c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (y == x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (y == y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (y == z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (y == int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (y != a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (y != b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (y != c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (y != x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (y != y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (y != z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (y != int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'z'):
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (z > a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (z > b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (z > c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (z > x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (z > y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (z > z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (z > int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (z < a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (z < b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (z < c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (z < x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (z < y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (z < z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (z < int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (z >= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (z >= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (z >= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (z >= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (z >= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (z >= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (z >= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (z <= a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (z <= b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (z <= c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (z <= x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (z <= y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (z <= z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (z <= int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (z == a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (z == b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (z == c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (z == x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (z == y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (z == z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (z == int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (z != a):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'b'):
                    if (z != b):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'c'):
                    if (z != c):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'x'):
                    if (z != x):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'y'):
                    if (z != y):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                elif(placeHolder[3] == 'z'):
                    if (z != z):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else'

                else:
                    if (z != int(placeHolder[3])):
                        ifCheck = 'true' 
                    else:
                        ifCheck = 'else' 

            else:
                print('Error in If statements')

        else:
            print('Compiler: Error for whileCheck creation')
            
    elif (placeHolder[0] == "else"):
        #make labels in assembly 
        writeASM('else:')

        #help specify address's
        arrayC.append(lineCounterASMR)
        liability = liability + 1

        if (ifCheck == 'true'):
            elseCheck = 'false'
        elif (ifCheck == 'else'):
            elseCheck = 'true'

    elif (placeHolder[0] == "while"):
        #don't need to worry about writing error, because it will overwrite itself
        whileCheck = 'true'

        #values to store for later
        whileStatement = placeHolder
        whileASMR = lineCounterASMR
        whileLine = i

        var4 = 'cmp ' + placeHolder[1] + ', ' + placeHolder[3]
        writeASM(var4)

        #Checks statment: prints jump
        if (placeHolder[2] == '<'): # while y = 3
            var4 = 'jl while'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '>'):
            var4 = 'jg while'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '<='):
            var4 = 'jle while'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '>='):
            var4 = 'jge while'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter
            
        elif (placeHolder[2] == '!='):
            var4 = 'jne while'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '='):
            var4 = 'je while'
            writeASM(var4)  #can put at end of if statement to make shorter 

        else:
            var4 = 'jmp end'
            writeASM(var4)  #can put at end of if statement to make shorter

        writeASM('')
        writeASM('while:')  #label for asm jump

        #help specify address's
        arrayC.append(lineCounterASMR)
        liability = liability + 1


        #conflicts of varibles: type any
        a = int(a)
        b = int(b)
        c = int(c)
        x = int(x)
        y = int(y)
        z = int(z)
    
        #while Check will go to 'true' or 'false' depends on statement
        if (placeHolder[1] == 'a'): # while y > 0 : 0 1 2 3
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (a > a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (a > b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (a > c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (a > x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (a > y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (a > z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (a > int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (a < a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (a < b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (a < c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (a < x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (a < y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (a < z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (a < int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (a >= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (a >= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (a >= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (a >= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (a >= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (a >= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (a >= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (a <= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (a <= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (a <= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (a <= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (a <= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (a <= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (a <= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (a == a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (a == b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (a == c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (a == x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (a == y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (a == z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (a == int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (a != a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (a != b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (a != c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (a != x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (a != y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (a != z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (a != int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            else:
                print('Error in If statements')
            
        elif (placeHolder[1] == 'b'):
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (b > a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (b > b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (b > c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (b > x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (b > y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (b > z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (b > int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (b < a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (b < b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (b < c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (b < x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (b < y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (b < z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (b < int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (b >= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (b >= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (b >= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (b >= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (b >= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (b >= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (b >= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (b <= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (b <= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (b <= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (b <= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (b <= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (b <= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (b <= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (b == a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (b == b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (b == c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (b == x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (b == y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (b == z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (b == int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (b != a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (b != b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (b != c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (b != x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (b != y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (b != z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (b != int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            else:
                print('Error in If statements')
                
        elif (placeHolder[1] == 'c'):
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (c > a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (c > b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (c > c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (c > x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (c > y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (c > z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (c > int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (c < a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (c < b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (c < c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (c < x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (c < y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (c < z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (c < int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (c >= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (c >= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (c >= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (c >= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (c >= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (c >= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (c >= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (c <= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (c <= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (c <= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (c <= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (c <= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (c <= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (c <= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (c == a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (c == b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (c == c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (c == x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (c == y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (c == z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (c == int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (c != a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (c != b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (c != c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (c != x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (c != y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (c != z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (c != int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'x'):
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (x > a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (x > b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (x > c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (x > x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (x > y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (x > z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (x > int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (x < a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (x < b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (x < c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (x < x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (x < y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (x < z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (x < int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (x >= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (x >= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (x >= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (x >= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (x >= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (x >= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (x >= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (x <= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (x <= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (x <= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (x <= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (x <= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (x <= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (x <= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (x == a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (x == b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (x == c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (x == x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (x == y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (x == z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (x == int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (x != a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (x != b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (x != c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (x != x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (x != y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (x != z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (x != int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'y'):
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (y > a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (y > b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (y > c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (y > x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (y > y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (y > z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (y > int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (y < a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (y < b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (y < c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (y < x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (y < y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (y < z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (y < int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (y >= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (y >= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (y >= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (y >= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (y >= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (y >= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (y >= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (y <= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (y <= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (y <= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (y <= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (y <= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (y <= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (y <= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (y == a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (y == b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (y == c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (y == x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (y == y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (y == z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (y == int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (y != a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (y != b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (y != c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (y != x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (y != y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (y != z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (y != int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'z'):
            if (placeHolder[2] == '>'):
                if(placeHolder[3] == 'a'):
                    if (z > a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (z > b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (z > c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (z > x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (z > y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (z > z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (z > int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<'):
                if(placeHolder[3] == 'a'):
                    if (z < a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (z < b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (z < c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (z < x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (z < y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (z < z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (z < int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '>='):
                if(placeHolder[3] == 'a'):
                    if (z >= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (z >= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (z >= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (z >= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (z >= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (z >= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (z >= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '<='):
                if(placeHolder[3] == 'a'):
                    if (z <= a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (z <= b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (z <= c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (z <= x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (z <= y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (z <= z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (z <= int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '='):
                if(placeHolder[3] == 'a'):
                    if (z == a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (z == b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (z == c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (z == x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (z == y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (z == z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (z == int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            elif (placeHolder[2] == '!='):
                if(placeHolder[3] == 'a'):
                    if (z != a):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'b'):
                    if (z != b):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'c'):
                    if (z != c):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'x'):
                    if (z != x):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'y'):
                    if (z != y):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                elif(placeHolder[3] == 'z'):
                    if (z != z):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false'

                else:
                    if (z != int(placeHolder[3])):
                        whileCheck = 'true' 
                    else:
                        whileCheck = 'false' 

            else:
                print('Error in If statements')

        else:
            print('Compiler: Error for whileCheck creation')

    elif (placeHolder[0] == "a" or "b" or "c" or "x" or "y" or "z"): #only positive range: 0 to 255
        #check lenght to figure out whats happening
        #3 = declaration, 5 = regular arithmetic, 7 = double arithmetic
        mathStuff(placeHolder) 

    else:
        print("Error for Parser")

    return 0

#---------------------------------------------------------------------
#Start to run stuff together
#---------------------------------------------------------------------
def projectCompiler(i):
    global whileCheck, whileASMR, ifCheck, elseCheck, fileName, placeHolder, lineCounterASMR, arrayAlign

    global a, b, c, x, y, z #putting this down in case its not keeping the varibales properely

    #just leave some empty space in the HLC after for error prevention
    lineG = CSV.lineCount(fileName) -3
    #if no empty line after code no error : lineG = CSV.lineCount(fileName) - 1
    #if empty line after code no error : lineG = CSV.lineCount(fileName) - 3



    while (i <= lineG):    #i = line number currently on
        indentCheck = checkIndent(fileName, i)

        if (indentCheck == 'true'):
            if (whileCheck == 'true'):
                placeHolder = whileStatement
                #checks before function
                #while Check will go to 'true' or 'false' depends on statement
                if (placeHolder[1] == 'a'): # while y > 0 : 0 1 2 3
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (a > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (a < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (a >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (a <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (a == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (a != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')
                    
                elif (placeHolder[1] == 'b'):
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (b > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (b < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (b >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (b <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (b == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (b != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')
                        
                elif (placeHolder[1] == 'c'):
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (c > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (c < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (c >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (c <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (c == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (c != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')
                    
                elif(placeHolder[1] == 'x'):
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (x > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (x < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (x >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (x <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (x == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (x != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')
                    
                elif(placeHolder[1] == 'y'):
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (y > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (y < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (y >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (y <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (y == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (y != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')
                    
                elif(placeHolder[1] == 'z'):
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (z > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (z < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (z >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (z <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (z == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (z != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')

                else:
                    print('Compiler: Error for whileCheck creation')

            else:
                #if this ends up in a funcion add global varibales
                #reset so they dont mistake them
                ifCheck = 'false'
                whileCheck = 'false'
                elseCheck = 'false'

        elif (indentCheck == 'false'): #means its outside of if or while loop
            if (whileCheck == 'true'): #only reset variables if outside of loop an while statments not fufilled
                #resets while so that the lineCounterASMR and whileCounter are back where they started
                lineCounterASMR =  whileASMR #resets linecounterASMR to where while conversion started
                i = whileLine + 1 # resets i to go back to HLC line
        elif (whileCheck == 'true'):
            if (placeHolder[0].strip() == ''): #only reset variables if outside of loop an while statments not fufilled
                #resets while so that the lineCounterASMR and whileCounter are back where they started
                lineCounterASMR =  whileASMR #resets linecounterASMR to where while conversion started
                i = whileLine + 1 # resets i to go back to HLC line

            if (whileCheck == 'true'):
                placeHolder = whileStatement
                #checks before function
                #while Check will go to 'true' or 'false' depends on statement
                if (placeHolder[1] == 'a'): # while y > 0 : 0 1 2 3
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (a > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (a < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (a >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (a <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (a == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (a != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (a != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (a != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (a != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (a != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (a != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (a != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')
                    
                elif (placeHolder[1] == 'b'):
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (b > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (b < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (b >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (b <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (b == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (b != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (b != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (b != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (b != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (b != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (b != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (b != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')
                        
                elif (placeHolder[1] == 'c'):
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (c > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (c < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (c >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (c <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (c == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (c != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (c != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (c != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (c != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (c != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (c != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (c != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')
                    
                elif(placeHolder[1] == 'x'):
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (x > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (x < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (x >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (x <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (x == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (x != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (x != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (x != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (x != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (x != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (x != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (x != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')
                    
                elif(placeHolder[1] == 'y'):
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (y > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (y < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (y >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (y <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (y == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (y != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (y != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (y != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (y != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (y != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (y != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (y != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')
                    
                elif(placeHolder[1] == 'z'):
                    if (placeHolder[2] == '>'):
                        if(placeHolder[3] == 'a'):
                            if (z > a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z > b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z > c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z > x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z > y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z > z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z > int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<'):
                        if(placeHolder[3] == 'a'):
                            if (z < a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z < b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z < c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z < x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z < y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z < z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z < int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '>='):
                        if(placeHolder[3] == 'a'):
                            if (z >= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z >= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z >= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z >= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z >= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z >= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z >= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '<='):
                        if(placeHolder[3] == 'a'):
                            if (z <= a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z <= b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z <= c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z <= x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z <= y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z <= z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z <= int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '='):
                        if(placeHolder[3] == 'a'):
                            if (z == a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z == b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z == c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z == x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z == y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z == z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z == int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    elif (placeHolder[2] == '!='):
                        if(placeHolder[3] == 'a'):
                            if (z != a):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'b'):
                            if (z != b):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'c'):
                            if (z != c):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'x'):
                            if (z != x):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'y'):
                            if (z != y):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        elif(placeHolder[3] == 'z'):
                            if (z != z):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false'

                        else:
                            if (z != int(placeHolder[3])):
                                whileCheck = 'true' 
                            else:
                                whileCheck = 'false' 

                    else:
                        print('Error in If statements')

                else:
                    print('Compiler: Error for whileCheck creation')

            else:
                #if this ends up in a funcion add global varibales
                #reset so they dont mistake them
                ifCheck = 'false'
                whileCheck = 'false'
                elseCheck = 'false'

        betaParser(i)
        i = i + 1   #Loop ends here and restarts
    return 0

