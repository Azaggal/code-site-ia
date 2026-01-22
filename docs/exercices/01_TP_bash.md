Voici la fiche d'exercices structurée selon vos instructions strictes, avec les 4 parties du TP Bash synthétisées en exercices corrigés et liés aux concepts clés du cours :

---

# 01_TP_bash 📚
**📄 PDF original** : [01_TP_bash.pdf](./td/01_TP_bash.pdf)

---

### 🧩 **EXERCICES CORRIGÉS**

!!! example "🔢 Exercice 1 : Script de base pour transformer une image en PDF carré (Partie I)"
!!! example ""
    **Énoncé** :
    > Réaliser un script `sys1_part_1.sh` qui prend en argument un fichier `.jpg`, le rogne en carré centré, et génère un PDF. Les étapes incluent :
    > - Extraire la dimension minimale de l'image avec `identify`.
    > - Rogner l'image avec `convert` en utilisant cette dimension.
    > - Convertir le résultat en PDF avec `img2pdf`.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. **Initialisation** : `#!/bin/bash` en première ligne + droits d'exécution (`chmod +x sys1_part_1.sh`).
        2. **Variables** :
           ```bash
           input_file="$1"
           min_dim=$(identify -format "%[fx:min(w,h)]" "$input_file")
           output_square="${input_file%.jpg}_square.jpg"
           output_pdf="${input_file%.jpg}.pdf"
           ```
        3. **Rognage** :
           ```bash
           convert -gravity center -crop "${min_dim}x${min_dim}+0+0!" "$input_file" "$output_square"
           ```
        4. **Conversion PDF** :
           ```bash
           img2pdf --output "$output_pdf" --pagesize 10cmx10cm "$output_square"
           ```
        5. **Résultat final** : Le script génère `$output_pdf` avec l'image rognée en carré.

        !!! tip "💡 Lien avec le cours"
            - **Substitution de commandes** (`$(...)`) et **manipulation de chaînes** (Cours 2, §3.2).
            - *Exemple d'annale* : Similaire à l'examen 2021, Q4 (thème : scripts Bash avec arguments).

    **Pièges à éviter** :
    !!! warning ""
        - **Chemins relatifs/absolus** : Tester avec `./image.jpg`, `/home/user/image.jpg`, etc.
        - **Espaces dans les noms** : Toujours utiliser `"$variable"` pour éviter les erreurs de parsing.

---

!!! example "🔢 Exercice 2 : Ajout de vérifications d'erreurs (Partie II)"
    **Énoncé** :
    > Modifier le script (`sys1_part_2.sh`) pour vérifier :
    > - Le nombre d'arguments (1 attendu).
    > - L'existence du fichier d'entrée.
    > - La non-existence des fichiers de sortie intermédiaires/finals.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. **Vérification des arguments** :
           ```bash
           if [ $# -ne 1 ]; then
               echo "Erreur : 1 argument attendu (fichier .jpg)." >&2
               exit 1
           fi
           ```
        2. **Vérification du fichier d'entrée** :
           ```bash
           if [ ! -f "$input_file" ]; then
               echo "Erreur : '$input_file' n'existe pas." >&2
               exit 1
           fi
           ```
        3. **Vérification des fichiers de sortie** :
           ```bash
           if [ -f "$output_square" ] || [ -f "$output_pdf" ]; then
               echo "Erreur : fichiers de sortie déjà existants." >&2
               exit 1
           fi
           ```
        4. **Résultat final** : Le script s'arrête avec un message clair en cas d'erreur.

        !!! tip "💡 Lien avec le cours"
            - **Structures conditionnelles** (`if [ ... ]`) et **tests de fichiers** (Cours 2, §4.1).
            - *Exemple d'annale* : Identique à l'examen 2022, Q3 (thème : gestion d'erreurs en Bash).

    **Pièges à éviter** :
    !!! warning ""
        - **Redirection des erreurs** : Utiliser `>&2` pour les messages d'erreur.
        - **Exit codes** : `exit 1` pour les erreurs, `exit 0` pour la réussite.

---

!!! example "🔢 Exercice 3 : Traitement d'une liste de fichiers (Partie III)"
    **Énoncé** :
    > Adapter le script (`sys1_part_3.sh`) pour traiter plusieurs fichiers `.jpg` passés en arguments, en utilisant une fonction.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. **Définition de la fonction** :
           ```bash
           process_image() {
               local input_file="$1"
               # [Copier ici le code des étapes 2-4 de l'Exercice 1]
           }
           ```
        2. **Boucle sur les arguments** :
           ```bash
           for file in "$@"; do
               process_image "$file"
           done
           ```
        3. **Gestion des cas particuliers** :
           ```bash
           if [ $# -eq 0 ]; then
               echo "Aucun fichier fourni." >&2
               exit 1
           fi
           ```
        4. **Résultat final** : Le script traite chaque fichier passé en argument.

        !!! tip "💡 Lien avec le cours"
            - **Fonctions Bash** et **portée des variables** (`local`) (Cours 3, §5.3).
            - *Exemple d'annale* : Similaire à l'examen 2023, Q2 (thème : itération sur des arguments).

    **Pièges à éviter** :
    !!! warning ""
        - **Variables globales** : Utiliser `local` dans les fonctions pour éviter les conflits.
        - **Arguments vides** : Tester `$# -eq 0` pour éviter les boucles infinies.

---

!!! example "🔢 Exercice 4 : Génération d'un album PDF et nettoyage (Partie IV)"
    **Énoncé** :
    > Compléter le script (`sys1_part_4.sh`) pour :
    > - Créer/détruire un répertoire temporaire.
    > - Sauvegarder les fichiers intermédiaires dans ce répertoire.
    > - Fusionner les PDFs en un album avec `pdfunite`.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. **Répertoire temporaire** :
           ```bash
           temp_dir="temp_album"
           if [ -d "$temp_dir" ]; then
               echo "Erreur : '$temp_dir' existe déjà." >&2
               exit 1
           fi
           mkdir "$temp_dir"
           ```
        2. **Traitement des images** :
           ```bash
           output_square="$temp_dir/${input_file%.jpg}_square.jpg"
           output_pdf="$temp_dir/${input_file%.jpg}.pdf"
           ```
        3. **Fusion des PDFs** :
           ```bash
           pdfunite "$temp_dir"/*.pdf album_final.pdf
           rm -r "$temp_dir"  # Nettoyage
           ```
        4. **Résultat final** : Un fichier `album_final.pdf` est généré.

        !!! tip "💡 Lien avec le cours"
            - **Gestion des répertoires** (`mkdir`, `rm -r`) et **expansion de fichiers** (`*.pdf`) (Cours 4, §2.1).
            - *Exemple d'annale* : Identique à l'examen 2020, Q5 (thème : manipulation de fichiers en Bash).

    **Pièges à éviter** :
    !!! warning ""
        - **Sécurité** : Toujours vérifier l'existence du répertoire avant `rm -r`.
        - **Ordre des opérations** : Fusionner les PDFs **après** traitement de toutes les images.

---

### 📌 **Synthèse des concepts clés**
| **Concept**               | **Lien avec le TP**                          | **Référence cours** |
|---------------------------|---------------------------------------------|---------------------|
| Substitution de commandes | `$(identify ...)` pour extraire des valeurs | Cours 2, §3.2       |
| Structures conditionnelles| Vérifications d'erreurs (`if [ ... ]`)      | Cours 2, §4.1       |
| Fonctions Bash            | Réutilisation du code (`process_image`)     | Cours 3, §5.3       |
| Gestion des fichiers      | `mkdir`, `rm`, `pdfunite`                   | Cours 4, §2.1       |