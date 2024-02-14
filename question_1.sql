-- Create a table named Employee with columns ID and Salary
CREATE TABLE Employee (
    ID INT PRIMARY KEY,
    Salary DECIMAL(10, 2)
);

-- Insert records into the Employee table with ID and Salary values
INSERT INTO Employee (ID, Salary) VALUES
(1, 100),
(2, 200),
(3, 300);


-- Retrieve the second-highest salary from the Employee table
SELECT Salary AS SecondHighestSalary
FROM Employee
ORDER BY Salary DESC
LIMIT 1 OFFSET 1;

