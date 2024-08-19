import socket
import sys
import mysql.connector
from datetime import datetime, timedelta

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

def handle_request(data):
    action = data[:5]
    if action == "CODAE":
        return arrendar_equipo(data[5:])
    else:
        return "ARRIENK, Acción inválida"

def arrendar_equipo(payload):
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        rut_usuario, id_equipo, tiempo_arriendo = payload.split(',')
        tiempo_arriendo = int(tiempo_arriendo)
        
        # Verificar si el dispositivo ya está arrendado
        cursor.execute("SELECT fecha_fin FROM Arriendos WHERE id_equipo = %s ORDER BY fecha_fin DESC LIMIT 1", (id_equipo,))
        resultado = cursor.fetchone()
        if resultado:
            fecha_fin_ultima = resultado[0]
            if fecha_fin_ultima > datetime.now():
                return "ARRIENK,Error: Este dispositivo está arrendado!"
        
        # Calcular el monto usando el servicio de cobro
        monto = calcular_cobro(id_equipo, tiempo_arriendo)
        if monto is None:
            return "ARRIENK, Error en cálculo de cobro"
        
        # Calcular fecha_inicio y fecha_fin
        fecha_inicio = datetime.now()
        fecha_fin = fecha_inicio + timedelta(seconds=tiempo_arriendo)
        
        # Formatear fechas para la consulta SQL
        fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
        fecha_fin_str = fecha_fin.strftime('%Y-%m-%d %H:%M:%S')
        
        # Registrar el arriendo en la base de datos
        query = (
            f"INSERT INTO Arriendos (id_equipo, rut_usuario, fecha, tiempo_arriendo, monto, fecha_fin) "
            f"VALUES ({id_equipo}, {rut_usuario}, '{fecha_inicio_str}', {tiempo_arriendo}, {monto}, '{fecha_fin_str}')"
        )
        print(query)  # Agrega esta línea para depuración
        cursor.execute(query)
        db_connection.commit()
        
        # Obtener la fecha de arriendo y fecha_fin registradas
        cursor.execute("SELECT fecha, fecha_fin FROM Arriendos ORDER BY id DESC LIMIT 1")
        resultado = cursor.fetchone()
        fecha = resultado[0]
        fecha_fin = resultado[1]
        
        return f"ARRIEOK,{fecha},{monto},{fecha_fin}"
    except Exception as e:
        return f"ARRIENK,Error: {str(e)}"
    finally:
        cursor.close()
        db_connection.close()

def calcular_cobro(id_equipo, tiempo_arriendo):
    try:
        message = f"{id_equipo},{tiempo_arriendo}"
        response = send_message("COBRO", "CODCP", message)
        
        response_parts = response.split(',')
        print(response)
        if response_parts[0] == "COBROOKK":
            return int(response_parts[1])
        else:
            return None
    except Exception as e:
        print(f"Error connecting to COBRO service: {str(e)}")
        return None

def send_message(service, action, data):
    message_data = f"{action}{data}"
    message = f"{len(message_data):05}{service}{message_data}".encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5000)
    sock.connect(bus_address)
    try:
        sock.sendall(message)
        amount_expected = int(sock.recv(5))
        amount_received = 0
        response = b''
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            response += chunk
    finally:
        sock.close()
    return response.decode()

try:
    message = b'00010sinitARRIE'
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
