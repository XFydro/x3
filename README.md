@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ✈ Sardonix Interpreter ***(NEW)***
> *"Lightweight as a feather, dumb as a rock"*                       
> **Current Version:** `3.94`      
> **Project Phase:** Active development               

---

## What's Sardonix??

**Sardonix** is a lightweight and efficient(less beefy) version of **MintEclipse v3.94**, designed with medium level compatibility with v3.94, with a well defined abstract syntax tree and better tokenisation system.

Built by **[Raven (formally known as XFydro)](https://x3documentation.neocities.org/developer)** with enthusiasm and insanity >:3.

---
## 🛠️ Usage

### 💻 Run a Script
```bash
python "C:/.../sardonix.py" "-f" "script.x3"
```

---
@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# 🌑 MintEclipse Interpreter

> *"The only bug-free zone is your imagination. Good luck."*                                    
> **Current Version:** `3.9x`                                                                     
> **Project Phase:** Active development (SUBJECT TO OTHER CONCURRENT ACTIVE PROJECTS)                       

---

## 🎮 What is MintEclipse?

**MintEclipse** is a custom-built interpreter designed for **X3-based scripting**, infused with enhanced control flow, dynamic variables, expression parsing, function definitions, and rich debugging capabilities.  
It’s **modular, powerful, expressive**, and still evolving with each chaotic burst of passion. :3

Built by **[Raven (formally known as XFydro)](https://x3documentation.neocities.org/developer)** with passion and 💖. (ok i kinda lost my sanity over this so this point is straight up a lie. -Raven #10.9.25)

---

## 🌐 Online Editor (X3 Support!!)

Wanna try writing and testing X3/MintEclipse code *instantly* in your browser?

🧪 **[CSX3 Editor – Online X3 IDE](https://csx3-beta.netlify.app/)**  
A beautiful, web-based editor created by a dear friend, supports X3!

---

## 🧩 Features

- ✅ **Rich Command Mapping**: Over 50 built-in commands (`reg`, `prt`, `if`, `while`, `def`, `call`, `fetch`, and more!)
- 🔣 **Custom Variable Engine** with type handling and expression evaluation
- 📦 **Additional Parameters** like `##random`, `##timestamp`, `##fetch:(url)`, `##env:(PATH)`
- 🔐 **Safe Execution Modes (using setclientrule)** (`semo(Script Execution Mode Only)`, repl toggle, and debug toggles(dev.debug))
- 📚 **Script Loader** with error isolation, step-by-step tracking, and layered debug levels
- 💥 **Fastmath** for raw math execution (`fastmath x = ($a * $b) + 5`)
- 📜 **Function Blocks** (`def`, `fncend`, `call`,`return`)
- 🧠 **Advanced Condition Evaluation** with fuzzy matching, `startswith`, `contains`, and `==ic`

---

## 📦 Requirements

- Python **3.6+**
- Internet access (for `fetch`, `##fetch:*`, and online packages)
- A Patient mindset because no one knows what goes on in the python runtime.

Required packages (auto-installed if not found):
- `psutil`
- `requests`

---

## 🛠️ Usage

### 💻 Run a Script
If you dont have the interpreter installed on PATH:
```bash
python "C:/.../minteclipse.py" "-f" "script.x3"
```
If you do have the interpreter installed on PATH (you can use our **[installer](https://github.com/XFydro/x3/releases/tag/installer1.5)** for that :3 )
```bash
x3 -f "./script.x3"
```
