from setuptools import setup, find_packages

setup(
    name="enso-cli",
    version="0.1.0",
    packages=['cli'],
    package_dir={"cli": "src/cli"},
    package_data={"": ["py.typed"]},
    install_requires=[
        "click",
        "pywebpush"
    ],
    entry_points={
        "console_scripts": [
            "enso=cli.cli:enso",
        ],
    },
    python_requires=">=3.7",
)