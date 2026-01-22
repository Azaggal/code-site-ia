import os
from pathlib import Path
import re
import fitz
from mistralai import Mistral

# --- CONFIGURATION ---
API_KEY = "Or0xeFkf3TTDOcwQC1wkFICk0WEeN4eb"  # Remplace par ta clé Mistral
client = Mistral(api_key=API_KEY)

# Dossiers d'entrée et de sortie
base_in = Path("docs")
base_out = Path("docs")

FICHES_REVISION_DIR = base_out / "fiches_revision"
FICHES_REVISION_DIR.mkdir(parents=True, exist_ok=True)

def extraire_texte(pdf_path):
    """Extrait le texte d'un PDF"""
    return " ".join([page.get_text() for page in fitz.open(pdf_path)])

def extraire_concepts_cles(texte, n=5):
    """Extrait les concepts clés d'un texte (noms propres, termes techniques)"""
    # Expression régulière pour capturer les termes en MAJUSCULES, mots-clés techniques, etc.
    pattern = r'\b[A-Z]{2,}[A-Za-z0-9\-_]*(?:\s[A-Z]{2,}[A-Za-z0-9\-_]*)*\b'
    concepts = re.findall(pattern, texte)
    # Filtrer les concepts trop courts ou génériques
    return list(set([
        c for c in concepts
        if len(c) > 3 and c.lower() not in {"le", "la", "les", "et", "des", "une", "pour"}
    ]))[:n]

def trouver_occurrences(concept, texte):
    """Trouve toutes les occurrences d'un concept dans un texte"""
    pattern = re.compile(rf'\b{re.escape(concept)}\b', re.IGNORECASE)
    return [m.start() for m in pattern.finditer(texte)]

def count_tokens(text):
    """Estime le nombre de tokens dans un texte (approximation)"""
    return len(text.split()) + len(text) // 4

def decouper_texte(texte, max_tokens=8000):
    paragraphs = texte.split('\n\n')  # Découpe par paragraphes
    chunks = []
    current_chunk = []
    current_length = 0

    for p in paragraphs:
        p_length = count_tokens(p)
        if current_length + p_length > max_tokens and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(p)
        current_length += p_length
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    return chunks

def generer(prompt, fichier_nom, sous_dossier):
    """Envoie au LLM Mistral et enregistre dans le bon dossier"""
    print(f"🧠 Traitement de {fichier_nom} -> {sous_dossier}...")
    print(f"Tokens estimés : {count_tokens(prompt)}")
    target_dir = base_out / sous_dossier
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        chat_response = client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = chat_response.choices[0].message.content
        with open(target_dir / f"{fichier_nom}.md", "w", encoding="utf-8") as f:
            f.write(response_text)
    except Exception as e:
        print(f"⚠️ Erreur pour {fichier_nom}: {e}")


def generer_fiche_revision(concept, extrait_cours, extrait_annale, annale_pdf_path):
    """Génère une fiche de révision pour un concept"""
    prompt = f"""
    Voici un concept clé extrait d'une annale : {concept}.

    Extrait du cours/TD où ce concept est expliqué :
    {extrait_cours[:2000]}

    Extrait de l'annale où ce concept est utilisé :
    {extrait_annale[:2000]}

    Génère une fiche de révision structurée comme suit :

    # {concept}
    **Source** : [Annale originale](./pdf/{annale_pdf_path.name})

    ## Explication (Cours/TD)
    [Explication claire et concise du concept, avec exemples si présents]

    ## Application (Annale)
    [Comment le concept est utilisé dans l'annale, pièges éventuels, attentes du correcteur]

    ## À retenir
    - [Liste des points clés à mémoriser]
    - [Erreurs fréquentes à éviter]
    """
    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erreur pour {concept}: {e}")
        return None

