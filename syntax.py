
Var_Reg = []
Var_Vals = []
List_Reg = []
List_Vals = []
Stats = True
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
            else:
                print("stored new var")
                Var_Reg.append(x[8:12])
                length = len(x)
                Var_Vals.append(x[13:len(x)])    
        if (x[4:7]=="str"):
            Var_Reg.append(x[8:12])
            length = len(x)
            Var_Vals.append(str(x[13:length]))
        if (x[4:7=="lst"]):
            x="null"
    if (x[0:3]=="prt"):
        length = len(x)
        print(x[4:length])
            
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

    if (x=="ext"):
        Stats = False
        print("Status=exit")            

    if (x=="c77"):
        print("hehehe")