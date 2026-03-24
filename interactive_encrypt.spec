# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['interactive_encrypt.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data'), ('src', 'src')],
    hiddenimports=[
        'phase0_preprocessing',
        'phase1_rotations',
        'phase2_dict_cipher',
        'phase3_concentric_rotations',
        'phase3_pairwise',
        'phase4_final_substitution',
        'phase3_visual',
        'alphabet',
        'numpy',
        'random',
        'hashlib',
        'hmac',
        'os',
        'sys',
        'time',
        'pathlib',
        'webbrowser',
        'datetime'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='interactive_encrypt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
