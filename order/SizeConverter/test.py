# mysetup.py
from distutils.core import setup

import py2exe

setup(console=[r"E:\workspace\SizeConverter\main.py",],
         data_files=[("data",
                   [r"E:\workspace\SizeConverter\data\coat.txt", 
                    r"E:\workspace\SizeConverter\data\trou.txt"]),],
      )