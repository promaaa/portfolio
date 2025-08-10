# De NAND à ALU 16 bits – Construire un processeur à partir de presque rien

## TL;DR
Projet éducatif open source retraçant la construction progressive d’un chemin de calcul : partir d’un unique opérateur universel (NAND), dériver les portes logiques, concevoir une ALU 8 bits puis l’étendre en 16 bits, ajouter un mini assembleur Python et valider le tout par des testbenches reproductibles (ex. 7 + 8 = 15). C’est le premier épisode de la série “From Bits to Chip”.

---
## 1. Contexte & Objectif
L’objectif de ce premier volet est de rendre tangible la phrase souvent abstraite : « Toute logique numérique peut être construite uniquement avec des NAND ». Plutôt que rester théorique, le dépôt montre un chemin concret et reproductible jusqu’à une ALU 16 bits fonctionnelle, avec un outillage minimal (Verilog + assembleur Python) et une validation automatisée.

---
## 2. Architecture pédagogique (approche bottom‑up)
Progression intentionnelle :
1. Porte universelle paramétrable (`nand_gate.v`)
2. Composition structurée des portes dérivées : AND (2 NAND), OR (3 NAND), etc.
3. Passage au niveau mot : opérandes 8 bits
4. Ajout des opérations arithmétiques et logiques (ALU 8 bits)
5. Extension dimensionnelle → ALU 16 bits (chaînage et gestion du report)
6. Outillage logiciel : assembleur textuel → machine code 16 bits
7. Validation systématique via testbenches simulables (Icarus Verilog)

---
## 3. Structure du dépôt (vue synthèse)
- `src/rtl/` : Modules Verilog (portes + ALU 8/16 bits)
- `src/testbenches/` : Bancs de test reproductibles
- `src/fpga/` : Point d’entrée top-level pour futures implémentations FPGA
- `tools/assembler/` : Parser + encodeur d’instructions 16 bits
- `tools/scripts/` : Scripts de build simulation / FPGA
- `examples/` : Exemples d’assemblage
- `docs/` : Script et slides pédagogiques

---
## 4. Le cœur logique : la famille des modules
### 4.1 Universalité de NAND
NAND est fonction complète : en combinant inversion + conjonction, on reconstruit toutes les autres logiques.  
Exemple (conceptuel) :
- NOT A = NAND(A, A)
- AND(A,B) = NOT(NAND(A,B))
- OR(A,B) = NAND(NOT A, NOT B)

Dans le code, chaque brique est paramétrée par `WIDTH` pour permettre un passage flexible de 1 bit à N bits sans dupliquer la logique.

### 4.2 ALU 8 bits
Fonctions prises en charge (opcode sur 3 bits) :
- 000 ADD
- 001 SUB
- 010 AND
- 011 OR
- 100 XOR
- 101 SHL (décalage gauche)
- 110 SHR (décalage droite)
- 111 NOT (unaires)

Points pédagogiques :
- Usage d’un registre étendu (9 bits) pour capturer le report
- Découplage sémantique entre valeur de sortie et drapeau de carry
- Simplicité volontaire (pas de pipeline ni de drapeaux Overflow/Zero exposés, mais facilement ajoutables)

### 4.3 Extension 16 bits
Stratégie : chaîner deux instances de l’ALU 8 bits.  
Enjeux :
- Propagation du carry (ADD, SUB)
- Cohérence des décalages multi‑octets (approche simplifiée ici)
- Base pour explorer ensuite : additions rapides (carry lookahead), pipeline, sign extension.

---
## 5. Mini assembleur Python
### 5.1 Objectif
Fournir un pont entre un langage symbolique lisible (mnémotechnique + registres) et un format binaire 16 bits aligné sur l’ALU définie.

### 5.2 Format d’instruction (actuel)
```
[15:13] Opcode (3 bits)
[12:10] Rd
[9:7]   Rs1
[6:4]   Rs2 (ou source unique selon type)
[3:0]   Réservé (future extension immédiats / flags)
```

### 5.3 Pipeline logiciel
1. `parser.py` : Nettoyage ligne, extraction opcode / opérandes
2. `encoder.py` : Mapping mnémotechnique → opcode binaire, packing bitfields
3. `main.py` : Orchestration, génération `.bin` + dump `.hex` lisible

### 5.4 Limites actuelles (et opportunités)
- Pas de labels résolus en branchements (labels collectés mais pas exploités)
- Pas d’immédiats ni de mémoire
- Pas de pseudo‑instructions
- Pas de détection avancée d’erreurs (opérandes hors plage, registres invalides)

---
## 6. Tests & Validation
### 6.1 Philosophie
Chaque niveau d’abstraction possède un testbench ciblé : une granularité fine permet d’isoler rapidement une régression.

### 6.2 Exemple emblématique
Addition 7 + 8 = 15 (`add7_plus_8.v`) :
```verilog
A  = 7;
B  = 8;
Op = 3'b000; // ADD
#10;
assert(Y == 15);
```

