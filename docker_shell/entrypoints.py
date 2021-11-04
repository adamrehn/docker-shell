from .DockerShell import DockerShell
from os.path import abspath, join
import argparse, sys

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

def pwsh():
	'''
	The entrypoint executed by running the `dpwsh` executable
	'''
	main('pwsh')

def main(shell=None):
	'''
	The entrypoint executed by running the `docker-shell` executable
	'''
	
	# Our supported command-line arguments
	parser = argparse.ArgumentParser(
		prog='docker-shell',
		usage='%(prog)s [-h] [--no-gpu] [--verbose] shell image [--] [ARGS FOR SHELL]',
		epilog='Additional arguments can be passed to the launched shell by specifying `--` followed by the arguments for the shell.'
	)
	parser.add_argument('shell', help='The shell to be launched inside the container (e.g. bash, sh, zsh, cmd, powershell, pwsh, etc.)')
	parser.add_argument('image', help='The fully-qualified tag for the container image to use')
	parser.add_argument('--no-gpu', action='store_true', help="Don't enable NVIDIA GPU support even if the container image and host system both support it")
	parser.add_argument('--verbose', action='store_true', help="Enable verbose output")
	parser.add_argument('--prefix-paths', default=None, help="Prefix to prepend to any absolute filesystem paths in the shell arguments (Unix paths only)")
	
	# If a shell was specified via a specific alias, inject it into our argument list
	if shell is not None:
		sys.argv[0] = 'docker-shell'
		sys.argv.insert(1, shell)
	
	# If too few command-line arguments were supplied, display the help message and exit
	if len(sys.argv) < 3:
		parser.print_help()
		sys.exit(0)
	
	# If additional arguments were supplied to pass to the shell, separate these from our own arguments and any flags to pass to Docker
	shellArgs = []
	if '--' in sys.argv:
		split = sys.argv.index('--')
		shellArgs = sys.argv[split+1:]
		sys.argv = sys.argv[:split]
	
	# Parse the supplied command-line arguments
	args, dockerArgs = parser.parse_known_args()
	
	# If a prefix was supplied then prepend it to any absolute filesystem paths in the shell arguments
	if args.prefix_paths is not None:
		shellArgs = list([
			join(args.prefix_paths, a[1:]) if a.startswith('/') and abspath(a) == a else a
			for a in shellArgs
		])
	
	try:
		
		# Connect to the Docker daemon
		shell = DockerShell(args.image, args.shell, noGPU=args.no_gpu, dockerArgs=dockerArgs, shellArgs=shellArgs)
		
		# Pull the specified container image if it is not already available
		if shell.requiresPull() == True:
			print("Unable to find image '{}' locally".format(args.image))
			shell.pull()
		
		# Start an interactive container and launch the requested shell
		sys.exit(shell.launch(verbose=args.verbose))
		
	except Exception as e:
		print('Error: {}'.format(e), file=sys.stderr)
		sys.exit(1)
