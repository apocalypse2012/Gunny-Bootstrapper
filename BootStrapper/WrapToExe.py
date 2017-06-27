from distutils.core import setup
import sys, os, py2exe

name = sys.argv[1]
sys.argv[1] = 'py2exe'
sys.path.append(os.path.dirname(os.path.abspath(name)))

setup(name=name[:-3],
      console=[name],
      options={
          'py2exe': {
              'bundle_files': 1,
              'compressed': True,
              'excludes':['_ssl', 'doctest', 'unittest', 'difflib', '_hashlib', '_tkinter', '_socket', 'unicodedata'],
              'includes':['importlib', 'json', 'shutil', 'filecmp', 'cmd'],
              'packages': [],
              'dist_dir': os.path.dirname(os.path.realpath(name))
          }
      },
      zipfile=None,
      )
