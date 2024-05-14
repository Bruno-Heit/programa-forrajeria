# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/Bruno/Desktop/PROGRAMACION/Proyectos/forrajeria-programa/main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/Bruno/Desktop/PROGRAMACION/Proyectos/forrajeria-programa/database', 'database/'), ('C:/Users/Bruno/Desktop/PROGRAMACION/Proyectos/forrajeria-programa/images', 'images/'), ('C:/Users/Bruno/Desktop/PROGRAMACION/Proyectos/forrajeria-programa/icons', 'icons/'), ('C:/Users/Bruno/Desktop/PROGRAMACION/Proyectos/forrajeria-programa/ui', 'ui/'), ('C:/Users/Bruno/Desktop/PROGRAMACION/Proyectos/forrajeria-programa/utils', 'utils/')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='gestion-forraje',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\Bruno\\Desktop\\PROGRAMACION\\Proyectos\\forrajeria-programa\\icons\\program_icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='gestion-forraje',
)
