#!/usr/bin/env python3
"""Load and check the project configuration from the .env file."""
import os

from dotenv import load_dotenv

# On charge les variables du fichier .env dans l'environnement
load_dotenv()


def get_setting(name: str) -> str:
    """Return a required environment variable or raise a clear error."""
    value = os.getenv(name)
    # Si la variable est absente ou vide, on explique quoi faire
    if not value:
        raise RuntimeError(
            f"Missing environment variable: {name}. "
            "Copy .env.example to .env and fill in the values."
        )
    return value


# Les deux réglages du projet, vérifiés dès le démarrage
OLLAMA_API_BASE = get_setting("OLLAMA_API_BASE")
MODEL_NAME = get_setting("MODEL_NAME")
