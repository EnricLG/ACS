"""
Full encryption pipeline for 1984 text:
- Phase 0: Preprocessing
- Phase 1: Multi-scale rotations
- Phase 2: Dictionary cipher
- Outputs saved after each phase for reference.
"""

import sys
import time
sys.path.append('src')
from phase0_preprocessing import Phase0Preprocessing
from phase1_rotations import Phase1Rotations
from phase2_dict_cipher import Phase2DictCipher

def clean_text(text: str) -> str:
    """Replace non‑ASCII punctuation with ASCII equivalents."""
    text = text.replace('‘', "'").replace('’', "'")
    text = text.replace('—', '-')
    # Optionally, remove any remaining non‑alphabet characters:
    # (alphabet defined in alphabet.py: 100 chars)
    return text

# Full 1984 text (with original punctuation)
texto_1984 = """It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him. The hallway smelt of boiled cabbage and old rag mats. At one end of it a coloured poster, too large for indoor display, had been tacked to the wall. It depicted simply an enormous face, more than a metre wide: the face of a man of about forty-five, with a heavy black moustache and ruggedly handsome features. Winston made for the stairs. It was no use trying the lift. Even at the best of times it was seldom working, and at present the electric current was cut off during daylight hours. It was part of the economy drive in preparation for Hate Week. The flat was seven flights up, and Winston, who was thirty-nine and had a varicose ulcer above his right ankle, went slowly, resting several times on the way. On each landing, opposite the lift-shaft, the poster with the enormous face gazed from the wall. It was one of those pictures which are so contrived that the eyes follow you about when you move. BIG BROTHER IS WATCHING YOU, the caption beneath it ran. Inside the flat a fruity voice was reading out a list of figures which had something to do with the production of pig-iron. The voice came from an oblong metal plaque like a dulled mirror which formed part of the surface of the right-hand wall. Winston turned a switch and the voice sank somewhat, though the words were still distinguishable. The instrument (the telescreen, it was called) could be dimmed, but there was no way of shutting it off completely. He moved over to the window: a smallish, frail figure, the meagreness of his body merely emphasized by the blue overalls which were the uniform of the Party. Outside, the world was still flat. He thought of the Ministry of Truth, with its millions of rooms, its endless corridors, its enormous staff, its race of lunatics not subject to orders from any human authority, but moving only at the bidding of the telescreens. He thought of the Ministry of Love, which was the real centre of power, the place of no windows, the place where there was no law. He thought of the Ministry of Plenty, with its pyramids of canned goods, its concrete piles, its mountains of scrap metal. He thought of the Ministry of Peace, which was concerned with war. And he thought of the face of Big Brother, which never changed, and which looked down on everything he did. He turned his eyes to the telescreen. The voice had continued, but now it changed its tone, becoming more urgent. It was giving instructions to the citizens of Oceania on how to behave during Hate Week. Winston listened with a mixture of fear and fascination. He had heard it all before, but it still had the power to disturb him. He was not particularly brave, but he was not a coward either. He was simply a man who had lived through too much to be surprised by anything any more. He had been born in the early years of the Revolution, and he had seen the Party grow from a small underground organization into the colossus that now bestrode the earth. He had seen the great purges, the forced marches, the famines, the wars. He had seen the Party change its mind about everything a dozen times. He had seen the comradeship of the early days turn into the icy discipline of the present. He had seen the Party’s enemies—the Trotskyists, the anarchists, the saboteurs—disappear one by one into the vortex of the Ministry of Love. He had seen the Party’s allies—the capitalists, the imperialists, the feudalists—become its enemies overnight. He had seen the Party’s slogans change from ‘War is Peace’ to ‘Peace is War’, from ‘Freedom is Slavery’ to ‘Slavery is Freedom’, from ‘Ignorance is Strength’ to ‘Strength is Ignorance’. He had seen the Party’s leaders—the great heroes of the Revolution—fall from grace and be executed as traitors. He had seen the Party’s history rewritten so many times that he no longer knew what was true and what was false."""

texto_1984 = clean_text(texto_1984)

# Fixed key and IV for reproducibility
master_key = bytes(range(32))   # 0x00..0x1f
iv = bytes(range(16))           # 0x00..0x0f

print("=" * 70)
print("Full encryption pipeline for 1984 text (Phases 0, 1, 2)")
print("=" * 70)

# Phase 0
print("\n🔷 Phase 0: Preprocessing...")
phase0 = Phase0Preprocessing()
start = time.time()
grid0, seed0 = phase0.process(texto_1984)
print(f"   Done in {time.time()-start:.2f}s. Seed: {seed0.hex()[:16]}...")

with open("output_1984_phase0.txt", "w") as f:
    f.write("Phase 0: Grid after preprocessing (100x100)\n")
    f.write("=" * 70 + "\n")
    for i in range(100):
        f.write(f"Row {i:3d}: {''.join(grid0[i])}\n")
    f.write(f"\nSeed: {seed0.hex()}\n")

# Phase 1
print("\n🔶 Phase 1: Rotations...")
rotations = Phase1Rotations(master_key, iv)
start = time.time()
grid1 = rotations.apply(grid0)
print(f"   Done in {time.time()-start:.2f}s.")

with open("output_1984_phase1.txt", "w") as f:
    f.write("Phase 1: Grid after multi-scale rotations (100x100)\n")
    f.write("=" * 70 + "\n")
    for i in range(100):
        f.write(f"Row {i:3d}: {''.join(grid1[i])}\n")
    f.write(f"\nSeed: {seed0.hex()}\n")
    f.write(f"Master key (first 16 bytes): {master_key.hex()[:16]}...\n")
    f.write(f"IV: {iv.hex()}\n")

# Phase 2
print("\n🔷 Phase 2: Dictionary cipher...")
cipher = Phase2DictCipher(master_key, iv)
start = time.time()
grid2 = cipher.encrypt(grid1)
print(f"   Done in {time.time()-start:.2f}s.")

with open("output_1984_phase2.txt", "w") as f:
    f.write("Phase 2: Final ciphertext after dictionary cipher (100x100)\n")
    f.write("=" * 70 + "\n")
    for i in range(100):
        f.write(f"Row {i:3d}: {''.join(grid2[i])}\n")
    f.write(f"\nSeed: {seed0.hex()}\n")
    f.write(f"Master key (first 16 bytes): {master_key.hex()[:16]}...\n")
    f.write(f"IV: {iv.hex()}\n")

print("\n✅ Output files created: output_1984_phase0.txt, output_1984_phase1.txt, output_1984_phase2.txt")