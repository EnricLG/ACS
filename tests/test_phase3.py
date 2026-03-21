import sys
sys.path.append('src')
from phase3_pairwise import Phase3Pairwise

# Create a 100x100 test grid with a repeating pattern of 0-99
test_grid = []
for i in range(100):
    row = []
    for j in range(100):
        row.append((i * 100 + j) % 100)  # ensures 0-99 values
    test_grid.append(row)

print("Original grid (first 3x3):")
for i in range(3):
    print(' '.join(f"{x:2d}" for x in test_grid[i][:3]))

# Transform
phase3 = Phase3Pairwise()
transformed = phase3.transform(test_grid)

print("\nTransformed grid (first 3x3 numbers):")
for i in range(3):
    print(' '.join(f"{x:5d}" for x in transformed[i][:3]))

# Inverse
recovered = phase3.inverse(transformed)

print("\nRecovered grid (first 3x3):")
for i in range(3):
    print(' '.join(f"{x:2d}" for x in recovered[i][:3]))

# Verify full 100x100 equality (check first few to save time, but we can check all)
success = True
for i in range(100):
    for j in range(100):
        if test_grid[i][j] != recovered[i][j]:
            print(f"Mismatch at ({i},{j}): {test_grid[i][j]} vs {recovered[i][j]}")
            success = False
            break
    if not success:
        break

if success:
    print("\n✅ Reversibility verified for 100x100 grid!")
else:
    print("\n❌ Reversibility failed.")