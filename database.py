import sqlite3

import pandas as pd


class BaseDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """ Connect to SQLite database """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def table_exists(self, table_name):
        # Query to check if table exists
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        # Execute the query
        self.cursor.execute(query)
        # Fetch one result
        result = self.cursor.fetchone()
        # Return True if a result is found (table exists), False otherwise
        return result is not None

    def create_table(self, table_name, columns_dict):
        """ Create a table dynamically """
        # Construct columns string with data types
        columns = ', '.join([f"{column} {data_type}" for column, data_type in columns_dict.items()])

        # Construct and execute the SQL CREATE TABLE statement
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(sql)

    def insert_data(self, table_name, data_dict):
        """ Insert data into the table dynamically """
        # Extract column names and values from data_dict
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join('?' * len(data_dict))
        values = tuple(data_dict.values())

        # Construct and execute the SQL INSERT statement
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, values)

    def update_data(self, table_name, data_dict, condition):
        columns = ', '.join([f"{column} = ?" for column in data_dict.keys()])
        values = list(data_dict.values())
        values.append(condition[1])

        query = f"""
        UPDATE {table_name}
        SET {columns}
        WHERE {condition[0]} = ?
        """
        self.cursor.execute(query, values)

    def fetch_all_data(self, table_name):
        """ Fetch all data from the table """
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def fetch_column(self, table, column):
        self.cursor.execute(f"SELECT {column} FROM {table}")
        return self.cursor.fetchall()

    def fetch_columns(self, table, column, filter_query: tuple):
        q_str = f"SELECT {column} FROM {table} WHERE {filter_query[0]} = ?"
        params = (filter_query[1],)
        self.cursor.execute(q_str, params)
        return self.cursor.fetchall()

    def fetch_row(self, table, condition: tuple):
        self.cursor.execute(f"SELECT * FROM {table} WHERE {condition[0]} = ?", (condition[1],))
        return self.cursor.fetchone()

    def update_row(self, table, update_data, condition):
        try:
            # Construct the SET clause of the SQL query
            set_clause = ', '.join(f"{key} = ?" for key in update_data.keys())

            # Construct the UPDATE query
            query = f"UPDATE {table} SET {set_clause} WHERE {condition[0]} = ?"
            params = list(update_data.values()) + [condition[1]]

            # Execute the update query
            self.cursor.execute(query, params)

            # Commit the transaction
            self.commit_changes()
            return True
        except sqlite3.Error as e:
            print(f"Error updating row: {e}")
            return False

    def delete_row(self, table_name: str, condition: tuple):
        try:
            # Construct the DELETE query
            query = f"DELETE FROM {table_name} WHERE {condition[0]} = ?"
            params = (condition[1],)

            # Execute the delete query
            cursor = self.conn.cursor()
            cursor.execute(query, params)

            # Commit the transaction
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting row: {e}")
            return False

    def commit_changes(self):
        """ Commit changes to the database """
        self.conn.commit()

    def close_connection(self):
        """ Close connection to the database """
        self.conn.close()

    def count_where(self, table, column: str, condition: tuple):
        self.conn.execute(f"""SELECT COUNT(*) FROM {table} WHERE {condition[0]} = ?""", (condition[1],))
        return self.cursor.fetchone()
