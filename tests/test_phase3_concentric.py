import sys
sys.path.append('src')
from phase3_concentric_rotations import Phase3ConcentricRotations
import random

# Create a simple test grid (100x100) with numbers 0..9999 as strings
test_grid = [[f"{i*100 + j:04d}" for j in range(100)] for i in range(100)]

print("Original grid (first 3x3):")
for i in range(3):
    print(' '.join(test_grid[i][:3]))

# Generate master key and IV
master_key = random.randbytes(32)
iv = random.randbytes(16)

# Apply transform
rotations = Phase3ConcentricRotations(master_key, iv)
transformed = rotations.transform(test_grid)

print("\nTransformed grid (first 3x3):")
for i in range(3):
    print(' '.join(transformed[i][:3]))

# Reverse
recovered = rotations.inverse(transformed)

print("\nRecovered grid (first 3x3):")
for i in range(3):
    print(' '.join(recovered[i][:3]))

# Verify
if all(test_grid[i][j] == recovered[i][j] for i in range(100) for j in range(100)):
    print("\n✅ Reversibility verified!")
else:
    print("\n❌ Reversibility failed.")