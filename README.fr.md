# Agents IA en Python

🇬🇧 English version: [README.md](README.md)

## Description

**AI Study Guide Generator** (générateur de fiches de révision) est un petit
système multi-agents construit avec Python, Google ADK, LiteLLM et Ollama.

Il reçoit un sujet de programmation, par exemple `Python decorators`, et génère
une fiche de révision en Markdown avec une explication, les notions clés, un
exemple, un exercice, les erreurs fréquentes, des commentaires de relecture et
un résumé final.

Le système suit un principe simple : **l'IA écrit, le code vérifie et
enregistre**. Trois agents génèrent le contenu, et deux outils Python
déterministes le valident et l'enregistrent.

## Prérequis

- **Système** : Ubuntu (développé sous Ubuntu dans WSL, sur Windows)
- **Python** : 3.12
- **Ollama** : pour faire tourner le modèle en local
- **Modèle** : `llama3.2` (environ 2 Go sur le disque), un petit modèle qui
  sait utiliser des outils
- **Matériel** : pas de carte graphique nécessaire. Le projet a été développé
  uniquement sur le processeur (CPU), aucune carte graphique n'étant utilisable
  sous WSL.
- **Bibliothèques Python** : listées dans `requirements.txt`

| Élément | Rôle |
|---|---|
| **Google ADK** | Bibliothèque Python qui sert à créer et lancer les agents |
| **LiteLLM** | Connecteur qui transmet les demandes des agents au fournisseur de modèle |
| **Ollama** | Programme qui fait tourner le modèle en local, sur `http://localhost:11434` |
| **llama3.2** | Petit modèle de langage local qui génère le texte |

```text
Google ADK  →  LiteLLM  →  Ollama  →  llama3.2
```

Aucune clé API ni compte payant n'est nécessaire.

## Installation

### 1. Installer Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama -v
```

Si Ollama ne tourne pas en tâche de fond, lance-le dans un autre terminal :

```bash
ollama serve
```

### 2. Télécharger et tester le modèle

```bash
ollama pull llama3.2
ollama show llama3.2
```

`tools` doit apparaître dans la partie **Capabilities**.

Vérifier que le modèle répond en local :

```bash
ollama run llama3.2
```

Tape une petite question, puis `/bye` pour quitter.

### 3. Créer et activer un environnement virtuel

```bash
python3 -m venv venv --prompt ai-agents
source venv/bin/activate
```

### 4. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

## Configuration

Les réglages sont rangés dans un fichier `.env`, lu par `config.py` au
démarrage. Crée-le à partir du fichier d'exemple :

```bash
cp .env.example .env
```

| Variable | Description | Exemple |
|---|---|---|
| `OLLAMA_API_BASE` | Adresse du serveur Ollama local | `http://localhost:11434` |
| `MODEL_NAME` | Modèle utilisé par LiteLLM (`ollama_chat/` + nom du modèle) | `ollama_chat/llama3.2` |

Pour utiliser un autre modèle, télécharge-le avec Ollama et modifie
`MODEL_NAME` : le code n'a pas besoin de changer.

Le vrai fichier `.env` reste en local : il est listé dans `.gitignore` et ne
doit jamais être envoyé sur GitHub.

## Lancement

Vérifie qu'Ollama tourne et que l'environnement virtuel est activé, puis :

```bash
./main.py
```

Tape un sujet quand il est demandé. Le programme affiche sa progression :

```text
Enter a programming topic: Python decorators
[1/5] Explainer agent is working...
[2/5] Practice designer agent is working...
[3/5] Reviewer agent is working...
[4/5] Validating the study guide...
All required sections are present.
[5/5] Saving the study guide...
Study guide saved to output/study_guide.md
```

La fiche est enregistrée dans `output/study_guide.md`.

## Exemple d'entrée

```text
Python decorators
```

## Exemple de sortie

Extrait raccourci de `output/study_guide.md` (la fiche est générée en
anglais) :

````markdown
# Topic: Python decorators

## Simple Explanation
Python decorators are a powerful feature that allows programmers to modify or
extend the behavior of a function without permanently changing it.

