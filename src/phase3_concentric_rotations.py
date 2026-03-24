"""
Phase 3: Concentric Square Rotations
- Stage 1: Divide grid into 4 quadrants of 25x25. For each quadrant, rotate concentric squares
  of odd sizes (3,5,...,25) around the quadrant's center.
- Stage 2: On the whole grid, rotate concentric squares of even sizes (2,4,...,100) around the grid's center.
- All rotation parameters (shift and direction) are key‑derived.
"""

import hashlib
import hmac
import random
from typing import List

class Phase3ConcentricRotations:
    def __init__(self, master_key: bytes, iv: bytes = None):
        self.master_key = master_key
        self.iv = iv if iv is not None else b'\x00' * 16
        self.size = 100
        self.quadrant_size = 25

        # Generate all rotation parameters
        self.params = self._generate_rotation_params()

    def _derive_seed(self, label: str) -> bytes:
        """Derive a seed for a given label."""
        data = self.iv + label.encode()
        return hmac.new(self.master_key, data, hashlib.sha256).digest()

    def _generate_rotation_params(self) -> dict:
        """
        Returns a dict with keys:
          - 'quadrant_odd_sizes': list of (size, shift) for odd sizes 3..25
          - 'whole_even_sizes': list of (size, shift) for even sizes 2..100
        Shift positive = clockwise, negative = counterclockwise.
        """
        params = {'quadrant_odd_sizes': [], 'whole_even_sizes': []}

        # Stage 1: quadrant odd sizes
        seed = self._derive_seed('quadrant_odd')
        rng = random.Random(seed)
        for size in range(3, 26, 2):      # 3,5,...,25
            shift = rng.randint(1, 4*size - 4)  # number of steps along the border
            direction = rng.choice(['cw', 'ccw'])
            shift_val = shift if direction == 'cw' else -shift
            params['quadrant_odd_sizes'].append((size, shift_val))

        # Stage 2: whole even sizes
        seed = self._derive_seed('whole_even')
        rng = random.Random(seed)
        for size in range(2, 101, 2):     # 2,4,...,100
            shift = rng.randint(1, 4*size - 4)
            direction = rng.choice(['cw', 'ccw'])
            shift_val = shift if direction == 'cw' else -shift
            params['whole_even_sizes'].append((size, shift_val))

        return params

    def _extract_border(self, grid, top, left, size):
        """Extract the border of a square in clockwise order."""
        border = []
        # top edge
        for j in range(left, left + size):
            border.append(grid[top][j])
        # right edge
        for i in range(top + 1, top + size):
            border.append(grid[i][left + size - 1])
        # bottom edge (right to left)
        for j in range(left + size - 2, left - 1, -1):
            border.append(grid[top + size - 1][j])
        # left edge (bottom to top)
        for i in range(top + size - 2, top, -1):
            border.append(grid[i][left])
        return border

    def _rotate_border(self, border, shift):
        """Rotate the border list by `shift` steps (positive = clockwise)."""
        n = len(border)
        if n == 0 or shift == 0:
            return border
        shift = shift % n
        return border[-shift:] + border[:-shift]

    def _insert_border(self, grid, top, left, size, rotated_border):
        """Insert rotated border back into the square."""
        idx = 0
        # top edge
        for j in range(left, left + size):
            grid[top][j] = rotated_border[idx]
            idx += 1
        # right edge
        for i in range(top + 1, top + size):
            grid[i][left + size - 1] = rotated_border[idx]
            idx += 1
        # bottom edge
        for j in range(left + size - 2, left - 1, -1):
            grid[top + size - 1][j] = rotated_border[idx]
            idx += 1
        # left edge
        for i in range(top + size - 2, top, -1):
            grid[i][left] = rotated_border[idx]
            idx += 1

    def _apply_rotations_to_quadrant(self, grid, quadrant_row, quadrant_col, params_list):
        """Apply concentric rotations to a single quadrant."""
        top = quadrant_row * self.quadrant_size
        left = quadrant_col * self.quadrant_size
        center_row = top + self.quadrant_size // 2
        center_col = left + self.quadrant_size // 2
        for size, shift in params_list:
            if size > self.quadrant_size:
                continue
            offset = (size - 1) // 2
            start_row = center_row - offset
            start_col = center_col - offset
            if start_row < top or start_col < left or start_row + size > top + self.quadrant_size or start_col + size > left + self.quadrant_size:
                continue
            border = self._extract_border(grid, start_row, start_col, size)
            rotated = self._rotate_border(border, shift)
            self._insert_border(grid, start_row, start_col, size, rotated)

    def _apply_rotations_to_whole(self, grid, params_list):
        """Apply concentric rotations to the whole grid."""
        # For even sizes, center is between cells (49,49)-(50,50)
        center_row = 50
        center_col = 50
        for size, shift in params_list:
            if size % 2 != 0:
                continue
            half = size // 2
            start_row = center_row - half
            start_col = center_col - half
            if start_row < 0 or start_col < 0 or start_row + size > self.size or start_col + size > self.size:
                continue
            border = self._extract_border(grid, start_row, start_col, size)
            rotated = self._rotate_border(border, shift)
            self._insert_border(grid, start_row, start_col, size, rotated)

    def transform(self, grid: List[List[str]]) -> List[List[str]]:
        import copy
        result = copy.deepcopy(grid)

        # Stage 1: quadrants
        params_odd = self.params['quadrant_odd_sizes']
        for qr in range(2):
            for qc in range(2):
                self._apply_rotations_to_quadrant(result, qr, qc, params_odd)

        # Stage 2: whole grid
        params_even = self.params['whole_even_sizes']
        self._apply_rotations_to_whole(result, params_even)

        return result

    def inverse(self, grid: List[List[str]]) -> List[List[str]]:
        import copy
        result = copy.deepcopy(grid)

        # Reverse stage 2 (whole grid)
        params_even = self.params['whole_even_sizes'][::-1]
        for size, shift in params_even:
            self._apply_rotations_to_whole(result, [(size, -shift)])

        # Reverse stage 1 (quadrants)
        params_odd = self.params['quadrant_odd_sizes'][::-1]
        for qr in range(2):
            for qc in range(2):
                self._apply_rotations_to_quadrant(result, qr, qc, [(size, -shift) for size, shift in params_odd])

        return result