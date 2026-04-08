-- Estructura de la base de datos para el Sistema Farmacarlo
CREATE DATABASE IF NOT EXISTS farmacarlo_db;
USE farmacarlo_db;

-- 1. Tabla de Categorías (Entidad Relacionada)
CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(50) NOT NULL
);

-- 2. Tabla de Proveedores (Entidad Relacionada)
CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre_proveedor VARCHAR(100) NOT NULL
);

-- 3. Tabla de Productos (Entidad Principal con Llaves Foráneas)
CREATE TABLE productos_mysql (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    id_categoria INT,
    id_proveedor INT,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
);

-- 4. Tabla de Usuarios (Para Autenticación)
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

-- Inserción de datos maestros para pruebas iniciales
INSERT INTO categorias (nombre_categoria) VALUES ('Analgésicos'), ('Antibióticos'), ('Vitaminas');
INSERT INTO proveedores (nombre_proveedor) VALUES ('Laboratorios Alfa'), ('Distribuidora Delta');
INSERT INTO usuarios (nombre, email, password) VALUES ('Admin', 'admin@farmacarlo.com', 'admin123');