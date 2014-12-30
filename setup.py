from setuptools import setup
setup(
	name='torrentsManager',
	version='0.1.0',
	author='Jonatan Dellagostin',
	author_email='jdellagostin@gmail.com',
	packages=['torrentsManager'],
	scripts=['bin/'],
	#url='http://pypi.python.org/pypi/TowelStuff/',
	license='LICENSE.txt',
	description='Torrents manager',
	long_description=open('README.txt').read(),
	install_requires=[
		"ConfigParser",
		"transmissionrpc",
		"dateutils >= 0.6.6",
		"logging",
		"ast",
		"tpb",
		"pytvdbapi"
    ],
)
