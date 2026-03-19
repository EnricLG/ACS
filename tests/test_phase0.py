import sys
sys.path.append('src')
from phase0_preprocessing import Phase0Preprocessing

text = "Hello world this is a secret message that needs to be encrypted"

phase0 = Phase0Preprocessing()
grid, seed = phase0.process(text)

# Guardar en archivo
with open('output_grid.txt', 'w') as f:
    f.write("GRID COMPLETO 100×100\n")
    f.write("=" * 60 + "\n")
    for i in range(100):
        f.write(f"Row {i:2d}: {''.join(grid[i])}\n")
    
    f.write("\n" + "=" * 60 + "\n")
    f.write("PALABRAS ORIGINALES\n")
    f.write("=" * 60 + "\n")
    
    all_text = ' '.join([''.join(row) for row in grid])
    original_words = text.split()
    
    for word in original_words:
        f.write(f"\nBuscando '{word}':\n")
        # Buscar en el texto
        for i in range(len(all_text) - len(word)):
            if all_text[i:i+len(word)] == word:
                row = i // 100
                col = i % 100
                f.write(f"  → Encontrada exacta en fila {row}, columna {col}\n")
        
        # Buscar con padding (word + letras extra)
        for padded_len in range(len(word), min(len(word)+5, 10)):
            for i in range(len(all_text) - padded_len):
                segment = all_text[i:i+padded_len]
                if segment.startswith(word) and len(segment) > len(word):
                    row = i // 100
                    col = i % 100
                    f.write(f"  → Encontrada con padding '{segment}' en fila {row}, columna {col}\n")

print(f"Archivo 'output_grid.txt' creado. Seed: {seed.hex()}")