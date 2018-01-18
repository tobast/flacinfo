""" Setuptools setup file for flacinfo """

from setuptools import setup


setup(
    name='flacinfo',
    version='1.0.0b1',
    description='A script analoguous to `mp3info`, but for flac files',
    url='https://github.com/tobast/flacinfo',
    author='Théophile `tobast` Bastian',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3',
    keywords='flac metadata',
    py_modules=['flacinfo'],
    entry_points={
        'console_scripts': [
            'flacinfo = flacinfo:main',
        ]
    }
    )
