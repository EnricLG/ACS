"""
Phase 3 Visual Mapping: convert numbers 0-9999 to visual representation.
Mode: 'both' (default) -> even -> char, odd -> color
      'colors' -> always color
      'chars'  -> always character (exotic)
"""

import random
import os
from typing import List

class Phase3Visual:
    def __init__(self, seed: bytes = None, mode: str = 'both', char_file: str = None):
        """
        Args:
            seed: random seed for shuffling and color generation
            mode: 'both', 'colors', or 'chars'
            char_file: path to file with 10000 characters (one per line)
        """
        if seed is None:
            seed = b'phase3_visual_default_seed'
        self.rng = random.Random(seed)
        self.mode = mode

        # Load characters
        if char_file is None:
            char_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'exotic_chars.txt')
        self.chars = self._load_chars(char_file)

        # Generate 10000 CSS colors
        self.colors = []
        for _ in range(10000):
            r = self.rng.randint(0, 255)
            g = self.rng.randint(0, 255)
            b = self.rng.randint(0, 255)
            self.colors.append(f"#{r:02x}{g:02x}{b:02x}")

        # Build reverse mappings
        self._rev_chars = {ch: i*2 for i, ch in enumerate(self.chars)}
        self._rev_colors = {col: i*2+1 for i, col in enumerate(self.colors)}

    def _load_chars(self, filepath: str) -> List[str]:
        """Load characters from file, one per line. Ensure at least 10000."""
        if not os.path.exists(filepath):
            print(f"⚠️  File {filepath} not found. Generating fallback characters...")
            chars = [chr(0x4E00 + i) for i in range(10000)]
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                chars = [line.strip() for line in f if line.strip()]
        if len(chars) < 10000:
            chars = (chars * (10000 // len(chars) + 1))[:10000]
        elif len(chars) > 10000:
            chars = chars[:10000]
        self.rng.shuffle(chars)
        return chars

    def to_visual(self, w: int) -> str:
        """Convert number 0-9999 to visual representation based on mode."""
        if not (0 <= w < 10000):
            raise ValueError(f"Value {w} out of range [0,9999]")
        if self.mode == 'colors':
            return self.colors[w]
        elif self.mode == 'chars':
            return self.chars[w]
        else:  # 'both'
            if w % 2 == 0:
                return self.chars[w // 2]
            else:
                return self.colors[(w - 1) // 2]

    def from_visual(self, visual: str) -> int:
        """Reverse mapping (only works for mode='both' because mixing)."""
        if self.mode == 'both':
            if visual in self._rev_chars:
                return self._rev_chars[visual]
            elif visual in self._rev_colors:
                return self._rev_colors[visual]
            else:
                raise ValueError(f"Visual '{visual}' not found")
        else:
            raise NotImplementedError("Reverse mapping only implemented for mode='both'")

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
            '<h2>Phase 4 Visual Output (Exotic Characters Only)</h2>',
            '<p>Grid size: 100x100</p>',
            '<table border="1" cellspacing="0" cellpadding="5">'
        ]

        for row in grid_visual:
            html_lines.append('     <tr>')
            for cell in row:
                if cell.startswith('#'):
                    html_lines.append(f'    <td style="background-color:{cell};">&nbsp;</td>')
                else:
                    html_lines.append(f'    <td style="font-size:20px; text-align:center;">{cell}</td>')
            html_lines.append('     </tr>')

        html_lines.append('</table>')
        html_lines.append('</body>')
        html_lines.append('</html>')

        return '\n'.join(html_lines)