# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['script_linker_test.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('./basic_functions.py', './basic_functions.py'),
        ('./graph.py', './graph.py'),
        ('./main.py', './main.py'),
        ('./optimization.py', './optimization.py'),
        ('./outline.py', './outline.py'),
        ('./path.py', './path.py'),
        ('./segment.py', './segment.py'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='script_linker_test',
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
