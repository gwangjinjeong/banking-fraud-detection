-- 계정계 데이터베이스 초기화
USE account_system;

-- 계좌 정보 테이블
CREATE TABLE IF NOT EXISTS accounts (
    account_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    account_type VARCHAR(20) NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0,
    daily_limit DECIMAL(15, 2) DEFAULT 10000000,
    daily_used DECIMAL(15, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    last_transaction_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 고객 정보 테이블
CREATE TABLE IF NOT EXISTS customers (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ssn_hash VARCHAR(64),
    phone VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(255),
    customer_grade VARCHAR(20) DEFAULT 'NORMAL',
    registration_date DATE,
    INDEX idx_grade (customer_grade)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 샘플 데이터 삽입
INSERT INTO accounts (account_id, user_id, account_type, balance, daily_limit, status, last_transaction_date) VALUES
('ACC001', 'USER001', 'CHECKING', 5000000, 3000000, 'ACTIVE', '2024-01-15 10:30:00'),
('ACC002', 'USER002', 'SAVINGS', 10000000, 5000000, 'ACTIVE', '2024-01-14 15:20:00'),
('ACC003', 'USER003', 'CHECKING', 500000, 1000000, 'DORMANT', '2022-06-10 09:00:00'),
('ACC004', 'USER004', 'CHECKING', 2000000, 2000000, 'ACTIVE', '2024-01-15 08:00:00'),
('ACC005', 'USER005', 'SAVINGS', 50000000, 10000000, 'ACTIVE', '2024-01-13 14:30:00');

INSERT INTO customers (user_id, name, customer_grade, registration_date) VALUES
('USER001', '김철수', 'GOLD', '2020-03-15'),
('USER002', '이영희', 'NORMAL', '2021-07-20'),
('USER003', '박민수', 'NORMAL', '2019-01-10'),
('USER004', '최정훈', 'VIP', '2018-05-05'),
('USER005', '한지민', 'GOLD', '2020-11-11');