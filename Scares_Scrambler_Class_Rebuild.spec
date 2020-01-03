# -*- mode: python -*-

block_cipher = None


a = Analysis(['Scares_Scrambler_Class_Rebuild.py'],
             pathex=['C:\\Users\\Cocoa\\Desktop\\Scares_Scrambler\\Build 16'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Scares_Scrambler_Class_Rebuild',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='Assets\\favi64.ico')
