from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import LLMConfig, get_llm
from prompts.director_prompt import get_director_system_prompt
from prompts.scenarios import get_scenario_script


def clean_text(text: str) -> str:
    """Nettoie le texte des caractères surrogates et invalides."""
    if not text:
        return ""
    return text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')


class DirectorAgent:
    """
    Agent superviseur qui analyse et dirige le scénario.

    Le Directeur fonctionne en arrière-plan :
    1. Il reçoit chaque message de l'arnaqueur
    2. Il analyse où en est l'arnaque dans le "script type"
    3. Il génère un nouvel objectif pour Jeanne

    Attributes:
        llm: Le modèle de langage pour l'analyse
        scenario: Le scénario d'arnaque en cours
        script: Les étapes du script d'arnaque
        current_stage: L'étape actuelle du script
        analysis_chain: La chaîne LangChain pour l'analyse
    """

    def __init__(self, scenario: str = "tech_support", model: str = None):
        """
        Initialise le Directeur avec un scénario.

        Args:
            scenario: Le type d'arnaque à simuler
                     ("tech_support", "bank_fraud", "lottery_scam")
            model: Modèle LLM (optionnel)

        EXPLICATION :
        Le Directeur utilise une température basse (0.3) car
        son analyse doit être précise et cohérente, pas créative.
        """
        self.llm = get_llm(
            model=model,
            temperature=0.3
        )


        self.scenario = scenario
        self.script = get_scenario_script(scenario)
        self.current_stage = 0

        self.analysis_history: List[Dict] = []

        self._create_analysis_chain()

    def _create_analysis_chain(self):
        """
        Crée la chaîne LangChain pour analyser la conversation.

        ARCHITECTURE DE LA CHAÎNE :
        prompt → llm → output_parser

        C'est une "chain" simple sans outils, car le Directeur
        n'a besoin que d'analyser et de produire du texte.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", get_director_system_prompt()),
            ("human", """
SCÉNARIO EN COURS: {scenario}

SCRIPT D'ARNAQUE TYPE:
{script}

ÉTAPE ACTUELLE: {current_stage}

DERNIER MESSAGE DE L'ARNAQUEUR:
"{scammer_message}"

HISTORIQUE RÉCENT:
{recent_history}

ANALYSE REQUISE:
1. À quelle étape du script sommes-nous ?
2. L'arnaqueur a-t-il progressé ou est-il bloqué ?
3. Quel devrait être le prochain objectif de Jeanne ?

Réponds avec UN SEUL objectif clair et concis pour Jeanne.
Format: "Objectif: [instruction précise]"
""")
        ])

        self.analysis_chain = prompt | self.llm | StrOutputParser()

    def analyze_and_update(
        self,
        scammer_message: str,
        recent_history: str = ""
    ) -> str:
        """
        Analyse le message et génère un nouvel objectif.

        Cette méthode est appelée après chaque message de l'arnaqueur
        pour adapter le comportement de Jeanne.

        Args:
            scammer_message: Le dernier message de l'arnaqueur
            recent_history: Les derniers échanges pour le contexte

        Returns:
            str: Le nouvel objectif pour l'agent Victime

        Exemple:
            >>> objective = director.analyze_and_update(
            ...     "Donnez-moi accès à votre ordinateur MAINTENANT !"
            ... )
            >>> print(objective)
            "Feindre de ne pas comprendre ce qu'est 'accès à distance'"
        """
        try:
            scammer_message = clean_text(scammer_message)
            recent_history = clean_text(recent_history)

            script_text = self._format_script()

            result = self.analysis_chain.invoke({
                "scenario": self.scenario,
                "script": script_text,
                "current_stage": self.script[self.current_stage]["name"],
                "scammer_message": scammer_message,
                "recent_history": recent_history
            })

            objective = self._parse_objective(result)

            self.analysis_history.append({
                "scammer_message": scammer_message,
                "stage": self.current_stage,
                "objective": objective
            })

            self._check_stage_progression(scammer_message)

            return objective

        except Exception as e:
            print(f"⚠️ Erreur Directeur: {e}")
            return "Continuer à être confuse et lente."

    def _format_script(self) -> str:
        """
        Formate le script d'arnaque pour le prompt.

        Returns:
            str: Le script formaté en texte lisible
        """
        lines = []
        for i, stage in enumerate(self.script):
            marker = "→ " if i == self.current_stage else "  "
            lines.append(f"{marker}{i+1}. {stage['name']}: {stage['description']}")
        return "\n".join(lines)

    def _parse_objective(self, llm_response: str) -> str:
        """
        Extrait l'objectif de la réponse du LLM.

        Args:
            llm_response: La réponse brute du LLM

        Returns:
            str: L'objectif nettoyé
        """
        if "Objectif:" in llm_response:
            parts = llm_response.split("Objectif:")
            if len(parts) > 1:
                return parts[1].strip().split("\n")[0]

        for line in llm_response.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                return line

        return llm_response.strip()

    def _check_stage_progression(self, scammer_message: str):
        """
        Vérifie si l'arnaqueur a fait progresser le script.

        Détecte des mots-clés pour passer à l'étape suivante.

        Args:
            scammer_message: Le message à analyser
        """
        message_lower = scammer_message.lower()
        current_triggers = self.script[self.current_stage].get("triggers", [])

        for trigger in current_triggers:
            if trigger.lower() in message_lower:
                if self.current_stage < len(self.script) - 1:
                    self.current_stage += 1
                    print(f"🎬 SCRIPT: Passage à l'étape {self.current_stage + 1}")
                break

    def get_current_stage_info(self) -> Dict:
        """
        Retourne les informations sur l'étape actuelle.

        Returns:
            Dict: Informations de l'étape (name, description, etc.)
        """
        return {
            "stage_number": self.current_stage + 1,
            "total_stages": len(self.script),
            **self.script[self.current_stage]
        }

    def reset(self, scenario: str = None):
        """
        Réinitialise le Directeur pour une nouvelle simulation.

        Args:
            scenario: Nouveau scénario (optionnel)
        """
        if scenario:
            self.scenario = scenario
            self.script = get_scenario_script(scenario)

        self.current_stage = 0
        self.analysis_history = []
        print(f"🔄 Directeur réinitialisé. Scénario: {self.scenario}")

