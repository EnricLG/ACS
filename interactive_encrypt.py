"""
Interactive encryption script for the layered cipher system.
Allows user to choose which phase to run, and displays the result.
"""

import sys
import os
import time
import random
import webbrowser
from pathlib import Path
from datetime import datetime

# --- Asegurar que se encuentran los módulos de src (funciona tanto en desarrollo como en ejecutable) ---
if getattr(sys, 'frozen', False):
    # Estamos en un ejecutable empaquetado por PyInstaller
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(base_path, 'src'))

# --- Importaciones de los módulos del proyecto ---
from phase0_preprocessing import Phase0Preprocessing
from phase1_rotations import Phase1Rotations
from phase2_dict_cipher import Phase2DictCipher
from phase3_concentric_rotations import Phase3ConcentricRotations
from phase3_pairwise import Phase3Pairwise
from phase4_final_substitution import Phase4FinalSubstitution
from phase3_visual import Phase3Visual
from alphabet import ALPHABET

# ----------------------------------------------------------------------

def get_text_input():
    """Get plaintext from user (multiline)."""
    print("\n" + "="*60)
    print("Enter the text you want to encrypt (press Ctrl+D on a new line to finish):")
    print("="*60)
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    return "\n".join(lines).strip()

def get_phase_choice():
    """Ask user which phase to stop at."""
    print("\n" + "="*60)
    print("Choose the phase to run up to:")
    print("  0 - Preprocessing (grid of characters)")
    print("  1 - Hierarchical rotations")
    print("  2 - Dictionary cipher")
    print("  3 - Concentric square rotations")
    print("  3b - Pairwise transform (numbers) -> colors output")
    print("  4 - Final substitution -> exotic characters output")
    print("="*60)
    while True:
        choice = input("Enter phase (0,1,2,3,3b,4): ").strip()
        if choice in ('0','1','2','3','3b','4'):
            return choice
        print("Invalid choice. Please enter 0,1,2,3,3b, or 4.")

def display_char_grid(grid, title, max_rows=10, max_cols=60):
    """Show a snippet of a character grid in the terminal."""
    print(f"\n📌 {title} (first {max_rows} rows, first {max_cols} chars):")
    for i in range(min(max_rows, len(grid))):
        row = ''.join(grid[i])[:max_cols]
        print(f"Row {i:2d}: {row}...")
    print(f"Full grid size: {len(grid)}x{len(grid[0])}")

