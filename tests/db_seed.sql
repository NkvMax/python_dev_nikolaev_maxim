USE db1;

-- Вставка пользователей
INSERT INTO users (login, email) VALUES
  ('vladimir', 'vladimir@example.com'),
  ('yanina',   'yanina@example.com'),
  ('natalya',  'natalya@example.com');

-- Вставка блогов
-- ** каждый блог принадлежит одному пользователю
INSERT INTO blog (owner_id, name, description) VALUES
  (
    (SELECT id FROM users WHERE login = 'vladimir' LIMIT 1),
    'Блог Владимира о Недвижимости',
    'Обсуждаем новостройки, ЖК, отзывы.'
  ),
  (
    (SELECT id FROM users WHERE login = 'yanina' LIMIT 1),
    'Янина: Жизнь и Квартиры',
    'Мои обзоры и заметки о новом жилье.'
  ),
  (
    (SELECT id FROM users WHERE login = 'natalya' LIMIT 1),
    'Наталья: Обзоры ЖК',
    'Рассказываю о планировках, достопримечательностях и инфраструктуре.'
  );

-- Вставка постов
-- ** каждый пост — определенный ЖК, привязанный к пользователю и блогу
INSERT INTO post (header, text, author_id, blog_id) VALUES
  (
    'ЖК Эдельвейс',
    'Описание ЖК Эдельвейс, вид на море, узкий проезд',
    (SELECT id FROM users WHERE login='vladimir' LIMIT 1),
    (SELECT id FROM blog WHERE name='Блог Владимира о Недвижимости' LIMIT 1)
  ),
  (
    'ЖК Ромашка',
    'Описание ЖК Ромашка, удобный район, рядом Калина Молл',
    (SELECT id FROM users WHERE login='yanina' LIMIT 1),
    (SELECT id FROM blog WHERE name='Янина: Жизнь и Квартиры' LIMIT 1)
  ),
  (
    'ЖК Ландыши',
    'Описание ЖК Ландыши, близость к центру, фитнес-зал, детские площадки',
    (SELECT id FROM users WHERE login='natalya' LIMIT 1),
    (SELECT id FROM blog WHERE name='Наталья: Обзоры ЖК' LIMIT 1)
  );

USE db2;

-- Справочник space_type
INSERT INTO space_type (name) VALUES
  ('global'),
  ('blog'),
  ('post');

-- Справочник event_type
INSERT INTO event_type (name) VALUES
  ('login'),
  ('comment'),
  ('create_post'),
  ('delete_post'),
  ('logout');


-- Логи для Владимира
INSERT INTO logs (`datetime`, user_id, space_type_id, event_type_id, object_id)
VALUES
  -- Владимир заходит в систему
  ('2025-03-01 08:00:00', 1,
    (SELECT id FROM space_type WHERE name='global' LIMIT 1),
    (SELECT id FROM event_type WHERE name='login' LIMIT 1),
    NULL
  ),
  -- Владимир комментирует пост ЖК Эдельвейс
  ('2025-03-01 08:05:00', 1,
    (SELECT id FROM space_type WHERE name='post' LIMIT 1),
    (SELECT id FROM event_type WHERE name='comment' LIMIT 1),
    (SELECT p.id FROM db1.post p WHERE p.header='ЖК Эдельвейс' LIMIT 1)
  ),
  -- Владимир выходит из системы
  ('2025-03-01 09:00:00', 1,
    (SELECT id FROM space_type WHERE name='global' LIMIT 1),
    (SELECT id FROM event_type WHERE name='logout' LIMIT 1),
    NULL
  );

-- Логи для Янины
INSERT INTO logs (`datetime`, user_id, space_type_id, event_type_id, object_id)
VALUES
  -- Янина заходит в систему
  ('2025-03-02 10:30:00', 2,
    (SELECT id FROM space_type WHERE name='global' LIMIT 1),
    (SELECT id FROM event_type WHERE name='login' LIMIT 1),
    NULL
  ),
  -- Янина комментирует пост ЖК Ромашка
  ('2025-03-02 10:40:00', 2,
    (SELECT id FROM space_type WHERE name='post' LIMIT 1),
    (SELECT id FROM event_type WHERE name='comment' LIMIT 1),
    (SELECT p.id FROM db1.post p WHERE p.header='ЖК Ромашка' LIMIT 1)
  ),
  -- Янина выходит
  ('2025-03-02 11:00:00', 2,
    (SELECT id FROM space_type WHERE name='global' LIMIT 1),
    (SELECT id FROM event_type WHERE name='logout' LIMIT 1),
    NULL
  );

-- Логи для Натальи
INSERT INTO logs (`datetime`, user_id, space_type_id, event_type_id, object_id)
VALUES
  -- Наталья заходит
  ('2025-03-03 07:00:00', 3,
    (SELECT id FROM space_type WHERE name='global' LIMIT 1),
    (SELECT id FROM event_type WHERE name='login' LIMIT 1),
    NULL
  ),
  -- Наталья комментирует пост ЖК Ландыши
  ('2025-03-03 07:15:00', 3,
    (SELECT id FROM space_type WHERE name='post' LIMIT 1),
    (SELECT id FROM event_type WHERE name='comment' LIMIT 1),
    (SELECT p.id FROM db1.post p WHERE p.header='ЖК Ландыши' LIMIT 1)
  ),
  -- Наталья выходит
  ('2025-03-03 08:00:00', 3,
    (SELECT id FROM space_type WHERE name='global' LIMIT 1),
    (SELECT id FROM event_type WHERE name='logout' LIMIT 1),
    NULL
  );
