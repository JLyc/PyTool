import sys
from cx_Freeze import setup, Executable


build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "build_exe": "c:\\test2", "silent": True}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "ESET",
        version = "0.1",
        description = "ESET testing tool",
        options = {"build_exe": build_exe_options},
        executables = [Executable("C0606_bad_extensions173.py")])