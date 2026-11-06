# AI Agents in Python: AI Study Guide Generator

A small multi-agent system built with Python, Google ADK, LiteLLM and Ollama.
It receives a programming topic and generates a Markdown study guide.

## Project structure

```
ai-agents-intro/
├── agents/     # AI agents (explainer, practice designer, reviewer)
├── tools/      # Deterministic Python tools (file writer, validation)
├── output/     # Generated study guides
├── data/       # Example topics
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── main.py
```

## Model provider

This project runs a **local model** with **Ollama**. No API key and no paid
account are needed.

| Component | Role |
|---|---|
| **Google ADK** | Python library used to create and run the agents |
| **LiteLLM** | Connector that sends the agents' requests to the model provider |
| **Ollama** | Program that runs the model locally, on `http://localhost:11434` |
| **llama3.2** | Small local language model that supports tools |

```text
Google ADK  →  LiteLLM  →  Ollama  →  llama3.2
```

## Setup

The project was developed on **Ubuntu (WSL)**.

### 1. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama -v
```

If Ollama is not running in the background, start it in a separate terminal:

```bash
ollama serve
```

### 2. Pull and test the model

```bash
ollama pull llama3.2
ollama show llama3.2
```

`tools` must appear under **Capabilities**: the agents need a model that can
call tools.

Test that the model answers locally:

```bash
ollama run llama3.2
```

Type a short question, then `/bye` to quit.

### 3. Create and activate a virtual environment

```bash
python3 -m venv venv --prompt ai-agents
source venv/bin/activate
```

### 4. Install the Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the environment variables

```bash
cp .env.example .env
```

| Variable | Description | Example |
|---|---|---|
| `OLLAMA_API_BASE` | Address of the local Ollama server | `http://localhost:11434` |
| `MODEL_NAME` | Model used by LiteLLM (`ollama_chat/` + model name) | `ollama_chat/llama3.2` |

The real `.env` file stays local: it is listed in `.gitignore` and must never
be committed.

## Usage

Make sure Ollama is running, activate the virtual environment, then run:

```bash
python3 main.py
```

### Example output

Topic: `Python decorators`

**Explanation**
================

Python decorators are a powerful feature that allows programmers to modify or extend the behavior of functions without permanently modifying them. A decorator is a small function that takes another function as an argument and returns a new function that "wraps" the original function. This new function, also known as the "decorator function", can then be applied to any function to modify its behavior.

**Key Concepts**
---------------

*   A decorator is a function that takes another function as an argument.
*   A decorator function returns a new function that wraps the original function.
*   Decorators are often used to:
    *   Add functionality to existing functions without modifying them.
    *   Create logging or authentication mechanisms for functions.
    *   Implement aspect-oriented programming (AOP) concepts.
*   Decorators are typically denoted by the `@` symbol before the decorator function name.
*   There are two types of decorators:
    *   **Simple decorators**: These are functions that take a function as an argument and return a new function.
    *   **Class decorators**: These are functions that take a class as an argument and return a new class.

**Example**
------------

```python
# Simple decorator example

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

Output:
```
Something is happening before the function is called.
Hello!
Something is happening after the function is called.
```

In this example, `my_decorator` is a simple decorator function that takes `say_hello` as an argument and returns a new function `wrapper`. The `wrapper` function calls `say_hello` inside it and adds some extra functionality. When `say_hello` is called, it's actually the `wrapper` function that's called, which executes the original `say_hello` function and then adds its own functionality.

## Reflection

_Coming soon._

## Author

Thomas
