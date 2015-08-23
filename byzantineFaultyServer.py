#!/usr/bin/python
# Cache Agent in Agent based management and control system
# Chen Wang, chenw@cmu.edu
import subprocess 
import argparse
import string,cgi,time
import json
import ntpath
import sys
import urllib2
import sqlite3 as lite
import shutil
import operator
import requests
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os # os. path
 
## Current Path
CWD = os.path.abspath('.')

## Global Varibles
PORT = 80     

## Global Variables for Database connection
con = None
cur = None

## Global variable to access GCE

def make_index( relpath ):     
    abspath = os.path.abspath(relpath) # ; print abspath
    flist = os.listdir( abspath ) # ; print flist
     
    rellist = []     
    for fname in flist :     
        # relname = os.path.join(relpath, fname)
        # rellist.append(relname)
        rellist.append(fname)
     
     # print rellist
    inslist = []     
    for r in rellist :     
        inslist.append( '<a href="%s">%s</a><br>' % (r,r) )
     
    # print inslist
     
    page_tpl = "<html><head></head><body>%s</body></html>"         
    ret = page_tpl % ( '\n'.join(inslist) , )
     
    return ret

def welcome_page():
    page = "<html>  \
                <title>  \
                    Server with Arbitrary Fault \
                </title> \
                <body>  \
                    <h1> Welcome!! </h1>\
                    <p>This is a server running with Arbitrary Faults </p>\
                    <p>You can use '/videos' to show all available videos in local cache! </p>\
                </body> \
            </html>"
    return page

def num(s):
        try:
                return int(s)
        except ValueError:
                return float(s)

# -----------------------------------------------------------------------
class MyHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if "ico" in self.command:
				return

			elif self.path == '/' :
				page = welcome_page()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write(page)
				return

			## Processing requests related to locally cached videos 
			elif self.path.startswith('/videos'):
				page = make_index( self.path.replace('/videos', '../videos') )
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write(page)
                return

            elif self.path.endswith(".html"):
                ## print curdir + sep + self.path
                f = open(curdir + sep + self.path)
                #note that this potentially makes every file on your computer readable by the internet
                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
                
            elif self.path.endswith(".esp"):   #our dynamic content
                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()
                self.wfile.write("hey, today is the " + str(time.localtime()[7]))
                self.wfile.write(" day in the year " + str(time.localtime()[0]))
                return

            else :
            	client_addr = self.client_address[0]
                filepath = '../videos' + self.path
                fileSz = os.path.getsize(filepath)
                f = open( os.path.join(CWD, filepath), 'rb' )
                #note that this potentially makes every file on your computer readable by the internet
                self.send_response(200)
                self.send_header('Content-type',    'application/octet-stream')
                self.send_header('Content-Length', str(fileSz))
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            return # be sure not to fall into "except:" clause ?       

        except IOError as e :  
             # debug     
             print e
             self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write("<HTML><HEAD></HEAD><BODY>POST OK.<BR><BR>");
            self.wfile.write( "File uploaded under name: " + os.path.split(fullname)[1] );
            self.wfile.write(  '<BR><A HREF=%s>back</A>' % ( UPLOAD_PAGE, )  )
            self.wfile.write("</BODY></HTML>");

#==========================================================================================
# Main Function of Cache Agent
#==========================================================================================
def main(argv):
    try:
	    server = HTTPServer(('', PORT), MyHandler)
	    print 'started httpserver...'
	    server.serve_forever()

    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main(sys.argv)
 
