-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Май 15 2026 г., 05:57
-- Версия сервера: 10.4.32-MariaDB
-- Версия PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `hotel_db`
--

-- --------------------------------------------------------

--
-- Структура таблицы `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `guest_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `check_in_date` date NOT NULL,
  `check_out_date` date NOT NULL,
  `status` varchar(50) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `bookings`
--

INSERT INTO `bookings` (`id`, `guest_id`, `room_id`, `check_in_date`, `check_out_date`, `status`, `total_price`, `created_at`) VALUES
(1, 1, 1, '2026-05-22', '2026-05-25', 'checked_out', 9000.00, '2026-05-14 17:33:49'),
(2, 1, 1, '2026-05-16', '2026-05-20', 'checked_out', 12000.00, '2026-05-14 17:35:43'),
(3, 1, 1, '2026-05-17', '2026-05-21', 'checked_out', 12000.00, '2026-05-14 17:37:19'),
(4, 1, 3, '2026-05-16', '2026-05-20', 'checked_out', 20000.00, '2026-05-14 17:44:07'),
(5, 1, 4, '2026-05-25', '2026-05-30', 'checked_out', 30000.00, '2026-05-14 18:00:22'),
(6, 2, 1, '2026-05-20', '2026-05-21', 'checked_out', 3000.00, '2026-05-14 18:01:43'),
(7, 1, 1, '2026-05-21', '2026-05-24', 'checked_in', 9000.00, '2026-05-15 08:32:41');

-- --------------------------------------------------------

--
-- Структура таблицы `booking_services`
--

