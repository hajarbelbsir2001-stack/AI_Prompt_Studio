def generate_prompt(domain, subject, objective, level, language, tone):

    prompt = f"""
Agis comme un expert en {domain}.

Explique le sujet suivant : {subject}.

Objectif :
{objective}

Le niveau de l'utilisateur est :
{level}

Réponds en :
{language}

Utilise un ton :
{tone}

Donne une réponse très détaillée., structurée et facile à comprendre.
"""

    return prompt