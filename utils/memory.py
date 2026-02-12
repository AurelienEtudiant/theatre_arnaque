from typing import List, Dict, Optional
from datetime import datetime


class ConversationManager:
    """
    Gestionnaire centralisé de la conversation.

    Cette classe maintient l'historique complet et fournit
    des méthodes pour accéder au contexte récent.

    Attributes:
        history: Liste complète des messages
        start_time: Heure de début de la simulation
        scenario: Le scénario en cours
    """

    def __init__(self, scenario: str = "tech_support"):
        """
        Initialise le gestionnaire de conversation.

        Args:
            scenario: Le scénario d'arnaque en cours
        """
        self.history: List[Dict] = []
        self.start_time = datetime.now()
        self.scenario = scenario
        self.turn_count = 0

    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """
        Ajoute un message à l'historique.

        Args:
            role: Le rôle ("scammer", "victim", "system")
            content: Le contenu du message
            metadata: Métadonnées optionnelles (effets sonores, etc.)
        """
        message = {
            "turn": self.turn_count,
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }

        self.history.append(message)

        if role in ["scammer", "victim"]:
            self.turn_count += 1

    def get_recent_history(self, n: int = 5) -> str:
        """
        Récupère les N derniers échanges formatés.

        Args:
            n: Nombre de messages à récupérer

        Returns:
            str: Historique formaté
        """
        recent = self.history[-n:] if len(self.history) >= n else self.history

        lines = []
        for msg in recent:
            role_emoji = {
                "scammer": "🦹 ARNAQUEUR",
                "victim": "👵 JEANNE",
                "system": "⚙️ SYSTÈME"
            }.get(msg["role"], msg["role"])

            lines.append(f"{role_emoji}: {msg['content'][:100]}...")

        return "\n".join(lines)

    def get_full_transcript(self) -> str:
        """
        Génère la transcription complète de la conversation.

        Returns:
            str: Transcription formatée
        """
        lines = [
            "=" * 60,
            f"🎭 TRANSCRIPTION - LE THÉÂTRE DE L'ARNAQUE",
            f"📅 Date: {self.start_time.strftime('%Y-%m-%d %H:%M')}",
            f"🎬 Scénario: {self.scenario}",
            f"📊 Nombre de tours: {self.turn_count}",
            "=" * 60,
            ""
        ]

        for msg in self.history:
            if msg["role"] == "system":
                lines.append(f"\n[{msg['content']}]\n")
            else:
                role_name = "ARNAQUEUR" if msg["role"] == "scammer" else "JEANNE"
                lines.append(f"{role_name}:")
                lines.append(f"  {msg['content']}")

                # Ajouter les métadonnées si présentes
                if msg.get("metadata", {}).get("sound_effects"):
                    effects = msg["metadata"]["sound_effects"]
                    lines.append(f"  🔊 [Effets: {', '.join(effects)}]")

                lines.append("")

        lines.append("=" * 60)
        lines.append("FIN DE LA TRANSCRIPTION")
        lines.append("=" * 60)

        return "\n".join(lines)

    def extract_sound_effects(self, message: str) -> List[str]:
        """
        Extrait les effets sonores d'un message.

        Args:
            message: Le message à analyser

        Returns:
            List[str]: Liste des effets trouvés
        """
        effects = []
        effect_markers = [
            "DOG_BARKING",
            "DOORBELL",
            "COUGHING",
            "TV_BACKGROUND",
            "PHONE_STATIC",
            "KETTLE_WHISTLE"
        ]

        for marker in effect_markers:
            if marker in message:
                effects.append(marker)

        return effects

    def get_statistics(self) -> Dict:
        """
        Génère des statistiques sur la conversation.

        Returns:
            Dict: Statistiques (durée, nombre de messages, etc.)
        """
        scammer_messages = [m for m in self.history if m["role"] == "scammer"]
        victim_messages = [m for m in self.history if m["role"] == "victim"]

        total_effects = 0
        for msg in victim_messages:
            total_effects += len(self.extract_sound_effects(msg["content"]))

        duration = datetime.now() - self.start_time

        return {
            "duration_seconds": duration.total_seconds(),
            "total_turns": self.turn_count,
            "scammer_messages": len(scammer_messages),
            "victim_messages": len(victim_messages),
            "sound_effects_used": total_effects,
            "scenario": self.scenario
        }

    def save_to_file(self, filepath: str):
        """
        Sauvegarde la transcription dans un fichier.

        Args:
            filepath: Chemin du fichier de sortie
        """
        transcript = self.get_full_transcript()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(transcript)

        print(f"Transcription sauvegardée: {filepath}")

    def reset(self):
        """
        Réinitialise la conversation.
        """
        self.history = []
        self.start_time = datetime.now()
        self.turn_count = 0
        print("🔄 Historique réinitialisé.")

