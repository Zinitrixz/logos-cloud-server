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
