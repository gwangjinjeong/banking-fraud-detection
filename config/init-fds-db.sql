-- FDS 데이터베이스 초기화
USE fds_system;

-- 블랙리스트 테이블
CREATE TABLE IF NOT EXISTS blacklist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    value VARCHAR(100) NOT NULL,
    reason VARCHAR(255),
    risk_level INT DEFAULT 5,
    listed_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATETIME,
    UNIQUE KEY uniq_blacklist (type, value),
    INDEX idx_type_value (type, value)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- FDS 사용자 위험도 테이블
CREATE TABLE IF NOT EXISTS user_risk_profiles (
    user_id VARCHAR(50) PRIMARY KEY,
    risk_score INT DEFAULT 0,
    fraud_count INT DEFAULT 0,
    last_fraud_date DATETIME,
    monitoring_level VARCHAR(20) DEFAULT 'NORMAL',
    notes TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 가맹점 정보 테이블
CREATE TABLE IF NOT EXISTS merchants (
    merchant_id VARCHAR(50) PRIMARY KEY,
    merchant_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    risk_category VARCHAR(20) DEFAULT 'LOW',
    country VARCHAR(50),
    is_high_risk BOOLEAN DEFAULT FALSE,
    INDEX idx_risk (is_high_risk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 샘플 블랙리스트 데이터
INSERT INTO blacklist (type, value, reason, risk_level) VALUES
('CARD_NUMBER', '4111-1111-1111-1111', 'Stolen card report', 10),
('IP_ADDRESS', '192.168.100.50', 'Known fraud IP', 8),
('ACCOUNT_ID', 'ACC999', 'Fraudulent account', 9),
('USER_ID', 'FRAUD_USER_001', 'Confirmed fraudster', 10);

-- 샘플 가맹점 데이터
INSERT INTO merchants (merchant_id, merchant_name, category, risk_category, country, is_high_risk) VALUES
('MERCH001', 'Amazon', 'E-Commerce', 'LOW', 'US', FALSE),
('MERCH002', 'Suspicious Gaming Site', 'Gaming', 'HIGH', 'Unknown', TRUE),
('MERCH003', 'Local Restaurant', 'Food', 'LOW', 'KR', FALSE),
('MERCH004', 'Crypto Exchange X', 'Cryptocurrency', 'HIGH', 'MT', TRUE);