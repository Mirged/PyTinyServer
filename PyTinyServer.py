import socket

RESPONSE_HEADER = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'

def serve_file(client_socket, filename):
    try:
        with open(filename, 'rb') as file:
            client_socket.send(RESPONSE_HEADER)
            client_socket.send(file.read())
    except FileNotFoundError:
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\nFile not found')

def handle_request(client_socket, main_page):
    request_data = client_socket.recv(1024).decode()
    request_lines = request_data.split('\r\n')
    filename = request_lines[0].split()[1][1:]
    if not filename:
        serve_file(client_socket, main_page)
    else:
        serve_file(client_socket, filename)
    client_socket.close()

def start_server(host, port, main_page):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f'Server listening on port {port}')
        while True:
            client_socket, address = server_socket.accept()
            print(f'Accepted connection from {address[0]}:{address[1]}')
            handle_request(client_socket, main_page)
