#Welcome to Sardonix! a Better X3 interpreter, made by Raven #7.9.25
#this software is licenced under MIT License, for more information check: https://github.com/XFydro/x3/blob/main/license.txt
#Sardonix is a work in progress, expect bugs and missing features TwT.
import sys, re, ast, os, time, random, math

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

class SardonixRuntimeError(Exception): ...
class VariableStore:
    def __init__(self):
        self.stack = [{}]
    def push(self):
        self.stack.append({})
    def pop(self):
        if len(self.stack) > 1:
            self.stack.pop()
    def clear(self):
        self.stack = [{}]
    def get(self, name):
        for frame in reversed(self.stack):
            if name in frame:
                return frame[name]
        raise SardonixRuntimeError(f"Variable not defined: ${name}");sys.exit(1)
    def set(self, name, value):
        self.stack[-1][name] = value
    def items(self):
        merged = {}
        for f in self.stack:
            merged.update(f)
        return merged

class Context:
    def __init__(self):
        self.vars = VariableStore()
        self.functions = {}
        self.return_value = None
COMMANDS = {}
def command(name):
    def wrap(fn):
        COMMANDS[name] = fn
        return fn
    return wrap

STRING_RE = re.compile(r'"([^"\\]|\\.)*"')
VAR_RE = re.compile(r'\$([A-Za-z_][A-Za-z0-9_]*)')
FUNC_MACRO_RE = re.compile(r'##([A-Za-z_][A-Za-z0-9_]*)\:\(\)')
FUNC_CALL_RE = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)\s*\((.*?)\)')
CALL_RE = re.compile(r'call\((\w+)\)')

class Node:
    def __init__(self, kind, value=None, children=None, line=0):
        self.kind = kind
        self.value = value
        self.children = children or []
        self.line = line

def tokenize(line):
    out, i, in_str = [], 0, False
    while i < len(line):
        ch = line[i]
        if ch == '"' and (i == 0 or line[i-1] != '\\'):
            in_str = not in_str
            out.append(ch)
            i += 1
            continue
        if ch == '#' and not in_str:
            if i + 1 < len(line) and line[i+1] == '#':
                out.append('##'); i += 2; continue
            else:
                break
        out.append(ch)
        i += 1
    line = ''.join(out).strip()
    if not line:
        return []
    tokens, i = [], 0
    while i < len(line):
        if line[i].isspace():
            i += 1; continue
        if line[i] == '"':
            j = i + 1; escaped = False
            while j < len(line):
                c = line[j]
                if c == '"' and not escaped:
                    break
                escaped = (c == '\\' and not escaped)
                j += 1
            if j >= len(line):
                raise SardonixRuntimeError("Unterminated string");sys.exit(1)
            tokens.append(line[i:j+1]); i = j+1
        else:
            j = i
            while j < len(line) and not line[j].isspace():
                j += 1
            tokens.append(line[i:j]); i = j
    return tokens

BLOCK_STARTERS = {"if", "while", "def", "try"}
BLOCK_END_MARKS = {"end", "fncend"}

def replace_nibbits(expr: str, ctx: Context = None):
    if "##msec" in expr:
        expr = expr.replace("##msec", str(int(time.time() * 1000)))
    if "##timestamp" in expr:
        expr = expr.replace("##timestamp", str(int(time.time())))
    if "##REPL" in expr:
        expr = expr.replace("##REPL", "0")
    # interpreter:vars macro returns a readable string
    if "##interpreter:vars" in expr:
        if ctx is not None:
            iv = ctx.vars.items()
            expr = expr.replace("##interpreter:vars", repr(iv))
        else:
            expr = expr.replace("##interpreter:vars", "{}")
    return expr

