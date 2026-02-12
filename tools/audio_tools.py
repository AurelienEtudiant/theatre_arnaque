from typing import List
from langchain.tools import tool, StructuredTool
from langchain_core.tools import BaseTool

@tool
def play_dog_bark() -> str:
    """
    Joue un aboiement de chien (Poupoune).

    Utilisez cet outil quand :
    - L'interlocuteur devient pressant ou agressif
    - Jeanne a besoin d'une excuse pour faire une pause
    - La situation devient tendue

    Le chien Poupoune est un petit yorkshire très protecteur
    qui n'aime pas quand sa maîtresse est stressée.

    Returns:
        str: Indicateur d'effet sonore à afficher
    """
    return "[🔊 SOUND_EFFECT: DOG_BARKING - Poupoune aboie fort]"


@tool
def play_doorbell() -> str:
    """
    Joue le son de la sonnette de la porte.

    Utilisez cet outil quand :
    - Jeanne a besoin de s'éloigner du téléphone
    - On veut faire attendre l'arnaqueur
    - L'audience a voté pour "quelqu'un sonne à la porte"

    La sonnette de Jeanne joue une mélodie de Big Ben.

    Returns:
        str: Indicateur d'effet sonore à afficher
    """
    return "[🔊 SOUND_EFFECT: DOORBELL - Ding dong ! La sonnette retentit]"


@tool
def play_coughing_fit() -> str:
    """
    Simule une quinte de toux de la vieille dame.

    Utilisez cet outil quand :
    - Jeanne veut gagner du temps
    - Elle est "submergée par l'émotion"
    - Elle a besoin d'une pause naturelle

    Jeanne a 78 ans et tousse souvent, surtout quand elle parle longtemps.

    Returns:
        str: Indicateur d'effet sonore à afficher
    """
    return "[🔊 SOUND_EFFECT: COUGHING - Jeanne tousse pendant 10 secondes]"


@tool
def play_tv_background() -> str:
    """
    Augmente le volume de la télévision en arrière-plan.

    Utilisez cet outil quand :
    - Jeanne veut faire répéter l'arnaqueur
    - Elle a besoin d'une excuse pour ne pas entendre
    - On veut ajouter du réalisme à la scène

    Jeanne regarde "Les Feux de l'Amour" tous les après-midis.

    Returns:
        str: Indicateur d'effet sonore à afficher
    """
    return "[🔊 SOUND_EFFECT: TV_BACKGROUND - Les Feux de l'Amour en fond sonore]"


@tool
def play_phone_static() -> str:
    """
    Simule des grésillements sur la ligne téléphonique.

    Utilisez cet outil quand :
    - Jeanne veut prétendre qu'elle entend mal
    - On veut créer de la confusion
    - L'arnaqueur dit quelque chose de compromettant

    Le vieux téléphone fixe de Jeanne a souvent des problèmes de ligne.

    Returns:
        str: Indicateur d'effet sonore à afficher
    """
    return "[🔊 SOUND_EFFECT: PHONE_STATIC - Grésillement sur la ligne]"


@tool
def play_kettle_whistle() -> str:
    """
    Joue le sifflement d'une bouilloire.

    Utilisez cet outil quand :
    - Jeanne doit "aller vérifier quelque chose"
    - On veut une pause naturelle dans la conversation
    - L'audience a voté pour un événement cuisine

    Jeanne boit beaucoup de thé et sa bouilloire siffle très fort.

    Returns:
        str: Indicateur d'effet sonore à afficher
    """
    return "[🔊 SOUND_EFFECT: KETTLE_WHISTLE - La bouilloire siffle !]"


# ============================================
# FONCTION D'EXPORT DES OUTILS
# ============================================

def get_audio_tools() -> List[BaseTool]:
    """
    Retourne la liste de tous les outils audio disponibles.

    Cette fonction est utilisée par l'Agent Victime pour
    configurer les outils disponibles dans l'AgentExecutor.

    Returns:
        List[BaseTool]: Liste des outils audio

    Exemple:
        >>> tools = get_audio_tools()
        >>> print([t.name for t in tools])
        ['play_dog_bark', 'play_doorbell', 'play_coughing_fit', ...]
    """
    return [
        play_dog_bark,
        play_doorbell,
        play_coughing_fit,
        play_tv_background,
        play_phone_static,
        play_kettle_whistle
    ]


# ============================================
# SIMULATEUR D'EFFETS SONORES (OPTIONNEL)
# ============================================

class AudioSimulator:
    """
    Classe optionnelle pour simuler la lecture réelle des sons.

    Dans une version complète, cette classe utiliserait pygame
    ou un autre module audio pour vraiment jouer les sons.

    Pour l'instant, elle affiche juste un texte formaté.
    """

    # Mapping des effets vers des descriptions
    EFFECTS = {
        "DOG_BARKING": "🐕 *Wouaf! Wouaf! Wouaf!*",
        "DOORBELL": "🔔 *Ding dong!*",
        "COUGHING": "🤧 *Kof kof kof... excusez-moi...*",
        "TV_BACKGROUND": "📺 *musique dramatique de soap opera*",
        "PHONE_STATIC": "📞 *Crrrr... chhhhh...*",
        "KETTLE_WHISTLE": "🫖 *SIIIIIFFLEMENT*"
    }

    @classmethod
    def render_effect(cls, effect_marker: str) -> str:
        """
        Transforme un marqueur d'effet en texte formaté.

        Args:
            effect_marker: Le marqueur retourné par un outil

        Returns:
            str: Texte formaté avec émoji et description
        """
        for key, value in cls.EFFECTS.items():
            if key in effect_marker:
                return f"\n{value}\n"
        return effect_marker

    @classmethod
    def extract_effects(cls, response: str) -> List[str]:
        """
        Extrait tous les effets sonores d'une réponse.

        Args:
            response: La réponse complète de l'agent

        Returns:
            List[str]: Liste des effets trouvés
        """
        effects = []
        for key in cls.EFFECTS.keys():
            if key in response:
                effects.append(key)
        return effects


# ============================================
# DOCUMENTATION SUPPLÉMENTAIRE
# ============================================
"""
COMMENT LE LLM UTILISE LES OUTILS :

1. Le LLM reçoit le message de l'arnaqueur
2. Il lit les descriptions des outils disponibles
3. Il décide si un outil est approprié pour la situation
4. Si oui, il appelle le tool avec les arguments requis
5. Il reçoit le résultat (le marqueur sonore)
6. Il intègre ce résultat dans sa réponse finale

EXEMPLE DE FLUX :

Arnaqueur: "Donnez-moi votre mot de passe MAINTENANT!"

LLM pense: "L'arnaqueur est agressif, je vais utiliser le chien"

LLM appelle: play_dog_bark()

LLM reçoit: "[🔊 SOUND_EFFECT: DOG_BARKING]"

LLM répond: "Oh mon dieu... Attendez ! POUPOUNE !
            [🔊 SOUND_EFFECT: DOG_BARKING]
            Arrête d'aboyer ma chérie ! Excusez-moi monsieur,
            mon chien n'aime pas quand on crie au téléphone..."

C'est cette capacité à utiliser des outils qui rend l'interaction
plus réaliste et impr��visible pour l'arnaqueur.
"""

