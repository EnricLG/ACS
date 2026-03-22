"""
Phase 3 Visual Mapping: convert numbers 0-9999 to visual representations.
Supports three modes:
- 'both': even numbers -> Chinese/exotic characters, odd numbers -> CSS colors.
- 'colors': all numbers -> CSS colors (from the color list).
- 'chars': all numbers -> characters (from the character list).
"""

import random
import os
from typing import List

class Phase3Visual:
    def __init__(self, seed: bytes = None, char_file: str = None, mode='both'):
        """
        Initialize visual mapping.

        Args:
            seed: Random seed for generating colors and shuffling characters.
            char_file: Path to a file with characters (one per line).
            mode: 'both', 'colors', or 'chars'. Determines output type.
        """
        if seed is None:
            seed = b'phase3_visual_default_seed'
        self.rng = random.Random(seed)
        self.mode = mode

        # Load characters (can be Chinese, exotic, etc.)
        if char_file is None:
            char_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'exotic_chars.txt')
        self.chars = self._load_chars(char_file)

        # Generate 10,000 CSS colors
        self.colors = []
        for _ in range(10000):
            r = self.rng.randint(0, 255)
            g = self.rng.randint(0, 255)
            b = self.rng.randint(0, 255)
            self.colors.append(f"#{r:02x}{g:02x}{b:02x}")

        # Build reverse mappings for decryption
        self._rev_chars = {ch: i for i, ch in enumerate(self.chars)}
        self._rev_colors = {col: i for i, col in enumerate(self.colors)}

    def _load_chars(self, filepath: str) -> List[str]:
        """Load characters from file, one per line."""
        if not os.path.exists(filepath):
            print(f"⚠️  File {filepath} not found. Generating fallback characters...")
            # Generate 10,000 characters from CJK block as fallback
            chars = [chr(0x4E00 + i) for i in range(10000)]
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                chars = [line.strip() for line in f if line.strip()]
        # Ensure we have at least 10000
        if len(chars) < 10000:
            chars = (chars * (10000 // len(chars) + 1))[:10000]
        elif len(chars) > 10000:
            chars = chars[:10000]
        # Shuffle characters using the PRNG for variety
        self.rng.shuffle(chars)
        return chars

    def to_visual(self, w: int) -> str:
        """Convert a number 0-9999 to its visual representation."""
        if not (0 <= w < 10000):
            raise ValueError(f"Value {w} out of range [0,9999]")

        if self.mode == 'both':
            if w % 2 == 0:
                return self.chars[w // 2]
            else:
                return self.colors[(w - 1) // 2]
        elif self.mode == 'colors':
            return self.colors[w]
        elif self.mode == 'chars':
            return self.chars[w]
        else:
            raise ValueError(f"Invalid mode: {self.mode}")

    def from_visual(self, visual: str) -> int:
        """Reverse: given a visual string, return the original w."""
        if self.mode in ('both', 'chars'):
            if visual in self._rev_chars:
                if self.mode == 'both':
                    return self._rev_chars[visual] * 2  # even numbers
                else:
                    return self._rev_chars[visual]
        if self.mode in ('both', 'colors'):
            if visual in self._rev_colors:
                if self.mode == 'both':
                    return self._rev_colors[visual] * 2 + 1
                else:
                    return self._rev_colors[visual]
        raise ValueError(f"Visual '{visual}' not found in mapping")

    def to_html(self, grid_visual):
        """Generate an HTML table showing the visual representation."""
        html_lines = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '<meta charset="UTF-8">',
            '<style>',
            'table { border-collapse: collapse; }',
            'td { width: 30px; height: 30px; text-align: center; font-size: 20px; }',
            '</style>',
            '</head>',
            '<body>',
            '<h2>Phase 3 Visual Output</h2>',
            '<p>Grid size: 100x100</p>',
            '<table border="1" cellspacing="0" cellpadding="5">'
        ]

        for row in grid_visual:
            html_lines.append('    <td>')
            for cell in row:
                if cell.startswith('#'):
                    # Color cell
                    html_lines.append(f'    <td style="background-color:{cell};">&nbsp;<\/td>')
                else:
                    # Character cell
                    html_lines.append(f'    <td style="font-size:20px; text-align:center;">{cell}<\/td>')
            html_lines.append('    <\/tr>')

        html_lines.append('<\/table>')
        html_lines.append('</body>')
        html_lines.append('</html>')
        return '\n'.join(html_lines)