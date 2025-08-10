import function_creation
from function_creation import createfunc

# Dictionaries for variable and list management
Var_Reg = {}
List_Reg = {}
Type_Reg = {}
Function_Reg = {}
output = "null"

def reset():
    global Var_Reg, List_Reg, output
    Var_Reg = {}
    List_Reg = {}
    output = "null"
    print("Reset")

def store_variable(name, value, type):
    if name in Var_Reg:
        print("Stored value")
    else:
        print("Stored new var")
    Var_Reg[name] = value
    Type_Reg[name] = type


def print_value(key):
    if key == "output":
        print(output)
    elif key in Var_Reg:
        print(Var_Reg[key])
    else:
        print(key)

def perform_operation(op, key, value):
    if key in Var_Reg and Type_Reg[key] == "int" and key.isdigit():
        current_value = int(float(Var_Reg[key]))
        new_value = int(value)
        if op == "add":
            Var_Reg[key] = current_value + new_value
        elif op == "mul":
            Var_Reg[key] = current_value * new_value
        elif op == "div":
            Var_Reg[key] = current_value // new_value
        elif op == "sub":
            Var_Reg[key] = current_value - new_value
        elif op == "fld":
            Var_Reg[key] = current_value // new_value
        elif op == "mod":
            Var_Reg[key] = current_value % new_value
        print(Var_Reg[key])
    else:
        if not Type_Reg[key] == "int":
            print(f"Variable {key} not found.")
        else:
            print("Variable is not a valid integer")
def check_equal(param1, param2):
    global output
    if ((not param1 in Var_Reg) and (not param2 in Var_Reg)):
        if param1 == param2:
            print("Parameter 1 is equal to Parameter 2")
            output = True
        else:
            output = False
    else:
        if Var_Reg[param1] == Var_Reg[param2]:
           print("Var 1 is equal to Var 2")
           output = True 
        else:
            output = False
def handle_command(command):
    global output

    cmd_parts = command.split()
    if (not command==""):
        cmd_type = cmd_parts[0]
    else:
        cmd_type = "null"
        print("invalid syntax")    

    if cmd_type == "reg":
        if cmd_parts[1] == "cls":
            reset()
        elif cmd_parts[1] == "int":
            name = cmd_parts[2]
            value = cmd_parts[3] if len(cmd_parts) > 3 else "0"
            store_variable(name, value, "int")
        elif cmd_parts[1] == "str":
            name = cmd_parts[2]
            type = cmd_parts[1]
            value = " ".join(cmd_parts[3:])
            store_variable(name, value, "str")
        elif cmd_parts[1] == "lst":
            print("In-development")

    elif cmd_type == "prt":
        print_value(command[4:])

    elif cmd_type == "fnc":
        if cmd_parts[1] in Function_Reg:
            print("Function already exists")
        else:
            createfunc(cmd_parts[1])    
            print("function created")

    elif cmd_type == "etr":
        if cmd_parts[1] == "var":
            print(str(Var_Reg))
        elif cmd_parts[1] == "lst":
            list_index = int(cmd_parts[2])
            print(List_Reg.get(list_index, "Index not found"))
        elif cmd_parts[1] == "fnc":
            print(Function_Reg)

    elif cmd_type in {"add", "mul", "div", "sub", "fld", "mod"}:
        key = cmd_parts[1]
        value = cmd_parts[2]
        perform_operation(cmd_type, key, value)

    elif cmd_type == "eqt":
        param1 = cmd_parts[1]
        param2 = cmd_parts[2]
        check_equal(param1, param2)

    elif cmd_type == "ext":
        print("Program Exited")
        return False

    elif cmd_type == "c77":
        createfunc("test")
    elif cmd_type == "null":
        print("")
    return True

def main():
    stats = True
    while stats:
        x = input("Type Command>>:")
        stats = handle_command(x)
    input('The Program has Been either Crashed OR Exited, press enter to close')

if __name__ == "__main__":
    main()
