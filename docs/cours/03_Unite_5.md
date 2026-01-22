# 03_Unite_5
**Lien vers le PDF source** : [03_Unite_5.pdf](./cm/03_Unite_5.pdf)

---

### **Contenu principal**

#### **Composition d’un ordinateur**
Un ordinateur comprend :
- Un **CPU** (*Central Processing Unit*) : exécute les instructions.
- De la **mémoire volatile** (**RAM**) : stocke temporairement données et programmes.
- Du **stockage permanent** (**HDD/SSD**) : conserve les fichiers sans alimentation.
- Des **processeurs spécialisés** (**GPU**) et des **périphériques d’E/S** (écran, clavier, etc.).
- Des **bus** pour connecter ces éléments.

---

#### **Du code source à l’exécution**
Un programme (**fichier binaire**) est stocké sur un **stockage permanent** sous forme de **séquences de bits** (1 octet = 8 bits).
- **Encodage des caractères** :
  - **ASCII** (7 bits), **ISO-8859-1** (8 bits), ou **UTF-8** (longueur variable).
  - Exemple : `01110000` = **112 en binaire** = **'p' en ASCII**.
- **Fichiers binaires** : contiennent des données non textuelles (exécutables, images, etc.), lisibles uniquement en **binaire** ou **hexadécimal**.

---

#### **Compilation et exécution d’un programme Java**
1. **Compilation** :
   - `javac HelloWorld.java` génère un fichier **`.class`** contenant :
     - **Métadonnées** (nom de la classe, méthodes, constantes).
     - **Bytecode** : instructions intermédiaires pour la **JVM** (*Java Virtual Machine*).
   - Outils : `javap -verbose -c HelloWorld` pour désassembler le bytecode.

2. **Exécution** :
   - La **JVM** (écrite en **C/C++**) interprète le **bytecode**.
   - La JVM elle-même est compilée en **code machine** (exécutable natif) via un compilateur comme **gcc**.
   - Le **code machine** est spécifique à un **ISA** (*Instruction Set Architecture*, ex: x86, ARM).

---

#### **Niveaux de code**
- **Code source** : lisible par l’humain (Java, C).
- **Bytecode** : intermédiaire pour la JVM (ex: `b20002`).
- **Assembly** : représentation lisible du **code machine** (ex: `invokevirtual #4`).
  - Utilise des **mnémoniques** pour simplifier la lecture.
  - Outils : **désassembleur** (pour convertir en assembly) et **assembleur** (pour convertir en code machine).
- **Code machine** : binaire exécutable par le CPU (ex: `48 83 ec 08` = `sub rsp,0x8` en x86-64).

---

#### **Rôle du CPU**
- **Exécute le code machine** stocké en **RAM** (mémoire volatile).
- Composants clés :
  - **Unité de contrôle** : gère le cycle d’exécution.
  - **ALU** (*Arithmetic Logic Unit*) : effectue les calculs.
  - **Registres** : mémoire ultra-rapide (ex: 16 registres en x86-64, 64 bits chacun).
- **Cycle d’exécution** :
  1. **Fetch** : lit l’instruction depuis la mémoire.
  2. **Decode** : interprète l’instruction.
  3. **Execute** : effectue l’opération (via l’**ALU**).
  4. **Write-back** : stocke le résultat.
- **Optimisations** :
  - **Pipeline** : parallélise les étapes du cycle.
  - **Superscalaire** : exécute plusieurs instructions simultanément.
  - **Multi-cœur** : plusieurs CPU sur une même puce.

---

#### **Concepts clés à retenir**
- **JVM** : interprète le **bytecode** et interagit avec l’OS.
- **ISA** : ensemble d’instructions spécifiques à un processeur (ex: x86 vs ARM).
- **Registres** : mémoire interne du CPU, limitée mais ultra-rapide.

---

### **Quiz**
<details>
<summary>🔍 Question 1 : Quelle est la différence entre **bytecode** et **code machine** ?</summary>
Le **bytecode** est un code intermédiaire généré par la compilation d’un programme Java (ex: `.class`), exécuté par la **JVM**. Le **code machine** est un binaire directement exécutable par le **CPU** (spécifique à un **ISA** comme x86 ou ARM). La JVM elle-même est compilée en code machine.
</details>

<details>
<summary>🔍 Question 2 : Pourquoi utilise-t-on l’**hexadécimal** pour représenter des données binaires ?</summary>
L’**hexadécimal** (base 16) est plus compact que le binaire (base 2). Par exemple, `01110000` (8 bits) s’écrit `70` en hexadécimal. Cela simplifie la lecture des **fichiers binaires** (exécutables, images) et réduit les erreurs.
</details>

<details>
<summary>🔍 Question 3 : Quels sont les 3 composants principaux d’un **CPU** ?</summary>
1. **Unité de contrôle** : gère le cycle d’exécution des instructions.
2. **ALU** (*Arithmetic Logic Unit*) : effectue les calculs et opérations logiques.
3. **Registres** : mémoire interne ultra-rapide (ex: 16 registres de 64 bits en x86-64).
</details>