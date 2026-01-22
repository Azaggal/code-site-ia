# 02_Unite_4
**Lien vers le PDF source** : [02_Unite_4.pdf](./cm/02_Unite_4.pdf)

---

## **Commandes utiles et expressions régulières (Regex)**

### **Commandes Unix essentielles**
- **`which`** : Affiche le **chemin** d’un exécutable.
- **`find <dossier> -name "<motif>"`** : Cherche récursivement des fichiers.
  - **`<motif>`** peut contenir des **jokers** (ex: `*.txt`).
- **`uniq`** : Supprime les **lignes dupliquées contiguës**.
  - **`-c`** : Compte les occurrences.
- **`sort`** : Trie les lignes (ordre **dictionnaire** par défaut).
  - **`-r`** : Ordre inverse.
  - **`-n`** : Ordre numérique.
  - **`-k<x>`** : Trie selon le **champ numéro *x***.

---

### **`grep` : Recherche avancée**
- **`grep`** ("**global regular expression print**") filtre les lignes contenant un **motif**.
  - **`-i`** : Ignore la **casse**.
  - **`-c`** : Compte les occurrences.
  - **`-v`** : Inverse la sélection (lignes **sans** le motif).
  - **`--color`** : Met en couleur les correspondances.
  - **`-o`** : Affiche **uniquement** les motifs trouvés.
- **Exemple** : `grep -i "creature" pg84.txt | wc -l` compte les lignes avec "creature" (insensible à la casse).

---

### **Expressions régulières (Regex)**
- **Définition** : **Motifs puissants** pour rechercher/manipuler du texte.
  - Utilisées dans **`grep`**, **`sed`**, **`awk`**, et langages (Python, Perl, etc.).
- **Variantes** :
  - **Regex basiques** (anciennes).
  - **Regex étendues** (modernes, activées avec `-E` dans `grep`).

#### **Opérateurs clés**
| Opérateur | Description | Exemple |
|-----------|-------------|---------|
| **`.`** | N’importe quel **caractère** | `grep -E "a.c"` → "abc", "a1c" |
| **`[ ]`** | **Ensemble** de caractères | `[aeiou]` → une voyelle |
| **`[^ ]`** | **Exclusion** de caractères | `[^0-9]` → non-chiffre |
| **`\`** | **Échappement** (pour `.`, `[`, `]`) | `\.` → point littéral |
| **`*`** | **0 ou plusieurs** occurrences | `a*b` → "b", "ab", "aab" |
| **`+`** | **1 ou plusieurs** occurrences | `a+b` → "ab", "aab" (pas "b") |
| **`{n,m}`** | **n à m** répétitions | `a{1,2}b` → "ab", "aab" |
| **`( )`** | **Groupe** de motifs | `(ac)*b` → "b", "acb", "acacb" |
| **`|`** | **OU** logique | `a|b` → "a" ou "b" |

#### **Limites de lignes/mots**
- **`^`** : Début de **ligne**.
- **`$`** : Fin de **ligne**.
- **`\<`** et **`\>`** (GNU) : Début/fin de **mot**.
  - Exemple : `\<free\>` → "free" mais pas "freedom".

---

### **SSH : Connexion sécurisée**
- **Définition** : **Protocole** pour des connexions **chiffrées** à distance.
  - **Client** (ex: `ssh`) et **serveur** (ex: `sshd`).
- **Authentification** :
  - **Mot de passe** (peu sécurisé).
  - **Clés cryptographiques** (recommandé, générées avec `ssh-keygen`).
- **Commandes de base** :
  - `ssh <utilisateur>@<machine>` : Connexion à un serveur.
  - `ssh <machine> <commande>` : Exécute une commande à distance.
  - **Redirection de ports** : `ssh -L <port_local>:<hôte>:<port_distant> <machine>`.

---

## **Quiz**
<details>
<summary>🔍 Question 1 : Quelle commande compte les lignes contenant "error" (insensible à la casse) dans un fichier `log.txt` ?</summary>
**Réponse** :
`grep -i -c "error" log.txt`
- **`-i`** ignore la casse.
- **`-c`** compte les occurrences.
</details>

<details>
<summary>🔍 Question 2 : Que fait `grep -E "a{2,3}b"` ?</summary>
**Réponse** :
Cherche les lignes contenant :
- **"aab"** (2 `a` suivis de `b`).
- **"aaab"** (3 `a` suivis de `b`).
Mais **pas** "ab" ou "aaaab".
</details>

<details>
<summary>🔍 Question 3 : Comment afficher uniquement les mots commençant par "S" dans un fichier `noms.txt` avec `awk` ?</summary>
**Réponse** :
`awk '$1 ~ /^S/' noms.txt`
- **`$1`** : Premier champ (mot).
- **`~ /^S/`** : Mot commençant par "S".
</details>

<details>
<summary>🔍 Question 4 : Pourquoi SSH est-il plus sécurisé que `rsh` ?</summary>
**Réponse** :
- **Chiffrement** : Toutes les données sont **encryptées**.
- **Authentification forte** : Clés cryptographiques ou certificats (vs. mots de passe en clair).
- **Vérification de l'identité** du serveur (via sa clé publique).
</details>