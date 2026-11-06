#!/usr/bin/env python3
"""Entry point of the AI Study Guide Generator."""
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.explainer_agent import explainer_agent


async def main():
    """Run the explainer agent on one topic and print its answer."""
    # Le sujet à expliquer
    topic = "Python decorators"

    # Pièce 1 : on crée le carnet, puis on y ouvre une page (la session)
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="study_guide_app",
        user_id="Thomas",
    )

    # Pièce 2 : le chef d'équipe qui transmet le travail à l'agent
    runner = Runner(
        agent=explainer_agent,
        app_name="study_guide_app",
        session_service=session_service,
    )

    # Pièce 3 : on met le sujet dans l'enveloppe (Content)
    # avec une seule feuille (Part) qui contient le texte
    message = types.Content(
        role="user",
        parts=[types.Part(text=topic)],
    )

    # Pièce 4 : l'agent travaille et renvoie des événements un par un ;
    # on n'affiche que le dernier, la réponse finale
    async for event in runner.run_async(
        user_id="Thomas",
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response():
            # On ouvre l'enveloppe, on prend la 1re feuille, on lit le texte
            print(event.content.parts[0].text)


# On lance main() seulement si on exécute ce fichier directement
if __name__ == "__main__":
    asyncio.run(main())
