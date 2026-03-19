import sys
sys.path.append('src')
from phase0_preprocessing import Phase0Preprocessing
from phase1_rotations import Phase1Rotations
import random

# 1. Create a test grid with visible pattern
print("=" * 60)
print("TESTING PHASE 1: MULTI-SCALE ROTATIONS")
print("=" * 60)

# Create a simple pattern grid (numbers 0-99 in each cell as string)
test_grid = []
for i in range(100):
    row = []
    for j in range(100):
        # Create a visible pattern: first digit = row//10, second digit = col//10
        pattern = f"{i//10}{j//10}"
        row.append(pattern)
    test_grid.append(row)

print("\nOriginal grid (first 5 rows, first 20 cols):")
for i in range(5):
    print(f"Row {i}: {''.join(test_grid[i][:20])}...")

# 2. Apply rotations
master_key = random.randbytes(32)
iv = random.randbytes(16)

rotations = Phase1Rotations(master_key, iv)
rotated_grid = rotations.apply(test_grid)

print("\n\nAfter rotations (first 5 rows, first 20 cols):")
for i in range(5):
    print(f"Row {i}: {''.join(rotated_grid[i][:20])}...")

# 3. Reverse rotations
reversed_grid = rotations.reverse(rotated_grid)

print("\n\nAfter reverse rotations (first 5 rows, first 20 cols):")
for i in range(5):
    print(f"Row {i}: {''.join(reversed_grid[i][:20])}...")

# 4. Verify reversibility
is_equal = True
for i in range(100):
    for j in range(100):
        if test_grid[i][j] != reversed_grid[i][j]:
            is_equal = False
            print(f"Mismatch at ({i},{j}): {test_grid[i][j]} vs {reversed_grid[i][j]}")
            break
    if not is_equal:
        break

print("\n" + "=" * 60)
if is_equal:
    print("✅ REVERSIBILITY VERIFIED: Original == Reversed")
else:
    print("❌ ERROR: Reversal failed")

# Show some rotation info
print("\nRotation parameters (sample):")
info = rotations.get_rotation_info()
for level, rots in list(info.items())[:3]:  # Show first 3 levels
    print(f"{level}: first 3x3 block rotations:")
    for r in rots[:3]:
        print(f"  {r[:3]}")