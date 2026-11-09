#!/usr/bin/env python3
"""Entry point of the AI Study Guide Generator."""
import json
import urllib.request
from urllib.error import URLError
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.explainer_agent import explainer_agent
from agents.practice_designer_agent import practice_designer_agent
from agents.reviewer_agent import reviewer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections
from config import MODEL_NAME, OLLAMA_API_BASE

def get_topic_from_user() -> str:
    """Ask the user for a topic, with a default value."""
    topic = input("Enter a programming topic: ").strip()
    # Si l'utilisateur ne tape rien, on prend un sujet par défaut
    if not topic:
        topic = "Python decorators"
    return topic


async def run_agent(agent, text: str) -> str:
    """Run one agent on a text and return its final answer."""
    # Pièce 1 : le carnet et une nouvelle page pour cet agent
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="study_guide_app",
        user_id="Thomas",
    )

    # Pièce 2 : le chef d'équipe, pour l'agent reçu en paramètre
    runner = Runner(
        agent=agent,
        app_name="study_guide_app",
        session_service=session_service,
    )

    # Pièce 3 : le texte reçu, mis dans l'enveloppe
    message = types.Content(
        role="user",
        parts=[types.Part(text=text)],
    )

    # Pièce 4 : on garde la réponse finale de l'agent
    answer = ""
    async for event in runner.run_async(
        user_id="Thomas",
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response():
            answer = event.content.parts[0].text

    return answer


def assemble_markdown(topic: str, explanation: str, practice: str) -> str:
    """Build the draft study guide."""
    # Le grand titre, puis l'explication et l'exercice
    return f"# Topic: {topic}\n\n{explanation}\n\n{practice}"


def assemble_final_markdown(draft: str, review: str) -> str:
    """Add the review to the draft to build the final study guide."""
    return f"{draft}\n\n{review}\n"


def check_ollama() -> None:
    """Check that Ollama is running and that the model is available."""
    # On demande à Ollama la liste des modèles téléchargés
    try:
        url = f"{OLLAMA_API_BASE}/api/tags"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.load(response)
    except (URLError, TimeoutError) as error:
        # Pas de réponse : Ollama est éteint ou l'adresse est fausse
        raise RuntimeError(
            f"Ollama is not reachable at {OLLAMA_API_BASE}. "
            "Start it with: ollama serve"
        ) from error

    # "ollama_chat/llama3.2" devient "llama3.2"
    model = MODEL_NAME.split("/")[-1]
    names = [item["name"] for item in data.get("models", [])]

    # Ollama range les modèles sous la forme "llama3.2:latest"
    if model not in names and f"{model}:latest" not in names:
        raise RuntimeError(
            f"Model '{model}' is not available. "
            f"Download it with: ollama pull {model}"
        )


async def main():
    """Run the full workflow: agents, assembly, validation, saving."""
        # On vérifie Ollama et le modèle avant de lancer quoi que ce soit
    check_ollama()
    topic = get_topic_from_user()

    # Agent 1 : il reçoit le sujet et renvoie l'explication
    print("[1/5] Explainer agent is working...")
    explanation = await run_agent(explainer_agent, topic)

    # Agent 2 : il reçoit le sujet ET l'explication, et renvoie l'exercice
    print("[2/5] Practice designer agent is working...")
    practice = await run_agent(
        practice_designer_agent,
        f"Create a practice exercise for this topic: {topic}\n\n"
        f"Here is the explanation:\n{explanation}",
    )

    # On assemble le brouillon
    draft = assemble_markdown(topic, explanation, practice)

    # Agent 3 : il relit le brouillon complet
    print("[3/5] Reviewer agent is working...")
    review = await run_agent(
        reviewer_agent,
        f"Review this draft study guide:\n\n{draft}",
    )

    # On assemble la fiche finale
    final_markdown = assemble_final_markdown(draft, review)

    # On valide AVANT d'enregistrer, et on affiche ce qui manque
    print("[4/5] Validating the study guide...")
    validation = validate_required_sections(final_markdown)
    if validation["valid"]:
        print("All required sections are present.")
    else:
        # La fiche est quand même enregistrée, mais on prévient l'utilisateur
        print("Warning: missing sections:", ", ".join(validation["missing"]))
        print("The local model may be inconsistent: try running again.")

    # On enregistre la fiche
    print("[5/5] Saving the study guide...")
    result = save_markdown_file("output/study_guide.md", final_markdown)

    # L'outil renvoie un message qui commence par "Error:" s'il a échoué
    if result.startswith("Error:"):
        print(result)
        print("Check that the output/ directory is writable.")
    else:
        print(f"Study guide saved to {result}")


# On lance main() seulement si on exécute ce fichier directement
if __name__ == "__main__":
    asyncio.run(main())
