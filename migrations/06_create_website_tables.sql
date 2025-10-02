-- Website Module Database Schema
-- This migration creates tables for contact us and pricing plans

-- Start transaction
START TRANSACTION;

-- Create contact_us table
CREATE TABLE IF NOT EXISTS contact_us (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NULL,
    whatsappNumber VARCHAR(20) NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create pricing_plans table
CREATE TABLE IF NOT EXISTS pricing_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    sessions VARCHAR(20) NOT NULL,
    duration VARCHAR(50) NOT NULL,
    base_price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    retention_discount DECIMAL(5,4) NOT NULL DEFAULT 0.0000,
    free_sessions INT NOT NULL DEFAULT 0,
    curriculum TEXT NOT NULL,
    features JSON NOT NULL,
    is_current TINYINT(1) DEFAULT 0,
    is_popular TINYINT(1) DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_is_active (is_active),
    INDEX idx_is_current (is_current),
    INDEX idx_is_popular (is_popular)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample pricing plans
INSERT INTO pricing_plans (title, sessions, duration, base_price, retention_discount, free_sessions, curriculum, features, is_current, is_popular, is_active) VALUES
('Topic Focus', '24', '3 months', 20.00, 0.0000, 3, 'US, UK, IB, Cambridge, Montessori, Middle East', 
 JSON_ARRAY('Single Topic Deep Dive', 'Concept Building Focus'), 0, 0, 1),
('Crash Course', '48', '6 months', 20.00, 0.0750, 6, 'US, UK, IB, Cambridge, Montessori, Middle East', 
 JSON_ARRAY('Complete Syllabus Coverage', 'Fast-paced Learning', 'Essential Concepts Only'), 1, 1, 1),
('Comprehensive Year', '96', '12 months', 20.00, 0.1500, 12, 'US, UK, IB, Cambridge, Montessori, Middle East', 
 JSON_ARRAY('Complete Year-long Syllabus', 'Extensive Topic Coverage', 'Deep Concept Understanding'), 0, 0, 1)
ON DUPLICATE KEY UPDATE title = VALUES(title);

-- Commit transaction
COMMIT;
