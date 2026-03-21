"""
Phase 3 Visual Mapping: convert numbers 0-9999 to Chinese characters or CSS colors.
Reversible using deterministic PRNG with fixed seed (so same number always maps to same visual).
"""

import random

class Phase3Visual:
    def __init__(self, seed: bytes = None):
        if seed is None:
            seed = b'phase3_visual_default_seed'
        self.rng = random.Random(seed)
        self._generate_mappings()

    def _generate_mappings(self):
        # Generate 10,000 Chinese characters (from CJK Unified Ideographs range)
        # Use a deterministic shuffle of a list of code points.
        # We'll take the range U+4E00 to U+9FFF (20,992 chars) and pick first 10,000 in shuffled order.
        all_cjk = [chr(cp) for cp in range(0x4E00, 0x9FFF+1)]  # about 20,992
        # Ensure we have at least 10,000
        if len(all_cjk) < 10000:
            all_cjk = all_cjk * (10000 // len(all_cjk) + 1)
        self.chinese = all_cjk[:10000]
        # Shuffle them using the PRNG
        self.rng.shuffle(self.chinese)

        # Generate 10,000 CSS colors as hex strings
        # We'll use the same PRNG to create 10,000 random colors (each 6 hex digits)
        self.colors = []
        for _ in range(10000):
            r = self.rng.randint(0, 255)
            g = self.rng.randint(0, 255)
            b = self.rng.randint(0, 255)
            self.colors.append(f"#{r:02x}{g:02x}{b:02x}")

        # Build reverse mappings for quick lookup
        self._rev_chinese = {ch: i*2 for i, ch in enumerate(self.chinese)}
        self._rev_colors = {col: i*2+1 for i, col in enumerate(self.colors)}

    def to_visual(self, w: int) -> str:
        """
        Convert a number 0-9999 to its visual representation.
        Even -> Chinese character
        Odd  -> CSS color string
        """
        if 0 <= w < 10000:
            if w % 2 == 0:
                return self.chinese[w // 2]
            else:
                return self.colors[(w - 1) // 2]
        else:
            raise ValueError(f"Value {w} out of range [0,9999]")

    def from_visual(self, visual: str) -> int:
        """
        Reverse: given a Chinese character or color string, return the original w.
        """
        if visual in self._rev_chinese:
            return self._rev_chinese[visual]
        elif visual in self._rev_colors:
            return self._rev_colors[visual]
        else:
            raise ValueError(f"Visual '{visual}' not found in mapping")