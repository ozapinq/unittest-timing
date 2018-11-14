from setuptools import setup, find_packages

setup(
    name="unittest-timing",
    version="1.0",
    description="TestRunner with test and TestCase setup/teardown timing",
    author="Nikolay Sedelnikov",
    author_email="n.sedelnikov@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True
)
