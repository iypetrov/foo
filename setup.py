from setuptools import setup, find_packages

with open("../../work/projects/besudb/bpa-dev-tools/README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as req_file:
    install_requires = req_file.read().splitlines()

setup(
    name="foo",
    version="1.0.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IliyaYavorovPetrov/foo",
    packages=find_packages(exclude=("tests",)),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'foo = src.__main__:main'
        ]
    },
    data_files=[('', ['.env'])]
)
