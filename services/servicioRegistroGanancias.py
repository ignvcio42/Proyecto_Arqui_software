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
    if action == "CODAE":
        return obtener_ganancias_arriendo(data[5:])
    elif action == "CODVA":
        return obtener_ganancias_ventas(data[5:])
    else:
        return "REGANNK, Acción inválida"

def obtener_ganancias_arriendo(payload):
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        fecha_inicio, fecha_fin = payload.split(',')
        query = f"SELECT fecha, monto FROM Arriendos WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'"
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            ganancias = "|".join([f"{row[0]},{row[1]}" for row in results])
            return f"REGANOK,{ganancias}"
        else:
            return "REGANNK, No hay ganancias en el intervalo proporcionado"
    except Exception as e:
        return f"REGANNK,Error: {str(e)}"
    finally:
        cursor.close()
        db_connection.close()

def obtener_ganancias_ventas(payload):
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        fecha_inicio, fecha_fin = payload.split(',')
        query = f"SELECT fecha, total FROM VentasAlimentos WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'"
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            ganancias = "|".join([f"{row[0]},{row[1]}" for row in results])
            return f"REGANOK,{ganancias}"
        else:
            return "REGANNK, No hay ganancias en el intervalo proporcionado"
    except Exception as e:
        return f"REGANNK,Error: {str(e)}"
    finally:
        cursor.close()
        db_connection.close()

try:
    message = b'00010sinitREGAN'
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
