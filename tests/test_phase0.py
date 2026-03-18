import sys
sys.path.append('src')
from phase0_preprocessing import Phase0Preprocessing

# Test text
text = "Hello world this is a secret message that needs to be encrypted"

# Process
phase0 = Phase0Preprocessing()
grid, seed = phase0.process(text)

# Show first 5 rows (first 50 characters of each)
print("First 5 rows of the 100×100 grid:")
for i in range(5):
    print(f"Row {i}: {''.join(grid[i][:50])}...")

print(f"\nGrid size: {len(grid)}x{len(grid[0])}")
print(f"Seed used: {seed.hex()}")