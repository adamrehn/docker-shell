import docker, itertools, os, platform, shutil, subprocess, sys
from packaging import version
from .Utility import Utility

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
		
		# Cache the host system's IP address so we only ever query it once
		self._hostIP = Utility.hostSystemIP()
		
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
	
	def launch(self, verbose=False):
		'''
		Starts an interactive container and launches a shell inside of it
		'''
		
		# Parse the Docker daemon version string
		dockerVersion = version.parse(self._docker.version()['Version'])
		
		# Retrieve the container image details
		details = self._docker.images.get(self._image).attrs
		
		# Determine the platform of both the host system and the container image
		hostPlatform = 'mac' if platform.system() == 'Darwin' else platform.system().lower()
		containerPlatform = details['Os']
		
		# Extract the list of environment variables set for the container image (if any)
		environmentPairs = details['Config']['Env'] if details['Config']['Env'] is not None else []
		environmentKeys = [pair.split('=', 1)[0] if '=' in pair else '' for pair in environmentPairs]
		
		# Bind-mount our working directory using an appropriate path for the container platform
		mount = 'C:\\hostdir' if containerPlatform == 'windows' else '/hostdir'
		
		# If we're running a Linux container on a Linux host, use host networking mode
		bothLinux = hostPlatform == 'linux' and containerPlatform == 'linux'
		networkArgs = ['--network', 'host'] if bothLinux else []
		
		# If we're using a container image with NVIDIA GPU support and the host supports it, enable GPU access
		gpuArgs = []
		if self._noGPU == False and bothLinux == True and shutil.which('nvidia-smi') is not None and 'NVIDIA_VISIBLE_DEVICES' in environmentKeys:
			
			# Use the appropriate detection logic and flags for the version of the Docker daemon we are communicating with
			if dockerVersion >= version.parse('19.03.0') and shutil.which('nvidia-container-cli') is not None:
				gpuArgs = ['--gpus', 'all']
			elif 'nvidia' in self._docker.info()['Runtimes']:
				['--runtime', 'nvidia']
		
		# Apply any bind mounts specified in the image labels, including any mounts specific to the host platform
		labels = details['Config']['Labels'] if details['Config']['Labels'] is not None else {}
		bindMounts = self._extractLabels(labels, 'docker-shell.mounts.') + self._extractLabels(labels, 'docker-shell.{}.mounts.'.format(hostPlatform))
		mountArgs = list(itertools.chain.from_iterable([['-v', mount] for mount in bindMounts]))
		
		# Apply any additional arguments specified in the image labels, including any arguments specific to the host platform
		extraArgs = self._extractLabels(labels, 'docker-shell.args.') + self._extractLabels(labels, 'docker-shell.{}.args.'.format(hostPlatform))
		
		# Assemble the completed `docker run` command
		command = [
			'docker', 'run',
			'--rm', '-ti',
			'-v', '{}:{}'.format(os.getcwd(), mount),
			'-w', mount,
			] + networkArgs + [
			] + gpuArgs + [
			] + mountArgs + [
			] + extraArgs + [
			] + self._args + [
			'--entrypoint', self._shell,
			self._image
		]
		
		# If verbose output is enabled, print the `docker run` command prior to executing it
		if verbose == True:
			print(command, file=sys.stderr)
		
		# Start the container and launch the shell
		subprocess.run(command)
	
	def _extractLabels(self, labels, prefix):
		'''
		Extracts the list of image labels whose keys match the specified prefix, applying our custom path expansion to the values
		'''
		return [self._expandVars(labels[key]) for key in labels if key.startswith(prefix)]
	
	def _expandVars(self, p):
		'''
		Expands environment variables and user home directories in a path, as well as our supported custom variables
		'''
		
		# Make a copy of the original environment variables and add our custom variables
		environ = os.environ.copy()
		os.environ['CWD'] = os.getcwd()
		os.environ['HOSTIP'] = self._hostIP
		
		# Expand paths and user home directories
		expanded = os.path.expanduser(os.path.expandvars(p))
		
		# Restore the original environment variables and return the expanded path
		os.environ = environ
		return expanded
