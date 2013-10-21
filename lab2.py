LISTING = '<a href="{file}">{file}<a/><br>'

import SocketServer
import re
import os

ROOT = 'C:\\logfile'


class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        path = re.findall('^GET (.*) HTTP\/1\.1$', self.data.splitlines()[0])[0]
        target = os.path.join(ROOT, *path.split('/'))
        if os.path.exists(target):
            # TODO: check if target is directory return list of files
            if os.path.isabs(target):
                content = '\n'.join([LISTING.format(file=f) for f in os.listdir(target)])
            else:
                content = open(target).read()
            self.request.sendall(content)
        else:
            self.request.sendall('404 not found')


if __name__ == "__main__":
    HOST, PORT = "localhost", 4765

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print 'listening on ', HOST, ':', PORT
    server.serve_forever()