def main():
    # 1. TRAITEMENT DES COURS (SYNTHÈSE)
    dir_theorie = base_in / "cours" / "cm"
    cours_index = {}
    if dir_theorie.exists():
        for pdf in dir_theorie.glob("*.pdf"):
            cours_index[pdf.stem] = extraire_texte(pdf)
            if not Path(f"./docs/cours/{pdf.stem}.md").exists():

                texte = "".join([page.get_text() for page in fitz.open(pdf)])
                chunks = decouper_texte(texte)
                for i, chunk in enumerate(chunks):
                    prompt = f"""
                        **INSTRUCTIONS PRÉCISES POUR LA CRÉATION DE LA FICHE** :

                        1. **Structure OBLIGATOIRE** (à respecter scrupuleusement) :
                        # Titre du cours
                        **Lien vers le PDF source** : [{pdf.stem}.pdf](./cm/{pdf.name})

                        ---

                        2. **Contenu principal** :
                        - Résume le texte en **paragraphe courts** (max 5 lignes)
                        - Utilise **uniquement des mots en gras** pour :
                        - Les **définitions** (ex: Une **matrice** est...)
                        - Les **formules** (ex: **det(A) = ...**)
                        - Les **concepts clés** (max 3 par paragraphe)

                        ---

                        !!! warning "⚠️ Points d'attention"  <!-- Section OPTIONNELLE -->
                            - [Piège 1] : [Description en 1 phrase max. Exemple : "Confondre **rang** et **dimension** d'une matrice."]
                            - [Piège 2] : [Autre erreur fréquente, si pertinente]
                            - [Piège 3] : [Seulement si 3 pièges majeurs dans le texte]
                            *⚠️ Cette section n'apparaît QUE si le texte contient des pièges évidents ou des concepts difficiles. Sinon, NE PAS l'inclure.*

                        ---

                        4. **Quiz** (OBLIGATOIRE mais flexible) :
                            [Entre **1 et 5 questions max** - priorise la qualité sur la quantité]
                            Format strict :
                            <details>
                            <summary>🔍 Question 1 : [Question sur le concept principal]</summary>
                            [Réponse concise en 2-3 phrases max]
                            </details>
                            <!-- Ajoute d'autres questions UNIQUEMENT si elles apportent une réelle valeur pédagogique -->
                            *Règles* :
                            - Chaque question doit tester un point différent
                            - Pas de questions redondantes
                            - Priorité aux concepts clés du chunk

                        ---
                        **TEXTE À SYNTHÉTISER** :
                        {chunk}

                        ---
                        **CONSIGNES NON-NÉGOCIABLES** :
                        1. **Section "Points d'attention"** :
                        - NE PAS l'inclure si le texte ne contient pas de pièges évidents
                        - Si inclusion, MAXIMUM 3 points

                        2. **Quiz** :
                        - MINIMUM 1 question (obligatoire)
                        - MAXIMUM 5 questions (mieux vaut 2-3 questions pertinentes que 5 questions forcées)
                        - Les questions doivent être **directement liées au contenu du chunk**

                        3. **Style** :
                        - Phrases courtes (max 20 mots)
                        - Pas de jargon inutile
                        - Exemples concrets si possible
                        - quand tu énumères, créer des listes à puces pour plus de clarté
                        - Ne Pas écrire les pièges en dehors du warning
                        """
                    generer(prompt, f"{pdf.stem}", "cours")

    # 2. TRAITEMENT DES TD (EXERCICES)
    dir_td = base_in / "exercices" / "td"
    td_index = {}
    if dir_td.exists():
        for pdf in dir_td.glob("*.pdf"):
            td_index[pdf.stem] = extraire_texte(pdf)
            if not (base_out / "exercices" / f"{pdf.stem}.md").exists():
                

                texte = "".join([page.get_text() for page in fitz.open(pdf)])
                chunks = decouper_texte(texte)
                for i, chunk in enumerate(chunks):
                    prompt = f"""
                                **INSTRUCTIONS STRICTES POUR LA FICHE D'EXERCICES** *(liée aux annales et cours)*

                                ---
                                ### 📝 **STRUCTURE OBLIGATOIRE POUR LES EXERCICES**
                                # Titre du sujet 📚
                                **📄 PDF original** : [{pdf.stem}.pdf](./td/{pdf.name})
                                *💡 Fiche conçue pour relier chaque exercice aux concepts du cours et aux attentes des annales.*

                                ---

                                ### 🧩 **EXERCICES CORRIGÉS** *(un bloc par exercice)*
                                !!! example "🔢 Exercice 1 : [Titre clair de l'exercice]"
                                    **Énoncé** :
                                    > [Énoncé exact de l'exercice, extrait du PDF. Utilise **$...$** pour les formules LaTeX]

                                    **Correction détaillée** :
                                    !!! success "🟢 Solution"  <!-- Balise verte pour la réponse -->
                                        **Étapes clés** :
                                        1. [Étape 1 avec explication concise]
                                        2. [Étape 2 avec **mots-clés en gras**]
                                        3. **Résultat final** : $formule\_latex$  <!-- Ex: $\boxed{{x=2}}$ -->

                                        !!! tip "💡 Lien avec le cours"
                                            Ce problème utilise le concept de **[concept clé]** (voir cours [référence]).
                                            *Exemple d'annale* : Ce type de question est tombé en [année] (ex: 2023, Q3).

                                    **Pièges à éviter** :
                                    !!! warning ""
                                        - [Erreur 1] : [Explication courte]
                                        - [Erreur 2] : [Exemple concret]

                                ---
                                **TEXTE À SYNTHÉTISER** (contient les exercices) :
                                {chunk}

                                ---
                                ### **CONSIGNES ABSOLUES**
                                1. **Format des réponses** :
                                - **Balise verte** (`!!! success`) **obligatoire** pour chaque solution.
                                - **LaTeX** pour TOUTES les formules : `$\int f(x)dx$` → $\int f(x)dx$.
                                - **Étapes numérotées** (1., 2., 3.) avec **1 phrase max par étape**.

                                2. **Lien avec les annales** :
                                - Ajoute **1 référence à une annale** par exercice (si pertinent).
                                - Exemple : *"Similaire à l'examen 2022, Q2 (thème : [thème])."*

                                3. **Exemple de sortie valide** :
                                ```markdown
                                !!! example "🔢 Exercice 1 : Calcul de déterminant"
                                    **Énoncé** :
                                    > Soit $A = \begin{{pmatrix}}1 & 2\\3 & 4\end{{pmatrix}}$. Calculer $det(A)$.

                                    !!! success "🟢 Solution"
                                        1. Appliquer la formule : $det(A) = ad - bc$.
                                        2. Substituer : $det(A) = (1)(4) - (2)(3) = -2$.
                                        3. **Résultat** : $\boxed{{-2}}$.

                                    !!! tip "💡 Lien avec le cours"
                                        Utilise la propriété des **matrices 2x2** (Cours 3, §2).
                                        *Exemple d'annale* : Identique à l'examen 2023, Q1b.
                        """
                    generer(prompt, f"{pdf.stem}", "exercices")

    # 3. TRAITEMENT DES ANNALES (RÉVISIONS CIBLÉES)
    dir_annales = base_in / "revisions" / "annales"
    if dir_annales.exists():
        for pdf in dir_annales.glob("*.pdf"):
            if not (base_out / "revisions" / f"{pdf.stem}.md").exists():
                texte = "".join([page.get_text() for page in fitz.open(pdf)])
                chunks = decouper_texte(texte)
                for i, chunk in enumerate(chunks):
                    prompt = f"""
                        **INSTRUCTIONS POUR LA FICHE D'ANALYSE D'ANNALE** *(liée aux cours/TD et optimisée pour la révision)*

                        ---
                        ### 📝 **STRUCTURE OBLIGATOIRE POUR LES ANNALES**
                        # {pdf.stem} 📄 (Annale {pdf.stem.split('_')[-1][:4]})  <!-- Ex: "Annale 2023" -->
                        **📄 PDF original** : [{pdf.stem}.pdf](./annales/{pdf.name})
                        *💡 Cette fiche relie chaque question d'examen aux concepts du cours et aux TDs.*

                        ---

                        ### 🎯 **ANALYSE GLOBALE**
                        !!! note "📊 Statistiques"
                            - **Thèmes abordés** : [Liste des 3-5 thèmes principaux, ex: "Algèbre linéaire (40%), Graphes (30%)"]
                            - **Types de questions** : [QCM, démonstrations, applications...]
                            - **Pièges fréquents** : [1-2 pièges récurrents dans cette annale]

                        ---
                        ### 🧩 **QUESTIONS DÉTAILLÉES** *(une par section)*
                        !!! example "🔢 Question 1 : [Titre clair extrait de l'annale]"
                            **Énoncé original** :
                            > [Texte exact de la question, avec **formules en $...$**]

                            **Correction et liens** :
                            !!! success "🟢 Solution"
                                1. **Méthode** : [Technique utilisée, ex: "Diagonalisation"]
                                2. **Étapes** : [Résolution détaillée]
                                3. **Résultat** : `$\boxed{{resultat}}$`  <!-- Accolades doublées -->

                            !!! tip "💡 Liens utiles"
                                - **Cours associé** : [Nom du cours] (voir [section])
                                - **TD similaire** : [Exercice X du TD Y]
                                - **Points clés** : [Concepts à retenir pour cette question]

                            !!! warning "⚠️ Pièges"
                                - [Erreur classique] : [Explication]
                                - **Conseil** : [Comment l'éviter]

                        ---
                        ### 📊 **SYNTHÈSE POUR LA RÉVISION**
                        !!! note "📌 À retenir"
                            - [Top 3 des concepts tombés]
                            - [1 question type à maîtriser]
                            - [1 méthode réutilisable]

                        ---
                        **TEXTE DE L'ANNALE À ANALYSER** :
                        {chunk}

                        ---
                        ### **CONSIGNES SPÉCIFIQUES POUR LES ANNALES**
                        1. **Structure** :
                        - **1 bloc par question** avec :
                            - Énoncé **fidèle** à l'annale
                            - Solution en **balise verte** (`!!! success`)
                            - **Liens explicites** vers cours/TD (ex: "Comme dans TD3, Q2")
                            - tu dois absolument traiter **toutes les questions**

                        2. **Exemple de sortie** :
                        ```markdown
                        !!! example "🔢 Question 2 : Matrices et applications linéaires"
                            **Énoncé original** :
                            > Soit $A \in M_n(\mathbb{{R}})$. Montrer que $A$ est inversible ssi $det(A) \neq 0$.

                            !!! success "🟢 Solution"
                                1. Utiliser la **caractérisation du déterminant** (Cours 4, §3).
                                2. **Preuve** : $A$ inversible ⇔ $\exists B, AB=I_n$ ⇔ $det(A) \neq 0$.
                                3. **Conclusion** : `$\boxed{{\text{{A inversible}} \Leftrightarrow \det(A) \neq 0}}$`

                            !!! tip "💡 Liens"
                                - **Cours** : "Déterminants et inversibilité" (Chapitre 4)
                                - **TD** : Exercice 5 (matrices inversibles)
                                - **Astuce** : Toujours vérifier le déterminant en premier !
                        """
                    generer(prompt, f"{pdf.stem}", "revisions")

                
                texte = "".join([page.get_text() for page in fitz.open(pdf)])
                chunks = decouper_texte(texte)

                annale_text = extraire_texte(pdf)
                concepts = extraire_concepts_cles(annale_text)

            # # 3. Pour chaque concept, trouver dans cours/TD
            #     for concept in concepts:
            #         # Chercher dans les cours
            #         for cours_nom, cours_text in cours_index.items():
            #             if concept.lower() in cours_text.lower():
            #                 occurrences = trouver_occurrences(concept, cours_text)
            #                 for pos in occurrences[:1]:  # Prendre la première occurrence
            #                     extrait_cours = cours_text[max(0, pos-200):pos+800]  # Contexte autour

            #                     # Générer la fiche
            #                     fiche_content = generer_fiche_revision(
            #                         concept,
            #                         extrait_cours,
            #                         annale_text,
            #                         pdf
            #                     )
            #                     if fiche_content:
            #                         with open(FICHES_REVISION_DIR / f"{pdf.stem}_{concept}.md", "w", encoding="utf-8") as f:
            #                             f.write(fiche_content)
            #                             f.write(f"\n[PDF de l'annale](./pdf/{pdf.name})\n")

            #         # Chercher dans les TD
            #         for td_nom, td_text in td_index.items():
            #             if concept.lower() in td_text.lower():
            #                 occurrences = trouver_occurrences(concept, td_text)
            #                 for pos in occurrences[:1]:
            #                     extrait_td = td_text[max(0, pos-200):pos+800]
            #                     fiche_content = generer_fiche_revision(
            #                         concept,
            #                         extrait_td,
            #                         annale_text,
            #                         pdf
            #                     )
            #                     if fiche_content:
            #                         with open(FICHES_REVISION_DIR / f"{pdf.stem}_{concept}_td.md", "w", encoding="utf-8") as f:
            #                             f.write(fiche_content)
            #                             f.write(f"\n[PDF de l'annale](./pdf/{pdf.name})\n")

                


            

    print("\n✅ Bravo ! Ton site a été structuré par catégories.")

if __name__ == "__main__":
    main()
