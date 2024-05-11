import mysql.connector

class ExpenseManager:
    def __init__(self, host, user, password, database):
        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db_connection.cursor()

    def add_expense(self, paid_by_user, amount, shares):
        # Insert expense into expense table
        add_expense_query = "INSERT INTO expense (paid_by_user, amount) VALUES (%s, %s)"
        self.cursor.execute(add_expense_query, (paid_by_user, amount))
        expense_id = self.cursor.lastrowid

        # Insert shares into share table
        add_share_query = "INSERT INTO share (expense_id, user, amount) VALUES (%s, %s, %s)"
        for user, share_amount in shares.items():
            self.cursor.execute(add_share_query, (expense_id, user, share_amount))

        # Commit the transaction
        self.db_connection.commit()
    
    def get_amount_owed(self, user):
        # Query to calculate total amount owed by a user to other
        owed_query = "select SUM(amount) from share where expense_id in (select expense_id from expense where paid_by_user = %s)"
        self.cursor.execute(owed_query, (user,))
        amount_owed = self.cursor.fetchone()[0]
        return amount_owed

    def get_amount_owes(self, user):
    # Query to calculate total amount user owes to others
        owes_query = """
            SELECT s.user, SUM(s.amount) AS share_amount
            FROM share s
            JOIN expense e ON s.expense_id = e.expense_id
            WHERE e.paid_by_user != %s AND s.user != %s
            GROUP BY s.user
        """
        self.cursor.execute(owes_query, (user, user))
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            result.append({'user': row[0], 'owes_amount': int(row[1])})
        return result

    def close_connection(self):
        self.cursor.close()
        self.db_connection.close()


# Example Usage
if __name__ == "__main__":
    # Establishing connection to MySQL database
    expense_manager = ExpenseManager(host="localhost", user="root", password="Ambuj123", database="test")
    
    # Add an expense and shares
    expense_manager.add_expense(paid_by_user="ram", amount=300, shares = {'shyam': 100, 'gyan': 100})
    expense_manager.add_expense(paid_by_user="shyam", amount=200, shares = {'ram': 100, 'gyan': 100})
    expense_manager.add_expense(paid_by_user="gyan", amount=400, shares = {'ram': 200, 'shyam': 400})
    
    # Calculate amount owed by a user
    user = 'ram'
    amount_owed = expense_manager.get_amount_owed(user)
    print(f"Amount owed by {user}: {amount_owed}")
    
    # Calculate amount user owes to others
    amount_owes = expense_manager.get_amount_owes(user)
    print(f"Amount {user} owes to others: {amount_owes}")
    
    # Closing database connection
    expense_manager.close_connection()
