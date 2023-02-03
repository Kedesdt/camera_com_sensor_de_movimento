import sys
from cx_Freeze import setup, Executable

build_exe_options = {'packages': ['numpy'], "include_files": ['gravador.py', "constantes.py", 'config.json']}

exe = Executable(script='run.py', base=None)

setup(name='Gravador',
      version='1.0',
      executables=[exe],
      options={'build_exe': build_exe_options})