from setuptools import find_packages, setup

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in strategic_gears_cms_site_api/__init__.py
from strategic_gears_cms_site_api import __version__ as version

setup(
	name="strategic_gears_cms_site_api",
	version=version,
	description="strategic-gears-cms-site-api",
	author="shyam",
	author_email="shyamkumar@8848digital.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)
