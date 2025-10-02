-- Migration: modify_result_display_config_structure
-- Version: 02
-- Created: 2024-12-01T12:00:00
-- Description: Remove redundant columns, add grid metadata table, and separate datatype fields

-- Start transaction
START TRANSACTION;

-- Step 1: Create grid_metadata table
CREATE TABLE grid_metadata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gridName VARCHAR(100) NOT NULL UNIQUE,
    gridNameId VARCHAR(50) NOT NULL UNIQUE,
    description TEXT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_grid_name (gridName),
    INDEX idx_grid_name_id (gridNameId),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Step 2: Insert default grid metadata
INSERT INTO grid_metadata (gridName, gridNameId, description) VALUES 
('users_grid', 'users_grid_001', 'User management grid configuration'),
('products_grid', 'products_grid_001', 'Product management grid configuration'),
('orders_grid', 'orders_grid_001', 'Order management grid configuration');

-- Step 3: Create temporary table with new structure
CREATE TABLE result_display_config_new (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gridNameId VARCHAR(50) NOT NULL,
    displayId VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    hidden TINYINT(1) DEFAULT 0,
    width INT NULL,
    sortIndex INT NOT NULL,
    ellipsis TINYINT(1) DEFAULT 0,
    align VARCHAR(20) NULL,
    dbDataType VARCHAR(50) NULL,
    codeDataType VARCHAR(50) NULL,
    format VARCHAR(100) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (gridNameId) REFERENCES grid_metadata(gridNameId) ON DELETE CASCADE,
    INDEX idx_grid_name_id (gridNameId),
    INDEX idx_sort_index (sortIndex),
    INDEX idx_display_id (displayId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Step 4: Copy data from old table to new table
INSERT INTO result_display_config_new (
    id, gridNameId, displayId, title, hidden, width, sortIndex, 
    ellipsis, align, dbDataType, codeDataType, format
)
SELECT 
    id, 'users_grid_001' as gridNameId, displayId, title, hidden, width, sortIndex, 
    ellipsis, align, dataType as dbDataType, dataType as codeDataType, format
FROM result_display_config;

-- Step 5: Drop old table
DROP TABLE result_display_config;

-- Step 6: Rename new table to original name
RENAME TABLE result_display_config_new TO result_display_config;

-- Step 7: Verify the new structure
-- This will be checked after migration runs

-- Commit transaction
COMMIT;