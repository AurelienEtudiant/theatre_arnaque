"""
Module des prompts système pour les agents.
"""

from prompts.victim_prompt import get_victim_system_prompt
from prompts.director_prompt import get_director_system_prompt
from prompts.moderator_prompt import get_moderator_system_prompt
from prompts.scenarios import get_scenario_script, SCENARIOS

__all__ = [
    "get_victim_system_prompt",
    "get_director_system_prompt",
    "get_moderator_system_prompt",
    "get_scenario_script",
    "SCENARIOS"
]

