"""
Visualización animada de la Fase 1 con colores distintos por fila.
Genera un GIF que muestra cada nivel de rotación.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio
import tempfile
import os

# ============================================
# 1. Configuración
# ============================================
SIZE = 16  # Tamaño de la cuadrícula (múltiplo de los tamaños de bloque)
LEVELS = [16, 8, 4, 2]  # Niveles de rotación (demostración jerárquica)

# Colores base para cada fila (16 colores distintos)
BASE_COLORS = [
    (1.0, 0.0, 0.0),  # rojo
    (0.0, 1.0, 0.0),  # verde
    (0.0, 0.0, 1.0),  # azul
    (1.0, 1.0, 0.0),  # amarillo
    (1.0, 0.0, 1.0),  # magenta
    (0.0, 1.0, 1.0),  # cyan
    (1.0, 0.5, 0.0),  # naranja
    (0.5, 0.0, 1.0),  # violeta
    (0.5, 1.0, 0.0),  # verde lima
    (1.0, 0.5, 0.5),  # rosa claro
    (0.5, 0.5, 1.0),  # azul claro
    (1.0, 0.5, 1.0),  # fucsia
    (0.5, 1.0, 0.5),  # verde menta
    (0.8, 0.4, 0.2),  # terracota
    (0.2, 0.8, 0.4),  # verde bosque
    (0.4, 0.2, 0.8)   # púrpura
]

# Asegurar que tenemos al menos SIZE colores (si no, repetimos)
if len(BASE_COLORS) < SIZE:
    BASE_COLORS = (BASE_COLORS * (SIZE // len(BASE_COLORS) + 1))[:SIZE]

# ============================================
# 2. Generar una cuadrícula de prueba (valores 0-99)
# ============================================
grid_numeric = np.zeros((SIZE, SIZE), dtype=int)
for i in range(SIZE):
    for j in range(SIZE):
        grid_numeric[i, j] = (i * SIZE + j) % 100

def colorize_grid(grid):
    """Convierte una cuadrícula numérica en una imagen RGB con color base por fila."""
    h, w = grid.shape
    img = np.zeros((h, w, 3))
    for i in range(h):
        base_color = BASE_COLORS[i]
        for j in range(w):
            # Intensidad: valor de 0 a 99 -> 0.2 a 1.0 (más brillante cuanto mayor)
            intensity = 0.2 + 0.8 * (grid[i, j] / 99.0)
            img[i, j] = [c * intensity for c in base_color]
    return img

# ============================================
# 3. Funciones de rotación
# ============================================
def rotate_block(block):
    """Rota un bloque 90° a la derecha (devuelve un nuevo array numérico)"""
    return np.rot90(block, k=-1)

def rotate_block_image(block_img):
    """Rota un bloque de imagen (RGB) 90° a la derecha"""
    return np.rot90(block_img, k=-1)

# ============================================
# 4. Aplicar rotaciones jerárquicas y guardar frames
# ============================================
def draw_frame(grid_numeric, level_idx, size, output_path):
    """Dibuja el frame con bloques destacados."""
    # Convertir a imagen RGB
    img = colorize_grid(grid_numeric)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img, interpolation='none')
    ax.set_title(f"Nivel {level_idx+1}: Bloques de {size}x{size}", fontsize=14)
    
    # Dibujar líneas de división de bloques
    blocks_per_side = SIZE // size
    for i in range(blocks_per_side + 1):
        ax.axhline(i*size - 0.5, color='white', linewidth=2)
        ax.axvline(i*size - 0.5, color='white', linewidth=2)
    
    # Añadir recuadro amarillo alrededor de cada bloque (opcional)
    for i in range(blocks_per_side):
        for j in range(blocks_per_side):
            rect = patches.Rectangle((j*size - 0.5, i*size - 0.5), size, size,
                                     linewidth=1, edgecolor='yellow', facecolor='none')
            ax.add_patch(rect)
    
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    plt.savefig(output_path, dpi=100)
    plt.close()

def create_animation():
    print("Generando frames...")
    frames_numeric = []  # Lista de grids numéricos en cada paso
    
    # Grid original
    current = grid_numeric.copy()
    frames_numeric.append(current)
    
    # Aplicar rotaciones nivel por nivel
    for idx, size in enumerate(LEVELS):
        blocks_per_side = SIZE // size
        next_grid = current.copy()
        for i in range(blocks_per_side):
            for j in range(blocks_per_side):
                # Rotamos los bloques con índice par (para mostrar variedad)
                if (i + j) % 2 == 0:
                    block = current[i*size:(i+1)*size, j*size:(j+1)*size]
                    rotated = rotate_block(block)
                    next_grid[i*size:(i+1)*size, j*size:(j+1)*size] = rotated
        frames_numeric.append(next_grid)
        current = next_grid
    
    # Guardar cada frame como imagen
    temp_dir = tempfile.mkdtemp()
    frame_files = []
    for idx, grid in enumerate(frames_numeric):
        # Para el nivel, usamos el tamaño correspondiente (el último es 1x1, pero lo mostramos como bloque de 2x2)
        size = LEVELS[idx] if idx < len(LEVELS) else 1
        file_path = os.path.join(temp_dir, f"frame_{idx:03d}.png")
        draw_frame(grid, idx, size, file_path)
        frame_files.append(file_path)
    
    # Crear GIF con duración de 3 segundos por frame
    print("Creando GIF...")
    images = [imageio.imread(f) for f in frame_files]
    imageio.mimsave('phase1_animation_colors.gif', images, duration=3000, loop=0)
    
    print("✅ Animación guardada como phase1_animation_colors.gif")
    # Limpiar archivos temporales
    for f in frame_files:
        os.remove(f)
    os.rmdir(temp_dir)

if __name__ == "__main__":
    create_animation()