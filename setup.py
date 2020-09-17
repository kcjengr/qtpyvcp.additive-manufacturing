from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("entry_points.ini", "r") as fh:
    entry_points = fh.read()

setup(
    name="qtpyvcp.custom-widgets-template",
    version="0.0.1",
    author="Kurt Jacobson",
    author_email="",
    description="Template repository for providing custom QtPyVCP widgets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kcjengr/qtpyvcp.custom-widgets-template",
    download_url="https://github.com/kcjengr/qtpyvcp.custom-widgets-template/tarball/master",
    packages=find_packages(),
    include_package_data=True,
    entry_points=entry_points
)
