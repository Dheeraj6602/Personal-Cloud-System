import sqlite3

# Connect to the database
conn = sqlite3.connect('cloud_storage.db')
c = conn.cursor()

# Execute a query to retrieve data
c.execute('SELECT * FROM Users')
users_data = c.fetchall()

c.execute('SELECT * FROM Files')
files_data = c.fetchall()

c.execute('SELECT * FROM Folders')
folders_data = c.fetchall()

c.execute('SELECT * FROM Shares')
shares_data = c.fetchall()

# Print the data
print("Users Table:")
for row in users_data:
    print(row)

print("\nFiles Table:")
for row in files_data:
    print(row)

print("\nFolders Table:")
for row in folders_data:
    print(row)

print("\nShares Table:")
for row in shares_data:
    print(row)

# Close the connection
conn.close()

# Connect to the database
conn = sqlite3.connect('cloud_storage.db')
c = conn.cursor()

# Get table names
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()

# Iterate through tables
for table in tables:
    table_name = table[0]
    print(f"\nTable: {table_name}")

    # Get column names and types
    c.execute(f"PRAGMA table_info({table_name});")
    columns = c.fetchall()

    # Print column names and types
    for column in columns:
        column_name = column[1]
        data_type = column[2]
        print(f"{column_name}: {data_type}")

# Close the connection
conn.close()


