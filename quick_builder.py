import os

from cx_Freeze import setup, Executable

foldr = 'quick_build'
for filename in os.listdir(foldr):
    print filename
    build_exe_options = {"packages": ["os"], "excludes": ["tkinter"],
                             "build_exe": "c:\\test\\" + filename[:-2], "silent": True}

    out = setup(name="ESET", version="0.1", description="ESET testing tool",
              options={"build_exe": build_exe_options},
              executables=[Executable(foldr + '/' +filename)])
              # executables=[Executable("ruletule.py")])

