from setuptools import setup, find_packages


__version__ = "0.0.1"


setup(
    name="demo",
    version=__version__,
    description="Flask demo application",
    author="Nick",
    author_email="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=0.10.0",
    ]
)
