# -*- mode: python ; coding: utf-8 -*-

import platform
import sys

block_cipher = None

# Detect platform and architecture (macOS is building for Raspberry Pi via Docker)
is_darwin = platform.system() == 'Darwin'
target_platform = 'linux' if is_darwin else sys.platform
target_arch = 'arm' if is_darwin else None

a = Analysis(
    ['rtlsdr_tool/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'numpy',
        'pyrtlsdr',
        'rtlsdr_tool',
        'rtlsdr_tool.cli',
        'rtlsdr_tool.sdr_reader',
        'rtlsdr_tool.output_writer',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='rtlsdr-tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_platform=target_platform,  # Note: actual cross-compilation happens in Docker
    target_arch=target_arch,
    codesign_identity=None,
    entitlements_file=None,
) 