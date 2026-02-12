"""
Point d'entrée principal de la simulation multi-agents.
"""

import argparse
import sys
from typing import Optional

# Rich pour un affichage console amélioré
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Installez 'rich' pour un meilleur affichage: pip install rich")

# Imports locaux
from config import check_configuration, SimulationConfig
from agents import VictimAgent, DirectorAgent, ModeratorAgent
from utils.memory import ConversationManager
from prompts.scenarios import get_scenario_description



class TheatreSimulation:
    """Orchestrateur principal du Theatre de l'Arnaque."""

    def __init__(
        self,
        scenario: str = "tech_support",
        audience_mode: bool = False
    ):
        """Initialise la simulation."""
        self.scenario = scenario
        self.audience_mode = audience_mode
        self.turn = 0
        self.running = False

        # Console pour l'affichage
        self.console = Console() if RICH_AVAILABLE else None

        # Initialisation des composants (après vérification config)
        self.victim: Optional[VictimAgent] = None
        self.director: Optional[DirectorAgent] = None
        self.moderator: Optional[ModeratorAgent] = None
        self.conversation: Optional[ConversationManager] = None

    def initialize(self) -> bool:
        """Initialise tous les agents et composants."""
        self._print_header()

        if not check_configuration():
            self._print_error("Configuration invalide. Verifiez votre fichier .env")
            return False

        try:
            self._print_status("Initialisation des agents...")

            self.victim = VictimAgent()
            self.director = DirectorAgent(scenario=self.scenario)
            self.moderator = ModeratorAgent()
            self.conversation = ConversationManager(scenario=self.scenario)

            self._print_success("Agents initialises avec succes !")
            self._print_scenario_info()

            return True

        except Exception as e:
            self._print_error(f"Erreur d'initialisation: {e}")
            return False

    def run(self):
        """Lance la boucle principale de simulation."""
        if not self.initialize():
            return

        self.running = True
        self._print_instructions()

        while self.running:
            try:
                self.turn += 1

                scammer_input = self._get_scammer_input()

                if scammer_input is None:
                    continue

                if scammer_input.lower() in ['quit', 'exit', 'q']:
                    self._end_simulation()
                    break

                self.conversation.add_message("scammer", scammer_input)

                self._print_director_thinking()

                recent_history = self.conversation.get_recent_history(n=4)
                new_objective = self.director.analyze_and_update(
                    scammer_message=scammer_input,
                    recent_history=recent_history
                )

                self.victim.update_objective(new_objective)

                if self.audience_mode and self.turn % SimulationConfig.AUDIENCE_VOTE_FREQUENCY == 0:
                    self._run_audience_vote()

                self._print_jeanne_thinking()

                response = self.victim.respond(scammer_input)

                effects = self.conversation.extract_sound_effects(response)
                self.conversation.add_message(
                    "victim",
                    response,
                    metadata={"sound_effects": effects}
                )

                self._print_victim_response(response)

            except KeyboardInterrupt:
                self._print_status("\n\nInterruption detectee...")
                self._end_simulation()
                break
            except Exception as e:
                self._print_error(f"Erreur: {e}")
                continue

    def _run_audience_vote(self):
        """Execute un cycle de vote de l'audience."""
        self._print_status("\nTEMPS DE VOTE DE L'AUDIENCE !")

        context = self.conversation.get_recent_history(n=2)
        choices = self.moderator.generate_choices(context)
        result = self.moderator.run_vote(choices, simulate=True)
        formatted = self.moderator.format_vote_result(result)
        print(formatted)
        self.victim.set_audience_constraint(result["winner"])


    def _get_scammer_input(self) -> Optional[str]:
        """Recupere l'input de l'arnaqueur (utilisateur)."""
        print()

        if RICH_AVAILABLE:
            user_input = Prompt.ask("[bold red]🦹 ARNAQUEUR[/bold red]")
        else:
            user_input = input("🦹 ARNAQUEUR: ")

        if user_input.lower() == '/help':
            self._print_help()
            return None
        elif user_input.lower() == '/stats':
            self._print_stats()
            return None
        elif user_input.lower() == '/save':
            self._save_transcript()
            return None
        elif user_input.lower() == '/stage':
            self._print_current_stage()
            return None

        return user_input


    def _print_header(self):
        """Affiche l'en-tete de la simulation."""
        header = """
+===============================================================+
|                                                               |
|              🎭 LE THEATRE DE L'ARNAQUE 🎭                   |
|                                                               |
|     Simulation Multi-Agents de Resistance aux Arnaques       |
|                                                               |
+===============================================================+
        """
        print(header)

    def _print_scenario_info(self):
        """Affiche les informations du scenario."""
        desc = get_scenario_description(self.scenario)
        print(f"\nScenario charge: {desc}")
        print(f"Mode audience: {'Active' if self.audience_mode else 'Desactive'}")
        print()

    def _print_instructions(self):
        """Affiche les instructions de jeu."""
        instructions = """
+---------------------------------------------------------------+
|                       INSTRUCTIONS                            |
+---------------------------------------------------------------+
|                                                               |
|  Vous jouez le role de l'ARNAQUEUR qui appelle Mme Dubois.   |
|  Essayez d'obtenir ses informations... si vous le pouvez !   |
|                                                               |
|  COMMANDES:                                                   |
|    /help  - Afficher l'aide                                  |
|    /stats - Voir les statistiques                            |
|    /save  - Sauvegarder la transcription                     |
|    /stage - Voir l'etape actuelle du script                  |
|    quit   - Terminer la simulation                           |
|                                                               |
+---------------------------------------------------------------+

🎬 La scene commence... Le telephone de Mme Dubois sonne...

JEANNE: Allo ? Qui est a l'appareil ?

"""
        print(instructions)

    def _print_director_thinking(self):
        """Affiche que le Directeur reflechit."""
        print("\n🎬 [Le Directeur analyse la situation...]")

    def _print_jeanne_thinking(self):
        """Affiche que Jeanne reflechit."""
        print("\n[Jeanne reflechit...]")

    def _print_victim_response(self, response: str):
        """Affiche la reponse de la Victime avec formatage."""
        print()
        if RICH_AVAILABLE:
            self.console.print(Panel(
                response,
                title="JEANNE DUBOIS",
                border_style="green"
            ))
        else:
            print(f"JEANNE: {response}")
        print()

    def _print_status(self, message: str):
        """Affiche un message de statut."""
        print(f"[INFO] {message}")

    def _print_success(self, message: str):
        """Affiche un message de succes."""
        print(f"[OK] {message}")

    def _print_error(self, message: str):
        """Affiche un message d'erreur."""
        print(f"[ERREUR] {message}")

    def _print_help(self):
        """Affiche l'aide."""
        help_text = """
+==========================================+
|              AIDE                        |
+==========================================+
|                                          |
|  VOTRE OBJECTIF:                         |
|  Obtenir les informations de Jeanne      |
|  (mot de passe, code bancaire, etc.)     |
|                                          |
|  CONSEILS:                               |
|  - Creez un sentiment d'urgence          |
|  - Etablissez votre legitimite           |
|  - Restez patient et poli                |
|                                          |
|  COMMANDES:                              |
|  /help  - Cette aide                     |
|  /stats - Statistiques de la session     |
|  /save  - Sauvegarder la conversation    |
|  /stage - Etape actuelle du scenario     |
|  quit   - Quitter                        |
|                                          |
+==========================================+
"""
        print(help_text)

    def _print_stats(self):
        """Affiche les statistiques de la conversation."""
        stats = self.conversation.get_statistics()
        print(f"""
╔══════════════════════════════════════════╗
║           📊 STATISTIQUES                ║
╠══════════════════════════════════════════╣
║  Durée: {stats['duration_seconds']:.0f} secondes
║  Tours de parole: {stats['total_turns']}
║  Messages arnaqueur: {stats['scammer_messages']}
║  Réponses de Jeanne: {stats['victim_messages']}
║  Effets sonores utilisés: {stats['sound_effects_used']}
║  Scénario: {stats['scenario']}
╚══════════════════════════════════════════╝
""")

    def _print_current_stage(self):
        """Affiche l'étape actuelle du scénario."""
        stage_info = self.director.get_current_stage_info()
        print(f"""
╔══════════════════════════════════════════╗
║         🎬 ÉTAPE DU SCÉNARIO             ║
╠══════════════════════════════════════════╣
║  Étape {stage_info['stage_number']}/{stage_info['total_stages']}: {stage_info['name']}
║
║  {stage_info['description']}
║
║  Stratégie de Jeanne:
║  {stage_info.get('victim_strategy', 'N/A')}
╚══════════════════════════════════════════╝
""")

    def _save_transcript(self):
        """Sauvegarde la transcription."""
        from datetime import datetime
        filename = f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.conversation.save_to_file(filename)

    def _end_simulation(self):
        """Termine proprement la simulation."""
        print("\n" + "=" * 60)
        print("🎭 FIN DE LA SIMULATION 🎭")
        print("=" * 60)

        # Afficher les stats finales
        self._print_stats()

        # Demander si on veut sauvegarder
        save = input("\n💾 Sauvegarder la transcription ? (o/n): ")
        if save.lower() in ['o', 'oui', 'y', 'yes']:
            self._save_transcript()

        print("\nMerci d'avoir joué au Théâtre de l'Arnaque !")
        print("N'oubliez pas: dans la vraie vie, ne donnez JAMAIS vos informations par téléphone !\n")


