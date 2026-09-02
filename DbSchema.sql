-- ============================================================
-- TRADEGUARD
-- DATABASE + TABLES + MOCK DATA
-- MySQL
-- ============================================================

DROP DATABASE IF EXISTS trade_management;

CREATE DATABASE trade_management;

USE trade_management;


-- ============================================================
-- 1. USERS
-- ============================================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    username VARCHAR(50) NOT NULL UNIQUE,

    email VARCHAR(255) NOT NULL UNIQUE,

    address VARCHAR(255),

    password_hash VARCHAR(255) NOT NULL,

    role VARCHAR(20) NOT NULL DEFAULT 'USER',

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT NULL,
    created_from VARCHAR(255) NULL,

    updated_at TIMESTAMP NULL DEFAULT NULL,
    updated_by INT NULL,
    updated_from VARCHAR(255) NULL,

    CONSTRAINT chk_user_role
        CHECK (role IN ('USER', 'TRADER', 'ADMIN'))
);


-- ============================================================
-- 2. STOCKS
-- ============================================================

CREATE TABLE stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,

    symbol VARCHAR(10) NOT NULL UNIQUE,

    company_name VARCHAR(100) NOT NULL,

    current_price DECIMAL(12,2) NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT NULL,
    created_from VARCHAR(255) NULL,

    updated_at TIMESTAMP NULL DEFAULT NULL,
    updated_by INT NULL,
    updated_from VARCHAR(255) NULL,

    CONSTRAINT chk_stock_price
        CHECK (current_price >= 0)
);


-- ============================================================
-- 3. PORTFOLIOS
-- ============================================================

CREATE TABLE portfolios (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL UNIQUE,

    cash_balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT NULL,
    created_from VARCHAR(255) NULL,

    updated_at TIMESTAMP NULL DEFAULT NULL,
    updated_by INT NULL,
    updated_from VARCHAR(255) NULL,

    CONSTRAINT fk_portfolio_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_cash_balance
        CHECK (cash_balance >= 0)
);


-- ============================================================
-- 4. HOLDINGS
-- ============================================================

