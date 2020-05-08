import os

class Configuration(object):
	'''
	Provides functionality for managing the configuration of docker-shell itself
	'''
	
	@staticmethod
	def windowsAutoSelectEnabled():
		'''
		Determines if automatic Docker daemon selection is enabled under Windows 10
		'''
		return os.environ.get('DOCKERSHELL_WINDOWS_AUTO_SELECT', '0').lower() in ['1', 'true']
