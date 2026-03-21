"""
Test con el texto de 1984 de George Orwell
Muestra el flujo completo: Fase 0 (preprocesamiento) + Fase 1 (rotaciones)
"""

import sys
sys.path.append('src')
from phase0_preprocessing import Phase0Preprocessing
from phase1_rotations import Phase1Rotations
import random
import time

# Texto de 1984 (primer párrafo del libro)
texto_1984 = """It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him. The hallway smelt of boiled cabbage and old rag mats. At one end of it a coloured poster, too large for indoor display, had been tacked to the wall. It depicted simply an enormous face, more than a metre wide: the face of a man of about forty-five, with a heavy black moustache and ruggedly handsome features. Winston made for the stairs. It was no use trying the lift. Even at the best of times it was seldom working, and at present the electric current was cut off during daylight hours. It was part of the economy drive in preparation for Hate Week. The flat was seven flights up, and Winston, who was thirty-nine and had a varicose ulcer above his right ankle, went slowly, resting several times on the way. On each landing, opposite the lift-shaft, the poster with the enormous face gazed from the wall. It was one of those pictures which are so contrived that the eyes follow you about when you move. BIG BROTHER IS WATCHING YOU, the caption beneath it ran."""

print("=" * 70)
print("🔐 TEST CON TEXTO DE 1984 - GEORGE ORWELL")
print("=" * 70)

print(f"\n📝 Texto original (primeros 200 caracteres):")
print(texto_1984[:200] + "...")
print(f"\n📊 Longitud total: {len(texto_1984)} caracteres")
print(f"📊 Palabras aproximadas: {len(texto_1984.split())}")

# Configuración
master_key = random.randbytes(32)
iv = random.randbytes(16)

# 1. Fase 0: Preprocesamiento
print("\n🔷 FASE 0: Generando grid 100x100...")
start = time.time()
phase0 = Phase0Preprocessing()
grid_inicial, seed = phase0.process(texto_1984)
tiempo_f0 = time.time() - start
print(f"   ✅ Grid creado en {tiempo_f0:.2f} segundos")
print(f"   Seed: {seed.hex()[:16]}...")

# Mostrar primeras filas del grid inicial
print("\n📌 PRIMERAS 5 FILAS DEL GRID INICIAL (primeros 60 caracteres):")
for i in range(5):
    fila = ''.join(grid_inicial[i][:60])
    print(f"Row {i:2d}: {fila}...")

# 2. Fase 1: Rotaciones
print("\n🔶 FASE 1: Aplicando rotaciones multiescala...")
rotaciones = Phase1Rotations(master_key, iv)
start = time.time()
grid_rotado = rotaciones.apply(grid_inicial)
tiempo_f1 = time.time() - start
print(f"   ✅ Rotaciones aplicadas en {tiempo_f1:.2f} segundos")

# Mostrar primeras filas del grid rotado
print("\n📌 PRIMERAS 5 FILAS DEL GRID ROTADO (primeros 60 caracteres):")
for i in range(5):
    fila = ''.join(grid_rotado[i][:60])
    print(f"Row {i:2d}: {fila}...")

# 3. Guardar grid rotado completo en un archivo
output_file = "output_1984_rotado.txt"
with open(output_file, 'w') as f:
    f.write("=" * 70 + "\n")
    f.write("GRID COMPLETO DESPUÉS DE ROTACIONES (100x100)\n")
    f.write("Texto original: 1984 - George Orwell\n")
    f.write("=" * 70 + "\n\n")
    
    for i in range(100):
        f.write(f"Row {i:3d}: {''.join(grid_rotado[i])}\n")
    
    # Añadir información de estadísticas
    f.write("\n" + "=" * 70 + "\n")
    f.write("ESTADÍSTICAS\n")
    f.write("=" * 70 + "\n")
    f.write(f"Longitud del texto original: {len(texto_1984)} caracteres\n")
    f.write(f"Tamaño del grid: 100x100 = 10000 caracteres\n")
    f.write(f"Palabras en grid: {len(''.join([''.join(row) for row in grid_inicial]).split())} aprox.\n")
    f.write(f"Seed usada: {seed.hex()}\n")
    f.write(f"Master key (primeros 16 bytes): {master_key.hex()[:16]}...\n")

print(f"\n📁 Archivo guardado: {output_file}")
print(f"   Abrirlo en VS Code con: code {output_file}")

# 4. Verificar reversibilidad
print("\n🔁 Verificando reversibilidad...")
grid_recuperado = rotaciones.reverse(grid_rotado)
es_igual = True
for i in range(100):
    for j in range(100):
        if grid_inicial[i][j] != grid_recuperado[i][j]:
            es_igual = False
            break
    if not es_igual:
        break

if es_igual:
    print("✅ La reversibilidad funciona: el grid recuperado es idéntico al inicial.")
else:
    print("❌ ERROR: No se pudo recuperar el grid original.")

print("\n" + "=" * 70)
print(f"⏱️  Tiempo total: {tiempo_f0 + tiempo_f1:.2f} segundos")
print("=" * 70)