def save_char_grid(grid, filename):
    """Save a character grid to a text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        for i, row in enumerate(grid):
            f.write(f"Row {i:3d}: {''.join(row)}\n")

# ----------------------------------------------------------------------

def main():
    print("\n" + "="*60)
    print("LAYERED CIPHER SYSTEM - INTERACTIVE ENCRYPTION")
    print("="*60)

    # 1. Get plaintext
    text = get_text_input()
    if not text:
        print("No text entered. Exiting.")
        return

    print(f"\n📝 Text length: {len(text)} characters, ~{len(text.split())} words.")

    # 2. Random key (always)
    master_key = random.randbytes(32)
    iv = random.randbytes(16)
    print("🔑 Using random key (unique per run).")

    # 3. User chooses phase
    phase_choice = get_phase_choice()

    # 4. Create output folder with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path("interactive_output") / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Output will be saved in: {out_dir}")

    start_time = time.time()

    # Phase 0
    print("\n🔷 Phase 0: Preprocessing...")
    phase0 = Phase0Preprocessing()
    grid0, seed = phase0.process(text)
    print("   Done.")
    save_char_grid(grid0, out_dir / "phase0_grid.txt")
    if phase_choice == '0':
        display_char_grid(grid0, "Grid after preprocessing")
        print(f"\n✅ Full grid saved to {out_dir / 'phase0_grid.txt'}")
        return

    # Phase 1
    print("\n🔶 Phase 1: Hierarchical rotations...")
    rotations = Phase1Rotations(master_key, iv)
    grid1 = rotations.apply(grid0)
    print("   Done.")
    save_char_grid(grid1, out_dir / "phase1_grid.txt")
    if phase_choice == '1':
        display_char_grid(grid1, "Grid after hierarchical rotations")
        print(f"\n✅ Full grid saved to {out_dir / 'phase1_grid.txt'}")
        return

    # Phase 2
    print("\n🔷 Phase 2: Dictionary cipher...")
    cipher2 = Phase2DictCipher(master_key, iv)
    grid2 = cipher2.encrypt(grid1)
    print("   Done.")
    save_char_grid(grid2, out_dir / "phase2_grid.txt")
    if phase_choice == '2':
        display_char_grid(grid2, "Grid after dictionary cipher")
        print(f"\n✅ Full grid saved to {out_dir / 'phase2_grid.txt'}")
        return

    # Phase 3
    print("\n🔶 Phase 3: Concentric square rotations...")
    phase3 = Phase3ConcentricRotations(master_key, iv)
    grid3 = phase3.transform(grid2)
    print("   Done.")
    save_char_grid(grid3, out_dir / "phase3_grid.txt")
    if phase_choice == '3':
        display_char_grid(grid3, "Grid after concentric rotations")
        print(f"\n✅ Full grid saved to {out_dir / 'phase3_grid.txt'}")
        return

    # Phase 3b: pairwise transform (numbers)
    print("\n🔷 Phase 3b: Pairwise transform...")
    grid3_ints = [[ALPHABET.index(ch) for ch in row] for row in grid3]
    pairwise = Phase3Pairwise()
    grid3b = pairwise.transform(grid3_ints)
    print("   Done.")
    # Save numeric grid (as text)
    with open(out_dir / "phase3b_numeric.txt", 'w') as f:
        for i, row in enumerate(grid3b):
            f.write(f"Row {i:3d}: " + " ".join(f"{x:05d}" for x in row) + "\n")
    if phase_choice == '3b':
        # Generate colors HTML
        print("\n🎨 Generating colors visual output...")
        visual_colors = Phase3Visual(seed=b'1984', mode='colors')
        grid_colors = [[visual_colors.to_visual(w) for w in row] for row in grid3b]
        html_colors = visual_colors.to_html(grid_colors)
        colors_file = out_dir / "phase3b_colors.html"
        colors_file.write_text(html_colors, encoding='utf-8')
        print(f"   Colors HTML saved: {colors_file}")
        print("🌐 Opening in browser...")
        webbrowser.open(str(colors_file.absolute()))
        print(f"\n✅ Done. Check your browser for the colors grid.")
        print(f"   Full numeric grid saved to {out_dir / 'phase3b_numeric.txt'}")
        return

    # Phase 4: final substitution
    print("\n🔶 Phase 4: Final substitution...")
    cipher4 = Phase4FinalSubstitution(master_key, iv)
    grid4 = cipher4.encrypt(grid3b)
    print("   Done.")
    # Save numeric grid
    with open(out_dir / "phase4_numeric.txt", 'w') as f:
        for i, row in enumerate(grid4):
            f.write(f"Row {i:3d}: " + " ".join(f"{x:05d}" for x in row) + "\n")
    if phase_choice == '4':
        # Generate exotic characters HTML
        print("\n🎨 Generating exotic characters visual output...")
        visual_chars = Phase3Visual(seed=b'1984', mode='chars')
        grid_chars = [[visual_chars.to_visual(w) for w in row] for row in grid4]
        html_chars = visual_chars.to_html(grid_chars)
        chars_file = out_dir / "phase4_exotic.html"
        chars_file.write_text(html_chars, encoding='utf-8')
        print(f"   Exotic HTML saved: {chars_file}")
        print("🌐 Opening in browser...")
        webbrowser.open(str(chars_file.absolute()))
        print(f"\n✅ Done. Check your browser for the exotic characters grid.")
        print(f"   Full numeric grid saved to {out_dir / 'phase4_numeric.txt'}")
        return

    # Should not happen
    print("Unexpected choice.")

if __name__ == "__main__":
    main()