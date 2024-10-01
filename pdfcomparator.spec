# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# Obtém o diretório atual do script
current_dir = os.path.dirname(os.path.abspath(__file__))

a = Analysis(['main.py'],
             pathex=[current_dir],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='PDFComparator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon=os.path.join(current_dir, 'path_to_your_icon.ico')) 
