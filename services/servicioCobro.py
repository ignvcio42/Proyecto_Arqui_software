import socket
import sys
import mysql.connector

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

def handle_request(data):
    action = data[:5]
    if action == "CODCP":
        return cobrar_por_equipo(data[5:])
    else:
        return "COBRONK, Acción inválida"

def cobrar_por_equipo(payload):
    print(payload)
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        id_equipo, tiempo_arriendo = payload.split(',')
        tiempo_arriendo = int(tiempo_arriendo)
        
        # Obtener la tarifa del equipo
        query = f"SELECT tarifa FROM Equipos WHERE id={id_equipo}"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            tarifa = result[0]
            monto = tarifa * tiempo_arriendo
            return f"COBROK,{monto}"
        else:
            return "COBRONK, Equipo no encontrado"
    except Exception as e:
        return f"COBRONK,Error: {str(e)}"
    finally:
        cursor.close()
        db_connection.close()

try:
    message = b'00010sinitCOBRO'
    print('sending {!r}'.format(message))
    sock.sendall(message)
    sinit = 1
    while True:
        print("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
        print("Processing ...")
        print('received {!r}'.format(data))
        if sinit == 1:
            sinit = 0
            print('Received sinit answer')
        else:
            print("Send answer")
            data = data.decode()[5:]  # Remove the first 5 characters (service name)
            response = handle_request(data)
            response_message = f"{len(response):05}{response}".encode()
            print('sending {!r}'.format(response_message))
            sock.sendall(response_message)
finally:
    print('closing socket')
    sock.close()
