#this software is licenced under CCPA4.0 BY-SA-NC, for more information check: https://creativecommons.org/licenses/by-nc-sa/4.0

import argparse
import time
import re
import os as sys1
import shlex 
import json
import difflib
import subprocess
import sys
import importlib
idle=0 #on default script mode.
version=3.6 #version (For IDE and more)
def install_package(package, alias=None): #package installation using subprocess.
    try:
        # Try importing the package
        module = importlib.import_module(package)
        if idle==1:
            print(f"{package} is already installed.")
    except ImportError:
        # Install the package if not found
        
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        # Try importing again after installation
        try:
            module = importlib.import_module(package)
        except ImportError:
            print(f"Error: Failed to import {package} after installation.")
            return None

    # Set alias if provided (eg:import {package} as alias)
    if alias:
        globals()[alias] = module
        print(f"Imported {package} as {alias}.")
    else:
        globals()[package] = module  # Standard import

    return module  
#install colorama and requests at the start. (too lazy to use this same command over and over again accross funcs :3)
install_package("colorama")
install_package("requests")

"""
Requirements:
__Python3.6+
__Pip(Latest Update for better experience)
__Basic Internet Access
__Minimal Hardware resources:2GB Ram
__[Terminal which supports ANSI color codes] #optional
__Patience because python is slow af :P

"""

