# 10_Unite_10
**Lien vers le PDF source** : [10_Unite_10.pdf](./cm/10_Unite_10.pdf)

---

### **Processus de création d'un exécutable**
La transformation du **code source** en **exécutable** passe par plusieurs étapes clés :
- **Prétraitement** : Résout les **macros** et les **directives `#include`**, produit un code C "pur".
- **Compilation** : Transforme le code C en **assembleur** (dépendant de l'**architecture**, ex: x86, ARM).
- **Assemblage** : Génère le **code machine** (fichier `.o` ou **objet**).
- **Édition de liens** : Combine plusieurs fichiers objets en un **exécutable** via le **linker** (`ld` sous Linux).

---

### **Fichiers objets et symboles**
Un **fichier objet** (`.o`) contient :
- Le **code machine** (section *text*).
- Les **données globales** (section *data*).
- L'espace réservé pour les **données non initialisées** (section *bss*).
- Les **tables de symboles** : Liste des **fonctions** et **variables** (définies ou **non résolues**).
- Les **informations de relocation** : Indiquent les adresses à modifier lors de l'édition de liens.

**Formats courants** :
- **ELF** (Linux), **COFF** (Windows), **Mach-O** (macOS).

**Outils pour inspecter** :
- `nm` : Affiche les **symboles** (ex: `nm myProg.o`).
  - `U` : Symbole **non défini** (à résoudre par le linker).
  - `T` : Fonction **définie** dans le fichier.
  - `D` : Donnée globale **initialisée**.

---

### **Bibliothèques : statiques vs dynamiques**
#### **Bibliothèques statiques** (`.a`)
- **Archives** de fichiers objets.
- **Incluses dans l'exécutable** : Copie du code dans chaque binaire.
- **Inconvénients** : Gaspillage d'espace disque/mémoire (ex: `libc` dupliquée).

#### **Bibliothèques dynamiques** (`.so`, `.dll`, `.dylib`)
- **Partagées** entre plusieurs processus.
- **Chargées en mémoire une seule fois** (économie de ressources).
- **Complexité accrue** :
  - Gestion de la **mémoire virtuelle** (chaque processus a sa propre copie des données).
  - Nécessite un **MMU** (Memory Management Unit).

**Outils** :
- `ldd` : Liste les **bibliothèques dynamiques** utilisées par un exécutable.
- `nm -D` : Affiche les symboles d'une bibliothèque dynamique.

---

### **Chargement dynamique et exécution**
- Le **dynamic linker/loader** (`ld-linux.so`) résout les symboles **non définis** au lancement.
- **Étapes** :
  1. Chargement des bibliothèques partagées.
  2. Résolution des adresses (via **PLT** et **GOT**).
  3. Exécution du programme.
- **Outils** :
  - `pmap` ou `/proc/<PID>/maps` : Affiche la **cartographie mémoire** d'un processus.

---

### **Manipulation avancée : `dlopen` et `dlsym`**
- **`dlopen`** : Charge une bibliothèque dynamique **à l'exécution**.
- **`dlsym`** : Récupère l'adresse d'un **symbole** (fonction/variable) dans la bibliothèque.
- **Cas d'usage** :
  - Plugins, wrappers, programmation réflexive.
- **Exemple** :
  ```c
  void* handle = dlopen("./libmy.so", RTLD_LAZY);
  void (*func)() = dlsym(handle, "ma_fonction");
  func(); // Appel de la fonction chargée dynamiquement
  dlclose(handle);
  ```

---

!!! warning "⚠️ Points d'attention"
    ```markdown
    - [Piège 1] : Confondre **bibliothèque statique** (`.a`) et **dynamique** (`.so`) : la première est incluse dans l'exécutable, la seconde est chargée à l'exécution.
    - [Piège 2] : Oublier de lier une bibliothèque dynamique avec `-l` (ex: `gcc prog.o -lncurses`).
    - [Piège 3] : Les symboles **non résolus** dans un exécutable (ex: `printf`) sont gérés par le **dynamic linker**, pas par le linker statique.
    ```

---

### **Quiz**
<details>
<summary>🔍 Question 1 : Quelle est la différence entre un fichier objet (`.o`) et un exécutable ?</summary>
Un **fichier objet** contient du **code machine non lié** (adresses non résolues) et des **symboles** (fonctions/variables). Un **exécutable** est le résultat de l'**édition de liens** : il combine plusieurs fichiers objets, résout les adresses, et est prêt à être exécuté. Les symboles non définis (ex: `printf`) sont résolus par le **dynamic linker** au lancement.
</details>

<details>
<summary>🔍 Question 2 : Pourquoi les bibliothèques dynamiques économisent-elles de la mémoire ?</summary>
Les bibliothèques dynamiques (`.so`) sont **chargées une seule fois en mémoire physique** et **partagées** entre plusieurs processus via la **mémoire virtuelle**. Chaque processus accède à la même copie du **code** (section *text*), mais a sa propre copie des **données** (sections *data/bss*).
</details>

<details>
<summary>🔍 Question 3 : À quoi sert la commande `nm -D lib.so` ?</summary>
`nm -D` affiche les **symboles exportés** par une bibliothèque dynamique (`.so`). Cela permet de vérifier quelles fonctions/variables sont disponibles pour être utilisées par d'autres programmes (ex: `T print_message` indique une fonction définie).
</details>