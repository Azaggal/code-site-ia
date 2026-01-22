# 06_Unite_7
**Lien vers le PDF source** : [06_Unite_7.pdf](./cm/06_Unite_7.pdf)

---

### **Boucles en assembleur x86**
Une **boucle** en assembleur x86 utilise des **instructions de saut conditionnel** (`jle`, `jnz`) et des **registres** pour contrôler l'exécution.
- **Exemple clé** : Le code initialise `rbx` à 15, puis décrémente (`dec rbx`) jusqu'à ce que `rbx = 0`.
- **Optimisation** : Remplacer `cmp rbx,0` + `jle` par `jnz` après `dec rbx` pour gagner en efficacité.
- **Piège** : La **syscall** peut écraser des registres (ex: `rcx`). Il faut les sauvegarder (`push`/`pop`) si nécessaire.

---

### **Conditions (`if-then-else`)**
Les **structures conditionnelles** en assembleur reposent sur :
- **`cmp`** : Compare deux valeurs (ex: `cmp ax, [y]`).
- **Sauts conditionnels** : `jge` (saut si ≥), `jl` (saut si <), etc.
- **Labels** : `sinon` et `continue` pour gérer les branches.
**Exemple** :
```asm
cmp ax, [y]  ; Compare x et y
jge sinon    ; Si x ≥ y, sauter à "sinon"
mov rsi, msg1 ; Sinon, charger msg1
jmp continue
sinon: mov rsi, msg2 ; Charger msg2
continue: ...         ; Suite du code
```

---

### **Modes d'adressage**
Les **modes d'adressage** définissent comment accéder aux **opérandes** :
1. **Immédiat** : Valeur fixe (`mov rax, 0x8`).
2. **Registre** : Utilise un registre (`mov rax, rbx`).
3. **Direct** : Accès mémoire via une adresse (`mov rax, [100]`).
4. **Indirect** :
   - **Simple** : `mov rax, [rbx]` (adresse stockée dans `rbx`).
   - **Avec déplacement** : `mov rax, [rbx+10]`.
   - **Général** : `mov rax, [rbx + scale*rsi + 10]` (où `scale ∈ {1,2,4,8}`).

**Cas pratique** :
Pour convertir une chaîne en minuscules :
```asm
mov rsi, len-1  ; Index de départ
loop:
  cmp BYTE [message+rsi], 'A'  ; Vérifier si majuscule
  jb cont                       ; Si non, sauter
  add BYTE [message+rsi], 'a'-'A' ; Convertir en minuscule
cont:
  dec rsi
  jge loop
```

---

### **Bonus : Opérandes de tailles différentes**
- **Problème** : `mov rax, BYTE [message]` échoue car `rax` (64 bits) et `BYTE` (8 bits) sont incompatibles.
- **Solutions** :
  - **`movzx`** : Étend avec des zéros (pour valeurs non signées).
  - **`movsx`** : Étend avec le bit de signe (pour valeurs signées).

---

!!! warning "⚠️ Points d'attention"
```markdown
- [Piège 1] : **Oublier de sauvegarder les registres** (ex: `rcx`) avant une **syscall**, qui peut les écraser.
- [Piège 2] : **Confondre `jge` et `jg`** : `jge` inclut l'égalité, `jg` non.
- [Piège 3] : **Adressage indirect** : `mov rax, [rbx]` charge la valeur à l'adresse stockée dans `rbx`, pas `rbx` lui-même.
```

---

### **Quiz**
<details>
<summary>🔍 Question 1 : Quelle instruction remplace avantageusement `cmp rbx,0` + `jle end` dans une boucle ?</summary>
**Réponse** : `jnz begin` après `dec rbx`. Cela évite une comparaison inutile et réduit le code à 2 instructions (`dec rbx` + `jnz`).
</details>

<details>
<summary>🔍 Question 2 : Comment implémenter un `if (x < y)` en assembleur x86 ?</summary>
**Réponse** :
1. Charger `x` et `y` dans des registres (ex: `mov ax, [x]`).
2. Comparer avec `cmp ax, [y]`.
3. Utiliser `jl` pour sauter au bloc "then" si `x < y`, sinon sauter au "else".
</details>

<details>
<summary>🔍 Question 3 : Que fait `mov rax, [rbx + 4*rsi + 8]` ?</summary>
**Réponse** : Charge dans `rax` la valeur située à l'adresse `rbx + 4*rsi + 8`. C'est un **adressage indirect généralisé** avec :
- **Base** : `rbx`.
- **Index** : `rsi` (multiplié par 4).
- **Déplacement** : `8`.
</details>