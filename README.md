# 🤖 Coding-Assistant-Agent

A lightweight, agentic coding assistant powered by **Gemini 2.5 Flash** that can read, write, and execute code inside a sandboxed working directory — all from a single terminal command.

```
$ python main.py "Fix the bug in calculator.py and run the tests"

 → Calling: get_files_info
 → Calling: get_file_content
 → Calling: write_file
 → Calling: run_python_file

All tests passed. Fixed an off-by-one error in the division handler on line 42.
```

---

## How it works

The agent runs a tool-use loop: it receives your prompt, decides which tools to call, gets the results, and repeats — until it has enough context to give you a final answer. It operates entirely within a sandboxed `working_directory` you configure, so it can never read or write files outside that folder.

```
your prompt
    │
    ▼
┌─────────────────────────────┐
│        Gemini 2.5 Flash     │
│   (function calling mode)   │
└────────────┬────────────────┘
             │ tool calls
    ┌─────────▼──────────┐
    │   Tool Dispatcher  │
    └──┬──────┬──────┬───┘
       │      │      │
  get_ │ write│  run │
  files│ _file│ _py  │
       │      │      │
    └──┴──────┴──────┘
         working_directory/
              (sandboxed)
```

---

## Features

- **Read** — list directories and read file contents (truncated at 10,000 chars)
- **Write** — create or overwrite files, with automatic directory creation
- **Execute** — run Python scripts with optional CLI arguments, with a 30-second timeout
- **Safe** — all file operations are path-checked against the working directory; escapes are blocked
- **Verbose mode** — inspect token counts and raw function call arguments per iteration

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/your-username/coding-assistant-agent.git
cd gemini-dev-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**
```bash
cp .env.example .env
# then edit .env and paste your Gemini API key
```

Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com).

**4. Set your working directory**

Open `functions/call_function.py` and set `working_directory` to the folder you want the agent to operate in:
```python
working_directory = "calculator"  # ← change this
```

---

## Usage

```bash
# Basic prompt
python main.py "What files are in the project?"

# Ask it to write and run code
python main.py "Write a Python script that prints the first 10 Fibonacci numbers and run it"

# Verbose mode (shows token counts + raw function args)
python main.py "Summarize the main.py file" --verbose
```

---

## Project structure

```
coding-assistant-agent/
├── main.py                  # Entry point — agent loop
├── config.py                # Shared constants (MAX_CHARS, etc.)
├── requirements.txt
├── .env.example
└── functions/
    ├── __init__.py
    ├── call_function.py     # Tool dispatcher
    ├── get_files_info.py    # List directory contents
    ├── get_files_content.py # Read file contents
    ├── write_file.py        # Write / create files
    └── run_python_file.py   # Execute Python scripts
```

---

## Configuration

| Constant | File | Default | Description |
|---|---|---|---|
| `working_directory` | `functions/call_function.py` | `"calculator"` | Sandboxed root for all file operations |
| `MAX_CHARS` | `config.py` | `10000` | Max characters read per file |
| `max_iters` | `main.py` | `20` | Max tool-call iterations per prompt |

---
