from setuptools import setup

setup(name='swgeo',
      version='0.1',
      description='Tools for geospatial analysis',
      url='https://github.com/yl238/swgeo',
      author='Sue Liu',
      license='GNU',
      packages=['swgeo'],
      install_requires=[
          'numpy',
          'folium',
          'matplotlib'
      ])