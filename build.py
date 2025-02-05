import PyInstaller.__main__
import os

# 确保在脚本所在目录运行
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PyInstaller.__main__.run([
    'main.py',
    '--name=行尾转换工具',
    '--onefile',
    '--icon=NONE',
    '--clean',
]) 