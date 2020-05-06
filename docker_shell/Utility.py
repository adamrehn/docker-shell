import socket

class Utility(object):
	
	@staticmethod
	def hostSystemIP():
		'''
		Determines the IP address of the host system, falling back to 127.0.0.1 upon failure
		'''
		# Code from <https://stackoverflow.com/a/28950776>
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			s.connect(('10.255.255.255', 1))
			ip = s.getsockname()[0]
		except:
			ip = '127.0.0.1'
		finally:
			s.close()
		return ip
