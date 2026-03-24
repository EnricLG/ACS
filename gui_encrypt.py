import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import os
import random
import webbrowser
from pathlib import Path
import tempfile

# Asegurar que se puedan importar los módulos del proyecto
sys.path.append(os.path.dirname(__file__))

from phase0_preprocessing import Phase0Preprocessing
from phase1_rotations import Phase1Rotations
from phase2_dict_cipher import Phase2DictCipher
from phase3_concentric_rotations import Phase3ConcentricRotations
from phase3_pairwise import Phase3Pairwise
from phase4_final_substitution import Phase4FinalSubstitution
from phase3_visual import Phase3Visual
from alphabet import ALPHABET

MAX_TEXT_LEN = 10000   # Límite para la cuadrícula 100x100

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Layered Cipher System")
        self.root.geometry("800x600")

        # Texto de entrada
        tk.Label(root, text="Enter text to encrypt (max 10000 chars):").pack(pady=5)
        self.text_input = scrolledtext.ScrolledText(root, height=10)
        self.text_input.pack(fill="both", expand=True, padx=10, pady=5)

        # Selección de fase
        tk.Label(root, text="Select output phase:").pack(pady=5)
        self.phase_var = tk.StringVar(value="4")
        phases = [("0 - Preprocessing", "0"), ("1 - Hierarchical rotations", "1"),
                  ("2 - Dictionary cipher", "2"), ("3 - Concentric rotations", "3"),
                  ("3b - Pairwise (colors)", "3b"), ("4 - Final (exotic chars)", "4")]
        for text, val in phases:
            tk.Radiobutton(root, text=text, variable=self.phase_var, value=val).pack(anchor="w", padx=20)

        # Botón de cifrado
        tk.Button(root, text="Encrypt", command=self.encrypt, bg="lightblue").pack(pady=10)

        # Área de resultado (texto)
        tk.Label(root, text="Output:").pack(pady=5)
        self.text_output = scrolledtext.ScrolledText(root, height=15)
        self.text_output.pack(fill="both", expand=True, padx=10, pady=5)

    def truncate_text(self, text):
        if len(text) > MAX_TEXT_LEN:
            messagebox.showwarning("Text truncated",
                                   f"The text is too long ({len(text)} chars).\nIt will be truncated to {MAX_TEXT_LEN} characters.")
            return text[:MAX_TEXT_LEN]
        return text

    def encrypt(self):
        plaintext = self.text_input.get("1.0", tk.END).strip()
        if not plaintext:
            messagebox.showwarning("Empty text", "Please enter some text.")
            return

        # Truncar si es necesario
        plaintext = self.truncate_text(plaintext)

        phase = self.phase_var.get()
        master_key = random.randbytes(32)
        iv = random.randbytes(16)

        try:
            # Fase 0
            phase0 = Phase0Preprocessing()
            grid0, _ = phase0.process(plaintext)

            if phase == "0":
                self.show_text_grid(grid0)
                return

            # Fase 1
            rot = Phase1Rotations(master_key, iv)
            grid1 = rot.apply(grid0)
            if phase == "1":
                self.show_text_grid(grid1)
                return

            # Fase 2
            cipher2 = Phase2DictCipher(master_key, iv)
            grid2 = cipher2.encrypt(grid1)
            if phase == "2":
                self.show_text_grid(grid2)
                return

            # Fase 3
            phase3 = Phase3ConcentricRotations(master_key, iv)
            grid3 = phase3.transform(grid2)
            if phase == "3":
                self.show_text_grid(grid3)
                return

            # Fase 3b
            grid3_ints = [[ALPHABET.index(ch) for ch in row] for row in grid3]
            pairwise = Phase3Pairwise()
            grid3b = pairwise.transform(grid3_ints)
            if phase == "3b":
                visual = Phase3Visual(seed=b'1984', mode='colors')
                grid_colors = [[visual.to_visual(w) for w in row] for row in grid3b]
                html = visual.to_html(grid_colors)
                self.show_html(html)
                return

            # Fase 4
            cipher4 = Phase4FinalSubstitution(master_key, iv)
            grid4 = cipher4.encrypt(grid3b)
            if phase == "4":
                visual = Phase3Visual(seed=b'1984', mode='chars')
                grid_chars = [[visual.to_visual(w) for w in row] for row in grid4]
                html = visual.to_html(grid_chars)
                self.show_html(html)
                return

        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")

    def show_text_grid(self, grid):
        """Muestra las primeras filas del grid de caracteres."""
        lines = [f"Row {i}: {''.join(row[:80])}..." for i, row in enumerate(grid[:10])]
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert("1.0", "\n".join(lines))
        self.text_output.insert(tk.END, f"\n... (full grid: 100x100)")

    def show_html(self, html):
        """Guarda el HTML en un archivo temporal y lo abre en el navegador."""
        fd, path = tempfile.mkstemp(suffix=".html")
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(html)
        webbrowser.open(path)
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert("1.0", f"HTML generated and opened in browser.\nTemporary file: {path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()