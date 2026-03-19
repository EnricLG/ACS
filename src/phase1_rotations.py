"""
Phase 1: Multi-scale Rotations
- Applies hierarchical rotations to the 100×100 grid
- Rotations: 0, 1, 2, or 3 quarter turns (0°, 90°, 180°, 270°)
- Order: largest to smallest blocks
"""

import random
from typing import List, Tuple, Dict
import numpy as np

class Phase1Rotations:
    """
    Applies reversible multi-scale rotations to a 100×100 grid.
    """
    
    def __init__(self, master_key: bytes, iv: bytes = None):
        """
        Initialize with master key for deterministic rotation parameters.
        
        Args:
            master_key: 32-byte master key
            iv: 16-byte initialization vector (optional)
        """
        self.master_key = master_key
        self.iv = iv or b'\x00' * 16
        self.rng = self._create_prng()
        
        # Define rotation levels
        self.levels = [
            (100, 1),   # size, number of blocks
            (50, 4),
            (25, 16),
            (20, 25),
            (10, 100),
            (5, 400),
            (4, 625)
        ]
        
        # Generate rotation parameters for all blocks
        self.rotations = self._generate_all_rotations()
    
    def _create_prng(self):
        """Create a deterministic PRNG from master key and IV."""
        import hashlib
        seed = hashlib.sha256(self.master_key + self.iv).digest()
        return random.Random(seed)
    
    def _generate_all_rotations(self) -> Dict[Tuple[int, int, int], int]:
        """
        Generate rotation values (0-3) for each block.
        Key: (level_index, block_row, block_col)
        Value: 0-3 (0=0°, 1=90°, 2=180°, 3=270° clockwise)
        """
        rotations = {}
        for level_idx, (size, num_blocks) in enumerate(self.levels):
            blocks_per_row = int(100 / size)
            for br in range(blocks_per_row):
                for bc in range(blocks_per_row):
                    # Use deterministic but seemingly random value
                    rotations[(level_idx, br, bc)] = self.rng.randint(0, 3)
        return rotations
    
    def _rotate_block(self, block: List[List[str]], rotation: int) -> List[List[str]]:
        """
        Rotate a square block clockwise by 0, 90, 180, or 270 degrees.
        
        Args:
            block: 2D list of characters
            rotation: 0-3 (0=0°, 1=90°, 2=180°, 3=270° clockwise)
        
        Returns:
            Rotated block
        """
        if rotation == 0:
            return block
        
        # Convert to numpy array for easy manipulation
        arr = np.array(block)
        
        if rotation == 1:  # 90° clockwise
            rotated = np.rot90(arr, k=-1).tolist()
        elif rotation == 2:  # 180°
            rotated = np.rot90(arr, k=2).tolist()
        elif rotation == 3:  # 270° clockwise (or 90° counter-clockwise)
            rotated = np.rot90(arr, k=1).tolist()
        else:
            rotated = block
        
        return rotated
    
    def _extract_block(self, grid: List[List[str]], size: int, block_row: int, block_col: int) -> List[List[str]]:
        """Extract a block of given size from the grid."""
        start_row = block_row * size
        start_col = block_col * size
        block = []
        for r in range(size):
            row = grid[start_row + r][start_col:start_col + size]
            block.append(row)
        return block
    
    def _insert_block(self, grid: List[List[str]], block: List[List[str]], size: int, block_row: int, block_col: int):
        """Insert a block back into the grid."""
        start_row = block_row * size
        start_col = block_col * size
        for r in range(size):
            for c in range(size):
                grid[start_row + r][start_col + c] = block[r][c]
    
    def apply(self, grid: List[List[str]]) -> List[List[str]]:
        """
        Apply all rotations to the grid (largest to smallest).
        
        Args:
            grid: 100x100 grid of characters
        
        Returns:
            Rotated grid
        """
        # Make a deep copy to avoid modifying original
        import copy
        result = copy.deepcopy(grid)
        
        # Apply rotations from largest to smallest
        for level_idx, (size, num_blocks) in enumerate(self.levels):
            blocks_per_row = int(100 / size)
            for br in range(blocks_per_row):
                for bc in range(blocks_per_row):
                    rotation = self.rotations[(level_idx, br, bc)]
                    if rotation > 0:
                        block = self._extract_block(result, size, br, bc)
                        rotated = self._rotate_block(block, rotation)
                        self._insert_block(result, rotated, size, br, bc)
        
        return result
    
    def reverse(self, grid: List[List[str]]) -> List[List[str]]:
        """
        Reverse all rotations (apply in opposite order, opposite direction).
        
        Args:
            grid: 100x100 grid of characters
        
        Returns:
            Original grid before rotations
        """
        import copy
        result = copy.deepcopy(grid)
        
        # Apply reverse rotations from smallest to largest
        for level_idx, (size, num_blocks) in reversed(list(enumerate(self.levels))):
            blocks_per_row = int(100 / size)
            for br in range(blocks_per_row):
                for bc in range(blocks_per_row):
                    rotation = self.rotations[(level_idx, br, bc)]
                    if rotation > 0:
                        # Reverse rotation: (4 - rotation) % 4
                        reverse_rot = (4 - rotation) % 4
                        block = self._extract_block(result, size, br, bc)
                        reversed_block = self._rotate_block(block, reverse_rot)
                        self._insert_block(result, reversed_block, size, br, bc)
        
        return result
    
    def get_rotation_info(self) -> Dict:
        """Return information about rotations for debugging."""
        info = {}
        for level_idx, (size, num_blocks) in enumerate(self.levels):
            blocks_per_row = int(100 / size)
            level_rots = []
            for br in range(blocks_per_row):
                row_rots = []
                for bc in range(blocks_per_row):
                    row_rots.append(self.rotations[(level_idx, br, bc)])
                level_rots.append(row_rots)
            info[f"level_{size}"] = level_rots
        return info