# AI Agents in Python

🇫🇷 Version française : [README.fr.md](README.fr.md)

## Description

**AI Study Guide Generator** is a small multi-agent system built with Python,
Google ADK, LiteLLM and Ollama.

It receives a programming topic, such as `Python decorators`, and generates a
Markdown study guide with an explanation, key concepts, an example, a practice
exercise, common mistakes, review comments and a final summary.

The system follows one simple principle: **the AI writes, the code checks and
saves**. Three agents generate the content, and two deterministic Python tools
validate and save it.

## Requirements

- **Operating system**: Ubuntu (developed on Ubuntu under WSL, Windows)
- **Python**: 3.12
- **Ollama**: to run the model locally
- **Model**: `llama3.2` (about 2 GB on disk), a small model that supports tools
- **Hardware**: no GPU required. The project was developed on CPU only, as no
  GPU was available under WSL.
- **Python libraries**: listed in `requirements.txt`

| Component | Role |
|---|---|
| **Google ADK** | Python library used to create and run the agents |
| **LiteLLM** | Connector that sends the agents' requests to the model provider |
| **Ollama** | Program that runs the model locally, on `http://localhost:11434` |
| **llama3.2** | Small local language model that generates the text |

```text
Google ADK  →  LiteLLM  →  Ollama  →  llama3.2
```

No API key and no paid account are needed.

## Setup

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

`tools` must appear under **Capabilities**.

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

## Configuration

The settings are stored in a `.env` file, read by `config.py` at startup.
Create it from the example file:

```bash
cp .env.example .env
```

| Variable | Description | Example |
|---|---|---|
| `OLLAMA_API_BASE` | Address of the local Ollama server | `http://localhost:11434` |
| `MODEL_NAME` | Model used by LiteLLM (`ollama_chat/` + model name) | `ollama_chat/llama3.2` |

To use another model, pull it with Ollama and change `MODEL_NAME`: the code
does not need to change.

The real `.env` file stays local: it is listed in `.gitignore` and must never
be committed.

## How to Run

Make sure Ollama is running and the virtual environment is activated, then:

```bash
./main.py
```

Enter a topic when asked. The program shows its progress:

```text
Enter a programming topic: Python decorators
[1/5] Explainer agent is working...
[2/5] Practice designer agent is working...
[3/5] Reviewer agent is working...
[4/5] Validating the study guide...
All required sections are present.
[5/5] Saving the study guide...
Study guide saved to output/study_guide.md
```

The study guide is saved in `output/study_guide.md`.

## Example Input

```text
Python decorators
```

## Example Output

Shortened excerpt of `output/study_guide.md`:

````markdown
# Topic: Python decorators

## Simple Explanation
Python decorators are a powerful feature that allows programmers to modify or
extend the behavior of a function without permanently changing it.

## Key Concepts
* **Decorators**: a function that takes another function as an argument and
  returns a new function that "wraps" the original function.
* **Decorator syntax**: `@decorator_name`, equivalent to
  `decorator_name(func)`.

## Example
```python
def my_decorator(func):
    def wrapper():
        print("Before the function is executed")
        func()
        print("After the function is executed")
    return wrapper

@my_decorator
def say_hello():
    print("Hello, world!")
```

## Practice Exercise
Create a decorator that prints a message before and after the execution of a
`greet(name)` function. ...

## Common Mistakes
...

## Review Comments
...

## Final Summary
...
````

## Project Structure

```text
ai-agents-intro/
├── agents/
│   ├── explainer_agent.py          # Explains the topic
│   ├── practice_designer_agent.py  # Creates the exercise and common mistakes
│   └── reviewer_agent.py           # Reviews the draft and summarizes it
├── tools/
│   ├── file_writer.py              # Saves the Markdown file
│   └── validation.py               # Checks the required sections
├── output/
│   └── study_guide.md              # Generated study guide
├── data/
│   └── topic_examples.json         # Example topics
├── config.py                       # Loads and checks the .env settings
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md                       # Documentation in English
├── README.fr.md                    # Documentation in French
└── main.py                         # Runs the full workflow
```

## Agents

All agents use the same model (`llama3.2`), with a different role and
different instructions.

| Agent | Input | Output (Markdown headings) |
|---|---|---|
| **Explainer** | The topic | `Simple Explanation`, `Key Concepts`, `Example` |
| **Practice Designer** | The topic and the explanation | `Practice Exercise`, `Common Mistakes` |
| **Reviewer** | The full draft | `Review Comments`, `Final Summary` |

The workflow is sequential: each agent uses the result of the previous one.

```text
Topic → Explainer → Practice Designer → Draft → Reviewer
      → Final Markdown → Validation → Save
```

## Tools

