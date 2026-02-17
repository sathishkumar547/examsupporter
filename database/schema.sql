-- Student Exam Supporter Database Schema
-- MySQL Table Creation Queries

-- Create database
CREATE DATABASE IF NOT EXISTS student_exam_supporter;
USE student_exam_supporter;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Materials table
CREATE TABLE IF NOT EXISTS materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    university VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Sample data for testing (optional)
-- INSERT INTO users (name, email, password) VALUES 
-- ('Test User', 'test@example.com', '$2b$12$YourHashedPasswordHere');

-- Show tables
SHOW TABLES;
