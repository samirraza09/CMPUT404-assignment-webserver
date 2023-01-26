#  coding: utf-8 
import socketserver
import os.path
from os import path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    host = "localhost:8080"
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        requestBody = self.data.decode('utf-8')
        requestLines = requestBody.split('\r\n')
        firstLine = requestLines[0]
        firstLineSplit = firstLine.split(' ');
        requestType = firstLineSplit[0]
        filePath = firstLineSplit[1]
        
        if len(requestLines) == 0 or len(requestType) == 0 or requestType.lower() != 'get':
            requestToSend = "HTTP/1.1 405 Method Not Allowed\r\nHost: " + self.host + "\n\n"
            print("Thrown 405")
            self.request.sendall(bytearray(requestToSend,'utf-8'))

        elif not path.exists('www' + filePath) or '/..' in filePath:
            requestToSend = "HTTP/1.1 404 Not Found\r\nHost: " + self.host + "\n\n"
            self.request.sendall(bytearray(requestToSend,'utf-8'))

        elif path.isfile('www' + filePath):
            if filePath[-4:] == '.css':
                requestToSend = "HTTP/1.1 200 OK\r\nHost: " + self.host + "\r\nContent-Type: text/css\n\n"
            
                # https://flaviocopes.com/python-read-file-content/
                requestToSend += open('./www' + filePath, 'r').read();
                self.request.sendall(bytearray(requestToSend,'utf-8'))

            requestToSend = "HTTP/1.1 200 OK\r\nHost: " + self.host + "\r\nContent-Type: text/html\n\n"
            
            # https://flaviocopes.com/python-read-file-content/
            requestToSend += open('./www' + filePath, 'r').read();
            self.request.sendall(bytearray(requestToSend,'utf-8'))

        # If the last character in the path is a / then add index.html
        elif filePath[len(filePath) - 1] == '/':
            filePath += 'index.html'
            requestToSend = "HTTP/1.1 200 OK\r\nHost: " + self.host + "\r\nContent-Type: text/html\n\n"
            
            # https://flaviocopes.com/python-read-file-content/
            requestToSend += open('./www' + filePath, 'r').read();
            self.request.sendall(bytearray(requestToSend,'utf-8'))

        # If the path ends with a directory but is missing a / send a 301
        elif path.exists('www' + filePath) and filePath[len(filePath) - 1] != '/':
            relocatedLocation = filePath + "/"

            requestToSend = "HTTP/1.1 301 Permanently Moved\r\nHost: " + self.host + "\r\nLocation "
            requestToSend += relocatedLocation + "\n\n"
            self.request.sendall(bytearray(requestToSend,'utf-8'))
 
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
