#---------------------------------------------------------------
#varibales/imports
#---------------------------------------------------------------
#file imports for functions
import ASM
import betaCompiler
import CSV

#file paths
fileName = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\HighLevelCode.txt")
fileName2 = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\Assembly.txt")
fileName3 = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\Machine.txt")

p = 0   #initialize varibale for assembler : Can I just put a 0 in the call function?

#---------------------------------------------------------------
#here to test certain functions seperately
#---------------------------------------------------------------

#compiler part
#i = 0
#betaCompiler.projectCompiler(i)

   

#checks assembly.txt length to determine loop size
lenG = CSV.lineCount(fileName2)

while(p < lenG):    #runs assembler
    #doesn't handle indents
    ASM.assembler(fileName2, p)
    p = p + 1

#csv creation
    