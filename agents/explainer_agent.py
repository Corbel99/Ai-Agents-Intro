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
        "Answer in Markdown with exactly these headings, in this order: "
        "## Topic, ## Simple Explanation, ## Key Concepts, ## Example. "
        "Under Key Concepts, write a bulleted list."
    ),
)
