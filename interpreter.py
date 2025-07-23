#this software is licenced under CC4.0 BY-SA-NC, for more information check: https://creativecommons.org/licenses/by-nc-sa/4.0
#MintEclipse 0.2
from difflib import SequenceMatcher
import datetime, platform, uuid, getpass, socket, traceback, builtins, argparse, time, re, os, shlex, json, difflib, subprocess, importlib, random, math, struct
#import cProfile
REPL=0 #on default script mode.
version=3.92 #version (For IDE and more)
def install_package(package, alias=None): #package installation using subprocess.
    import sys

    try:
        # Try importing the package
        module = importlib.import_module(package)
        if REPL==1:
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
install_package("psutil") #import psutil for memory usage and other system info.
install_package("requests") #import requests for HTTP requests.
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
        def __init__(self, debug=False): 
            self.local_variables = {}
            self.REPL=REPL
            self.current_line=0
            self.variables = {} #variable dictionary
            self.functions = {} #function dictionary, kinda messy
            self.current_function_name = None
            self.in_function_definition = False #flag to indicate if the code is currently in a function definition
            self.local = False #local variable flag, used to indicate if a var is being declared locally or globally
            self.control_stack = [] #that if else and stuff, for basic control flow monitoring
            self.debug = False #only used as a placeholder, replaced by the new BETTER debug system
            self.debuglog = [] #i have no idea why i made this
            self.output = None #output for functions like fetch, i will think of improving this.
            self.log_messages = [] #old log messages record, still works but deprecated
            self.execution_state = {} #thought of removing this but it is still used in some control flow magic so ye.
            self.return_flag = False
            self.return_value = None
            #Debug Init---
            self.ctrflwdebug = False
            self.prtdebug = False
            self.mathdebug = False
            self.filedebug = False
            self.clramadebug = False
            self.cmdhandlingdebug = False
            self.reqdebug=False
            self.conddebug=False
            self.vardebug=False
            #---
            #Rules Init--
            self.fastmathrule=False #NEVER USE FASTMATH ON DEFAULT, ONLY CHANGE THIS IF YOU KNOW WHAT YOU'RE DOING.
            self.semo=False #Script Execution Mode Only, this is used to prevent REPL from executing commands.
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
                'fastmath': self.cmd_fastmath,
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
                'return': self.cmd_return,
                'inc': self.cmd_inc,
                'dec': self.cmd_dec,
                'wait': self.cmd_wait,
                'log': self.cmd_log,
                'fncend': self.cmd_fncend,
                'dev.debug': self.dev,
                'load': self.load,
                'flush': self.flush,
                'reinit': self.cmd_reinit, 
                '--info': self.info,
                'setclientrule': self.setclientrule,
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
            self.additional_parameters = {
                "##random": lambda: random.random(),
                "##randint": lambda: random.randint(0, 100),
                "##timeseconds": lambda: time.time(),
                "##timestamp": lambda: int(time.time()),
                "##date": lambda: datetime.datetime.now().strftime("%Y-%m-%d"),
                "##time": lambda: datetime.datetime.now().strftime("%H:%M:%S"),
                "##datetime": lambda: datetime.datetime.now(),
                "##datetime:iso": lambda: datetime.datetime.now().isoformat(),
                "##datetime:utc": lambda: datetime.datetime.now(datetime.timezone.utc).isoformat(),
                
                "##REPL": lambda: self.REPL,  # Current interpreter state
                "##uuid": lambda: str(uuid.uuid4()),
                "##uuid:hex": lambda: uuid.uuid4().hex,
                "##user": lambda: getpass.getuser(),
                "##hostname": lambda: socket.gethostname(),
                "##platform": lambda: platform.system(),
                "##osversion": lambda: platform.version(),
                "##cwd": lambda: os.getcwd(),
                "##randbool": lambda: random.choice([True, False]),
                "##msec": lambda: int(time.time() * 1000),
                "##env": lambda key="": os.environ.get(key, "") if key else dict(os.environ),  # Use like `##env:PATH`
                "##upper": lambda txt="": txt.upper(),
                "##lower": lambda txt="": txt.lower(),
                "##reverse": lambda txt="": txt[::-1],
                "##capitalize": lambda txt="": txt.capitalize(),
                "##pingreport": lambda host="8.8.8.8": os.system(f"ping -n 1 {host}" if os.name == "nt" else f"ping -c 1 {host}") == 0,
                "##ping": lambda host="8.8.8.8": (
                    lambda output: (
                        re.search(r'time[=<]?\s*([\d.]+)\s*ms', output).group(1)
                        if re.search(r'time[=<]?\s*([\d.]+)\s*ms', output) else "unreachable"
                    )
                )(
                    subprocess.getoutput(
                        f"ping -n 1 {host}" if platform.system().lower() == "windows"
                        else f"ping -c 1 {host}"
                    )
                ),
                "##fetch": lambda url="": requests.get(url).text if 'requests' in globals() else "[Requests module not available]",
                "##fetch:json": lambda url="": requests.get(url).json() if 'requests' in globals() else "[Requests module not available]",
                "##fetch:status": lambda url="": requests.get(url).status_code if 'requests' in globals() else "[Requests module not available]",
                "##fetch:headers": lambda url="": requests.get(url).headers if 'requests' in globals() else "[Requests module not available]",
                "##fetch:content": lambda url="": requests.get(url).content if 'requests' in globals() else "[Requests module not available]",
                "##fetch:html": lambda url="": requests.get(url).text if 'requests' in globals() else "[Requests module not available]",
                "##fetch:xml": lambda url="": requests.get(url).text if 'requests' in globals() else "[Requests module not available]",
                
                "##rgb": lambda hex="#000000": tuple(int(hex.strip("#")[i:i+2], 16) for i in (0, 2, 4)),

                "##readfile": lambda path="": open(path, "r").read() if os.path.exists(path) else "[File not found]",

                "##interpreter:vars": lambda: list(self.variables.keys()),
                "##interpreter:funcs": lambda: list(getattr(self, "functions", {}).keys()),
                "##interpreter:memory": lambda: f"{round(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024, 2)} MB" if 'psutil' in globals() else "[psutil module not available]",
                "##interpreter:platform": lambda: platform.platform(),
            }

        def setclientrule(self, args):
            if args=="fastmath":
                self.fastmathrule=True if self.fastmathrule == False else False
                print(f"[DEBUG] Fastmath rule set to {self.fastmathrule}.")
            if args=="SEMO":
                # Script Execution Mode Only
                self.semo = True if self.semo == False else False
                print(f"[DEBUG] SEMO rule set to {self.semo}.")

            if args=="reset":
                # Reset all rules to default
                self.fastmathrule = False
                self.semo = False
                print("[DEBUG] All client rules reset to default.")
        def info(self):
            print(f'Running on version:{version},MintEclipse 0.2')
            print(f'Developed by XFydro 08.2024-Present, under CC4.0 BY-SA-NC license.')

        def flush(self):
            del self.variables
            del self.functions
            del self.current_function_name
            del self.in_function_definition
            del self.control_stack
            del self.debug
            del self.debuglog
            del self.output
            del self.log_messages
            del self.execution_state
            #Reinit the interpreter
            self.REPL=REPL
            self.variables = {} #variable dictionary
            self.functions = {} #function dictionary, kinda messy
            self.current_function_name = None
            self.in_function_definition = False #flag to indicate if the code is currently in a function definition
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
            self.vardebug=False
            #---
            #Rules Init--
            self.fastmathrule=False #NEVER USE FASTMATH ON DEFAULT, ONLY CHANGE THIS IF YOU KNOW WHAT YOU'RE DOING.
            self.semo=False #Script Execution Mode Only, this is used to prevent REPL from executing commands.
            #---
        def comment_strip(self, s):
            return s.split('\\')[0]

        def load(self, filename: str) -> None:
            """
            Securely loads and executes commands from a given file using the interpreter.
            Provides layered debug output and tracks line-by-line success/failure statistics >:3
            muhahahahaahahahahaha
            """

            success_count = 0
            fail_count = 0

            try:
                # Validate filename type
                if not isinstance(filename, str):
                    raise TypeError(f"Expected filename as str, got {type(filename).__name__}.")

                # Check file existence and permissions
                if not os.path.isfile(filename):
                    raise FileNotFoundError(f"File '{filename}' does not exist.")
                if not os.access(filename, os.R_OK):
                    raise PermissionError(f"No read permission for file '{filename}'.")

                # Try to create the interpreter instance
                try:
                    interpreter = Interpreter()
                except Exception as interp_init_err:
                    raise RuntimeError(f"Interpreter init failed: {interp_init_err}")

                if self.filedebug:
                    print(f"[DEBUG-{self.filedebug}] Opening file: {filename}")

                # Read and process commands
                with open(filename, 'r', encoding='utf-8', errors='replace') as file:
                    for lineno, line in enumerate(file, 1):
                        command = line.strip()
                        if not command or command.startswith("#"):
                            continue

                        try:
                            interpreter.handle_command(command)
                            success_count += 1

                            if self.filedebug == 2:
                                print(f"[Line {lineno}]  Executed: {command}")

                        except Exception as cmd_err:
                            fail_count += 1

                            if self.filedebug == 1:
                                print(f"[Line {lineno}]  Failed.")
                            elif self.filedebug >= 2:
                                print(f"[Line {lineno}]  Command: '{command}'\n   └─ Reason: {cmd_err}")
                                if self.filedebug >= 3:
                                    print("   └─ Traceback:")
                                    traceback.print_exc()
                            continue

            except (FileNotFoundError, PermissionError, TypeError, RuntimeError) as critical:
                if self.filedebug:
                    print(f"[LOAD-CRITICAL]  {critical}")
                if self.REPL == 0:
                    self.cmd_exit()

            except Exception as unknown:
                if self.filedebug:
                    print(f"[LOAD-UNKNOWN]  Unexpected error:\n{unknown}")
                    if self.filedebug >= 3:
                        traceback.print_exc()
                if self.REPL == 0:
                    self.cmd_exit()

            finally:
                if self.filedebug:
                    print(f"[DEBUG-{self.filedebug}] Load complete.")
                    print(f" ├─ Successes: {success_count}")
                    print(f" └─ Failures: {fail_count}")

        def log(self, message):
            if self.debug:
                print(f"[DEBUG]: {message}")
                self.debuglog.append(f"[DEBUG]: {message}")

        def cmd_clear(self, args):
            if args!="legacy":  
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                print("\n" * 100) #for terminals that dont support cls.

        def cmd_if(self, condition):
            """
            Evaluate an IF condition and push it to the control stack.
            """
            try:
                condition = self.replace_additional_parameters(condition)  # Replace any additional parameters like ##random, ##REPL, etc :3
                result = self.eval_condition(condition)  # Pass the full condition as a single string
            except ValueError as e:
                print(f"--ErrID77: Invalid IF condition '{condition}'. Details: {e}")
                if self.REPL == 0: self.cmd_exit()

            # Push IF block to control stack (remains until `end`)
            self.control_stack.append({"type": "if", "executed": result, "has_else": False})
            if self.ctrflwdebug:
                print(f"[DEBUG] IF condition '{condition}' evaluated to {result}, pushed to stack.")

            if not result:
                if self.ctrflwdebug:
                    print("[DEBUG] Skipping subsequent commands inside this IF block.")
        def evaluate_math_expression(self, expression):
            # Replace variables in the expression
            expression = self.replace_variables(expression)
            try:
                return eval(expression, {"__builtins__": {}}, {})
            except Exception as e:
                print(f"[MATH ERROR] {e}")
                return "<MATH_ERROR>"

        def cmd_else(self):
            """
            Execute an ELSE block only if the preceding IF block was false.
            """
            if not self.control_stack:
                print("--ErrID78: ELSE without a matching IF.")
                if self.REPL == 0:
                    self.cmd_exit()
                return
            last_if = self.control_stack[-1]
            if last_if["type"] != "if":
                print("--ErrID78: ELSE without a matching IF.")
                if self.REPL == 0:
                    self.cmd_exit()
                return
            if last_if.get("has_else", False):
                print("--ErrID79: Multiple ELSE statements for the same IF.")
                if self.REPL == 0:
                    self.cmd_exit()
                return
            last_if["has_else"] = True
            last_if["executed"] = not last_if["executed"]
            if self.ctrflwdebug:
                if last_if["executed"]:
                    print("[DEBUG] ELSE block will execute.")
                else:
                    print("[DEBUG] Skipping ELSE block because IF condition was true.")
                
        def cmd_while(self, condition):
            """
            Implements a while-loop functionality with proper nested execution.
            Skips pushing a new while-loop if the last one is on the same line.
            """
            # Check if the last control block is a while on the same line
            if (self.control_stack and 
                self.control_stack[-1]["type"] == "while" and 
                self.control_stack[-1]["start_line"] == self.current_line):
                if self.ctrflwdebug:
                    print(f"[DEBUG] Skipping duplicate WHILE on line {self.current_line}")
                return  # Exit without pushing a new while

            # Respect the current execution state (inside IF blocks, etc.)
            if not self.should_execute():
                executed = False
            else:
                try:
                    executed = self.eval_condition(condition)
                except ValueError as e:
                    print(f"--ErrID90: Invalid WHILE condition '{condition}'. Details: {e}")
                    if self.REPL == 0:
                        self.cmd_exit()
                    return

            self.control_stack.append({
                "type": "while",
                "condition": condition,
                "executed": executed,
                "start_line": self.current_line
            })

            if self.ctrflwdebug:
                print(f"[DEBUG] WHILE condition '{condition}' evaluated to {executed}, pushed to stack.")

        def cmd_end(self):
            """
            Handles 'end' for 'if', 'else', and 'while' blocks.
            For 'while', it only loops if it was executed and the condition is still true.
            """
            if not self.control_stack:
                print("--ErrID91: 'end' without matching control block.")
                if self.REPL == 0:
                    self.cmd_exit()
                return

            block = self.control_stack.pop()
            debug = self.ctrflwdebug
            block_type = block.get("type")

            if debug:
                print(f"[DEBUG] END: Popped block: {block}")

            if block_type == "while":
                # Only evaluate loop again if it was actually active
                if block["executed"]:
                    try:
                        condition_still_true = self.eval_condition(block["condition"])
                    except Exception as e:
                        print(f"--ErrID92: WHILE condition failed at END. Details: {e}")
                        if self.REPL == 0:
                            self.cmd_exit()
                        return

                    if condition_still_true:
                        if debug:
                            print(f"[DEBUG] Repeating WHILE: jumping to line {block['start_line']}")
                        self.control_stack.append(block)
                        self.current_line = block["start_line"] - 1
                        return  # DONTT continue past this point
                    else:
                        if debug:
                            print(f"[DEBUG] Exiting WHILE loop")
                else:
                    if debug:
                        print(f"[DEBUG] Skipping WHILE block recheck (never executed)")

            elif block_type in ("if", "else"):
                if debug:
                    print(f"[DEBUG] Closing {block_type.upper()} block")

            else:
                print(f"--ErrID93: Unknown control block type '{block_type}' during END.")
                if self.REPL == 0:
                    self.cmd_exit()
                return

            self.execution_state = (
                self.control_stack[-1]["executed"]
                if self.control_stack else True
            )


        def find_while_start(self, condition):
            """Finds the start of the while loop in the script."""
            '''i feel something is wrong with this but i dont know what'''
            for i in range(self.current_line, -1, -1):
                line = self.lines[i].strip()
                if line.startswith("while ") and condition in line:
                    return i + 1  # Return line after while statement
            return self.current_line
        def should_execute(self):
            """
            Determine if the current block should execute based on active IF conditions.
            """
            
            if not self.control_stack:
                return True
            for block in reversed(self.control_stack):
                if ((block["type"] == "if" and not block["executed"]) or 
                    (block["type"] == "else" and not block["executed"])):
                    return False

            return True 

        def replace_variables(self, text):
            # Match and replace ##function:(args)
            text = self.replace_additional_parameters(text)

            def func_replacer(match):
                full_expr = match.group(1)
                if ':' in full_expr and full_expr.endswith(')'):
                    func_name, arg_str = full_expr.split(':', 1)
                    arg_str = arg_str.strip("()")

                    try:
                        prev_output = self.output
                        processed_args = self.replace_additional_parameters(args)
                        result = self.cmd_call(f"{func_name} {processed_args}")

                        self.output = prev_output  

                        return str(result) if result is not None else ""
                    except Exception as e:
                        return f"<ERROR:{e}>"
                return f"<INVALID:{full_expr}>"

            def inline_func_replacer(match):
                raw = match.group(1)
                func_name, args = raw.split(":", 1)
                args = args.strip("()")  # REMOVE THE PARENTHESES FROM ARGUMENTS AAAAAAAAA
                result = self.cmd_call(f"{func_name} {args}")
                return str(result) if result is not None else ""

            text = re.sub(r"##([\w]+:\([^\)]*\))", inline_func_replacer, text)

            def replacer(match):
                var_name = match.group(1)
                if var_name in self.local_variables:
                    return str(self.local_variables[var_name][0])
                elif var_name in self.variables:
                    return str(self.variables[var_name][0])
                else:
                    return f"<UNDEFINED:{var_name}>"
            return re.sub(r"\$([a-zA-Z_][a-zA-Z0-9_]*)", replacer, text)

        def eval_condition(self, condition_str):
            """
            Evaluate a custom IF condition string. Supports:
            - AND (&) / OR (|) with correct precedence (AND before OR)
            - Negation with !
            - Comparisons: ==, !=, >, <, >=, <=
            - Advanced: startswith, contains, ==ic (case-insensitive), |+| (fuzzy similarity)
            - Variables from self.variables (as lists) and literals (strings/numbers)
            - Parentheses for grouping"""

            if self.conddebug:
                print(f"[DEBUG] Evaluating condition: {condition_str}")

            condition_str = self.replace_variables(condition_str)

            def debug(msg):
                """Debug helper to print messages if conddebug is enabled.
                   This avoids cluttering output when not debugging conditions,
                   Print debug messages only if conddebug is enabled"""

                if self.conddebug:
                    print(f"[DEBUG] {msg}")

            def get_value(token):
                # Resolve a token to its actual value.
                token = token.strip()
                # quoted string -> strip quotes
                if (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'")):
                    val = token[1:-1]
                    debug(f"Resolved literal string {token} -> {val!r}")
                    return val
                if token in self.variables:
                    lst = self.variables[token]
                    if not lst:
                        debug(f"Warning: variable '{token}' is empty")
                        return None
                    val = lst[0]
                    debug(f"Resolved variable '{token}' -> {val!r}")
                    return val
                # Try numeric conversion
                try:
                    if '.' in token:
                        val = float(token)
                    else:
                        val = int(token)
                    debug(f"Parsed numeric literal {token} -> {val!r}")
                    return val
                except ValueError:
                    # Not a number, return as string
                    debug(f"Interpreting token {token} as string {token!r}")
                    return token

            def compare_values(left, op, right):
                # Perform comparison, with type-safety
                debug(f"Comparing {left!r} {op} {right!r}")
                # Handle None from missing var as False condition
                if left is None or right is None:
                    debug("One operand is None (undefined); comparison -> False")
                    return False
                # Numeric vs string: attempt to coerce
                if isinstance(left, (int, float)) and isinstance(right, str):
                    try:
                        right = float(right) if '.' in right else int(right)
                        debug(f"Coerced right operand to number: {right!r}")
                    except ValueError:
                        debug("Type mismatch (number vs non-numeric string); comparison -> False")
                        return False
                if isinstance(right, (int, float)) and isinstance(left, str):
                    try:
                        left = float(left) if '.' in left else int(left)
                        debug(f"Coerced left operand to number: {left!r}")
                    except ValueError:
                        debug("Type mismatch (string vs non-numeric number); comparison -> False")
                        return False

                # Case-insensitive equal
                if op == "==ic":
                    if isinstance(left, str) and isinstance(right, str):
                        result = left.lower() == right.lower()
                        debug(f"Case-insensitive equal? -> {result}")
                        return result
                    else:
                        debug("==ic used on non-strings; comparison -> False")
                        return False

                # startswith/contains assume string left operand
                if op == "startswith":
                    if isinstance(left, str):
                        result = left.startswith(str(right))
                        debug(f"{left!r}.startswith({right!r}) -> {result}")
                        return result
                    else:
                        debug("startswith used on non-string; comparison -> False")
                        return False
                if op == "contains":
                    if isinstance(left, str):
                        result = str(right) in left
                        debug(f"{right!r} in {left!r} -> {result}")
                        return result
                    else:
                        debug("contains used on non-string; comparison -> False")
                        return False
                if op == "|+|":
                    if isinstance(left, str) and isinstance(right, str):
                        # Compute similarity percentage [0-100]
                        ratio = SequenceMatcher(None, left, right).ratio() * 100  # returns float [0,100]
                        debug(f"Similarity of {left!r} |+| {right!r} = {ratio:.1f}%")
                        # Interpret condition as True if similarity >= threshold?
                        # If right is numeric (threshold), we'd have to reframe.
                        # Here we return the ratio for caller to compare.
                        return ratio
                    else:
                        debug("|+| used on non-strings; comparison -> 0%")
                        return 0
                # Numeric and default comparisons
                try:
                    if op == "==":
                        return left == right
                    elif op == "!=":
                        return left != right
                    elif op == ">":
                        return left > right
                    elif op == "<":
                        return left < right
                    elif op == ">=":
                        return left >= right
                    elif op == "<=":
                        return left <= right
                except Exception as e:
                    debug(f"Error during comparison: {e}")
                    return False

                debug(f"Unknown operator {op}; comparison -> False")
                return False

            def eval_simple(expr):
                """Evaluate a simple expression without top-level & or |."""
                expr = expr.strip()
                # Parentheses
                if expr.startswith("(") and expr.endswith(")"):
                    # Ensure matching parentheses
                    paren = 0
                    for idx, ch in enumerate(expr):
                        if ch == "(":
                            paren += 1
                        elif ch == ")":
                            paren -= 1
                            if paren == 0 and idx < len(expr)-1:
                                break
                    else:
                        # Fully parenthesized
                        debug(f"Evaluating parenthesized expr {expr}")
                        return self.eval_condition(expr[1:-1])

                # Split by whitespace to find tokens and operator
                # We check multi-char ops first
                ops = ["==ic", "|+|", ">=", "<=", "!=", "==", ">", "<", "startswith", "contains"]
                for op in ops:
                    parts = [p.strip() for p in expr.split(op)]
                    if len(parts) == 2:
                        left_val = get_value(parts[0])
                        right_val = get_value(parts[1])
                        result = compare_values(left_val, op, right_val)
                        debug(f"Result of {parts[0]} {op} {parts[1]} -> {result}")
                        return result

                # If no operator, interpret as boolean of the value
                val = get_value(expr)
                truth = bool(val)
                debug(f"Truth value of {expr!r} -> {truth}")
                return truth

            def eval_and(term):
                """Evaluate AND-separated factors."""
                factors = []
                buf = ""
                level = 0
                in_quotes = None
                for i, ch in enumerate(term):
                    if ch in "\"'":
                        if in_quotes is None:
                            in_quotes = ch
                        elif in_quotes == ch:
                            in_quotes = None
                    if ch == "(" and in_quotes is None:
                        level += 1
                    elif ch == ")" and in_quotes is None:
                        level -= 1
                    if ch == "&" and level == 0 and in_quotes is None:
                        factors.append(buf.strip())
                        buf = ""
                    else:
                        buf += ch
                factors.append(buf.strip())

                result = True
                for factor in factors:
                    if factor.startswith("!"):
                        debug(f"Applying negation to {factor[1:]}")
                        res = not eval_simple(factor[1:])
                    else:
                        res = eval_simple(factor)
                    result = result and bool(res)
                    debug(f"AND so far -> {result}")
                    if not result:
                        break  # short-circuit
                return result

            # Main OR-level split
            terms = []
            buf = ""
            level = 0
            in_quotes = None
            for i, ch in enumerate(condition_str):
                if ch in "\"'":
                    if in_quotes is None:
                        in_quotes = ch
                    elif in_quotes == ch:
                        in_quotes = None
                if ch == "(" and in_quotes is None:
                    level += 1
                elif ch == ")" and in_quotes is None:
                    level -= 1
                # Split on top-level |
                if ch == "|" and level == 0 and in_quotes is None:
                    terms.append(buf.strip())
                    buf = ""
                else:
                    buf += ch
            terms.append(buf.strip())

            final_result = False
            for term in terms:
                res = eval_and(term)
                debug(f"OR-term '{term}' -> {res}")
                final_result = final_result or res
                if final_result:
                    break  # short-circuit OR
            debug(f"Final result of '{condition_str}' -> {final_result}")
            return final_result
        def cmd_prt(self, raw_args):
            """
            Enhanced print command with styled, formatted, and interactive output.
            """
            if not raw_args:
                print("--ErrID37: No arguments provided for prt command.")
                if self.REPL == 0: self.cmd_exit()
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
                args = self.replace_variables(args)

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
                    border_char = settings["border"]
                    padding = 1  # space between text and border
                    content_line = f"{border_char}{' ' * padding}{args}{' ' * padding}{border_char}"
                    border_length = len(content_line)
                    
                    border_line = border_char * (border_length // len(border_char))
                    if len(border_line) < border_length:
                        border_line += border_char[:border_length - len(border_line)]  # fill the gap

                    args = f"{border_line}\n{content_line}\n{border_line}"

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
                args = self.replace_additional_parameters(args)

                # Handle output & animated printing with delay
                if settings["delay"]:
                    import sys
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
                print(f"--ErrID38: Value error in prt command. Details: {e}")
                if self.REPL == 0: self.cmd_exit()

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
                    print("--ErrID50: Missing filename or content for create_file command.")
                    if self.REPL == 0: self.cmd_exit()

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
                print("--ErrID52: Missing filename or variable name for read_file command.")
                if self.REPL == 0: self.cmd_exit()

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
                print(f"--ErrID53: File '{filename}' not found.")
                if self.REPL == 0: self.cmd_exit()

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
                    print("--ErrID55: Missing filename or content for append_file command.")
                    if self.REPL == 0: self.cmd_exit()

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
            install_package("requests")
            """Fetch data from a given API URL or from a variable in Var_Reg."""
            if not url:
                print("--ErrID11: No URL or variable provided.")
                self.output = None
                if self.REPL == 0: self.cmd_exit()

                return

            if url in self.variables:
                url = self.variables[url]

            if not isinstance(url, str) or not url.strip():
                print("--ErrID12: Invalid URL or variable key provided.")
                self.output = None
                if self.REPL == 0: self.cmd_exit()

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

        def store_variable(self, var_name, value, data_type, local=False):
            target = self.local_variables if local else self.variables
            if data_type == "list" and not isinstance(value, list):
                value = [value]
            if value != "output":
                target[var_name] = (value, data_type)
            else:
                target[var_name] = (self.output, data_type)

        def handle_command(self, command):
            """Processes commands, handles function definitions, and executes appropriately."""
            # Early return for empty lines or comments
            if self.REPL == 1 and self.semo == True and not(command=="setclientrule SEMO"):
                print("--ErrID72: Script Execution Mode Only (SEMO) is enabled. Cannot run commands.")
                self.cmd_exit()
            if not command or command.startswith(("//", "\\")):
                return

            if getattr(self, "in_function_definition", False):
                if command.strip().lower() == "fncend":
                    if self.cmdhandlingdebug:
                        print(f"[DEBUG] Ending function '{self.current_function_name}'")
                    self.command_mapping["fncend"]()
                    return
                else:
                    self.functions[self.current_function_name]["body"].append(command)
                    if self.cmdhandlingdebug:
                        print(f"[DEBUG] Added line to function '{self.current_function_name}': {command}")
                    return




            # Prepare command parts (special handling for 'prt' to preserve spaces)
            is_prt = command.startswith('prt ')
            if is_prt:
                parts = re.findall(r'\S+|\s+', command)
                cmd = 'prt'
                args = command[4:]  # Keep original spacing after 'prt'
            else:
                command = command.strip()
                parts = command.split()
                if not parts:  # Handle case where command was all whitespace
                    return
                cmd = parts[0]
                args = ' '.join(parts[1:]).strip()

            # Strip comments from arguments (except for prt which handles its own formatting)
            if not is_prt and "//" in args:
                args = self.comment_strip(args)

            # Check execution state
            if not self.should_execute():
                control_flow_commands = {"else", "end", "while", "if"}  # ← added while and if here
                if cmd in control_flow_commands:
                    if self.ctrflwdebug:
                        print(f"[DEBUG] Handling control command '{cmd}' even in inactive block")
                    if cmd in {"else", "end"}:
                        self.command_mapping[cmd]()
                    else:
                        self.command_mapping[cmd](args)
                else:
                    if self.cmdhandlingdebug:
                        print(f"[DEBUG] Skipping command '{command}' due to inactive block")
                return

            # Execute recognized commands
            if cmd in self.command_mapping:
                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Handling command: '{command}'")

                # No-arg commands
                no_arg_commands = {"else", "end", "dev.custom", "flush", "--info", "reinit", "fncend"}
                if cmd in no_arg_commands:
                    self.command_mapping[cmd]()
                else:
                    self.command_mapping[cmd](args)

                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Command '{cmd}' executed with args: '{args}'")
            else:
                print(f"--ErrID73: Unrecognized command: {command}")
                if self.REPL == 0:
        
                    self.cmd_exit()
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
            - dev variable     → Enables variable handling debugging
            - dev All          → Enables all debugging options
            - dev cmdhandling  → Enables Command handling debugging
            - dev None         → Disables all debugging options
            """
            
            #  Debugging options dictionary
            debug_options = {
                "controlflow": "ctrflwdebug",
                "print": "prtdebug",
                "math": "mathdebug",
                "file": "filedebug",
                "colorama": "clramadebug",
                "requests": "reqdebug",
                "cmdhandling": "cmdhandlingdebug",
                "condition": "conddebug",
                "variable": "vardebug",
            }

            if not raw_args.strip():
                print("[SELF-DEBUG] Please provide a debug option (e.g., 'dev controlflow').")
                return

            args = raw_args.lower().split()  # Convert input to lowercase for case-insensitive matching 

            if "all" in args or "none" in args:
                enable = "all" in args
                self.debug = enable
                for attr in debug_options.values():
                    setattr(self, attr, enable)
                print(f"[SELF-DEBUG] {'Enabled' if enable else 'Disabled'} all debugging options.")
                return

            enabled_any = False
            for dbg_option in args:
                if dbg_option in debug_options:
                    current = getattr(self, debug_options[dbg_option])
                    new_state = not current
                    setattr(self, debug_options[dbg_option], new_state)
                    print(f"[SELF-DEBUG] {'Enabled' if new_state else 'Disabled'} debugging for: {dbg_option}")
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
        #DEPRECATED IN MintEclipse
        def cmd_catch(self, args):
            if not self.control_stack or self.control_stack[-1]["type"] != "try":
                print("--ErrID35: 'catch' command outside of 'try' block")
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
                print("--ErrID36: No error to catch")
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
                print("--ErrID70: Incorrect syntax for str_len. Expected: str_len var_name result_var")
                if self.REPL == 0: self.cmd_exit()

                return

            var_name, result_var = parts  

            if var_name in self.variables:
                value = self.variables[var_name][0]
                if isinstance(value, str):
                    length = len(value)
                    self.store_variable(result_var, length, "int", local=self.local)
                    if self.cmdhandlingdebug:
                        print(f"[DEBUG]Length of '{var_name}' stored in '{result_var}': {length}")
                else:
                    print(f"--ErrID71: Variable '{var_name}' is not a string.")
                    if self.REPL == 0: self.cmd_exit()

                print(f"--ErrID72: Variable '{var_name}' not found.")
                if self.REPL == 0: self.cmd_exit()
        def similarity_percentage(self, str1, str2):
            similarity = difflib.SequenceMatcher(None, str(str1), str(str2)).ratio() * 100
            return float(similarity)
        def replace_additional_parameters(self, input_str):
            """
            Replaces ##key and ##key:(arg) additional parameters safely and completely.
            Handles:
                - ##key
                - ##key:with:colons
                - ##key:(argument)
                - ##key:with:colons:(argument)
            """

            if not isinstance(input_str, str):
                return input_str

            #  STEP 1: Bracket-style params like ##key:(value)
            bracket_pattern = re.compile(r"(##[a-zA-Z_]\w*(?::[a-zA-Z_]\w+)*):\(([^()]*)\)")
            matches = bracket_pattern.findall(input_str)

            for full_key, arg in matches:
                func = self.additional_parameters.get(full_key)
                arg_value = arg

                #  Resolve $variables
                if arg.startswith("$"):
                    varname = arg[1:]
                    arg_value = str(self.variables[varname][0]) if varname in self.variables else "<UNDEFINED>"

                #  Safe function call with arg
                try:
                    if callable(func):
                        result = str(func(arg_value)) if arg_value.strip() else str(func())
                        if result is None:
                            result = "None"
                    else:
                        #print(f"--ErrID38: Function '{full_key}' not defined.")
                        #if self.REPL == 0: self.cmd_exit()
                        #result="None"
                        continue
                        
                except Exception as e:
                    result = f"<CRITICAL ERROR: {e}>"

                input_str = input_str.replace(f"{full_key}:({arg})", result)

            #  STEP 2: Simple param replacements, including colons
            for key in sorted(self.additional_parameters, key=len, reverse=True):
                func = self.additional_parameters[key]

                #  Skip if key already used in bracket-style
                if re.search(rf"{re.escape(key)}:\(", input_str):
                    continue

                if key in input_str:
                    try:
                        result = str(func())
                        if result is None:
                            result = f"<CRITICAL ERROR: {key} returned None>"
                    except Exception as e:
                        result = f"<CRITICAL ERROR: {e}>"

                    input_str = input_str.replace(key, result)

            return input_str

        def cmd_reg(self, raw_args):
            """
            Registers a variable. Supports math expressions, string values, and variable substitution.
            Syntax:
                reg int varname 5
                reg int varname $x * 2
                reg int varname $x * $y
                reg int varname "$string"
            """
            raw_args = self.replace_additional_parameters(raw_args)
            parts = raw_args.strip().split()

            if len(parts) < 3:
                print("--ErrID80: Invalid variable registration format.")
                if self.REPL == 0: self.cmd_exit()
                return

            var_type = parts[0]   # int, float, str, etc.
            var_name = parts[1]   # Variable name
            var_value_raw = " ".join(parts[2:])  # The expression or literal value

            if self.vardebug:
                print(f"[DEBUG] Parsed Variable '{var_name}' of type '{var_type}' with value '{var_value_raw}'")

            try:
                # Variable substitution
                def var_replacer(match):
                    var = match.group(1)
                    val = None
                    if var in self.local_variables:
                        val = self.local_variables[var][0]
                    elif var in self.variables:
                        val = self.variables[var][0]
                    else:
                        raise ValueError(f"--ErrID38: Variable '${var}' not found.")

                    # For strings, add quotes
                    return f'"{val}"' if isinstance(val, str) and not val.replace(".", "", 1).isdigit() else str(val)

                var_value = re.sub(r'\$([a-zA-Z_]\w*)', var_replacer, var_value_raw)

                if self.mathdebug:
                    print(f"[DEBUG] After substitution: '{var_value}'")

                # Evaluate math expressions for numeric types
                if var_type in ["int", "float"]:
                    evaluated = eval(var_value, {"__builtins__": {}}, {})
                    if var_type == "int":
                        final_value = int(evaluated)
                    else:
                        final_value = float(evaluated)

                else:
                    # For strings, remove surrounding quotes if needed
                    if var_value.startswith('"') and var_value.endswith('"'):
                        final_value = var_value[1:-1]
                    else:
                        final_value = var_value  # raw value fallback

            except Exception as e:
                print(f"--ErrID84: Failed to evaluate variable '{var_name}': {e}")
                if self.REPL == 0: self.cmd_exit()
                return

            # Store the value
            if self.vardebug:
                print(f"[DEBUG] Storing variable '{var_name}' = {final_value} (Type: {type(final_value).__name__}) in {'local' if self.in_function_definition else 'global'} scope")

            self.store_variable(var_name, final_value, var_type, local=self.local)



            if self.vardebug:
                print(f"[DEBUG] Registered variable '{var_name}' = {final_value} (Type: {var_type})")

        def cmd_delete_file(self, args):
            """
            Deletes a specified file.
            Syntax: delete_file filename
            """
            filename = args.strip()
            try:
                os.remove(filename)
                print(f"File '{filename}' deleted successfully.")
            except FileNotFoundError:
                print(f"--ErrID57: File '{filename}' not found.")
                if self.REPL == 0: self.cmd_exit()

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
                os.makedirs(directory_name, exist_ok=True)
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
                os.rmdir(directory_name)
                print(f"Directory '{directory_name}' deleted successfully.")
            except FileNotFoundError:
                print(f"--ErrID60: Directory '{directory_name}' not found.")
                if self.REPL == 0: self.cmd_exit()

            except OSError:
                print(f"--ErrID61: Directory '{directory_name}' is not empty.")
                if self.REPL == 0: self.cmd_exit()

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
                    print("--ErrID63: Missing filename or keyword for search_file command.")
                    if self.REPL == 0: self.cmd_exit()

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
                print(f"--ErrID64: File '{filename}' not found.")
                if self.REPL == 0: self.cmd_exit()

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
                    print(f"--ErrID66: Variable '{var_name}' not defined or not numeric.")
                    if self.REPL == 0: self.cmd_exit()

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
                    print("--ErrID68: Missing variable name or value for set_env command.")
                    if self.REPL == 0: self.cmd_exit()

                    return

                var_name, value = parts[0], parts[1]
                os.environ[var_name] = value
                print(f"Environment variable '{var_name}' set to '{value}'.")
            except Exception as e:
                print(f"[CRITICAL ERROR] Failed to set environment variable. Error: {e}")
                self.cmd_exit()
        def cmd_inp(self, raw_args):
            """
            inp command: Takes user input and stores it as a variable.
            Usage: inp var_name "prompt" [default]
            
            Parameters:
                var_name: Name of the variable to store
                prompt: Text to display when asking for input (in quotes)
                default: (optional) Default value if user enters nothing
            
            Examples:
                inp username "Enter your username"
                inp timeout "Enter timeout in seconds" 30
                inp retry "Retry on failure? (true/false)" false
            """
            try:
                # Check if raw_args is empty or whitespace
                if not raw_args.strip():
                    raise ValueError("No arguments provided")
                    
                # Properly split arguments using shlex (handles quotes correctly)
                args = shlex.split(raw_args)
                
                # Validate argument count
                if len(args) < 2:
                    raise ValueError("Missing arguments. Expected at least variable name and prompt")
                    
                # Extract and validate arguments
                var_name = args[0]
                if not var_name.isidentifier():
                    raise ValueError(f"'{var_name}' is not a valid variable name")
                    
                prompt = args[1]
                default = args[2] if len(args) > 2 else None
                
                # Build and display the input prompt
                prompt_text = f"{prompt}"
                if default is not None:
                    prompt_text += f" [default: {default}]"
                prompt_text += ": "
                
                # Get user input
                user_input = input(prompt_text).strip()
                
                # Use default if input is empty and default exists
                if not user_input and default is not None:
                    user_input = default
                elif not user_input:
                    raise ValueError("No input provided and no default specified")
                    
                # Determine the type of input and convert if needed
                if user_input.lower() in ("true", "false"):
                    value = user_input.lower() == "true"
                    var_type = "bool"
                elif user_input.isdigit():
                    value = int(user_input)
                    var_type = "int"
                elif user_input.replace('.', '', 1).isdigit() and user_input.count('.') < 2:
                    value = float(user_input)
                    var_type = "float"
                else:
                    value = user_input
                    var_type = "str"
                
                # Store or update the variable
                self.store_variable(var_name, value, var_type, local=self.local)

                
            except Exception as e:
                error_message = f"Error in inp command: {str(e)}"
                if self.control_stack and self.control_stack[-1]["type"] == "try":
                    self.control_stack[-1]["error"] = error_message
                else:
                    print(f"{error_message}")
                    if self.REPL == 0: 
                        self.cmd_exit("Exiting due to error in inp command.")
        def cmd_fetch(self, args):
            if len(args) < 1:
                print("--ErrID3: Incorrect number of arguments for fetch command")
                if self.REPL == 0: self.cmd_exit()
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
        def cmd_return(self, args):
            """
            Stops execution of the current function and returns a value.
            Syntax:
                return value
            """
            if self.ctrflwdebug:
                print(f"[DEBUG] Return triggered with value: {args}")
            
            self.return_flag = True
            self.return_value = self.replace_variables(args)

        def cmd_def(self, args):
            """
            Starts the definition of a new function with optional parameters.
            Syntax:
                def function_name [param1 param2 param3...]
            Example:
                def greet name
                prt "Hello, $name!"
                fncend
            """
            try:
                tokens = args.strip().split()

                # 🧱 Validate function name
                if not tokens:
                    print("--ErrID3: Missing function name. Usage: def function_name [params]")
                    if self.REPL == 0: self.cmd_exit()
                    return

                function_name = tokens[0]
                if not function_name.isidentifier():
                    print(f"--ErrID4: Invalid function name '{function_name}'. Must be a valid identifier.")
                    if self.REPL == 0: self.cmd_exit()
                    return

                if function_name in self.functions:
                    print(f"--ErrID8: Function '{function_name}' is already defined.")
                    if self.REPL == 0: self.cmd_exit()
                    return

                # 🌟 Capture parameters
                params = tokens[1:]  # Remaining tokens are parameters
                if self.ctrflwdebug:
                    print(f"[DEBUG] Defining function '{function_name}' with params: {params}")

                self.functions[function_name] = {
                    "params": params,
                    "body": []
                }

                self.current_function_name = function_name
                self.in_function_definition = True

            except Exception as e:
                print(f"[CRITICAL ERROR] cmd_def: {e}")
                if self.REPL == 0: self.cmd_exit()
                
        def cmd_fncend(self):
            """
            Marks the end of a function definition block.
            """
            if not getattr(self, "in_function_definition", False):
                print("--ErrID9: 'fncend' used outside of a function definition.")
                if self.REPL == 0: self.cmd_exit()
                return

            if self.ctrflwdebug:
                print(f"[DEBUG] Function '{self.current_function_name}' definition completed.")

            self.in_function_definition = False
            self.current_function_name = None 
        def cmd_call(self, args):
            """
            Calls a previously defined function, passing arguments as needed.
            Syntax:
                call function_name [args...]
            """
            self.local=True
            args = self.replace_additional_parameters(args)
            parts = shlex.split(args.strip())
            if not parts:
                print("--ErrID36: No function name specified in 'call'")
                if self.REPL == 0: self.cmd_exit()
                return

            function_name = parts[0]
            if function_name not in self.functions:
                print(f"--ErrID37: Function '{function_name}' not defined.")
                if self.REPL == 0: self.cmd_exit()
                return

            fnc = self.functions[function_name]
            fnc_params = fnc.get("params", [])
            fnc_body = fnc.get("body", [])
            passed_args = parts[1:]

            # ⚠ Check parameter count
            if len(passed_args) != len(fnc_params):
                print(f"--ErrID38: Function '{function_name}' expects {len(fnc_params)} args, got {len(passed_args)}")
                if self.REPL == 0: self.cmd_exit()
                return
            # Setup local variables
            self.local_variables = {}
            for param, value in zip(fnc_params, passed_args):
                self.store_variable(param, value, "str", local=True)


            if self.ctrflwdebug:
                print(f"[DEBUG] Calling function '{function_name}' with arguments: {dict(zip(fnc_params, passed_args))}")

            for command in fnc_body:
                self.handle_command(command)
                if self.return_flag:
                    break
            # Capture return and clear local scope
            result = self.return_value
            self.return_flag = False
            self.return_value = None
            self.local_variables = {}
            self.local=False
            return result
        def cmd_switch(self, args):
            """Switch-case implementation."""
            if not args:
                print("--ErrID3: Incorrect number of arguments for switch command")
                if self.REPL == 0: self.cmd_exit()

            switch_var = args[0]
            if switch_var not in self.variables:
                print(f"--ErrID31: Variable '{switch_var}' not defined.")
                if self.REPL == 0: self.cmd_exit()

            self.control_stack.append({"type": "switch", "variable": self.variables[switch_var][0], "executed": False})

        def cmd_case(self, args):
            """Case block in a switch."""
            if not self.control_stack or self.control_stack[-1]["type"] != "switch":
                print("--ErrID32: 'case' command outside of 'switch' block.")
                if self.REPL == 0: self.cmd_exit()

            case_value = args[0]
            current_switch = self.control_stack[-1]
            if not current_switch["executed"] and current_switch["variable"] == case_value:
                current_switch["executed"] = True
                self.handle_command(" ".join(args[1:]))

        def cmd_default(self, args):
            """Default block in a switch."""
            if not self.control_stack or self.control_stack[-1]["type"] != "switch":
                print("--ErrID33: 'default' command outside of 'switch' block.")
                if self.REPL == 0: self.cmd_exit()

            self.control_stack[-1]["default"] = args

        def cmd_inc(self, args):
            """Increment a registered integer variable."""
            if len(args) != 1:
                print("--ErrID03: INC requires exactly one argument (variable name).")
                if self.REPL == 0:
                    self.cmd_exit()
                return

            var_name = args[0]
            var_data = self.variables.get(var_name)
            if self.vardebug:
                print(f"[DEBUG] Attempting to increment variable '{var_name}' with data: {var_data}")
            if var_data:
                new_value = var_data[0] + 1
                self.variables[var_name] = (new_value, "int")
                if self.ctrflwdebug:
                    print(f"[DEBUG] INC: {var_name} incremented to {new_value}")
            else:
                print(f"--ErrID34: Variable '{var_name}' is not defined or not an integer.")
                if self.REPL == 0:
                    self.cmd_exit()


        def cmd_dec(self, args):
            """Decrement a registered integer variable."""
            if len(args) != 1:
                print("--ErrID03: DEC requires exactly one argument (variable name).")
                if self.REPL == 0:
                    self.cmd_exit()
                return

            var_name = args[0]
            var_data = self.variables.get(var_name)

            if var_data and var_data[1] == "int":
                new_value = var_data[0] - 1
                self.variables[var_name] = (new_value, "int")
                if self.ctrflwdebug:
                    print(f"[DEBUG] DEC: {var_name} decremented to {new_value}")
            else:
                print(f"--ErrID34: Variable '{var_name}' is not defined or not an integer.")
                if self.REPL == 0:
                    self.cmd_exit()
                    
        def cmd_wait(self, args):
            """Wait for a specified number of seconds."""
            try:
                duration = int(args)
                self.log_debug(f"Waiting for {duration} seconds...")
                time.sleep(duration)
            except ValueError:
                print("--ErrID3: Duration must be an integer.")
                if self.REPL == 0: self.cmd_exit()

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
        def cmd_pow(self, args):
            self.perform_arithmetic_operation(args, operation="pow")
        def cmd_inv_sqrt(self, args):
            self.perform_arithmetic_operation(args, operation="inv_sqrt")


        def cmd_fastmath(self,a):x,e=a.split('=',1);r=eval(e,{'__builtins__':None,'math':math},{k:self.variables[k][0]for k in self.variables});self.variables[x.strip()]=[r,'float'if type(r) is float else'int']
        """
        oh god this is insane on so many levels like just look at this
        this makes me wonna vomit.
        Absolutely disgusting piece of code just for the sake of faster math operations.
        Syntax: fastmath <var_name> = <expression>
        """

        def perform_arithmetic_operation(self, args, operation):
            """
            Handles arithmetic operations with variable and expression support.
            Syntax: <var_name> <operand1> <operand2 or math expression>
            Example:
                add result $a 5
                mul area $length * $width
            """
            try:
                args = shlex.split(args)

                if len(args) < 3:
                    raise ValueError(f"Syntax: {operation} <var_name> <operand1> <operand2 or expression>")

                var_name, op1_token = args[0], args[1]
                op2_expr = " ".join(args[2:])  # Full math expression or raw operand

                op1_key = op1_token.lstrip("$")
                if op1_key in self.variables:
                    operand1 = self.variables[op1_key][0]
                else:
                    try:
                        operand1 = float(op1_token) if '.' in op1_token else int(op1_token)
                    except ValueError:
                        raise ValueError(f"Invalid operand1: '{op1_token}'")

                def substitute_vars(expr):
                    def replace_var(match):
                        varname = match.group(0).lstrip("$")
                        if varname in self.variables:
                            return str(self.variables[varname][0])
                        else:
                            raise ValueError(f"Variable '{varname}' not defined in expression.")
                    return re.sub(r'\$?[a-zA-Z_]\w*', replace_var, expr)

                op2_eval = substitute_vars(op2_expr)
                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Evaluating op2: '{op2_expr}' -> '{op2_eval}'")

                try:
                    operand2 = eval(op2_eval, {"__builtins__": {}})
                except Exception as e:
                    raise ValueError(f"Failed to evaluate expression '{op2_expr}': {e}")

                # -- Convert both to int or float --
                try:
                    operand1 = float(operand1) if '.' in str(operand1) else int(operand1)
                    operand2 = float(operand2) if '.' in str(operand2) else int(operand2)
                except ValueError:
                    raise TypeError("Operands must be numeric.")
                operations = {
                    "add": lambda x, y: x + y,
                    "sub": lambda x, y: x - y,
                    "mul": lambda x, y: x * y,
                    "div": lambda x, y: x / y if y != 0 else (_ for _ in ()).throw(ZeroDivisionError("Division by zero")),
                    "mod": lambda x, y: x % y if y != 0 else (_ for _ in ()).throw(ZeroDivisionError("Modulo by zero")),
                    "pow": lambda x, y: x ** y,
                    "sqrt": lambda x: x ** 0.5 if x >= 0 else (_ for _ in ()).throw(ValueError("Square root of negative number")),
                    "inv_sqrt": lambda x: 1 / (x ** 0.5) if x > 0 else (_ for _ in ()).throw(ValueError("Inverse square root of non-positive number"))

                }

                if operation not in operations:
                    raise ValueError(f"Unknown operation '{operation}'.")
                result = operations[operation](operand1, operand2)

                result_type = "int" if isinstance(result, int) or result == int(result) else "float"
                self.store_variable(var_name, int(result) if result_type == "int" else result, result_type, local=self.local)

                if self.mathdebug:
                    print(f"[DEBUG] {operation.upper()}: {operand1} {operation} {operand2} = {result} (stored as {result_type} in '{var_name}')")

            except Exception as e:
                print(f"[ERROR] {e}")
                if self.REPL == 0: 
                    self.cmd_exit()

        def try_convert(self, value):
            try:
                return float(value) if '.' in str(value) else int(value)
            except ValueError:
                return None

        def get_variable_value(self, var_name):
            if var_name in self.variables:
                return self.variables[var_name][0]  #  Return the stored value
            return var_name  #  Return the variable name itself if undefined

        def cmd_open_terminal(self, args):
            install_package('pygetwindow', "gw") #Import pygetwindow as "gw" lol.

            from colorama import Fore, Style #for custom font color in terminal

            # Fix incorrect spelling of split()
            if "," not in args:
                args = args.split()
            else:
                args = args.split(", ")

            if len(args) < 5:
                print("--ErrID100: Incorrect usage. Expected format: open_terminal command x y width height [load] [ColorName]")
                if self.REPL == 0: self.cmd_exit()

                return

            # Check if 'load' is given BEFORE checking colors
            load_mode = False
            if "load=true" in args:
                args.remove("load=true")  # Remove it from the list
                load_mode = True

            # Check if a valid color name is given (after "load" is handled)
            color_name = None
            if len(args) > 5:  
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
                print("--ErrID100: Incorrect usage. Expected format: open_terminal command x y width height [load] [ColorName]")
                if self.REPL == 0: self.cmd_exit()

                return

            command, pos_x, pos_y, width, height = args

            try:
                pos_x, pos_y, width, height = map(int, [pos_x, pos_y, width, height])
            except ValueError:
                print("--ErrID101: Position and size parameters must be integers.")
                if self.REPL == 0: self.cmd_exit()

                return

            terminal_title = "CMD"

            # If 'load' is given, modify the command to load the first argument in the interpreter
            if load_mode:
                command = f'python.exe "MintEclipse.py" -f "{command}"'

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
            self.flush()

            import argparse
            import time
            import re
            import os
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
            if self.REPL==0:
                try:
                    target_line = int(line_number)
                    if target_line < 1 or target_line > len(self.script_lines):
                        print(f"--ErrID75: Line {target_line} is out of range.")
                        if self.REPL == 0: self.cmd_exit()

                        return
                    self.current_line = target_line - 1  # Adjusted for 0-based index
                    if self.cmdhandlingdebug:
                        print(f"[DEBUG] Jumping to line {target_line}.")

                except ValueError:
                    print(f"--ErrID76: Invalid line number '{line_number}'. Must be an integer.")
                    if self.REPL == 0: self.cmd_exit()
                except Exception as e:
                    print(f"[CRITICAL ERROR]: '{e}'")    
            else:
                print(f"[DEBUG] GOTO command is not available in REPL mode.")
    def main():
        try:
            parser = argparse.ArgumentParser(description="X3 Interpreter")
            parser.add_argument('-f', '--file', type=str, help='File to execute as a script')
            parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
            args = parser.parse_args()
            
            #uses debug mode if nessecary idk
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
                            interpreter.current_line += 1  # Move to the next line unless `goto` changes it (i hope this doesnt breaks anything)

                except Exception as exc:
                    print(f"[CRITICAL ERROR] Could not load {args.file} due to reason:{exc}")            
            else:
                global REPL
                REPL = 1
                interpreter.REPL = 1
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
        #cProfile.run("main()")
        main()
except (KeyboardInterrupt, EOFError):
    print("\n")

except Exception as e:
    print(f"[CRITICAL ERROR]: {e},\nTerminating script.")
#Official 1k lines of code!!-November/24
#Development Phase start of Eclispe-March/25
#Official release of Eclispe 0.9. May/25
#Development Phase start of MintEclipse. June/25
#Official 2k lines of code!!-July/25
