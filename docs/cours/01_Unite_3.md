# Introduction aux Systèmes d'Exploitation : Scripting

**Lien vers le PDF source** : [01_Unite_3.pdf](./cm/01_Unite_3.pdf)

---

## **Variables Shell et Variables d'Environnement**
- Une **variable shell** est définie avec `=` (sans espaces). Exemple : `MA_VARIABLE="valeur"`.
- Pour récupérer sa valeur, on utilise `$` : `echo $MA_VARIABLE`.
- Les **variables shell** sont locales à une instance de shell.

- Une **variable d'environnement** est gérée par l'**OS** et héritée par les processus enfants.
- En **Java**, on les récupère via `System.getenv()`. En **C**, via `getenv()`.
- La commande `export` transforme une variable shell en variable d'environnement.

## **Commande `$PATH`**
- `$PATH` est une **variable d'environnement** listant les répertoires où chercher les exécutables.
- Exemple : `echo $PATH` affiche `/usr/bin:/bin:...`.
- La commande `which` localise un exécutable dans `$PATH`.

## **Substitutions en Ligne de Commande**
- Le shell interprète les commandes en plusieurs étapes :
  - Expansion des **wildcards** (`*`, `?`, `[..]`).
  - Substitution des **variables** (`$VAR`).
  - Exécution des commandes imbriquées (`` `cmd` `` ou `$(cmd)`).
- Exemple : `ls *.java` liste tous les fichiers `.java`.

### **Globbing (Wildcards)**
- `*` : séquence de caractères quelconque.
- `?` : un seul caractère.
- `[abc]` : un caractère parmi `a`, `b` ou `c`.
- Exemple : `rm exp?.txt` supprime `exp1.txt`, `expA.txt`, etc.

## **Guillemets et Substitutions**
- `` `cmd` `` ou `$(cmd)` : exécute `cmd` et remplace par son résultat.
- `"..."` : conserve les espaces, mais substitue les variables.
- `'...'` : interdit toute substitution (variables, globbing, commandes).

## **Scripting Shell**
- Un **script shell** est un fichier texte contenant des commandes shell.
- Pour l'exécuter :
  - `source script.sh` : dans le shell courant.
  - `sh script.sh` : dans un sous-shell.
  - Avec un **shebang** (`#!/bin/sh`) et `chmod u+x script.sh` pour le rendre exécutable.

### **Arguments dans les Scripts**
- `$0` : nom du script.
- `$1`, `$2`, ... : arguments positionnels.
- `$#` : nombre d'arguments.
- `$@` : tous les arguments (respecte les espaces si entre guillemets).
- `$*` : tous les arguments (fusionne les espaces).

### **Structures de Contrôle**
- **Boucles** :
  ```bash
  for i in "$@"; do echo "$i"; done
  ```
- **Tests** :
  ```bash
  if [ -e "$fichier" ]; then echo "Existe"; fi
  ```
  - Attention aux espaces autour de `[`, `]`, et des opérateurs (`-ge`, `-e`).

---

## **Quiz**
<details>
<summary>🔍 Question 1 : Quelle est la différence entre une variable shell et une variable d'environnement ?</summary>
Une **variable shell** est locale à une instance de shell et n'est pas héritée par les processus enfants. Une **variable d'environnement** est gérée par l'OS et transmise aux processus enfants (via `export` ou `setenv` en C).
</details>

<details>
<summary>🔍 Question 2 : Que fait la commande `ls *.txt` et qui effectue l'expansion ?</summary>
`ls *.txt` liste tous les fichiers avec l'extension `.txt`. L'expansion est effectuée par le **shell** (via **globbing**), pas par la commande `ls`.
</details>

<details>
<summary>🔍 Question 3 : Pourquoi utiliser `"$@"` plutôt que `$*` dans un script ?</summary>
`"$@"` préserve les espaces dans les arguments (ex: `"fichier 1.txt"` reste un seul argument). `$*` fusionne les arguments en une seule chaîne, ce qui peut casser les noms de fichiers avec espaces.
</details>

<details>
<summary>🔍 Question 4 : Comment rendre un script exécutable et l'appeler sans `sh` ?</summary>
1. Ajouter un **shebang** (`#!/bin/sh`) en première ligne.
2. Rendre le fichier exécutable : `chmod u+x script.sh`.
3. Lancer le script : `./script.sh`.
</details>