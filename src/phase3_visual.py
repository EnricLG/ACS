"""
Phase 3 Visual Mapping: convert numbers 0-9999 to Chinese characters or CSS colors.
Reversible using deterministic PRNG with fixed seed.
"""

import random
import os

class Phase3Visual:
    def __init__(self, seed: bytes = None, chinese_file: str = None):
        """
        Initialize visual mapping.
        
        Args:
            seed: Random seed for generating colors and shuffling characters.
            chinese_file: Path to a file with Chinese characters (one per line).
                          If None, uses default generated list.
        """
        if seed is None:
            seed = b'phase3_visual_default_seed'
        self.rng = random.Random(seed)
        
        # Load Chinese characters
        if chinese_file is None:
            # Try default location
            chinese_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'chinese_chars.txt')
        self.chinese = self._load_chinese_chars(chinese_file)
        
        # Generate 10,000 CSS colors
        self.colors = []
        for _ in range(10000):
            r = self.rng.randint(0, 255)
            g = self.rng.randint(0, 255)
            b = self.rng.randint(0, 255)
            self.colors.append(f"#{r:02x}{g:02x}{b:02x}")

        # Build reverse mappings for decryption
        self._rev_chinese = {ch: i*2 for i, ch in enumerate(self.chinese)}
        self._rev_colors = {col: i*2+1 for i, col in enumerate(self.colors)}

    def _load_chinese_chars(self, filepath: str):
        """Load Chinese characters from file, one per line."""
        # If file doesn't exist, generate fallback characters from Unicode range
        if not os.path.exists(filepath):
            print(f"⚠️  File {filepath} not found. Generating fallback Chinese characters...")
            # Generate 10,000 characters from CJK Unified Ideographs block
            chars = []
            start = 0x4E00
            for i in range(10000):
                chars.append(chr(start + i))
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                chars = [line.strip() for line in f if line.strip()]
        
        # Ensure we have at least 10000 characters
        if len(chars) < 10000:
            print(f"⚠️  Only {len(chars)} chars found. Repeating to reach 10000...")
            chars = (chars * (10000 // len(chars) + 1))[:10000]
        elif len(chars) > 10000:
            chars = chars[:10000]
        
        # Shuffle characters using the PRNG for variety
        self.rng.shuffle(chars)
        return chars

    def to_visual(self, w: int) -> str:
        """
        Convert a number 0-9999 to its visual representation.
        Even numbers → Chinese character.
        Odd numbers → CSS color.
        """
        if not (0 <= w < 10000):
            raise ValueError(f"Value {w} out of range [0,9999]")
        
        if w % 2 == 0:
            return self.chinese[w // 2]
        else:
            return self.colors[(w - 1) // 2]

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
            '<h2>Phase 3 Visual Output (Chinese Characters / CSS Colors)</h2>',
            '<p>Grid size: 100x100</p>',
            '<table border="1" cellspacing="0" cellpadding="5">'
        ]
        
        for row in grid_visual:
            html_lines.append('    <tr>')
            for cell in row:
                if cell.startswith('#'):
                    # Color cell
                    html_lines.append(f'    <td style="background-color:{cell};">&nbsp;</td>')
                else:
                    # Chinese character cell
                    html_lines.append(f'    <td style="font-size:20px; text-align:center;">{cell}</td>')
            html_lines.append('    </tr>')
        
        html_lines.append('</table>')
        html_lines.append('</body>')
        html_lines.append('</html>')
        
        return '\n'.join(html_lines)