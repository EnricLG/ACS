"""
Test de integración: Fase 0 (preprocesamiento) + Fase 1 (rotaciones)
Muestra el grid antes y después de las rotaciones, y guarda el resultado en un archivo.
"""

import sys
sys.path.append('src')
from phase0_preprocessing import Phase0Preprocessing
from phase1_rotations import Phase1Rotations
import random
import os

# Configuración
texto_original = "Hello world this is a secret message that needs to be encrypted"
master_key = random.randbytes(32)
iv = random.randbytes(16)

print("=" * 70)
print("INTEGRACIÓN FASE 0 + FASE 1")
print("=" * 70)

# 1. Fase 0: Preprocesamiento
print("\n🔷 FASE 0: Generando grid 100x100...")
phase0 = Phase0Preprocessing()
grid_inicial, seed = phase0.process(texto_original)
print(f"   Grid creado. Seed: {seed.hex()[:16]}...")

# Mostrar primeras filas del grid inicial
print("\n📌 PRIMERAS 5 FILAS DEL GRID INICIAL (primeros 60 caracteres):")
for i in range(5):
    fila = ''.join(grid_inicial[i][:60])
    print(f"Row {i:2d}: {fila}...")

# 2. Fase 1: Rotaciones
print("\n🔶 FASE 1: Aplicando rotaciones multiescala...")
rotaciones = Phase1Rotations(master_key, iv)
grid_rotado = rotaciones.apply(grid_inicial)
print("   Rotaciones aplicadas.")

# Mostrar primeras filas del grid rotado
print("\n📌 PRIMERAS 5 FILAS DEL GRID ROTADO (primeros 60 caracteres):")
for i in range(5):
    fila = ''.join(grid_rotado[i][:60])
    print(f"Row {i:2d}: {fila}...")

# 3. Guardar grid rotado completo en un archivo
output_file = "output_grid_rotado.txt"
with open(output_file, 'w') as f:
    f.write("GRID COMPLETO DESPUÉS DE ROTACIONES (100x100)\n")
    f.write("=" * 70 + "\n")
    for i in range(100):
        f.write(f"Row {i:3d}: {''.join(grid_rotado[i])}\n")
    
    # Añadir información de búsqueda de palabras originales
    f.write("\n" + "=" * 70 + "\n")
    f.write("BÚSQUEDA DE PALABRAS ORIGINALES (con padding)\n")
    f.write("=" * 70 + "\n")
    
    # Convertir el grid rotado a texto continuo
    all_text = ' '.join([''.join(row) for row in grid_rotado])
    
    palabras_originales = texto_original.split()
    for palabra in palabras_originales:
        # La palabra puede tener padding (hasta 9 letras)
        encontradas = []
        for lon in range(len(palabra), 10):  # buscar longitudes desde la original hasta 9
            for i in range(len(all_text) - lon):
                segmento = all_text[i:i+lon]
                if segmento.startswith(palabra):
                    # Calcular fila y columna aproximadas
                    fila = i // 100
                    col = i % 100
                    encontradas.append((segmento, fila, col))
        if encontradas:
            f.write(f"\n✅ '{palabra}' encontrada como:\n")
            for seg, fila, col in encontradas[:3]:  # mostrar solo las primeras 3
                f.write(f"   - '{seg}' en fila {fila}, columna {col}\n")
        else:
            f.write(f"\n❌ '{palabra}' NO encontrada (puede estar fragmentada por espacios)\n")

print(f"\n📁 Archivo guardado: {output_file}")
print("   Puedes abrirlo en VS Code con: code output_grid_rotado.txt")

# 4. Verificar reversibilidad (opcional)
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