from http.server import BaseHTTPRequestHandler, HTTPServer
from StorageData import *
from re import search, match
import json
import logging
import time

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def _set_response(self, response):
        self.send_response(response[0])
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response[1].encode(encoding='utf_8'))

    def do_GET(self):
        print(self.path)
        list_one_requisition = search('/(user)\/([a-z0-9]+)(?:\/?$)', self.path)
        if self.path == "/user/":
            response = list_all_users()
            self._set_response(response)

        elif list_one_requisition:
            print("listar unico")
            response = list_one_user(list_one_requisition.group(2))
            self._set_response(response)

    def do_POST(self):
        print("POST requisition recieve")
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        response = create_user(post_data)
        self._set_response(response)


    def do_PUT(self):
        print("Put requisition received")
        print(self.path)
        content_length = int(self.headers['Content-Length'])
        requisition_body = self.rfile.read(content_length)
        if self.path == "/user/updatepassword/":
            response = update_password(requisition_body)
            self._set_response(response)

        elif self.path == "/user/checkpassword/":
            response = check_password(requisition_body)
            self._set_response(response)

        elif self.path == "/user/updateuser/":
            print("Atualizar usuario")
            response = update_user(requisition_body)
            self._set_response(response)


    def do_DELETE(self):
        print("DELETE requisition received")
        list_one_requisition = search('/(user)\/([a-z0-9]+)(?:\/?$)', self.path)
        if list_one_requisition:
            user_id = list_one_requisition.group(2)
            response = delete_user(user_id)
            self._set_response(response)




if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
