import requests
import argparse
import time

class Interpreter:
    def __init__(self, debug=False):
        self.variables = {}
        self.functions = {}
        self.control_stack = []
        self.debug = debug
        self.output = None
        self.status = True
        self.IDLE = 1  # Set to 1 when running interactively
        self.log_messages = []

    def log(self, message):
        if self.debug:
            print(f"[DEBUG]: {message}")

    def eval_condition(self, condition):
        # Create a safe local scope with defined variables
        safe_scope = {var: value[0] for var, value in self.variables.items() if value[1] in ['int', 'str']}

        # Replace variables in condition with their values
        for var in safe_scope:
            condition = condition.replace(var, str(safe_scope[var]))
    
        try:
             # Handle different comparison operators
            if '==' in condition:
                left, right = condition.split('==')
                return self.compare_values(left.strip(), right.strip(), '==')
            elif '!=' in condition:
                left, right = condition.split('!=')
                return self.compare_values(left.strip(), right.strip(), '!=')
            elif '>=' in condition:
                left, right = condition.split('>=')
                return self.compare_values(left.strip(), right.strip(), '>=')
            elif '<=' in condition:
                left, right = condition.split('<=')
                return self.compare_values(left.strip(), right.strip(), '<=')
            elif '>' in condition:
                left, right = condition.split('>')
                return self.compare_values(left.strip(), right.strip(), '>')
            elif '<' in condition:
                left, right = condition.split('<')
                return self.compare_values(left.strip(), right.strip(), '<')
            else:
                self.handle_error(f"Invalid condition: {condition}")
                return False
        except Exception as e:
            self.handle_error(f"Error evaluating condition: {e}")
            return False

    def compare_values(self, left, right, operator):
        # Try to convert both values to integers, if possible
        try:
           left_val = int(left)
           right_val = int(right)
        except ValueError:
            # If they can't be converted to integers, treat them as strings
            left_val = left
            right_val = right
    
        # Perform the appropriate comparison based on the operator
        if operator == '==':
            return left_val == right_val
        elif operator == '!=':
            return left_val != right_val
        elif operator == '>':
            return left_val > right_val
        elif operator == '<':
            return left_val < right_val
        elif operator == '>=':
            return left_val >= right_val
        elif operator == '<=':
            return left_val <= right_val
        else:
            self.handle_error(f"Unknown operator: {operator}")
            return False

    def fetch_data_from_api(self, url=None, timeout=20):
        """Fetch data from a given API URL or from a variable in Var_Reg."""
        if not url:
            print("ErrID11: No URL or variable provided.")
            return "null"

        if url in self.variables:
            url = self.variables[url][0]

        if not url or not isinstance(url, str):
            print("ErrID12: Invalid URL or variable key provided.")
            return "null"

        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            self.output = response.text
            if self.IDLE != 0:
                print("Data fetched successfully.")
        except requests.exceptions.RequestException as e:
            print(f"ErrID10: Failed to fetch data from API. Error: {e}")
            self.output = "null"

    def store_variable(self, var_name, value, data_type):
        self.variables[var_name] = (value, data_type)
        self.cmd_log(f"Stored variable '{var_name}' with value {value} and type {data_type}")
        

    def handle_command(self, command):
        parts = command.split()
        try:
            cmd = parts[0]
            args = parts[1:]
        except IndexError:
            self.cmd_log(f"Index error encountered")

        command_mapping = {
            'reg': self.cmd_reg,
            'prt': self.cmd_prt,
            'add': self.cmd_add,
            'sub': self.cmd_sub,
            'mul': self.cmd_mul,
            'div': self.cmd_div,
            'mod': self.cmd_mod,
            'inp': self.cmd_inp,
            'if': self.cmd_if,
            'else': self.cmd_else,
            'end': self.cmd_end,
            'fetch': self.cmd_fetch,
            'exit': self.cmd_exit,
            'for': self.cmd_for,
            'while': self.cmd_while,
            'def': self.cmd_def,
            'call': self.cmd_call,
            'switch': self.cmd_switch,
            'case': self.cmd_case,
            'default': self.cmd_default,
            'inc': self.cmd_inc,
            'dec': self.cmd_dec,
            'try': self.cmd_try,
            'catch': self.cmd_catch,
            'repeat': self.cmd_repeat,
            'wait': self.cmd_wait,
            'log': self.cmd_log,
            'read_log': self.cmd_read_log, 
            'easter': self.cmd_easteregg,       
            }

        if cmd in command_mapping:
            command_mapping[cmd](args)
        else:
            print(f"ErrID0: Unknown command '{cmd}'")

    def cmd_reg(self, args):
        if len(args) < 3:
            print("ErrID3: Incorrect number of arguments for reg command")
            return

        data_type = args[1]
        var_name = args[0]
        value = " ".join(args[2:])

        if  not(("int" == data_type) or ("str" == data_type) or ("lst" == data_type)):
            print("ErrID3: Invalid data type")
            print(data_type)
            return

        if data_type == "int":
            value = int(value)
        elif data_type == "str":
            value = value.strip('"')
        elif data_type == "lst":
            value = value.split(',')

        self.store_variable(var_name, value, data_type)

    def cmd_prt(self, args):
        value = " ".join(args)
        if value in self.variables:
            print(self.variables[value][0])
        else:
            print(value)

    def handle_arithmetic(self, operation, args):
        if len(args) != 2:
            self.handle_error(f"Incorrect number of arguments for '{operation}' command")
            return
        var_name, value = args
        if var_name in self.variables and self.variables[var_name][1] == "int":
            try:
                value = int(value)
                if operation == 'add':
                    self.variables[var_name] = (self.variables[var_name][0] + value, "int")
                elif operation == 'sub':
                    self.variables[var_name] = (self.variables[var_name][0] - value, "int")
                elif operation == 'mul':
                    self.variables[var_name] = (self.variables[var_name][0] * value, "int")
                elif operation == 'div':
                    self.variables[var_name] = (self.variables[var_name][0] // value, "int")
                elif operation == 'mod':
                    self.variables[var_name] = (self.variables[var_name][0] % value, "int")
            except ValueError:
                self.handle_error(f"Invalid value '{value}' for {operation}")

    def cmd_add(self, args):
        self.handle_arithmetic('add', args)

    def cmd_sub(self, args):
        self.handle_arithmetic('sub', args)

    def cmd_mul(self, args):
        self.handle_arithmetic('mul', args)

    def cmd_div(self, args):
        self.handle_arithmetic('div', args)

    def cmd_mod(self, args):
        self.handle_arithmetic('mod', args)

    def cmd_inp(self, args):
        if len(args) != 2:
            print("ErrID3: Incorrect number of arguments for inp command")
            return

        var_name = args[0]
        prompt = args[1].strip('"')
        user_input = input(f"{prompt} ")
        
        try:
            if user_input.isnumeric()==True:
                self.store_variable(var_name, int(user_input), 'int')
            else:
                self.store_variable(var_name, user_input.strip('"'), 'str')      
        except ValueError or AttributeError:
            self.store_variable(var_name, user_input.strip('"'), 'str')

    def cmd_if(self, args):
        condition = " ".join(args)
        result = self.eval_condition(condition)

        self.control_stack.append({
            "type": "if",
            "active": result
        })

    def cmd_else(self, args):
        if not self.control_stack or self.control_stack[-1]["type"] != "if":
            print("ErrID19: 'else' command outside of 'if' block")
            return
        
        if self.control_stack[-1]["active"]:
            self.control_stack[-1]["active"] = False

    def cmd_end(self, args):
        if self.control_stack:
            self.control_stack.pop()

    def cmd_fetch(self, args):
        if len(args) != 1:
            print("ErrID3: Incorrect number of arguments for fetch command")
            return
        url = args[0].strip('"')
        self.fetch_data_from_api(url)

    def cmd_exit(self, args):
        print("Program Quitted")
        exit()

    def cmd_for(self, args):
        if len(args) != 3:
            print("ErrID3: Incorrect number of arguments for 'for' command")
            return
        var_name, start, end = args
        try:
            start = int(start)
            end = int(end)
        except ValueError:
            print("ErrID16: 'for' loop start and end must be integers")
            return
        self.store_variable(var_name, start, "int")
        self.control_stack.append({
            "type": "for",
            "var": var_name,
            "start": start,
            "end": end,
            "current": start,
            "active": True
        })

    def cmd_while(self, args):
        if not args:
            print("ErrID3: Missing condition for 'while' command")
            return
        condition = " ".join(args)
        result = self.eval_condition(condition)
        self.control_stack.append({
            "type": "while",
            "condition": condition,
            "active": result
        })

    def cmd_def(self, args):
        if not args:
            print("ErrID3: Missing function name for 'def' command")
            return
        func_name = args[0]
        params = args[1:]
        if func_name in self.functions:
            print(f"ErrID19: Function '{func_name}' already defined")
            return
        self.functions[func_name] = params

    def cmd_call(self, args):
        if len(args) != 1:
            print("ErrID3: Incorrect number of arguments for 'call' command")
            return
        func_name = args[0]
        if func_name not in self.functions:
            print(f"ErrID19: Function '{func_name}' not defined")
            return

        params = self.functions[func_name]
        # You could add more logic here to handle parameters if needed
        for param in params:
            self.handle_command(param)

    def cmd_switch(self, args):
        if len(args) != 1:
            print("ErrID3: Incorrect number of arguments for 'switch' command")
            return
        switch_var = args[0]
        self.control_stack.append({
            "type": "switch",
            "var": switch_var,
            "cases": [],
            "active": True
        })

    def cmd_case(self, args):
        if not self.control_stack or self.control_stack[-1]["type"] != "switch":
            print("ErrID19: 'case' command outside of 'switch' block")
            return
        case_value = args[0]
        self.control_stack[-1]["cases"].append(case_value)

    def cmd_default(self, args):
        if not self.control_stack or self.control_stack[-1]["type"] != "switch":
            print("ErrID19: 'default' command outside of 'switch' block")
            return
        self.control_stack[-1]["default"] = True

    def cmd_inc(self, args):
        if len(args) != 1:
            print("ErrID3: Incorrect number of arguments for inc command")
            return
        var_name = args[0]
        if var_name in self.variables and self.variables[var_name][1] == "int":
            self.variables[var_name] = (self.variables[var_name][0] + 1, "int")

    def cmd_dec(self, args):
        if len(args) != 1:
            print("ErrID3: Incorrect number of arguments for dec command")
            return
        var_name = args[0]
        if var_name in self.variables and self.variables[var_name][1] == "int":
            self.variables[var_name] = (self.variables[var_name][0] - 1, "int")

    def cmd_try(self, args):
        self.control_stack.append({
            "type": "try",
            "active": True
        })

    def cmd_catch(self, args):
        if not self.control_stack or self.control_stack[-1]["type"] != "try":
            print("ErrID19: 'catch' command outside of 'try' block")
            return
        self.control_stack[-1]["active"] = False

    def cmd_repeat(self, args):
        if not self.control_stack or self.control_stack[-1]["type"] != "repeat":
            print("ErrID19: 'repeat' command outside of a valid context")
            return
        # Logic for repeat command would go here

    def cmd_wait(self, args):
        if len(args) != 1:
            print("ErrID3: Incorrect number of arguments for wait command")
            return
        try:
            wait_time = int(args[0])
            time.sleep(wait_time)
        except ValueError:
            print("ErrID16: Wait time must be an integer")

    def cmd_log(self, message):
        if self.debug:
            print(f"[DEBUG]: {message}")
        self.log_messages.append(message)  # Save the message to log
    def cmd_easteregg(self):
        self.cmd_log("hi")
# Implement cmd_read_log
    def cmd_read_log(self, args):
        if not self.log_messages:
            print("No log messages found.")
        else:
            for index, message in enumerate(self.log_messages):
                print(f"{index + 1}: {message}")

    def handle_error(self, message):
       print(f"Error: {message}")

    def read_input(self):
        while True:
            command = input("Enter command: ").strip()
            if command.lower() == 'exit':
                self.cmd_exit([])
            elif command:
                self.handle_command(command)

    def read_from_file(self, filename):
        """Read commands from a file and execute them."""
        try:
            with open(filename, 'r') as file:
                for line in file:
                    # Ignore empty lines and comments
                    stripped_line = line.strip()
                    if not stripped_line or stripped_line.startswith("#"):
                        continue
                    # If defining a function, collect its commands
                    if self.control_stack and self.control_stack[-1]["type"] == "def":
                        if stripped_line.lower() == "end":
                            self.cmd_end([], local_vars=None)
                        else:
                            func_name = self.control_stack[-1]["function_name"]
                            self.functions[func_name]["commands"].append(stripped_line)
                    else:
                        self.handle_command(stripped_line)
        except FileNotFoundError:
            print(f"ErrID7: File '{filename}' not found. Please check the filename and try again.")
        except IOError as e:
            print(f"ErrID8: An I/O error occurred while reading '{filename}': {e}")

    def main_loop(self, mode=None, filename=None):
        """Main loop of the interpreter."""
        if mode == "file" and filename:
            self.read_from_file(filename)
            self.exit_program()
            return
        while self.status:
            try:
                line = input("Enter command: ").strip()
                if not line:
                    continue  # Ignore empty inputs
                # If defining a function, collect its commands
                if self.control_stack and self.control_stack[-1]["type"] == "def":
                    if line.lower() == "end":
                        self.cmd_end([], local_vars=None)
                    else:
                        func_name = self.control_stack[-1]["function_name"]
                        self.functions[func_name]["commands"].append(line)
                else:
                    self.handle_command(line)
            except KeyboardInterrupt:
                print("\nExiting...")
                self.exit_program()
            except Exception as e:
                print(f"ErrID5: Runtime error: {e}")

def main():
    parser = argparse.ArgumentParser(description="X3 Interpreter")
    parser.add_argument('--mode', choices=['file', 'idle'], default='idle', help='Mode to run the interpreter in.')
    parser.add_argument('--file', type=str, help='Path to the X3 script file to execute.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
    args = parser.parse_args()

    interpreter = Interpreter(debug=args.debug)
    if args.mode == 'file' and args.file:
        interpreter.main_loop(mode='file', filename=args.file)
    else:
        interpreter.main_loop()

if __name__ == "__main__":
    main()
