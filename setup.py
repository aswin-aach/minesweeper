from setuptools import setup, find_packages

setup(
    name="minesweeper",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'minesweeper=main:main',
        ],
    },
    include_package_data=True,
    description="A Minesweeper clone with Tkinter GUI",
    author="Minesweeper Team",
)
