#!/usr/bin/env python3
"""Deterministic tool: validates the study guide sections."""
REQUIRED_SECTIONS = [
    "Topic",
    "Simple Explanation",
    "Key Concepts",
    "Example",
    "Practice Exercise",
    "Common Mistakes",
    "Review Comments",
    "Final Summary",
]


def validate_required_sections(markdown: str) -> dict:
    """Check that every required section heading is in the Markdown."""
    missing = []

    # Pour chaque section obligatoire, on cherche son titre Markdown
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in markdown:
            missing.append(section)

    # Le contenu est valide seulement s'il ne manque aucune section
    return {"valid": len(missing) == 0, "missing": missing}
