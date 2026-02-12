from typing import Dict, List

TECH_SUPPORT_SCRIPT = [
    {
        "name": "Contact Initial",
        "description": "L'arnaqueur se présente comme le support Microsoft/Windows",
        "triggers": ["microsoft", "windows", "support", "technique", "virus", "problème"],
        "victim_strategy": "Demander de répéter le nom et l'entreprise plusieurs fois",
        "example_phrases": [
            "Bonjour, je suis du support technique Microsoft",
            "Nous avons détecté un virus sur votre ordinateur",
            "Votre PC envoie des alertes à nos serveurs"
        ]
    },
    {
        "name": "Création de Panique",
        "description": "L'arnaqueur crée un sentiment d'urgence avec le virus",
        "triggers": ["urgent", "danger", "immédiat", "hackers", "piraté", "données"],
        "victim_strategy": "Rester calme, parler de Raymond qui 'gérait ça avant'",
        "example_phrases": [
            "C'est TRÈS urgent madame !",
            "Des hackers ont accès à vos données",
            "Vous risquez de tout perdre"
        ]
    },
    {
        "name": "Demande d'Accès Distant",
        "description": "L'arnaqueur demande d'installer TeamViewer/AnyDesk",
        "triggers": ["teamviewer", "anydesk", "accès", "distance", "contrôle", "installer", "télécharger"],
        "victim_strategy": "Feindre de ne pas comprendre ce qu'est un accès à distance",
        "example_phrases": [
            "Je vais vous aider à distance",
            "Installez TeamViewer",
            "Donnez-moi le code qui s'affiche"
        ]
    },
    {
        "name": "Escalade de Pression",
        "description": "L'arnaqueur devient plus pressant/agressif",
        "triggers": ["maintenant", "vite", "dépêchez", "obligatoire", "nécessaire"],
        "victim_strategy": "Utiliser le chien qui aboie, se plaindre de maux de tête",
        "example_phrases": [
            "Vous DEVEZ le faire maintenant !",
            "C'est obligatoire pour votre sécurité",
            "Dépêchez-vous !"
        ]
    },
    {
        "name": "Demande de Paiement",
        "description": "L'arnaqueur demande un paiement pour la 'réparation'",
        "triggers": ["payer", "carte", "bancaire", "euros", "frais", "facture", "cadeau"],
        "victim_strategy": "Dire qu'on n'a pas de carte, que le neveu gère les finances",
        "example_phrases": [
            "Il y aura des frais de réparation",
            "Vous pouvez payer par carte",
            "Achetez des cartes cadeaux iTunes"
        ]
    },
    {
        "name": "Tentative Finale",
        "description": "Dernière tentative désespérée de l'arnaqueur",
        "triggers": ["dernier", "dernière", "chance", "sinon", "police", "poursuites"],
        "victim_strategy": "Menacer d'appeler son neveu policier (inventé)",
        "example_phrases": [
            "C'est votre dernière chance",
            "Sinon nous serons obligés de...",
            "La police sera contactée"
        ]
    }
]


BANK_FRAUD_SCRIPT = [
    {
        "name": "Contact Bancaire",
        "description": "L'arnaqueur se fait passer pour la banque",
        "triggers": ["banque", "conseiller", "compte", "crédit agricole", "bnp", "société générale"],
        "victim_strategy": "Demander le nom de l'agence et du directeur",
        "example_phrases": [
            "Je suis votre conseiller bancaire",
            "Il y a un problème sur votre compte",
            "Nous avons détecté des mouvements suspects"
        ]
    },
    {
        "name": "Alerte Fraude",
        "description": "L'arnaqueur prétend qu'il y a une fraude en cours",
        "triggers": ["fraude", "suspect", "prélèvement", "volé", "sécurité"],
        "victim_strategy": "S'inquiéter mais dire qu'on va rappeler la banque",
        "example_phrases": [
            "Quelqu'un essaie de vider votre compte",
            "Il y a eu un prélèvement frauduleux",
            "Nous devons sécuriser votre compte"
        ]
    },
    {
        "name": "Demande de Codes",
        "description": "L'arnaqueur demande les codes d'accès",
        "triggers": ["code", "pin", "mot de passe", "identifiant", "sms", "confirmation"],
        "victim_strategy": "Dire qu'on ne les connaît pas, que c'est le neveu qui gère",
        "example_phrases": [
            "Donnez-moi votre code de carte",
            "Quel est votre mot de passe ?",
            "Lisez-moi le code reçu par SMS"
        ]
    },
    {
        "name": "Faux Virement de Sécurité",
        "description": "L'arnaqueur demande de transférer l'argent",
        "triggers": ["virement", "transférer", "compte sécurisé", "coffre", "protection"],
        "victim_strategy": "Proposer d'aller à l'agence en personne",
        "example_phrases": [
            "Transférez votre argent sur ce compte sécurisé",
            "C'est un coffre-fort numérique",
            "Faites un virement de protection"
        ]
    }
]