def parse(lines):
    root = Node("block", line=0)
    stack = [root]
    for idx, raw in enumerate(lines, start=1):
        toks = tokenize(raw)
        if not toks: continue
        head, rest = toks[0], toks[1:]
        if head in ("if", "while", "def"):
            node = Node(head, value=' '.join(rest), line=idx)
            stack[-1].children.append(node)
            body = Node("block", line=idx)
            node.children.append(body)
            stack.append(body)
    
        elif head == "else":
            if len(stack) < 2:
                raise SardonixRuntimeError(f"Unexpected 'else' at line {idx}");sys.exit(1)
            last_if = stack[-2].children[-1]
            if last_if.kind != "if":
                raise SardonixRuntimeError(f"'else' without matching 'if' at line {idx}");sys.exit(1)
            if rest and rest[0] == "if":
                chain = Node("elif", value=' '.join(rest[1:]), line=idx)
                body = Node("block", line=idx)
                chain.children.append(body)
                last_if.children.append(chain)
                stack[-1] = body
            else:
                body = Node("block", line=idx)
                last_if.children.append(Node("else", children=[body], line=idx))
                stack[-1] = body
        elif head in BLOCK_END_MARKS:
            if len(stack) == 1:
                raise SardonixRuntimeError(f"Unexpected '{head}' at line {idx}");sys.exit(1)
            stack.pop()
        else:
            stack[-1].children.append(Node("cmd", value=(head, rest), line=idx))
    if len(stack) != 1:
        raise SardonixRuntimeError("Missing 'end'");sys.exit(1)
    return root

ALLOWED_NODES = {
    ast.Expression, ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Compare,
    ast.Name, ast.Load, ast.Constant,
    ast.And, ast.Or, ast.Not,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.USub, ast.UAdd,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
}
SAFE_NAMES = {"true": True, "false": False, "null": None}

def _assert_safe(node):
    if type(node) not in ALLOWED_NODES:
        raise SardonixRuntimeError(f"Illegal expression element: {type(node).__name__}");sys.exit(1)
    for child in ast.iter_child_nodes(node):
        _assert_safe(child)
def split_call_args(s: str):
    """Split function call args by commas at top level, respect quotes and nested parentheses."""
    args = []
    buf = []
    i = 0
    in_str = False
    depth = 0
    while i < len(s):
        ch = s[i]
        if ch == '"' and (i == 0 or s[i-1] != '\\'):
            in_str = not in_str
            buf.append(ch)
            i += 1
            continue
        if in_str:
            buf.append(ch)
            i += 1
            continue
        if ch in "([{":
            depth += 1
            buf.append(ch)
            i += 1
            continue
        if ch in ")]}":
            depth -= 1
            buf.append(ch)
            i += 1
            continue
        if ch == ',' and depth == 0:
            args.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    if buf:
        args.append("".join(buf).strip())
    # filter out empty args (e.g. no args)
    if len(args) == 1 and args[0] == "":
        return []
    return args
