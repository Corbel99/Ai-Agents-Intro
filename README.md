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

_Coming soon._

## Reflection

_Coming soon._

## Author

Thomas
