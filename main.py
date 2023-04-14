import socket

HOST = ''  # empty string means we listen on all available interfaces
PORT = 8080

# response header with content type of HTML
RESPONSE_HEADER = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'

def serve_file(client_socket, filename):
    # try to open the requested file
    try:
        with open(filename, 'rb') as file:
            # send the response header
            client_socket.send(RESPONSE_HEADER)
            # send the file contents
            client_socket.send(file.read())
    except FileNotFoundError:
        # if the file isn't found, send a 404 error
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\nFile not found')

def handle_request(client_socket, address):
    # read the request data from the client socket
    request_data = client_socket.recv(1024).decode()
    # split the request data into lines
    request_lines = request_data.split('\r\n')
    # extract the requested filename from the first line of the request
    filename = request_lines[0].split()[1][1:]  # remove leading slash

    # if the requested filename is empty, redirect to index.html
    if not filename:
        client_socket.send(b'HTTP/1.1 301 Moved Permanently\r\nLocation: /index.html\r\n\r\n')
        return

    # serve the requested file
    serve_file(client_socket, filename)

    # close the client socket
    client_socket.close()

def main():
    # create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # bind the socket to a host and port
        server_socket.bind((HOST, PORT))
        # listen for incoming connections
        server_socket.listen()

        print(f'Server listening on port {PORT}')

        while True:
            # accept a client connection
            client_socket, address = server_socket.accept()
            print(f'Accepted connection from {address[0]}:{address[1]}')
            # handle the client request
            handle_request(client_socket, address)

if __name__ == '__main__':
    main()
