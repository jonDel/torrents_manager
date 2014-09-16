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
        "BeautifulSoup <= 3.2.1",
        "mechanize >= 0.2.5",
        "GitPython >= 0.3.2",
        "logging >= 0.4.9.6",
        "dateutils >= 0.6.6",
        "paramiko >= 1.7.7.1",
        "pexpect >= 2.4",
    ],
)
