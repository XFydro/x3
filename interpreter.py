import requests
import argparse
import time
import re
import os as sys1
import shlex 
import json
from colorama import Fore, Style, init
import subprocess
import sys
#patch23:42 13-01-2025--#1:Install packages automatically.
#patch21:29 05-02-2025--#2:Fixed Log Functionality
#patch22:10 11-02-2025--#3:Fixed Fetch Functionality
#addition22:30 11-02-2025--#1:Added flush to reset interpreter state

def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install the modules
install_package("colorama")
install_package("requests")

# Test imports
try:
    import colorama
    import requests
    print("Loaded 2 extra modules: colorama, requests.")
except ImportError as e:
    print(f"Error importing modules: {e}")
"""
Requirements:
__Python3.6+
__Pip(Latest Update for better experience)
__Installed Colorama Module
__Installed Requests Module
__Minimal Hardware resources:2GB Ram
__Terminal which supports ANSI color codes
__Patience because python is slow af

"""
try:
    
    class Interpreter:
        def __init__(self, debug=False):
            
            self.variables = {}
            self.functions = {}
            self.control_stack = []
            self.debug = False
            self.debuglog = []
            self.output = None
            self.status = True
            self.log_messages = []
            self.nested_loops = []
            self.special_command=[]
            self.if_stack = []
            self.functions = {}
            self.execution_state = {}
            self.h = 0
            #Debug Init---
            self.ctrflwdebug = False
            self.prtdebug = False
            self.mathdebug = False
            self.filedebug = False
            self.clramadebug = False
            self.cmdhandlingdebug = False
            #---
            self.command_mapping = {
                'cls': self.cmd_clear,
                'dev.debug': self.dev,
                'w_file': self.cmd_create_file,
                'r_file': self.cmd_read_file,
                'a_file': self.cmd_append_file,           
                'del_file': self.cmd_delete_file,     
                'create_dir': self.cmd_create_dir,
                'delete_dir': self.cmd_delete_dir,
                'search_file': self.cmd_search_file,
                'sqrt': self.cmd_sqrt,
                'sys_info': self.cmd_sys_info,
                'set_env': self.cmd_set_env,                
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
                'while': self.cmd_while,
                'def': self.cmd_def,
                'call': self.cmd_call,
                'switch': self.cmd_switch,
                'case': self.cmd_case,
                'default': self.cmd_default,
                'inc': self.cmd_inc,
                'dec': self.cmd_dec,
                'catch': self.cmd_catch,
                'repeat': self.cmd_repeat,
                'wait': self.cmd_wait,
                'log': self.cmd_log,
                'fncend': self.cmd_fncend,
                'dev.debug': self.dev,
                'load': self.load,
                'dev.custom': self.DEVCUSTOMTESTING,
                'flush': self.flush,
            }
            self.exceptional_commands={
                "//",
                "",
                " ",
            }
        
            self.color_dict = {
                    # Foreground Colors (Approx ROYGBIV)
                    "-/red": "\033[91m",         # Bright red
                    "-/orange": "\033[38;5;214m",  # Approximate orange (256 color mode)
                    "-/yellow": "\033[93m",      # Bright yellow
                    "-/green": "\033[92m",       # Bright green
                    "-/blue": "\033[94m",        # Bright blue
                    "-/indigo": "\033[38;5;57m",  # Approximate indigo (256 color mode)
                    "-/violet": "\033[38;5;135m",  # Approximate violet (256 color mode)
                    "-/cyan": "\033[96m",        # Bright cyan
                    "-/white": "\033[97m",       # Bright white
                    
                    # Background Colors
                    "-bg/red": "\033[41m",       # Red background
                    "-bg/orange": "\033[48;5;214m",  # Orange background (256 color mode)
                    "-bg/yellow": "\033[43m",    # Yellow background
                    "-bg/green": "\033[42m",     # Green background
                    "-bg/blue": "\033[44m",      # Blue background
                    "-bg/indigo": "\033[48;5;57m",  # Indigo background (256 color mode)
                    "-bg/violet": "\033[48;5;135m",  # Violet background (256 color mode)
                    "-bg/cyan": "\033[46m",      # Cyan background
                    "-bg/white": "\033[47m",     # White background
                    
                    # Bold Colors
                    "-bold/red": "\033[1;91m",    # Bold bright red
                    "-bold/orange": "\033[1;38;5;214m",  # Bold orange (256 color mode)
                    "-bold/yellow": "\033[1;93m", # Bold bright yellow
                    "-bold/green": "\033[1;92m",  # Bold bright green
                    "-bold/blue": "\033[1;94m",   # Bold bright blue
                    "-bold/indigo": "\033[1;38;5;57m",  # Bold indigo (256 color mode)
                    "-bold/violet": "\033[1;38;5;135m",  # Bold violet (256 color mode)
                    "-bold/cyan": "\033[1;96m",   # Bold bright cyan
                    "-bold/white": "\033[1;97m",  # Bold bright white
                }
        def flush(self):
            self.variables = {}
            self.functions = {}
            self.control_stack = []
            self.debug = False
            self.debuglog = []
            self.output = None
            self.status = True
            self.log_messages = []
            self.nested_loops = []
            self.special_command=[]
            self.if_stack = []
            self.functions = {}
            self.execution_state = {}
            self.h = 0
            #Debug Init---
            self.ctrflwdebug = False
            self.prtdebug = False
            self.mathdebug = False
            self.filedebug = False
            self.clramadebug = False
            self.cmdhandlingdebug = False
        def DEVCUSTOMTESTING(self):
            print(self.control_stack)            
        def load(self, filename):
            try:
                interpreter = Interpreter()
                with open(filename, 'r') as file:
                    for line in file:
                        command = line.strip()
                        interpreter.handle_command(command)
            except FileNotFoundError:
                print(f"Error: The file '{filename}' was not found.")
            except Exception as e:
                print(f"An error occurred while executing commands from '{filename}': {e}")  
        def is_float(self, num):
            return True if type(num)=="float" else False;    
        def log(self, message):
            if self.debug:
                print(f"[DEBUG]: {message}")
                self.debuglog.append(f"[DEBUG]: {message}")
                                    
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
                exit(0)
        def cmd_clear(self, args):
            if args!="legacy":
                sys1.system('cls' if sys1.name == 'nt' else 'clear')
            else:
                print("\n" * 100)

        def cmd_if(self, condition):
            """
            Start an `if` block by evaluating the condition.
            """
            try:
                # Parse and evaluate the condition
                left, operator, right = self.parse_condition(condition)
                result = self.eval_condition(left, operator, right)
            except ValueError as e:
                print(f"[CRITICAL ERROR]: Invalid IF condition '{condition}'. Details: {e}")
                self.cmd_exit()

            # Register the IF block in the control stack
            self.control_stack.append({"type": "if", "executed": result, "allow_else": not result})

            if self.ctrflwdebug:
                print(f"[DEBUG] IF condition '{condition}' evaluated to {result}")

            # Set execution state based on the condition
            self.execution_state = result

        def cmd_else(self):
            """
            Handle an `else` block for conditional execution.
            """
            if not self.control_stack or self.control_stack[-1]["type"] != "if":
                print("[CRITICAL ERROR]: ELSE without matching IF. Terminating script.")
                self.cmd_exit()

            last_if = self.control_stack[-1]

            if last_if["allow_else"]:
                self.execution_state = True
                last_if["allow_else"] = False  # Prevent multiple ELSE blocks from executing
                if self.ctrflwdebug:
                    print("[DEBUG] ELSE block executed")
            else:
                self.execution_state = False
                if self.ctrflwdebug:
                    print("[DEBUG] ELSE block skipped")

        def cmd_end(self):
            """
            End the current control block (IF/ELSE).
            """
            if not self.control_stack or self.control_stack[-1]["type"] not in {"if", "else"}:
                print("[CRITICAL ERROR]: END without a matching control block. Terminating script.")
                self.cmd_exit()

            # Pop the last block and restore execution state
            self.control_stack.pop()
            self.execution_state = not self.control_stack or self.control_stack[-1].get("executed", True)

            if self.ctrflwdebug:
                print("[DEBUG] END block executed. Restored execution state")

        def should_execute(self):
            """
            Determine if the current block should execute based on the control stack.
            """
            if self.h == 0:
                return True  # Always execute at the base level

            a = self.h
            execute = True  # Assume execution is allowed

            # Check the control stack for preceding conditions
            while a > 0:
                current_block = self.control_stack[a - 1]

                if isinstance(current_block, dict):
                    if current_block.get("type") == "if":
                        if not current_block.get("executed"):
                            execute = False  # A previous 'if' failed, so execution is blocked
                        else:
                            return True  # If a previous 'if' was True, we allow execution
                    elif current_block.get("type") == "else":
                        previous_block = self.control_stack[a - 2] if a - 2 >= 0 else None
                        if previous_block and previous_block.get("allow_else"):
                            execute = True  # Allow execution for valid 'else' blocks
                        else:
                            print("Misplaced else statement")
                            sys1.exit()
                
                a -= 1  # Move up the stack

            return execute  # Return final execution decision

        def parse_condition(self, condition):
            """
            Parse a condition into left-hand side, operator, and right-hand side.
            Args:
                condition (str): The condition string.
            Returns:
                tuple: (left, operator, right) for standard conditions or (left, operator) for 'exists'.
            """
            # Split the condition into parts
            parts = condition.split()
            if len(parts) < 2:
                raise ValueError(f"Invalid condition format: '{condition}'. Expected at least: <left> <operator> [<right>].")

            left = parts[0]
            operator = parts[1]

            # Handle 'exists' which does not require a right operand
            if operator == "exists":
                return left, operator

            if len(parts) < 3:
                raise ValueError(f"Invalid condition format: '{condition}'. Expected: <left> <operator> <right>.")

            right = ' '.join(parts[2:])
            return left, operator, right


        def eval_condition(self, left, operator, right=None):
            """
            Evaluate a condition by comparing left and right operands using the given operator.

            Args:
                left (str): The left operand, which could be a variable name.
                operator (str): The comparison operator (e.g., '==', 'exists').
                right (str, optional): The right operand, which could be a variable name or literal value.

            Returns:
                bool: The result of the evaluation.
            """
            # Handle the 'exists' operator
            if operator == "exists":
                exists = left in self.variables
                if self.ctrflwdebug:
                    print(f"[DEBUG] Left Value '{left}' in VARIABLES: {exists}")
                return exists

            # Resolve left and right values
            left == left.strip('"')
            if left in self.variables:
                left_value = self.variables[left][0]
                self.cmd_log(f"Left Value {left_value} in VARIABLE_LIST: True")
            else:
                left_value = left
                self.cmd_log(f"Left Value {left_value} in VARIABLE_LIST: False")

            if right in self.variables:
                right_value = self.variables[right][0]
                self.cmd_log(f"Right Value {right_value} in VARIABLE_LIST: True")
            else:
                right_value = right
                self.cmd_log(f"Right Value {right_value} in VARIABLE_LIST: False")
            # Attempt type conversion for numeric comparisons
            try:
                if isinstance(left_value, str) and left_value.isdigit():
                    left_value = int(left_value)
                elif isinstance(left_value, str) and self.is_float(left_value):
                    left_value = float(left_value)

                if right_value is not None:
                    if isinstance(right_value, str) and right_value.isdigit():
                        right_value = int(right_value)
                    elif isinstance(right_value, str) and self.is_float(right_value):
                        right_value = float(right_value)
            except ValueError as e:
                self.cmd_log(f"Type conversion error: {e}")
                return False

            # Debug logging for evaluation
            if self.ctrflwdebug:
                self.cmd_log(f"Evaluating: Left: {left_value}, Operator: {operator}, Right: {right_value}")

            # Perform the operation based on the operator
            try:
                if operator == '==':
                    return left_value == right_value
                elif operator == '>':
                    return left_value > right_value
                elif operator == '<':
                    return left_value < right_value
                elif operator == '>=':
                    return left_value >= right_value
                elif operator == '<=':
                    return left_value <= right_value
                elif operator == '!=':
                    return left_value != right_value
            except TypeError as e:
                self.cmd_log(f"Type mismatch during evaluation: {e}")
                return False

            self.cmd_log(f"Unsupported operator: {operator}")
            return False



        def cmd_prt(self, raw_args):
            """
            Enhanced print command with styled, formatted, and interactive output.
            """
            if not raw_args:
                print("ErrID37: No arguments provided for prt command.")
                return

            # Default configurations
            settings = {
                "color_code": "",
                "alignment": None,
                "delay": None,
                "log_message": False,
                "title": None,
                "save_to_file": None,
                "format_type": None,
                "case": None,
                "border": None,
                "text_effect": None,  # New feature for text effects like bold, italic
            }

            try:
                # Clean and process raw arguments
                args = raw_args[1:-1] if raw_args.startswith('"') and raw_args.endswith('"') else raw_args
                args = args.replace("/n", "\n")
                # Parse settings using regex
                settings_pattern = re.compile(r"(align|delay|title|tofile|format|case|border|effect)=(\S+)")
                matches = settings_pattern.findall(args)
                for key, value in matches:
                    if key == "delay":
                        try:
                            settings[key] = float(value)
                        except ValueError:
                            raise ValueError(f"Invalid delay value: '{value}'")
                    else:
                        settings[key] = value.lower()

                #Removing start and end quotes
                args = settings_pattern.sub("", args).strip()
                args = args[1:-1] if args.startswith('"') and args.endswith('"') else args


                # Handle log flag
                if "log" in args:
                    args = args.replace("log", "").strip()
                    settings["log_message"] = True

                # Variable interpolation
                for var in re.findall(r'\$[a-zA-Z_]\w*', args):
                    var_name = var[1:]
                    args =args.replace(var, str(self.variables.get(var_name, (f"<{var_name}>",))[0]))

                # Case transformations
                if settings["case"] == "upper":
                    args = args.upper()
                elif settings["case"] == "lower":
                    args = args.lower()

                # Alignment handling
                if settings["alignment"] == "center":
                    args = args.center(80)
                elif settings["alignment"] == "right":
                    args = args.rjust(80)
                elif settings["alignment"] == "left":
                    args = args.ljust(80)

                # Add border if specified
                if settings["border"]:
                    border_char = settings["border"] if len(settings["border"]) == 1 else "*"
                    border_line = border_char * (len(args) + 4)
                    args = f"{border_line}\n{border_char} {args} {border_char}\n{border_line}"

                # Apply text effects
                if settings["text_effect"]:
                    if settings["text_effect"] == "bold":
                        args = f"\033[1m{args}\033[0m"
                    elif settings["text_effect"] == "italic":
                        args = f"\033[3m{args}\033[0m"

                # Update terminal title
                if settings["title"]:
                    print(f"\033]0;{settings['title']}\a", end="")

                # Format output
                if settings["format_type"] == "json":
                    args = json.dumps({"message": args}, indent=4)
                elif settings["format_type"] == "html":
                    args = f"<p>{args}</p>"

                # Save to file
                if settings["save_to_file"]:
                    with open(settings["save_to_file"], "w") as file:
                        file.write(args + "\n")

                # Log message
                if settings["log_message"]:
                    self.log_messages.append(args)

                # Animated printing with delay
                if settings["delay"]:
                    for char in args:
                        print(settings["color_code"] + char, end="", flush=True)
                        time.sleep(settings["delay"])
                    print("\033[0m")  # Reset color
                elif args=="output":
                    print(self.output)    
                else:
                    print(settings["color_code"] + args + "\033[0m")
                if self.prtdebug:
                    print("[DEBUG] Print Settings: ")
            except ValueError as e:
                print(f"ErrID38: Value error in prt command. Details: {e}")
            except Exception as e:
                print(f"ErrID39: Unexpected error in prt command. Details: {e}")


        def cmd_create_file(self, args):
            """
            Creates a new file and writes content to it.
            Syntax: create_file filename "content"
            """
            try:
                parts = args.split(' ', 1)
                if len(parts) < 2:
                    print("ErrID50: Missing filename or content for create_file command.")
                    return
                
                filename = parts[0]
                content = parts[1][1:-1] if parts[1].startswith('"') and parts[1].endswith('"') else parts[1]
                with open(filename, 'w') as f:
                    f.write(content)
                print(f"File '{filename}' created successfully.")
            except Exception as e:
                print(f"ErrID51: Failed to create file. Error: {e}")

        def cmd_read_file(self, args):
            """
            Reads the content of a file and prints or stores it.
            Syntax: read_file filename [var_name]
            """
            parts = args.split()

            # Ensure the command has at least the required arguments
            if len(parts) < 2:
                print("ErrID52: Missing filename or variable name for read_file command.")
                return

            filename = parts[0]

            # Check if the filename is a variable reference and not a quoted literal
            if filename in self.variables and not (filename.startswith('"') and filename.endswith('"')):
                filename = self.variables[filename][0]

            try:
                with open(filename, 'r') as f:
                    content = f.read()

                var_name = parts[1]  # Store the content in the specified variable
                self.store_variable(var_name, content, "str")
                print(f"File content stored in variable '{var_name}'.")
            except FileNotFoundError:
                print(f"ErrID53: File '{filename}' not found.")
            except Exception as e:
                print(f"ErrID54: Failed to read file. Error: {e}")

        def cmd_append_file(self, args):
            """
            Appends content to an existing file.
            Syntax: append_file filename "content"
            """
            try:
                parts = args.split(' ', 1)
                if len(parts) < 2:
                    print("ErrID55: Missing filename or content for append_file command.")
                    return
                
                filename = parts[0]
                content = parts[1].strip('"')  # Strip quotes from content
                with open(filename, 'a') as f:
                    f.write(content)
                print(f"Content appended to file '{filename}' successfully.")
            except Exception as e:
                print(f"ErrID56: Failed to append to file. Error: {e}")


        def fetch_data_from_api(self, url=None, timeout=20):
            """Fetch data from a given API URL or from a variable in Var_Reg."""
            if not url:
                print("ErrID11: No URL or variable provided.")
                self.output = None
                return

            if url in self.variables:
                url = self.variables[url]

            if not isinstance(url, str) or not url.strip():
                print("ErrID12: Invalid URL or variable key provided.")
                self.output = None
                return

            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                self.output = response.text.strip()  # Store the fetched data, removing any trailing whitespace
                print(f"[DEBUG] Data fetched and stored in output: {self.output}")
            except requests.exceptions.RequestException as e:
                print(f"ErrID10: Failed to fetch data from API. Error: {e}")
                self.output = None

        def store_variable(self, var_name, value, data_type):
            if not value=="output":
                self.variables[var_name] = (value, data_type)
            else:
                self.variables[var_name] = (self.output, data_type)    
            self.cmd_log(f"Stored variable '{var_name}' with value '{value}' and type {data_type}")
            
        def cmd_fncend(self):
            """Marks the end of a function definition."""
            if hasattr(self, "current_function_name"):
                if self.ctrflwdebug:
                    print(f"[DEBUG] End of function definition for '{self.current_function_name}'")
                # Remove the current function context
                del self.current_function_name
                self.in_function_definition = False  # Update the flag to exit definition mode
        def handle_command(self, command):     
            """Processes commands, handles function definitions, and executes appropriately."""
            #if command.startswith("dev.")==True:
            #    self.dev(command)
            #    return   
            if not self.should_execute():
                # Special handling for control flow commands
                if cmd in {"if", "else", "end"}:
                    if cmd == "if":
                        self.cmd_if(' '.join(parts[1:]))
                        self.h += 1  # Register the block if necessary
                    elif cmd == "else":
                        self.cmd_else()
                        self.h += 1
                    elif cmd == "end":
                        self.cmd_end()
                        self.h -= 1
                    elif cmd == "dev.debug":
                        return True    
                else:
                    # Skip non-control-flow commands
                    if self.cmdhandlingdebug:
                        print(f"[DEBUG] Skipping command '{command}' due to if_stack state.")
                    print("skipped")
                    return
                print("skipped")
                return
            if command == "fncend":
                self.cmd_fncend()
                return
            command = command.strip()
            if not command or command.startswith("//"):  # Ignore comments or empty lines
                return


            # Check if the command is 'prt' to preserve whitespace
            if command.startswith("prt"):
                parts = re.findall(r'\S+|\s+', command)
            else:
                parts = command.split()

            cmd = parts[0].strip()
            # Check if the current command should execute


            if cmd in self.command_mapping or cmd in self.exceptional_commands:
                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Handling command: '{command}'")
                if command=="//" or command=="" or command==" ":
                    return
                # If in function definition mode, add command to function and return
                if getattr(self, "in_function_definition", False):
                    if cmd != "fncend":  # Avoid adding 'fncend' to the function's list
                        self.functions[self.current_function_name].append(command)
                        if self.cmdhandlingdebug:
                            print(f"[DEBUG] Adding command '{command}' to function '{self.current_function_name}'")
                    return

                # Commands that don’t take arguments
                no_arg_commands = ["else","end","dev.custom","flush"]

                # Process command if recognized
                if cmd in self.command_mapping:
                    if cmd in no_arg_commands:
                        self.command_mapping[cmd]()
                    else:
                        # Keep whitespace intact for `prt`, standard join for other commands
                        args = ''.join(parts[1:]).strip() if cmd == "prt" else ' '.join(parts[1:])
                        self.command_mapping[cmd](args)

                    if self.cmdhandlingdebug:
                        print(f"[DEBUG] Command '{cmd}' executed with args: '{args if 'args' in locals() else ''}'")
            else:
                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Unrecognized command: {command}. Known commands: {list(self.command_mapping.keys())} AND Exceptional commands: {list(self.exceptional_commands.keys())}")
                self.cmd_log("ErrId0:Unknown Command, Terminating Script")   
                sys.exit(0)
        def dev(self, raw_args):
            args = raw_args.split()
            dbg_option = args[0]
            if dbg_option == "controlflow":
                self.ctrflwdebug = True  
            elif dbg_option == "print":
                self.prtdebug = True
            elif dbg_option == "math":
                self.mathdebug = True
            elif dbg_option == "file":
                self.filedebug = True    
            elif dbg_option == "colorama":
                self.clramadebug = True
            elif dbg_option == "requests":
                self.reqdebug = True  
            elif (dbg_option == "None") or (dbg_option == "All"):
                self.debug = True
                self.ctrflwdebug = True
                self.prtdebug = True
                self.mathdebug = True
                self.filedebug = True
                self.clramadebug = True
                self.cmdhandlingdebug = True
                self.reqdebug = True
            else:
                print("[SELF-DEBUG] Incorrect usuage of the debug command")    
        def cmd_try(self, args):
            self.control_stack.append({
                "type": "try",
                "active": True,
                "error": None
            })
            self.cmd_log("[LOG] Entering try block")

        def cmd_catch(self, args):
            if not self.control_stack or self.control_stack[-1]["type"] != "try":
                print("ErrID35: 'catch' command outside of 'try' block")
                self.cmd_exit("Exiting due to invalid catch command.")
                return

            current_try = self.control_stack[-1]
            if current_try["error"]:
                error_message = current_try["error"]
                self.control_stack.pop()  # Pop the try block after handling
                self.cmd_log(f"[LOG] Catching exception: {error_message}")
                # Handle the catch block logic
                # You can add custom behavior here (e.g., setting default values)

                # Default action: set 'age' to 18 if an error occurred
                self.store_variable("age", 18, "int")
                self.cmd_log(f"[LOG] Defaulting age to 18")

            else:
                print("ErrID36: No error to catch")
                self.cmd_exit("Exiting due to invalid catch behavior.")

        def cmd_log(self, *args):
            """
            Logs messages or variable states for debugging.
            Accepts multiple arguments and concatenates them into a single log message.

            Args:
                *args: Variable number of arguments to be logged.
            """
            # Join all arguments into a single string
            message = " ".join(map(str, args))

            # Optionally, write logs to a file if in debug mode
            with open("x3_debug.log", "a") as log_file:
                log_file.write(f"{message}\n")

            # Print to the console in debug mode
            if self.debug:
                print(f"[DEBUG] {message}")
                self.debuglog.append(f"[DEBUG] {message}")

        def cmd_reg(self, args):
            # Ensure we have at least 3 elements in args (variable name, data type, and value)
            arg = args.split()
            
            if len(arg) < 3:
                print("ErrID3: Incorrect number of arguments for reg command")
                self.cmd_exit()
                return

            var_name = arg[0]
            data_type = arg[1]
            value = " ".join(arg[2:])

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
        def cmd_delete_file(self, args):
            """
            Deletes a specified file.
            Syntax: delete_file filename
            """
            filename = args.strip()
            try:
                sys1.remove(filename)
                print(f"File '{filename}' deleted successfully.")
            except FileNotFoundError:
                print(f"ErrID57: File '{filename}' not found.")
            except Exception as e:
                print(f"ErrID58: Failed to delete file. Error: {e}")
        def cmd_create_dir(self, args):
            """
            Creates a new directory.
            Syntax: create_dir directory_name
            """
            directory_name = args.strip()
            try:
                sys1.makedirs(directory_name, exist_ok=True)
                print(f"Directory '{directory_name}' created successfully.")
            except Exception as e:
                print(f"ErrID59: Failed to create directory. Error: {e}")
        def cmd_delete_dir(self, args):
            """
            Deletes an empty directory.
            Syntax: delete_dir directory_name
            """
            directory_name = args.strip()
            try:
                sys1.rmdir(directory_name)
                print(f"Directory '{directory_name}' deleted successfully.")
            except FileNotFoundError:
                print(f"ErrID60: Directory '{directory_name}' not found.")
            except OSError:
                print(f"ErrID61: Directory '{directory_name}' is not empty.")
            except Exception as e:
                print(f"ErrID62: Failed to delete directory. Error: {e}")
        def cmd_search_file(self, args):
            """
            Searches for a keyword or pattern in a file.
            Syntax: search_file filename "keyword"
            """
            try:
                parts = args.split(' ', 1)
                if len(parts) < 2:
                    print("ErrID63: Missing filename or keyword for search_file command.")
                    return

                filename, keyword = parts[0], parts[1].strip('"')
                with open(filename, 'r') as f:
                    lines = f.readlines()
                results = [line.strip() for line in lines if keyword in line]
                if results:
                    print(f"Found {len(results)} matching lines:")
                    for line in results:
                        print(line)
                else:
                    print(f"No matches found for '{keyword}' in '{filename}'.")
            except FileNotFoundError:
                print(f"ErrID64: File '{filename}' not found.")
            except Exception as e:
                print(f"ErrID65: Failed to search file. Error: {e}")
        def cmd_sqrt(self, args):
            """
            Calculates the square root of a number.
            Syntax: sqrt var_name
            """
            try:
                var_name = args.strip()
                if var_name in self.variables and isinstance(self.variables[var_name][0], (int, float)):
                    value = self.variables[var_name][0]
                    result = value ** 0.5
                    self.store_variable(f"{var_name}_sqrt", result, "float")
                    print(f"Square root of {value} stored in '{var_name}_sqrt'.")
                else:
                    print(f"ErrID66: Variable '{var_name}' not defined or not numeric.")
            except Exception as e:
                print(f"ErrID67: Failed to calculate square root. Error: {e}")
        def cmd_sys_info(self, args):
            """
            Displays system information.
            Syntax: sys_info
            """
            import platform
            info = {
                "OS": platform.system(),
                "Version": platform.version(),
                "Release": platform.release(),
                "Processor": platform.processor(),
            }
            for key, value in info.items():
                print(f"{key}: {value}")
        def cmd_set_env(self, args):
            """
            Sets an environment variable.
            Syntax: set_env VAR_NAME value
            """
            try:
                parts = args.split(' ', 1)
                if len(parts) < 2:
                    print("ErrID68: Missing variable name or value for set_env command.")
                    return

                var_name, value = parts[0], parts[1]
                sys1.environ[var_name] = value
                print(f"Environment variable '{var_name}' set to '{value}'.")
            except Exception as e:
                print(f"ErrID69: Failed to set environment variable. Error: {e}")

        def cmd_inp(self, raw_args):
            """
            inp command: Takes user input and stores it as a variable.
            Usage: inp var_name "prompt" [default]
            """
            try:
                # Properly split arguments using shlex (handles quotes correctly)
                args = shlex.split(raw_args)
                
                if len(args) < 2:
                    error_message = "ErrID3: Missing arguments for inp command. Usage: inp var_name \"prompt\" [default]"
                    if self.control_stack and self.control_stack[-1]["type"] == "try":
                        self.control_stack[-1]["error"] = error_message
                        self.cmd_log(f"[ERROR] {error_message}")
                    else:
                        print(f"[CRITICAL ERROR]: {error_message}")
                        self.cmd_exit("Exiting due to error in inp command.")
                    return

                # Extract arguments
                var_name = args[0]
                prompt = args[1]
                default = args[2] if len(args) > 2 else None

                # Prompt user for input
                user_input = input(f"{prompt} [{default if default else 'no default'}]: ").strip()

                # Use default if input is empty
                if not user_input and default is not None:
                    user_input = default

                # Dynamically detect the type of input
                if user_input.lower() in ["true", "false"]:
                    value, var_type = (user_input.lower() == "true", 'bool')
                elif user_input.isnumeric():
                    value, var_type = (int(user_input), 'int')
                elif user_input.replace('.', '', 1).isdigit() and user_input.count('.') == 1:
                    value, var_type = (float(user_input), 'float')
                else:
                    value, var_type = (user_input, 'str')

                # Update existing variable or store a new one
                if var_name in self.variables:
                    self.variables[var_name] = (value, var_type)
                    self.cmd_log(f"Updated variable: {var_name} = {value} ({var_type})")
                else:
                    self.store_variable(var_name, value, var_type)
                    self.cmd_log(f"Stored input: {var_name} = {value} ({var_type})")

            except Exception as e:
                error_message = f"Error in inp command: {str(e)}"
                if self.control_stack and self.control_stack[-1]["type"] == "try":
                    self.control_stack[-1]["error"] = error_message
                    self.cmd_log(f"[ERROR] {error_message}")
                else:
                    print(f"[CRITICAL ERROR]: {error_message}")
                    self.cmd_exit("Exiting due to error in inp command.")

            
        def cmd_fetch(self, args):
            if len(args) < 1:
                print("ErrID3: Incorrect number of arguments for fetch command")
                self.cmd_exit()
                return
            url = args[0]
            if url in self.variables:           
                self.fetch_data_from_api(self.variables[url])
            else:
                self.fetch_data_from_api(args)
        def cmd_exit(self, args=None):
            if args:
                print(f"[CRITICAL ERROR]: {args}")
            print("Terminating script.")
            exit()  # Safely exits the script, or you can use other termination logic


        def log_debug(self, message):
            """Unified debug logger."""
            if self.debug:
                print(f"[DEBUG] {message}")
                self.debuglog.append(f"[DEBUG] {message}")
        def cmd_exit_ce(self):
            """Exit the program with an error message."""
            print("Exiting due to an error.")
            exit(1)

        """
        //Deprecated
        def cmd_for(self, args):
            try:
                loop_var, start, end, step = args
                start, end, step = int(start), int(end), int(step)
                self.loop_stack.append((loop_var, start, end, step))
                for i in range(start, end, step):
                    self.variables[loop_var] = (i, 'int')
                    self.log_debug(f"Loop iteration {loop_var} = {i}")
            except ValueError:
                print("ErrID40: Invalid arguments for 'for' loop. Expected: var start end step")
                self.cmd_exit()
                */
        """
        def cmd_while(self, condition):
            """
            Implements the while-loop functionality in the interpreter.

            Args:
                condition (str): The loop condition to evaluate.
            """
            try:
                # Parse the condition into left, operator, and right
                left, operator, right = self.parse_condition(condition)

                # Mark the start of a while-loop block
                self.control_stack.append("while")
                loop_body = []

                # Collect commands for the loop body
                while True:
                    command="end"
                    loop_body.append(command)
                    break

                # Execute the loop while the condition evaluates to True
                while self.eval_condition(left, operator, right):
                    for cmd in loop_body:
                        self.handle_command(cmd)

            except Exception as e:
                print(f"[CRITICAL ERROR]: {e}")
                self.cmd_exit()

        def cmd_def(self, args):
            """
            Define a new function. Begins a function definition mode where commands
            will be stored in the function until `fncend` is encountered.

            Args:
                args (str): The name of the function to define.

            Syntax:
                def function_name
            """
            try:
                # Ensure arguments are provided
                tokens = args.strip().split()
                if len(tokens) != 1:
                    raise ValueError("ErrID3: Incorrect number of arguments for 'def' command. Expected syntax: def function_name")

                function_name = tokens[0]

                # Check if a function with the same name already exists
                if function_name in self.functions:
                    raise ValueError(f"ErrID8: Function '{function_name}' already defined.")

                # Initialize a new function in the functions dictionary
                self.functions[function_name] = []
                self.current_function_name = function_name
                self.in_function_definition = True  # Enter function definition mode

                # Debug log
                self.log_debug(f"Defining function '{function_name}'")
                print(f"Function '{function_name}' definition started. Add commands and end with 'fncend'.")

            except ValueError as e:
                print(str(e))
                self.cmd_exit("Exiting due to function definition error.")
            except Exception as e:
                print(f"Unexpected error in 'def' command: {str(e)}")
                self.cmd_exit("Exiting due to an unexpected error in 'def' command.")


        def cmd_call(self, args):
            """Call a defined function."""
            function_name = args.split()[0]
            if function_name not in self.functions:
                print(f"ErrID36: Function '{function_name}' not defined.")
                self.cmd_exit()

            self.log_debug(f"Calling function '{function_name}'")
            for command in self.functions[function_name]:
                self.handle_command(command)

        def cmd_switch(self, args):
            """Switch-case implementation."""
            if not args:
                print("ErrID3: Incorrect number of arguments for switch command")
                self.cmd_exit()

            switch_var = args[0]
            if switch_var not in self.variables:
                print(f"ErrID31: Variable '{switch_var}' not defined.")
                self.cmd_exit()

            self.control_stack.append({"type": "switch", "variable": self.variables[switch_var][0], "executed": False})

        def cmd_case(self, args):
            """Case block in a switch."""
            if not self.control_stack or self.control_stack[-1]["type"] != "switch":
                print("ErrID32: 'case' command outside of 'switch' block.")
                self.cmd_exit()

            case_value = args[0]
            current_switch = self.control_stack[-1]
            if not current_switch["executed"] and current_switch["variable"] == case_value:
                current_switch["executed"] = True
                self.handle_command(" ".join(args[1:]))

        def cmd_default(self, args):
            """Default block in a switch."""
            if not self.control_stack or self.control_stack[-1]["type"] != "switch":
                print("ErrID33: 'default' command outside of 'switch' block.")
                self.cmd_exit()

            self.control_stack[-1]["default"] = args

        def cmd_inc(self, args):
            """Increment a variable."""
            if len(args) != 1:
                print("ErrID3: Incorrect number of arguments for inc command")
                self.cmd_exit()

            var_name = args[0]
            if var_name in self.variables and self.variables[var_name][1] == "int":
                self.variables[var_name] = (self.variables[var_name][0] + 1, "int")
            else:
                print(f"ErrID34: Variable '{var_name}' not defined or not an integer.")
                self.cmd_exit()

        def cmd_dec(self, args):
            """Decrement a variable."""
            if len(args) != 1:
                print("ErrID3: Incorrect number of arguments for dec command")
                self.cmd_exit()

            var_name = args[0]
            if var_name in self.variables and self.variables[var_name][1] == "int":
                self.variables[var_name] = (self.variables[var_name][0] - 1, "int")
            else:
                print(f"ErrID34: Variable '{var_name}' not defined or not an integer.")
                self.cmd_exit()

        def cmd_repeat(self, args):
            """Repeat a command a given number of times."""
            if len(args) != 2:
                print("ErrID3: Incorrect number of arguments for repeat command")
                self.cmd_exit()

            try:
                loop_count = int(args[0])
                command_to_repeat = args[1]
                for _ in range(loop_count):
                    self.handle_command(command_to_repeat)
            except ValueError:
                print("ErrID3: Loop count must be an integer.")
                self.cmd_exit()

        def cmd_wait(self, args):
            """Wait for a specified number of seconds."""
            if len(args) != 1:
                print("ErrID3: Incorrect number of arguments for wait command")
                self.cmd_exit()

            try:
                duration = int(args[0])
                self.log_debug(f"Waiting for {duration} seconds...")
                time.sleep(duration)
            except ValueError:
                print("ErrID3: Duration must be an integer.")
                self.cmd_exit()

            
        def cmd_read_log(self, args):
            for message in self.log_messages:
                print("This feature was removed due to memory errors and slow proessing speeds")

        def cmd_add(self, args):
            self.perform_arithmetic_operation(args, operation="add")

        def cmd_sub(self, args):
            self.perform_arithmetic_operation(args, operation="sub")

        def cmd_mul(self, args):
            self.perform_arithmetic_operation(args, operation="mul")

        def cmd_div(self, args):
            self.perform_arithmetic_operation(args, operation="div")

        def cmd_mod(self, args):
            self.perform_arithmetic_operation(args, operation="mod")
        import shlex  # Import for proper argument parsing

        def perform_arithmetic_operation(self, args, operation):
            """
            Handles arithmetic operations dynamically with improved error handling.
            Supported operations: add, sub, mul, div, mod
            """
            try:
                # Properly parse arguments using shlex to handle spaces correctly
                args = shlex.split(args)
                if len(args) != 3:
                    raise ValueError(f"Incorrect number of arguments. Expected 3, got {len(args)}. Syntax: <var_name> <operand1> <operand2>")

                var_name, op1, op2 = args

                # Retrieve and validate operand values
                try:
                    operand1 = self.get_variable_value(op1)
                    operand2 = self.get_variable_value(op2)
                except KeyError as e:
                    raise KeyError(f"Variable '{e.args[0]}' not defined.")

                # Ensure operands are numeric
                try:
                    operand1 = float(operand1) if '.' in str(operand1) else int(operand1)
                    operand2 = float(operand2) if '.' in str(operand2) else int(operand2)
                except ValueError:
                    raise TypeError("Operands must be valid numeric values.")

                # Define supported operations
                operations = {
                    "add": lambda x, y: x + y,
                    "sub": lambda x, y: x - y,
                    "mul": lambda x, y: x * y,
                    "div": lambda x, y: x / y if y != 0 else ZeroDivisionError("Division by zero is not allowed."),
                    "mod": lambda x, y: x % y if y != 0 else ZeroDivisionError("Modulo by zero is not allowed.")
                }

                # Execute operation
                if operation not in operations:
                    raise ValueError(f"Unsupported operation '{operation}'. Valid operations: {', '.join(operations.keys())}")

                result = operations[operation](operand1, operand2)

                if isinstance(result, ZeroDivisionError):
                    raise result  # Trigger error if division/modulo by zero

                # Determine result type
                result_type = "int" if isinstance(result, int) else "float"
                self.store_variable(var_name, result, result_type)

                if self.mathdebug:
                    print(f"[DEBUG] Stored result: {var_name} = {result} ({result_type})")

            except (KeyError, ValueError, TypeError) as e:
                print(f"[ERROR] {e}")
            except ZeroDivisionError as e:
                print(f"[ERROR] {e}")
            except Exception as e:
                print(f"[ERROR] Unexpected error during {operation}: {e}")

        def get_variable_value(self, var_name):
            """
            Fetches the value of a variable, ensuring it exists and is numeric.
            """
            if var_name in self.variables:
                value, var_type = self.variables[var_name]
                if not isinstance(value, (int, float)):
                    if value.isnumeric():
                        return int(value)
                    else:
                        raise ValueError(f"Variable '{var_name}' is not numeric.")
                return value
            
            else:
                # If not a variable, attempt to cast directly
                try:
                    return int(var_name) if "." not in var_name else float(var_name)
                except ValueError:
                    raise KeyError(var_name)
    def main():
        parser = argparse.ArgumentParser(description="X3 Interpreter")
        parser.add_argument('-f', '--file', type=str, help='File to execute as a script')
        parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
        args = parser.parse_args()
        
        #uses debug mode if nessecary
        interpreter = Interpreter(debug=args.debug)

        # If a file is provided, read commands from the file
        if args.file:
            try:
                with open(args.file, 'r') as script_file:
                    for line in script_file:
                        interpreter.handle_command(line.strip())
            except Exception as exc:
                print(f"Could not load {args.file} due to reason:{exc}")            
        else:
            # IDLE mode (Will be removed in v3.x idk)
            while True:
                try:
                    user_input = input(">>")
                    interpreter.handle_command(user_input.strip())
                except (KeyboardInterrupt, EOFError):
                    print("\nExiting.")
                    break
    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"[CRITICAL ERROR]: {e},\nTerminating script.")
#Official 1k lines of code!!-November/24
#Official X3 Runner release -January/25
