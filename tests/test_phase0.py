"""
Test de la Fase 0 (preprocesamiento) con el texto de 1984.
Muestra el grid de 100×100 generado y guarda el resultado.
"""

import sys
sys.path.append('src')
from phase0_preprocessing import Phase0Preprocessing

# Texto de 1984 (primer párrafo del libro)
texto_1984 = """It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him. The hallway smelt of boiled cabbage and old rag mats. At one end of it a coloured poster, too large for indoor display, had been tacked to the wall. It depicted simply an enormous face, more than a metre wide: the face of a man of about forty-five, with a heavy black moustache and ruggedly handsome features. Winston made for the stairs. It was no use trying the lift. Even at the best of times it was seldom working, and at present the electric current was cut off during daylight hours. It was part of the economy drive in preparation for Hate Week. The flat was seven flights up, and Winston, who was thirty-nine and had a varicose ulcer above his right ankle, went slowly, resting several times on the way. On each landing, opposite the lift-shaft, the poster with the enormous face gazed from the wall. It was one of those pictures which are so contrived that the eyes follow you about when you move. BIG BROTHER IS WATCHING YOU, the caption beneath it ran."""

print("=" * 70)
print("🔐 FASE 0 – TEST CON TEXTO DE 1984 (GEORGE ORWELL)")
print("=" * 70)

print(f"\n📝 Texto original (primeros 200 caracteres):")
print(texto_1984[:200] + "...")
print(f"\n📊 Longitud total: {len(texto_1984)} caracteres")
print(f"📊 Palabras aproximadas: {len(texto_1984.split())}")

# Procesar con Fase 0
phase0 = Phase0Preprocessing()
grid, seed = phase0.process(texto_1984)

# Mostrar primeras filas
print("\n📌 PRIMERAS 5 FILAS DEL GRID INICIAL (primeros 60 caracteres):")
for i in range(5):
    fila = ''.join(grid[i][:60])
    print(f"Row {i:2d}: {fila}...")

# Guardar grid completo en archivo
output_file = "output_phase0_1984.txt"
with open(output_file, 'w') as f:
    f.write("=" * 70 + "\n")
    f.write("GRID COMPLETO DESPUÉS DE FASE 0 (100×100)\n")
    f.write("Texto original: 1984 – George Orwell\n")
    f.write("=" * 70 + "\n\n")
    for i in range(100):
        f.write(f"Row {i:3d}: {''.join(grid[i])}\n")
    f.write(f"\nSeed usada: {seed.hex()}\n")

print(f"\n📁 Archivo guardado: {output_file}")
print("   Abrirlo con: code output_phase0_1984.txt")