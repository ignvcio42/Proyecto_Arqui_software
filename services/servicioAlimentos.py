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
    payload = data[5:]
    if action == "CODAA":
        return añadir_alimento(payload)
    elif action == "CODEA":
        return eliminar_alimento(payload)
    elif action == "CODMA":
        return modificar_alimento(payload)
    elif action == "CODIA":
        return obtener_info_alimento(payload)
    elif action == "CODIT":
        return obtener_info_todos_alimentos()
    else:
        return "ALIMENK, Acción inválida"

def añadir_alimento(payload):
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        nombre, precio, stock = payload.split(',')
        query = f"INSERT INTO Alimentos (nombre, precio, stock) VALUES ('{nombre}', {precio}, {stock})"
        cursor.execute(query)
        db_connection.commit()
        return f"ALIMEOK,{cursor.lastrowid}"
    except mysql.connector.Error as err:
        return f"ALIMENK, Error: {err}"
    finally:
        cursor.close()
        db_connection.close()

def eliminar_alimento(id_alimento):
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        query = f"DELETE FROM Alimentos WHERE id={id_alimento}"
        cursor.execute(query)
        db_connection.commit()
        if cursor.rowcount == 0:
            return "ERROR, No se encontró el equipo con el ID especificado"
        return "ALIMEOK, Alimento eliminado"
    except mysql.connector.Error as err:
        return f"ALIMENK, Error: {err}"
    finally:
        cursor.close()
        db_connection.close()

def modificar_alimento(payload):
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        id_alimento, nombre, precio, stock = payload.split(',')
        query = f"UPDATE Alimentos SET nombre='{nombre}', precio={precio}, stock={stock} WHERE id={id_alimento}"
        cursor.execute(query)
        db_connection.commit()
        return "ALIMEOK, Alimento modificado"
    except mysql.connector.Error as err:
        return f"ALIMENK, Error: {err}"
    finally:
        cursor.close()
        db_connection.close()

def obtener_info_alimento(id_alimento):
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        query = f"SELECT * FROM Alimentos WHERE id={id_alimento}"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            response = f"ALIMEOK,{result[0]},{result[1]},{result[2]},{result[3]}"
        else:
            response = "ALIMENK, Alimento no encontrado"
        return response
    finally:
        cursor.close()
        db_connection.close()

def obtener_info_todos_alimentos():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        query = "SELECT * FROM Alimentos"
        cursor.execute(query)
        results = cursor.fetchall()
        response = "ALIMEOK," + "|".join([f"{row[0]},{row[1]},{row[2]},{row[3]}" for row in results])
        return response
    finally:
        cursor.close()
        db_connection.close()

try:
    message = b'00010sinitALIME'
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
