from setuptools import setup, find_packages

setup(name='nephelae_paparazzi',
      version='0.1',
      description='Paprazzi UAV utilities for nephelae_project',
      url='ssh://git@redmine.laas.fr/laas/users/simon/nephelae/nephelae-devel/nephelae_paparazzi.git',
      author='Pierre Narvor',
      author_email='pnarvor@laas.fr',
      licence='bsd3',
      packages=find_packages(include=['nephelae_paparazzi*']),
      install_requires=[
        'numpy',
        'matplotlib',
        'ivy-python',
        'netCDF4',
        'defusedxml',
        'utm',
        'lxml'
      ],
      zip_safe=False)


