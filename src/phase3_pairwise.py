"""
Phase 3: Pairwise Linear Transform (base‑100 encoding)
- Takes a 100x100 grid of integers 0-99 (from previous phases)
- Combines consecutive cells (row-major order, last with first) into numbers 0-9999:
    w = a * 100 + b
- Output is a 100x100 grid of integers (0-9999)
- Fully reversible.
"""

from typing import List, Tuple

class Phase3Pairwise:
    """
    Transforms a grid of values by pairing consecutive cells.
    """

    def __init__(self):
        pass  # No key needed; the transform is deterministic.

    def transform(self, grid: List[List[int]]) -> List[List[int]]:
        """
        Convert a 100x100 grid of values 0-99 into a 100x100 grid of values 0-9999.
        """
        # Flatten the grid row-major
        flat = []
        for row in grid:
            flat.extend(row)
        # Ensure length is 10000
        assert len(flat) == 10000, f"Grid has {len(flat)} cells, expected 10000"

        # Create pairs (last with first)
        pairs = []
        for i in range(10000):
            a = flat[i]
            b = flat[(i + 1) % 10000]
            w = a * 100 + b   # base 100 → 0‑9999
            pairs.append(w)

        # Reshape back to 100x100
        result = [pairs[i*100:(i+1)*100] for i in range(100)]
        return result

    def inverse(self, grid: List[List[int]]) -> List[List[int]]:
        """
        Recover the original 0-99 grid from a 100x100 grid of 0-9999 values.
        """
        flat = []
        for row in grid:
            flat.extend(row)
        assert len(flat) == 10000

        # Recover a and b
        a_list = []
        b_list = []
        for w in flat:
            a = w // 100
            b = w % 100
            a_list.append(a)
            b_list.append(b)

        # The original sequence is exactly a_list (because b_list[i] should equal a_list[(i+1)%10000])
        # We'll just return a_list (the first element of each pair)
        result = [a_list[i*100:(i+1)*100] for i in range(100)]
        return result