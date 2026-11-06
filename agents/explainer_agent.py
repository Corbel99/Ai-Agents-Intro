#!/usr/bin/env python3
"""Explainer agent: explains a programming topic."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


explainer_agent = Agent(
    name="explainer_agent",
    model=LiteLlm(model="ollama_chat/llama3.2"),
    instruction=(
        "You are a programming expert who explains concepts "
        "to beginner students. "
        "You receive a programming topic. "
        "Answer in Markdown with three parts, in this order: "
        "a short explanation, a list of key concepts, "
        "and one simple example."
    ),
)
