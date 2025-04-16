-- USERS
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    mode TEXT DEFAULT 'Basic',
    active_role TEXT DEFAULT 'Guide',
    wincoin INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- INSIGHTS
CREATE TABLE IF NOT EXISTS insights (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    zone TEXT,
    insight TEXT,
    wincoin INTEGER,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- ZION
CREATE TABLE IF NOT EXISTS zion_manifest (
    id SERIAL PRIMARY KEY,
    type TEXT,
    content TEXT,
    created_by TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- ENTITIES / CARDS (из logos_knowledge_core.json)
CREATE TABLE IF NOT EXISTS cards (
    id SERIAL PRIMARY KEY,
    category TEXT,
    zone TEXT,
    title TEXT,
    description TEXT
);

-- TASKS (по зонам)
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    zone TEXT,
    task TEXT
);

-- RITUALS
CREATE TABLE IF NOT EXISTS rituals (
    id SERIAL PRIMARY KEY,
    mode TEXT,
    trigger TEXT,
    name TEXT,
    description TEXT
);

-- ROLES (из logos_roles.json)
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    zone TEXT,
    role TEXT,
    description TEXT
);

-- 1. Уникальные карточки
CREATE TABLE IF NOT EXISTS user_cards (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  card TEXT NOT NULL,
  category TEXT,
  zone TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Мягкая терапия (предложения игроку)
CREATE TABLE IF NOT EXISTS therapy_suggestions (
  id SERIAL PRIMARY KEY,
  username TEXT,
  trauma_area TEXT,
  suggested_method TEXT,
  technique TEXT,
  note TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Лог событий
CREATE TABLE IF NOT EXISTS user_events (
  id SERIAL PRIMARY KEY,
  username TEXT,
  event TEXT,
  metadata TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Список выданных карточек
CREATE TABLE IF NOT EXISTS seen_cards (
  "user" TEXT,
  card TEXT,
  category TEXT,
  timestamp TEXT
);

-- Таблица травм
CREATE TABLE IF NOT EXISTS trauma_map (
  trauma TEXT,
  approach TEXT,
  technique TEXT
);

-- Автосохранённые инсайты
CREATE TABLE IF NOT EXISTS autosaved_insights (
  "user" TEXT,
  insight TEXT,
  zone TEXT,
  wincoin INTEGER,
  message TEXT,
  timestamp TEXT
);

-- Хроника игрока
CREATE TABLE IF NOT EXISTS user_journey (
  "user" TEXT,
  event TEXT,
  zone TEXT,
  detail TEXT,
  timestamp TEXT
);
