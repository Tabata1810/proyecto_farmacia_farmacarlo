-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `farmacarlo_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre_categoria` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nombre_categoria`) VALUES
(1, 'Medicamentos_Antibióticos_Antiinfecciosos'),
(2, 'Higiene_Cuidado Personal'),
(3, 'Salud_Intima'),
(4, 'Medicamentos_Analgésicos_Antiinflamatorios'),
(5, 'Medicamentos_Digestivos'),
(6, 'Suplementos_Vitaminas'),
(7, 'Medicamentos_Cardiovasculares'),
(8, 'Medicamentos_Antialergicos_Respiratorios');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `cedula` varchar(15) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre`, `cedula`, `telefono`, `correo`) VALUES
(4, 'Maria Belen ', '1759255558', '0998525555', 'belen@gmail.com'),
(7, 'Juan', '1756826845', '0985555555', 'juan@gmai.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_ventas`
--

CREATE TABLE `detalle_ventas` (
  `id_detalle` int(11) NOT NULL,
  `id_venta` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos_mysql`
--

CREATE TABLE `productos_mysql` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `productos_mysql`
--

INSERT INTO `productos_mysql` (`id`, `nombre`, `cantidad`, `precio`, `id_categoria`) VALUES
(1, 'Femen ', 15, 4.20, 4),
(2, 'Migraflash', 23, 5.00, 4),
(4, 'Fanter Comprimidos', 10, 42.00, 1),
(5, 'Acteric Comprimidos', 20, 9.10, 1),
(6, 'Algivex', 18, 8.40, 4),
(7, 'Altrom Comprimidos', 11, 22.40, 4),
(8, 'Analgan Rapid', 18, 14.50, 4),
(9, 'Apronax Capsulas Liquidas ', 19, 27.00, 4),
(10, 'Apronax Tabletas ', 22, 11.00, 4),
(11, 'Jabon intimo mujer', 14, 1.50, 3),
(12, 'Astros', 10, 22.20, 6),
(13, 'Astrosamin', 15, 22.20, 6),
(14, 'Aspirina Advance', 12, 12.00, 4),
(15, 'Beralmat', 14, 9.20, 8),
(16, 'Berifem', 11, 3.40, 3),
(17, 'Bonfiest', 16, 14.40, 4),
(18, 'Cartidol Plus', 10, 23.10, 7),
(20, 'Celeridan ', 20, 15.40, 8),
(21, 'Acrofibrato', 22, 17.10, 7),
(22, 'Aldactone', 12, 8.10, 7),
(23, 'Bilidren Enzimático', 17, 10.50, 5),
(24, 'Buscapina', 8, 8.00, 5),
(25, 'Digesta', 10, 10.60, 5),
(26, 'Digestotal Biliar', 12, 22.20, 5),
(30, 'Pasta dental ', 15, 2.00, 2),
(31, 'Toallas Humedas', 20, 2.00, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id_proveedor` int(11) NOT NULL,
  `nombre_empresa` varchar(100) NOT NULL,
  `contacto_vendedor` varchar(100) DEFAULT NULL,
  `telefono_proveedor` varchar(15) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `nombre_empresa`, `contacto_vendedor`, `telefono_proveedor`, `direccion`, `telefono`, `correo`) VALUES
(5, 'Mediya', 'Cesar Bastidas ', '0998525555', 'Quito', NULL, 'mediya@gmail.com'),
(7, 'Farmaenlace', 'Carlos Medina', '0985555555', 'Quito', NULL, 'Farmaenlace@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `email`, `password`) VALUES
(1, 'Belen Andrea Bastidas Paredes', 'Belen@gmail.com', '12345'),
(2, 'Carlo', 'admin@correo.com', '1234'),
(3, 'Alexandra Ponce', 'alexandra@gmail.com', '123'),
(4, 'Tabata Cifuentes', 'tabatacifuentes@gmail.com', '123'),
(5, 'Carlos Medina', 'carlos@gmail.com', '123');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id_venta` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `total` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id_venta`, `id_cliente`, `fecha`, `total`) VALUES
(2, 4, '2026-04-09 08:13:54', 7.98),
(3, 4, '2026-04-09 10:04:46', 5.00),
(4, 4, '2026-04-09 13:00:51', 23.10);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `cedula` (`cedula`);

--
-- Indices de la tabla `detalle_ventas`
--
ALTER TABLE `detalle_ventas`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `fk_ventas_cabecera` (`id_venta`);

--
-- Indices de la tabla `productos_mysql`
--
ALTER TABLE `productos_mysql`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_categoria` (`id_categoria`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id_proveedor`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id_venta`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `detalle_ventas`
--
ALTER TABLE `detalle_ventas`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos_mysql`
--
ALTER TABLE `productos_mysql`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalle_ventas`
--
ALTER TABLE `detalle_ventas`
  ADD CONSTRAINT `fk_ventas_cabecera` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`) ON DELETE CASCADE;

--
-- Filtros para la tabla `productos_mysql`
--
ALTER TABLE `productos_mysql`
  ADD CONSTRAINT `fk_categoria` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
