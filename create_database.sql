-- 创建数据库
CREATE DATABASE IF NOT EXISTS chunithm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE chunithm_db;

CREATE TABLE IF NOT EXISTS songs (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    bpm INT NOT NULL,
    origin_from VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_title (title),
    INDEX idx_artist (artist),
    INDEX idx_genre (genre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 难度表
CREATE TABLE IF NOT EXISTS difficulties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    song_id INT NOT NULL,
    difficulty_type ENUM('BASIC', 'ADVANCED', 'EXPERT', 'MASTER', 'ULTRA', 'WORLD\'S END') NOT NULL,
    level_value DECIMAL(4,1) NOT NULL,
    level_display VARCHAR(10) NOT NULL,
    chart_id INT NOT NULL,
    combo INT NOT NULL,
    charter VARCHAR(255) NOT NULL,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
    INDEX idx_song_difficulty (song_id, difficulty_type),
    INDEX idx_level (level_value)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;