LOTTERY_SCAM_SCRIPT = [
    {
        "name": "Annonce du Gain",
        "description": "L'arnaqueur annonce un gain extraordinaire",
        "triggers": ["gagné", "loterie", "prix", "million", "tirage", "félicitations"],
        "victim_strategy": "Se montrer étonnée car elle ne joue jamais",
        "example_phrases": [
            "Félicitations ! Vous avez gagné !",
            "Votre numéro a été tiré au sort",
            "Vous êtes l'heureuse gagnante de 100 000€"
        ]
    },
    {
        "name": "Demande de Frais",
        "description": "L'arnaqueur demande des frais pour débloquer le gain",
        "triggers": ["frais", "taxe", "débloquer", "virement", "mandat"],
        "victim_strategy": "Demander pourquoi on ne déduit pas les frais du gain",
        "example_phrases": [
            "Il y a juste des frais de dossier",
            "Vous devez payer la taxe de déblocage",
            "Envoyez un mandat de 500€"
        ]
    },
    {
        "name": "Pression Temporelle",
        "description": "L'arnaqueur crée une date limite",
        "triggers": ["expire", "délai", "aujourd'hui", "minuit", "perdu"],
        "victim_strategy": "Dire qu'on doit en parler avec la famille d'abord",
        "example_phrases": [
            "L'offre expire ce soir",
            "Vous avez jusqu'à minuit",
            "Après, le prix sera attribué à quelqu'un d'autre"
        ]
    }
]


GRANDCHILD_SCAM_SCRIPT = [
    {
        "name": "Identification Familiale",
        "description": "L'arnaqueur prétend être un membre de la famille",
        "triggers": ["mamie", "grand-mère", "c'est moi", "reconnais", "petit-fils", "nièce"],
        "victim_strategy": "Demander des détails que seul le vrai petit-fils connaîtrait",
        "example_phrases": [
            "Mamie, c'est moi !",
            "Tu ne reconnais pas ma voix ?",
            "C'est ton petit-fils préféré"
        ]
    },
    {
        "name": "Annonce du Problème",
        "description": "L'arnaqueur annonce être dans une situation difficile",
        "triggers": ["accident", "prison", "hôpital", "arrêté", "problème", "aide"],
        "victim_strategy": "S'inquiéter mais proposer d'appeler ses parents",
        "example_phrases": [
            "J'ai eu un accident",
            "Je suis à l'hôpital",
            "La police m'a arrêté"
        ]
    },
    {
        "name": "Demande d'Argent Urgent",
        "description": "L'arnaqueur demande de l'argent immédiatement",
        "triggers": ["argent", "caution", "envoyer", "western union", "liquide"],
        "victim_strategy": "Dire qu'on n'a pas autant, proposer d'appeler les parents",
        "example_phrases": [
            "J'ai besoin de 5000€ pour la caution",
            "Envoie l'argent par Western Union",
            "Quelqu'un va passer le chercher"
        ]
    },
    {
        "name": "Secret Imposé",
        "description": "L'arnaqueur demande de ne rien dire à personne",
        "triggers": ["secret", "personne", "parents", "pas dire", "entre nous"],
        "victim_strategy": "Promettre mais dire qu'on doit quand même vérifier",
        "example_phrases": [
            "Ne dis rien à maman",
            "C'est un secret entre nous",
            "Ils ne doivent pas savoir"
        ]
    }
]

SCENARIOS: Dict[str, List[Dict]] = {
    "tech_support": TECH_SUPPORT_SCRIPT,
    "bank_fraud": BANK_FRAUD_SCRIPT,
    "lottery_scam": LOTTERY_SCAM_SCRIPT,
    "grandchild_scam": GRANDCHILD_SCAM_SCRIPT
}


def get_scenario_script(scenario_name: str) -> List[Dict]:
    """
    Récupère le script d'un scénario par son nom.

    Args:
        scenario_name: Le nom du scénario (tech_support, bank_fraud, etc.)

    Returns:
        List[Dict]: La liste des étapes du script

    Raises:
        ValueError: Si le scénario n'existe pas
    """
    if scenario_name not in SCENARIOS:
        available = ", ".join(SCENARIOS.keys())
        raise ValueError(f"Scénario '{scenario_name}' inconnu. Disponibles: {available}")

    return SCENARIOS[scenario_name]


def get_scenario_description(scenario_name: str) -> str:
    """
    Retourne une description lisible du scénario.

    Args:
        scenario_name: Le nom du scénario

    Returns:
        str: Description formatée
    """
    descriptions = {
        "tech_support": "🖥️ Arnaque au Support Technique Microsoft - L'arnaqueur prétend que votre PC a un virus",
        "bank_fraud": "🏦 Arnaque au Faux Conseiller Bancaire - L'arnaqueur se fait passer pour votre banque",
        "lottery_scam": "🎰 Arnaque à la Loterie - L'arnaqueur annonce un faux gain",
        "grandchild_scam": "👨‍👩‍👦 Arnaque au Petit-Fils - L'arnaqueur prétend être un membre de la famille en difficulté"
    }

    return descriptions.get(scenario_name, f"Scénario: {scenario_name}")

