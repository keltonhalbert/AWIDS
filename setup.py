from setuptools import setup

setup(
      name = "AWIDS",
      version = "1.0.0",
      author = "Kelton Halbert",
      author_email = "keltonhalbert@tempestchasing.com",
      description = ("A surface weather data plotting package built on MATPLOTLIB, NUMPY, and SCIPY"),
      license = "Creative Commons",
      keywords = "Python Weather Packages",
      url = "https://github.com/keltonhalbert/AWIDS",
      packages=['awids'],
      package_data = {'awids':['*.npz']},
      classifiers=["Development Status :: 2 - Pre-Alpha"],
      )