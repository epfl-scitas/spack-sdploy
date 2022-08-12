import setuptools

setuptools.setup(
    name="YAML Reader",
    version="0.1",
    author="SCITAS",
    author_email="hpc@epfl.ch",
    install_requires=["pyyaml"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "yareed = yareed.main:main",
        ]
    }
)
