-- Rollback migration for modify_result_display_config_structure
-- Version: R02
-- Created: 2024-12-01T12:00:00
-- Description: Restore original result_display_config structure

-- Step 1: Create temporary table with original structure
CREATE TABLE result_display_config_old (
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

-- Step 2: Copy data from current table to old structure table
INSERT INTO result_display_config_old (
    id, displayId, title, `key`, hidden, sorter, width, fixed, 
    dataIndex, sortIndex, type, ellipsis, align, dataType, format
)
SELECT 
    id, displayId, title, displayId as `key`, hidden, 0 as sorter, 
    width, NULL as fixed, displayId as dataIndex, sortIndex, 
    'grid' as type, ellipsis, align, COALESCE(dbDataType, codeDataType) as dataType, format
FROM result_display_config;

-- Step 3: Drop current table
DROP TABLE result_display_config;

-- Step 4: Drop grid_metadata table
DROP TABLE grid_metadata;

-- Step 5: Rename old structure table to original name
RENAME TABLE result_display_config_old TO result_display_config;
