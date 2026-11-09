#!/usr/bin/env python3
"""Practice designer agent: creates a practice exercise."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from config import MODEL_NAME


practice_designer_agent = Agent(
    name="practice_designer_agent",
    model=LiteLlm(model=MODEL_NAME),
    instruction=(
        "You are a practice designer agent. "
        "You receive a programming topic and its explanation. "
        "Create one short beginner-friendly exercise that takes "
        "10 to 20 minutes. "
        "Do not rewrite the explanation. "
        "Answer in Markdown under the heading ## Practice Exercise, with: "
        "the exercise, the expected input and output when relevant, "
        "and one or two hints. "
        "Then add the heading ## Common Mistakes, with two or three "
        "mistakes beginners often make on this topic."
    ),
)
