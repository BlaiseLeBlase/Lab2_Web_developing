# response = '''HTTP/1.1 {status}
# Connection: Close
#
# {html}
# '''
#
# context = {}
#
# context['status'] = 200
# context['html'] = '<html></html>'
#
# response.format(**context)


import SocketServer
import re
import os
import os.path

ROOT = 'C:\logfile\\'


class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        path = re.findall('^GET (.*) HTTP\/1\.1$', self.data.splitlines()[0])[0]
        target = os.path.join(ROOT, *path.split('/'))
        if os.path.exists(target):
            # TODO: check if target is directory return list of files
            content = open(target).read()
            self.request.sendall(content)
        else:
            self.request.sendall('404 not found')


if __name__ == "__main__":
    HOST, PORT = "localhost", 4765

    # Create the server, binding to localhost on port 4765
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print 'listening on ', HOST, ':', PORT
    server.serve_forever()