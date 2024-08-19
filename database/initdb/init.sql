CREATE DATABASE IF NOT EXISTS CyberCafeManager;

USE CyberCafeManager;

-- Tabla Equipos
CREATE TABLE Equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    tipo TEXT,
    tarifa INT
);

-- Tabla Usuarios
CREATE TABLE Usuarios (
    rut INT PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT
);

-- Tabla Arriendos
CREATE TABLE Arriendos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_equipo INT,
    rut_usuario INT,
    fecha DATETIME, -- Cambiar el tipo de datos a DATETIME
    tiempo_arriendo INT,
    monto INT,
    fecha_fin DATETIME,
    FOREIGN KEY (id_equipo) REFERENCES Equipos(id),
    FOREIGN KEY (rut_usuario) REFERENCES Usuarios(rut)
);

-- Tabla Alimentos
CREATE TABLE Alimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio INT,
    stock INT
);

-- Tabla VentasAlimentos
CREATE TABLE VentasAlimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rut_usuario INT,
    id_alimento INT,
    fecha DATE,
    total INT,
    FOREIGN KEY (rut_usuario) REFERENCES Usuarios(rut),
    FOREIGN KEY (id_alimento) REFERENCES Alimentos(id)
);

-- Tabla Juegos
CREATE TABLE Juegos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    id_equipo INT,
    FOREIGN KEY (id_equipo) REFERENCES Equipos(id)
);