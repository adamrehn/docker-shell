from os.path import abspath, dirname, join
from setuptools import setup

# Read the README markdown data from README.md
with open(abspath(join(dirname(__file__), 'README.md')), 'rb') as readmeFile:
	__readme__ = readmeFile.read().decode('utf-8')

setup(
	name='docker-shell',
	version='0.0.2',
	description='Docker Interactive Shell Runner',
	long_description=__readme__,
	long_description_content_type='text/markdown',
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Environment :: Console'
	],
	keywords='docker interactive console terminal',
	url='http://github.com/adamrehn/docker-shell',
	author='Adam Rehn',
	author_email='adam@adamrehn.com',
	license='MIT',
	packages=['docker_shell'],
	zip_safe=True,
	python_requires = '>=3.5',
	install_requires = [
		'docker>=4.0.0',
		'setuptools>=38.6.0',
		'twine>=1.11.0',
		'wheel>=0.31.0'
	],
	entry_points = {
		'console_scripts': [
			'docker-shell=docker_shell.entrypoints:main',
			'dbash=docker_shell.entrypoints:bash',
			'dsh=docker_shell.entrypoints:sh',
			'dzsh=docker_shell.entrypoints:zsh',
			'dcmd=docker_shell.entrypoints:cmd',
			'dps=docker_shell.entrypoints:powershell',
			'dpowershell=docker_shell.entrypoints:powershell'
		]
	}
)
