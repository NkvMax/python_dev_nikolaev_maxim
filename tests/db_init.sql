-- Создаем db1
CREATE DATABASE IF NOT EXISTS db1
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE db1;

-- Таблица users - единый справочник пользователей
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  login VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  UNIQUE KEY uk_users_login (login)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

-- Таблица blog
CREATE TABLE IF NOT EXISTS blog (
  id INT AUTO_INCREMENT PRIMARY KEY,
  owner_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  CONSTRAINT fk_blog_owner
    FOREIGN KEY (owner_id)
    REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

-- Таблица post
CREATE TABLE IF NOT EXISTS post (
  id INT AUTO_INCREMENT PRIMARY KEY,
  header VARCHAR(255) NOT NULL,
  text TEXT,
  author_id INT NOT NULL,
  blog_id INT NOT NULL,
  CONSTRAINT fk_post_author
    FOREIGN KEY (author_id)
    REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_post_blog
    FOREIGN KEY (blog_id)
    REFERENCES blog(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

-- Создаем db2
CREATE DATABASE IF NOT EXISTS db2
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE db2;

-- Таблица space_type
CREATE TABLE IF NOT EXISTS space_type (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

-- Таблица event_type
CREATE TABLE IF NOT EXISTS event_type (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

-- Таблица logs
CREATE TABLE IF NOT EXISTS logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  `datetime` DATETIME NOT NULL,
  user_id INT NOT NULL,
  space_type_id INT NOT NULL,
  event_type_id INT NOT NULL,
  object_id INT DEFAULT NULL,

  CONSTRAINT fk_logs_space_type
    FOREIGN KEY (space_type_id)
    REFERENCES space_type(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  CONSTRAINT fk_logs_event_type
    FOREIGN KEY (event_type_id)
    REFERENCES event_type(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;
