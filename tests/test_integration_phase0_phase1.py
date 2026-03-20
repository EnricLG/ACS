"""
Test de integración: Fase 0 + Fase 1 con el texto completo de 1984.
Muestra el grid antes y después de las rotaciones.
"""

import sys
sys.path.append('src')
from phase0_preprocessing import Phase0Preprocessing
from phase1_rotations import Phase1Rotations
import random
import time

# Texto completo de 1984 (mismo que en test_phase0)
texto_1984_completo = """It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him. The hallway smelt of boiled cabbage and old rag mats. At one end of it a coloured poster, too large for indoor display, had been tacked to the wall. It depicted simply an enormous face, more than a metre wide: the face of a man of about forty-five, with a heavy black moustache and ruggedly handsome features. Winston made for the stairs. It was no use trying the lift. Even at the best of times it was seldom working, and at present the electric current was cut off during daylight hours. It was part of the economy drive in preparation for Hate Week. The flat was seven flights up, and Winston, who was thirty-nine and had a varicose ulcer above his right ankle, went slowly, resting several times on the way. On each landing, opposite the lift-shaft, the poster with the enormous face gazed from the wall. It was one of those pictures which are so contrived that the eyes follow you about when you move. BIG BROTHER IS WATCHING YOU, the caption beneath it ran. Inside the flat a fruity voice was reading out a list of figures which had something to do with the production of pig-iron. The voice came from an oblong metal plaque like a dulled mirror which formed part of the surface of the right-hand wall. Winston turned a switch and the voice sank somewhat, though the words were still distinguishable. The instrument (the telescreen, it was called) could be dimmed, but there was no way of shutting it off completely. He moved over to the window: a smallish, frail figure, the meagreness of his body merely emphasized by the blue overalls which were the uniform of the Party. Outside, the world was still flat. He thought of the Ministry of Truth, with its millions of rooms, its endless corridors, its enormous staff, its race of lunatics not subject to orders from any human authority, but moving only at the bidding of the telescreens. He thought of the Ministry of Love, which was the real centre of power, the place of no windows, the place where there was no law. He thought of the Ministry of Plenty, with its pyramids of canned goods, its concrete piles, its mountains of scrap metal. He thought of the Ministry of Peace, which was concerned with war. And he thought of the face of Big Brother, which never changed, and which looked down on everything he did. He turned his eyes to the telescreen. The voice had continued, but now it changed its tone, becoming more urgent. It was giving instructions to the citizens of Oceania on how to behave during Hate Week. Winston listened with a mixture of fear and fascination. He had heard it all before, but it still had the power to disturb him. He was not particularly brave, but he was not a coward either. He was simply a man who had lived through too much to be surprised by anything any more. He had been born in the early years of the Revolution, and he had seen the Party grow from a small underground organization into the colossus that now bestrode the earth. He had seen the great purges, the forced marches, the famines, the wars. He had seen the Party change its mind about everything a dozen times. He had seen the comradeship of the early days turn into the icy discipline of the present. He had seen the Party’s enemies—the Trotskyists, the anarchists, the saboteurs—disappear one by one into the vortex of the Ministry of Love. He had seen the Party’s allies—the capitalists, the imperialists, the feudalists—become its enemies overnight. He had seen the Party’s slogans change from ‘War is Peace’ to ‘Peace is War’, from ‘Freedom is Slavery’ to ‘Slavery is Freedom’, from ‘Ignorance is Strength’ to ‘Strength is Ignorance’. He had seen the Party’s leaders—the great heroes of the Revolution—fall from grace and be executed as traitors. He had seen the Party’s history rewritten so many times that he no longer knew what was true and what was false."""

# Configuración
master_key = random.randbytes(32)
iv = random.randbytes(16)

print("=" * 70)
print("🔐 INTEGRACIÓN FASE 0 + FASE 1 – TEXTO COMPLETO DE 1984")
print("=" * 70)

print(f"\n📝 Texto original (primeros 200 caracteres):")
print(texto_1984_completo[:200] + "...")
print(f"\n📊 Longitud total: {len(texto_1984_completo)} caracteres")
print(f"📊 Palabras aproximadas: {len(texto_1984_completo.split())}")

# 1. Fase 0
print("\n🔷 FASE 0: Generando grid 100x100...")
start = time.time()
phase0 = Phase0Preprocessing()
grid_inicial, seed = phase0.process(texto_1984_completo)
tiempo_f0 = time.time() - start
print(f"   ✅ Grid creado en {tiempo_f0:.2f} segundos")
print(f"   Seed: {seed.hex()[:16]}...")

print("\n📌 PRIMERAS 5 FILAS DEL GRID INICIAL (primeros 60 caracteres):")
for i in range(5):
    fila = ''.join(grid_inicial[i][:60])
    print(f"Row {i:2d}: {fila}...")

# 2. Fase 1
print("\n🔶 FASE 1: Aplicando rotaciones multiescala...")
rotaciones = Phase1Rotations(master_key, iv)
start = time.time()
grid_rotado = rotaciones.apply(grid_inicial)
tiempo_f1 = time.time() - start
print(f"   ✅ Rotaciones aplicadas en {tiempo_f1:.2f} segundos")

print("\n📌 PRIMERAS 5 FILAS DEL GRID ROTADO (primeros 60 caracteres):")
for i in range(5):
    fila = ''.join(grid_rotado[i][:60])
    print(f"Row {i:2d}: {fila}...")

# 3. Guardar grid rotado completo en archivo
output_file = "output_1984_rotado.txt"
with open(output_file, 'w') as f:
    f.write("=" * 70 + "\n")
    f.write("GRID COMPLETO DESPUÉS DE ROTACIONES (100×100)\n")
    f.write("Texto original: 1984 – George Orwell (completo)\n")
    f.write("=" * 70 + "\n\n")
    for i in range(100):
        f.write(f"Row {i:3d}: {''.join(grid_rotado[i])}\n")
    f.write(f"\nSeed usada: {seed.hex()}\n")
    f.write(f"Master key (primeros 16 bytes): {master_key.hex()[:16]}...\n")

print(f"\n📁 Archivo guardado: {output_file}")
print("   Abrirlo con: code output_1984_rotado.txt")

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