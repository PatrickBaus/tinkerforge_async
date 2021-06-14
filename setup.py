from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
   name='tinkerforge_async',
   version='1.1.2',
   author='Patrick Baus',
   author_email='patrick.baus@physik.tu-darmstadt.de',
   url='https://github.com/PatrickBaus/TinkerforgeAsync',
   description='An AsyncIO implementation for the Tinkerforge API',
   long_description=long_description,
   classifiers=[
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Topic :: Home Automation',
   ],
   keywords='TinkerForge API',
   license='GPL',
   license_files=('LICENSE',),
   packages=['tinkerforge_async'],  # same as name
   install_requires=['async-timeout', ],  # external packages as dependencies
)