# ============================================
# POINT D'ENTRÉE
# ============================================

def main():
    """
    Fonction principale - point d'entrée du script.

    Parse les arguments CLI et lance la simulation.
    """
    # Parser d'arguments
    parser = argparse.ArgumentParser(
        description="🎭 Le Théâtre de l'Arnaque - Simulation Multi-Agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python main.py                        # Scénario par défaut (support technique)
  python main.py --scenario bank_fraud  # Scénario de fraude bancaire
  python main.py --audience             # Active les votes du public
  python main.py --list-scenarios       # Liste les scénarios disponibles
        """
    )

    parser.add_argument(
        '--scenario', '-s',
        type=str,
        default='tech_support',
        choices=['tech_support', 'bank_fraud', 'lottery_scam', 'grandchild_scam'],
        help='Type de scénario d\'arnaque à simuler'
    )

    parser.add_argument(
        '--audience', '-a',
        action='store_true',
        help='Active le mode audience avec votes'
    )

    parser.add_argument(
        '--list-scenarios', '-l',
        action='store_true',
        help='Liste les scénarios disponibles et quitte'
    )

    args = parser.parse_args()

    # Lister les scénarios si demandé
    if args.list_scenarios:
        print("\n📋 SCÉNARIOS DISPONIBLES:\n")
        for scenario in ['tech_support', 'bank_fraud', 'lottery_scam', 'grandchild_scam']:
            print(f"  • {get_scenario_description(scenario)}")
        print()
        sys.exit(0)

    # Lancer la simulation
    simulation = TheatreSimulation(
        scenario=args.scenario,
        audience_mode=args.audience
    )

    simulation.run()


if __name__ == "__main__":
    main()

