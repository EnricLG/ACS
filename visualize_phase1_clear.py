"""
Visualización clara de la Fase 1: rotaciones jerárquicas.
Muestra paso a paso cómo se rotan los bloques en cada nivel.
Usa números en lugar de colores para que se vea el movimiento.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio
import tempfile
import os
import random

# ============================================
# 1. Configuración
# ============================================
SIZE = 16                     # Tamaño de la cuadrícula (16x16)
LEVELS = [16, 8, 4, 2]        # Niveles de rotación

# Generar cuadrícula con números para que se vea claramente el movimiento
grid_numeric = np.zeros((SIZE, SIZE), dtype=int)
for i in range(SIZE):
    for j in range(SIZE):
        # Números de 0 a 99, pero para que se vea el patrón usamos coordenadas
        grid_numeric[i, j] = i * SIZE + j  # Cada celda tiene un número único

# ============================================
# 2. Función para rotar un bloque
# ============================================
def rotate_block(block, k):
    """
    Rota un bloque numérico.
    k = 0: 0°
    k = 1: 90° derecha
    k = 2: 180°
    k = 3: 270° derecha (90° izquierda)
    """
    return np.rot90(block, k=-k)  # rot90 con k=-1 rota 90° derecha

# ============================================
# 3. Aplicar rotaciones nivel por nivel (mostrando cada paso)
# ============================================
def apply_rotations_step_by_step(grid, levels):
    """
    Aplica rotaciones a cada nivel, mostrando un frame por nivel.
    En cada nivel, se rotan TODOS los bloques con un ángulo fijo (para que se vea).
    """
    frames = [grid.copy()]
    current = grid.copy()
    
    for level_idx, size in enumerate(levels):
        blocks_per_side = SIZE // size
        next_grid = current.copy()
        
        # Para este ejemplo, rotamos cada bloque 90° (k=1) para que se vea el efecto
        k = 1  # 90° derecha
        
        for i in range(blocks_per_side):
            for j in range(blocks_per_side):
                block = current[i*size:(i+1)*size, j*size:(j+1)*size]
                rotated = rotate_block(block, k)
                next_grid[i*size:(i+1)*size, j*size:(j+1)*size] = rotated
        
        frames.append(next_grid)
        current = next_grid
    
    return frames

# ============================================
# 4. Dibujar un frame con números y contornos
# ============================================
def draw_frame(grid, level_idx, size, output_path):
    """Dibuja la cuadrícula con números y recuadros de bloques."""
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Mostrar números en cada celda
    for i in range(SIZE):
        for j in range(SIZE):
            ax.text(j, i, str(grid[i, j]), ha='center', va='center', fontsize=8)
    
    # Establecer límites y quitar ejes
    ax.set_xlim(-0.5, SIZE-0.5)
    ax.set_ylim(SIZE-0.5, -0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Dibujar líneas de la cuadrícula
    for i in range(SIZE + 1):
        ax.axhline(i - 0.5, color='gray', linewidth=0.5)
        ax.axvline(i - 0.5, color='gray', linewidth=0.5)
    
    # Dibujar contornos de bloques del nivel actual
    if size > 1:
        blocks_per_side = SIZE // size
        for i in range(blocks_per_side + 1):
            ax.axhline(i*size - 0.5, color='red', linewidth=3)
            ax.axvline(i*size - 0.5, color='red', linewidth=3)
    
    ax.set_title(f"Nivel {level_idx+1}: Bloques de {size}x{size} (rotación 90°)", fontsize=14)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

# ============================================
# 5. Crear animación
# ============================================
def create_animation():
    print("Generando frames...")
    frames_numeric = apply_rotations_step_by_step(grid_numeric, LEVELS)
    print(f"Número de frames: {len(frames_numeric)}")
    
    # Guardar cada frame como imagen
    temp_dir = tempfile.mkdtemp()
    frame_files = []
    for idx, grid in enumerate(frames_numeric):
        size = LEVELS[idx] if idx < len(LEVELS) else 1
        file_path = os.path.join(temp_dir, f"frame_{idx:03d}.png")
        draw_frame(grid, idx, size, file_path)
        frame_files.append(file_path)
    
    # Crear GIF con duración de 3 segundos por frame
    print("Creando GIF...")
    images = [imageio.imread(f) for f in frame_files]
    imageio.mimsave('phase1_clear.gif', images, duration=3000, loop=0)
    
    print("✅ Animación guardada como phase1_clear.gif")
    # Limpiar archivos temporales
    for f in frame_files:
        os.remove(f)
    os.rmdir(temp_dir)

if __name__ == "__main__":
    create_animation()