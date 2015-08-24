#!/usr/bin/python
# Cache Agent in Agent based management and control system
# Chen Wang, chenw@cmu.edu
#!/bin/env python
import sys
import os

try:
    # Python 2.x
    from SocketServer import ThreadingMixIn
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer
except ImportError:
    # Python 3.x
    from socketserver import ThreadingMixIn
    from http.server import SimpleHTTPRequestHandler, HTTPServer

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
	def do_GET(self):
		filepath = self.path
		fileSz = os.path.getsize(filepath)
		print "File Size:", fileSz
    	pass

#==========================================================================================
# Main Function of Cache Agent
#==========================================================================================
def main(argv):
	if sys.argv[1:]:
	    port = int(sys.argv[1])
	else:
	    port = 80

	if sys.argv[2:]:
	    os.chdir(sys.argv[2])

	server = ThreadingSimpleServer(('', port), SimpleHTTPRequestHandler)
	try:
	    while 1:
	        sys.stdout.flush()
	        server.handle_request()
	except KeyboardInterrupt:
	    print("Finished")

if __name__ == '__main__':
    main(sys.argv)
 