## Key Concepts
* **Decorators**: a function that takes another function as an argument and
  returns a new function that "wraps" the original function.
* **Decorator syntax**: `@decorator_name`, equivalent to
  `decorator_name(func)`.

## Example
```python
def my_decorator(func):
    def wrapper():
        print("Before the function is executed")
        func()
        print("After the function is executed")
    return wrapper

@my_decorator
def say_hello():
    print("Hello, world!")
```

## Practice Exercise
Create a decorator that prints a message before and after the execution of a
`greet(name)` function. ...

## Common Mistakes
...

## Review Comments
...

## Final Summary
...
````

## Structure du projet

```text
ai-agents-intro/
├── agents/
│   ├── explainer_agent.py          # Explique le sujet
│   ├── practice_designer_agent.py  # Crée l'exercice et les erreurs fréquentes
│   └── reviewer_agent.py           # Relit le brouillon et le résume
├── tools/
│   ├── file_writer.py              # Enregistre le fichier Markdown
│   └── validation.py               # Vérifie les sections obligatoires
├── output/
│   └── study_guide.md              # Fiche de révision générée
├── data/
│   └── topic_examples.json         # Exemples de sujets
├── config.py                       # Lit et vérifie les réglages du .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md                       # Documentation en anglais
├── README.fr.md                    # Documentation en français
└── main.py                         # Lance l'enchaînement complet
```

## Agents

Tous les agents utilisent le même modèle (`llama3.2`), avec un rôle et des
instructions différents.

| Agent | Ce qu'il reçoit | Ce qu'il produit (titres Markdown) |
|---|---|---|
| **Explicateur** (*Explainer*) | Le sujet | `Simple Explanation`, `Key Concepts`, `Example` |
| **Concepteur d'exercices** (*Practice Designer*) | Le sujet et l'explication | `Practice Exercise`, `Common Mistakes` |
| **Relecteur** (*Reviewer*) | Le brouillon complet | `Review Comments`, `Final Summary` |

L'enchaînement est séquentiel : chaque agent utilise le résultat du précédent.

```text
Sujet → Explicateur → Concepteur d'exercices → Brouillon → Relecteur
      → Markdown final → Validation → Enregistrement
```

## Outils

Les outils sont des fonctions Python classiques et **déterministes** : la même
entrée donne toujours le même résultat. Ils n'utilisent pas le modèle.

| Outil | Fichier | Rôle |
|---|---|---|
| `save_markdown_file()` | `tools/file_writer.py` | Crée le dossier parent si besoin, écrit le fichier Markdown et renvoie son chemin, ou un message clair commençant par `Error:`. |
| `validate_required_sections()` | `tools/validation.py` | Vérifie que les 8 titres obligatoires sont présents et renvoie `{"valid": ..., "missing": [...]}`. |

## Checklist d'auto-validation

- [x] **Tâche 0** : structure du projet créée (`agents/`, `tools/`, `output/`,
  `data/`, `README.md`, `requirements.txt`, `.env.example`, `.gitignore`,
  `main.py`).
- [x] **Tâche 1** : environnement virtuel, dépendances, Ollama et `llama3.2`
  installés ; le modèle répond en local.
- [x] **Tâche 2** : agent explicateur avec un rôle clair et des instructions
  précises, testé avec `Python decorators` et `HTTP status codes`.
- [x] **Tâche 3** : `save_markdown_file()` testée seule, puis utilisée pour
  enregistrer la sortie dans `output/`.
- [x] **Tâche 4** : `validate_required_sections()` renvoie le statut de
  validation et les sections manquantes.
- [x] **Tâche 5** : agent concepteur d'exercices basé sur le sujet et
  l'explication.
- [x] **Tâche 6** : agent relecteur qui commente sans réécrire la fiche.
- [x] **Tâche 7** : enchaînement séquentiel qui produit une fiche complète avec
  les 8 sections obligatoires.
- [x] **Tâche 8** : erreurs claires pour les variables manquantes, Ollama
  éteint, le modèle absent, le sujet vide, les erreurs d'écriture et l'échec de
  validation.
- [x] **Tâche 9** : README complété avec la réflexion et les limites connues.

## Réflexion

