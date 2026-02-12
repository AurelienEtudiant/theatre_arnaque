"""
Module des agents LLM pour le Théâtre de l'Arnaque.

Ce module contient les trois agents principaux :
- VictimAgent : Mme Jeanne Dubois, la victime
- DirectorAgent : Le superviseur silencieux
- ModeratorAgent : Le gestionnaire de l'audience

Chaque agent utilise LangChain pour l'orchestration.
"""

from agents.victim_agent import VictimAgent
from agents.director_agent import DirectorAgent
from agents.moderator_agent import ModeratorAgent

__all__ = [
    "VictimAgent",
    "DirectorAgent",
    "ModeratorAgent"
]

