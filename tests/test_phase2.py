import sys
import random
sys.path.append('src')
from phase2_dict_cipher import Phase2DictCipher
from alphabet import ALPHABET

# Create a 100x100 test grid with a deterministic pattern
test_grid = []
for i in range(100):
    row = []
    for j in range(100):
        idx = (i * 100 + j) % 100
        row.append(ALPHABET[idx])
    test_grid.append(row)

print("Original grid (first 5 rows, first 10 cols):")
for i in range(5):
    print(''.join(test_grid[i][:10]))

# Generate a master key and IV
master_key = random.randbytes(32)
iv = random.randbytes(16)

# Create cipher object
cipher = Phase2DictCipher(master_key, iv)

# Encrypt
encrypted = cipher.encrypt(test_grid)
print("\nEncrypted grid (first 5 rows, first 10 cols):")
for i in range(5):
    print(''.join(encrypted[i][:10]))

# Decrypt
decrypted = cipher.decrypt(encrypted)
print("\nDecrypted grid (first 5 rows, first 10 cols):")
for i in range(5):
    print(''.join(decrypted[i][:10]))

# Verify full reversibility
success = True
for i in range(100):
    for j in range(100):
        if test_grid[i][j] != decrypted[i][j]:
            print(f"Mismatch at ({i},{j}): expected '{test_grid[i][j]}', got '{decrypted[i][j]}'")
            success = False
            break
    if not success:
        break

if success:
    print("\n✅ Reversibility verified! The Phase 2 works correctly.")
else:
    print("\n❌ Decryption failed.")