### 6.3 Catégories de tests
- Validation logique primitive (porte NAND)
- Validation fonctionnelle ALU 16 bits (chaînage)
- Scénario démonstratif pédagogique (7 + 8)
- Génération binaire via assembleur + inspection hexadécimale

### 6.4 Extensions test possibles
- Ajout de tests pseudo-aléatoires (fuzz) sur l’ALU
- Couverture (gcov + verilator) pour quantifier branches
- Tests de non-régression CI (GitHub Actions)

---
## 7. Découvertes & Enseignements
| Thème | Observation | Implication |
|-------|-------------|-------------|
| Universalité | NAND suffit réellement à tout reconstruire | Renforce la compréhension structurelle des portes |
| Paramétrisation | `WIDTH` réduit duplication | Favorise extension future (bus plus larges) |
| Séparation logique / assemblage | Introduire tôt un assembleur clarifie le contrat ISA | Prépare l’intégration d’un futur pipeline |
| Simplicité ALU | Design combinatoire brut facile à tester | Sert de base pour explorer optimisations timing |
| Chaînage 8→16 bits | Montre coûts de la propagation de carry | Transition future vers adders accélérés |
| Format binaire épuré | Réserves basses 4 bits pour évolutions | Flexibilité sans casser compatibilité |

---
## 8. Contraintes & Choix assumés
- Pas de pipeline : lisibilité prioritaire
- Pas de registres d’état exposés (flags) pour ne pas alourdir l’épisode 1
- Décalages non “cross‑lane” sophistiqués (implémentation minimale)
- Assembleur minimaliste (pas de macros / symbolique avancée)

---
## 9. Axes d’amélioration (Roadmap technique)
1. Ajouter un flag Zero / Negative / Overflow
2. Instructions immédiates (format étendu)
3. `LOAD`, `STORE`, `BRANCH{EQ,NE}` (exploiter labels)
4. Fichier de registres explicite
5. Pipeline 2/3 étapes (Fetch / Exec / Writeback)
6. CI + couverture (Verilator)
7. Addition optimisée (carry lookahead)
8. Assembleur enrichi (erreurs structurées)

---
## 10. Pertinence portfolio
- Compréhension verticale : logique booléenne → architecture
- Outillage logiciel associé (assembleur)
- Discipline de test (Makefile, scripts)
- Code lisible et extensible
- Documentation pédagogique cohérente

---
## 11. Extraits Illustratifs
Porte universelle paramétrée :
```verilog
assign y = ~(a & b);
```
Chaînage conceptuel ALU 16 bits :
```
ALU_low  (A[7:0],  B[7:0])  → carry → ALU_high (A[15:8], B[15:8])
```
Encodage (ADD R0,R1,R2) :
```
Opcode=000 Rd=000 Rs1=001 Rs2=010 xxxx
```

---
## 12. Leçons personnelles (neutre)
- Formaliser tôt les conventions réduit les ambiguïtés.
- Un assembleur simple force la stabilisation d’une ISA.
- Granularité des testbenches = diagnostic rapide.
- Prévoir des bits réservés évite les refontes.

---
## 13. Limites actuelles
- Pas de mesures timing scriptées.
- Pas de fuzz massif.
- Pas de linking multi-fichiers assembleur.
- Pas de mémoire / PC / branchements.

---
## 14. Reproduction rapide
Installation (macOS) :
```bash
brew install icarus-verilog python3 make
```
Simulation démo :
```bash
make sim-add7_plus_8
```
ALU 16 bits :
```bash
make sim-tb_alu16
```
Assembler un exemple :
```bash
make assembler
hexdump -C tools/assembler/test.bin
```

---
## 15. Pistes pédagogiques
- Réécrire l’ALU en style purement structurel (half/full adders)
- Ajouter flags Zero/Carry/Overflow
- Étendre assembleur (labels actifs, immédiats)
- Script de fuzz (génération aléatoire A,B,Op + modèle Python)

---
## 16. Conclusion
Base claire : un socle logique minimal formalisé jusqu’à une ALU 16 bits, avec un outillage léger favorisant l’exploration. Transition naturelle vers mémoire, pipeline et exécution de programmes. Démystification effective : du concept académique à l’artefact exécutable.

---
## 17. Ressources
- Dépôt : https://github.com/promaaa/nand2cpu
- Script & Slides : dossier `docs/`
- Vidéo (Episode 1) : lien README
- Inspirations : Nand2Tetris, MIT 6.004

---
## 18. Licence
MIT (usage éducatif encouragé).

---
## 19. Résumé (court)
ALU 16 bits construite à partir d’une seule porte NAND. Verilog paramétré, assembleur Python, testbenches reproductibles. Base extensible vers une architecture complète. Démonstration d’ingénierie verticale et de rigueur pédagogique.
