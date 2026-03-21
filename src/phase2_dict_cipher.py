"""
Phase 2: Horizontal/Vertical Dictionary Cipher
- Uses 100 horizontal permutations (one per row)
- Uses 100 vertical dictionaries that form a Latin square
- Uses 100 row-specific permutations to choose which vertical dict to use per cell
- Dynamic line shifts based on previous row's ciphertext
- All parameters derived from master key and IV
"""

import hashlib
import hmac
import random
from typing import List, Tuple
from alphabet import ALPHABET

class Phase2DictCipher:
    def __init__(self, master_key: bytes, iv: bytes = None):
        self.master_key = master_key
        self.iv = iv if iv is not None else b'\x00' * 16
        self.alphabet = ALPHABET
        self.char_to_idx = {ch: i for i, ch in enumerate(self.alphabet)}

        self._derive_seeds()
        self._generate_horizontal_dicts()
        self._generate_vertical_dicts_as_latin_square()
        self._generate_row_order()
        self._build_lookup_tables()

    def _derive_seeds(self):
        self.seed_h = hmac.new(self.master_key, self.iv + b'horizontal', hashlib.sha256).digest()
        self.seed_v = hmac.new(self.master_key, self.iv + b'vertical', hashlib.sha256).digest()
        self.seed_order = hmac.new(self.master_key, self.iv + b'order', hashlib.sha256).digest()

    def _permutation_from_seed(self, seed: bytes, size: int = 100) -> List[int]:
        rng = random.Random(seed)
        perm = list(range(size))
        rng.shuffle(perm)
        return perm

    def _generate_horizontal_dicts(self):
        # Horizontal dictionaries are independent permutations
        self.horizontal = []
        for i in range(100):
            seed = self.seed_h + i.to_bytes(4, 'big')
            perm = self._permutation_from_seed(seed)
            self.horizontal.append([self.alphabet[p] for p in perm])

    def _generate_vertical_dicts_as_latin_square(self):
        # Build a Latin square of size 100 using the classic construction L0[i][j] = (i + j) mod 100
        # Then apply random row permutation, column permutation, and symbol permutation
        size = 100
        # 1. Standard Latin square: L0[i][j] = (i + j) % size
        L0 = [[(i + j) % size for j in range(size)] for i in range(size)]

        # 2. Random row permutation (derived from seed_v)
        seed_row_perm = self.seed_v + b'row_perm'
        row_perm = self._permutation_from_seed(seed_row_perm, size)
        # 3. Random column permutation
        seed_col_perm = self.seed_v + b'col_perm'
        col_perm = self._permutation_from_seed(seed_col_perm, size)
        # 4. Random symbol permutation (remap numbers 0..size-1 to characters)
        seed_sym_perm = self.seed_v + b'sym_perm'
        sym_perm = self._permutation_from_seed(seed_sym_perm, size)
        # Apply permutations
        L = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                # Apply row and column permutations
                val = L0[row_perm[i]][col_perm[j]]
                # Apply symbol permutation
                L[i][j] = sym_perm[val]
        # Now convert numbers to characters
        self.vertical = []
        for i in range(size):
            row = [self.alphabet[L[i][j]] for j in range(size)]
            self.vertical.append(row)

    def _generate_row_order(self):
        # Row order permutations (P_i)
        self.row_order = []
        for i in range(100):
            seed = self.seed_order + i.to_bytes(4, 'big')
            perm = self._permutation_from_seed(seed)
            self.row_order.append(perm)

    def _build_lookup_tables(self):
        # Horizontal index: for each row, map char -> position
        self.horiz_idx = []
        for row_dict in self.horizontal:
            self.horiz_idx.append({ch: i for i, ch in enumerate(row_dict)})

        # Inverse row order: for each row, map k -> p
        self.inv_row_order = []
        for perm in self.row_order:
            inv = [0] * 100
            for idx, val in enumerate(perm):
                inv[val] = idx
            self.inv_row_order.append(inv)

        # Vertical lookup: for each character index and output index, which vertical dictionary k
        # Since vertical dictionaries form a Latin square, this mapping is unique.
        self.vertical_lookup = [[-1] * 100 for _ in range(100)]
        for k, col_dict in enumerate(self.vertical):
            for out_idx, ch in enumerate(col_dict):
                ch_idx = self.char_to_idx[ch]
                # There should be no conflict because the square is Latin
                self.vertical_lookup[ch_idx][out_idx] = k

    def encrypt(self, grid: List[List[str]]) -> List[List[str]]:
        result = [[''] * 100 for _ in range(100)]

        for i in range(100):
            if i == 0:
                shift_col = [0] * 100
            else:
                prev_row_cipher = result[i-1]
                shift_col = [self.horiz_idx[i-1][ch] for ch in prev_row_cipher]

            for j in range(100):
                plain_char = grid[i][j]
                p = self.horiz_idx[i][plain_char]
                k = self.row_order[i][p]
                s = shift_col[j]
                out_idx = (j + s) % 100
                out_char = self.vertical[k][out_idx]
                result[i][j] = out_char

        return result

    def decrypt(self, cipher_grid: List[List[str]]) -> List[List[str]]:
        result = [[''] * 100 for _ in range(100)]

        for i in range(100):
            if i == 0:
                shift_col = [0] * 100
            else:
                prev_row_cipher = cipher_grid[i-1]
                shift_col = [self.horiz_idx[i-1][ch] for ch in prev_row_cipher]

            for j in range(100):
                cipher_char = cipher_grid[i][j]
                s = shift_col[j]
                out_idx = (j + s) % 100
                ch_idx = self.char_to_idx[cipher_char]
                k = self.vertical_lookup[ch_idx][out_idx]
                if k == -1:
                    raise ValueError(f"Decryption failed at ({i},{j}) – no mapping found")
                p = self.inv_row_order[i][k]
                original_char = self.horizontal[i][p]
                result[i][j] = original_char

        return result