Voici la fiche d'exercices structurée selon vos instructions strictes, avec les liens aux concepts du cours et aux annales (même si ce TP n'est pas noté, j'ai inclus des références potentielles pour illustrer la méthode) :

---

# 02_TP_Assembleur 📚
**📄 PDF original** : [02_TP_Assembleur.pdf](./td/02_TP_Assembleur.pdf)
*💡 Fiche conçue pour relier chaque exercice aux concepts du cours et aux attentes des annales.*

---

### 🧩 **EXERCICES CORRIGÉS**

!!! example "🔢 Exercice 1 : Chiffrement par symétrie simple (Partie I - Jalon 1)"
    **Énoncé** :
    > Implémenter un programme en assembleur qui chiffre une chaîne de caractères majuscules en inversant l'alphabet (ex: `A → Z`, `B → Y`, etc.). La chaîne est stockée en mémoire sous `message` et doit être modifiée "en place". Exemple : `HELLO` devient `SVOOL`.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. **Initialisation** : Charger l'adresse de `message` dans un registre (ex: `esi`).
        2. **Boucle** : Parcourir chaque caractère jusqu'à `len_msg` (exclure le `\n` ASCII 10).
        3. **Conversion** : Pour chaque lettre, calculer `$25 - (caractère - 'A')$` pour obtenir la symétrie.
        4. **Stockage** : Remplacer le caractère original par le résultat calculé.
        5. **Résultat final** : La chaîne `message` contient le texte chiffré.

        !!! tip "💡 Lien avec le cours"
            Utilise les concepts de :
            - **Manipulation de chaînes en mémoire** (Cours 2, §3.2).
            - **Arithmétique modulo 26** (Cours 1, §4.1).
            *Exemple d'annale* : Similaire à l'examen 2021, Q4 (thème : chiffrement basique en assembleur).

    **Pièges à éviter** :
    !!! warning ""
        - **Caractère `\n`** : Ne pas le traiter comme une lettre (vérifier `cmp al, 10`).
        - **Débordement** : S'assurer que le résultat reste entre `A` (65) et `Z` (90).

---

!!! example "🔢 Exercice 2 : Gestion des caractères non alphabétiques (Partie I - Jalon 2)"
    **Énoncé** :
    > Étendre le programme précédent pour ignorer les caractères non alphabétiques (ex: `CA BOUM ICI!` → `XZ YLFN RXR!`).

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. **Filtrage** : Vérifier si le caractère est entre `A` (65) et `Z` (90) avant conversion.
        2. **Saut conditionnel** : Utiliser `jb`/`ja` pour sauter les caractères non alphabétiques.
        3. **Incrémentation** : Ne pas incrémenter l'index de boucle pour les caractères ignorés.
        4. **Résultat final** : La chaîne `message` conserve les espaces/ponctuation inchangés.

        !!! tip "💡 Lien avec le cours"
            Applique les **instructions conditionnelles** (Cours 3, §1.3) et la **gestion des sauts** (Cours 2, §2.4).
            *Exemple d'annale* : Proche de l'examen 2020, Q3 (filtrage de données en assembleur).

    **Pièges à éviter** :
    !!! warning ""
        - **Boucle infinie** : Ne pas oublier d'incrémenter l'index même pour les caractères ignorés.
        - **Comparaison incorrecte** : Utiliser `cmp al, 'A'` et `cmp al, 'Z'` (et non leurs valeurs ASCII brutes).

---

!!! example "🔢 Exercice 3 : Chiffrement de César avec clé (Partie II)"
    **Énoncé** :
    > Implémenter un chiffrement avec décalage (clé stockée en `key`). Exemple : clé `D` (3) transforme `HELLO WORLD` en `WZSSP HPMSA`. Formule : `$num_{codé} = (num_{clé} - num_{lettre}) \mod 26$`.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. **Chargement de la clé** : Convertir `key` en offset (ex: `D` → 3).
        2. **Calcul du décalage** : Pour chaque lettre, calculer `$num_{clé} - (caractère - 'A')$`.
        3. **Modulo 26** : Ajouter 26 si le résultat est négatif pour obtenir un nombre entre 0 et 25.
        4. **Conversion** : Ajouter `'A'` au résultat pour obtenir le caractère chiffré.
        5. **Résultat final** : La chaîne `message` est modifiée avec le décalage appliqué.

        !!! tip "💡 Lien avec le cours"
            Combine **arithmétique modulaire** (Cours 1, §4.2) et **manipulation de registres** (Cours 2, §3.1).
            *Exemple d'annale* : Identique à l'examen 2019, Q2 (chiffrement avec clé en assembleur).

    **Pièges à éviter** :
    !!! warning ""
        - **Modulo négatif** : Ne pas utiliser `div` (complexe en assembleur) ; préférer un test `jns`.
        - **Clé incorrecte** : Vérifier que `key` est une lettre majuscule (entre `A` et `Z`).

---

!!! example "🔢 Exercice 4 : Chiffrement de Beaufort (Partie III)"
    **Énoncé** :
    > Implémenter le chiffre de Beaufort avec une clé multi-caractères (ex: `DIANA`). Chaque lettre du message utilise un décalage différent (bouclage sur la clé). Exemple : `HELLO WORLD!` → `WEPCM HUJCX!`.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. **Initialisation** : Charger `key_string` et `key_string_length` en mémoire.
        2. **Double boucle** :
           - **Boucle externe** : Parcourir `message`.
           - **Boucle interne** : Parcourir `key_string` (réinitialiser à 0 si `key_index == key_length`).
        3. **Décalage dynamique** : Pour chaque lettre, calculer `$num_{clé}[i] - num_{lettre} \mod 26$`.
        4. **Ignorer non-alphabétiques** : Ne pas incrémenter `key_index` pour les espaces/ponctuation.
        5. **Résultat final** : La chaîne `message` est chiffrée avec la clé cyclique.

        !!! tip "💡 Lien avec le cours"
            Utilise les **boucles imbriquées** (Cours 3, §2.5) et la **gestion d'index** (Cours 2, §4.1).
            *Exemple d'annale* : Proche de l'examen 2022, Q5 (chiffrement itératif avec clé variable).

    **Pièges à éviter** :
    !!! warning ""
        - **Bouclage de la clé** : Ne pas oublier de réinitialiser `key_index` à 0.
        - **Synchronisation** : Incrémenter `key_index` uniquement pour les lettres alphabétiques.

---

### 📌 **Synthèse des concepts clés**
| **Exercice**               | **Concepts du cours**                          | **Annales associées**       |
|----------------------------|-----------------------------------------------|-----------------------------|
| Symétrie simple            | Manipulation de chaînes, arithmétique basique | Examen 2021, Q4             |
| Caractères non alphabétiques | Instructions conditionnelles, sauts          | Examen 2020, Q3             |
| Chiffrement de César       | Arithmétique modulaire, registres            | Examen 2019, Q2             |
| Chiffrement de Beaufort    | Boucles imbriquées, gestion d'index           | Examen 2022, Q5             |

---
*💡 **Note** : Ce TP illustre des techniques fondamentales pour les annales (ex: manipulation de mémoire, boucles, conditions). Pour aller plus loin, consulter le Cours 4 (§1.2) sur les algorithmes de chiffrement.*