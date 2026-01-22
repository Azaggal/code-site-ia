# 08_Unite_8
**Lien vers le PDF source** : [08_Unite_8.pdf](./cm/08_Unite_8.pdf)

---

### **Mécanisme d'invocation et gestion de la pile**
Le **mécanisme d'invocation** (procédures en C, méthodes en Java) permet d'écrire du code **réutilisable**. Son défi principal : **mémoriser l'adresse de retour** après un appel.

- Une **pile d'appels** (*call stack*) est utilisée pour gérer les appels de fonctions.
  - **Structure LIFO** (Dernier Entré, Premier Sorti) : les appels les plus récents sont traités en premier.
  - **Croissance vers les adresses basses** (sur x86) : la pile grandit des adresses hautes vers les basses.

### **Rôle de la pile**
La **pile** remplit plusieurs fonctions clés :
- **Stocker l'adresse de retour** après un appel de fonction.
- **Passer des paramètres** (via registres ou pile).
- **Allouer des variables locales** (déclarées dans une fonction).
- **Récupérer les valeurs de retour**.

### **Gestion en assembleur x86-64**
- **Registre `rsp`** : pointe vers le **sommet de la pile**.
- **Opérations de base** :
  - **`push`** : ajoute une valeur sur la pile (`rsp` décrémente de 8 octets).
  - **`pop`** : retire une valeur de la pile (`rsp` incrémente de 8 octets).
- **Instructions spéciales** :
  - **`call adresse`** : pousse l'adresse de retour sur la pile et saute à `adresse`.
  - **`ret`** : dépile l'adresse de retour et y saute.

### **Problèmes courants et solutions**
- **Ordre des fonctions** : une fonction doit être définie **avant** son appel (ou après une sortie du programme).
  - Exemple : placer `foo` **avant** `_start` pour éviter des erreurs d'exécution.

### **Variables locales et cadres de pile**
- Les **variables locales** sont allouées **sur la pile**.
- Chaque appel de fonction crée un **cadre de pile** (*stack frame*) :
  - **Registre `rbp`** (*base pointer*) : pointe vers la base du cadre courant.
  - **Structure typique** :
    - Adresse de retour (au-dessus de `rbp`).
    - Variables locales (en dessous de `rbp`).
  - **Prologue/épilogue** :
    - **Prologue** : sauvegarde `rbp`, initialise le cadre (`mov rbp, rsp`).
    - **Épilogue** : restaure `rbp` et `rsp` avant `ret`.

### **Passage de paramètres**
- **Mécanismes** :
  - **Registres** (par défaut, ex: `rdi`, `rsi` en x86-64 Linux).
  - **Pile** (si trop de paramètres).
- **Types de passage** :
  - **Par valeur** : copie de la valeur (modifications non répercutées).
  - **Par référence** : passage d'une adresse (modifications visibles).
- **Convention d'appel** (ABI Linux) :
  - Registres **callee-saved** : `rbx`, `rsp`, `rbp` (doivent être restaurés).
  - Registres **caller-saved** : les autres (peuvent être écrasés).

### **Retour de valeurs**
- **Registres** (ex: `rax` pour les petits résultats).
- **Pile** (espace réservé avant l'appel pour les gros résultats).

---

!!! warning "⚠️ Points d'attention"
```markdown
- [Piège 1] : Confondre **`rsp`** (sommet de pile) et **`rbp`** (base du cadre courant).
- [Piège 2] : Oublier de **sauvegarder `rbp`** avant de modifier le cadre de pile.
- [Piège 3] : Négliger l'ordre des **paramètres** (registres vs. pile) selon l'ABI.
```

---

### **Quiz**
<details>
<summary>🔍 Question 1 : Pourquoi la pile est-elle essentielle pour les appels de fonctions ?</summary>
La pile permet de **mémoriser l'adresse de retour** après un appel, de **passer des paramètres**, et d'**allouer des variables locales**. Sans elle, le programme ne saurait pas où revenir après l'exécution d'une fonction.
</details>

<details>
<summary>🔍 Question 2 : Quelle est la différence entre `push` et `pop` en x86-64 ?</summary>
- **`push`** : ajoute une valeur sur la pile et décrémente `rsp` de 8 octets (pile grandit vers le bas).
- **`pop`** : retire une valeur de la pile et incrémente `rsp` de 8 octets (pile rétrécit).
</details>

<details>
<summary>🔍 Question 3 : Que se passe-t-il si une fonction modifie `rax` sans le sauvegarder avant un appel ?</summary>
Si `rax` n'est pas sauvegardé, sa valeur peut être **écrasée** par la fonction appelée (car `rax` est un registre *caller-saved* en ABI Linux). Cela peut corrompre les données du programme appelant.
</details>

<details>
<summary>🔍 Question 4 : Comment les variables locales sont-elles accessibles dans un cadre de pile ?</summary>
Elles sont accessibles via **`rbp` avec un offset négatif** (ex: `[rbp - 8]` pour la première variable locale). `rbp` pointe vers la base du cadre, et les variables locales sont stockées en dessous.
</details>