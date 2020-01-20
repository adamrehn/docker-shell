import docker, os, platform, shutil, subprocess
from packaging import version

class DockerShell(object):
	
	def __init__(self, image, shell, noGPU=False, args=[]):
		'''
		Creates a new shell runner and connects to the Docker daemon
		'''
		
		# Store our configuration details
		self._image = image
		self._shell = shell
		self._noGPU = noGPU
		self._args = args
		
		# Attempt to connect to the Docker daemon
		self._docker = docker.from_env()
		self._docker.ping()
	
	def requiresPull(self):
		'''
		Determines if our container image needs to be pulled
		'''
		try:
			self._docker.images.get(self._image)
			return False
		except:
			return True
	
	def launch(self):
		'''
		Starts an interactive container and launches a shell inside of it
		'''
		
		# Parse the Docker daemon version string
		dockerVersion = version.parse(self._docker.version()['Version'])
		
		# Retrieve the container image details
		details = self._docker.images.get(self._image).attrs
		
		# Extract the list of environment variables set for the container image (if any)
		environmentPairs = details['Config']['Env'] if details['Config']['Env'] is not None else []
		environmentKeys = [pair.split('=', 1)[0] if '=' in pair else '' for pair in environmentPairs]
		
		# Bind-mount our working directory using an appropriate path for the container platform
		mount = 'C:\\hostdir' if details['Os'] == 'windows' else '/hostdir'
		
		# If we're running a Linux container on a Linux host, use host networking mode
		bothLinux = platform.system() == 'Linux' and details['Os'] == 'linux'
		networkArgs = ['--network', 'host'] if bothLinux else []
		
		# If we're using a container image with NVIDIA GPU support and the host supports it, enable GPU access
		gpuArgs = []
		if self._noGPU == False and bothLinux == True and shutil.which('nvidia-smi') is not None and 'NVIDIA_VISIBLE_DEVICES' in environmentKeys:
			
			# Use the appropriate detection logic and flags for the version of the Docker daemon we are communicating with
			if dockerVersion >= version.parse('19.03.0') and shutil.which('nvidia-container-cli') is not None:
				gpuArgs = ['--gpus', 'all']
			elif 'nvidia' in self._docker.info()['Runtimes']:
				['--runtime', 'nvidia']
		
		# Start the container and launch the shell
		subprocess.run([
			'docker', 'run',
			'--rm', '-ti',
			'-v', '{}:{}'.format(os.getcwd(), mount),
			'-w', mount,
			] + networkArgs + [
			] + gpuArgs + [
			] + self._args + [
			'--entrypoint', self._shell,
			self._image
		])
