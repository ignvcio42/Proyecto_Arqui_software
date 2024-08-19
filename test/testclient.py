import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:
        # Send message in the specified format
        if input('Send formatted message to service? y/n: ') != 'y':
            break
        equipo = "PC1"
        descripcion = "pc gigante"
        tipo = "PC"
        tarifa = "100"
        datos = f"{equipo}-{descripcion}-{tipo}-{tarifa}"
        servicio = "CODAE"
        longitud_datos = len(servicio + datos)
        message = f"{longitud_datos:05}{servicio}{datos}".encode()
        print('sending {!r}'.format(message))
        sock.sendall(message)

        # Look for the response
        print("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            print("Checking service answer ...")
            print('received {!r}'.format(data))


finally:
    print('closing socket')
    sock.close()