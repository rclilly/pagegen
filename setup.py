from setuptools import setup

files=['skel/*', 'pagegen.conf', 'changelog']

setup(name = 'pagegen',
	version='3.0.0',
	description='Static site generator',
	author='Oliver Fields',
	author_email='pagegen@phnd.net',
	url='http://pagegen.phnd.net',
	license='GPLv3',
	packages=['pagegen'],
	#package_data={'pagegen' : files },
	long_description="""Python static site generator with reStructuredText markup.""",
	install_requires=['lxml','docutils','configparser'],
        entry_points={
            'console_scripts': ['pagegen=pagegen.pagegen:main']
        }
)
