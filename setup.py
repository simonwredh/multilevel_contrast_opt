
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'contrast_opt'
AUTHOR = 'Simon Wredh'
AUTHOR_EMAIL = 'simon_wredh@mymail.sutd.edu.sg'
URL = 'https://github.com/simon-wredh/contrast_opt'

LICENSE = 'MIT License'
DESCRIPTION = 'Contrast optimisation of multi-layer thin-film stack'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )