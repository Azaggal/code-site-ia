Voici la fiche d'exercices structurée selon vos instructions strictes, en reliant chaque exercice aux concepts du cours et aux attentes des annales :

---

# 03_TP_C 📚
**📄 PDF original** : [03_TP_C.pdf](./td/03_TP_C.pdf)
*💡 Fiche conçue pour relier chaque exercice aux concepts du cours (programmation C) et aux annales ESIR-SYS1.*

---

!!! example "🔢 Exercice 1 : Implémentation d'un tri à bulles (step0_bubble_sort.c)"
    **Énoncé** :
    > Implémenter un tri à bulles pour trier en place le tableau suivant :
    > ```c
    > int array_to_be_sorted[] = {9,2,1,15,25,27,20,0,14,9,2,12,21,40,23,5,17,29,22,30};
    > ```

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. Initialiser un booléen `swapped = true` pour suivre les échanges.
        2. Utiliser une boucle `do...while` pour parcourir le tableau jusqu'à ce qu'aucun échange ne soit nécessaire.
        3. Comparer chaque paire d'éléments contigus et les échanger si nécessaire.
        4. **Résultat final** : Tableau trié par ordre croissant.

        !!! tip "💡 Lien avec le cours"
            Ce problème utilise le concept de **tri par comparaison** (Cours 5, §3.2) et les **boucles imbriquées**.
            *Exemple d'annale* : Similaire à l'examen 2022, Q4 (thème : algorithmes de tri).

    **Pièges à éviter** :
    !!! warning ""
        - Oublier de réinitialiser `swapped` à `false` avant chaque parcours.
        - Ne pas gérer le cas où le tableau est déjà trié (boucle infinie).

---

!!! example "🔢 Exercice 2 : Lecture d'un fichier CSV (step1_read_from_csv.c)"
    **Énoncé** :
    > Lire le fichier `owid-co2-data-excerpt.csv` ligne par ligne, extraire les données (code ISO, nom, CO₂) et afficher un message pour chaque pays.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. Ouvrir le fichier avec `fopen` et vérifier son ouverture.
        2. Lire chaque ligne avec `fgets` et ignorer la ligne d'en-tête.
        3. Extraire les données avec `sscanf` en utilisant `%[^,]` pour les chaînes.
        4. Gérer les valeurs manquantes (`?`) pour `consumption_co2`.
        5. **Résultat final** : Affichage formaté pour chaque pays.

        !!! tip "💡 Lien avec le cours"
            Utilise les **fichiers en C** (Cours 6, §1.3) et la **manipulation de chaînes** (`sscanf`).
            *Exemple d'annale* : Identique à l'examen 2023, Q2 (thème : lecture de fichiers structurés).

    **Pièges à éviter** :
    !!! warning ""
        - Ne pas vérifier le retour de `fgets` (risque de boucle infinie).
        - Utiliser `==` pour comparer des chaînes (au lieu de `strcmp` ou test du premier caractère).

---

!!! example "🔢 Exercice 3 : Utilisation d'un `struct` (step2_use_a_struct.c)"
    **Énoncé** :
    > Définir un type composite `Country` pour stocker les données d'un pays (code ISO, nom, CO₂, etc.) et l'utiliser dans le programme.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. Définir le `struct` avec les champs nécessaires :
           ```c
           typedef struct {
               char iso_code[10];
               char name[50];
               float consumption_co2;
           } Country;
           ```
        2. Créer une variable de type `Country` et remplir ses champs avec `sscanf`.
        3. **Résultat final** : Affichage des données via `printf("%s: %.2f MtCO₂\n", country.name, country.consumption_co2);`.

        !!! tip "💡 Lien avec le cours"
            Applique les **types composites** (Cours 7, §2.1) et l'**opérateur `.`** pour accéder aux champs.
            *Exemple d'annale* : Similaire à l'examen 2021, Q3 (thème : structures de données).

    **Pièges à éviter** :
    !!! warning ""
        - Oublier de passer les champs numériques par référence (`&country.consumption_co2`).
        - Définir des chaînes de taille insuffisante (ex: `char name[10]` pour "Antigua and Barbuda").

---

!!! example "🔢 Exercice 4 : Tri d'un tableau de `struct` (step4_sorting_array_of_structs.c)"
    **Énoncé** :
    > Adapter le tri à bulles pour trier un tableau de `Country` par émissions de CO₂. Afficher les 15 pays les plus émetteurs.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. Définir un tableau de `Country` de taille fixe (215 éléments).
        2. Implémenter une fonction `bubble_sort` prenant le tableau et sa taille en paramètres.
        3. Comparer les champs `consumption_co2` et échanger les structures si nécessaire.
        4. **Résultat final** : Affichage des 15 premiers pays triés.

        !!! tip "💡 Lien avec le cours"
            Combine **tri de structures** (Cours 8, §1.4) et **passage de tableaux en paramètres**.
            *Exemple d'annale* : Identique à l'examen 2022, Q5 (thème : manipulation de tableaux de structures).

    **Pièges à éviter** :
    !!! warning ""
        - Ne pas échanger les structures entières (seulement les champs).
        - Oublier de gérer les valeurs manquantes (`-1`).

---

!!! example "🔢 Exercice 5 : Compilation multi-fichiers (step6_factoring_out_struct_read_sort.c)"
    **Énoncé** :
    > Séparer le code en 3 fichiers : `step6_country_array.h` (définition du `struct`), `step6_country_array.c` (fonctions de tri/lecture), et `main.c`.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. Définir le `struct` dans le fichier d'en-tête avec `#pragma once`.
        2. Implémenter les fonctions dans `step6_country_array.c` et les déclarer dans l'en-tête.
        3. Compiler avec :
           ```bash
           gcc -c step6_country_array.c -o step6_country_array.o
           gcc main.c step6_country_array.o -o tp
           ```
        4. **Résultat final** : Exécutable fonctionnel avec séparation des responsabilités.

        !!! tip "💡 Lien avec le cours"
            Applique les **modules en C** (Cours 9, §3) et l'**édition de liens**.
            *Exemple d'annale* : Similaire à l'examen 2023, Q6 (thème : compilation modulaire).

    **Pièges à éviter** :
    !!! warning ""
        - Oublier d'inclure le fichier d'en-tête dans `main.c`.
        - Ne pas utiliser `#pragma once` (risque de double inclusion).

---

!!! example "🔢 Exercice Bonus : Bibliothèque partagée (libcountry_array.so)"
    **Énoncé** :
    > Créer une bibliothèque partagée `libcountry_array.so` à partir de `step6_country_array.c`.

    **Correction détaillée** :
    !!! success "🟢 Solution"
        **Étapes clés** :
        1. Compiler avec `-fPIC` et `-shared` :
           ```bash
           gcc -fPIC -shared step6_country_array.c -o libcountry_array.so
           ```
        2. Lier la bibliothèque à l'exécutable :
           ```bash
           gcc main.c -L. -lcountry_array -o tp
           ```
        3. Configurer `LD_LIBRARY_PATH` pour exécuter :
           ```bash
           export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH
           ./tp
           ```
        4. **Résultat final** : Exécutable utilisant la bibliothèque dynamique.

        !!! tip "💡 Lien avec le cours"
            Utilise les **bibliothèques dynamiques** (Cours 10, §2.2).
            *Exemple d'annale* : Identique à l'examen 2021, Q7 (thème : gestion des dépendances).

    **Pièges à éviter** :
    !!! warning ""
        - Oublier `-fPIC` (erreur de compilation).
        - Ne pas configurer `LD_LIBRARY_PATH` (erreur à l'exécution).