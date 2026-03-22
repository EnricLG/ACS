import sys
sys.path.append('src')
from phase3_visual import Phase3Visual

# Leer el archivo visual generado
with open('output_1984_phase3_visual.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extraer solo las filas de datos (las que comienzan con 'Row')
grid_visual = []
for line in lines:
    if line.startswith('Row'):
        parts = line.split(':')
        if len(parts) > 1:
            row_data = parts[1].strip().split()
            grid_visual.append(row_data)

print(f'Grid size: {len(grid_visual)}x{len(grid_visual[0]) if grid_visual else 0}')

# Crear visualizador y generar HTML
visual = Phase3Visual(seed=b'1984')
with open('output_1984_phase3_visual.html', 'w', encoding='utf-8') as f:
    f.write(visual.to_html(grid_visual))

print('✅ output_1984_phase3_visual.html generado')