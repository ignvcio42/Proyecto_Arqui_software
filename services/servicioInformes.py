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
    if action == "CODGG":
        return generar_informe_ganancia_equipos()
    elif action == "CODGU":
        return generar_informe_uso_equipos()
    elif action == "CODGV":
        return generar_informe_ventas()
    else:
        return "INFORNK, Acción inválida"

def generar_informe_ganancia_equipos():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        query = "SELECT tipo, SUM(Arriendos.monto) FROM Arriendos JOIN Equipos ON Arriendos.id_equipo = Equipos.id GROUP BY tipo"
        cursor.execute(query)
        results = cursor.fetchall()
        #print(results)
        montos_por_tipo = "|".join([f"{row[0]},{row[1]}" for row in results])
        monto_total = sum(row[1] for row in results)
        response = f"INFOROK,{montos_por_tipo},{monto_total}"
        return response
    except Exception as e:
        return f"INFORNK,Error: {str(e)}"
    finally:
        cursor.close()
        db_connection.close()

def generar_informe_uso_equipos():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        query = """
        SELECT Equipos.id, Equipos.nombre, SUM(Arriendos.tiempo_arriendo), SUM(Arriendos.monto) 
        FROM Arriendos 
        JOIN Equipos ON Arriendos.id_equipo = Equipos.id 
        GROUP BY Equipos.id, Equipos.nombre
        """
        cursor.execute(query)
        results = cursor.fetchall()
        uso_equipos = "|".join([f"{row[0]},{row[1]},{row[2]},{row[3]}" for row in results])
        response = f"INFOROK,{uso_equipos}"
        return response
    except Exception as e:
        return f"INFORNK,Error: {str(e)}"
    finally:
        cursor.close()
        db_connection.close()

def generar_informe_ventas():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        query = "SELECT Alimentos.id, Alimentos.nombre, SUM(VentasAlimentos.total) FROM VentasAlimentos JOIN Alimentos ON VentasAlimentos.id_alimento = Alimentos.id GROUP BY Alimentos.id, Alimentos.nombre"
        cursor.execute(query)
        results = cursor.fetchall()
        ventas_alimentos = "|".join([f"{row[0]},{row[1]},{row[2]}" for row in results])
        monto_total = sum(row[2] for row in results)
        response = f"INFOROK,{ventas_alimentos},{monto_total}"
        return response
    except Exception as e:
        return f"INFORNK,Error: {str(e)}"
    finally:
        cursor.close()
        db_connection.close()

try:
    message = b'00010sinitINFOR'
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