try:
    
    class Interpreter:
        def __init__(self, debug=False): #debug set to false as default, you wouldn't want 100 lines of debug as default dont you?
            
            self.variables = {} #variable dictionary
            self.functions = {} #function dictionary, kinda messy
            self.control_stack = [] #that if else and stuff, for basic control flow monitoring
            self.debug = False #only used as a placeholder, replaced by the new BETTER debug system
            self.debuglog = [] #i have no idea why i made this
            self.output = None #output for functions like fetch, i will think of improving this.
            self.log_messages = [] #old log messages record, still works but deprecated
            self.execution_state = {} #thought of removing this but it is still used in some control flow magic so ye.
            #Debug Init---
            self.ctrflwdebug = False
            self.prtdebug = False
            self.mathdebug = False
            self.filedebug = False
            self.clramadebug = False
            self.cmdhandlingdebug = False
            self.reqdebug=False
            self.conddebug=False
            #---
            self.command_mapping = { 
                'terminal': self.cmd_open_terminal,
                'goto': self.cmd_goto,
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
                'str_len': self.str_len,
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
                 #'switch': self.cmd_switch, removed in eclipse
                 #'case': self.cmd_case, removed in eclipse
                 #'default': self.cmd_default, removed in eclipse
                'inc': self.cmd_inc,
                'dec': self.cmd_dec,
                 #'catch': self.cmd_catch, removed in eclipse
                 #'repeat': self.cmd_repeat, removed in eclipse
                'wait': self.cmd_wait,
                'log': self.cmd_log,
                'fncend': self.cmd_fncend,
                'dev.debug': self.dev,
                'load': self.load,
                'dev.custom': self.DEVCUSTOMTESTING,
                'flush': self.flush,
                'reinit': self.cmd_reinit, 
                '--info': self.info,
            }
            self.exceptional_commands={
                "//",
                "",
                " ",
            }
        
            self.color_dict = { #doesn't works anymore for some reason
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
        def info(self):
            print(version)
        def flush(self):
            self.variables = {}
            self.functions = {}
            self.control_stack = []
            self.debug = False
            self.debuglog = []
            self.output = None
            self.log_messages = []
            self.functions = {}
            self.execution_state = {}
            #Debug Init---
            self.ctrflwdebug = False
            self.prtdebug = False
            self.mathdebug = False
            self.filedebug = False
            self.clramadebug = False
            self.cmdhandlingdebug = False
            self.reqdebug=False
            self.conddebug=False
            #---         
        def load(self, filename):
            try:
                interpreter = Interpreter()
                with open(filename, 'r') as file:
                    for line in file:
                        command = line.strip()
                        interpreter.handle_command(command)
            except FileNotFoundError:
                if self.filedebug:
                    print(f"ErrId53: The file '{filename}' was not found.")
                    if idle == 0: self.cmd_exit()

            except Exception as e:
                if self.filedebug:
                    print(f"[DEBUG] An error occurred while executing commands from '{filename}': {e}")  

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
                print("\n" * 100) #for terminals that dont support cls.

        def cmd_if(self, condition):
            """
            Evaluate an IF condition and push it to the control stack.
            """
            try:
                result = self.eval_condition(condition)  # Pass the full condition as a single string
            except ValueError as e:
                print(f"ErrId77: Invalid IF condition '{condition}'. Details: {e}")
                if idle == 0: self.cmd_exit()

            # Push IF block to control stack (remains until `end`)
            self.control_stack.append({"type": "if", "executed": result, "has_else": False})
            if self.ctrflwdebug:
                print(f"[DEBUG] IF condition '{condition}' evaluated to {result}, pushed to stack.")

            if not result:
                if self.ctrflwdebug:
                    print("[DEBUG] Skipping subsequent commands inside this IF block.")

        def cmd_else(self):
            """
            Execute an ELSE block only if the preceding IF block was false.
            """
            if not self.control_stack:
                print("ErrId78: ELSE without a matching IF.")
                if idle == 0:
                    self.cmd_exit()
                return

            # Check the last block in the stack; it must be an IF block
            last_if = self.control_stack[-1]
            if last_if["type"] != "if":
                print("ErrId78: ELSE without a matching IF.")
                if idle == 0:
                    self.cmd_exit()
                return

            if last_if.get("has_else", False):
                print("ErrId79: Multiple ELSE statements for the same IF.")
                if idle == 0:
                    self.cmd_exit()
                return

            # Mark that this IF block now has an ELSE
            last_if["has_else"] = True

            # Execute ELSE block only if the IF condition was false
            last_if["executed"] = not last_if["executed"]

            if self.ctrflwdebug:
                if last_if["executed"]:
                    print("[DEBUG] ELSE block will execute.")
                else:
                    print("[DEBUG] Skipping ELSE block because IF condition was true.")
                
        def cmd_while(self, condition):
            """
            Implements a while-loop functionality with proper nested execution.
            """
            try:
                result = self.eval_condition(condition)
                self.control_stack.append({
                    "type": "while",
                    "condition": condition,
                    "executed": result,
                    "start_line": self.current_line  # 🚀 STORE WHERE WHILE STARTED
                })
                if self.ctrflwdebug:
                    print(f"[DEBUG] WHILE condition '{condition}' evaluated to {result}, pushed to stack.")
            except ValueError as e:
                print(f"ErrId90: Invalid WHILE condition '{condition}'. Details: {e}")
                if idle == 0: self.cmd_exit()

        def cmd_end(self):
            """
            Properly handle 'end' for while loops, ensuring they actually repeat.
            """
            if not self.control_stack:
                print("ErrId91: END without a matching control block.")
                if idle == 0: self.cmd_exit()
                return

            popped_block = self.control_stack.pop()
            if self.ctrflwdebug:
                print(f"[DEBUG] END: Popped block: {popped_block}")

            if popped_block["type"] == "while":
                if self.eval_condition(popped_block["condition"]):
                    self.control_stack.append(popped_block)  # Keep the loop running
                    self.current_line = popped_block["start_line"] - 1  # 🚀 JUMP BACK TO WHILE!
                else:
                    if self.ctrflwdebug:
                        print(f"[DEBUG] Exiting WHILE loop: {popped_block}")

            if self.control_stack:
                self.execution_state = self.control_stack[-1]["executed"]
            else:
                self.execution_state = True  # Default to true if no conditions are left

        def find_while_start(self, condition):
            """Finds the start of the while loop in the script."""
            for i in range(self.current_line, -1, -1):  # Search backward
                if self.lines[i].strip().startswith("while ") and condition in self.lines[i]:
                    return i  # Jump back to this line
            return self.current_line  # Fail-safe to avoid crashes

        def should_execute(self):
            """
            Determine if the current block should execute based on active IF conditions.
            """
            if not self.control_stack:
                return True  # No active conditions, execute normally

            for i in range(len(self.control_stack) - 1, -1, -1):
                block = self.control_stack[i]
                if self.ctrflwdebug:
                    print(f"[DEBUG] Checking control block at depth {i}: {block}")

                if block["type"] == "if" and not block["executed"]:
                    if self.ctrflwdebug:
                        print("[DEBUG] Skipping execution due to failed IF condition.")
                    return False  # If any parent IF failed, block execution

                if block["type"] == "else" and not block["executed"]:
                    if self.ctrflwdebug:
                        print("[DEBUG] Skipping execution due to failed ELSE condition.")
                    return False  # Block ELSE if the IF was True

            return True  # Default: Execute if no issues were found

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
        def eval_condition(self, condition_str):
            """
            Evaluate an IF condition while ensuring AND (" & ") has higher precedence than OR (" | ").
            Supports negation (!var) and extended comparisons (startswith, endswith, contains).
            """
            if self.conddebug:
                print(f"[DEBUG] Processing IF condition: {condition_str}")  

            # Step 1: Process AND conditions first
            def process_and_conditions(and_condition):
                """Ensure AND conditions are evaluated before OR."""
                and_parts = and_condition.split(" & ")
                results = [process_single_condition(cond.strip()) for cond in and_parts]
                if self.conddebug:
                    print(f"[DEBUG] AND Conditions: {and_parts} -> {results}")  
                return all(results)

            # Step 2: Split OR conditions, evaluating AND groups first
            or_conditions = condition_str.split(" | ")
            
            def try_convert(value):
                """Attempts to convert strings to numbers when needed."""
                if isinstance(value, (int, float)):
                    return value
                if isinstance(value, str) and value.replace(".", "", 1).isdigit():
                    return float(value) if "." in value else int(value)
                return value.strip('"')  # 🚨 STRIP QUOTES FROM STRINGS

            def process_single_condition(cond):
                """Evaluate a single condition safely."""
                parts = cond.split()

                # Handle negation (!var)
                if len(parts) == 1:
                    if parts[0].startswith("!"):
                        var_name = parts[0][1:]  # Remove "!"
                        result = var_name not in self.variables  # NOT condition
                        if self.conddebug:
                            print(f"[DEBUG] Condition '!{var_name}' -> {result}")  
                        return result
                    result = parts[0] in self.variables  # Normal EXISTS check
                    if self.conddebug:
                        print(f"[DEBUG] Condition '{parts[0]} exists' -> {result}")  
                    return result
                
                elif len(parts) >= 3:
                    left = parts[0]
                    operator = parts[1]
                    right = " ".join(parts[2:])  # Handle cases where right side has spaces
                else:
                    if self.conddebug:
                        print(f"[DEBUG] Invalid condition format: {cond}")  
                    return False  # Invalid format

                # Resolve left and right values
                left_value = self.variables.get(left, [left])[0]
                right_value = self.variables.get(right, [right])[0] if right is not None else None

                # Convert both values to numeric if possible
                left_value = try_convert(left_value)
                right_value = try_convert(right_value)

                # Ensure both sides are comparable
                if isinstance(left_value, (int, float)) and isinstance(right_value, str):
                    if self.conddebug:
                        print(f"[DEBUG] Type mismatch: Cannot compare '{left_value}' with '{right_value}'") 
                    return False
                if isinstance(left_value, str) and isinstance(right_value, (int, float)):
                    if self.conddebug:
                        print(f"[DEBUG] Type mismatch: Cannot compare '{left_value}' with '{right_value}'")  
                    return False
                if self.conddebug:
                    print(f"[DEBUG] Evaluating: Left='{left_value}', Operator='{operator}', Right='{right_value}'")  
                comparisons = {
                    "==": lambda x, y: x == y,
                    "!=": lambda x, y: x != y,
                    ">": lambda x, y: x > y,
                    "<": lambda x, y: x < y,
                    ">=": lambda x, y: x >= y,
                    "<=": lambda x, y: x <= y,

                    # Fixed Negated Comparisons
                    "!>": lambda x, y: not (x > y),
                    "!<": lambda x, y: not (x < y),
                    "!>=": lambda x, y: not (x >= y),
                    "!<=": lambda x, y: not (x <= y),
                    "!==": lambda x, y: x is not y,

                    # String Operations
                    "startswith": lambda x, y: str(x).startswith(str(y)),
                    "endswith": lambda x, y: str(x).endswith(str(y)),
                    "contains": lambda x, y: str(y) in str(x),
                    "!contains": lambda x, y: str(y) not in str(x),
                    "equals_ignore_case": lambda x, y: str(x).lower() == str(y).lower(),

                    # Length-Based Comparisons
                    "len==": lambda x, y: len(str(x)) == int(y),
                    "len!=": lambda x, y: len(str(x)) != int(y),
                    "len>": lambda x, y: len(str(x)) > int(y),
                    "len<": lambda x, y: len(str(x)) < int(y),

                    # Identity Comparisons
                    "is": lambda x, y: id(x) == id(y),
                    "is not": lambda x, y: id(x) != id(y),

                    # 🔥 New: `|+|` for Similarity Percentage (0-100%)
                    "|+|": lambda x, y: int(difflib.SequenceMatcher(None, str(x), str(y)).ratio() * 100),
                }

                result = comparisons.get(operator, lambda x, y: False)(left_value, right_value)
                if self.conddebug:
                    print(f"[DEBUG] Condition '{left} {operator} {right}' -> {result}")  
                return result

            # 🚨 Process AND conditions before OR
            results = [process_and_conditions(cond.strip()) for cond in or_conditions]
            if self.conddebug:
                print(f"[DEBUG] OR Conditions: {or_conditions} -> {results}")  
            return any(results)



        def cmd_prt(self, raw_args):
            """
            Enhanced print command with styled, formatted, and interactive output.
            """
            if not raw_args:
                print("ErrID37: No arguments provided for prt command.")
                if idle == 0: self.cmd_exit()

                return

            # Default settings
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
                "text_effect": None,
            }

            try:
                # Preserve spaces inside quotes
                args = raw_args[1:-1] if raw_args.startswith('"') and raw_args.endswith('"') else raw_args
                args = re.sub(r"(?<!\\)/n", "\n", args)  # Replace `/n` with newlines

                # Parse settings using regex
                settings_pattern = re.compile(r"(align|delay|title|tofile|format|case|border|effect|log)(?:=(\S+))?")
                matches = settings_pattern.findall(args)
                for key, value in matches:
                    settings[key] = float(value) if key == "delay" else value.lower()

                # Remove settings from args
                args = settings_pattern.sub("", args).strip().replace("  ", " ")

                # Handle log flag
                if "log" in args.split():
                    args = args.replace("log", "").strip()
                    settings["log_message"] = True

                # Variable interpolation
                args = re.sub(r"\$([a-zA-Z_]\w*)", lambda m: str(self.variables.get(m.group(1), ["<" + m.group(1) + ">"])[0]), args)

                # Apply case transformations
                if settings["case"] == "upper":
                    args = args.upper()
                elif settings["case"] == "lower":
                    args = args.lower()

                # Apply text alignment
                if settings["alignment"] == "center":
                    args = args.center(80)
                elif settings["alignment"] == "right":
                    args = args.rjust(80)
                elif settings["alignment"] == "left":
                    args = args.ljust(80)

                # Add borders if specified
                if settings["border"]:
                    border_char = settings["border"] if len(settings["border"]) == 1 else "*"
                    border_line = border_char * (len(args) + 4)
                    args = f"{border_line}\n{border_char} {args} {border_char}\n{border_line}"

                # Apply text effects
                effect_map = {"bold": "\033[1m", "italic": "\033[3m"}
                if settings["text_effect"] in effect_map:
                    args = f"{effect_map[settings['text_effect']]}{args}\033[0m"

                # Update terminal title
                if settings["title"]:
                    print(f"\033]0;{settings['title']}\a", end="")

                # Format output
                if settings["format_type"] == "json":
                    args = json.dumps({"message": args}, indent=4)
                elif settings["format_type"] == "html":
                    args = f"<p>{args}</p>"

                # Save output to file
                if settings["save_to_file"]:
                    with open(settings["save_to_file"], "w") as file:
                        file.write(args + "\n")

                # Log message if needed
                if settings["log_message"]:
                    self.log_messages.append(args)

                # Handle output & animated printing with delay
                if settings["delay"]:
                    for char in args:
                        sys.stdout.write(settings["color_code"] + char)
                        sys.stdout.flush()
                        time.sleep(settings["delay"])
                    print("\033[0m")  # Reset color
                elif args.strip() == "output":
                    print(self.output)
                else:
                    print(args)

                if self.prtdebug:
                    print("[DEBUG] Print Settings: ", settings)

            except ValueError as e:
                print(f"ErrID38: Value error in prt command. Details: {e}")
                if idle == 0: self.cmd_exit()

            except Exception as e:
                print(f"[CRITICAL ERROR] Unexpected error in prt command. Details: {e}")
                self.cmd_exit()


        def cmd_create_file(self, args):
            """
            Creates a new file and writes content to it.
            Syntax: create_file filename "content"
            """
            try:
                parts = args.split(' ', 1)
                if len(parts) < 2:
                    print("ErrID50: Missing filename or content for create_file command.")
                    if idle == 0: self.cmd_exit()

                    return
                
                filename = parts[0]
                content = parts[1][1:-1] if parts[1].startswith('"') and parts[1].endswith('"') else parts[1]
                with open(filename, 'r', encoding='utf-8', errors='replace') as f:
                    f.write(content)
                print(f"File '{filename}' created successfully.")
            except Exception as e:
                print(f"[CRITICAL ERROR] Failed to create file. Error: {e}")
                self.cmd_exit()


        def cmd_read_file(self, args):
            """
            Reads the content of a file and prints or stores it.
            Syntax: read_file filename [var_name]
            """
            parts = args.split()

            # Ensure the command has at least the required arguments
            if len(parts) < 2:
                print("ErrID52: Missing filename or variable name for read_file command.")
                if idle == 0: self.cmd_exit()

                return

            filename = parts[0]

            # Check if the filename is a variable reference and not a quoted literal
            if filename in self.variables and not (filename.startswith('"') and filename.endswith('"')):
                filename = self.variables[filename][0]

            try:
                with open(filename, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()

                var_name = parts[1]  # Store the content in the specified variable
                self.store_variable(var_name, content, "str")
                print(f"File content stored in variable '{var_name}'.")
            except FileNotFoundError:
                print(f"ErrID53: File '{filename}' not found.")
                if idle == 0: self.cmd_exit()

            except Exception as e:
                print(f"[CRITICAL ERROR] Failed to read file. Error: {e}")
                self.cmd_exit()
        def cmd_append_file(self, args):
            """
            Appends content to an existing file.
            Syntax: append_file filename "content"
            """
            try:
                parts = args.split(' ', 1)
                if len(parts) < 2:
                    print("ErrID55: Missing filename or content for append_file command.")
                    if idle == 0: self.cmd_exit()

                    return
                
                filename = parts[0]
                content = parts[1].strip('"')  # Strip quotes from content
                with open(filename, 'r', encoding='utf-8', errors='replace') as f:
                    f.write(content)
                print(f"Content appended to file '{filename}' successfully.")
            except Exception as e:
                print(f"[CRITICAL ERROR] Failed to append to file. Error: {e}")
                self.cmd_exit()

        def fetch_data_from_api(self, url=None, timeout=20):
            """Fetch data from a given API URL or from a variable in Var_Reg."""
            if not url:
                print("ErrID11: No URL or variable provided.")
                self.output = None
                if idle == 0: self.cmd_exit()

                return

            if url in self.variables:
                url = self.variables[url]

            if not isinstance(url, str) or not url.strip():
                print("ErrID12: Invalid URL or variable key provided.")
                self.output = None
                if idle == 0: self.cmd_exit()

                return

            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                self.output = response.text.strip()  # Store the fetched data, removing any trailing whitespace
                if self.reqdebug:
                    print(f"[DEBUG] Data fetched and stored in output: {self.output}")
            except requests.exceptions.RequestException as e:
                print(f"[CRITICAL ERROR] Failed to fetch data from API. Error: {e}")
                self.output = None
                self.cmd_exit()


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
            
            if command.startswith("prt"):
                parts = re.findall(r'\S+|\s+', command)
            else:
                parts = command.split()

            if not command or command.startswith("//"):  # Ignore comments or empty lines
                return
            if not command.startswith('prt '):
                command = command.strip()
            else:
                command = command[4:]  # Remove "prt " but keep spaces
            cmd = parts[0].strip()

            # FIRST, CHECK `should_execute()`
            if not self.should_execute():
                if cmd in {"else", "end"}:
                    if self.ctrflwdebug:
                        print(f"[DEBUG] Handling '{cmd}' command even in a failed IF block.")
                    self.command_mapping[cmd]()  # Ensure `else` and `end` always execute
                    return
                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Skipping command '{command}' due to failed IF condition.")
                return  # Exit immediately, preventing execution

            # If command is recognized, handle it
            if cmd in self.command_mapping:
                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Handling command: '{command}'")
                
                # Process commands that don't require arguments
                no_arg_commands = ["else","end","dev.custom","flush","--info"]
                if cmd in no_arg_commands:
                    self.command_mapping[cmd]()
                else:
                    args = ' '.join(parts[1:]).strip()
                    self.command_mapping[cmd](args)
                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Command '{cmd}' executed with args: '{args if 'args' in locals() else ''}'")
            else:
                print(f"ErrId73: Unrecognized command: {command}.")
                if idle == 0: self.cmd_exit()

        def dev(self, raw_args):
            """
            Enable or disable various debugging options dynamically.
            
            Usage:
            - dev controlflow  → Enables control flow debugging
            - dev print        → Enables print debugging
            - dev math         → Enables math debugging
            - dev file         → Enables file handling debugging
            - dev colorama     → Enables Colorama debugging
            - dev requests     → Enables requests debugging
            - dev condition    → Enables condition evaluation debugging
            - dev All          → Enables all debugging options
            - dev cmdhandling  → Enables Command handling debugging
            - dev None         → Disables all debugging options
            """
            
            # 🚀 Debugging options dictionary
            debug_options = {
                "controlflow": "ctrflwdebug",
                "print": "prtdebug",
                "math": "mathdebug",
                "file": "filedebug",
                "colorama": "clramadebug",
                "requests": "reqdebug",
                "cmdhandling": "cmdhandlingdebug",
                "condition": "conddebug",  # 🆕 Added condition debugging
            }

            if not raw_args.strip():
                print("[SELF-DEBUG] Please provide a debug option (e.g., 'dev controlflow').")
                return

            args = raw_args.lower().split()  # Convert input to lowercase for case-insensitive matching

            if "all" in args or "none" in args:
                # ✅ Toggle all debugging options
                enable = "all" in args
                self.debug = enable
                for attr in debug_options.values():
                    setattr(self, attr, enable)
                print(f"[SELF-DEBUG] {'Enabled' if enable else 'Disabled'} all debugging options.")
                return

            # ✅ Enable specific debug options
            enabled_any = False
            for dbg_option in args:
                if dbg_option in debug_options:
                    setattr(self, debug_options[dbg_option], True)
                    print(f"[SELF-DEBUG] Enabled debugging for: {dbg_option}")
                    enabled_any = True
                else:
                    print(f"[SELF-DEBUG] Incorrect usage: Unknown debug option '{dbg_option}'.")

            if not enabled_any:
                print("[SELF-DEBUG] No valid debug options provided. Use 'dev All' to enable all.")


        """
        def cmd_try(self, args):
            self.control_stack.append({
                "type": "try",
                "active": True,
                "error": None
            })
            self.cmd_log("[LOG] Entering try block")
        """
        """
        #DEPRECATED IN ECLIPSE
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
        """
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
        def str_len(self, args):
            """
            Returns the length of a string variable.
            Syntax: str_len var_name result_var
            """
            parts = args.split()
            if len(parts) != 2:
                print("ErrID70: Incorrect syntax for str_len. Expected: str_len var_name result_var")
                if idle == 0: self.cmd_exit()

                return

            var_name, result_var = parts  

            if var_name in self.variables:
                value = self.variables[var_name][0]
                if isinstance(value, str):
                    length = len(value)
                    self.store_variable(result_var, length, "int")
                    if self.cmdhandlingdebug:
                        print(f"[DEBUG]Length of '{var_name}' stored in '{result_var}': {length}")
                else:
                    print(f"ErrID71: Variable '{var_name}' is not a string.")
                    if idle == 0: self.cmd_exit()

                print(f"ErrID72: Variable '{var_name}' not found.")
                if idle == 0: self.cmd_exit()

        def similarity_percentage(self, str1, str2):
            return int(difflib.SequenceMatcher(None, str(str1), str(str2)).ratio() * 100)

        def cmd_reg(self, raw_args):
            """
            Register a variable, allowing math expressions if 'eval=True' is provided.
            Supports operations: +, -, *, /, (), and variables.

            Example:
            reg int var1 5
            reg int var2 (var1 * 10) / 2 eval=True
            """

            parts = raw_args.split()
            if len(parts) < 3:
                print("ErrId80: Invalid variable registration format.")
                if idle == 0: self.cmd_exit()
                return

            var_type = parts[0]   # int, float, str, etc.
            var_name = parts[1]   # Variable name
            var_value = " ".join(parts[2:])  # Everything after var name
            if "|+|" in var_value:
                var_value = re.sub(r'(\w+)\s*\|\+\|\s*(\w+)', r'self.similarity_percentage(\1, \2)', var_value)

            # Check if eval=True is present
            math_mode = "eval=True" in var_value
            if math_mode:
                var_value = var_value.replace("eval=True", "").strip().strip('"')  # Remove extra quotes

            for var in re.findall(r'\b[a-zA-Z_]\w*\b', var_value):  
                if var in self.variables:  
                    var_type = type(self.variables[var][0])
                    if var_type == str:
                        var_value = var_value.replace(var, f'"{self.variables[var][0]}"')  # Keep as string
                    else:
                        var_value = var_value.replace(var, str(self.variables[var][0]))  # Convert numbers properly

                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Math expression before eval: {var_value} (Type: {type(var_value)})")  # 🚀 Debugging

            try:
                # Skip eval() if var_value is already numeric
                if isinstance(var_value, (int, float)) or var_value.replace(".", "", 1).isdigit():
                    var_value = float(var_value) if "." in var_value else int(var_value)
                else:
                    # 🚀 Evaluate only if it's an actual math expression
                    if isinstance(var_value, (str, bool)) and math_mode:
                        var_value = var_value
                    else:
                        var_value = eval(var_value)

            except ValueError as ve:
                print(ve)
                return
            except SyntaxError:
                print(f"ErrId84: Invalid Expression: {var_value}")
                return
            except Exception as e:
                if self.mathdebug:
                    print(f"[CRITICAL ERROR] Math evaluation failed: {e}")
                if idle == 0: self.cmd_exit()
                return

            # 🚀 Improved type handling with strict checks
            try:
                # Ensure correct type handling
                if isinstance(var_value, int):
                    self.variables[var_name] = [var_value]  # Store properly as an int
                elif isinstance(var_value, float):
                    self.variables[var_name] = [var_value]  # Store as float
                else:
                    self.variables[var_name] = [str(var_value)]  # Default to string

            except ValueError as e:
                print(e)
                if idle == 0: self.cmd_exit()
                return

            if self.cmdhandlingdebug:
                print(f"[DEBUG] Registered variable '{var_name}' = {self.variables[var_name][0]} (Type: {var_type})")

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
                if idle == 0: self.cmd_exit()

            except Exception as e:
                print(f"[CRITICAL ERROR] Failed to delete file. Error: {e}")
                self.cmd_exit()
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
                print(f"[CRITICAL ERROR] Failed to create directory. Error: {e}")
                self.cmd_exit()
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
                if idle == 0: self.cmd_exit()

            except OSError:
                print(f"ErrID61: Directory '{directory_name}' is not empty.")
                if idle == 0: self.cmd_exit()

            except Exception as e:
                print(f"[CRITICAL ERROR] Failed to delete directory. Error: {e}")
                self.cmd_exit()
        def cmd_search_file(self, args):
            """
            Searches for a keyword or pattern in a file.
            Syntax: search_file filename "keyword"
            """
            try:
                parts = args.split(' ', 1)
                if len(parts) < 2:
                    print("ErrID63: Missing filename or keyword for search_file command.")
                    if idle == 0: self.cmd_exit()

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
                if idle == 0: self.cmd_exit()

            except Exception as e:
                print(f"[CRITICAL ERROR] Failed to search file. Error: {e}")
                self.cmd_exit()
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
                    if idle == 0: self.cmd_exit()

            except Exception as e:
                print(f"[CRITICAL ERROR] Failed to calculate square root. Error: {e}")
                self.cmd_exit()
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
                    if idle == 0: self.cmd_exit()

                    return

                var_name, value = parts[0], parts[1]
                sys1.environ[var_name] = value
                print(f"Environment variable '{var_name}' set to '{value}'.")
            except Exception as e:
                print(f"[CRITICAL ERROR] Failed to set environment variable. Error: {e}")
                self.cmd_exit()
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
                    print(f"{error_message}")
                    if idle == 0: self.cmd_exit()

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
                    print(f"{error_message}")
                    self.cmd_exit("Exiting due to error in inp command.")

        def cmd_fetch(self, args):
            if len(args) < 1:
                print("ErrID3: Incorrect number of arguments for fetch command")
                if idle == 0: self.cmd_exit()
                return
            url = args[0]
            if url in self.variables:           
                self.fetch_data_from_api(self.variables[url])
            else:
                self.fetch_data_from_api(args)

        def cmd_exit(self, args=None):
            if args:
                print(f"[Exit]: {args}")
            if self.cmdhandlingdebug:    
                print("[DEBUG] Exiting")
            exit()  # Safely exits the script, or you can use other termination logic


        def log_debug(self, message):
            """Unified debug logger."""
            if self.debug:
                print(f"[DEBUG] {message}")
                self.debuglog.append(f"[DEBUG] {message}")
        def cmd_exit_ce(self, error):
            """Exit the program with an error message."""
            print(f"Exiting, Error Code:{error}")
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
                if idle == 0: self.cmd_exit()
        """
        """
        //Deprecated Version
        def cmd_while(self, condition):
            Implements the while-loop functionality in the interpreter.
            Args:
                condition (str): The loop condition to evaluate.
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
                if idle == 0: self.cmd_exit()
        """
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
                    print("ErrID3: Incorrect number of arguments for 'def' command. Expected syntax: def function_name")
                    if idle == 0: self.cmd_exit()


                function_name = tokens[0]

                # Check if a function with the same name already exists
                if function_name in self.functions:
                    print(f"ErrID8: Function '{function_name}' already defined.")
                    if idle == 0: self.cmd_exit()


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
                if idle == 0: self.cmd_exit()

            self.log_debug(f"Calling function '{function_name}'")
            for command in self.functions[function_name]:
                self.handle_command(command)

        def cmd_switch(self, args):
            """Switch-case implementation."""
            if not args:
                print("ErrID3: Incorrect number of arguments for switch command")
                if idle == 0: self.cmd_exit()

            switch_var = args[0]
            if switch_var not in self.variables:
                print(f"ErrID31: Variable '{switch_var}' not defined.")
                if idle == 0: self.cmd_exit()

            self.control_stack.append({"type": "switch", "variable": self.variables[switch_var][0], "executed": False})

        def cmd_case(self, args):
            """Case block in a switch."""
            if not self.control_stack or self.control_stack[-1]["type"] != "switch":
                print("ErrID32: 'case' command outside of 'switch' block.")
                if idle == 0: self.cmd_exit()

            case_value = args[0]
            current_switch = self.control_stack[-1]
            if not current_switch["executed"] and current_switch["variable"] == case_value:
                current_switch["executed"] = True
                self.handle_command(" ".join(args[1:]))

        def cmd_default(self, args):
            """Default block in a switch."""
            if not self.control_stack or self.control_stack[-1]["type"] != "switch":
                print("ErrID33: 'default' command outside of 'switch' block.")
                if idle == 0: self.cmd_exit()

            self.control_stack[-1]["default"] = args

        def cmd_inc(self, args):
            """Increment a variable."""
            if len(args) != 1:
                print("ErrID3: Incorrect number of arguments for inc command")
                if idle == 0: self.cmd_exit()

            var_name = args[0]
            if var_name in self.variables and self.variables[var_name][1] == "int":
                self.variables[var_name] = (self.variables[var_name][0] + 1, "int")
            else:
                print(f"ErrID34: Variable '{var_name}' not defined or not an integer.")
                if idle == 0: self.cmd_exit()

        def cmd_dec(self, args):
            """Decrement a variable."""
            if len(args) != 1:
                print("ErrID3: Incorrect number of arguments for dec command")
                if idle == 0: self.cmd_exit()

            var_name = args[0]
            if var_name in self.variables and self.variables[var_name][1] == "int":
                self.variables[var_name] = (self.variables[var_name][0] - 1, "int")
            else:
                print(f"ErrID34: Variable '{var_name}' not defined or not an integer.")
                if idle == 0: self.cmd_exit()
        """
        #Removed In Eclipse.
        def cmd_repeat(self, args):
            if len(args) != 2:
                print("ErrID3: Incorrect number of arguments for repeat command")
                if idle == 0: self.cmd_exit()

            try:
                loop_count = int(args[0])
                command_to_repeat = args[1]
                for _ in range(loop_count):
                    self.handle_command(command_to_repeat)
            except ValueError:
                print("ErrID3: Loop count must be an integer.")
                if idle == 0: self.cmd_exit()
        """
        def cmd_wait(self, args):
            """Wait for a specified number of seconds."""


            try:
                duration = int(args)
                self.log_debug(f"Waiting for {duration} seconds...")
                time.sleep(duration)
            except ValueError:
                print("ErrID3: Duration must be an integer.")
                if idle == 0: self.cmd_exit()

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

        def perform_arithmetic_operation(self, args, operation):
            """
            Handles arithmetic operations dynamically with support for 'eq=True' flag.
            If 'eq=True' is present, the second operand is first evaluated as an equation.
            Supported operations: add, sub, mul, div, mod
            """
            try:
                # Parse arguments using shlex to handle spaces correctly
                args = shlex.split(args)

                # Ensure at least 3 arguments are present
                if len(args) < 3:
                    raise ValueError(f"Incorrect number of arguments. Expected at least 3, got {len(args)}. Syntax: <var_name> <operand1> <operand2> [eq=True]")
                # Check for 'eq=True' flag
                eq_mode = "eq=True" in args
                if eq_mode:
                    args.remove("eq=True")  # Remove flag from arguments

                if len(args) != 3:
                    raise ValueError(f"Incorrect number of arguments after processing flags. Expected 3, got {len(args)}.")
                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Parsed arguments: {args}")  

                var_name, op1, op2 = args  # 🚀 Safely unpack after validation
                # Retrieve and validate operand values
                try:
                    operand1 = self.get_variable_value(op1)
                except KeyError:
                    raise KeyError(f"Variable '{op1}' not defined.")
                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Before eq processing: var_name={var_name}, op1={op1}, op2={op2}, eq_mode={eq_mode}")

                if eq_mode:
                    # Evaluate op2 as an equation before using it
                    try:
                        for var in re.findall(r'[a-zA-Z_]\w*', op2):  # Find variable names in equation
                            if var in self.variables:
                                op2 = op2.replace(var, str(self.variables[var][0]))
                        operand2 = eval(op2)  # Evaluate equation
                    except Exception as e:
                        raise ValueError(f"Failed to evaluate equation '{op2}': {e}")
                else:
                    try:
                        operand2 = self.get_variable_value(op2)
                    except KeyError:
                        raise KeyError(f"Variable '{op2}' not defined.")

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
            if var_name in self.variables:
                return self.variables[var_name][0]  # 🚀 Return the stored value
            return var_name  # 🚀 Return the variable name itself if undefined

        def cmd_open_terminal(self, args):
            install_package('pygetwindow', "gw") #Import pygetwindow as "gw" lol.

            from colorama import Fore, Style #for custom font color in terminal

            # Fix incorrect spelling of split()
            if "," not in args:
                args = args.split()
            else:
                args = args.split(", ")

            if len(args) < 5:
                print("ErrID100: Incorrect usage. Expected format: open_terminal command x y width height [load] [ColorName]")
                if idle == 0: self.cmd_exit()

                return

            # Check if 'load' is given BEFORE checking colors
            load_mode = False
            if "load" in args:
                args.remove("load")  # Remove it from the list
                load_mode = True

            # Check if a valid color name is given (after "load" is handled)
            color_name = None
            if len(args) > 5:  # Now, check if a 6th argument is present
                last_arg = args[-1]
                valid_colors = {
                    "Black": "0", "Blue": "1", "Green": "2", "Aqua": "3",
                    "Red": "4", "Purple": "5", "Yellow": "6", "White": "7",
                    "Gray": "8", "LBlue": "9", "LGreen": "A", "LAqua": "B",
                    "LRed": "C", "LPurple": "D", "LYellow": "E", "BWhite": "F"
                }

                if last_arg in valid_colors:
                    color_name = valid_colors[last_arg]
                    args.pop()  # Remove color from argument list

            # Extract remaining arguments
            if len(args) < 5:
                print("ErrID100: Incorrect usage. Expected format: open_terminal command x y width height [load] [ColorName]")
                if idle == 0: self.cmd_exit()

                return

            command, pos_x, pos_y, width, height = args

            try:
                pos_x, pos_y, width, height = map(int, [pos_x, pos_y, width, height])
            except ValueError:
                print("ErrID101: Position and size parameters must be integers.")
                if idle == 0: self.cmd_exit()

                return

            terminal_title = "CMD"

            # If 'load' is given, modify the command to load the first argument in the interpreter
            if load_mode:
                command = f'python.exe "eclipse1.py" -f "{command}"'

            # Set default color to White if none provided
            cmd_color = color_name if color_name else "7"

            # Default CMD start command with color
            cmd = f'start "CMD" cmd /k "title {terminal_title} & chcp 65001 & color {cmd_color} & {command}"'

            # Open the terminal
            subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
            time.sleep(1.0)

            windows = [win for win in gw.getWindowsWithTitle(terminal_title)]

            if windows:
                terminal_window = windows[0]
                terminal_window.moveTo(pos_x, pos_y)
                terminal_window.resizeTo(width, height)
                print(f"Terminal opened at ({pos_x}, {pos_y}) with size {width}x{height}.")
            else:
                print("Warning: Could not find the Command Prompt window.")
        def cmd_reinit(self): #to bring back the interpreter to its initial state. 
            self.cmd_flush()

            import argparse
            import time
            import re
            import os as sys1
            import shlex 
            import json
            import difflib
            import subprocess
            import sys
            import importlib
            
        def cmd_goto(self, line_number):
            """
            Moves execution to a specific line in the script file.(Script Execution Mode Only)
            """
            if idle==0:
                try:
                    target_line = int(line_number)
                    if target_line < 1 or target_line > len(self.script_lines):
                        print(f"ErrId75: Line {target_line} is out of range.")
                        if idle == 0: self.cmd_exit()

                        return
                    self.current_line = target_line - 1  # Adjusted for 0-based index
                    if self.cmdhandlingdebug:
                        print(f"[DEBUG] Jumping to line {target_line}.")

                except ValueError:
                    print(f"ErrId76: Invalid line number '{line_number}'. Must be an integer.")
                    if idle == 0: self.cmd_exit()

                except Exception as e:
                    print(f"[CRITICAL ERROR]: '{e}'")    
            else:
                print(f"[DEBUG] GOTO command is not available in REPL/IDLE mode.")
    def main():
        try:
            parser = argparse.ArgumentParser(description="X3 Interpreter")
            parser.add_argument('-f', '--file', type=str, help='File to execute as a script')
            parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
            args = parser.parse_args()
            
            #uses debug mode if nessecary
            interpreter = Interpreter(debug=args.debug)

            # If a file is provided, read commands from the file
            if args.file:
                try:
                    with open(args.file, 'r', encoding='utf-8', errors='replace') as script_file:
                        interpreter.script_lines = script_file.readlines()  # Store all lines in memory
                        interpreter.current_line = 0

                        while interpreter.current_line < len(interpreter.script_lines):
                            line = interpreter.script_lines[interpreter.current_line].strip()
                            interpreter.handle_command(line)
                            interpreter.current_line += 1  # Move to the next line unless `goto` changes it

                except Exception as exc:
                    print(f"[CRITICAL ERROR] Could not load {args.file} due to reason:{exc}")            
            else:
                idle=1 #for repl and ide mode.
                while True:
                    try:
                        user_input = input(">>")
                        interpreter.handle_command(user_input.strip())
                    except (KeyboardInterrupt, EOFError):
                        print("\nExiting.")
                        break
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")

    if __name__ == "__main__":
        main()
except (KeyboardInterrupt, EOFError):
    print("\nExiting.")

except Exception as e:
    print(f"[CRITICAL ERROR]: {e},\nTerminating script.")
#Official 1k lines of code!!-November/24
#Development Phase start of Eclispe-March/25
#Official release of Eclispe prototype 0.6.