CREATE TABLE `booking_services` (
  `id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price_at_booking` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `cleaning_tasks`
--

CREATE TABLE `cleaning_tasks` (
  `id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `assigned_to_id` int(11) DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `cleaning_tasks`
--

INSERT INTO `cleaning_tasks` (`id`, `room_id`, `assigned_to_id`, `status`, `created_at`, `completed_at`) VALUES
(1, 1, NULL, 'done', '2026-05-14 17:59:29', '2026-05-14 17:59:36'),
(2, 1, NULL, 'done', '2026-05-14 18:14:37', '2026-05-14 18:15:06'),
(3, 2, NULL, 'done', '2026-05-14 18:14:56', '2026-05-14 18:15:07'),
(4, 4, NULL, 'done', '2026-05-14 18:14:58', '2026-05-14 18:15:07'),
(5, 3, NULL, 'done', '2026-05-14 18:14:59', '2026-05-14 18:15:07'),
(6, 1, NULL, 'done', '2026-05-14 18:15:23', '2026-05-14 18:26:32'),
(7, 2, NULL, 'done', '2026-05-14 18:15:24', '2026-05-14 18:26:33');

-- --------------------------------------------------------

--
-- Структура таблицы `guests`
--

CREATE TABLE `guests` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `passport_number` varchar(50) NOT NULL,
  `passport_issued_by` varchar(200) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `preferences` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `guests`
--

INSERT INTO `guests` (`id`, `user_id`, `passport_number`, `passport_issued_by`, `birth_date`, `preferences`) VALUES
(1, 3, '', NULL, NULL, ''),
(2, 4, '', NULL, NULL, '');

-- --------------------------------------------------------

--
-- Структура таблицы `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `roles`
--

INSERT INTO `roles` (`id`, `name`) VALUES
(1, 'Администратор'),
(2, 'Горничная'),
(4, 'Гость'),
(3, 'Управляющий');

-- --------------------------------------------------------

--
-- Структура таблицы `rooms`
--

CREATE TABLE `rooms` (
  `id` int(11) NOT NULL,
  `room_number` varchar(10) NOT NULL,
  `room_type_id` int(11) NOT NULL,
  `capacity` int(11) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `rooms`
--

INSERT INTO `rooms` (`id`, `room_number`, `room_type_id`, `capacity`, `status`) VALUES
(1, '101', 1, 4, 'occupied'),
(2, '102', 2, 4, 'available'),
(3, '103', 3, 4, 'available'),
(4, '104', 4, 6, 'available');

-- --------------------------------------------------------

--
-- Структура таблицы `room_types`
--

CREATE TABLE `room_types` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `base_price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `room_types`
--

INSERT INTO `room_types` (`id`, `name`, `description`, `base_price`) VALUES
(1, 'Стандарт', NULL, 3000.00),
(2, 'Люкс', NULL, 8000.00),
(3, 'Полулюкс', NULL, 5000.00),
(4, 'Семейный', NULL, 6000.00);

-- --------------------------------------------------------

--
-- Структура таблицы `services`
--

CREATE TABLE `services` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `category` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `services`
--

INSERT INTO `services` (`id`, `name`, `price`, `category`) VALUES
(1, 'Завтрак', 500.00, 'meal'),
(2, 'Обед', 700.00, 'meal'),
(3, 'Ужин', 800.00, 'meal'),
(4, 'Спа-процедура', 2500.00, 'spa'),
(5, 'Трансфер из аэропорта', 1500.00, 'transfer');

-- --------------------------------------------------------

--
-- Структура таблицы `stays`
--

CREATE TABLE `stays` (
  `id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `guest_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `check_in_time` datetime DEFAULT NULL,
  `check_out_time` datetime DEFAULT NULL,
  `total_amount` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `stays`
--

INSERT INTO `stays` (`id`, `booking_id`, `guest_id`, `room_id`, `check_in_time`, `check_out_time`, `total_amount`) VALUES
(1, 1, 1, 1, '2026-05-14 18:14:32', '2026-05-14 18:14:37', 9000.00),
(2, 2, 1, 2, '2026-05-14 18:14:44', '2026-05-14 18:14:56', 12000.00),
(3, 3, 1, 4, '2026-05-14 18:14:47', '2026-05-14 18:14:58', 12000.00),
(4, 4, 1, 3, '2026-05-14 18:14:49', '2026-05-14 18:14:59', 20000.00),
(5, 5, 1, 1, '2026-05-14 18:15:18', '2026-05-14 18:15:23', 30000.00),
(6, 6, 2, 2, '2026-05-14 18:15:22', '2026-05-14 18:15:24', 3000.00),
(7, 7, 1, 1, '2026-05-15 08:34:00', NULL, 9000.00);

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role_id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role_id`, `first_name`, `last_name`, `phone`, `created_at`, `is_active`) VALUES
(1, 'admin', 'admin@hotel.com', '$2b$12$MwxFzxzS1IDrZSpG28aH0.C98PuQS4l6thHGmEGP5ENAFjdlZ8OgK', 1, 'Администратор', 'Системы', NULL, '2026-05-14 17:23:42', 1),
(2, 'maid', 'maid@hotel.com', '$2b$12$nYURzc5eLrou4FZSe/nQLelnB8zsKGiayUsw0KQOrAJB8gdp0wvae', 2, 'Горничная', 'Служба', NULL, '2026-05-14 17:23:42', 1),
(3, 'guest', 'guest@example.com', '$2b$12$BG9eC2TeZ9cWjxsqA7PPxuk85f2lRHzFFfvOyNCrX92i86yefiJrK', 4, 'Тестовый', 'Гость', NULL, '2026-05-14 17:23:43', 1),
(4, 'ya', 'ya@ya.ya', '$2b$12$635ypnPLHH987BU9CG6G4edih3wXjadtHicHjVZA/Wyr/YZBiHT7e', 4, 'qwerty', 'ty', '+79999999999', '2026-05-14 18:01:28', 1);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bookings_guest_id` (`guest_id`),
  ADD KEY `bookings_room_id` (`room_id`);

--
-- Индексы таблицы `booking_services`
--
ALTER TABLE `booking_services`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bookingservices_booking_id` (`booking_id`),
  ADD KEY `bookingservices_service_id` (`service_id`);

--
-- Индексы таблицы `cleaning_tasks`
--
ALTER TABLE `cleaning_tasks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cleaningtasks_room_id` (`room_id`),
  ADD KEY `cleaningtasks_assigned_to_id` (`assigned_to_id`);

--
-- Индексы таблицы `guests`
--
ALTER TABLE `guests`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `guests_user_id` (`user_id`);

--
-- Индексы таблицы `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `roles_name` (`name`);

--
-- Индексы таблицы `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `rooms_room_number` (`room_number`),
  ADD KEY `rooms_room_type_id` (`room_type_id`);

--
-- Индексы таблицы `room_types`
--
ALTER TABLE `room_types`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `stays`
--
ALTER TABLE `stays`
  ADD PRIMARY KEY (`id`),
  ADD KEY `stays_booking_id` (`booking_id`),
  ADD KEY `stays_guest_id` (`guest_id`),
  ADD KEY `stays_room_id` (`room_id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_username` (`username`),
  ADD UNIQUE KEY `users_email` (`email`),
  ADD KEY `users_role_id` (`role_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `booking_services`
--
ALTER TABLE `booking_services`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `cleaning_tasks`
--
ALTER TABLE `cleaning_tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `guests`
--
ALTER TABLE `guests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `room_types`
--
ALTER TABLE `room_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `services`
--
ALTER TABLE `services`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `stays`
--
ALTER TABLE `stays`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`guest_id`) REFERENCES `guests` (`id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`);

--
-- Ограничения внешнего ключа таблицы `booking_services`
--
ALTER TABLE `booking_services`
  ADD CONSTRAINT `booking_services_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`),
  ADD CONSTRAINT `booking_services_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`);

--
-- Ограничения внешнего ключа таблицы `cleaning_tasks`
--
ALTER TABLE `cleaning_tasks`
  ADD CONSTRAINT `cleaning_tasks_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`),
  ADD CONSTRAINT `cleaning_tasks_ibfk_2` FOREIGN KEY (`assigned_to_id`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `guests`
--
ALTER TABLE `guests`
  ADD CONSTRAINT `guests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `rooms`
--
ALTER TABLE `rooms`
  ADD CONSTRAINT `rooms_ibfk_1` FOREIGN KEY (`room_type_id`) REFERENCES `room_types` (`id`);

--
-- Ограничения внешнего ключа таблицы `stays`
--
ALTER TABLE `stays`
  ADD CONSTRAINT `stays_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`),
  ADD CONSTRAINT `stays_ibfk_2` FOREIGN KEY (`guest_id`) REFERENCES `guests` (`id`),
  ADD CONSTRAINT `stays_ibfk_3` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`);

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
