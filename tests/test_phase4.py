import sys
import random
sys.path.append('src')
from phase4_final_substitution import Phase4FinalSubstitution

# Create a test grid of numbers 0-9999 (a simple pattern)
test_grid = []
for i in range(100):
    row = []
    for j in range(100):
        row.append((i * 100 + j) % 10000)
    test_grid.append(row)

print("Original grid (first 3x3):")
for i in range(3):
    print(' '.join(f"{x:5d}" for x in test_grid[i][:3]))

# Generate master key and IV
master_key = random.randbytes(32)
iv = random.randbytes(16)

# Encrypt
cipher = Phase4FinalSubstitution(master_key, iv)
encrypted = cipher.encrypt(test_grid)

print("\nEncrypted grid (first 3x3):")
for i in range(3):
    print(' '.join(f"{x:5d}" for x in encrypted[i][:3]))

# Decrypt
decrypted = cipher.decrypt(encrypted)

print("\nDecrypted grid (first 3x3):")
for i in range(3):
    print(' '.join(f"{x:5d}" for x in decrypted[i][:3]))

# Verify
success = True
for i in range(100):
    for j in range(100):
        if test_grid[i][j] != decrypted[i][j]:
            print(f"Mismatch at ({i},{j}): {test_grid[i][j]} vs {decrypted[i][j]}")
            success = False
            break
    if not success:
        break

if success:
    print("\n✅ Reversibility verified! Phase 4 works correctly.")
else:
    print("\n❌ Decryption failed.")