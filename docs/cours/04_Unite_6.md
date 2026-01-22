# 04_Unite_6
**Lien vers le PDF source** : [04_Unite_6.pdf](./cm/04_Unite_6.pdf)

---

### **Introduction au langage assembleur x86**
Le **langage assembleur** est une représentation textuelle du **code machine** (séquences de bits). Il facilite la manipulation des instructions processeur, comme `sub rsp,0x8` (soustraire 8 au **registre** `rsp`).

- **Compilation** :
  - `nasm -felf64 fichier.asm` → génère un **fichier objet** (`.o`).
  - `ld fichier.o` → crée un **exécutable** (par défaut `a.out`).

---

### **Structure d’un fichier assembleur NASM**
Un fichier assembleur est organisé en **sections** :
- **`.data`** : Réserve de l’espace pour les **données initialisées** (ex: `message: db "Hello, World!", 10`).
  - **Directives** : `db` (byte), `dw` (word), `equ` (constante).
  - **Labels** : Permettent de référencer des adresses mémoire (ex: `mov rsi, message`).
- **`.text`** : Contient le **code exécutable**.
  - Doit inclure `GLOBAL _start` pour définir le **point d’entrée** du programme.

---

### **Instructions assembleur**
- **Format général** : `[label:] <opération> <opérande1>,<opérande2> [; commentaire]`.
  - **Notation Intel** : Le résultat est stocké dans la **première opérande** (contrairement à AT&T).
  - **Exemple** : `mov rax, 1` (copie la valeur 1 dans `rax`).

#### **Types d’opérations** :
1. **Transfert de données** : `mov`, `push`, `pop`.
2. **Arithmétique** : `add`, `sub`, `inc`, `dec`, `neg`.
3. **Logique** : `and`, `or`, `xor`, `not` (opérations **bit à bit**).
4. **Contrôle de flux** : `jmp` (saut inconditionnel), `je`/`jne` (sauts conditionnels).
5. **Complexes** : Appels système (`syscall`), opérations flottantes.

---

### **Opérandes**
#### **Registres** :
- **64 bits** : `rax`, `rbx`, `rsp` (préfixe `R`).
- **32 bits** : `eax`, `ebx` (préfixe `E`).
- **16 bits** : `ax`, `bx` (pas de préfixe).
- **8 bits** : `al` (low), `ah` (high) pour `ax`/`bx`/`cx`/`dx`.
  - **Hiérarchie** : `al` ⊂ `ax` ⊂ `eax` ⊂ `rax` (comme des poupées russes).

#### **Mémoire** :
- Accès via des **adresses** (ex: `[100]` = contenu à l’adresse 100).
- **Endianness** :
  - **Little-endian** (x86) : L’octet **le moins significatif** est stocké en premier.
    - Exemple : `0x0a0b0c0d` → mémoire : `0d 0c 0b 0a`.
  - **Big-endian** : L’octet **le plus significatif** en premier.
- **Limitation** : Impossible d’effectuer `mov [200], [100]` (2 opérandes mémoire interdites).

#### **Nombres signés** :
- Encodage sur `n` bits : Les valeurs ≥ `2^(n-1)` représentent des **nombres négatifs**.
  - Exemple sur 8 bits : `-2` = `0xFE`, `2` = `0x02`.
  - **Piège** : `add`/`sub` fonctionnent, mais `mul`/`div` nécessitent `imul`/`idiv`.

---

### **Appels système (x86-64)**
- **`syscall`** : Invoque une fonction du noyau Linux.
  - **Registres utilisés** :
    - `rax` : Numéro de l’appel système (ex: `1` pour `write`).
    - `rdi`, `rsi`, `rdx` : Arguments (ex: descripteur de fichier, adresse, taille).
  - **Exemple** :
    ```asm
    mov rax, 1      ; write
    mov rdi, 1      ; stdout
    mov rsi, message ; adresse du message
    mov rdx, msgLen ; taille
    syscall
    ```

---

!!! warning "⚠️ Points d'attention"
    - [Piège 1] : Confondre **little-endian** et **big-endian** lors de la lecture/écriture en mémoire.
    - [Piège 2] : Oublier que `mov M, M` est **interdit** (une opérande doit être un registre).
    - [Piège 3] : Utiliser `mul` au lieu de `imul` pour les **nombres signés** (comportement différent).

---

### **Quiz**
<details>
<summary>🔍 Question 1 : Quelle est la différence entre les sections `.data` et `.text` dans un fichier NASM ?</summary>
La section **`.data`** stocke les **données initialisées** (variables, chaînes de caractères) via des directives comme `db` ou `dw`. La section **`.text`** contient le **code exécutable** et doit inclure `GLOBAL _start` pour définir le point d’entrée du programme.
</details>

<details>
<summary>🔍 Question 2 : Pourquoi l’instruction `mov [200], [100]` est-elle invalide en assembleur x86 ?</summary>
Les processeurs x86 **interdisent les opérations avec deux opérandes mémoire** dans une même instruction. Il faut passer par un **registre intermédiaire** :
```asm
mov ax, [100]  ; Charge la valeur à l'adresse 100 dans ax
mov [200], ax  ; Stocke ax à l'adresse 200
```
</details>

<details>
<summary>🔍 Question 3 : Que représente `0x0a0b0c0d` en mémoire sur un processeur little-endian ?</summary>
En **little-endian**, l’octet **le moins significatif** (`0d`) est stocké en premier. La mémoire contiendra donc :
`0d 0c 0b 0a` (dans cet ordre).
</details>

<details>
<summary>🔍 Question 4 : Pourquoi les compilateurs utilisent-ils `xor rdi, rdi` au lieu de `mov rdi, 0` ?</summary>
`xor rdi, rdi` est **plus rapide** que `mov rdi, 0` car elle utilise une opération bit à bit (1 cycle d’horloge) et ne nécessite pas de constante immédiate. C’est une optimisation courante pour mettre un registre à zéro.
</details>