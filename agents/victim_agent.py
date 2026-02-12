from typing import List, Optional
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from config import LLMConfig, get_llm
from tools.audio_tools import get_audio_tools
from prompts.victim_prompt import get_victim_system_prompt


def clean_text(text: str) -> str:
    """Nettoie le texte des caractères surrogates et invalides."""
    if not text:
        return ""
    return text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')


class VictimAgent:
    """
    Agent LLM représentant Mme Jeanne Dubois.

    Cette classe encapsule toute la logique de l'agent victime :
    - Initialisation du LLM et des outils
    - Gestion du contexte dynamique (objectifs, contraintes)
    - Génération des réponses en personnage

    Attributes:
        llm: Le modèle de langage OpenAI
        tools: Liste des outils audio disponibles
        memory: Mémoire conversationnelle
        agent_executor: L'exécuteur d'agent LangChain
        current_objective: Objectif courant défini par le Directeur
        audience_constraint: Contrainte temporaire de l'audience
    """

    def __init__(self, model: str = None):
        """
        Initialise l'agent Victime.

        Args:
            model: Nom du modèle LLM à utiliser (défaut: config)

        EXPLICATION :
        1. On crée le LLM avec la clé API de l'environnement
        2. On récupère les outils audio (définis dans tools/audio_tools.py)
        3. On initialise la mémoire conversationnelle
        4. On crée l'agent avec le prompt système
        """
        self.llm = get_llm(
            model=model,
            temperature=0.8
        )

        self.tools = get_audio_tools()

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="input"
        )

        self.current_objective = "Répondre poliment mais lentement."
        self.audience_constraint = None

        self._create_agent()

    def _create_agent(self):
        """
        Crée l'AgentExecutor LangChain avec les Tools.

        EXPLICATION DU PROMPT :
        Le prompt est structuré en plusieurs parties :
        1. System: Le personnage de base (Jeanne Dubois)
        2. Dynamic Context: L'objectif courant du Directeur
        3. Audience Event: Les contraintes du vote public
        4. Chat History: L'historique de la conversation
        5. Human: Le message de l'arnaqueur

        C'est cette structure modulaire qui permet au Directeur
        de modifier le comportement de Jeanne en temps réel.
        """
        # Construction du prompt avec placeholders dynamiques
        prompt = ChatPromptTemplate.from_messages([
            ("system", get_victim_system_prompt()),
            ("system", "OBJECTIF ACTUEL: {current_objective}"),
            ("system", "CONTRAINTE AUDIENCE: {audience_constraint}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_openai_tools_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )

    def update_objective(self, new_objective: str):
        """
        Met à jour l'objectif courant de Jeanne.

        Cette méthode est appelée par le DirectorAgent pour
        modifier le comportement de Jeanne en fonction du script.

        Args:
            new_objective: Le nouvel objectif (ex: "Feindre la confusion")

        Exemple:
            agent.update_objective("Faire croire que l'ordinateur ne démarre pas")
        """
        self.current_objective = new_objective
        print(f"🎬 DIRECTEUR: Nouvel objectif → {new_objective}")

    def set_audience_constraint(self, constraint: Optional[str]):
        """
        Applique une contrainte temporaire de l'audience.

        Après un vote du public, cette contrainte modifie
        temporairement le comportement de Jeanne.

        Args:
            constraint: La contrainte (ex: "Quelqu'un sonne à la porte")
                       None pour retirer la contrainte
        """
        self.audience_constraint = constraint
        if constraint:
            print(f"👥 AUDIENCE: Contrainte appliquée → {constraint}")

    def respond(self, scammer_message: str) -> str:
        """
        Génère une réponse de Jeanne à l'arnaqueur.

        Cette méthode est le cœur de l'agent :
        1. Elle reçoit le message de l'arnaqueur
        2. Elle passe le contexte complet au LLM
        3. Le LLM peut décider d'utiliser des outils audio
        4. Elle retourne la réponse en personnage

        Args:
            scammer_message: Le message de l'arnaqueur

        Returns:
            str: La réponse de Jeanne (peut inclure des effets sonores)

        Exemple:
            >>> response = agent.respond("Donnez-moi votre mot de passe !")
            >>> print(response)
            "Oh mon dieu... Mon mot de passe ? Attendez...
             [SOUND_EFFECT: DOG_BARKING]
             POUPOUNE ! Pas maintenant !"
        """
        try:
            scammer_message = clean_text(scammer_message)


            result = self.agent_executor.invoke({
                "input": scammer_message,
                "current_objective": self.current_objective,
                "audience_constraint": self.audience_constraint or "Aucune contrainte spéciale."
            })

            return result["output"]

        except Exception as e:
            print(f"⚠️ Erreur agent: {e}")
            return "Oh... Excusez-moi, je n'ai pas bien compris... Vous pouvez répéter ?"

    def reset(self):
        """
        Réinitialise l'agent pour une nouvelle simulation.

        Efface la mémoire et remet les objectifs par défaut.
        """
        self.memory.clear()
        self.current_objective = "Répondre poliment mais lentement."
        self.audience_constraint = None
        print("🔄 Agent Victime réinitialisé.")

