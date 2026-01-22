# 09_Unite_9
**Lien vers le PDF source** : [09_Unite_9.pdf](./cm/09_Unite_9.pdf)

---

### **Introduction au langage C**
Le **langage C** est l’**ancêtre de C++ et Java**, et constitue le **"DNA"** des **systèmes d’exploitation** (Linux, outils comme `bash`, `ssh`). Ses **avantages** incluent :
- **Proximité avec le matériel** (performance).
- **Vitesse d’exécution**.
- **Bibliothèques riches**.
Ses **inconvénients** :
- **Complexité** (gestion manuelle de la **mémoire**, **pointeurs**).
- **Concurrents récents** : **Go** (Google) et **Rust** (Mozilla).

---

### **Syntaxe de base**
- **Langage procédural** : utilise des **fonctions** (pas d’objets).
- **Point d’entrée** : la fonction **`main`**.
- **Déclaration de fonction** :
  ```c
  ret_type func(type1 arg1, type2 arg2) { <body> return <valeur>; }
  ```
- **`void`** : type de retour pour les fonctions sans valeur de retour.
- **Syntaxe proche de Java** (boucles `for`, `if`, `while`), mais **pas de POO** (pas de `class`, `String`, etc.).
- **Concepts spécifiques à C** :
  - **Pointeurs**.
  - **`struct`** (structures de données).

---

### **Types de données de base**
- **Tout est un nombre** : entiers ou flottants.
- **Types entiers** :
  - `char`, `short`, `int`, `long`, `long long` (tailles croissantes).
  - **`signed` par défaut** (sauf `char`, dépendant de l’implémentation).
  - **Modificateurs** : `unsigned`, `signed`.
  - **Taille non standardisée** (ex: `char` = 1 octet).
- **Types flottants** :
  - `float`, `double`, `long double` (tailles variables, ex: 32/64/128 bits).
- **Type `char`** :
  - **Double rôle** : caractère **ET** entier 8 bits.

---

### **Tableaux et pointeurs**
- **Tableaux** :
  - Syntaxe : `type nom[size];` (ex: `int tab[5];`).
  - **Initialisation** :
    ```c
    int tab[] = {1, 2, 3}; // Taille implicite
    char str[] = "abcd";   // Ajoute automatiquement '\0'
    ```
  - **Indexation** : commence à **0**.
- **Pointeurs** :
  - **Définition** : une **adresse mémoire** + type pointé.
  - **Syntaxe** :
    - `int *ptr` : pointeur vers un `int`.
    - `*ptr` : **déréférencement** (accès à la valeur pointée).
    - `&var` : **adresse** de la variable `var`.
  - **Arithmétique des pointeurs** :
    - `ptr + n` ajoute `n * sizeof(type)` à l’adresse.
    - Ex: `int *ptr2 = ptr + 1` ajoute 4 octets (si `int` = 32 bits).

---

### **Passage de paramètres**
- **Passage par valeur** :
  ```c
  void foo1(int i) { i = i + 2; } // Modifie une copie locale
  ```
- **Passage par référence** (via pointeurs) :
  ```c
  void foo2(int *ptr_i) { *ptr_i = *ptr_i + 2; } // Modifie la valeur originale
  ```

---

### **Chaînes de caractères (`strings`)**
- **Pas de type dédié** : une **chaîne** est un **`char*`** pointant vers une zone mémoire terminée par **`\0`**.
- **Exemple** :
  ```c
  char *str = "abcd"; // Alloue 5 octets ('a', 'b', 'c', 'd', '\0')
  ```
- **Pièges courants** :
  - **Copies non bornées** (risque de **buffer overflow**).
  - **Oubli du `\0`** (comportement indéfini).
- **Manipulation** :
  ```c
  printf("%c", str[1]);      // Affiche 'b'
  printf("%s", str + 2);     // Affiche "cd" (décalage de 2 octets)
  ```

---

### **Exemple de programme**
```c
int main(int argc, char **argv) {
  char x[] = "it's a wonderful world";
  char delta = 'a' - 'A'; // Différence ASCII entre minuscule et majuscule
  for (int i = 0; i < sizeof(x) - 1; i++) {
    if (x[i] >= 'a' && x[i] <= 'z') x[i] -= delta; // Convertit en majuscules
  }
  printf("%s\n", x); // Affiche "IT'S A WONDERFUL WORLD"
}
```
- **Note** : `'a'` (caractère) ≠ `"a"` (chaîne de 2 octets : `'a' + '\0'`).

---

### **Résumé des compétences**
À l’issue de cette unité, vous devez pouvoir :
- Décrire les **types de base** de C (`int`, `char`, `float`, etc.).
- Analyser et écrire des **programmes simples** en C.
- Comprendre le **double rôle du `char`** (caractère/entier).
- Manipuler **chaînes de caractères** et leurs **pièges** (`\0`, buffer overflow).
- Expliquer le lien entre **tableaux et pointeurs** (`tab[i] ≡ *(tab + i)`).
- Utiliser l’**arithmétique des pointeurs** et le **casting**.

---

### **Quiz**
<details>
<summary>🔍 Question 1 : Pourquoi le langage C est-il souvent utilisé pour les systèmes d’exploitation ?</summary>
C est **proche du matériel** (accès direct à la mémoire, performance) et **rapide**, ce qui est crucial pour les noyaux de systèmes. Il offre aussi un **contrôle fin** sur les ressources, contrairement à des langages comme Java.
</details>

<details>
<summary>🔍 Question 2 : Quelle est la différence entre `char *str = "hello";` et `char str[] = "hello";` ?</summary>
- `char *str` : crée un **pointeur** vers une chaîne **immuable** (stockée en mémoire statique).
- `char str[]` : crée un **tableau modifiable** en mémoire (copie locale de la chaîne).
</details>

<details>
<summary>🔍 Question 3 : Que fait ce code et pourquoi ?</summary>
```c
int i = 10;
int *ptr = &i;
*ptr = 20;
printf("%d", i); // Affiche 20
```
Le **pointeur `ptr`** stocke l’**adresse de `i`**. En modifiant `*ptr`, on modifie **directement la valeur de `i`** (déréférencement).
</details>

<details>
<summary>🔍 Question 4 : Pourquoi ce code est-il dangereux ?</summary>
```c
char buffer[10];
strcpy(buffer, "Une très longue chaîne qui dépasse la taille du buffer");
```
La fonction `strcpy` ne vérifie pas la taille du buffer. Si la chaîne source est plus longue que 10 octets, cela provoque un **buffer overflow** (écrasement de mémoire).
</details>