#!/usr/bin/env python3
"""Explainer agent: explains a programming topic."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from config import MODEL_NAME


explainer_agent = Agent(
    name="explainer_agent",
    model=LiteLlm(model=MODEL_NAME),
    instruction=(
        "You are a programming expert who explains concepts "
        "to beginner students. "
        "You receive a programming topic. "
        "Answer in Markdown with exactly these headings, in this order: "
        "## Simple Explanation, ## Key Concepts, ## Example. "
        "Under Key Concepts, write a bulleted list."
    ),
)
