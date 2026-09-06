# -*- mode: python ; coding: utf-8 -*-
import os
import sys
spec_dir = os.path.dirname(os.path.abspath(SPEC))
src_dir  = os.path.join(spec_dir, "src")
app_dir  = os.path.join(src_dir, "app")
asset_dir = os.path.join(src_dir, "assets")
ui_dir   = os.path.join(src_dir, "ui")
target   = os.path.join(app_dir, "game_of_life.py")
icon      = os.path.join(asset_dir, "CGOL_game.ico")

a = Analysis(
    [target],
    pathex=[spec_dir, src_dir, app_dir, asset_dir, ui_dir],
    binaries=[],
    datas=[],
    hiddenimports=['static_init'],
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
    name='Game of Life',
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
	icon=[icon]
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Game of Life',
)
