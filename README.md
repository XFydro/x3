# 🌑 MintEclipse Interpreter

> *"The only bug-free zone is your imagination. Good luck."*  
> **Current Version:** `3.9` | **Project Phase:** Active development

---

## 🎮 What is MintEclipse?

**MintEclipse** is a custom-built interpreter designed for **X3-based scripting**, infused with enhanced control flow, dynamic variables, expression parsing, function definitions, and rich debugging capabilities.  
It’s **modular, powerful, expressive**, and still evolving with each chaotic burst of passion. :3

Built by **[Raven (formally known as XFydro)](https://x3documentation.neocities.org/developer)** with passion and 💖.

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
- Terminal that supports ANSI colors (optional but ✨ pretty ✨)
- Patience... Python is slow af 🐌💤

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
If you do have the interpreter installed on PATH (you can use our **[installer](https://github.com/XFydro/x3/blob/installer1.2/interpreter.py)** for that :3 )
```bash
x3 -f "./script.x3"
```
