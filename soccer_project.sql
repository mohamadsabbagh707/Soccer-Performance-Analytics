CREATE DATABASE soccer_project;
GO

USE soccer_project;
GO


CREATE TABLE Match_Statistics (
    match_id INT PRIMARY KEY,
    difficulty_level VARCHAR(10) NOT NULL,
    shots INT NOT NULL,
    goals INT NOT NULL,
    saves INT NOT NULL,
    power_shot_count INT NOT NULL,
    accuracy FLOAT NOT NULL,
    CONSTRAINT CHK_difficulty_level CHECK (difficulty_level IN ('Easy', 'Normal', 'Hard')),
    CONSTRAINT CHK_shots_nonnegative CHECK (shots >= 0),
    CONSTRAINT CHK_goals_nonnegative CHECK (goals >= 0),
    CONSTRAINT CHK_saves_nonnegative CHECK (saves >= 0),
    CONSTRAINT CHK_power_shot_count_nonnegative CHECK (power_shot_count >= 0),
    CONSTRAINT CHK_accuracy_range CHECK (accuracy >= 0 AND accuracy <= 1),
    CONSTRAINT CHK_goals_le_shots CHECK (goals <= shots),
    CONSTRAINT CHK_saves_le_shots CHECK (saves <= shots),
    CONSTRAINT CHK_power_shots_le_shots CHECK (power_shot_count <= shots)
);

-- Verify data was imported from Cleaned CSV file
SELECT * FROM Match_Stats;