def eval_expr(expr: str, ctx: Context):
    """
    Evaluate an expression string safely, with:
    - variable substitution $name
    - function calls syntax: fname(arg1, arg2, ...)
      (finds the def whose name matches fname)
    - existing CALL_RE macros still supported (legacy)
    """
    # 1) Handle expression-style function calls: name(arg, ...)
    def func_call_replacer(m):
        fname = m.group(1)
        argtext = m.group(2).strip()
        # find function definition by name (your parser stores def key as "name param1 param2")
        fn_key = None
        for key in ctx.functions.keys():
            if key.split()[0] == fname:
                fn_key = key
                break
        if fn_key is None:
            raise SardonixRuntimeError(f"Function not defined: {fname}"); sys.exit(1)

        # parse argument expressions
        call_args = split_call_args(argtext) if argtext != "" else []
        # evaluate each argument in the current ctx (recursively)
        evaled_args = []
        for a in call_args:
            if a == "":
                evaled_args.append(0)
            else:
                evaled_args.append(eval_expr(a, ctx))

        # Prepare a local context to run the function body
        fn_node = ctx.functions[fn_key]  # this is the Node block for the function body
        # extract parameter names from the def key
        parts = fn_key.split()
        params = parts[1:] if len(parts) > 1 else []

        if len(evaled_args) != len(params):
            raise SardonixRuntimeError(f"Function '{fname}' expects {len(params)} args, got {len(evaled_args)}"); sys.exit(1)

        # run the function in a fresh context that shares function definitions
        local_ctx = Context()
        local_ctx.functions = ctx.functions
        # set parameters as variables (no $ in param names used in def)
        for pname, pval in zip(params, evaled_args):
            # store as variable without the $ prefix
            local_ctx.vars.set(pname, pval)

        # execute function body
        # Note: run_program returns (value, returned_flag) but for functions we rely on ctx.return_value
        run_program(fn_node, local_ctx, in_function=True)
        result = local_ctx.return_value
        return str(result if result is not None else 0)

    # run the function-call replacer repeatedly until no more matches (handles nested calls)
    prev = None
    new_expr = expr
    while prev != new_expr:
        prev = new_expr
        new_expr = FUNC_CALL_RE.sub(func_call_replacer, new_expr)

    expr = new_expr

    # keep legacy call(name) macro handling (if present)
    def call_replacer(m):
        funcname = m.group(1)
        if funcname not in ctx.functions:
            raise SardonixRuntimeError(f"Function not defined: {funcname}");sys.exit(1)
        local_ctx = Context()
        local_ctx.functions = ctx.functions
        old_return = ctx.return_value
        ctx.return_value = None
        run_program(ctx.functions[funcname], local_ctx)
        result = local_ctx.return_value
        ctx.return_value = old_return
        return str(result if result is not None else 0)

    expr = CALL_RE.sub(call_replacer, expr)

    # variable substitution into safe python identifiers for AST eval
    mapping = {}
    def repl(m):
        name = m.group(1)
        val = ctx.vars.get(name)  # will throw if missing
        pyname = f"__v_{name}"
        mapping[pyname] = val
        return pyname

    pre = VAR_RE.sub(repl, expr)

    tree = ast.parse(pre, mode="eval")
    _assert_safe(tree)
    return eval(compile(tree, "<expr>", "eval"), {"__builtins__": {}}, {**SAFE_NAMES, **mapping})
def comment_stripper(line: str) -> str:
    """
    Removes // and # comments from a line of Sardonix code,
    while keeping text inside quotes safe.
    """
    result = ""
    in_str = False
    i = 0
    while i < len(line):
        ch = line[i]
        # toggle string mode when encountering an unescaped "
        if ch == '"' and (i == 0 or line[i - 1] != '\\'):
            in_str = not in_str
            result += ch
            i += 1
            continue
        # handle // comments only if not inside a string
        if not in_str and ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
            break  # everything after // is ignored
        # handle # comments only if not inside a string
        if not in_str and ch == "#":
            break
        result += ch
        i += 1
    return result.strip()

def run_program(node: Node, ctx: Context, in_function=False):
    pc = 0
    children = node.children
    returned_value = None
    while pc < len(children):
        child = children[pc]
        if child.kind == "cmd":
            name, args = child.value
            if name == "call":
                funcname = args[0]
                if funcname not in ctx.functions:
                    raise SardonixRuntimeError(f"Function not defined: {funcname}");sys.exit(1)
                local_ctx = Context()
                local_ctx.functions = ctx.functions
                old_return = ctx.return_value
                ctx.return_value = None
                run_program(ctx.functions[funcname], local_ctx)
                ctx.return_value = local_ctx.return_value

            elif name == "return":
                ctx.return_value = eval_expr(" ".join(args), ctx) if args else None
                return 
            else:
                handler = COMMANDS.get(name)
                
                if not handler:
                    raise SardonixRuntimeError(f"Unknown command '{name}' at line {child.line}");sys.exit(1)
                handler(args, ctx, child)
        elif child.kind == "if":
            if eval_expr(child.value, ctx):
                val, ret = run_program(child.children[0], ctx, in_function=in_function)
                if ret:
                    return val, True
            else:
                executed = False
                for sub in child.children[1:]:
                    if sub.kind == "elif" and eval_expr(sub.value, ctx):
                        val, ret = run_program(sub.children[0], ctx, in_function=in_function)
                        executed = True
                        if ret:
                            return val, True
                        break
                    elif sub.kind == "else":
                        if not executed:
                            val, ret = run_program(sub.children[0], ctx, in_function=in_function)
                            if ret:
                                return val, True
                        break
        elif child.kind == "while":
            loop_guard = 0
            while eval_expr(child.value, ctx):
                val, ret = run_program(child.children[0], ctx, in_function=in_function)
                if ret:
                    return val, True
                loop_guard += 1
                if loop_guard > 5_000_000:
                    raise SardonixRuntimeError("While loop guard tripped");sys.exit(1)
        elif child.kind == "def":
            ctx.functions[child.value] = child.children[0]

        pc += 1
    return returned_value, False

