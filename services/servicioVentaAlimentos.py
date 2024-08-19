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
    if action == "CODAC":
        return vender_alimento(data[5:])
    else:
        return "VENALNK, Acción inválida"

def vender_alimento(payload):
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root_password",
            database="CyberCafeManager"
        )
        cursor = db_connection.cursor()
        
        rut_usuario, nombre_alimento, cantidad = payload.split(',')
        cantidad = int(cantidad)
        
        # Obtener información del alimento
        query = f"SELECT id, precio, stock FROM Alimentos WHERE nombre='{nombre_alimento}'"
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)
        if result:
            id_alimento, precio, stock = result
            if stock < cantidad:
                return "VENALNK,Stock insuficiente"
            
            # Calcular total de la venta
            total = precio * cantidad
            
            # Actualizar el inventario
            nuevo_stock = stock - cantidad
            update_query = f"UPDATE Alimentos SET stock={nuevo_stock} WHERE id={id_alimento}"
            cursor.execute(update_query)
            
            # Registrar la venta
            insert_query = f"INSERT INTO VentasAlimentos (rut_usuario, id_alimento, fecha, total) VALUES ({rut_usuario}, {id_alimento}, NOW(), {total})"
            cursor.execute(insert_query)
            db_connection.commit()
            
            return f"VENALOK,{total}"
        else:
            return "VENALNK,Alimento no encontrado"
    except Exception as e:
        return f"VENALNK,Error: {str(e)}"
    finally:
        cursor.close()
        db_connection.close()

try:
    message = b'00010sinitVENAL'
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
