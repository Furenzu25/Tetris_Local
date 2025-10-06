# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('game_logic', 'game_logic'), ('rendering', 'rendering'), ('networking', 'networking')],
    hiddenimports=['pygame', 'game_logic', 'rendering', 'networking', 'game_logic.pieces', 'game_logic.board', 'game_logic.game_engine', 'rendering.renderer', 'networking.protocol', 'networking.server', 'networking.client'],
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
    [],
    exclude_binaries=True,
    name='Tetris_Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Tetris_Launcher',
)
app = BUNDLE(
    coll,
    name='Tetris_Launcher.app',
    icon=None,
    bundle_identifier=None,
)
