-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-11-2024 a las 03:25:57
-- Versión del servidor: 8.3.0
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db_autos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comentario_publicacion`
--

CREATE TABLE `comentario_publicacion` (
  `Id_Comentario` int NOT NULL,
  `Id_Publicacion` int DEFAULT NULL,
  `Comentario` text CHARACTER SET latin1 COLLATE latin1_swedish_ci,
  `Fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comentario_publicacion`
--

INSERT INTO `comentario_publicacion` (`Id_Comentario`, `Id_Publicacion`, `Comentario`, `Fecha`) VALUES
(15, 20, 'hola bro', '2024-09-29 16:47:39'),
(17, 20, 'gfrgreg', '2024-10-15 16:51:08'),
(20, 20, 'rtytyty', '2024-10-15 17:12:57'),
(21, 20, 'lkilil', '2024-10-15 17:13:57'),
(33, 26, 'hola', '2024-11-26 18:45:36'),
(34, 26, 'hola', '2024-11-26 18:46:14'),
(35, 26, 'hola', '2024-11-26 18:48:05'),
(36, 26, 'hola', '2024-11-26 18:48:24'),
(38, 26, 'aa', '2024-11-26 18:59:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `likes`
--

CREATE TABLE `likes` (
  `id_Like` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `Id_Publicacion` int DEFAULT NULL,
  `like_status` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `likes`
--

INSERT INTO `likes` (`id_Like`, `user_id`, `Id_Publicacion`, `like_status`) VALUES
(19, 10, 20, 1),
(21, 7, 20, 1),
(48, 8, 20, 1),
(86, 8, 41, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `messages`
--

CREATE TABLE `messages` (
  `id_Mensaje` int NOT NULL,
  `user_sender` int NOT NULL,
  `user_receiver` int NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `messages`
--

INSERT INTO `messages` (`id_Mensaje`, `user_sender`, `user_receiver`, `message`, `timestamp`) VALUES
(11, 8, 7, 'Hola, Estoy Interesado', '2024-11-11 11:38:36'),
(12, 11, 8, 'Hola, Estoy Interesado', '2024-11-20 07:57:50'),
(13, 11, 8, 'hola', '2024-11-20 07:58:05'),
(14, 8, 11, 'hola', '2024-11-20 07:58:37'),
(15, 11, 8, 'como estas', '2024-11-20 07:59:46'),
(16, 8, 8, 'hola', '2024-11-20 09:00:40'),
(17, 8, 7, 'hola', '2024-11-22 09:20:51'),
(18, 7, 8, 'ok', '2024-11-22 09:44:49'),
(19, 8, 8, 'va', '2024-11-22 09:45:34'),
(20, 8, 8, 'hola bro', '2024-11-22 09:47:46'),
(21, 7, 8, 'hola', '2024-11-22 09:49:17'),
(22, 8, 7, 'hola', '2024-11-22 09:49:31'),
(23, 8, 7, 'aaa', '2024-11-22 09:50:10'),
(24, 7, 8, 'hhh', '2024-11-22 09:50:14'),
(25, 8, 8, 'gtf', '2024-11-22 10:04:25'),
(26, 8, 8, 'alo', '2024-11-22 10:04:43'),
(27, 8, 8, 'heelo', '2024-11-22 10:05:00'),
(28, 7, 8, 'ok', '2024-11-22 10:08:18'),
(29, 8, 7, 'fokc', '2024-11-22 10:09:16'),
(30, 7, 8, 'jj', '2024-11-22 10:11:56'),
(31, 8, 7, 'kk', '2024-11-22 10:12:08'),
(32, 7, 8, 'hola', '2024-11-28 21:39:01'),
(33, 8, 7, 'como estas', '2024-11-28 21:41:00'),
(34, 8, 10, 'Hola, Estoy Interesado', '2024-11-29 09:35:37'),
(35, 10, 8, 'hola', '2024-11-29 09:37:27');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `publicacion_vehiculos`
--

CREATE TABLE `publicacion_vehiculos` (
  `Id_Publicacion` int NOT NULL,
  `nombre_vehiculo` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `precio` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `descripcion` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `imgVehiculo` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `imgVehiculo2` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `latitud` float NOT NULL,
  `longitud` float NOT NULL,
  `maps_url` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `map_image` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `user_id` int NOT NULL,
  `marca` text COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `publicacion_vehiculos`
--

INSERT INTO `publicacion_vehiculos` (`Id_Publicacion`, `nombre_vehiculo`, `precio`, `descripcion`, `imgVehiculo`, `imgVehiculo2`, `latitud`, `longitud`, `maps_url`, `map_image`, `user_id`, `marca`) VALUES
(20, 'Subaru brz', '9500', 'se vende subaru brz', 'Subaru_brz_1.jpg', 'Subaru_brz_2.jpg', 13.3384, -88.4571, 'https://www.google.com/maps?q=13.3384204,-88.4570837', 'https://maps.googleapis.com/maps/api/staticmap?center=13.3384204,-88.4570837&zoom=15&size=400x200&maptype=roadmap&markers=color:red%7Clabel:S%7C13.3384204,-88.4570837&key=AIzaSyCO764uG2EnYUWrmDsgRwWSGPU51nRS1Nc', 8, ''),
(26, 'Toyota gt86', '8000', 'se vende', 'Toyota_gt86_1.jpg', 'Toyota_gt86_2.jpg', 13.3384, -88.4571, 'https://www.google.com/maps?q=13.3384208,-88.4570888', 'https://maps.googleapis.com/maps/api/staticmap?center=13.3384208,-88.4570888&zoom=15&size=400x200&maptype=roadmap&markers=color:red%7Clabel:S%7C13.3384208,-88.4570888&key=AIzaSyCO764uG2EnYU WrmDsgRwWSGPU51nRS1Nc', 11, 'Toyota'),
(41, 'BMW M4 competition', '22500', 'Vendo BMW M4 competition nuevo.', 'BMW_M4_competition_1.jpg', 'BMW_M4_competition_2.jpg', 13.3384, -88.4571, 'https://www.google.com/maps?q=13.3384186,-88.4570972', 'https://maps.googleapis.com/maps/api/staticmap?center=13.3384186,-88.4570972&zoom=15&size=400x200&maptype=roadmap&markers=color:red%7Clabel:S%7C13.3384186,-88.4570972&key=AIzaSyCO764uG2EnYU WrmDsgRwWSGPU51nRS1Nc', 10, 'BMW');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `NombreCompleto` varchar(100) NOT NULL,
  `NumeroTelefono` varchar(9) NOT NULL,
  `imgPerfilUsuario` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `imgFondoUsuario` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `NombreCompleto`, `NumeroTelefono`, `imgPerfilUsuario`, `imgFondoUsuario`) VALUES
(7, 'Juanito@gmail.com', '123', 'Juan Diaz', '75678987', '/static/imagenes/honda_adelante.jpeg', NULL),
(8, 'gerson@gmail.com', '123', 'Gerson Geovanni Guevara Rivas', '7732-4545', '/static/imagenes/silvia.jpg', '/static/imagenes/hellcat.jpg'),
(9, 'juanantonio@gmail.com', 'juanito123', 'Juan Antonio Diaz', '77984453', NULL, NULL),
(10, 'William@gmail.com', 'Wiliam321', 'William Alexander Aparicio Zelaya', '74567643', NULL, NULL),
(11, 'rolandodaniel@gmail.com', 'rolando12345', 'Rolando Iglesias', '78543221', '/static/imagenes/challenger_str.jpg', '/static/imagenes/hellcat.jpg');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `comentario_publicacion`
--
ALTER TABLE `comentario_publicacion`
  ADD PRIMARY KEY (`Id_Comentario`),
  ADD KEY `id_publicacion` (`Id_Publicacion`);

--
-- Indices de la tabla `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`id_Like`),
  ADD UNIQUE KEY `user_id` (`user_id`,`Id_Publicacion`),
  ADD KEY `likes_ibfk_2` (`Id_Publicacion`);

