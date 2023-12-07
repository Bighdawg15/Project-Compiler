#---------------------------------------------------------------
#varibales/imports
#---------------------------------------------------------------
#file imports for functions
import ASM
import betaCompiler
import CSV

#---------------------------------------------------------------
#here to test certain functions seperately
#---------------------------------------------------------------

#leave a shit ton of empty lines at the end of HLC to get rid of content[i] error

#also fix \n


fileName = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\HighLevelCode.txt")
fileName2 = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\Assembly.txt")
fileName3 = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\Machine.txt")

i = 0
betaCompiler.projectCompiler(i)

lenG = CSV.lineCount(fileName2) - 3
p = 0

while(p < lenG):    #runs assembler
    #doesn't handle indents
    ASM.assembler(fileName2, p)
    p = p + 1
    
    