from .DockerShell import DockerShell
import argparse, subprocess, sys

def bash():
	'''
	The entrypoint executed by running the `dbash` executable
	'''
	main('bash')

def sh():
	'''
	The entrypoint executed by running the `dsh` executable
	'''
	main('sh')

def zsh():
	'''
	The entrypoint executed by running the `dzsh` executable
	'''
	main('zsh')

def cmd():
	'''
	The entrypoint executed by running the `dcmd` executable
	'''
	main('cmd')

def powershell():
	'''
	The entrypoint executed by running the `dps` or `dpowershell` executables
	'''
	main('powershell')

def main(shell=None):
	'''
	The entrypoint executed by running the `docker-shell` executable
	'''
	
	# Our supported command-line arguments
	parser = argparse.ArgumentParser(prog='docker-shell')
	parser.add_argument('shell', help='The shell to be launched inside the container (e.g. bash, sh, zsh, cmd, powershell, etc.)')
	parser.add_argument('image', help='The fully-qualified tag for the container image to use')
	parser.add_argument('--no-gpu', action='store_true', help="Don't enable NVIDIA GPU support even if the container image and host system both support it")
	parser.add_argument('--verbose', action='store_true', help="Enable verbose output")
	
	# If a shell was specified via a specific alias, inject it into our argument list
	if shell is not None:
		sys.argv[0] = 'docker-shell'
		sys.argv.insert(1, shell)
	
	# If too few command-line arguments were supplied, display the help message and exit
	if len(sys.argv) < 3:
		parser.print_help()
		sys.exit(0)
	
	# Parse the supplied command-line arguments
	args, extraArgs = parser.parse_known_args()
	
	try:
		
		# Connect to the Docker daemon
		shell = DockerShell(args.image, args.shell, noGPU=args.no_gpu, args=extraArgs)
		
		# Pull the specified container image if it is not already available
		if shell.requiresPull() == True:
			print("Unable to find image '{}' locally".format(args.image))
			subprocess.run(['docker', 'pull', args.image], check=True)
		
		# Start an interactive container and launch the requested shell
		shell.launch(verbose=args.verbose)
		
	except Exception as e:
		print('Error: {}'.format(e), file=sys.stderr)
		sys.exit(1)
