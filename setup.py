import setuptools

setuptools.setup(
	name="enkanetwork.py",
	version="1.0.0",
	author="M-307",
	author_email="contact@m-307.tk",
	description="Library for fetching JSON data from site https://enka.shinshin.moe/",
	long_description=open("./README.md", "r", encoding="utf-8").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/mrwan200/enkanetwork-py",
	keywords = ['enkanetwork.py', 'enkanetwork', 'enka.shinshin.moe', 'genshinapi'],
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=open("./requirements.txt", "r", encoding="utf-8").readlines(),
	python_requires=">=3.6",
	include_package_data=True
)