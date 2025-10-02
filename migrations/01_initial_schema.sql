-- Initial Database Schema for KSeekers
-- This migration creates all necessary tables and sample data

-- Start transaction
START TRANSACTION;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NULL,
    is_active TINYINT(1) DEFAULT 1,
    is_admin TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create OTPs table
CREATE TABLE IF NOT EXISTS otps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    code VARCHAR(10) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_used TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_code (code),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create result_display_config table
CREATE TABLE IF NOT EXISTS result_display_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    displayId VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    `key` VARCHAR(100) NOT NULL,
    hidden TINYINT(1) DEFAULT 0,
    sorter TINYINT(1) DEFAULT 0,
    width INT NULL,
    fixed VARCHAR(50) NULL,
    dataIndex VARCHAR(100) NOT NULL,
    sortIndex INT NOT NULL,
    type VARCHAR(50) NOT NULL,
    ellipsis TINYINT(1) DEFAULT 0,
    align VARCHAR(20) NULL,
    dataType VARCHAR(50) NULL,
    format VARCHAR(100) NULL,
    INDEX idx_type (type),
    INDEX idx_sort_index (sortIndex)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create lookup_types table
CREATE TABLE IF NOT EXISTS lookup_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create lookup_values table
CREATE TABLE IF NOT EXISTS lookup_values (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lookup_type_id INT NOT NULL,
    code VARCHAR(50) NOT NULL,
    value VARCHAR(255) NOT NULL,
    description TEXT NULL,
    is_active TINYINT(1) DEFAULT 1,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lookup_type_id) REFERENCES lookup_types(id) ON DELETE CASCADE,
    UNIQUE KEY unique_lookup_code (lookup_type_id, code),
    INDEX idx_lookup_type_id (lookup_type_id),
    INDEX idx_code (code),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default admin user
INSERT INTO users (username, email, phone, is_active, is_admin) 
VALUES ('admin', 'admin@example.com', '1234567890', 1, 1)
ON DUPLICATE KEY UPDATE username = username;

-- Insert sample result display configurations
INSERT INTO result_display_config (displayId, title, `key`, hidden, sorter, width, dataIndex, sortIndex, type, ellipsis) VALUES
('id', 'ID', 'id', 0, 1, 80, 'id', 1, 'string', 0),
('name', 'Name', 'name', 0, 1, 150, 'name', 2, 'string', 1),
('email', 'Email', 'email', 0, 1, 200, 'email', 3, 'string', 1),
('phone', 'Phone', 'phone', 0, 0, 120, 'phone', 4, 'string', 0),
('created_at', 'Created', 'created_at', 0, 1, 150, 'created_at', 5, 'date', 0),
('status', 'Status', 'status', 0, 1, 100, 'status', 6, 'string', 0),
('amount', 'Amount', 'amount', 0, 1, 120, 'amount', 7, 'number', 0),
('description', 'Description', 'description', 0, 0, 250, 'description', 8, 'string', 1)
ON DUPLICATE KEY UPDATE displayId = VALUES(displayId);

-- Insert sample lookup types
INSERT INTO lookup_types (name, description) VALUES
('user_status', 'User account status'),
('user_roles', 'User role types'),
('priority_levels', 'Priority levels for tasks'),
('document_types', 'Types of documents')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- Insert sample lookup values
INSERT INTO lookup_values (lookup_type_id, code, value, description, is_active, sort_order) VALUES
-- User status values
((SELECT id FROM lookup_types WHERE name = 'user_status'), 'active', 'Active', 'User account is active', 1, 1),
((SELECT id FROM lookup_types WHERE name = 'user_status'), 'inactive', 'Inactive', 'User account is inactive', 1, 2),
((SELECT id FROM lookup_types WHERE name = 'user_status'), 'suspended', 'Suspended', 'User account is suspended', 1, 3),
-- User roles
((SELECT id FROM lookup_types WHERE name = 'user_roles'), 'admin', 'Administrator', 'Full system access', 1, 1),
((SELECT id FROM lookup_types WHERE name = 'user_roles'), 'user', 'Regular User', 'Standard user access', 1, 2),
((SELECT id FROM lookup_types WHERE name = 'user_roles'), 'guest', 'Guest', 'Limited access', 1, 3),
-- Priority levels
((SELECT id FROM lookup_types WHERE name = 'priority_levels'), 'low', 'Low', 'Low priority', 1, 1),
((SELECT id FROM lookup_types WHERE name = 'priority_levels'), 'medium', 'Medium', 'Medium priority', 1, 2),
((SELECT id FROM lookup_types WHERE name = 'priority_levels'), 'high', 'High', 'High priority', 1, 3),
((SELECT id FROM lookup_types WHERE name = 'priority_levels'), 'urgent', 'Urgent', 'Urgent priority', 1, 4),
-- Document types
((SELECT id FROM lookup_types WHERE name = 'document_types'), 'pdf', 'PDF Document', 'Portable Document Format', 1, 1),
((SELECT id FROM lookup_types WHERE name = 'document_types'), 'doc', 'Word Document', 'Microsoft Word Document', 1, 2),
((SELECT id FROM lookup_types WHERE name = 'document_types'), 'xls', 'Excel Spreadsheet', 'Microsoft Excel Spreadsheet', 1, 3),
((SELECT id FROM lookup_types WHERE name = 'document_types'), 'img', 'Image File', 'Image file (JPG, PNG, etc.)', 1, 4)
ON DUPLICATE KEY UPDATE code = VALUES(code);

-- Commit transaction
COMMIT;
