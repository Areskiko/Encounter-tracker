# -*- mode: python -*-

from kivy_deps import sdl2, glew

block_cipher = None


a = Analysis(['frontend.py'],
             pathex='.',
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
         cipher=block_cipher)


exe = EXE(pyz, Tree('.','Data'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='app',
          debug=False,
          strip=False,
          upx=True,
          console=False, icon='icon.ico' )
