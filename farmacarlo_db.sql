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
-- Estructura de tabla para la tabla `productos_mysql`
--

CREATE TABLE `productos_mysql` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `productos_mysql`
--

INSERT INTO `productos_mysql` (`id`, `nombre`, `cantidad`, `precio`) VALUES
(1, 'Femen ', 15, 4.20),
(2, 'Migraflash', 23, 5.00),
(3, 'Diabaid', 12, 21.00),
(4, 'Fanter Comprimidos', 10, 42.00),
(5, 'Acteric Comprimidos', 20, 9.10),
(6, 'Algivex', 18, 8.40),
(7, 'Alfrom Comprimidos', 11, 22.40),
(8, 'Analgan Rapid', 18, 14.50),
(9, 'Apronax Capsulas Liquidas ', 19, 27.00),
(10, 'Apronax Tabletas ', 22, 11.00),
(11, 'Artrichine', 14, 1.50),
(12, 'Astros', 10, 22.20),
(13, 'Astrosamin', 15, 22.20),
(14, 'Aspirina Advance', 12, 12.00),
(15, 'Beralmat', 14, 9.20),
(16, 'Berifem', 11, 3.40),
(17, 'Bonfiest', 16, 14.40),
(18, 'Cartidol Plus', 10, 23.10),
(19, 'Cefanorm', 12, 24.00),
(20, 'Celeridan ', 20, 15.40),
(21, 'Acrofibrato', 22, 17.10),
(22, 'Aldactone', 12, 8.10),
(23, 'Bilidren Enzimático', 17, 10.50),
(24, 'Buscapina', 8, 8.00),
(25, 'Digesta', 10, 10.60),
(26, 'Digestotal Biliar', 12, 22.20),
(27, 'Qg5', 7, 23.40);

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
(1, 'Tabata Domenica Cifuentes Ponce', 'tabatacifuentes@gmail.com', '1234');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `productos_mysql`
--
ALTER TABLE `productos_mysql`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `productos_mysql`
--
ALTER TABLE `productos_mysql`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
