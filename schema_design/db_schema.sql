-- Создание отдельной схемы для контента:
CREATE SCHEMA IF NOT EXISTS content;

SET search_path TO content,public;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


-- Карточка кинопроизведения:
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path TEXT,
    rating FLOAT,
    type TEXT not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- Жанры кинопроизведений:
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- Связка жанров и кинопроизведений:
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created_at timestamp with time zone
);

-- Актеры:
CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name TEXT NOT NULL,
    birth_date DATE,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- Связка актеров и кинопроизведений:
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT NOT NULL,
    created_at timestamp with time zone
);

-- Создание уникальново композитного индекса для связки фильм-жанр:
CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre ON genre_film_work (film_work_id, genre_id);

-- Создание уникального композитного индекса для связки фильм-актер:
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_role ON person_film_work (film_work_id, person_id, role);
