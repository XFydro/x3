# Luna PROTOTYPE 0.1
# Licensed under CC4.0 BY-SA-NC
# For more information: https://creativecommons.org/licenses/by-nc-sa/4.0

import argparse
import time
import re
import os
import shlex 
import json
import difflib
import subprocess
import cProfile
import sys
import importlib
import random
import math
import numpy as np
import struct
from typing import Dict, Tuple, List, Any, Optional, Callable, Union

# Global configuration
IDLE_MODE = 0  # Default script mode
VERSION = "3.9"  # Current version
DEBUG_LOG_FILE = "x3_debug.log"

class Interpreter:
    """Main interpreter class for the X3 language."""
    
    def __init__(self, debug: bool = False) -> None:
        """Initialize interpreter with default state."""
        self.current_line: int = 0
        self.variables: Dict[str, Tuple[Any, str]] = {}  # {name: (value, type)}
        self.functions: Dict[str, List[str]] = {}  # {name: [commands]}
        self.control_stack: List[Dict[str, Any]] = []
        self.debug: bool = debug
        self.debuglog: List[str] = []
        self.output: Optional[str] = None
        self.log_messages: List[str] = []
        self.execution_state: Dict[str, Any] = {}
        self.script_lines: List[str] = []
        
        # Debug flags
        self.ctrflwdebug: bool = False
        self.prtdebug: bool = False
        self.mathdebug: bool = False
        self.filedebug: bool = False
        self.clramadebug: bool = False
        self.cmdhandlingdebug: bool = False
        self.reqdebug: bool = False
        self.conddebug: bool = False
        
        # Rules
        self.fastmathrule: bool = False
        
        # Command mapping
        self.command_mapping: Dict[str, Callable] = {
            'host': self.cmd_host_file,
            'terminal': self.cmd_open_terminal,
            'goto': self.cmd_goto,
            'cls': self.cmd_clear,
            'dev.debug': self.dev,
            'wfile': self.cmd_create_file,
            'rfile': self.cmd_read_file,
            'afile': self.cmd_append_file,
            'delfile': self.cmd_delete_file,
            'createdir': self.cmd_create_dir,
            'deletedir': self.cmd_delete_dir,
            'searchfile': self.cmd_search_file,
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
            'wait': self.cmd_wait,
            'log': self.cmd_log,
            'fncend': self.cmd_fncend,
            'load': self.load,
            'flush': self.flush,
            'reinit': self.cmd_reinit,
            '--info': self.info,
        }
        
        self.exceptional_commands: set = {"//", "", " "}
        
        # Color dictionary
        self.color_dict: Dict[str, str] = {
            # Foreground Colors
            "-/red": "\033[91m",
            "-/orange": "\033[38;5;214m",
            "-/yellow": "\033[93m",
            "-/green": "\033[92m",
            "-/blue": "\033[94m",
            "-/indigo": "\033[38;5;57m",
            "-/violet": "\033[38;5;135m",
            "-/cyan": "\033[96m",
            "-/white": "\033[97m",
            
            # Background Colors
            "-bg/red": "\033[41m",
            "-bg/orange": "\033[48;5;214m",
            "-bg/yellow": "\033[43m",
            "-bg/green": "\033[42m",
            "-bg/blue": "\033[44m",
            "-bg/indigo": "\033[48;5;57m",
            "-bg/violet": "\033[48;5;135m",
            "-bg/cyan": "\033[46m",
            "-bg/white": "\033[47m",
            
            # Bold Colors
            "-bold/red": "\033[1;91m",
            "-bold/orange": "\033[1;38;5;214m",
            "-bold/yellow": "\033[1;93m",
            "-bold/green": "\033[1;92m",
            "-bold/blue": "\033[1;94m",
            "-bold/indigo": "\033[1;38;5;57m",
            "-bold/violet": "\033[1;38;5;135m",
            "-bold/cyan": "\033[1;96m",
            "-bold/white": "\033[1;97m",
        }
        
        # Additional parameters
        self.additional_parameters: Dict[str, Callable] = {
            "##random": lambda: random.random(),
            "##randint": lambda: random.randint(0, 100),
            "##timeseconds": lambda: time.time(),
            "##timestamp": lambda: int(time.time())
        }
        
        # Install required packages
        self.install_package("colorama")
        self.install_package("requests")

    def install_package(self, package: str, alias: Optional[str] = None) -> Optional[Any]:
        """Install a Python package if not already installed."""
        try:
            module = importlib.import_module(package)
            if IDLE_MODE == 1:
                print(f"{package} is already installed.")
        except ImportError:
            print(f"{package} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            
            try:
                module = importlib.import_module(package)
            except ImportError:
                print(f"Error: Failed to import {package} after installation.")
                return None

        if alias:
            globals()[alias] = module
            print(f"Imported {package} as {alias}.")
        else:
            globals()[package] = module

        return module

    def info(self) -> None:
        """Print interpreter version information."""
        print(f"Luna PROTOTYPE {VERSION}")

    def flush(self) -> None:
        """Reset interpreter state to initial conditions."""
        self.current_line = 0
        self.variables = {}
        self.functions = {}
        self.control_stack = []
        self.debug = False
        self.debuglog = []
        self.output = None
        self.log_messages = []
        self.execution_state = {}
        
        # Reset debug flags
        self.ctrflwdebug = False
        self.prtdebug = False
        self.mathdebug = False
        self.filedebug = False
        self.clramadebug = False
        self.cmdhandlingdebug = False
        self.reqdebug = False
        self.conddebug = False
        
        # Reset rules
        self.fastmathrule = False

    def comment_strip(self, s: str) -> str:
        """Remove comments from a command string."""
        return s.split('\\')[0]

    def load(self, filename: str) -> None:
        """Load and execute commands from a .x3 file."""
        if not os.path.exists(filename):
            if self.filedebug:
                print(f"ErrId53: The file '{filename}' does not exist.")
            if not IDLE_MODE:
                self.cmd_exit()
            return
            
        if not os.path.isfile(filename):
            if self.filedebug:
                print(f"ErrId54: The path '{filename}' is not a file.")
            if not IDLE_MODE:
                self.cmd_exit()
            return
                
        if not filename.endswith('.x3'):
            if self.filedebug:
                print(f"ErrId55: The file '{filename}' is not a .x3 file.")
            if not IDLE_MODE:
                self.cmd_exit()
            return

        try:
            with open(filename, 'r') as test_file:
                pass
        except PermissionError:
            if self.filedebug:
                print(f"ErrId56: Permission denied for file '{filename}'.")
            if not IDLE_MODE:
                self.cmd_exit()
            return
        except IOError as e:
            if self.filedebug:
                print(f"ErrId57: An I/O error occurred while accessing '{filename}': {e}")
            if not IDLE_MODE:
                self.cmd_exit()
            return
                
        try:
            interpreter = Interpreter()
            with open(filename, 'r') as file:
                for line in file:
                    command = line.strip()
                    interpreter.handle_command(command)
        except FileNotFoundError:
            if self.filedebug:
                print(f"ErrId53: The file '{filename}' was not found.")
                if not IDLE_MODE: 
                    self.cmd_exit()
        except Exception as e:
            if self.filedebug:
                print(f"[DEBUG] An error occurred while executing commands from '{filename}': {e}")

    def log(self, message: str) -> None:
        """Log a debug message if debugging is enabled."""
        if self.debug:
            print(f"[DEBUG]: {message}")
            self.debuglog.append(f"[DEBUG]: {message}")

    def cmd_clear(self, args: str = "") -> None:
        """Clear the terminal screen."""
        if args != "legacy":  
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("\n" * 100)

    def cmd_if(self, condition: str) -> None:
        """Evaluate an IF condition and push it to the control stack."""
        try:
            result = self.eval_condition(condition)
        except ValueError as e:
            print(f"ErrId77: Invalid IF condition '{condition}'. Details: {e}")
            if not IDLE_MODE: 
                self.cmd_exit()

        self.control_stack.append({
            "type": "if", 
            "executed": result, 
            "has_else": False
        })
        
        if self.ctrflwdebug:
            print(f"[DEBUG] IF condition '{condition}' evaluated to {result}, pushed to stack.")

        if not result and self.ctrflwdebug:
            print("[DEBUG] Skipping subsequent commands inside this IF block.")

    def cmd_else(self) -> None:
        """Execute an ELSE block only if the preceding IF block was false."""
        if not self.control_stack:
            print("ErrId78: ELSE without a matching IF.")
            if not IDLE_MODE:
                self.cmd_exit()
            return

        last_if = self.control_stack[-1]
        if last_if["type"] != "if":
            print("ErrId78: ELSE without a matching IF.")
            if not IDLE_MODE:
                self.cmd_exit()
            return

        if last_if.get("has_else", False):
            print("ErrId79: Multiple ELSE statements for the same IF.")
            if not IDLE_MODE:
                self.cmd_exit()
            return

        last_if["has_else"] = True
        last_if["executed"] = not last_if["executed"]

        if self.ctrflwdebug:
            if last_if["executed"]:
                print("[DEBUG] ELSE block will execute.")
            else:
                print("[DEBUG] Skipping ELSE block because IF condition was true.")
                
    def cmd_while(self, condition: str) -> None:
        """Implement a while-loop with proper nested execution."""
        if (self.control_stack and 
            self.control_stack[-1]["type"] == "while" and 
            self.control_stack[-1]["start_line"] == self.current_line):
            if self.ctrflwdebug:
                print(f"[DEBUG] Skipping duplicate WHILE on line {self.current_line}")
            return

        try:
            result = self.eval_condition(condition)
            self.control_stack.append({
                "type": "while",
                "condition": condition,
                "executed": result,
                "start_line": self.current_line
            })
            if self.ctrflwdebug:
                print(f"[DEBUG] WHILE condition '{condition}' evaluated to {result}, pushed to stack.")
        except ValueError as e:
            print(f"ErrId90: Invalid WHILE condition '{condition}'. Details: {e}")
            if not IDLE_MODE:
                self.cmd_exit()

    def cmd_end(self) -> None:
        """Handle 'end' for control structures like while loops."""
        if not self.control_stack:
            print("ErrId91: END without a matching control block")
            if not IDLE_MODE: 
                self.cmd_exit()
            return

        popped_block = self.control_stack.pop()
        debug = self.ctrflwdebug

        if debug:
            print(f"[DEBUG] END: Popped block: {popped_block}")

        if popped_block["type"] == "while":
            if self.eval_condition(popped_block["condition"]):
                self.control_stack.append(popped_block)
                self.current_line = popped_block["start_line"] - 1
            elif debug:
                print(f"[DEBUG] Exiting WHILE loop: {popped_block}")

        self.execution_state = (
            self.control_stack[-1]["executed"] 
            if self.control_stack 
            else True
        )

    def find_while_start(self, condition: str) -> int:
        """Find the start of a while loop in the script."""
        for i in range(self.current_line, -1, -1):
            line = self.lines[i].strip()
            if line.startswith("while ") and condition in line:
                return i + 1
        return self.current_line

    def should_execute(self) -> bool:
        """
        Determine if current block should execute based on control flow.
        Handles if/else blocks, while loops, and function definitions.
        """
        if not self.control_stack:
            return True
        
        # Check all blocks from innermost to outermost
        for block in reversed(self.control_stack):
            block_type = block.get("type")
            
            # Skip function definitions - they're just containers
            if block_type == "function_def":
                continue
                
            # Handle if/else blocks
            if block_type in ("if", "else"):
                if not block.get("executed", True):
                    return False
                    
            # Handle while loops
            elif block_type == "while":
                if not block.get("executed", True):
                    return False
                    
            # Handle function calls
            elif block_type == "function_call":
                if not block.get("executed", True):
                    return False

        return True
    def eval_condition(self, condition_str: str) -> bool:
        """Evaluate a conditional expression with proper operator precedence."""
        def process_and_conditions(and_condition: str) -> bool:
            and_parts = and_condition.split(" & ")
            results = [process_single_condition(cond.strip()) for cond in and_parts] 
            return all(results)

        or_conditions = condition_str.split(" | ")
        
        def try_convert(value: Any) -> Any:
            if isinstance(value, (int, float)):
                return value
            if isinstance(value, str) and value.replace(".", "", 1).isdigit():
                return float(value) if "." in value else int(value)
            return value.strip('"')

        def process_single_condition(cond: str) -> bool:
            parts = cond.split()

            if len(parts) == 1:
                if parts[0].startswith("!"):
                    var_name = parts[0][1:]
                    result = var_name not in self.variables
                    if self.conddebug:
                        print(f"[DEBUG] Condition '!{var_name}' -> {result}")  
                    return result
                result = parts[0] in self.variables
                if self.conddebug:
                    print(f"[DEBUG] Condition '{parts[0]} exists' -> {result}")  
                return result
            
            elif len(parts) >= 3:
                left = parts[0]
                operator = parts[1]
                right = " ".join(parts[2:])
            else:
                if self.conddebug:
                    print(f"[DEBUG] Invalid condition format: {cond}")  
                return False

            left_value = self.variables.get(left, [left])[0]
            right_value = self.variables.get(right, [right])[0] if right is not None else None

            left_value = try_convert(left_value)
            right_value = try_convert(right_value)
            
            if isinstance(left_value, (int, float)) and isinstance(right_value, str):
                if self.conddebug:
                    print(f"[DEBUG] Type mismatch: Cannot compare '{left_value}'({type(left_value)}) with '{right_value}'({type(right_value)})") 
                return False
            if isinstance(left_value, str) and isinstance(right_value, (int, float)):
                if self.conddebug:
                    print(f"[DEBUG] Type mismatch: Cannot compare '{left_value}'({type(left_value)}) with '{right_value}'({type(right_value)})") 
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
                "!>": lambda x, y: not (x > y),
                "!<": lambda x, y: not (x < y),
                "!>=": lambda x, y: not (x >= y),
                "!<=": lambda x, y: not (x <= y),
                "!==": lambda x, y: x is not y,
                "startswith": lambda x, y: str(x).startswith(str(y)),
                "endswith": lambda x, y: str(x).endswith(str(y)),
                "contains": lambda x, y: str(y) in str(x),
                "!contains": lambda x, y: str(y) not in str(x),
                "==ic": lambda x, y: str(x).lower() == str(y).lower(),
                "l==": lambda x, y: len(str(x)) == int(y),
                "l!=": lambda x, y: len(str(x)) != int(y),
                "l>": lambda x, y: len(str(x)) > int(y),
                "l<": lambda x, y: len(str(x)) < int(y),
                "is": lambda x, y: id(x) == id(y),
                "is not": lambda x, y: id(x) != id(y),
                "|+|": lambda x, y: int(difflib.SequenceMatcher(None, str(x), str(y)).ratio() * 100),
            }

            result = comparisons.get(operator, lambda x, y: False)(left_value, right_value)
            if self.conddebug:
                print(f"[DEBUG] Condition '{left} {operator} {right}' -> {result}")  
            return result

        results = [process_and_conditions(cond.strip()) for cond in or_conditions]
        if self.conddebug:
            print(f"[DEBUG] OR Conditions: {or_conditions} -> {results}")  
        return any(results)

    def cmd_prt(self, raw_args: str) -> None:
        """Enhanced print command with formatting and styling options."""
        if not raw_args:
            print("ErrID37: No arguments provided for prt command.")
            if not IDLE_MODE: 
                self.cmd_exit()
            return

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
            args = raw_args[1:-1] if raw_args.startswith('"') and raw_args.endswith('"') else raw_args

            settings_pattern = re.compile(r"(color_code|align|delay|title|tofile|format|case|border|effect|log)(?:=(\S+))?")
            matches = settings_pattern.findall(args)
            for key, value in matches:
                settings[key] = value.lower() if key != "delay" else float(value)

            args = settings_pattern.sub("", args).strip().replace("  ", " ")
            args = re.sub(r"\$([a-zA-Z_]\w*)", 
                         lambda m: str(self.variables.get(m.group(1), ["<" + m.group(1) + ">"])[0]), 
                         args)

            if settings["case"] == "upper":
                args = args.upper()
            elif settings["case"] == "lower":
                args = args.lower()

            if settings["alignment"] == "center":
                args = args.center(80)
            elif settings["alignment"] == "right":
                args = args.rjust(80)
            elif settings["alignment"] == "left":
                args = args.ljust(80)

            if settings["border"]:
                border_char = settings["border"] if len(settings["border"]) == 1 else "*"
                border_line = border_char * (len(args) + 4)
                args = f"{border_line}\n{border_char} {args} {border_char}\n{border_line}"

            effect_map = {"bold": "\033[1m", "italic": "\033[3m"}
            if settings["text_effect"] in effect_map:
                args = f"{effect_map[settings['text_effect']]}{args}\033[0m"

            if settings["title"]:
                print(f"\033]0;{settings['title']}\a", end="")

            if settings["format_type"] == "json":
                args = json.dumps({"message": args}, indent=4)
            elif settings["format_type"] == "html":
                args = f"<p>{args}</p>"

            if settings["save_to_file"]:
                with open(settings["save_to_file"], "w") as file:
                    file.write(args + "\n")

            if settings["log_message"]:
                self.log_messages.append(args)

            if settings["delay"]:
                for char in args:
                    sys.stdout.write(self.color_dict.get(settings["color_code"], "") + char)
                    sys.stdout.flush()
                    time.sleep(settings["delay"])
                print("\033[0m")
            else:
                print(self.color_dict.get(settings["color_code"], "") + args + "\033[0m")

            if self.prtdebug:
                print("[DEBUG] Print Settings: ", settings)

        except ValueError as e:
            print(f"ErrID38: Value error in prt command. Details: {e}")
            if not IDLE_MODE: 
                self.cmd_exit()
        except Exception as e:
            print(f"[CRITICAL ERROR] Unexpected error in prt command. Details: {e}")
            self.cmd_exit()

    def cmd_create_file(self, args: str) -> None:
        """Create a new file with specified content."""
        try:
            parts = args.split(' ', 1)
            if len(parts) < 2:
                print("ErrID50: Missing filename or content for create_file command.")
                if not IDLE_MODE: 
                    self.cmd_exit()
                return
            
            filename = parts[0]
            content = parts[1][1:-1] if parts[1].startswith('"') and parts[1].endswith('"') else parts[1]
            with open(filename, 'w', encoding='utf-8', errors='replace') as f:
                f.write(content)
            print(f"File '{filename}' created successfully.")
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to create file. Error: {e}")
            self.cmd_exit()

    def cmd_read_file(self, args: str) -> None:
        """Read content from a file and store it."""
        parts = args.split()

        if len(parts) < 2:
            print("ErrID52: Missing filename or variable name for read_file command.")
            if not IDLE_MODE: 
                self.cmd_exit()
            return

        filename = parts[0]

        if filename in self.variables and not (filename.startswith('"') and filename.endswith('"')):
            filename = self.variables[filename][0]

        try:
            with open(filename, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            var_name = parts[1]
            self.store_variable(var_name, content, "str")
            print(f"File content stored in variable '{var_name}'.")
        except FileNotFoundError:
            print(f"ErrID53: File '{filename}' not found.")
            if not IDLE_MODE: 
                self.cmd_exit()
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to read file. Error: {e}")
            self.cmd_exit()

    def cmd_append_file(self, args: str) -> None:
        """Append content to an existing file."""
        try:
            parts = args.split(' ', 1)
            if len(parts) < 2:
                print("ErrID55: Missing filename or content for append_file command.")
                if not IDLE_MODE: 
                    self.cmd_exit()
                return
            
            filename = parts[0]
            content = parts[1].strip('"')
            with open(filename, 'a', encoding='utf-8', errors='replace') as f:
                f.write(content)
            print(f"Content appended to file '{filename}' successfully.")
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to append to file. Error: {e}")
            self.cmd_exit()

    def fetch_data_from_api(self, url: Optional[str] = None, timeout: int = 20) -> None:
        """Fetch data from a specified URL or variable."""
        if not url:
            print("ErrID11: No URL or variable provided.")
            self.output = None
            if not IDLE_MODE: 
                self.cmd_exit()
            return

        if isinstance(url, str) and url in self.variables:
            url = self.variables[url]

        if not isinstance(url, str) or not url.strip():
            print("ErrID12: Invalid URL or variable key provided.")
            self.output = None
            if not IDLE_MODE: 
                self.cmd_exit()
            return

        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            self.output = response.text.strip()
            if self.reqdebug:
                print(f"[DEBUG] Data fetched and stored in output: {self.output}")
        except requests.exceptions.RequestException as e:
            print(f"[CRITICAL ERROR] Failed to fetch data from API. Error: {e}")
            self.output = None
            self.cmd_exit()

    def store_variable(self, var_name: str, value: Any, data_type: str) -> None:
        """Store a variable with type information."""
        if value != "output":
            self.variables[var_name] = (value, data_type)
        else:
            self.variables[var_name] = (self.output, data_type)
        self.cmd_log(f"Stored variable '{var_name}' with value '{value}' and type {data_type}")

    def cmd_fncend(self) -> None:
        """Mark the end of a function definition."""
        if hasattr(self, "current_function_name"):
            if self.ctrflwdebug:
                print(f"[DEBUG] End of function definition for '{self.current_function_name}'")
            del self.current_function_name
            self.in_function_definition = False

    def handle_command(self, command):
        """Processes commands, handles function definitions, and executes appropriately."""
        # Early return for empty lines or comments
        if not command or command.startswith(("//", "\\")):
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
            if cmd in {"else", "end"}:
                if self.ctrflwdebug:
                    print(f"[DEBUG] Handling '{cmd}' command even in failed IF block")
                self.command_mapping[cmd]()
            elif self.cmdhandlingdebug:
                print(f"[DEBUG] Skipping command '{command}' due to failed IF condition")
            return

        # Execute recognized commands
        if cmd in self.command_mapping:
            if self.cmdhandlingdebug:
                print(f"[DEBUG] Handling command: '{command}'")

            # No-arg commands
            no_arg_commands = {"else", "end", "dev.custom", "flush", "--info", "reinit", "dev.debug", "exit","fncend"}
            if cmd in no_arg_commands:
                self.command_mapping[cmd]()
            else:
                self.command_mapping[cmd](args)

            if self.cmdhandlingdebug:
                print(f"[DEBUG] Command '{cmd}' executed with args: '{args}'")
        else:
            print(f"ErrId73: Unrecognized command: {command}")
            if IDLE_MODE == 0:  # Note: 'idle' should probably be 'self.idle'?
                self.cmd_exit()
    def dev(self, raw_args: str) -> None:
        """Enable or disable debugging options dynamically."""
        debug_options = {
            "controlflow": "ctrflwdebug",
            "print": "prtdebug",
            "math": "mathdebug",
            "file": "filedebug",
            "colorama": "clramadebug",
            "requests": "reqdebug",
            "cmdhandling": "cmdhandlingdebug",
            "condition": "conddebug",
        }

        if not raw_args.strip():
            print("[SELF-DEBUG] Please provide a debug option (e.g., 'dev controlflow').")
            return

        args = raw_args.lower().split()

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
                setattr(self, debug_options[dbg_option], True)
                print(f"[SELF-DEBUG] Enabled debugging for: {dbg_option}")
                enabled_any = True
            else:
                print(f"[SELF-DEBUG] Incorrect usage: Unknown debug option '{dbg_option}'.")

        if not enabled_any:
            print("[SELF-DEBUG] No valid debug options provided. Use 'dev All' to enable all.")

    def cmd_log(self, *args: Any) -> None:
        """Log messages for debugging purposes."""
        message = " ".join(map(str, args))
        with open(DEBUG_LOG_FILE, "a") as log_file:
            log_file.write(f"{message}\n")

        if self.debug:
            print(f"[DEBUG] {message}")
            self.debuglog.append(f"[DEBUG] {message}")

    def str_len(self, args: str) -> None:
        """Calculate and store the length of a string variable."""
        parts = args.split()
        if len(parts) != 2:
            print("ErrID70: Incorrect syntax for str_len. Expected: str_len var_name result_var")
            if not IDLE_MODE: 
                self.cmd_exit()
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
                if not IDLE_MODE: 
                    self.cmd_exit()
        else:
            print(f"ErrID72: Variable '{var_name}' not found.")
            if not IDLE_MODE: 
                self.cmd_exit()

    def similarity_percentage(self, str1: str, str2: str) -> float:
        """Calculate the similarity percentage between two strings."""
        similarity = difflib.SequenceMatcher(None, str(str1), str(str2)).ratio() * 100
        return float(similarity)

    def replace_additional_parameters(self, input_str: str) -> str:
        """Replace special parameters with their computed values."""
        for key, func in self.additional_parameters.items():
            if key in input_str:
                result = str(func())
                input_str = input_str.replace(key, result)
        return input_str

    def cmd_reg(self, raw_args: str) -> None:
        """Register a variable with optional math evaluation."""
        raw_args = self.replace_additional_parameters(raw_args)

        parts = raw_args.split()
        if len(parts) < 3:
            print("ErrId80: Invalid variable registration format.")
            if not IDLE_MODE: 
                self.cmd_exit()
            return

        var_type = parts[0]
        var_name = parts[1]
        var_value = " ".join(parts[2:])
        
        if "|+|" in var_value:
            var_value = re.sub(
                r'(\w+)\s*\|\+\|\s*(\w+)',
                lambda match: str(self.similarity_percentage(match.group(1), match.group(2))),
                var_value
            )

        math_mode = "eval=true" in var_value
        if math_mode:
            var_value = var_value.replace("eval=true", "").strip().strip('"')

        matches = re.findall(r'\$([a-zA-Z_]\w*)', var_value)
        for var in matches:
            if var in self.variables:
                var_data = self.variables[var][0]
                replacement = f'"{var_data}"' if isinstance(var_data, str) else str(var_data)
                var_value = re.sub(rf'\${var}\b', replacement, var_value)
            else:
                raise ValueError(f"Variable '${var}' not found.")
                
        try:
            if isinstance(var_value, (int, float)) or var_value.replace(".", "", 1).isdigit():
                var_value = float(var_value) if "." in var_value else int(var_value)
            elif math_mode:
                operators = ["+", "-", "*", "/", "**", "%", "//"]
                var_value = re.sub('"', "", var_value)
                var_value = re.sub(r"(\d+(\.\d+)?)", r"\1", var_value)
                while any(op in str(var_value) for op in operators):
                    try:
                        var_value = eval(var_value, {"__builtins__": None}, {})
                        var_value = int(var_value)
                    except Exception as e:
                        print(f"ErrId85: Error during evaluation: {e}")
                        if not IDLE_MODE: 
                            self.cmd_exit()
                        return
            else:
                var_value = str(var_value)

        except ValueError as ve:
            print(ve)
            return
        except SyntaxError:
            print(f"ErrId84: Invalid Expression: {var_value}")
            if not IDLE_MODE: 
                self.cmd_exit()
            return
        except Exception as e:
            if self.mathdebug:
                print(f"[CRITICAL ERROR] Math evaluation failed: {e}")
            if not IDLE_MODE: 
                self.cmd_exit()
            return

        try:
            if isinstance(var_value, int):
                self.variables[var_name] = [var_value] 
            elif isinstance(var_value, float):
                self.variables[var_name] = [var_value]
            else:
                self.variables[var_name] = [str(var_value)] 

        except ValueError as e:
            print(e)
            if not IDLE_MODE: 
                self.cmd_exit()
            return

        if self.cmdhandlingdebug:
            print(f"[DEBUG] Registered variable '{var_name}' = {self.variables[var_name][0]} (Type: {var_type})")

    def cmd_delete_file(self, args: str) -> None:
        """Delete a specified file."""
        filename = args.strip()
        try:
            os.remove(filename)
            print(f"File '{filename}' deleted successfully.")
        except FileNotFoundError:
            print(f"ErrID57: File '{filename}' not found.")
            if not IDLE_MODE: 
                self.cmd_exit()
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to delete file. Error: {e}")
            self.cmd_exit()

    def cmd_create_dir(self, args: str) -> None:
        """Create a new directory."""
        directory_name = args.strip()
        try:
            os.makedirs(directory_name, exist_ok=True)
            print(f"Directory '{directory_name}' created successfully.")
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to create directory. Error: {e}")
            self.cmd_exit()

    def cmd_delete_dir(self, args: str) -> None:
        """Delete an empty directory."""
        directory_name = args.strip()
        try:
            os.rmdir(directory_name)
            print(f"Directory '{directory_name}' deleted successfully.")
        except FileNotFoundError:
            print(f"ErrID60: Directory '{directory_name}' not found.")
            if not IDLE_MODE: 
                self.cmd_exit()
        except OSError:
            print(f"ErrID61: Directory '{directory_name}' is not empty.")
            if not IDLE_MODE: 
                self.cmd_exit()
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to delete directory. Error: {e}")
            self.cmd_exit()

    def cmd_search_file(self, args: str) -> None:
        """Search for a keyword in a file."""
        try:
            parts = args.split(' ', 1)
            if len(parts) < 2:
                print("ErrID63: Missing filename or keyword for search_file command.")
                if not IDLE_MODE: 
                    self.cmd_exit()
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
            if not IDLE_MODE: 
                self.cmd_exit()
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to search file. Error: {e}")
            self.cmd_exit()

    def cmd_sqrt(self, args: str) -> None:
        """Calculate square root of a variable."""
        try:
            var_name = args.strip()
            if var_name in self.variables and isinstance(self.variables[var_name][0], (int, float)):
                value = self.variables[var_name][0]
                result = value ** 0.5
                self.store_variable(f"{var_name}_sqrt", result, "float")
                print(f"Square root of {value} stored in '{var_name}_sqrt'.")
            else:
                print(f"ErrID66: Variable '{var_name}' not defined or not numeric.")
                if not IDLE_MODE: 
                    self.cmd_exit()
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to calculate square root. Error: {e}")
            self.cmd_exit()

    def cmd_sys_info(self, args: str) -> None:
        """Display system information."""
        import platform
        info = {
            "OS": platform.system(),
            "Version": platform.version(),
            "Release": platform.release(),
            "Processor": platform.processor(),
        }
        for key, value in info.items():
            print(f"{key}: {value}")

    def cmd_set_env(self, args: str) -> None:
        """Set an environment variable."""
        try:
            parts = args.split(' ', 1)
            if len(parts) < 2:
                print("ErrID68: Missing variable name or value for set_env command.")
                if not IDLE_MODE: 
                    self.cmd_exit()
                return

            var_name, value = parts[0], parts[1]
            os.environ[var_name] = value
            print(f"Environment variable '{var_name}' set to '{value}'.")
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to set environment variable. Error: {e}")
            self.cmd_exit()

    def cmd_inp(self, raw_args: str) -> None:
        """Get user input and store as a variable."""
        try:
            if not raw_args.strip():
                raise ValueError("No arguments provided")
                
            args = shlex.split(raw_args)
            
            if len(args) < 2:
                raise ValueError("Missing arguments. Expected at least variable name and prompt")
                
            var_name = args[0]
            if not var_name.isidentifier():
                raise ValueError(f"'{var_name}' is not a valid variable name")
                
            prompt = args[1]
            default = args[2] if len(args) > 2 else None
            
            prompt_text = f"{prompt}"
            if default is not None:
                prompt_text += f" [default: {default}]"
            prompt_text += ": "
            
            user_input = input(prompt_text).strip()
            
            if not user_input and default is not None:
                user_input = default
            elif not user_input:
                raise ValueError("No input provided and no default specified")
                
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
            
            self.store_variable(var_name, value, var_type)
            self.cmd_log(f"Stored input: {var_name} = {value} ({var_type})")
            
        except Exception as e:
            error_message = f"Error in inp command: {str(e)}"
            if self.control_stack and self.control_stack[-1]["type"] == "try":
                self.control_stack[-1]["error"] = error_message
                self.cmd_log(f"[ERROR] {error_message}")
            else:
                print(f"{error_message}")
                if not IDLE_MODE: 
                    self.cmd_exit("Exiting due to error in inp command.")

    def cmd_fetch(self, args: str) -> None:
        """Fetch data from a URL."""
        if len(args) < 1:
            print("ErrID3: Incorrect number of arguments for fetch command")
            if not IDLE_MODE: 
                self.cmd_exit()
            return
            
        url = args[0]
        if url in self.variables:           
            self.fetch_data_from_api(self.variables[url])
        else:
            self.fetch_data_from_api(args)

    def cmd_exit(self, args: Optional[str] = None) -> None:
        """Exit the interpreter."""
        if args:
            print(f"[Exit]: {args}")
        if self.cmdhandlingdebug:    
            print("[DEBUG] Exiting")
        sys.exit(0)

    def log_debug(self, message: str) -> None:
        """Log a debug message."""
        if self.debug:
            print(f"[DEBUG] {message}")
            self.debuglog.append(f"[DEBUG] {message}")

    def cmd_exit_ce(self, error: str) -> None:
        """Exit with an error code."""
        print(f"Exiting, Error Code:{error}")
        sys.exit(1)

    def cmd_wait(self, args: str) -> None:
        """Wait for specified seconds."""
        try:
            duration = int(args)
            self.log_debug(f"Waiting for {duration} seconds...")
            time.sleep(duration)
        except ValueError:
            print("ErrID3: Duration must be an integer.")
            if not IDLE_MODE: 
                self.cmd_exit()

    def cmd_add(self, args: str) -> None:
        """Perform addition operation."""
        self.perform_arithmetic_operation(args, operation="add")

    def cmd_sub(self, args: str) -> None:
        """Perform subtraction operation."""
        self.perform_arithmetic_operation(args, operation="sub")

    def cmd_mul(self, args: str) -> None:
        """Perform multiplication operation."""
        self.perform_arithmetic_operation(args, operation="mul")

    def cmd_div(self, args: str) -> None:
        """Perform division operation."""
        self.perform_arithmetic_operation(args, operation="div")

    def cmd_mod(self, args: str) -> None:
        """Perform modulo operation."""
        self.perform_arithmetic_operation(args, operation="mod")

    def _fast_inv_sqrt(self, x: float) -> float:
        """Quake III Fast Inverse Square Root Algorithm."""
        if x <= 0:
            return float('inf')
        i = struct.unpack('>l', struct.pack('>f', x))[0]
        i = 0x5F3759DF - (i >> 1)
        y = struct.unpack('>f', struct.pack('>l', i))[0]
        return y * (1.5 - 0.5 * x * y * y)

    def cmd_fastmath(self, args):
        """Hyper-optimized math evaluation with multiple backends:
        fastmath var = <expression> [method=(quake|numpy|math)]
        """
        try:
            # Precompile regex patterns for better performance
            COMMENT_PATTERN = re.compile(r'//.*')
            METHOD_PATTERN = re.compile(r'\bmethod=(quake|numpy|math)\b')
            VAR_PATTERN = re.compile(r'\$([a-zA-Z_]\w*)')
            SQRT_PATTERN = re.compile(r'sqrt\(([^)]+)\)')
            INV_SQRT_PATTERN = re.compile(r'\*\*-0\.5|\*\*\(-0\.5\)|\/?sqrt\(')

            # Strip comments and whitespace in one pass
            args = COMMENT_PATTERN.sub('', args).strip()

            # Extract method (default to 'math')
            method_match = METHOD_PATTERN.search(args)
            method = method_match.group(1) if method_match else 'math'
            args = METHOD_PATTERN.sub('', args).strip()

            # Parse assignment more robustly
            parts = args.split('=', 1)
            if len(parts) != 2:
                raise ValueError("Syntax: fastmath <var> = <expression> [method=quake|numpy|math]")
            var_name, expr = map(str.strip, parts)

            # Create evaluation context
            var_cache = {k: v[0] for k, v in self.variables.items()}
            safe_globals = {'__builtins__': None}

            # Optimized variable substitution
            def safe_replace(match):
                var = match.group(1)
                return str(var_cache.get(f'${var}', match.group(0)))
            expr = VAR_PATTERN.sub(safe_replace, expr)

            # Determine evaluation strategy
            if method == 'quake' and INV_SQRT_PATTERN.search(expr):
                # Handle inverse square root with Quake method
                sqrt_match = SQRT_PATTERN.search(expr)
                x_val = float(eval(
                    sqrt_match.group(1) if sqrt_match else expr.split('**')[0].strip('()'),
                    safe_globals,
                    var_cache
                ))
                result = self._fast_inv_sqrt(x_val)
            else:
                # Standard evaluation with selected backend
                if method == 'numpy':
                    safe_globals['np'] = np
                elif method == 'math':
                    safe_globals['math'] = math
                
                result = eval(expr, safe_globals, var_cache)

            # Store result with type detection
            result_type = 'float' if isinstance(result, (float, np.floating)) else 'int'
            self.variables[var_name] = [float(result) if result_type == 'float' else int(result), result_type]

        except Exception as e:
            print(f"FastMath Error: {e}")
            if not getattr(self, 'idle', 0):  # Safer idle check
                self.cmd_exit()
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

    def get_variable_value(self, var_name: str) -> Any:
        """Get value of a variable or return the name if undefined."""
        if var_name in self.variables:
            return self.variables[var_name][0]
        return var_name

    def cmd_open_terminal(self, args: str) -> None:
        """Open a new terminal window with specified parameters."""
        self.install_package('pygetwindow', "gw")
        from colorama import Fore, Style

        if "," not in args:
            args = args.split()
        else:
            args = args.split(", ")

        if len(args) < 5:
            print("ErrID100: Incorrect usage. Expected format: open_terminal command x y width height [load] [ColorName]")
            if not IDLE_MODE: 
                self.cmd_exit()
            return

        load_mode = False
        if "load" in args:
            args.remove("load")
            load_mode = True

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
                args.pop()

        if len(args) < 5:
            print("ErrID100: Incorrect usage. Expected format: open_terminal command x y width height [load] [ColorName]")
            if not IDLE_MODE: 
                self.cmd_exit()
            return

        command, pos_x, pos_y, width, height = args

        try:
            pos_x, pos_y, width, height = map(int, [pos_x, pos_y, width, height])
        except ValueError:
            print("ErrID101: Position and size parameters must be integers.")
            if not IDLE_MODE: 
                self.cmd_exit()
            return

        terminal_title = "CMD"

        if load_mode:
            command = f'python.exe "luna.py" -f "{command}"'

        cmd_color = color_name if color_name else "7"
        cmd = f'start "CMD" cmd /k "title {terminal_title} & chcp 65001 & color {cmd_color} & {command}"'

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

    def cmd_reinit(self) -> None:
        """Reinitialize the interpreter."""
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

    def cmd_goto(self, line_number: str) -> None:
        """Jump to a specific line in script execution mode."""
        if not IDLE_MODE:
            try:
                target_line = int(line_number)
                if target_line < 1 or target_line > len(self.script_lines):
                    print(f"ErrId75: Line {target_line} is out of range.")
                    if not IDLE_MODE: 
                        self.cmd_exit()
                    return
                self.current_line = target_line - 1
                if self.cmdhandlingdebug:
                    print(f"[DEBUG] Jumping to line {target_line}.")

            except ValueError:
                print(f"ErrId76: Invalid line number '{line_number}'. Must be an integer.")
                if not IDLE_MODE: 
                    self.cmd_exit()
            except Exception as e:
                print(f"[CRITICAL ERROR]: '{e}'")    
        else:
            print(f"[DEBUG] GOTO command is not available in REPL/IDLE mode.")

    def cmd_host_file(self, args: str) -> None:
        """Host a folder as a live-reloading HTTP server."""
        import http.server
        import socketserver
        import threading
        from pathlib import Path
        from urllib.parse import unquote
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        try:
            parser = argparse.ArgumentParser(description='Host a folder with live-reloading')
            parser.add_argument('directory', help='Directory to serve')
            parser.add_argument('port', type=int, help='Port to serve on')
            parser.add_argument('--interval', type=float, default=1.0,
                            help='Live-reload check interval in seconds')
            args = parser.parse_args(args.split())
            
            directory = Path(args.directory).resolve()
            if not directory.exists():
                raise FileNotFoundError(f"Directory not found: {directory}")
            if not directory.is_dir():
                raise NotADirectoryError(f"Path is not a directory: {directory}")
                
            if not (0 < args.port < 65536):
                raise ValueError("Port must be between 1 and 65535")

            os.chdir(directory)

            reload_file = directory / ".reload"
            with open(reload_file, "w") as f:
                f.write("initial")
                
            INDEX_FILES = ["index.html", "html.html", "default.html"]
            
            for index_file in INDEX_FILES:
                index_path = directory / index_file
                if index_path.exists() and index_path.is_file():
                    try:
                        with open(index_path, "r+", encoding='utf-8') as f:
                            content = f.read()
                            if "<!-- live reload -->" not in content:
                                reload_script = f"""
                                <!-- live reload -->
                                <script>
                                let lastContent = "";
                                setInterval(() => {{
                                fetch("/.reload?_=" + Date.now()) // prevent caching
                                    .then(res => res.text())
                                    .then(txt => {{
                                    if (lastContent && lastContent !== txt) {{
                                        console.log("Reload triggered");
                                        location.reload();
                                    }}
                                    lastContent = txt;
                                    }})
                                    .catch(err => console.error("Live reload error:", err));
                                }}, {int(args.interval * 1000)});
                                </script>
                                """
                                if "</body>" in content:
                                    content = content.replace("</body>", reload_script + "</body>")
                                elif "</head>" in content:
                                    content = content.replace("</head>", reload_script + "</head>")
                                else:
                                    content += reload_script
                                
                                f.seek(0)
                                f.write(content)
                                f.truncate()
                        break
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        print(f"[WARNING] Could not inject live-reload into {index_file}: {e}")

            class ReloadHandler(FileSystemEventHandler):
                def on_modified(self, event):
                    if not event.is_directory and event.src_path != str(reload_file):
                        with open(reload_file, "w") as f:
                            f.write(str(time.time()))

            class SafeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
                def translate_path(self, path):
                    path = super().translate_path(path)
                    path = unquote(path)
                    return os.normpath(path)
                
                def end_headers(self):
                    self.send_header('Cache-Control', 'no-store, must-revalidate')
                    self.send_header('Expires', '0')
                    super().end_headers()
                    
                def log_message(self, format, *args):
                    return

            observer = Observer()
            observer.schedule(ReloadHandler(), path=str(directory), recursive=True)
            observer.start()

            class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
                daemon_threads = True
                allow_reuse_address = True

            server = None
            try:
                with ThreadedTCPServer(("", args.port), SafeHTTPRequestHandler) as httpd:
                    server = httpd
                    print(f"Live server running on http://localhost:{args.port}")
                    print(f"Live-reload interval: {args.interval} seconds")
                    print("Press Ctrl+C to stop")
                    httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer is shutting down...")
            except Exception as e:
                print(f"[ERROR] Server error: {e}")
            finally:
                if observer.is_alive():
                    observer.stop()
                    observer.join()
                if server:
                    server.shutdown()
                if reload_file.exists():
                    reload_file.unlink()

        except Exception as e:
            print(f"[ERROR] Could not start web server: {e}")
            return
    def cmd_def(self, args: str) -> None:
        """
        Define a new function. Enters function definition mode where commands
        are stored until 'fncend' is encountered.
        """
        try:
            tokens = args.strip().split()
            if len(tokens) != 1:
                print("ErrID3: Incorrect number of arguments for 'def'. Expected: def function_name")
                if not IDLE_MODE: 
                    self.cmd_exit()
                return

            function_name = tokens[0]

            if function_name in self.functions:
                print(f"ErrID8: Function '{function_name}' already defined.")
                if not IDLE_MODE: 
                    self.cmd_exit()
                return

            # Initialize function definition
            self.functions[function_name] = {
                'commands': [],
                'start_line': self.current_line if hasattr(self, 'current_line') else 0
            }
            self.current_function_name = function_name
            self.in_function_definition = True

            # Push function definition block to control stack
            self.control_stack.append({
                'type': 'function_def',
                'name': function_name,
                'executed': True
            })

            if self.ctrflwdebug:
                print(f"[DEBUG] Started function definition for '{function_name}'")

        except Exception as e:
            print(f"Error in function definition: {str(e)}")
            if not IDLE_MODE:
                self.cmd_exit()
    def cmd_call(self, args: str) -> None:
        """
        Call a defined function with proper control flow handling.
        """
        try:
            if not args.strip():
                print("ErrID3: Missing function name for 'call' command")
                if not IDLE_MODE: 
                    self.cmd_exit()
                return

            function_name = args.strip()

            if function_name not in self.functions:
                print(f"ErrID36: Function '{function_name}' not defined.")
                if not IDLE_MODE: 
                    self.cmd_exit()
                return

            # Push function call to control stack
            self.control_stack.append({
                'type': 'function_call',
                'name': function_name,
                'return_line': self.current_line if hasattr(self, 'current_line') else 0,
                'executed': True
            })

            if self.ctrflwdebug:
                print(f"[DEBUG] Calling function '{function_name}'")

            # Execute each command in the function
            for cmd in self.functions[function_name]['commands']:
                self.handle_command(cmd)

            # Pop function call from stack when done
            if self.control_stack and self.control_stack[-1]['type'] == 'function_call':
                self.control_stack.pop()

        except Exception as e:
            print(f"Error calling function: {str(e)}")
            if not IDLE_MODE:
                self.cmd_exit()
    def cmd_fncend(self) -> None:
        """Mark the end of a function definition."""
        if not hasattr(self, 'current_function_name'):
            print("ErrID40: 'fncend' without matching 'def'")
            if not IDLE_MODE: 
                self.cmd_exit()
            return

        # Pop the function definition block from control stack
        if self.control_stack and self.control_stack[-1]['type'] == 'function_def':
            self.control_stack.pop()

        if self.ctrflwdebug:
            print(f"[DEBUG] Ended function definition for '{self.current_function_name}'")

        del self.current_function_name
        self.in_function_definition = False
def main() -> None:
    """Main entry point for the interpreter."""
    try:
        parser = argparse.ArgumentParser(description="X3 Interpreter")
        parser.add_argument('-f', '--file', type=str, help='File to execute as a script')
        parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
        args = parser.parse_args()
        
        interpreter = Interpreter(debug=args.debug)

        if args.file:
            try:
                with open(args.file, 'r', encoding='utf-8', errors='replace') as script_file:
                    interpreter.script_lines = script_file.readlines()
                    interpreter.current_line = 0

                    while interpreter.current_line < len(interpreter.script_lines):
                        line = interpreter.script_lines[interpreter.current_line].strip()
                        interpreter.handle_command(line)
                        interpreter.current_line += 1

            except Exception as exc:
                print(f"[CRITICAL ERROR] Could not load {args.file} due to reason:{exc}")            
        else:
            global IDLE_MODE
            IDLE_MODE = 1
            while True:
                try:
                    user_input = input(">>")
                    interpreter.handle_command(user_input.strip())
                except (KeyboardInterrupt, EOFError):
                    print("\nExiting.")
                    break
    except (KeyboardInterrupt, EOFError):
        print("\n")
    except Exception as e:
        print(f"[CRITICAL ERROR]: {e},\nTerminating script.")

if __name__ == "__main__":
    main()
