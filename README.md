# Proyecto Arquitectura de Software
## Cyber Café Mánager (CCM)

> [!CAUTION]
> Se requiere instalar mysql-connector-python, mysql, openpyxl


### Iniciar Sistema
- Para iniciar los servicios se pueden iniciar todos con `python services/startServices.py`
- Para iniciar el cliente se utiliza `python cliente.py`
- Es necesario crear la db de la carpeta 'database', se inicia utilizando `docker-compose up -d`, luego si se desea observar dentro de la base de datos, en la consola de el contenedor ingresar `mysql -u root -p` con la contraseña `root_password`

## Servicios

### 1. Servicio de Equipos (`servicioEquipos.py`)

**Funciones Principales:**
- **obtener_info_equipo(id_equipo):** Devuelve información detallada de un equipo específico.
- **obtener_info_todos_equipos():** Proporciona información de todos los equipos, separando los disponibles y arrendados.
- **añadir_equipo(payload):** Añade un nuevo equipo a la base de datos.
- **eliminar_equipo(id_equipo):** Elimina un equipo específico de la base de datos.
- **modificar_equipo(payload):** Modifica los detalles de un equipo específico.

### 2. Servicio de Usuarios (`servicioUsuarios.py`)

**Funciones Principales:**
- **añadir_usuario(payload):** Añade un nuevo usuario a la base de datos.
- **eliminar_usuario(rut):** Elimina un usuario específico de la base de datos.
- **modificar_usuario(payload):** Modifica los detalles de un usuario específico.
- **obtener_info_usuario(rut):** Proporciona información detallada de un usuario específico.
- **obtener_info_todos_usuarios():** Proporciona información de todos los usuarios.

### 3. Servicio de Alimentos (`servicioAlimentos.py`)

**Funciones Principales:**
- **añadir_alimento(payload):** Añade un nuevo alimento a la base de datos.
- **eliminar_alimento(id_alimento):** Elimina un alimento específico de la base de datos.
- **modificar_alimento(payload):** Modifica los detalles de un alimento específico.
- **obtener_info_alimento(id_alimento):** Proporciona información detallada de un alimento específico.
- **obtener_info_todos_alimentos():** Proporciona información de todos los alimentos.

### 4. Servicio de Arriendos (`servicioArriendos.py`)

**Funciones Principales:**
- **arrendar_equipo(payload):** Registra un nuevo arriendo de equipo, verificando la disponibilidad y calculando el costo.

### 5. Servicio de Cobro (`servicioCobro.py`)

**Funciones Principales:**
- **cobrar_por_equipo(payload):** Calcula el costo de arriendo de un equipo basado en la tarifa y el tiempo de arriendo.

### 6. Servicio de Venta de Alimentos (`servicioVentaAlimentos.py`)

**Funciones Principales:**
- **vender_alimento(payload):** Registra una venta de alimentos, actualiza el inventario y calcula el total de la venta.

### 7. Servicio de Registro de Ganancias (`servicioRegistroGanancias.py`)

**Funciones Principales:**
- **obtener_ganancias_arriendo(payload):** Obtiene las ganancias generadas por los arriendos en un intervalo de tiempo específico.
- **obtener_ganancias_ventas(payload):** Obtiene las ganancias generadas por la venta de alimentos en un intervalo de tiempo específico.

### 8. Servicio de Juegos (`servicioJuegos.py`)

**Funciones Principales:**
- **agregar_juego(payload):** Añade un nuevo juego a la base de datos.
- **quitar_juego(id_juego):** Elimina un juego específico de la base de datos.
- **modificar_juego(payload):** Modifica los detalles de un juego específico.
- **obtener_info_juego(id_juego):** Proporciona información detallada de un juego específico.
- **obtener_info_todos_juegos():** Proporciona información de todos los juegos.

### 9. Servicio de Informes (`servicioInformes.py`)

**Funciones Principales:**
- **generar_informe_ganancia_equipos():** Genera un informe de las ganancias por tipo de equipos.
- **generar_informe_uso_equipos():** Genera un informe del uso de equipos.
- **generar_informe_ventas():** Genera un informe de las ventas de alimentos.

