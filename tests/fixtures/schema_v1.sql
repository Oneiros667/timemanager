CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    display_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    notes TEXT NOT NULL DEFAULT '',
    state TEXT NOT NULL DEFAULT 'inbox'
        CHECK (state IN ('inbox', 'ready', 'active', 'done', 'dropped')),
    planned_date TEXT,
    is_highlight INTEGER NOT NULL DEFAULT 0 CHECK (is_highlight IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE INDEX tasks_user_state
    ON tasks (user_id, state, planned_date);

CREATE UNIQUE INDEX tasks_one_active_highlight
    ON tasks (user_id, planned_date)
    WHERE is_highlight = 1 AND state NOT IN ('done', 'dropped');
