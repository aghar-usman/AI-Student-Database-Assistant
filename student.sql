-- Create the database
CREATE DATABASE StudentRecords;
GO

-- Use the newly created database
USE StudentRecords;
GO

-- Create the Students table with constraints
CREATE TABLE Students (  -- Changed table name to match queries
    StudentID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Age INT CHECK (Age > 0),
    Class NVARCHAR(50) NOT NULL,
    FeesPaid DECIMAL(10,2) CHECK (FeesPaid >= 0),
    TotalFees DECIMAL(10,2) CHECK (TotalFees >= 0),
    Address NVARCHAR(255),
    PhoneNumber NVARCHAR(15) UNIQUE,  
    Email NVARCHAR(100) UNIQUE,        
    AdmissionDate DATE DEFAULT GETDATE(),
    AttendancePercentage DECIMAL(5,2) CHECK (AttendancePercentage BETWEEN 0 AND 100), -- Added
    ExamScore DECIMAL(5,2) CHECK (ExamScore BETWEEN 0 AND 100), -- Added
    Remarks NVARCHAR(255), -- Added
    CONSTRAINT UQ_Student UNIQUE (Name, Age, Class), 
    CONSTRAINT CHK_Fees CHECK (FeesPaid <= TotalFees) 
);
GO

-- Insert sample data
INSERT INTO Students (Name, Age, Class, FeesPaid, TotalFees, Address, PhoneNumber, Email, AttendancePercentage, ExamScore, Remarks)
VALUES
('Rahul Sharma', 16, '10th Grade', 25000, 50000, 'Mumbai, India', '9876543210', 'rahul@example.com', 85.5, 78.2, 'Good in mathematics, needs improvement in English'),
('Anjali Verma', 15, '9th Grade', 20000, 50000, 'Bangalore, India', '9823456789', 'anjali@example.com', 92.3, 88.0, 'Excellent in science, very active in class'),
('Arjun Kumar', 14, '8th Grade', 15000, 40000, 'Delhi, India', '9876501234', 'arjun@example.com', 75.8, 65.4, 'Struggles with algebra, requires extra coaching'),
('Neha Singh', 17, '11th Grade', 30000, 60000, 'Kolkata, India', '9845123456', 'neha@example.com', 89.4, 92.1, 'Top performer in physics, recommended for Olympiad'),
('Rohan Das', 18, '12th Grade', 32000, 65000, 'Chennai, India', '9978123456', 'rohan@example.com', 70.2, 55.8, 'Needs to focus more on academics, often late'),
('Pooja Iyer', 15, '9th Grade', 22000, 50000, 'Hyderabad, India', '9812345678', 'pooja@example.com', 95.0, 91.2, 'Excellent discipline, leadership skills observed'),
('Amit Khanna', 16, '10th Grade', 26000, 50000, 'Pune, India', '9834567890', 'amit@example.com', 60.5, 48.0, 'Requires intervention, low engagement in class'),
('Meera Kapoor', 17, '11th Grade', 28000, 60000, 'Jaipur, India', '9898765432', 'meera@example.com', 80.0, 85.5, 'Hardworking, but struggles with time management');
GO

-- Retrieve data to verify
SELECT * FROM Students;
GO