def _unquote(tok):
    if tok.startswith('"') and tok.endswith('"'):
        return bytes(tok[1:-1], "utf-8").decode("unicode_escape")
    return tok
@command("//")
def cmd_comment(args, ctx: Context, node: Node):
    pass 
@command("del")
def cmd_del(args, ctx: Context, node: Node):
    """
    Deletes a variable or function from the current context.
    Usage:
        del var variable_name
        del func function_name
    """
    if len(args) != 2:
        raise SardonixRuntimeError(
            f"Invalid syntax for 'del' at line {node.line}. "
            "Expected: del var/func name"
        )

    target_type, name = args[0], args[1]

    if target_type == "var":
        try:
            ctx.vars.get(name)  # check if exists
            # Actually delete from the top stack frame
            for frame in reversed(ctx.vars.stack):
                if name in frame:
                    del frame[name]
                    print(f"[DEBUG] Deleted variable '{name}'.")
                    break
        except SardonixRuntimeError:
            raise SardonixRuntimeError(f"Variable '{name}' not defined.")

    elif target_type == "func":
        if name in ctx.functions:
            del ctx.functions[name]
            print(f"[DEBUG] Deleted function '{name}'.")
        else:
            raise SardonixRuntimeError(f"Function '{name}' not defined.")

    else:
        raise SardonixRuntimeError(
            f"Unknown target type '{target_type}' in 'del'. Use 'var' or 'func'."
        )

@command("prt")
def cmd_prt(args, ctx: Context, node: Node):
    parts_raw = []
    joined = " ".join(args)
    joined = replace_nibbits(joined, ctx)
    def var_repl(m):
        name = m.group(1)
        try:
            return str(ctx.vars.get(name))
        except SardonixRuntimeError:
            sys.exit(1)
    joined_vars = VAR_RE.sub(var_repl, joined)
    parts = [p.strip() for p in joined_vars.split("+")]
    out = []
    for part in parts:
        if part.startswith('"') and part.endswith('"'):
            out.append(_unquote(part))
        else:
            try:
                val = eval_expr(part, ctx)
                out.append(str(val))
            except Exception:
                out.append(part)
    print("".join(out))
@command("return")
def cmd_return(args, ctx: Context, node: Node):
    ctx.return_value = eval_expr(" ".join(args), ctx) if args else None

@command("reg")
def cmd_reg(args, ctx: Context, node: Node):
    if len(args) < 2:
        raise SardonixRuntimeError(f"reg needs: reg name value (line {node.line})");sys.exit(1)
    if args[0] in ("int", "float", "str"):
        vtype = args[0]
        if len(args) < 3:
            raise SardonixRuntimeError(f"Missing value for typed reg at line {node.line}");sys.exit(1)
        name = args[1]
        if not name.startswith("$"):
            name = "$" + name
        value_expr = " ".join(args[2:])
    else:
        vtype = None
        name = args[0]
        if not name.startswith("$"):
            raise SardonixRuntimeError(f"Variable must start with $ (line {node.line})");sys.exit(1)
        value_expr = " ".join(args[1:])
    value_expr = replace_nibbits(value_expr, ctx)
    val = eval_expr(value_expr, ctx)
    if vtype == "int":
        val = int(val)
    elif vtype == "float":
        val = float(val)
    elif vtype == "str":
        val = str(val)
    ctx.vars.set(name[1:], val)

@command("exit")
def cmd_exit(args, ctx: Context, node: Node):
    code = 0
    if args:
        try:
            code = int(eval_expr(" ".join(args), ctx))
        except Exception:
            code = 0
    sys.exit(code)
def _resolve_target(name):
    return name[1:] if name.startswith("$") else name

