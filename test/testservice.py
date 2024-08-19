import socket
import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='CyberCafeManager',
            user='root',
            password='root_password'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port where the bus will listen
bus_address = ('localhost', 5000)
print('starting up on {} port {}'.format(*bus_address))
sock.bind(bus_address)

# Listen for incoming connections
sock.listen(1)

try:
    while True:
        print('waiting for a connection')
        client_socket, client_address = sock.accept()
        try:
            print('connection from', client_address)

            while True:
                # Receive the message
                amount_received = 0
                amount_expected = int(client_socket.recv(5))
                data = b''
                while amount_received < amount_expected:
                    chunk = client_socket.recv(amount_expected - amount_received)
                    if not chunk:
                        break
                    data += chunk
                    amount_received += len(chunk)

                if not data:
                    break

                # Process the received message
                print("Processing ...")
                print('received {!r}'.format(data))

                #EJEMPLO: 00026CODAEPC1-pc gigante-PC-100
                #Servicio: define el codigo a usar por ejemplo: CODAE -> Crear un equipo
                servicio = data[:5].decode()
                #datos es todo lo que va despues de eso "PC1-pc gigante-PC-100"
                datos = data[5:].decode()
                print(f"Service: {servicio}, Data: {datos}")

                #dataArray lo separa, por guiones
                dataArray = datos.split('-')

                db_connection = connect_db()
                if db_connection is not None:
                    cursor = db_connection.cursor()
                    query = "INSERT INTO Equipo (nombre, descripcion, tipo, tarifa) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (dataArray[0], dataArray[1], dataArray[2], dataArray[3]))
                    db_connection.commit()
                    equipo_id = cursor.lastrowid
                    db_connection.close()

                # Here you can further process the `datos` according to your logic

                # Send the response
                response = f"{servicio}{datos}"
                response_length = len(response)
                message = f"{response_length:05}{response}".encode()
                print('sending {!r}'.format(message))
                client_socket.sendall(message)
        finally:
            client_socket.close()
finally:
    print('closing socket')
    sock.close()