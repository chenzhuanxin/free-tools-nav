# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 打包配置：M3U8 影视资源搜索下载器
# 用法（在 m3u8-downloader 目录下）：
#   set WORKPATH=D:\pysbuild
#   C:\Python314\python.exe -m PyInstaller --workpath "%WORKPATH%\build" --distpath "%WORKPATH%\dist" m3u8tool.spec

import os

block_cipher = None

a = Analysis(
    ["m3u8tool.py"],
    pathex=[os.path.abspath(".")],
    binaries=[],
    datas=[
        ("web/index.html", "web"),        # 前端页面
        ("sources.json", "."),             # 资源站配置
    ],
    hiddenimports=[
        "Crypto",                          # pycryptodome
        "Crypto.Cipher",
        "Crypto.Cipher.AES",
        "Crypto.Util",
        "Crypto.Util.Padding",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        "tkinter", "matplotlib", "numpy", "pandas", "PIL",
        "PyQt5", "PyQt6", "PySide2", "PySide6",
        "scipy", "sqlite3", "test", "unittest", "xmlrpc",
    ],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="M3U8下载器",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,       # 单文件模式，解压到临时目录
    console=False,             # --noconsole
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
