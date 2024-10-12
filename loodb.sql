DROP DATABASE IF EXISTS loodb;

CREATE DATABASE IF NOT EXISTS loodb;

USE loodb;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username TEXT,
    pwd TEXT,
    email TEXT,
     
)

CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    establishment_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (establishment_id) REFERENCES establishments(establishment_id) ON DELETE CASCADE
);

CREATE TABLE bathrooms (
    bathroom_id INT AUTO_INCREMENT PRIMARY KEY,
    establishment_id INT,
    cleanliness_rating INT CHECK (cleanliness_rating >= 1 AND cleanliness_rating <= 5),
    accessibility_rating INT CHECK (accessibility_rating >= 1 AND accessibility_rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (establishment_id) REFERENCES establishments(establishment_id) ON DELETE CASCADE
);
