"""
Audit: Statistical properties of the cipher.
Tests if ciphertexts are uniformly distributed and independent of plaintext.
"""

import sys
import random
import numpy as np
from collections import Counter

sys.path.append('src')
from phase0_preprocessing import Phase0Preprocessing
from phase1_rotations import Phase1Rotations
from phase2_dict_cipher import Phase2DictCipher
from phase3_concentric_rotations import Phase3ConcentricRotations
from phase3_pairwise import Phase3Pairwise
from phase4_final_substitution import Phase4FinalSubstitution
from phase3_visual import Phase3Visual
from alphabet import ALPHABET

def get_final_numbers(plaintext, master_key, iv):
    """Run full pipeline and return final numbers (0-9999)."""
    phase0 = Phase0Preprocessing()
    grid0, _ = phase0.process(plaintext)
    rotations = Phase1Rotations(master_key, iv)
    grid1 = rotations.apply(grid0)
    cipher2 = Phase2DictCipher(master_key, iv)
    grid2 = cipher2.encrypt(grid1)
    phase3 = Phase3ConcentricRotations(master_key, iv)
    grid3 = phase3.transform(grid2)
    grid3_ints = [[ALPHABET.index(ch) for ch in row] for row in grid3]
    pairwise = Phase3Pairwise()
    grid3b = pairwise.transform(grid3_ints)
    cipher4 = Phase4FinalSubstitution(master_key, iv)
    grid4 = cipher4.encrypt(grid3b)
    # Flatten
    return [x for row in grid4 for x in row]

def test_uniformity():
    """Check if numbers 0-9999 appear with roughly equal frequency."""
    print("\n" + "="*60)
    print("TEST 1: UNIFORMITY OF OUTPUT NUMBERS")
    print("="*60)
    
    # Use a fixed key and a long plaintext
    master_key = bytes(range(32))
    iv = bytes(range(16))
    plaintext = " ".join(["test word"] * 1000)  # ~7000 words
    
    print("Generating ciphertext...")
    numbers = get_final_numbers(plaintext, master_key, iv)
    print(f"Total numbers: {len(numbers)}")
    
    # Count frequencies
    counter = Counter(numbers)
    expected = len(numbers) / 10000
    print(f"Expected frequency per value: {expected:.2f}")
    
    # Check min and max
    min_freq = min(counter.values())
    max_freq = max(counter.values())
    print(f"Min frequency: {min_freq}")
    print(f"Max frequency: {max_freq}")
    
    # Chi-square test (simplified)
    chi2 = sum((count - expected)**2 / expected for count in counter.values())
    print(f"Chi-square statistic: {chi2:.2f}")
    print(f"Critical value (99% confidence, 9999 df): ~10400")
    
    if chi2 < 11000:
        print("✅ Distribution appears roughly uniform.")
    else:
        print("⚠️ Distribution may not be uniform.")

def test_avalanche():
    """Test avalanche effect: small change in plaintext should cause large change in ciphertext."""
    print("\n" + "="*60)
    print("TEST 2: AVALANCHE EFFECT")
    print("="*60)
    
    master_key = bytes(range(32))
    iv = bytes(range(16))
    
    plaintext1 = "This is a secret message that needs to be encrypted."
    plaintext2 = "This is a secret message that needs to be encrypted?"  # one char changed
    
    print("Encrypting two very similar messages...")
    nums1 = get_final_numbers(plaintext1, master_key, iv)
    nums2 = get_final_numbers(plaintext2, master_key, iv)
    
    # Count differing positions
    diffs = sum(1 for a, b in zip(nums1, nums2) if a != b)
    total = len(nums1)
    diff_ratio = diffs / total
    print(f"Total cells: {total}")
    print(f"Different cells: {diffs} ({diff_ratio*100:.1f}%)")
    
    if diff_ratio > 0.45:
        print("✅ Avalanche effect is strong.")
    else:
        print("⚠️ Avalanche effect could be stronger.")

def test_key_sensitivity():
    """Test that tiny key changes produce very different outputs."""
    print("\n" + "="*60)
    print("TEST 3: KEY SENSITIVITY")
    print("="*60)
    
    plaintext = "This is a secret message that needs to be encrypted."
    master_key1 = bytes(range(32))
    master_key2 = bytes(range(32))
    # Flip one bit
    master_key2 = master_key2[:0] + bytes([master_key2[0] ^ 1]) + master_key2[1:]
    iv = bytes(range(16))
    
    print("Encrypting with two nearly identical keys...")
    nums1 = get_final_numbers(plaintext, master_key1, iv)
    nums2 = get_final_numbers(plaintext, master_key2, iv)
    
    diffs = sum(1 for a, b in zip(nums1, nums2) if a != b)
    total = len(nums1)
    diff_ratio = diffs / total
    print(f"Different cells: {diffs} ({diff_ratio*100:.1f}%)")
    
    if diff_ratio > 0.45:
        print("✅ Key sensitivity is strong.")
    else:
        print("⚠️ Key sensitivity could be stronger.")

if __name__ == "__main__":
    test_uniformity()
    test_avalanche()
    test_key_sensitivity()