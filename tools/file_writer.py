#!/usr/bin/env python3
"""Deterministic tool: saves Markdown content to a file."""


from pathlib import Path

def save_markdown_file(file_path: str, content: str) -> str:
    """Save Markdown content to a file and return the saved path."""
    # On transforme le texte du chemin en objet Path
    path = Path(file_path)

    try:
        # On crée le dossier parent (ex : output/) s'il n'existe pas
        path.parent.mkdir(parents=True, exist_ok=True)

        # On écrit le contenu Markdown dans le fichier
        path.write_text(content, encoding="utf-8")
    except OSError as error:
        # Si l'écriture échoue, on renvoie un message clair au lieu de planter
        return f"Error: could not save {path}: {error}"

    # On renvoie le chemin du fichier, converti en texte
    return str(path)