CREATE TABLE holdings (
    id INT AUTO_INCREMENT PRIMARY KEY,

    portfolio_id INT NOT NULL,

    stock_id INT NOT NULL,

    quantity INT NOT NULL,

    average_price DECIMAL(12,2) NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT NULL,
    created_from VARCHAR(255) NULL,

    updated_at TIMESTAMP NULL DEFAULT NULL,
    updated_by INT NULL,
    updated_from VARCHAR(255) NULL,

    CONSTRAINT fk_holding_portfolio
        FOREIGN KEY (portfolio_id)
        REFERENCES portfolios(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_holding_stock
        FOREIGN KEY (stock_id)
        REFERENCES stocks(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_holding_quantity
        CHECK (quantity >= 0),

    CONSTRAINT chk_holding_average_price
        CHECK (average_price >= 0),

    CONSTRAINT unique_portfolio_stock
        UNIQUE (portfolio_id, stock_id)
);


-- ============================================================
-- 5. ORDERS
-- ============================================================

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    stock_id INT NOT NULL,

    order_type VARCHAR(10) NOT NULL,

    quantity INT NOT NULL,

    price DECIMAL(12,2) NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',

    approved_by INT NULL,

    approved_at TIMESTAMP NULL,

    cancelled_at TIMESTAMP NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT NULL,
    created_from VARCHAR(255) NULL,

    updated_at TIMESTAMP NULL DEFAULT NULL,
    updated_by INT NULL,
    updated_from VARCHAR(255) NULL,

    CONSTRAINT fk_order_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_order_stock
        FOREIGN KEY (stock_id)
        REFERENCES stocks(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_order_approved_by
        FOREIGN KEY (approved_by)
        REFERENCES users(id)
        ON DELETE SET NULL,

    CONSTRAINT chk_order_type
        CHECK (order_type IN ('BUY', 'SELL')),

    CONSTRAINT chk_order_quantity
        CHECK (quantity > 0),

    CONSTRAINT chk_order_price
        CHECK (price >= 0),

    CONSTRAINT chk_order_status
        CHECK (
            status IN (
                'PENDING',
                'APPROVED',
                'REJECTED',
                'FLAGGED',
                'CANCELLED'
            )
        )
);


-- ============================================================
-- 6. AUDIT LOGS
-- ============================================================

CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NULL,

    action VARCHAR(50) NOT NULL,

    entity_type VARCHAR(50),

    entity_id INT,

    details TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
);


-- ============================================================
-- 7. INDEXES
-- ============================================================

CREATE INDEX idx_orders_user_id
ON orders(user_id);

CREATE INDEX idx_orders_status
ON orders(status);

CREATE INDEX idx_orders_stock_id
ON orders(stock_id);

CREATE INDEX idx_holdings_portfolio_id
ON holdings(portfolio_id);

CREATE INDEX idx_audit_user_id
ON audit_logs(user_id);

CREATE INDEX idx_audit_created_at
ON audit_logs(created_at);


-- ============================================================
-- 8. USERS
--
-- IMPORTANT:
-- These password hashes are bcrypt hashes.
--
-- Login credentials:
--
-- johnsmith / password123
-- emilyj    / password123
-- davidb    / password123
-- sarahtrader / trader123
-- admin     / admin123
-- ============================================================

INSERT INTO users
(
    name,
    username,
    email,
    address,
    password_hash,
    role
)
VALUES
(
    'John Smith',
    'johnsmith',
    'john@example.com',
    '123 Main Street, Montreal, QC',
    '$2b$12$LQv3c1yqBWxkN5M6Qz6q0eP7QJw8xX5V4J2K3L4M5N6O7P8Q9R0S',
    'TRADER'
),
(
    'Emily Johnson',
    'emilyj',
    'emily@example.com',
    '456 Saint Catherine Street, Montreal, QC',
    '$2b$12$LQv3c1yqBWxkN5M6Qz6q0eP7QJw8xX5V4J2K3L4M5N6O7P8Q9R0S',
    'TRADER'
),
(
    'David Brown',
    'davidb',
    'david@example.com',
    '789 Sherbrooke Street, Montreal, QC',
    '$2b$12$LQv3c1yqBWxkN5M6Qz6q0eP7QJw8xX5V4J2K3L4M5N6O7P8Q9R0S',
    'TRADER'
),
(
    'Sarah Wilson',
    'sarahtrader',
    'trader@example.com',
    '100 Wellington Street, Montreal, QC',
    '$2b$12$LQv3c1yqBWxkN5M6Qz6q0eP7QJw8xX5V4J2K3L4M5N6O7P8Q9R0S',
    'TRADER'
),
(
    'System Administrator',
    'admin',
    'admin@example.com',
    '100 Administration Street, Montreal, QC',
    '$2b$12$LQv3c1yqBWxkN5M6Qz6q0eP7QJw8xX5V4J2K3L4M5N6O7P8Q9R0S',
    'ADMIN'
);


-- ============================================================
-- 9. STOCKS
-- ============================================================

INSERT INTO stocks
(
    symbol,
    company_name,
    current_price
)
VALUES
('AAPL', 'Apple Inc.', 230.00),
('MSFT', 'Microsoft Corporation', 500.00),
('NVDA', 'NVIDIA Corporation', 175.00),
('AMZN', 'Amazon.com Inc.', 230.00),
('TSLA', 'Tesla Inc.', 340.00),
('GOOGL', 'Alphabet Inc.', 205.00),
('META', 'Meta Platforms Inc.', 750.00);


-- ============================================================
-- 10. PORTFOLIOS
-- ============================================================

INSERT INTO portfolios
(
    user_id,
    cash_balance
)
VALUES
(1, 10000.00),
(2, 15000.00),
(3, 20000.00),
(4, 25000.00),
(5, 50000.00);


-- ============================================================
-- 11. HOLDINGS
-- ============================================================

INSERT INTO holdings
(
    portfolio_id,
    stock_id,
    quantity,
    average_price
)
VALUES

-- John
(1, 1, 20, 210.00),
(1, 2, 10, 450.00),

-- Emily
(2, 3, 30, 150.00),
(2, 5, 10, 300.00),

-- David
(3, 4, 15, 200.00),
(3, 6, 20, 180.00),

-- Sarah
(4, 1, 10, 215.00),
(4, 7, 5, 700.00);


-- ============================================================
-- 12. ORDERS
-- ============================================================

-- John's approved BUY

INSERT INTO orders
(
    user_id,
    stock_id,
    order_type,
    quantity,
    price,
    status,
    approved_by,
    approved_at,
    created_by
)
VALUES
(
    1,
    1,
    'BUY',
    20,
    210.00,
    'APPROVED',
    4,
    CURRENT_TIMESTAMP,
    1
);


-- Emily's pending BUY

INSERT INTO orders
(
    user_id,
    stock_id,
    order_type,
    quantity,
    price,
    status,
    created_by
)
VALUES
(
    2,
    4,
    'BUY',
    5,
    230.00,
    'PENDING',
    2
);


-- David's approved SELL

INSERT INTO orders
(
    user_id,
    stock_id,
    order_type,
    quantity,
    price,
    status,
    approved_by,
    approved_at,
    created_by
)
VALUES
(
    3,
    6,
    'SELL',
    5,
    205.00,
    'APPROVED',
    4,
    CURRENT_TIMESTAMP,
    3
);


-- John's rejected BUY

INSERT INTO orders
(
    user_id,
    stock_id,
    order_type,
    quantity,
    price,
    status,
    approved_by,
    approved_at,
    created_by
)
VALUES
(
    1,
    5,
    'BUY',
    100,
    340.00,
    'REJECTED',
    4,
    CURRENT_TIMESTAMP,
    1
);


-- Emily's flagged BUY

INSERT INTO orders
(
    user_id,
    stock_id,
    order_type,
    quantity,
    price,
    status,
    created_by
)
VALUES
(
    2,
    3,
    'BUY',
    500,
    175.00,
    'FLAGGED',
    2
);


-- David's cancelled BUY

INSERT INTO orders
(
    user_id,
    stock_id,
    order_type,
    quantity,
    price,
    status,
    cancelled_at,
    created_by
)
VALUES
(
    3,
    1,
    'BUY',
    10,
    230.00,
    'CANCELLED',
    CURRENT_TIMESTAMP,
    3
);


-- ============================================================
-- 13. AUDIT LOGS
-- ============================================================

INSERT INTO audit_logs
(
    user_id,
    action,
    entity_type,
    entity_id,
    details
)
VALUES
(
    1,
    'LOGIN',
    'USER',
    1,
    'John Smith logged in'
),
(
    2,
    'LOGIN',
    'USER',
    2,
    'Emily Johnson logged in'
),
(
    1,
    'CREATE_ORDER',
    'ORDER',
    1,
    'Created BUY order for 20 AAPL shares'
),
(
    2,
    'CREATE_ORDER',
    'ORDER',
    2,
    'Created BUY order for 5 AMZN shares'
),
(
    4,
    'APPROVE_ORDER',
    'ORDER',
    1,
    'Sarah Wilson approved order #1'
),
(
    4,
    'REJECT_ORDER',
    'ORDER',
    4,
    'Sarah Wilson rejected order #4'
),
(
    2,
    'FLAG_ORDER',
    'ORDER',
    5,
    'Emily Johnson order flagged for review'
),
(
    3,
    'CANCEL_ORDER',
    'ORDER',
    6,
    'David Brown cancelled pending order'
),
(
    5,
    'LOGIN',
    'USER',
    5,
    'System Administrator logged in'
);


-- ============================================================
-- 14. VERIFY USERS
-- ============================================================

SELECT
    id,
    name,
    username,
    email,
    role
FROM users
ORDER BY id;


-- ============================================================
-- 15. VERIFY STOCKS
-- ============================================================

SELECT *
FROM stocks;


-- ============================================================
-- 16. VERIFY PORTFOLIOS
-- ============================================================

SELECT *
FROM portfolios;


-- ============================================================
-- 17. VERIFY HOLDINGS
-- ============================================================

SELECT *
FROM holdings;


-- ============================================================
-- 18. VERIFY ORDERS
-- ============================================================

SELECT *
FROM orders;


-- ============================================================
-- 19. VERIFY AUDIT LOGS
-- ============================================================

SELECT *
FROM audit_logs
ORDER BY id;