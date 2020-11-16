from setuptools import setup

def readme():
	with open("README.rst") as f:
		return f.read()

def install_requires():
	with open("requirements.txt") as f:
		return f.readlines()

setup(name="tmpmail",
	version="0.1",
	description="Create and view temporary mailbox using 1secmail API.",
	long_description=readme(),
	classifiers=[
	"Development Status :: 3 - Alpha",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python :: 3.7",
	"Topic :: Utilities",
	],
	keywords=["mail", "email"],
	#url="http://github.com/meashishsaini/bsnl",
	author="Ashish Saini",
	author_email="sainiashish08@gmail.com",
	license="MIT",
	packages=["tmpmail"],
	install_requires=install_requires(),
	entry_points={
	"console_scripts": ["tmpmail=tmpmail.main:parse"],
	},
	include_package_data=True,
	zip_safe=False)
