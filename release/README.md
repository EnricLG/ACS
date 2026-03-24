# Layered Cipher System - Interactive Application

This is a standalone executable version of the multi-layer encryption system. It allows you to encrypt any text and see the result after each phase.

## 🚀 Quick Start

### Linux
1. Download the `linux` folder
2. Open a terminal in that folder
3. Run: `./interactive_encrypt`
   (or double-click `run.sh`)

### Windows / macOS
- Currently only Linux builds are provided.
- For Windows/macOS, you can run the Python script directly from the main repository.

## 📖 How to Use

1. **Enter your text** – paste or type the message you want to encrypt. Press `Ctrl+D` (Linux) or `Ctrl+Z` (Windows) on a new line when finished.
2. **Choose the phase** – select which encryption layer you want to see:
   - `0` – Preprocessing (word padding + filler words)
   - `1` – Hierarchical rotations
   - `2` – Dictionary cipher
   - `3` – Concentric square rotations
   - `3b` – Pairwise transform (numbers → colors)
   - `4` – Final substitution (numbers → exotic characters)
3. **Wait** – the program will process your text and open the result in your browser (for phases 3b and 4) or save a text file (for phases 0–3).

## 📁 Output Files

All results are saved in a timestamped folder inside `interactive_output/`:
- Phase 0–3: text grids (`.txt`)
- Phase 3b: `phase3b_colors.html` (visual grid of colors)
- Phase 4: `phase4_exotic.html` (visual grid of exotic characters)

## 🔐 Security Notes

- Each run uses a **random key** (unique per session).
- The executable is self-contained (no Python installation needed).
- For educational purposes only. Not audited for production use.

## 🛠️ Requirements

- Linux x86_64 (Ubuntu 20.04+ recommended)
- A web browser (for HTML output)

## 📦 Included Files

linux/
├── interactive_encrypt # Main executable
├── data/ # Required character lists
│ └── exotic_chars.txt # 10,000 exotic Unicode characters
└── run.sh # Convenience launcher


## 🧪 Testing

Tested on Ubuntu 22.04 and 24.04.

## 📄 License

MIT – see main repository for details.

## 🔗 Main Repository

[https://github.com/EnricLG/ACS](https://github.com/EnricLG/ACS)
EOF