"""
Agent Modérateur d'Audience
===========================

Cet agent gère l'interaction avec le public/l'audience.
Il permet aux spectateurs d'influencer le cours de la simulation.

RÔLE :
- Collecter les propositions du public
- Filtrer les suggestions inappropriées
- Sélectionner les 3 meilleures options pour un vote
- Transformer le choix gagnant en contrainte pour Jeanne

EXEMPLES DE PROPOSITIONS :
- "Quelqu'un sonne à la porte"
- "Le four commence à brûler"
- "Jeanne renverse son café sur le clavier"
- "Le chat saute sur la table"
"""

from typing import List, Optional, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import random

from config import LLMConfig, get_llm
from prompts.moderator_prompt import get_moderator_system_prompt


class ModeratorAgent:
    """
    Agent qui gère les propositions et votes de l'audience.

    L'audience peut proposer des événements qui vont perturber
    la conversation. Le Modérateur :
    1. Filtre les propositions inappropriées
    2. Sélectionne les plus pertinentes
    3. Organise le vote
    4. Transforme le gagnant en contrainte

    Attributes:
        llm: Le modèle de langage pour le filtrage
        pending_proposals: Propositions en attente
        vote_history: Historique des votes
        filter_chain: Chaîne pour filtrer les propositions
    """

    def __init__(self, model: str = None):
        """
        Initialise le Modérateur.

        Args:
            model: Modèle LLM (optionnel)
        """
        self.llm = get_llm(
            model=model,
            temperature=0.5
        )

        self.pending_proposals: List[str] = []

        self.vote_history: List[Dict] = []

        self._create_filter_chain()

    def _create_filter_chain(self):
        """
        Crée la chaîne pour filtrer et sélectionner les propositions.

        CRITÈRES DE FILTRAGE :
        - Pas de contenu inapproprié
        - Cohérent avec le contexte (dame âgée à la maison)
        - Réaliste et amusant
        - Perturbant pour l'arnaqueur
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", get_moderator_system_prompt()),
            ("human", """
CONTEXTE ACTUEL DE LA CONVERSATION:
{context}

PROPOSITIONS DE L'AUDIENCE:
{proposals}

TÂCHE:
1. Filtre les propositions inappropriées (violence, contenu adulte, etc.)
2. Évalue la pertinence de chaque proposition (cohérence avec le contexte)
3. Sélectionne les 3 meilleures propositions

