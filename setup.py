import setuptools

setuptools.setup(
	name="enkanetwork.py",
	version="1.2.4",
	author="M-307",
	author_email="me@m307.dev",
	description="Library for fetching JSON data from site https://enka.network/",
	long_description=open("README.md", "r", encoding="utf-8").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/mrwan200/EnkaNetwork.py",
	keywords = ['enkanetwork.py', 'enkanetwork', 'enka.network', 'genshinapi'],
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[
		"pydantic",
		"aiohttp"
	],
	python_requires=">=3.6",
	include_package_data=True
)