import sys
sys.path.append('src')
from phase3_visual import Phase3Visual

# Leer archivo de colores (Fase 3)
with open('output_1984_phase3b_colors.txt', 'r') as f:
    lines = f.readlines()

grid_colors = []
for line in lines:
    if line.startswith('Row'):
        parts = line.split(':')
        if len(parts) > 1:
            grid_colors.append(parts[1].strip().split())

print(f"Grid colores: {len(grid_colors)}x{len(grid_colors[0]) if grid_colors else 0}")

# Generar HTML de colores con modo colors
visual = Phase3Visual(seed=b'1984', mode='colors')
with open('docs/sample_output_phase3_colors_1984.html', 'w', encoding='utf-8') as f:
    f.write(visual.to_html(grid_colors))

print("✅ docs/sample_output_phase3_colors_1984.html generado")

# Leer archivo de caracteres exóticos (Fase 4)
with open('output_1984_phase4_exotic.txt', 'r') as f:
    lines = f.readlines()

grid_exotic = []
for line in lines:
    if line.startswith('Row'):
        parts = line.split(':')
        if len(parts) > 1:
            grid_exotic.append(parts[1].strip().split())

print(f"Grid exóticos: {len(grid_exotic)}x{len(grid_exotic[0]) if grid_exotic else 0}")

# Generar HTML de caracteres con modo chars
visual2 = Phase3Visual(seed=b'1984', mode='chars')
with open('docs/sample_output_phase4_exotic_1984.html', 'w', encoding='utf-8') as f:
    f.write(visual2.to_html(grid_exotic))

print("✅ docs/sample_output_phase4_exotic_1984.html generado")