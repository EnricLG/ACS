"""
Genera una lista de 10,000 caracteres de diversas escrituras (griego, cirílico, hebreo, árabe, tailandés, chino, etc.)
"""

import os

# Directorio de salida
os.makedirs("data", exist_ok=True)

# Definición de rangos (inicio, fin, descripción)
ranges = [
    # Griego
    (0x0370, 0x03FF, "Greek"),
    # Cirílico
    (0x0400, 0x04FF, "Cyrillic"),
    # Hebreo
    (0x0590, 0x05FF, "Hebrew"),
    # Árabe
    (0x0600, 0x06FF, "Arabic"),
    # Devanagari (hindi)
    (0x0900, 0x097F, "Devanagari"),
    # Bengalí
    (0x0980, 0x09FF, "Bengali"),
    # Gurmukhi
    (0x0A00, 0x0A7F, "Gurmukhi"),
    # Gujarati
    (0x0A80, 0x0AFF, "Gujarati"),
    # Oriya
    (0x0B00, 0x0B7F, "Oriya"),
    # Tamil
    (0x0B80, 0x0BFF, "Tamil"),
    # Telugu
    (0x0C00, 0x0C7F, "Telugu"),
    # Kannada
    (0x0C80, 0x0CFF, "Kannada"),
    # Malayalam
    (0x0D00, 0x0D7F, "Malayalam"),
    # Sinhala
    (0x0D80, 0x0DFF, "Sinhala"),
    # Tailandés
    (0x0E00, 0x0E7F, "Thai"),
    # Lao
    (0x0E80, 0x0EFF, "Lao"),
    # Tibetano
    (0x0F00, 0x0FFF, "Tibetan"),
    # Birmano
    (0x1000, 0x109F, "Burmese"),
    # Georgiano
    (0x10A0, 0x10FF, "Georgian"),
    # Etíope
    (0x1200, 0x137F, "Ethiopic"),
    # Cherokee
    (0x13A0, 0x13FF, "Cherokee"),
    # Hiragana
    (0x3040, 0x309F, "Hiragana"),
    # Katakana
    (0x30A0, 0x30FF, "Katakana"),
    # Hangul (coreano) – cogemos los primeros 3000
    (0xAC00, 0xAC00 + 3000, "Hangul"),
    # CJK (chino/japonés/coreano) – cogemos los primeros 2500
    (0x4E00, 0x4E00 + 2500, "CJK"),
    # Tai Viet
    (0xAA80, 0xAADF, "Tai Viet"),
]

chars = []
for start, end, name in ranges:
    for cp in range(start, end):
        try:
            ch = chr(cp)
            chars.append(ch)
        except (ValueError, OverflowError):
            continue

print(f"Total characters collected: {len(chars)}")

# Tomar exactamente 10,000
if len(chars) > 10000:
    chars = chars[:10000]
elif len(chars) < 10000:
    # Si no llegamos, repetir caracteres de forma cíclica
    print("WARNING: Not enough chars, repeating...")
    chars = (chars * (10000 // len(chars) + 1))[:10000]

# Guardar en archivo
output_path = "data/exotic_chars.txt"
with open(output_path, "w", encoding="utf-8") as f:
    for ch in chars:
        f.write(ch + "\n")

print(f"Saved {len(chars)} characters to {output_path}")