help_descriptions={
'add':"""
Description: Adds two numbers.
Usage: add var_name num1 num2
Example: add result 5 10
This will store the sum of 5 and 10 in the variable 'result'.
""",
'a_file':"""
Description: Appends text to a file.
Usage: a_file file_path text_to_append
Example: a_file /path/to/file.txt "Hello, World!"
This will append "Hello, World!" to the specified file.
""",
'call':"""
Description: Calls a defined function with arguments.
Usage: call function_name arg1 arg2 ...S
Example: call myFunction 5 "Hello"
This will call the function 'myFunction' with the arguments 5 and "Hello".
""",
'cls':"""
Description: Clears the console screen.
Usage: cls [legacy]
Example: cls
This will clear the console screen. If 'legacy' is provided, it will use a legacy method.
""",
'create_dir':"""
Description: Creates a new directory.
Usage: create_dir dir_path
Example: create_dir /path/to/new_directory
This will create a new directory at the specified path.
""",
'dec':"""
Description: Decreases a variable's value by a specified amount.
Usage: dec var_name amount
Example: dec counter 1
This will decrease the value of 'counter' by 1.
""",
'def':"""
Description: Defines a new function.
Usage: def function_name param1 param2 ...
Example: def myFunction x y
This will define a new function named 'myFunction' with parameters x and y.
""",
'del':"""
Description: Deletes a variable or function.
Usage: del (var/func) name
Example: del var myVariable
This will delete the variable named 'myVariable'.
""",
'del_file':"""
Description: Deletes a specified file.
Usage: del_file file_path
Example: del_file /path/to/file.txt
This will delete the specified file.
""",
'delete_dir':"""
Description: Deletes a specified directory.
Usage: delete_dir dir_path
Example: delete_dir /path/to/directory
This will delete the specified directory.
""",
'dev.debug':"""
Description: Toggles developer debug mode.
Usage: dev.debug
Example: dev.debug
This will toggle the developer debug mode on or off.
""",
'div':"""
Description: Divides two numbers.
Usage: div var_name num1 num2
Example: div result 10 2
This will store the result of 10 divided by 2 in the variable 'result'.
""",
'else':"""
Description: Marks the else block in conditional statements.
Usage: else
Example: if condition
             ...
         else ...
This will execute the code in the else block if the condition is false.
""",
'end':"""
Description: Marks the end of a conditional block.
Usage: end
Example: if condition
             ...
         end
This will signify the end of the conditional block.
""",
'exit':"""
Description: Exits the interpreter.
Usage: exit [code]
Example: exit 0
This will exit the interpreter with the specified exit code (default is none).
""",
'fastmath':"""
Description: Does mathmatical calculations on a variable in a optimized manner.
Usage: fastmath var_name = value
Example: fastmath counter = counter + 5
This will increase the value of 'counter' by 5.
""",
'fetch':"""
Description: Fetches content from a URL.
Usage: fetch var_name url
Example: fetch content http://example.org
This will store the content fetched from the URL into the variable 'content'.
""",
'flush':"""
[WARNING] Usuage is deprecated and will be removed in future versions. Use 'reinit' instead.
Description: Resets the interpreter state.
Usage: flush
Example: flush
This will reset the interpreter state, clearing all variables and functions.
""",
'fncend':"""
Description: Marks the end of a function definition.
Usage: fncend
Example: def myFunction x y
             ...
         fncend
This will signify the end of the function definition.
""",
'goto':"""
Description: Jumps to a specified line number in the script.
Usage: goto line_number
Example: goto 10
This will jump to line number 10 in the script.
""",
'if':"""
Description: Starts a if conditional block.
Usage: if condition
Example: if x > 5
             ...
         end
This will start a conditional block that executes if the condition is true.
""",
'inc':"""
Description: Increases a variable's value by a specified amount.
Usage: inc var_name amount
Example: inc counter 1
This will increase the value of 'counter' by 1.
""",
'inp':"""
Description: Prompts the user for input and stores it in a variable.
Usage: inp var_name prompt_text [default_value]
Example: inp userName "Enter your name: " "Guest"
This will prompt the user to enter their name and store it in 'userName', defaulting to "Guest" if no input is provided.
""",
'load':"""
Description: Loads and executes a script from a file.
Usage: load file_path
Example: load /path/to/script.txt
This will load and execute the script located at the specified file path.
""",
'mod':"""
Description: Calculates the modulus of two numbers.
Usage: mod var_name num1 num2
Example: mod result 10 3
This will store the result of 10 mod 3 in the variable 'result'.
""",
'mul':"""
Description: Multiplies two numbers.
Usage: mul var_name num1 num2
Example: mul result 5 10
This will store the product of 5 and 10 in the variable 'result'.
""",
'prt':"""
Description: Prints text or variable values to the console.
Usage: prt word1 word2 word3 $var1 $var2 $var3 ...
Example: prt "Hello, " $userName "!"
This will print "Hello, " followed by the value of 'userName' and an exclamation mark.
""",
'reg':"""
Description: Creates a new variable.
Usage: reg (int/float/bool/str) var_name value
Example: reg int counter 0
This will create a new integer variable named 'counter' with an initial value of 0.
""",
'reinit':"""
Description: Resets the interpreter state.
Usage: reinit
Example: reinit
This will reset the interpreter state, clearing all variables and functions.
""",
'return':"""
Description: Returns a value from a function.
Usage: return value
Example: return 5
This will return the value 5 from the current function.
""",
'r_file':"""
Description: Reads content from a file and stores it in a variable.
Usage: r_file var_name file_path
Example: r_file content /path/to/file.txt
This will read the content of the specified file and store it in the variable 'content'.
""",
'search_file':"""
Description: Searches for a specific text in a file.
Usage: search_file file_path search_text
Example: search_file /path/to/file.txt "Hello"
This will search for the text "Hello" in the specified file and print the lines containing it.
""",
'setclientrule':"""
Description: Sets a client rule with specified parameters.
Usage: setclientrule (repl, fastmath, semo, pedl,disableprt) (repl, fastmath, semo, pedl,disableprt) ...
Example: setclientrule repl fastmath
This will set the client rules to enable repl and fastmath features.
""",
'sqrt':"""
Description: Calculates the square root of a number.
Usage: sqrt var_name num
Example: sqrt result 16
This will store the square root of 16 in the variable 'result'.
""",
'sub':"""
Description: Subtracts one number from another.
Usage: sub var_name num1 num2
Example: sub result 10 5
This will store the result of 10 minus 5 in the variable 'result'.
""",
'terminal':"""
Description: Opens a new terminal window.
Usage: terminal command x y width height [load=true] [ColorName]
Example: terminal script.x3 100 100 800 600 load=true green
This will open a new terminal window at position (100, 100) with size 800x600, load the script 'script.x3', and set the text color to green.
""",
'try':"""
Description: Starts a try block for exception handling.
Usage: try
Example: try
             ...
         end
This will start a try block that can be used for exception handling.
""",
'wait':"""
Description: Pauses execution for a specified number of seconds.
Usage: wait seconds
Example: wait 5.5
This will pause execution for 5.5 seconds.
""",
'while':"""
Description: Starts a while loop that continues as long as the condition is true.
Usage: while condition
Example: while x < 10
             ...
         end
This will start a loop that continues executing as long as the condition is true.
""",
'w_file':"""
Description: Writes text to a file, overwriting existing content.
Usage: w_file file_path text_to_write
Example: w_file /path/to/file.txt "Hello, World!"
This will write "Hello, World!" to the specified file, overwriting any existing content.
""",
'--info':"""
Description: Displays information about the interpreter.
Usage: --info
Example: --info
This will display information about the interpreter, including version and author details.
""",
}
