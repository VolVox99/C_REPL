from setuptools import setup, find_packages

setup(
    name="c_repl",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "c_repl = c_repl.__main__:main",
        ],
    },
)