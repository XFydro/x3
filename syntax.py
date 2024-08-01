
Var_Reg = []
Var_Vals = []
List_Reg = []
List_Vals = []
Stats = True
output = "null"

while(Stats):
    x = input("Type Command>>:")
    if (x[0:3]=="reg"):
        if (x[4:7]=="cls"):
            Var_Vals = []
            Var_Reg = []
            List_Reg = []
            List_Vals = []
            print("resetted")
        if (x[4:7]=="int"):
            if x[8:12] in Var_Reg:
                print("stored val")
                length = len(x)
                varindex = Var_Reg.index(x[8:12])
                Var_Vals[varindex] = x[13:length] 
            elif (not x[8:12]=="outp"):
                print("stored new var")
                Var_Reg.append(x[8:12])
                length = len(x)
                Var_Vals.append(x[13:len(x)])  
            else:
                varindex = Var_Reg.index(x[8:12])
                Var_Vals[varindex] = output       
        if (x[4:7]=="str"):
            Var_Reg.append(x[8:12])
            length = len(x)
            Var_Vals.append(str(x[13:length]))
        if (x[4:7=="lst"]):
            print("in-development")
    if (x[0:3]=="prt"):
        if (not x[4:10]=="output"):
            length = len(x)
            print(x[4:length])
        elif (x[4:10]=="output"):
            print(output)    
        elif (x[4:10] in Var_Reg):
            
            print()    
    if (x[0:3]=="fnc"):
        if (not x[4:5 == "()"]):
            print("Syntax Error")

    if (x[0:3]=="etr"):
        if (x[4:7]=="var"):
            print(str(Var_Reg))   
            print(str(Var_Vals))     
        if (x[4:7]=="lst"):
            length = len(x)
            list_extract = x[8:length]
            print(List_Reg[list_extract]) 

    if (x[0:3]=="add"):
        length = len(x)
        add_val = x[9:length]
        varindex = Var_Reg.index(x[4:8])
        var_val_strip =int(Var_Vals[varindex])
        Var_Vals[varindex] = int(str(var_val_strip).strip()) + int(str(add_val.strip()))
        print(Var_Vals[varindex])   
    
    if (x[0:3]=="mul"):
        length = len(x)
        add_val = x[9:length]
        varindex = Var_Reg.index(x[4:8])
        var_val_strip =int(Var_Vals[varindex])
        Var_Vals[varindex] = int(str(var_val_strip).strip()) * int(str(add_val.strip()))
        print(Var_Vals[varindex])   
 
    if (x[0:3]=="div"):
        length = len(x)
        add_val = x[9:length]
        varindex = Var_Reg.index(x[4:8])
        var_val_strip =int(Var_Vals[varindex])
        Var_Vals[varindex] = int(str(var_val_strip).strip()) // int(str(add_val.strip()))
        print(Var_Vals[varindex])
   
    if (x[0:3]=="sub"):
        length = len(x)
        add_val = x[9:length]
        varindex = Var_Reg.index(x[4:8])
        var_val_strip =int(Var_Vals[varindex])
        Var_Vals[varindex] = int(str(var_val_strip).strip()) - int(str(add_val.strip()))
        print(Var_Vals[varindex]) 
  
    if (x[0:3]=="fld"):
        length = len(x)
        add_val = x[9:length]
        varindex = Var_Reg.index(x[4:8])
        var_val_strip =int(Var_Vals[varindex])
        Var_Vals[varindex] = int(str(var_val_strip).strip()) // int(str(add_val.strip()))
        print(Var_Vals[varindex])   
    
    if (x[0:3]=="mod"):
        length = len(x)
        add_val = x[9:length]
        varindex = Var_Reg.index(x[4:8])
        var_val_strip =int(Var_Vals[varindex])
        Var_Vals[varindex] = int(str(var_val_strip).strip()) % int(str(add_val.strip()))
        print(Var_Vals[varindex])  
    
    if (x[0:3]=="eqt"):
        if (x[4:8]==x[9:13]):
            print("Parameter 1 is equal to Parameter 2")
            output=True
        else:
            output=False    
        
    if (x[0:3]=="ext"):
        Stats = False
        print("Program Exited")            

    if (x=="c77"):
        print("hehehe")
input('The Program has Been either Crashed OR Exited, press enter to close')
        
