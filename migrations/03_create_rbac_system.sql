-- Migration: Create RBAC (Role-Based Access Control) System
-- Version: 03
-- Created: 2024-12-01T15:00:00
-- Description: Create comprehensive RBAC system with roles, rights, user-role, and role-right tables

-- Step 1: Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    is_active TINYINT(1) DEFAULT 1,
    is_system_role TINYINT(1) DEFAULT 0 COMMENT 'System roles cannot be deleted',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_is_active (is_active),
    INDEX idx_is_system_role (is_system_role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Step 2: Create rights table (permissions/access rights)
CREATE TABLE IF NOT EXISTS rights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    resource_type ENUM('ui_page', 'api_endpoint', 'feature', 'action') NOT NULL,
    resource_path VARCHAR(500) NOT NULL COMMENT 'UI page route or API endpoint path',
    http_method VARCHAR(10) NULL COMMENT 'HTTP method for API endpoints (GET, POST, PUT, DELETE, etc.)',
    is_active TINYINT(1) DEFAULT 1,
    is_system_right TINYINT(1) DEFAULT 0 COMMENT 'System rights cannot be deleted',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_resource_type (resource_type),
    INDEX idx_resource_path (resource_path),
    INDEX idx_http_method (http_method),
    INDEX idx_is_active (is_active),
    INDEX idx_is_system_right (is_system_right)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Step 3: Create user_roles table (many-to-many relationship between users and roles)
CREATE TABLE IF NOT EXISTS user_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    assigned_by INT NULL COMMENT 'User who assigned this role',
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL COMMENT 'Optional expiration date for the role assignment',
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_user_role (user_id, role_id),
    INDEX idx_user_id (user_id),
    INDEX idx_role_id (role_id),
    INDEX idx_assigned_by (assigned_by),
    INDEX idx_expires_at (expires_at),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Step 4: Create role_rights table (many-to-many relationship between roles and rights)
CREATE TABLE IF NOT EXISTS role_rights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    right_id INT NOT NULL,
    granted_by INT NULL COMMENT 'User who granted this right to the role',
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (right_id) REFERENCES rights(id) ON DELETE CASCADE,
    FOREIGN KEY (granted_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_role_right (role_id, right_id),
    INDEX idx_role_id (role_id),
    INDEX idx_right_id (right_id),
    INDEX idx_granted_by (granted_by),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Step 5: Insert super admin role with wildcard permissions
INSERT INTO roles (name, display_name, description, is_active, is_system_role) VALUES
('super_admin', 'Super Administrator', 'Full system access with wildcard (*) permissions', 1, 1)
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- Step 6: Insert wildcard right for super admin
INSERT INTO rights (name, display_name, description, resource_type, resource_path, http_method, is_active, is_system_right) VALUES
('*', 'All Permissions', 'Wildcard permission granting access to everything', 'feature', '*', '*', 1, 1)
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- Step 7: Assign wildcard right to super admin role
INSERT INTO role_rights (role_id, right_id, is_active)
SELECT r.id, rt.id, 1
FROM roles r, rights rt
WHERE r.name = 'super_admin' AND rt.name = '*'
ON DUPLICATE KEY UPDATE is_active = 1;

-- Step 8: Assign super admin role to all existing users
INSERT INTO user_roles (user_id, role_id, is_active)
SELECT u.id, r.id, 1
FROM users u, roles r
WHERE r.name = 'super_admin'
ON DUPLICATE KEY UPDATE is_active = 1;

-- Step 9: Create indexes for better performance
CREATE INDEX idx_user_roles_active ON user_roles(user_id, is_active);
CREATE INDEX idx_role_rights_active ON role_rights(role_id, is_active);
CREATE INDEX idx_rights_resource_type_path ON rights(resource_type, resource_path);
CREATE INDEX idx_rights_http_method_path ON rights(http_method, resource_path);

-- Step 10: Add comments for documentation
ALTER TABLE roles COMMENT = 'System roles for RBAC';
ALTER TABLE rights COMMENT = 'System rights/permissions for RBAC';
ALTER TABLE user_roles COMMENT = 'Many-to-many relationship between users and roles';
ALTER TABLE role_rights COMMENT = 'Many-to-many relationship between roles and rights';