@command("add")
def cmd_add(args, ctx: Context, node: Node):
    target = _resolve_target(args[0])
    ctx.vars.set(target, eval_expr(args[1], ctx) + eval_expr(args[2], ctx))

@command("sub")
def cmd_sub(args, ctx: Context, node: Node):
    target = _resolve_target(args[0])
    ctx.vars.set(target, eval_expr(args[1], ctx) - eval_expr(args[2], ctx))

@command("mul")
def cmd_mul(args, ctx: Context, node: Node):
    target = _resolve_target(args[0])
    ctx.vars.set(target, eval_expr(args[1], ctx) * eval_expr(args[2], ctx))

@command("div")
def cmd_div(args, ctx: Context, node: Node):
    target = _resolve_target(args[0])
    b = eval_expr(args[2], ctx)
    if b == 0:
        raise SardonixRuntimeError("Division by zero");sys.exit(1)
    ctx.vars.set(target, eval_expr(args[1], ctx) / b)

@command("mod")
def cmd_mod(args, ctx: Context, node: Node):
    target = _resolve_target(args[0])
    ctx.vars.set(target, eval_expr(args[1], ctx) % eval_expr(args[2], ctx))

@command("pow")
def cmd_pow(args, ctx: Context, node: Node):
    target = _resolve_target(args[0])
    ctx.vars.set(target, eval_expr(args[1], ctx) ** eval_expr(args[2], ctx))

@command("inp")
def cmd_inp(args, ctx: Context, node: Node):
    if not args:
        raise SardonixRuntimeError("inp requires at least a variable name");sys.exit(1)
    varname = args[0]
    prompt = ""
    default = ""
    if len(args) >= 2:
        prompt = args[1].strip('"')
    if len(args) >= 3:
        default = args[2]
    val = ""
    try:
        val = input((prompt + " ") if prompt else "")
        if val == "" and default != "":
            val = default
    except EOFError:
        val = default
    ctx.vars.set(varname[1:], val)
#forgot to comment this out at the first place TwT #1.10.25-Raven
#@command("rand")
#def cmd_rand(args, ctx: Context, node: Node):
#    if len(args) == 3:
#        lo = int(eval_expr(args[1], ctx)); hi = int(eval_expr(args[2], ctx))
#        ctx.vars.set(args[0][1:], random.randint(lo, hi))
#    else:
#        ctx.vars.set(args[0][1:], random.random())

@command("len")
def cmd_len(args, ctx: Context, node: Node):
    if len(args) != 2:
        raise SardonixRuntimeError("len usage: len <var> <value>");sys.exit(1)
    ctx.vars.set(args[0][1:], len(str(eval_expr(args[1], ctx))))

@command("load")
def cmd_load(args, ctx: Context, node: Node):
    if not args:
        raise SardonixRuntimeError("load requires a filename")
    path = _unquote(args[0])
    if not os.path.exists(path):
        raise SardonixRuntimeError(f"File not found: {path}")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()
        
        # Strip both # and // comments (but not inside strings)
        processed = []
        for line in raw_lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            if line_stripped.startswith("//"):
                continue  # skip full-line // comments
            # remove inline // if outside quotes
            newline = ""
            in_str = False
            i = 0
            while i < len(line):
                ch = line[i]
                if ch == '"' and (i == 0 or line[i-1] != '\\'):
                    in_str = not in_str
                    newline += ch
                    i += 1
                    continue
                if not in_str and ch == "/" and i+1 < len(line) and line[i+1] == "/":
                    break  # stop at start of // comment
                newline += ch
                i += 1
            if newline.strip():
                processed.append(newline.rstrip())
        
        run_program(parse(processed), ctx)
    except Exception as e:
        raise SardonixRuntimeError(f"Failed to load file {path}: {e}")

@command("concat")
def cmd_concat(args, ctx: Context, node: Node):
    if len(args) < 2:
        raise SardonixRuntimeError("concat needs at least 2 args");sys.exit(1)
    result = "".join(str(eval_expr(ctx, a) if False else (ctx.vars.get(a[1:]) if a.startswith("$") else a)) for a in args[1:])

