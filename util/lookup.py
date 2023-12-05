import socket

class Resolve:

    def fqdn(self, fqdn):
        try:
            return socket.gethostbyname(fqdn)

        except socket.gaierror:
            return None