--
-- Indices de la tabla `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id_Mensaje`),
  ADD KEY `user_sender` (`user_sender`),
  ADD KEY `user_receiver` (`user_receiver`);

--
-- Indices de la tabla `publicacion_vehiculos`
--
ALTER TABLE `publicacion_vehiculos`
  ADD PRIMARY KEY (`Id_Publicacion`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `comentario_publicacion`
--
ALTER TABLE `comentario_publicacion`
  MODIFY `Id_Comentario` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `likes`
--
ALTER TABLE `likes`
  MODIFY `id_Like` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=88;

--
-- AUTO_INCREMENT de la tabla `messages`
--
ALTER TABLE `messages`
  MODIFY `id_Mensaje` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT de la tabla `publicacion_vehiculos`
--
ALTER TABLE `publicacion_vehiculos`
  MODIFY `Id_Publicacion` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `comentario_publicacion`
--
ALTER TABLE `comentario_publicacion`
  ADD CONSTRAINT `comentario_publicacion_ibfk_1` FOREIGN KEY (`Id_Publicacion`) REFERENCES `publicacion_vehiculos` (`Id_Publicacion`) ON DELETE CASCADE;

--
-- Filtros para la tabla `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`Id_Publicacion`) REFERENCES `publicacion_vehiculos` (`Id_Publicacion`) ON DELETE CASCADE;

--
-- Filtros para la tabla `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`user_sender`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`user_receiver`) REFERENCES `users` (`user_id`);

--
-- Filtros para la tabla `publicacion_vehiculos`
--
ALTER TABLE `publicacion_vehiculos`
  ADD CONSTRAINT `publicacion_vehiculos_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