The tools are regular, **deterministic** Python functions: the same input
always gives the same result. They do not use the model.

| Tool | File | Role |
|---|---|---|
| `save_markdown_file()` | `tools/file_writer.py` | Creates the parent directory if needed, writes the Markdown file and returns its path, or a clear `Error:` message. |
| `validate_required_sections()` | `tools/validation.py` | Checks that the 8 required headings are present and returns `{"valid": ..., "missing": [...]}`. |

## Self-Validation Checklist

- [x] **Task 0**: project structure created (`agents/`, `tools/`, `output/`,
  `data/`, `README.md`, `requirements.txt`, `.env.example`, `.gitignore`,
  `main.py`).
- [x] **Task 1**: virtual environment, dependencies, Ollama and `llama3.2`
  installed; the model answers locally.
- [x] **Task 2**: explainer agent with a clear role and specific instructions,
  tested with `Python decorators` and `HTTP status codes`.
- [x] **Task 3**: `save_markdown_file()` tested alone, then used to save the
  output in `output/`.
- [x] **Task 4**: `validate_required_sections()` returns the validation status
  and the missing sections.
- [x] **Task 5**: practice designer agent based on the topic and explanation.
- [x] **Task 6**: reviewer agent that comments without rewriting the guide.
- [x] **Task 7**: sequential workflow producing a complete study guide with the
  8 required sections.
- [x] **Task 8**: clear errors for missing variables, Ollama not running,
  model not available, empty topic, file-writing errors and validation
  failure.
- [x] **Task 9**: README completed with the reflection and known limitations.

## Reflection

**1. What is the difference between a direct LLM call and an AI agent?**

With a direct call, you ask the model a question and it answers, without any
specific role. An agent is the model configured by me: I give it a role and
precise instructions (and possibly tools), so that it always does the same
type of work in the same way. In short: the model is the brain; the agent is
the brain plus a job description plus tools.

**2. What role does each agent have in your system?**

The first agent answers with an explanation of the requested topic. The second
one creates an exercise on the same topic, with the common mistakes beginners
make. The last one reviews the two previous answers (the draft), gives a
recommendation (approve or revise) and writes the final summary.

**3. What role does each tool have in your system?**

The first tool saves the agents' answers directly in a Markdown file. The
second one checks that the generated study guide contains all the predefined
sections. Unlike the model, these tools are deterministic: the AI writes, the
code checks and saves.

**4. What was the most difficult part of the project?**

The most difficult part was checking Ollama and the model (task 8): the code
uses notions that were new to me, such as HTTP requests. More generally, the
project introduces many new tools at once (ADK, LiteLLM, Ollama), and putting
all the steps together end to end requires keeping a lot of things in mind.

**5. What limitation did you observe when using your selected model?**

Mainly the response time: since Ollama runs on the CPU (no GPU available under
WSL), each agent takes a while to answer, and the full workflow of three
agents takes about **45 seconds**.

## Known Limitations

- **Speed**: on CPU only, a full run takes about 45 seconds.
- **Hallucinations**: the small model sometimes invents details. During the
  tests, it described "Before / After / Surround decorators" as categories of
  decorators (they are not), and presented context managers as a type of
  decorator (they are a different concept).
- **Non-deterministic output**: the same topic does not always give the same
  answer. A run can produce an empty answer or miss a section, and running it
  again can fix it.
- **Inconsistent formatting**: the model does not always follow the requested
  heading level (for example `### Example` instead of `## Example`). The
  validator accepts both levels for this reason.
- **Exercise solutions**: the practice designer sometimes gives the full
  solution code along with the exercise.
- **Structural validation only**: the validator checks that the headings
  exist, not that the content is correct or useful.
- **Prompts in English**: the instructions and headings are in English; a
  topic or instructions in another language may break the validation.

## Troubleshooting

| Problem | Message | Solution |
|---|---|---|
| `.env` file missing or incomplete | `RuntimeError: Missing environment variable: OLLAMA_API_BASE` | Run `cp .env.example .env` and check the values. |
| Ollama is not running | `RuntimeError: Ollama is not reachable at http://localhost:11434` | Start it with `ollama serve` (or `sudo systemctl start ollama`). |
| Model not downloaded | `RuntimeError: Model 'llama3.2' is not available` | Run `ollama pull llama3.2`. |
| Empty topic | `ValueError: Topic cannot be empty.` | Type a topic, for example `Python decorators`. |
| File cannot be written | `Error: could not save output/study_guide.md: ...` | Check that the `output/` directory is writable. |
| Missing sections | `Warning: missing sections: ...` | The local model is not deterministic: run the project again. |

When an error occurs, read the **last line** of the traceback: it contains
the explanation.

## Author

Thomas
