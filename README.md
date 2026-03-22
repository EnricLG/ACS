# Layered Cipher System (LCS) – A Multi‑Layer Encryption Exercise

This project demonstrates a **4‑phase encryption pipeline** that transforms any plaintext into a 100×100 grid of symbols. Each phase is fully reversible when the secret keys are known, but without them the ciphertext becomes computationally infeasible to decode – even if the algorithm and the original plaintext are known.

## 🔐 The Four Phases

### Phase 0 – Preprocessing
- Real words are padded to at least 6 characters.
- A large list of filler words (English words, names, cities, times, random 5‑digit numbers) is used to fill the remaining grid cells.
- The result is a 100×100 grid of characters (from a 100‑character alphabet).

### Phase 1 – Hierarchical Rotations
- The grid is recursively divided into blocks of sizes 100, 50, 25, 20, 10, 5 and 4.
- Each block is independently rotated 0, 90, 180 or 270 degrees, following a key‑derived pattern.
- Total possible rotation configurations: **4^1171 ≈ 10⁷⁰⁵** – a number vastly larger than the number of atoms in the observable universe.

### Phase 2 – Dictionary Cipher
- 100 horizontal dictionaries (permutations of the 100‑character alphabet) and 100 vertical dictionaries (arranged as a Latin square) are derived from the key.
- For each cell (row i, column j):
  1. The plain character is replaced by its index in the row’s horizontal dictionary (p).
  2. A vertical dictionary index k = row‑specific permutation[i][p] is chosen.
  3. A dynamic shift s (based on the ciphertext of the previous row) is applied to the column index.
  4. The output character is taken from vertical[k] at position (j + s) mod 100.
- Even with a known plaintext, the 100 horizontal, 100 vertical, and 100 row‑order permutations create an **effective key space of (100!)³⁰⁰ ≈ 10^47,400**.

### Phase 3 – Pairwise Transform & Colour Output
- The 100×100 grid of characters is flattened and consecutive cells are combined into numbers **w = a·100 + b** (0–9999).
- These numbers are then mapped to **CSS colours** (using a deterministic random palette) to produce a purely visual output.

### Phase 4 – Final Substitution & Exotic Character Output
- The same numbers (0–9999) are further transformed using a **keyed pseudo‑random permutation** (a 14‑bit Feistel network with cycle walking).
- The result is mapped to a list of **10 000 exotic Unicode characters** (Greek, Cyrillic, Arabic, Thai, Chinese, Hiragana, etc.) – producing the final ciphertext.

## 📊 Decoding Difficulty (Even with Known Plaintext)

All phases are **public algorithms**, but the secret keys (master key + IV) determine:
- The filler word list order
- All 100 horizontal and vertical permutations
- All 100 row‑order permutations
- All rotation angles for every block
- The pseudo‑random permutations in Phase 4

Without the key, an attacker faces an astronomically large search space:

| Component                          | Size                           |
|------------------------------------|--------------------------------|
| Rotations (Phase 1)                | 4^1171 ≈ 10⁷⁰⁵                |
| Dictionary cipher (Phase 2)        | (100!)^300 ≈ 10^47,400        |
| Final substitution (Phase 4)       | 10 000! ≈ 10^35,660           |

Even if the attacker could try 10²⁰ combinations per second, the time required would be many orders of magnitude longer than the age of the universe.

## 🌐 Sample Outputs

All sample outputs were generated with the **full 1984 text** and can be viewed online via GitHub Pages:

- [Phase 0 – Preprocessed grid (text)](https://github.com/EnricLG/ACS/blob/master/docs/sample_output_phase0_1984.txt)
- [Phase 1 – After hierarchical rotations (text)](https://github.com/EnricLG/ACS/blob/master/docs/sample_output_phase1_rotated_1984.txt)
- [Phase 2 – After dictionary cipher (text)](https://github.com/EnricLG/ACS/blob/master/docs/sample_output_phase2_1984.txt)
- [Phase 3 – Colour‑only output (HTML)](https://enriclg.github.io/ACS/sample_output_phase3_colors_1984.html)
- [Phase 4 – Exotic‑character output (HTML)](https://enriclg.github.io/ACS/sample_output_phase4_exotic_1984.html)

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