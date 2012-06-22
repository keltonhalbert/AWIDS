from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
import os

cpath = os.path.join( os.path.dirname(__file__), 'awids/barnesinterp.pyx' )

setup(
      name = "AWIDS",
      version = "1.2.0",
      author = "Kelton Halbert",
      author_email = "keltonhalbert@tempestchasing.com",
      description = ("A surface weather data plotting package built on MATPLOTLIB, NUMPY, and SCIPY"),
      license = "Creative Commons",
      keywords = "Python Weather Packages",
      url = "https://github.com/keltonhalbert/AWIDS",
      packages=['awids'],
      package_data = {'awids':['*.npz', '*.pyx', '*.so', '*.c']},
      classifiers=["Development Status :: 2 - Pre-Alpha"], 
      cmdclass = {'build_ext': build_ext},
      ext_modules = [Extension("barnesinterp", [cpath], include_dirs=[numpy.get_include()])]
      )