## Cliente (`cliente.py`)

El cliente es una aplicación que interactúa con los diferentes servicios del sistema de gestión del Cyber Café. Utiliza un menú de opciones para facilitar la interacción del usuario con el sistema, permitiendo realizar diversas operaciones como gestión de equipos, usuarios, alimentos, juegos, arriendos, ventas, y generación de informes.

### Funciones Principales

#### Gestión de Equipos
- **añadir_equipo(nombre, descripcion, tipo, tarifa):** Añade un nuevo equipo al sistema.
- **eliminar_equipo(id_equipo):** Elimina un equipo específico del sistema.
- **modificar_equipo(id_equipo, nombre, descripcion, tipo, tarifa):** Modifica los detalles de un equipo específico.
- **obtener_info_equipo(id_equipo):** Proporciona información detallada de un equipo específico.
- **obtener_info_todos_equipos():** Proporciona información de todos los equipos, separando los disponibles y arrendados.

#### Gestión de Usuarios
- **añadir_usuario(nombre, rut, email):** Añade un nuevo usuario al sistema.
- **eliminar_usuario(rut):** Elimina un usuario específico del sistema.
- **modificar_usuario():** Modifica los detalles de un usuario específico.
- **obtener_info_usuario(rut):** Proporciona información detallada de un usuario específico.
- **obtener_info_todos_usuarios():** Proporciona información de todos los usuarios.

#### Gestión de Alimentos
- **añadir_alimento(nombre, precio, stock):** Añade un nuevo alimento al sistema.
- **eliminar_alimento(id_alimento):** Elimina un alimento específico del sistema.
- **modificar_alimento(id_alimento, nombre, precio, stock):** Modifica los detalles de un alimento específico.
- **obtener_info_alimento(id_alimento):** Proporciona información detallada de un alimento específico.
- **obtener_info_todos_alimentos():** Proporciona información de todos los alimentos.

#### Gestión de Juegos
- **agregar_juego(nombre, descripcion, id_equipo):** Añade un nuevo juego al sistema.
- **quitar_juego(id_juego):** Elimina un juego específico del sistema.
- **modificar_juego(id_juego, nombre, descripcion, id_equipo):** Modifica los detalles de un juego específico.
- **obtener_info_juego(id_juego):** Proporciona información detallada de un juego específico.
- **obtener_info_todos_juegos():** Proporciona información de todos los juegos.

#### Arriendo de Equipos
- **arrendar_equipo(rut_cliente, id_equipo, tiempo_arriendo):** Registra un nuevo arriendo de equipo, verificando la disponibilidad y calculando el costo.

#### Venta de Alimentos
- **vender_alimento(rut_usuario, nombre_alimento, cantidad):** Registra una venta de alimentos, actualiza el inventario y calcula el total de la venta.

#### Registro de Ganancias
- **obtener_ganancias_arriendo(fecha_inicio, fecha_fin):** Obtiene las ganancias generadas por los arriendos en un intervalo de tiempo específico.
- **obtener_ganancias_ventas(fecha_inicio, fecha_fin):** Obtiene las ganancias generadas por la venta de alimentos en un intervalo de tiempo específico.

#### Generación de Informes
- **generar_informe_ganancia_equipos():** Genera un informe de las ganancias por tipo de equipos.
- **generar_informe_uso_equipos():** Genera un informe del uso de equipos.
- **generar_informe_ventas():** Genera un informe de las ventas de alimentos.

### Menú de Opciones

El cliente presenta un menú de opciones que permite al usuario seleccionar la operación que desea realizar. Las opciones del menú incluyen:
1. Gestión de equipos
2. Gestión de usuarios
3. Gestión de alimentos
4. Gestión de juegos
5. Arriendo de equipos
6. Venta de alimentos
7. Registro de ganancias
8. Informes
9. Salir

Cada una de estas opciones despliega submenús específicos que permiten al usuario interactuar con las diferentes funciones del sistema.
