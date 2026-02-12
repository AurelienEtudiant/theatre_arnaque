"""
Module des outils (Tools) pour les agents.

Ce module expose les outils disponibles pour les agents LLM.
"""

from tools.audio_tools import (
    get_audio_tools,
    play_dog_bark,
    play_doorbell,
    play_coughing_fit,
    play_tv_background,
    play_phone_static,
    play_kettle_whistle
)

__all__ = [
    "get_audio_tools",
    "play_dog_bark",
    "play_doorbell",
    "play_coughing_fit",
    "play_tv_background",
    "play_phone_static",
    "play_kettle_whistle"
]

