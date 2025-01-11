import requests
import argparse
import time
import re
import os
try:
    class Interpreter:
        def __init__(self, debug=False):
            self.variables = {}
            self.functions = {}
            self.control_stack = []
            self.debug = False
            self.output = None
            self.status = True
            self.log_messages = []
            self.nested_loops = []
            self.special_command=[]
            self.if_stack = []
            self.functions = {}  # Store function definitions here

        def log(self, message):
            if self.debug:
                print(f"[DEBUG]: {message}")
                                    
        def cmd_exec(self, line, main_vars):
            tokens = line.split()
            
            if tokens[0] == "extract":
                if len(tokens) > 1:
                    var_name = tokens[1]
                    self.cmd_extract(var_name, main_vars)
                else:
                    print("Error: No variable name provided for extraction.")
            else:
                # Here you can handle other commands like assignments, prints, etc.
                # For example, a simple assignment might look like:
                if "=" in line:
                    var_name, value = line.split("=")
                    main_vars[var_name.strip()] = eval(value.strip())  # Be careful with eval

                    
        def cmd_if(self, condition):
            # Ensure condition is in string format
            if isinstance(condition, list):
                condition = ' '.join(condition)

            # Parse and evaluate the condition
            left, operator, right = self.parse_condition(condition)
            result = self.eval_condition(left, operator, right)

            # Push True or False based on condition result
            self.if_stack.append(result)

            if self.debug:
                print(f"[DEBUG] IF condition '{condition}' evaluated to {result}")
            return result

        def cmd_else(self):
            # Check for preceding `if`
            if not self.if_stack:
                raise SyntaxError("Else without a preceding if statement")

            # Get the last `if` condition result without removing it
            last_condition = self.if_stack[-1]

            if last_condition:
                # If the `if` was True, skip the `else` block
                if self.debug:
                    print("[DEBUG] ELSE block skipped due to True IF condition")
                self.skip_next_block = True
            else:
                # If the `if` was False, execute the `else` block
                if self.debug:
                    print("[DEBUG] ELSE block executed due to False IF condition")
                self.skip_next_block = False

        def cmd_end(self):
            # Handle regular conditional blocks
            if not self.if_stack:
                raise SyntaxError("End without a preceding if/else block")
            self.if_stack.pop()
            if self.debug:
                print("[DEBUG] End of conditional block")



        def should_execute(self):
            # to check if the current command is ready to be executed based on the if_stack
            return all(self.if_stack)

        def parse_condition(self, condition):
            # Ensure condition is a string for splitting
            if not isinstance(condition, str):
                raise TypeError("Condition should be a string")
                
            # Parsing condition, extracting left, operator, and right
            parts = condition.split()
            left = parts[0]
            operator = parts[1]
            right = ' '.join(parts[2:])
            return left, operator, right

        def eval_condition(self, left, operator, right):
            # Get the left and right values, allowing for variable substitution
            left_value = self.variables.get(left, left)
            right_value = self.variables.get(right, right)

            # Check the operator and perform the comparison
            if operator == '==':
                return str(left_value) == str(right_value)
            elif operator == '>':
                return float(left_value) > float(right_value)
            elif operator == '<':
                return float(left_value) < float(right_value)

            return False

        def cmd_prt(self, message):
            # Check if message exists as a key in self.variables
            if self.debug != True:
                if message in self.variables:
                    # Access the first element if it's a tuple
                    value = self.variables[message]
                    print(value[0] if isinstance(value, tuple) else value)  # Print the first item if it's a tuple
                else:
                    print(message.strip('"')) #raw message with the " symbols removed
            else:
                if message in self.variables:
                    # Access the first element if it's a tuple
                    value = self.variables[message]
                    print(f"[DEBUG] Printing the value of var {message}" +": "+ value[0] if isinstance(value, tuple) else value)  # Print the first item if it's a tuple
                else:
                    print(f"[DEBUG] Printing"+": "+message.strip('"')) #raw message with the " symbols removed            
                
        def fetch_data_from_api(self, url=None, timeout=20):
            """Fetch data from a given API URL or from a variable in Var_Reg."""
            if not url:
                print("ErrID11: No URL or variable provided.")
                self.cmd_exit()
                self.output = None
                return

            if url in self.variables:
                url = self.variables[url]

            if not url or not isinstance(url, str):
                print("ErrID12: Invalid URL or variable key provided.")
                self.cmd_exit()
                self.output = None
                return

            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                self.output = response.text.strip()  # Store the fetched data, removing any trailing whitespace
                print(f"[DEBUG] Data fetched and stored in output: {self.output}")
            except requests.exceptions.RequestException as e:
                print(f"ErrID10: Failed to fetch data from API. Error: {e}")
                self.cmd_exit()
                self.output = None


        def store_variable(self, var_name, value, data_type):
            if not value=="output":
                self.variables[var_name] = (value, data_type)
            else:
                self.variables[var_name] = (self.output, data_type)    
            self.cmd_log(f"Stored variable '{var_name}' with value {value} and type {data_type}")
            
        def cmd_fncend(self):
            """Marks the end of a function definition."""
            if hasattr(self, "current_function_name"):
                if self.debug:
                    print(f"[DEBUG] End of function definition for '{self.current_function_name}'")
                # Remove the current function context
                del self.current_function_name
                self.in_function_definition = False  # Update the flag to exit definition mode

        def handle_command(self, command):
            """Processes commands, handles function definitions, and executes appropriately."""
            if self.debug:
                print(f"[DEBUG] Handling command: '{command}'")

            # If in function definition mode, add command to function and return
            if getattr(self, "in_function_definition", False):
                if command != "fncend":  # Avoid adding 'fncend' to the function's list
                    self.functions[self.current_function_name].append(command)
                    if self.debug:
                        print(f"[DEBUG] Adding command '{command}' to function '{self.current_function_name}'")
                return

            # Check for the `fncend` command and reset the function definition state
            if command == "fncend":
                self.cmd_fncend()
                return
            # Debug print for each command received
            if self.debug:
                print(f"[DEBUG] Handling command: '{command}'")

            # Check if the command is 'prt' to preserve whitespace
            if command.startswith("prt"):
                parts = re.findall(r'\S+|\s+', command)  # Keep whitespace for prt command
            else:
                parts = command.split()  # Standard split for other commands

            cmd = parts[0].strip()

            # Check if any control stack has a skip condition set to True
            if self.control_stack and self.control_stack[-1].get("skip"):
                if self.debug:
                    print(f"[DEBUG] Skipping command '{command}' due to control stack skip flag")
                return  

            # Mapping commands to methods
            command_mapping = {
                'dev.debug': self.devdebug,
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
                'fncend': self.cmd_fncend,
            }

            # Commands that don’t take arguments
            no_arg_commands = ["else", "end", "dev.debug"]

            # Process command if recognized
            if cmd in command_mapping:
                if cmd in no_arg_commands:
                    command_mapping[cmd]()
                else:
                    # Keep whitespace intact for `prt`, standard join for other commands
                    args = ''.join(parts[1:]).strip() if cmd == "prt" else ' '.join(parts[1:])
                    command_mapping[cmd](args)

                if self.debug:
                    print(f"[DEBUG] Command '{cmd}' executed with args: '{args if 'args' in locals() else ''}'")
            
            if cmd in ["end"]:
                self.skip_next_block = False
        def devdebug(self):
            self.debug = True
            del self.log_messages
            
        def cmd_reg(self, args):
            # Ensure we have at least 3 elements in args (variable name, data type, and value)
            args = args.split()
            if len(args) < 3:
                print("ErrID3: Incorrect number of arguments for reg command")
                self.cmd_exit()
                return

            var_name = args[0]
            data_type = args[1]
            value = " ".join(args[2:])

            # Check if the value is a reference to another variable or a direct value
            if value in self.variables:
                # Fetch the value from the variables dictionary if it exists
                stored_value = self.variables[value]
                value = stored_value[0] if isinstance(stored_value, tuple) else stored_value
            elif value == "output":
                # Fetch from self.output if the value is the keyword 'output'
                value = self.output

            # Convert value to the specified data type if it's not already in the variables
            if data_type == "int":
                try:
                    value = int(value)
                except ValueError:
                    print(f"Error: Cannot convert '{value}' to integer.")
                    return
            elif data_type == "str":
                # Strip any surrounding quotes for string type
                value = value.strip('"')

            # Store the variable using the corrected type and value
            self.store_variable(data_type, value, var_name)

        def cmd_inp(self, args):
            if len(args) != 2:
                print("ErrID3: Incorrect number of arguments for inp command")
                self.cmd_exit()
                return

            var_name = args[0]
            prompt = args[1].strip('"')
            user_input = input(f"{prompt} ")
            
            try:
                if user_input.isnumeric():
                    self.store_variable(var_name, int(user_input), 'int')
                else:
                    self.store_variable(var_name, user_input.strip('"'), 'str')      
            except ValueError or AttributeError:
                self.store_variable(var_name, user_input.strip('"'), 'str')
  
            
        def cmd_fetch(self, args):
            if len(args) < 1:
                print("ErrID3: Incorrect number of arguments for fetch command")
                self.cmd_exit()
                return
            url = args[0]
            if url in self.variables:           
                self.fetch_data_from_api(self.variables[url])

        def cmd_exit(self, args):
            print("Exiting the interpreter.")
            exit()

        def cmd_for(self, args):
            if len(args) != 4:
                print("ErrID3: Incorrect number of arguments for for command")
                self.cmd_exit()
                return

            loop_var = args[0]
            start = int(args[1])
            end = int(args[2])
            step = int(args[3])

            for i in range(start, end, step):
                self.variables[loop_var] = (i, 'int')
                self.nested_loops.append((loop_var, start, end, step))
                # Execute nested loops in sequence
                self.cmd_log(f"Loop variable '{loop_var}' set to {i}")

        def cmd_while(self, args):
            if len(args) < 1:
                print("ErrID3: Incorrect number of arguments for while command")
                self.cmd_exit()
                return

            condition = " ".join(args)
            while self.eval_condition(condition):
                self.cmd_log(f"While loop condition '{condition}' is True")

        def cmd_def(self, args):
            tokens = args.split()
            if len(tokens) < 1:
                print("ErrID3: Incorrect number of arguments for def command")
                self.cmd_exit()
                return

            function_name = tokens[0]
            self.current_function_name = function_name
            self.functions[function_name] = []  # Start a new list for storing commands
            if self.debug:
                print(f"[DEBUG] Defining function '{function_name}'")


        def cmd_call(self, args):
            function_name = args.split()[0]
            if function_name not in self.functions:
                print(f"ErrID36: Function '{function_name}' not defined.")
                self.cmd_exit()
                return

            if self.debug:
                print(f"[DEBUG] Calling function '{function_name}'")

            for command in self.functions[function_name]:
                self.handle_command(command)  # Execute each command in the function

        def cmd_switch(self, args):
            if len(args) < 1:
                print("ErrID3: Incorrect number of arguments for switch command")
                self.cmd_exit()
                return
            switch_variable = args[0]
            if switch_variable not in self.variables:
                print(f"ErrID31: Variable '{switch_variable}' not defined.")
                self.cmd_exit()
                return

            self.control_stack.append({
                "type": "switch",
                "variable": self.variables[switch_variable][0],
                "cases": []
            })

        def cmd_case(self, args):
            if not self.control_stack or self.control_stack[-1]["type"] != "switch":
                print("ErrID32: 'case' command outside of 'switch' block")
                self.cmd_exit()
                return
            case_value = args[0]
            self.control_stack[-1]["cases"].append(case_value)

        def cmd_default(self, args):
            if not self.control_stack or self.control_stack[-1]["type"] != "switch":
                print("ErrID33: 'default' command outside of 'switch' block")
                self.cmd_exit()
                return
            self.control_stack[-1]["default"] = args

        def cmd_inc(self, args):
            if len(args) != 1:
                print("ErrID3: Incorrect number of arguments for inc command")
                self.cmd_exit()
                return
            var_name = args[0]
            if var_name in self.variables and self.variables[var_name][1] == "int":
                self.variables[var_name] = (self.variables[var_name][0] + 1, "int")
            else:
                print(f"ErrID34: Variable '{var_name}' not defined or not an integer.")
                self.cmd_exit()

        def cmd_dec(self, args):
            if len(args) != 1:
                print("ErrID3: Incorrect number of arguments for dec command")
                self.cmd_exit()
                return
            var_name = args[0]
            if var_name in self.variables and self.variables[var_name][1] == "int":
                self.variables[var_name] = (self.variables[var_name][0] - 1, "int")
            else:
                print(f"ErrID34: Variable '{var_name}' not defined or not an integer.")
                self.cmd_exit()

        def cmd_try(self, args):
            self.control_stack.append({
                "type": "try",
                "active": True
            })

        def cmd_catch(self, args):
            if not self.control_stack or self.control_stack[-1]["type"] != "try":
                print("ErrID35: 'catch' command outside of 'try' block")
                self.cmd_exit()
                return
            # Handle the catch logic
            self.cmd_log("Catching exceptions inside try block")

        def cmd_repeat(self, args):
            if len(args) != 2:
                print("ErrID3: Incorrect number of arguments for repeat command")
                self.cmd_exit()
                return

            loop_count = int(args[0])
            command_to_repeat = args[1]

            for _ in range(loop_count):
                self.handle_command(command_to_repeat)

        def cmd_wait(self, args):
            if len(args) != 1:
                print("ErrID3: Incorrect number of arguments for wait command")
                self.cmd_exit()
                return

            duration = int(args[0])
            self.cmd_log(f"Waiting for {duration} seconds...")
            time.sleep(duration)

        def cmd_log(self, args):
            """Removed due to memory errors"""
        
        def cmd_read_log(self, args):
            for message in self.log_messages:
                print("This feature was removed due to memory errors and slow proessing speeds")

        def cmd_add(self, args):
            if len(args) != 3:
                print("ErrID3: Incorrect number of arguments for add command")
                self.cmd_exit()
                return

            var_name = args[0]
            operand1 = int(self.variables[args[1]][0])
            operand2 = int(self.variables[args[2]][0])

            result = operand1 + operand2
            self.store_variable(var_name, result, "int")

        def cmd_sub(self, args):
            if len(args) != 3:
                print("ErrID3: Incorrect number of arguments for sub command")
                self.cmd_exit()
                return

            var_name = args[0]
            operand1 = int(self.variables[args[1]][0])
            operand2 = int(self.variables[args[2]][0])

            result = operand1 - operand2
            self.store_variable(var_name, result, "int")

        def cmd_mul(self, args):
            if len(args) != 3:
                print("ErrID3: Incorrect number of arguments for mul command")
                self.cmd_exit()
                return

            var_name = args[0]
            operand1 = int(self.variables[args[1]][0])
            operand2 = int(self.variables[args[2]][0])

            result = operand1 * operand2
            self.store_variable(var_name, result, "int")

        def cmd_div(self, args):
            if len(args) != 3:
                print("ErrID3: Incorrect number of arguments for div command")
                self.cmd_exit()
                return

            var_name = args[0]
            operand1 = int(self.variables[args[1]][0])
            operand2 = int(self.variables[args[2]][0])

            if operand2 == 0:
                print("ErrID4: Division by zero")
                self.cmd_exit()
                return

            result = operand1 / operand2
            self.store_variable(var_name, result, "int")

        def cmd_mod(self, args):
            if len(args) != 3:
                print("ErrID3: Incorrect number of arguments for mod command")
                self.cmd_exit()
                return

            var_name = args[0]
            operand1 = int(self.variables[args[1]][0])
            operand2 = int(self.variables[args[2]][0])

            if operand2 == 0:
                print("ErrID4: Division by zero")
                self.cmd_exit()
                return

            result = operand1 % operand2
            self.store_variable(var_name, result, "int")

    def main():
        parser = argparse.ArgumentParser(description="X3 Interpreter")
        parser.add_argument('-f', '--file', type=str, help='File to execute as a script')
        parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
        args = parser.parse_args()

        #uses debug mode if nessecary
        interpreter = Interpreter(debug=args.debug)

        # If a file is provided, read commands from the file
        if args.file:
            with open(args.file, 'r') as script_file:
                for line in script_file:
                    interpreter.handle_command(line.strip())
        else:
            # IDLE mode (Will be removed in v3.x idk)
            while True:
                try:
                    user_input = input("X3> ")
                    interpreter.handle_command(user_input.strip())
                except (KeyboardInterrupt, EOFError):
                    print("\nExiting.")
                    break

    if __name__ == "__main__":
        main()
except Exception as E:
    print("[CRITICAL ERROR]: {E}")
    try:
        main()
    except Exception as E:
            print("[OVERCRITICAL ERROR]: {E},End of Script")    