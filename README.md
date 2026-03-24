# Layered Cipher System (LCS)

A multi‑layer encryption exercise that transforms any plaintext into a 100×100 grid of symbols. Each layer is fully reversible when the secret key is known, but without it the ciphertext is computationally unbreakable.

## 🔐 The Phases

### Phase 0 – Preprocessing
- Real words are padded to at least 6 characters.
- A large list of filler words (English words, names, cities, times, random 5‑digit numbers) is used to fill the remaining grid cells.
- The result is a 100×100 grid of characters (from a 100‑character alphabet).

### Phase 1 – Hierarchical Rotations
- The grid is recursively divided into blocks of sizes 100, 50, 25, 20, 10, 5 and 4.
- Each block is independently rotated 0, 90, 180 or 270 degrees, following a key‑derived pattern.
- **Security contribution:** 4¹¹⁷¹ ≈ 10⁷⁰⁵ possible configurations.

### Phase 2 – Dictionary Cipher
- 100 horizontal dictionaries (permutations of the 100‑character alphabet) and 100 vertical dictionaries (arranged as a Latin square) are derived from the key.
- For each cell (row i, column j):
  1. The plain character is replaced by its index in the row’s horizontal dictionary (p).
  2. A vertical dictionary index k = row‑specific permutation[i][p] is chosen.
  3. A dynamic shift s (based on the ciphertext of the previous row) is applied to the column index.
  4. The output character is taken from vertical[k] at position (j + s) mod 100.
- **Security contribution:** (100!)³⁰⁰ ≈ 10⁴⁷ ⁴⁰⁰.

### Phase 3 – Concentric Square Rotations
- **Stage 1 (Quadrants):** The grid is divided into 4 quadrants of 25×25. In each quadrant, concentric squares of odd sizes (3,5,7,…,25) are rotated around the quadrant’s center. For a square of side `s`, the border contains `4·(s-1)` cells, and a rotation can be any number of steps from 1 to `4·(s-1)` (direction also matters, giving `4·(s-1)` possibilities). The total number of possible rotations for this stage is the product over all odd sizes of `(4·(s-1))^4` (four quadrants).
- **Stage 2 (Whole grid):** On the full 100×100 grid, concentric squares of even sizes (2,4,6,…,100) are rotated around the grid’s center. Each even‑sized square contributes `4·(s-1)` possibilities.
- All rotation parameters are derived from the master key.
- **Security contribution:** The total number of configurations for Phase 3 is:
- This product is larger than 10³⁰⁰, adding a massive additional barrier.

### Phase 4 – Pairwise Transform & Final Substitution
- The character grid after Phase 3 is flattened and consecutive cells are combined into numbers **w = a·100 + b** (0‑9999). This step is deterministic (no key).
- The numbers then undergo a **keyed pseudo‑random permutation** (14‑bit Feistel with cycle walking) to produce the final ciphertext numbers.
- **Security contribution of the final substitution:** 10 000! ≈ 10³⁵ ⁶⁶⁰.

### Visual Outputs
- **Colors:** The numbers after the pairwise transform (before final substitution) are mapped to a fixed palette of 10 000 CSS colors, producing a purely visual grid. This is an intermediate visualisation (no security).
- **Exotic characters:** The final ciphertext numbers are mapped to 10 000 Unicode characters from diverse scripts (Greek, Cyrillic, Arabic, Thai, Chinese, Hiragana, etc.) – the final obfuscated output.

## 📊 Decoding Difficulty (Even with Known Plaintext)

All phases are public algorithms, but the secret keys (master key + IV) determine all permutations and rotation patterns. Without the key, an attacker faces an astronomically large search space:

| Component                                | Size / Security Contribution            |
|------------------------------------------|-----------------------------------------|
| Hierarchical rotations (Phase 1)         | 4¹¹⁷¹ ≈ 10⁷⁰⁵                           |
| Dictionary cipher (Phase 2)              | (100!)³⁰⁰ ≈ 10⁴⁷ ⁴⁰⁰                    |
| Concentric square rotations (Phase 3)    | > 10³⁰⁰                                 |
| Final substitution (Phase 4)             | 10 000! ≈ 10³⁵ ⁶⁶⁰                      |

Even if an attacker could try 10²⁰ combinations per second, the time required would be many orders of magnitude longer than the age of the universe.

## 🌐 Sample Outputs (Generated with 1984 text)

All outputs are available online via GitHub Pages:

- [Phase 0 – Preprocessed grid (text)](https://github.com/EnricLG/ACS/blob/master/docs/sample_output_phase0_1984.txt)
- [Phase 1 – After hierarchical rotations (text)](https://github.com/EnricLG/ACS/blob/master/docs/sample_output_phase1_rotated_1984.txt)
- [Phase 2 – After dictionary cipher (text)](https://github.com/EnricLG/ACS/blob/master/docs/sample_output_phase2_1984.txt)
- [Phase 3 – After concentric rotations (text)](https://github.com/EnricLG/ACS/blob/master/docs/sample_output_phase3_concentric_1984.txt)
- [Intermediate – Pairwise numbers (text)](https://github.com/EnricLG/ACS/blob/master/docs/sample_output_phase3b_numeric_1984.txt)
- [Visual – Colors only (HTML)](https://enriclg.github.io/ACS/sample_output_phase3_colors_1984.html)
- [Final – Exotic characters only (HTML)](https://enriclg.github.io/ACS/sample_output_phase4_exotic_1984.html)

*Note: The HTML files are large (100×100 tables); they open correctly in any modern browser.*

## 🧪 Requirements & Usage

- Python 3.8+
- Dependencies: `numpy`, `pycryptodome`, `psutil`, `imageio` (for animations)
- Install: `pip install -r requirements.txt`
- Run the full pipeline: `python tests/test_full_1984.py`

## ⚠️ Educational Purpose Only

This project was built as a **learning exercise** to explore the design of layered cryptographic primitives. It has not been independently audited and **must not be used to protect real sensitive data**. For production encryption, rely on well‑established standards such as AES‑256 or ChaCha20.

---

**Author:** EnricLG  
**License:** MIT  
**Repository:** [https://github.com/EnricLG/ACS](https://github.com/EnricLG/ACS)

"I invite anyone to test, audit, or attempt to break the system – without the keys, the ciphertext is designed to be mathematically unbreakable."

    Note: The system is designed for texts up to about 10,000 characters (the 100×100 grid). If your input exceeds this, it will be automatically truncated.