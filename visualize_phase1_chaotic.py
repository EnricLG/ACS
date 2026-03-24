"""
Visualización animada de la Fase 1 con rotaciones aleatorias y caóticas.
Muestra el efecto jerárquico de rotaciones sobre una cuadrícula de 32x32.
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
SIZE = 32                     # Tamaño de la cuadrícula (múltiplo de los tamaños de bloque)
LEVELS = [32, 16, 8, 4, 2]   # Niveles de rotación (de mayor a menor)
# Para cada bloque en cada nivel, elegiremos un ángulo aleatorio 0-3 (0°,90°,180°,270°)

# Colores base para cada fila (32 colores distintos)
BASE_COLORS = []
# Generamos colores brillantes variando el tono en el círculo cromático
for i in range(SIZE):
    hue = i / SIZE                     # 0 a 1
    # Convertir HSV a RGB (usamos saturación=1, valor=1)
    # Fórmula simplificada para colores vivos
    r = (1 + np.cos(2 * np.pi * (hue - 0.0))) / 2
    g = (1 + np.cos(2 * np.pi * (hue - 1/3))) / 2
    b = (1 + np.cos(2 * np.pi * (hue - 2/3))) / 2
    BASE_COLORS.append((r, g, b))

# ============================================
# 2. Generar cuadrícula de prueba (valores 0-99)
# ============================================
grid_numeric = np.zeros((SIZE, SIZE), dtype=int)
for i in range(SIZE):
    for j in range(SIZE):
        # Crear un patrón con gradiente horizontal para que se vea el efecto de rotación
        grid_numeric[i, j] = (j % 100)  # Patrón de columnas
        # También podemos añadir variación vertical para más contraste
        # grid_numeric[i, j] = (i * SIZE + j) % 100

def colorize_grid(grid):
    """Convierte la cuadrícula numérica en imagen RGB con color base por fila."""
    h, w = grid.shape
    img = np.zeros((h, w, 3))
    for i in range(h):
        base_color = BASE_COLORS[i]
        for j in range(w):
            # Intensidad: 0.3 + 0.7 * (valor/99) para variar brillo
            intensity = 0.3 + 0.7 * (grid[i, j] / 99.0)
            img[i, j] = [c * intensity for c in base_color]
    return img

# ============================================
# 3. Función para rotar un bloque (numérico)
# ============================================
def rotate_block(block, k):
    """
    Rota un bloque numérico.
    k = 0: 0°
    k = 1: 90° derecha
    k = 2: 180°
    k = 3: 270° derecha (90° izquierda)
    """
    return np.rot90(block, k=-k)  # k=1 -> rot90(k=-1) es 90° derecha

# ============================================
# 4. Aplicar rotaciones jerárquicas con ángulos aleatorios
# ============================================
def apply_random_rotations(grid, levels):
    """
    Aplica rotaciones aleatorias a cada bloque en cada nivel.
    Devuelve una lista de grids (uno por nivel + original).
    """
    frames = [grid.copy()]
    current = grid.copy()
    
    # Fijamos semilla para que la animación sea reproducible
    rng = random.Random(42)
    
    for level_idx, size in enumerate(levels):
        blocks_per_side = SIZE // size
        next_grid = current.copy()
        # Para cada bloque, elegir un ángulo aleatorio
        rotations = {}
        for i in range(blocks_per_side):
            for j in range(blocks_per_side):
                # Cada bloque puede rotar 0,1,2,3 veces
                k = rng.randint(0, 3)
                rotations[(i, j)] = k
                if k > 0:
                    block = current[i*size:(i+1)*size, j*size:(j+1)*size]
                    rotated = rotate_block(block, k)
                    next_grid[i*size:(i+1)*size, j*size:(j+1)*size] = rotated
        frames.append(next_grid)
        current = next_grid
    return frames

# ============================================
# 5. Dibujar un frame con los contornos de bloques
# ============================================
def draw_frame(grid_numeric, level_idx, size, output_path):
    """Dibuja el frame con bloques destacados."""
    img = colorize_grid(grid_numeric)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img, interpolation='none')
    ax.set_title(f"Nivel {level_idx+1}: Bloques de {size}x{size}", fontsize=16)
    
    # Dibujar líneas de división de bloques
    blocks_per_side = SIZE // size
    for i in range(blocks_per_side + 1):
        ax.axhline(i*size - 0.5, color='white', linewidth=1.5)
        ax.axvline(i*size - 0.5, color='white', linewidth=1.5)
    
    # Opcional: recuadro amarillo en cada bloque
    for i in range(blocks_per_side):
        for j in range(blocks_per_side):
            rect = patches.Rectangle((j*size - 0.5, i*size - 0.5), size, size,
                                     linewidth=1, edgecolor='yellow', facecolor='none')
            ax.add_patch(rect)
    
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    plt.savefig(output_path, dpi=120)
    plt.close()

# ============================================
# 6. Crear animación
# ============================================
def create_animation():
    print("Generando frames con rotaciones aleatorias...")
    frames_numeric = apply_random_rotations(grid_numeric, LEVELS)
    print(f"Número de frames: {len(frames_numeric)}")
    
    # Guardar cada frame como imagen
    temp_dir = tempfile.mkdtemp()
    frame_files = []
    for idx, grid in enumerate(frames_numeric):
        size = LEVELS[idx] if idx < len(LEVELS) else 1
        file_path = os.path.join(temp_dir, f"frame_{idx:03d}.png")
        draw_frame(grid, idx, size, file_path)
        frame_files.append(file_path)
    
    # Crear GIF con duración de 2.5 segundos para el original, 2 segundos para cada paso
    print("Creando GIF...")
    images = [imageio.imread(f) for f in frame_files]
    # Duraciones: primera imagen (original) 3s, las demás 2s
    durations = [3000] + [2000] * (len(images)-1)
    imageio.mimsave('phase1_chaotic.gif', images, duration=durations, loop=0)
    
    print("✅ Animación guardada como phase1_chaotic.gif")
    # Limpiar archivos temporales
    for f in frame_files:
        os.remove(f)
    os.rmdir(temp_dir)

if __name__ == "__main__":
    create_animation()