**1. Quelle est la différence entre un appel direct à un modèle et un agent IA ?**

Avec un appel direct, on pose une question au modèle et il répond, sans rôle
précis. Un agent, c'est le modèle configuré par mes soins : je lui donne un
rôle et des instructions précises (et éventuellement des outils), pour qu'il
fasse toujours le même type de travail de la même façon. En résumé : le modèle
est le cerveau ; l'agent, c'est le cerveau plus une fiche de poste plus des
outils.

**2. Quel rôle a chaque agent dans ton système ?**

Le premier agent répond par une explication du sujet demandé. Le deuxième crée
un exercice sur ce même sujet, avec les erreurs fréquentes des débutants. Le
dernier passe en revue les deux réponses précédentes (le brouillon), donne une
recommandation (approuver ou retravailler) et écrit le résumé final.

**3. Quel rôle a chaque outil dans ton système ?**

Le premier outil enregistre les réponses des agents directement dans un
fichier Markdown. Le second vérifie que la fiche générée contient toutes les
sections prédéfinies. Contrairement au modèle, ces outils sont
déterministes : l'IA écrit, le code vérifie et enregistre.

**4. Quelle a été la partie la plus difficile du projet ?**

La partie la plus difficile a été la vérification d'Ollama et du modèle
(tâche 8) : le code utilise des notions nouvelles pour moi, comme les requêtes
HTTP. Plus globalement, le projet introduit beaucoup d'outils nouveaux d'un
coup (ADK, LiteLLM, Ollama), et assembler toutes les étapes bout à bout demande
de garder beaucoup de choses en tête.

**5. Quelle limite as-tu observée avec le modèle choisi ?**

Principalement le temps de réponse : comme Ollama tourne sur le processeur
(aucune carte graphique utilisable sous WSL), chaque agent met un moment à
répondre, et l'enchaînement complet des trois agents prend environ
**45 secondes**.

## Limites connues

- **Vitesse** : sur processeur uniquement, une exécution complète prend
  environ 45 secondes.
- **Hallucinations** : le petit modèle invente parfois des détails. Pendant les
  tests, il a présenté des « Before / After / Surround decorators » comme des
  catégories de décorateurs (ce n'en sont pas), et les context managers comme
  un type de décorateur (c'est une notion différente).
- **Réponses non déterministes** : le même sujet ne donne pas toujours la même
  réponse. Une exécution peut produire une réponse vide ou oublier une section,
  et la relancer peut régler le problème.
- **Mise en forme irrégulière** : le modèle ne respecte pas toujours le niveau
  de titre demandé (par exemple `### Example` au lieu de `## Example`). C'est
  pour ça que le validateur accepte les deux niveaux.
- **Solutions dans les exercices** : le concepteur d'exercices donne parfois le
  code complet de la solution avec l'exercice.
- **Validation de la structure uniquement** : le validateur vérifie que les
  titres existent, pas que le contenu est juste ou utile.
- **Instructions en anglais** : les instructions et les titres sont en
  anglais ; un sujet ou des instructions dans une autre langue peuvent faire
  échouer la validation.

## Dépannage

| Problème | Message | Solution |
|---|---|---|
| Fichier `.env` absent ou incomplet | `RuntimeError: Missing environment variable: OLLAMA_API_BASE` | Lancer `cp .env.example .env` et vérifier les valeurs. |
| Ollama ne tourne pas | `RuntimeError: Ollama is not reachable at http://localhost:11434` | Le démarrer avec `ollama serve` (ou `sudo systemctl start ollama`). |
| Modèle non téléchargé | `RuntimeError: Model 'llama3.2' is not available` | Lancer `ollama pull llama3.2`. |
| Sujet vide | `ValueError: Topic cannot be empty.` | Taper un sujet, par exemple `Python decorators`. |
| Écriture du fichier impossible | `Error: could not save output/study_guide.md: ...` | Vérifier que le dossier `output/` est accessible en écriture. |
| Sections manquantes | `Warning: missing sections: ...` | Le modèle local n'est pas déterministe : relancer le projet. |

En cas d'erreur, lis la **dernière ligne** du message d'erreur : c'est là que
se trouve l'explication.

## Auteur

Thomas
