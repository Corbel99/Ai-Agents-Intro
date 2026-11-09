#!/usr/bin/env python3
"""Entry point of the AI Study Guide Generator."""
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.explainer_agent import explainer_agent
from agents.practice_designer_agent import practice_designer_agent
from agents.reviewer_agent import reviewer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections


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


async def main():
    """Generate a study guide for one topic, save it and validate it."""
    topic = "Python decorators"

    # Agent 1 : il reçoit le sujet et renvoie l'explication
    explanation = await run_agent(explainer_agent, topic)

    # Agent 2 : il reçoit le sujet ET l'explication, et renvoie l'exercice
    exercise = await run_agent(
        practice_designer_agent,
        f"Topic: {topic}\n\nExplanation:\n{explanation}",
    )

    # On colle les deux réponses pour former le brouillon de la fiche
    study_guide = explanation + "\n\n" + exercise

    # Agent 3 : il relit le brouillon complet et renvoie ses commentaires
    review = await run_agent(reviewer_agent, study_guide)
    print("REVIEW:", review)

    # On ajoute les commentaires à la fin de la fiche
    study_guide = study_guide + "\n\n" + review

    # On enregistre la fiche, puis on la vérifie
    result = save_markdown_file("output/study_guide.md", study_guide)
    print(result)

    validation = validate_required_sections(study_guide)
    print(validation)

# On lance main() seulement si on exécute ce fichier directement
if __name__ == "__main__":
    asyncio.run(main())
