CREATE DATABASE school;

USE school;

-- Students Table
CREATE TABLE Students (
    StudentID INT PRIMARY KEY IDENTITY,
    Name VARCHAR(100),
    Age INT,
    ClassID INT,
    TuitionFees DECIMAL(10, 2),
    TransportFees DECIMAL(10, 2),
    ExamFees DECIMAL(10, 2),
    FeesPaid DECIMAL(10, 2),
    Address VARCHAR(255),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(100),
    AdmissionDate DATE,
    AttendancePercentage DECIMAL(5, 2),
    ExamScore DECIMAL(5, 2),
    Status VARCHAR(50),
    Remarks TEXT
);

-- Classes Table
CREATE TABLE Classes (
    ClassID INT PRIMARY KEY IDENTITY,
    ClassName VARCHAR(50)
);

-- Teachers Table
CREATE TABLE Teachers (
    TeacherID INT PRIMARY KEY IDENTITY,
    Name VARCHAR(100),
    SubjectID INT,
    PhoneNumber VARCHAR(20),
    Email VARCHAR(100)
);

-- Subjects Table
CREATE TABLE Subjects (
    SubjectID INT PRIMARY KEY IDENTITY,
    SubjectName VARCHAR(100)
);

-- Courses Table
CREATE TABLE Courses (
    CourseID INT PRIMARY KEY IDENTITY,
    CourseName VARCHAR(100),
    Description TEXT,
    TeacherID INT
);

-- Enrollments Table
CREATE TABLE Enrollments (
    EnrollmentID INT PRIMARY KEY IDENTITY,
    StudentID INT,
    CourseID INT,
    Term VARCHAR(50),
    EnrollmentDate DATE
);

-- Exams Table
CREATE TABLE Exams (
    ExamID INT PRIMARY KEY IDENTITY,
    SubjectID INT,
    Term VARCHAR(50)
);

-- ExamResults Table
CREATE TABLE ExamResults (
    ResultID INT PRIMARY KEY IDENTITY,
    ExamID INT,
    StudentID INT,
    MarksObtained DECIMAL(5, 2),
    TotalMarks DECIMAL(5, 2)
);

-- Attendance Table
CREATE TABLE Attendance (
    AttendanceID INT PRIMARY KEY IDENTITY,
    StudentID INT,
    CourseID INT,
    Date DATE,
    Status VARCHAR(20)
);

-- Payments Table
CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY IDENTITY,
    StudentID INT,
    AmountPaid DECIMAL(10, 2),
    PaymentDate DATE,
    PaymentMethod VARCHAR(50)
);

-- Parents Table
CREATE TABLE Parents (
    ParentID INT PRIMARY KEY IDENTITY,
    StudentID INT,
    Name VARCHAR(100),
    Relationship VARCHAR(50),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(100)
);

-- ExamTypes Table
CREATE TABLE ExamTypes (
    ExamTypeID INT PRIMARY KEY IDENTITY,
    ExamType VARCHAR(50),
    Weightage DECIMAL(5, 2)
);

-- Grades Table
CREATE TABLE Grades (
    GradeID INT PRIMARY KEY IDENTITY,
    MinMarks DECIMAL(5, 2),
    MaxMarks DECIMAL(5, 2),
    Grade VARCHAR(10)
);

-- HomeroomTeachers Table
CREATE TABLE HomeroomTeachers (
    HomeroomID INT PRIMARY KEY IDENTITY,
    TeacherID INT,
    ClassID INT
);

-- Logs Table
CREATE TABLE Logs (
    LogID INT PRIMARY KEY IDENTITY,
    TableName VARCHAR(100),
    Action VARCHAR(50),
    ActionDate DATETIME,
    UserID INT,
    UserRole VARCHAR(50),
    OldValue TEXT,
    NewValue TEXT,
    Details TEXT
);

--Inserting Example Value --
 -- Inserting data into Classes table
INSERT INTO Classes (ClassName) VALUES ('Class 1');
INSERT INTO Classes (ClassName) VALUES ('Class 2');

-- Inserting data into Students table
INSERT INTO Students (Name, Age, ClassID, TuitionFees, TransportFees, ExamFees, FeesPaid, Address, PhoneNumber, Email, AdmissionDate, AttendancePercentage, ExamScore, Status, Remarks) 
VALUES ('Student 1', 10, 1, 50000.00, 5000.00, 2000.00, 22000.00, 'Address 1', '9876543210', 'student1@school.com', '2025-01-10', 95.00, 88.00, 'Active', 'Good Performance');

-- Inserting data into Teachers table
INSERT INTO Teachers (Name, SubjectID, PhoneNumber, Email) 
VALUES ('Teacher 1', 1, '9123456789', 'teacher1@school.com');

-- Inserting data into Subjects table
INSERT INTO Subjects (SubjectName) VALUES ('Mathematics');
INSERT INTO Subjects (SubjectName) VALUES ('Science');

-- Inserting data into Payments table
INSERT INTO Payments (StudentID, AmountPaid, PaymentDate, PaymentMethod) 
VALUES (1, 10000.00, '2025-03-10', 'Credit Card');

-- Inserting data into Parents table
INSERT INTO Parents (StudentID, Name, Relationship, PhoneNumber, Email) 
VALUES (1, 'Parent 1', 'Father', '9876543210', 'parent1@school.com');

