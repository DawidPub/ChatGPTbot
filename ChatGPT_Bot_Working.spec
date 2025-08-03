# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_all

datas = [('chatgpt_gui.py', '.'), ('chatgpt_bot_core.py', '.')]
binaries = []
hiddenimports = ['chatgpt_gui', 'chatgpt_bot_core', 'selenium', 'selenium.webdriver', 'selenium.webdriver.chrome', 'selenium.webdriver.chrome.service', 'selenium.webdriver.chrome.options', 'selenium.webdriver.common', 'selenium.webdriver.common.by', 'selenium.webdriver.common.keys', 'selenium.webdriver.common.action_chains', 'selenium.webdriver.support', 'selenium.webdriver.support.ui', 'selenium.webdriver.support.wait', 'selenium.webdriver.support.expected_conditions', 'selenium.common.exceptions', 'webdriver_manager', 'webdriver_manager.chrome', 'json', 'time', 'threading']
hiddenimports += collect_submodules('tkinter')
hiddenimports += collect_submodules('selenium')
hiddenimports += collect_submodules('webdriver_manager')
tmp_ret = collect_all('selenium')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('webdriver_manager')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='ChatGPT_Bot_Working',
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
    name='ChatGPT_Bot_Working',
)
