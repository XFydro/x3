# 🌑 MintEclipse Interpreter

> *"An expressive, extensible, emotionally charged scripting interpreter born from chaos and creativity."*  
> **Current Version:** `3.92` | **Project Phase:** Active development

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
- 📦 **Additional Parameters** like `##random`, `##timestamp`, `##fetch:url`, `##env:PATH`
- 🔐 **Safe Execution Modes** (`SEMO(Script Execution Mode Only)`, REPL toggle, and debug toggles(dev.debug))
- 📚 **Script Loader** with error isolation, step-by-step tracking, and layered debug levels
- 🎨 **ANSI Color Dictionary** for styled console outputs (doesnt works as expected)
- 💥 **Fastmath Rule** for raw math execution (`fastmath x = (a * b) + 5`)
- 📜 **Function Blocks** (`def`, `fncend`, `call`)
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
```bash
python "minteclipse.py" "-f" "script.x3"
