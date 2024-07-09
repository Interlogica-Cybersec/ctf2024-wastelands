from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import logging
import time
import re

LOG_FILE = f'{int(time.time())}.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimpleCTFServer(BaseHTTPRequestHandler):
    response_headers = []

    def send_header(self, keyword, value):
        self.response_headers.append((keyword, value))
        super().send_header(keyword, value)

    def end_headers(self):
        self.log_response_headers()
        self.response_headers = []
        super().end_headers()

    def log_response_headers(self):
        log_message = ''
        for header, value in self.response_headers:
            if header.strip() == "" and value.strip() == "":
                break
            log_message += f'\n\t{header}: {value}'
        logging.info(log_message + '\n')

    def do_GET(self):
        parsed_path = urlparse(self.path)
        self.response_headers = []
        
        if parsed_path.path == '/verify':
            query = parse_qs(parsed_path.query)
            username = query.get('username', ['Guest'])[0]
            message = "Unauthorized."
            
            self.send_response(401)
            self.send_header('Content-type', 'text/plain')
            self.send_header('X-Role', 'none')
            self.send_header('X-Username', username)
            self.end_headers()
            self.wfile.write(message.encode())
        elif parsed_path.path == '/status':
            role = "none"
            with open(LOG_FILE, 'r') as log_file:
                log_contents = log_file.read()
                matches = re.findall(r'^\s*X-Role: (\w+)', log_contents, re.MULTILINE)
                if matches:
                    role = matches[-1]

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            if role.lower() == 'admin':
                state = f'ROLE\n----\n[{role}] Access granted. Auth Link: /verify/auth/b54809755c600191a7eb56f625e53712 \n\nCHANGELOG\n---------\n[2025-03-02] GovGPT 0.4! Resolved some "interpretation" issues. Maybe\n\nTODO\n----\n[2025-03-05] Our security researcher has informed us that it is possible to execute arbitrary JavaScript code [ alert(1) ] on the Authenticator. I will fix it tomorrow.\n\n'
            else:
                state = f'ROLE\n----\n[{role}] Unauthorized\n\n'
            cleaned_log_contents = "\n".join(line.strip() for line in log_contents.split("\n"))
            response_content = state + "LOGS\n----\n" + cleaned_log_contents
            self.wfile.write(response_content.encode())

        elif parsed_path.path == '/verify/auth/b54809755c600191a7eb56f625e53712': 
            content = '''
                <!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>GovGPT Authenticator</title>
                    <link rel="icon" type="image/x-icon" href="/static/glitch.ico">
                    <style>
                        body,
                        html {
                            height: 100%;
                            margin: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            background-color: #111;
                            color: #fff;
                        }

                        .scanner {
                            border: 16px solid #444;
                            border-top-width: 60px;
                            border-bottom-width: 60px;
                            border-radius: 36px;
                            height: 580px;
                            width: 300px;
                            box-shadow: 0 0 10px #000;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            background: #333;
                            padding: 20px;
                        }

                        .instructions {
                            text-align: center;
                            margin-bottom: 20px;
                            font-size: 16px;
                            padding: 0 10px;
                        }

                        form {
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                        }

                        input[type="text"] {
                            margin-bottom: 20px;
                            padding: 10px;
                            border-radius: 5px;
                            border: 1px solid #ddd;
                            width: 80%;
                            background-color: #444;
                            color: #fff;
                        }

                        input[type="submit"] {
                            padding: 10px 20px;
                            border-radius: 5px;
                            border: none;
                            background-color: #284257;
                            color: white;
                            cursor: pointer;
                        }

                        input[type="submit"]:hover {
                            background-color: #397990;
                        }

                        .logo {
                            width: 200px;
                            margin-bottom: 20px;
                        }
                    </style>
                </head>

                <body>

                    <div class="scanner">
                        <img src="/logo2.png" alt="Logo" class="logo">
                        <div class="instructions">Verified. Welcome!<br><br><b>NTRLGC{L3T5_5PL1T_TH15!}</b></div>
                    </div>

                </body>

                </html>
            '''
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())

        elif parsed_path.path == '/glitch':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('glitch.html', 'rb') as f:
                self.wfile.write(f.read())

        elif parsed_path.path == '/logo.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('logo.png', 'rb') as f:
                self.wfile.write(f.read())

        elif parsed_path.path == '/logo2.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('logo2.png', 'rb') as f:
                self.wfile.write(f.read())

        elif parsed_path.path == '/static/glitch.ico':
            self.send_response(200)
            self.send_header('Content-type', 'image/vnd.microsoft.icon')
            self.end_headers()
            with open('glitch.ico', 'rb') as f:
                self.wfile.write(f.read())
        else:
            content = '''
                <!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>GovGPT Authenticator</title>
                    <link rel="icon" type="image/x-icon" href="/static/glitch.ico">
                    <style>
                        body,
                        html {
                            height: 100%;
                            margin: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            background-color: #111;
                            color: #fff;
                        }

                        .scanner {
                            border: 16px solid #444;
                            border-top-width: 60px;
                            border-bottom-width: 60px;
                            border-radius: 36px;
                            height: 580px;
                            width: 300px;
                            box-shadow: 0 0 10px #000;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            background: #333;
                            padding: 20px;
                        }

                        .instructions {
                            text-align: center;
                            margin-bottom: 20px;
                            font-size: 16px;
                            padding: 0 10px;
                        }

                        form {
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                        }

                        input[type="text"] {
                            margin-bottom: 20px;
                            padding: 10px;
                            border-radius: 5px;
                            border: 1px solid #ddd;
                            width: 80%;
                            background-color: #444;
                            color: #fff;
                        }

                        input[type="submit"] {
                            padding: 10px 20px;
                            border-radius: 5px;
                            border: none;
                            background-color: #284257;
                            color: white;
                            cursor: pointer;
                        }

                        input[type="submit"]:hover {
                            background-color: #397990;
                        }

                        .logo {
                            width: 200px;
                            margin-bottom: 20px;
                        }
                    </style>
                </head>

                <body>

                    <div class="scanner">
                        <img src="/logo.png" alt="Logo" class="logo">
                        <div class="instructions">Insert your username and identify yourself with the fingerprint scanner.<br></div>
                        <form action="/verify" method="GET">
                            <input type="text" name="username">
                            <input type="submit" value="Send">
                        </form>
                    </div>

                </body>

                </html>
            '''
            self.send_response(401)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())
        print(f'end {parsed_path.path}')
def run(server_class=ThreadingHTTPServer, handler_class=SimpleCTFServer, port=5100):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server listening on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
