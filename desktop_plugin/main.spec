# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis([
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/main.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/Tray/Tray.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/desktop_round_plugin/desktop_round_plugin_ui.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/desktop_round_plugin/desktop_round_plugin_controller.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/BaseUI/BaseUI.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/desktop_plugin/desktop_plugin_ui.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/desktop_plugin/desktop_plugin_controller.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/Control/QRoundProgressBar/Position_Enum.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/Control/QRoundProgressBar/QRoundProgressBar.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/Control/QRoundProgressBar/BarStyle_Enum.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/Control/QRoundProgressBar/UpdateFlags_Enum.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/password_enter/password_enter_dialog_controller.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/password_enter/password_enter_dialog.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/UI/password_enter/password_enter_dialog.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/Service/Memory/Memory.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/Service/CPU/CPU.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/Service/OSVersion/OSVersion.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/Service/lunar/lunar.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/Service/weather/weather_requests.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/Thread/weatherThread.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/Thread/HardwareInfo_Thread.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/Tool/logHelper.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/Tool/ImagePlus.py',
'/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/Tool/PathHelper.py'
],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
app = BUNDLE(exe,
             name='desktop_plugin.app',
             icon='/Users/naoki/dev/Python/desktop_plugin/desktop_plugin/Resource/MacMemoryToolIcon.icns',
             bundle_identifier=None)
