import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

class LLMConfig:
    """
    Configuration des modèles de langage.

    Cette classe centralise tous les paramètres liés aux LLMs :
    - Clé API OpenAI ou Google (Gemini)
    - Modèle à utiliser
    - Paramètres de génération (température, tokens max, etc.)

    PROVIDERS SUPPORTÉS:
    - openai: GPT-3.5, GPT-4
    - gemini: Gemini 1.5 Flash, Gemini 1.5 Pro, Gemini 2.0
    """

    # Provider LLM - CHARGÉ DEPUIS L'ENVIRONNEMENT
    # Options: "openai", "gemini"
    PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")

    # Clé API OpenAI - CHARGÉE DEPUIS L'ENVIRONNEMENT
    # JAMAIS codée en dur dans le code !
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Clé API Google (Gemini) - CHARGÉE DEPUIS L'ENVIRONNEMENT
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    # URL de base pour Ollama (si utilisation locale)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Modèle par défaut
    # OpenAI: gpt-4, gpt-3.5-turbo, gpt-4-turbo
    # Gemini: gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash
    DEFAULT_MODEL: str = os.getenv("LLM_MODEL", "gemini-2.0-flash")

    # Paramètres de génération
    TEMPERATURE: float = 0.7  # Créativité (0=déterministe, 1=créatif)
    MAX_TOKENS: int = 500     # Longueur max des réponses

    @classmethod
    def validate(cls) -> bool:
        """
        Vérifie que la configuration est valide.

        Returns:
            bool: True si la config est valide, False sinon
        """
        if cls.PROVIDER == "gemini":
            if not cls.GOOGLE_API_KEY:
                print("⚠️  ATTENTION: GOOGLE_API_KEY non définie !")
                print("   Veuillez créer un fichier .env avec votre clé API.")
                print("   Obtenez-la sur: https://aistudio.google.com/apikey")
                return False
            if cls.GOOGLE_API_KEY.startswith("your"):
                print("⚠️  ATTENTION: GOOGLE_API_KEY n'est pas configurée !")
                print("   Remplacez la valeur dans .env par votre vraie clé.")
                return False
            print(f"✅ Provider: Gemini ({cls.DEFAULT_MODEL})")
            return True

        elif cls.PROVIDER == "openai":
            if not cls.OPENAI_API_KEY:
                print("⚠️  ATTENTION: OPENAI_API_KEY non définie !")
                print("   Veuillez créer un fichier .env avec votre clé API.")
                print("   Exemple: cp .env.example .env")
                return False
            if cls.OPENAI_API_KEY.startswith("sk-your"):
                print("⚠️  ATTENTION: OPENAI_API_KEY n'est pas configurée !")
                print("   Remplacez la valeur dans .env par votre vraie clé.")
                return False
            print(f"✅ Provider: OpenAI ({cls.DEFAULT_MODEL})")
            return True

        else:
            print(f"⚠️  Provider inconnu: {cls.PROVIDER}")
            print("   Options valides: openai, gemini")
            return False


# ================================================
# CONFIGURATION DE LA SIMULATION
# ================================================

class SimulationConfig:
    """
    Paramètres de la simulation du théâtre de l'arnaque.
    """

    # Mode debug
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Fréquence des votes audience (tous les X tours)
    AUDIENCE_VOTE_FREQUENCY: int = 3

    # Nombre de propositions à présenter au vote
    AUDIENCE_CHOICES_COUNT: int = 3

    # Durée simulée des pauses (en secondes textuelles)
    PAUSE_DURATION: int = 2

    # Activer/désactiver les effets sonores
    SOUND_EFFECTS_ENABLED: bool = True


# ================================================
# CONFIGURATION DES SCÉNARIOS
# ================================================

class ScenarioConfig:
    """
    Configuration des scénarios d'arnaque disponibles.
    """

    # Scénarios disponibles
    AVAILABLE_SCENARIOS = [
        "tech_support",    # Arnaque support technique Microsoft
        "bank_fraud",      # Arnaque faux conseiller bancaire
        "lottery_scam",    # Arnaque à la loterie
        "grandchild_scam", # Arnaque au petit-fils en difficulté
    ]

    # Scénario par défaut
    DEFAULT_SCENARIO: str = "tech_support"


# ================================================
# VÉRIFICATION AU DÉMARRAGE
# ================================================

def check_configuration() -> bool:
    """
    Vérifie toute la configuration au démarrage.

    Cette fonction est appelée au lancement de l'application
    pour s'assurer que tout est correctement configuré.

    Returns:
        bool: True si tout est OK, False sinon
    """
    print("🔧 Vérification de la configuration...")

    # Vérifier la config LLM
    if not LLMConfig.validate():
        return False

    # Vérifier que le fichier .env existe
    if not env_path.exists():
        print("⚠️  Fichier .env non trouvé.")
        print("   Créez-le avec: cp .env.example .env")
        return False

    print("✅ Configuration valide !")
    return True


# ================================================
# FONCTION GET_LLM - FACTORY POUR LES MODÈLES
# ================================================

def get_llm(model: Optional[str] = None, temperature: float = 0.7):
    """
    Factory pour créer le bon LLM selon le provider configuré.

    Args:
        model: Nom du modèle (optionnel, utilise DEFAULT_MODEL sinon)
        temperature: Température de génération (0-1)

    Returns:
        Un objet LLM compatible LangChain (ChatOpenAI ou ChatGoogleGenerativeAI)

    Raises:
        ValueError: Si le provider n'est pas supporté
    """
    model_name = model or LLMConfig.DEFAULT_MODEL
    provider = LLMConfig.PROVIDER.lower()

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=LLMConfig.GOOGLE_API_KEY,
            temperature=temperature,
            convert_system_message_to_human=True
        )

    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model_name,
            openai_api_key=LLMConfig.OPENAI_API_KEY,
            temperature=temperature,
            max_tokens=LLMConfig.MAX_TOKENS
        )

    else:
        raise ValueError(f"Provider LLM non supporté: {provider}. Utilisez 'openai' ou 'gemini'.")

llm_config = LLMConfig()
simulation_config = SimulationConfig()
scenario_config = ScenarioConfig()

