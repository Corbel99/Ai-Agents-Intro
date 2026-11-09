#!/usr/bin/env python3
"""Reviewer agent: reviews the generated study guide."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from config import MODEL_NAME


reviewer_agent = Agent(
    name="reviewer_agent",
    model=LiteLlm(model=MODEL_NAME),
    instruction=(
        "You are a reviewer agent. "
        "You receive a draft study guide. "
        "Review it for clarity, completeness and usefulness. "
        "Do not rewrite the guide. "
        "Answer in Markdown under the heading ## Review Comments, with: "
        "missing information, unclear parts, short and specific "
        "suggestions, and a final recommendation: approve or revise. "
        "Then add the heading ## Final Summary, with a summary of the "
        "guide in two or three sentences."
    ),
)