Réponds avec exactement 3 propositions, une par ligne, format:
1. [Proposition 1]
2. [Proposition 2]
3. [Proposition 3]
""")
        ])

        self.filter_chain = prompt | self.llm | StrOutputParser()

    def add_proposal(self, proposal: str) -> bool:
        """
        Ajoute une proposition de l'audience.

        Args:
            proposal: La proposition à ajouter

        Returns:
            bool: True si ajoutée, False si rejetée immédiatement
        """
        if len(proposal.strip()) < 5:
            return False

        forbidden_words = ["mort", "tuer", "suicide", "violence"]
        if any(word in proposal.lower() for word in forbidden_words):
            print(f"⚠️ Proposition rejetée (contenu interdit)")
            return False

        self.pending_proposals.append(proposal.strip())
        print(f"✅ Proposition ajoutée: '{proposal[:50]}...'")
        return True

    def generate_choices(self, context: str = "") -> List[str]:
        """
        Génère les 3 choix pour le vote à partir des propositions.

        Si pas assez de propositions, en génère automatiquement.

        Args:
            context: Le contexte actuel de la conversation

        Returns:
            List[str]: Les 3 propositions à voter
        """
        if len(self.pending_proposals) < 3:
            self._add_default_proposals()

        try:
            proposals_text = "\n".join([
                f"- {p}" for p in self.pending_proposals
            ])

            result = self.filter_chain.invoke({
                "context": context or "Conversation en cours",
                "proposals": proposals_text
            })

            choices = self._parse_choices(result)

            self.pending_proposals = []

            return choices

        except Exception as e:
            print(f"⚠️ Erreur Modérateur: {e}")
            return self._get_fallback_choices()

    def _add_default_proposals(self):
        """
        Ajoute des propositions par défaut si l'audience n'en a pas assez.
        """
        defaults = [
            "Quelqu'un sonne à la porte",
            "Le chien Poupoune veut sortir",
            "La bouilloire siffle",
            "Jeanne doit aller aux toilettes",
            "Un voisin l'appelle par la fenêtre",
            "Elle ne trouve plus ses lunettes",
            "La télévision change de chaîne toute seule",
            "Elle reçoit un autre appel",
        ]

        while len(self.pending_proposals) < 5:
            choice = random.choice(defaults)
            if choice not in self.pending_proposals:
                self.pending_proposals.append(choice)

    def _parse_choices(self, llm_response: str) -> List[str]:
        """
        Parse les 3 choix de la réponse du LLM.

        Args:
            llm_response: La réponse brute du LLM

        Returns:
            List[str]: Les 3 choix extraits
        """
        choices = []

        for line in llm_response.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                clean = line.lstrip("0123456789.-) ").strip()
                if clean:
                    choices.append(clean)

        while len(choices) < 3:
            choices.append(random.choice(self._get_fallback_choices()))

        return choices[:3]

    def _get_fallback_choices(self) -> List[str]:
        """
        Retourne des choix par défaut en cas d'erreur.

        Returns:
            List[str]: Choix de secours
        """
        return [
            "Quelqu'un sonne à la porte",
            "Poupoune commence à aboyer fort",
            "La ligne téléphonique grésille"
        ]

    def run_vote(self, choices: List[str], simulate: bool = True) -> Dict:
        """
        Lance un vote sur les 3 propositions.

        Args:
            choices: Les 3 propositions à voter
            simulate: Si True, simule des votes aléatoires

        Returns:
            Dict: Résultat du vote avec le gagnant
        """
        if simulate:
            total_votes = 100
            votes = self._simulate_votes(len(choices), total_votes)
        else:
            votes = [0] * len(choices)
            print("\n👥 VOTE DE L'AUDIENCE:")
            for i, choice in enumerate(choices):
                print(f"   {i+1}. {choice}")

            try:
                user_vote = int(input("\nVotre vote (1-3): ")) - 1
                if 0 <= user_vote < len(choices):
                    votes[user_vote] = 1
            except ValueError:
                votes[0] = 1

        winner_idx = votes.index(max(votes))
        winner = choices[winner_idx]
        total = sum(votes)

        result = {
            "choices": choices,
            "votes": votes,
            "percentages": [round(v/total*100) for v in votes] if total > 0 else [0]*len(votes),
            "winner": winner,
            "winner_index": winner_idx
        }

        self.vote_history.append(result)

        return result

    def _simulate_votes(self, num_choices: int, total_votes: int) -> List[int]:
        """
        Simule une distribution de votes réaliste.

        Args:
            num_choices: Nombre de choix
            total_votes: Nombre total de votes

        Returns:
            List[int]: Votes par choix
        """
        weights = [random.random() for _ in range(num_choices)]
        total_weight = sum(weights)
        votes = [int(w/total_weight * total_votes) for w in weights]

        diff = total_votes - sum(votes)
        if diff > 0:
            votes[0] += diff

        return votes

    def format_vote_result(self, result: Dict) -> str:
        """
        Formate le résultat du vote pour l'affichage.

        Args:
            result: Le résultat du vote

        Returns:
            str: Texte formaté
        """
        lines = ["\n👥 RÉSULTAT DU VOTE DE L'AUDIENCE:"]
        lines.append("=" * 40)

        for i, (choice, pct) in enumerate(zip(result["choices"], result["percentages"])):
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            marker = "→ " if i == result["winner_index"] else "  "
            lines.append(f"{marker}{i+1}. {choice}")
            lines.append(f"   {bar} {pct}%")

        lines.append(f"\n🏆 GAGNANT: {result['winner']}")
        lines.append("=" * 40)

        return "\n".join(lines)

    def reset(self):
        """
        Réinitialise le Modérateur.
        """
        self.pending_proposals = []
        self.vote_history = []
        print("🔄 Modérateur réinitialisé.")

