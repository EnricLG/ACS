import os

os.makedirs("data", exist_ok=True)

# Generar 10,000 caracteres chinos desde el bloque CJK
start = 0x4E00
count = 10000

chars = [chr(start + i) for i in range(count)]

with open("data/chinese_chars.txt", "w", encoding="utf-8") as f:
    for ch in chars:
        f.write(ch + "\n")

print(f"✅ Generados {len(chars)} caracteres chinos en data/chinese_chars.txt")