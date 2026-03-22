"""
Phase 4: Final Substitution with 10,000 dictionaries per value (simulated with FPE)
- Uses a Feistel network on 14-bit numbers (range 0-16383) with cycle walking to map to 0-9999.
- Fully reversible.
"""

import hashlib
import hmac
from typing import List

class Phase4FinalSubstitution:
    def __init__(self, master_key: bytes, iv: bytes = None):
        self.master_key = master_key
        self.iv = iv if iv is not None else b'\x00' * 16
        self.range_size = 10000
        self.block_size = 14          # bits (2^14 = 16384 > 10000)
        self.half_bits = self.block_size // 2   # 7 bits
        self.mask = (1 << self.half_bits) - 1   # 0x7F

    def _derive_subkey(self, i: int, j: int) -> bytes:
        """Derive a unique 32-byte subkey for each cell."""
        data = self.iv + i.to_bytes(2, 'big') + j.to_bytes(2, 'big')
        return hmac.new(self.master_key, data, hashlib.sha256).digest()

    def _round_function(self, x: int, round_key: bytes) -> int:
        """F: takes a 7-bit number, returns a 7-bit number."""
        h = hashlib.sha256(round_key + x.to_bytes(1, 'big')).digest()
        return int.from_bytes(h[:2], 'big') & self.mask

    def _feistel(self, x: int, subkey: bytes, rounds: int = 8) -> int:
        """Apply Feistel network to a 14-bit number."""
        left = x >> self.half_bits
        right = x & self.mask
        for r in range(rounds):
            round_key = hashlib.sha256(subkey + r.to_bytes(1, 'big')).digest()
            f = self._round_function(right, round_key)
            left, right = right, left ^ f
        return (left << self.half_bits) | right

    def _inverse_feistel(self, y: int, subkey: bytes, rounds: int = 8) -> int:
        """Inverse of Feistel: apply rounds in reverse order."""
        left = y >> self.half_bits
        right = y & self.mask
        for r in reversed(range(rounds)):
            round_key = hashlib.sha256(subkey + r.to_bytes(1, 'big')).digest()
            f = self._round_function(left, round_key)
            left, right = right ^ f, left
        return (left << self.half_bits) | right

    def _permute(self, x: int, subkey: bytes) -> int:
        """Apply Feistel with cycle walking to map into [0, range_size-1]."""
        y = x
        while True:
            y = self._feistel(y, subkey)
            if y < self.range_size:
                return y

    def _inverse_permute(self, y: int, subkey: bytes) -> int:
        """Inverse of _permute."""
        x = y
        while True:
            x = self._inverse_feistel(x, subkey)
            if x < self.range_size:
                return x

    def encrypt(self, grid: List[List[int]]) -> List[List[int]]:
        result = [[0]*100 for _ in range(100)]
        for i in range(100):
            for j in range(100):
                val = grid[i][j]
                subkey = self._derive_subkey(i, j)
                result[i][j] = self._permute(val, subkey)
        return result

    def decrypt(self, grid: List[List[int]]) -> List[List[int]]:
        result = [[0]*100 for _ in range(100)]
        for i in range(100):
            for j in range(100):
                val = grid[i][j]
                subkey = self._derive_subkey(i, j)
                result[i][j] = self._inverse_permute(val, subkey)
        return result