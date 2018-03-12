from setuptools import setup

setup(
    name="airswap",
    version='0.1',
    py_modules=['airswap'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        airswap=airswap:displayAvgPrice
    ''',
)