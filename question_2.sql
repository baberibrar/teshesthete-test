CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    Amount INT
);

INSERT INTO Orders (OrderID, CustomerID, OrderDate, Amount) VALUES
(1001, 101, '2024-01-01', 100),
(1002, 102, '2024-01-02', 150),
(1003, 103, '2024-01-03', 200),
(1001, 101, '2024-01-01', 100),
(1003, 103, '2024-01-03', 200);



SELECT O1.OrderID, O1.CustomerID, O1.OrderDate, O1.Amount
FROM Orders O1
JOIN (
    SELECT OrderID, CustomerID, OrderDate, Amount
    FROM Orders
    GROUP BY OrderID, CustomerID, OrderDate, Amount
    HAVING COUNT(*) > 1
) AS O2 ON O1.OrderID = O2.OrderID
         AND O1.CustomerID = O2.CustomerID
         AND O1.OrderDate = O2.OrderDate
         AND O1.Amount = O2.Amount
ORDER BY O1.OrderID;