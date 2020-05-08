import docker, os, platform, subprocess, time
from .Configuration import Configuration

class DaemonSelection(object):
	'''
	Provides functionality for automatically selecting the most appropriate Docker daemon when starting a container
	'''
	
	@staticmethod
	def selectDaemon(shell, image):
		'''
		Automatically selects the appropriate Docker daemon for the specified shell and image
		'''
		
		# Determine if we are running Docker Desktop under Windows 10 and automatic selection is enabled
		if platform.system().lower() == 'windows' and platform.win32_ver()[0] == '10' and Configuration.windowsAutoSelectEnabled():
			
			# Select the Windows Docker daemon or the Linux Docker daemon based on which shell was specified
			# (Note that this check relies on the user specifying "pwsh" if their intention is to use PowerShell Core under Linux)
			daemon = 'windows' if shell in ['cmd', 'powershell'] else 'linux'
			
			# If the selected Docker daemon is not the currently active one then switch to it
			if DaemonSelection._detectCurrentDaemon() != daemon:
				
				# Trigger the daemon switch
				print('Automatically switching Docker Desktop to {} containers mode...'.format(daemon.title()), flush=True)
				subprocess.run([os.path.join(os.environ['ProgramFiles'], 'Docker', 'Docker', 'DockerCli.exe'), '-SwitchDaemon'], check=True)
				
				# Wait until the switch has completed
				while DaemonSelection._detectCurrentDaemon() != daemon:
					time.sleep(1)
	
	@staticmethod
	def _detectCurrentDaemon():
		'''
		Detects which Docker daemon is currently active when running Docker Desktop under Windows 10
		'''
		client = docker.from_env()
		return client.info()['OSType'].lower()
