# innovaccer
assignment
install below package: 
`pip install mysql-connector-python`

Table creation queries: 
```
CREATE TABLE expense (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    paid_by_user VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL
);
```

```
CREATE TABLE share (
    share_id INT AUTO_INCREMENT PRIMARY KEY,
    expense_id INT NOT NULL,
    user VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (expense_id) REFERENCES expense(expense_id)
)```



