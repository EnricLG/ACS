import sys
import random
from collections import defaultdict

sys.path.append('src')
from phase4_final_substitution import Phase4FinalSubstitution

def test_key_diversity_detailed(samples=20):
    print("\n" + "="*60)
    print("TEST: KEY DIVERSITY (detailed)")
    print("="*60)
    
    iv = bytes(range(16))
    results = []  # list of (master_key, first_cell_value, full_grid_sample)
    
    for i in range(samples):
        master_key = random.randbytes(32)
        cipher = Phase4FinalSubstitution(master_key, iv)
        # Test with a simple dummy grid (100x100 of zeros)
        test_grid = [[0]*100 for _ in range(100)]
        encrypted = cipher.encrypt(test_grid)
        # Store first cell and a hash of the whole grid
        first_cell = encrypted[0][0]
        # Simple hash: sum of first 100 cells (not cryptographic, but enough to spot identity)
        grid_hash = sum(encrypted[0][:100])
        results.append((master_key, first_cell, grid_hash, encrypted))
    
    # Group by first cell value
    groups = defaultdict(list)
    for mk, fc, gh, grid in results:
        groups[fc].append((mk, gh, grid))
    
    collisions = {fc: group for fc, group in groups.items() if len(group) > 1}
    
    if not collisions:
        print("✅ No collisions in first cell for these samples.")
        return
    
    print(f"⚠️ Found collisions in first cell for values: {list(collisions.keys())}")
    print("Checking if full grids are identical...")
    
    for fc, group in collisions.items():
        # Compare first two grids in the group
        grid1 = group[0][2]
        grid2 = group[1][2]
        # Compare all cells
        identical = all(grid1[i][j] == grid2[i][j] for i in range(100) for j in range(100))
        if identical:
            print(f"   ❌ FULL COLLISION: two different keys produced identical 100x100 grid!")
        else:
            print(f"   ✅ Only first cell collided; full grids are different.")

if __name__ == "__main__":
    test_key_diversity_detailed()