@command("sleep")
def cmd_sleep(args, ctx: Context, node: Node):
    if not args:
        raise SardonixRuntimeError("sleep needs seconds");sys.exit(1)
    time.sleep(float(eval_expr(" ".join(args), ctx)))

@command("wait")
def cmd_wait(args, ctx: Context, node: Node):
    if not args:
        raise SardonixRuntimeError("wait needs seconds");sys.exit(1)
    time.sleep(float(eval_expr(" ".join(args), ctx)))

@command("fastmath")
def cmd_fastmath(args, ctx: Context, node: Node):
    if len(args) >= 3 and args[1] == "=":
        var = args[0]
        expr = " ".join(args[2:])
        expr = replace_nibbits(expr, ctx)
        val = eval_expr(expr, ctx)
        ctx.vars.set(var, val)
    else:
        raise SardonixRuntimeError("fastmath usage: fastmath <var> = <expr>");sys.exit(1)

@command("sqrt")
def cmd_sqrt(args, ctx: Context, node: Node):
    if len(args) != 1:
        raise SardonixRuntimeError("sqrt usage: sqrt <var>");sys.exit(1)
    name = args[0].lstrip("$")
    v = ctx.vars.get(name)
    val = math.sqrt(float(v))
    ctx.vars.set(name + "_sqrt", val)

@command("sys_info")
def cmd_sys_info(args, ctx: Context, node: Node):
    print("OS:", os.name, "Platform:", sys.platform, "Python:", sys.version)

@command("setclientrule")
def cmd_setclientrule(args, ctx: Context, node: Node):
    # stub: just store a value
    if len(args) >= 1:
        ctx.vars.set("clientrule:" + args[0], True)

@command("dev.debug")
def cmd_dev_debug(args, ctx: Context, node: Node):
    # simple toggle/store
    arg = args[0] if args else None
    ctx.vars.set("_DEBUG", arg or "All")

@command("reinit")
def cmd_reinit(args, ctx: Context, node: Node):
    ctx.vars.clear()

@command("flush")
def cmd_flush(args, ctx: Context, node: Node):
    sys.stdout.flush()

@command("cls")
def cmd_cls(args, ctx: Context, node: Node):
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass

@command("goto")
def cmd_goto(args, ctx: Context, node: Node):
    """
    goto <line_number>
    Jumps execution to the given line number (1-based index in the current program).
    """
    if len(args) != 1:
        raise SardonixRuntimeError("goto requires exactly one argument (line number).")
    try:
        target = int(args[0])
    except ValueError:
        raise SardonixRuntimeError(f"goto argument must be an integer, got: {args[0]}")
    if target <= 0:
        raise SardonixRuntimeError("goto line numbers start at 1.")
    ctx.goto_target = target - 1

@command("fncend")
def cmd_fncend(args, ctx: Context, node: Node):
    # parsed as block end; nothing to do here :/
    return

def run_source(src: str, ctx=None):
    ctx = ctx or Context()
    run_program(parse(src.splitlines()), ctx)
    return ctx

def run_file(path: str, ctx=None):
    with open(path, "r", encoding="utf-8") as f:
        return run_source(f.read(), ctx)

def repl():
    ctx = Context()
    buf, depth = [], 0
    while True:
        try:
            prompt = "... " if depth > 0 else ">>> "
            line = input(prompt)
            line = comment_stripper(line)
            tl = tokenize(line)
            if not tl: continue
            if tl[0] in BLOCK_STARTERS:
                depth += 1
            elif tl[0] in BLOCK_END_MARKS:
                depth -= 1
                if depth < 0:
                    print("Syntax: stray 'end'"); depth = 0; buf.clear(); continue
            buf.append(line)
            if depth == 0:
                try:
                    run_program(parse(buf), ctx)
                except SardonixRuntimeError as e:
                    print(f"Error: {e}")
                    sys.exit(1)
                buf.clear()
        except KeyboardInterrupt:
            print("\n^C"); buf.clear(); depth = 0
        except EOFError:
            print(); break

if __name__ == "__main__":
    if len(sys.argv) > 1: run_file(sys.argv[1])
    else: repl()
