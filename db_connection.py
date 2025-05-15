"""
db_connection.py - Database connection module for College Event Participation Tracker
"""

import mysql.connector
from mysql.connector import Error
import os
from getpass import getpass
import configparser
import sys


class DatabaseConnection:
    """Class to handle database connections and basic operations"""

    def __init__(self, config_file='config.ini'):
        """Initialize the database connection"""
        self.connection = None
        self.cursor = None
        self.config_file = config_file
        self.connect()

    def create_config_if_not_exists(self):
        """Create a new configuration file if it doesn't exist"""
        if not os.path.exists(self.config_file):
            print("\n" + "="*60)
            print(" First time setup: Database Configuration")
            print("="*60)
            print("\nPlease provide your MySQL database credentials:")
            
            config = configparser.ConfigParser()
            config['DATABASE'] = {
                'Host': input('Host [localhost]: ') or 'localhost',
                'User': input('Username [root]: ') or 'root',
                'Password': getpass('Password [leave empty for no password]: ') or '',
                'Database': input('Database name [college_events]: ') or 'college_events'
            }
            
            try:
                with open(self.config_file, 'w') as configfile:
                    config.write(configfile)
                print("\nConfiguration saved successfully! You can edit it later in config.ini")
            except Exception as e:
                print(f"Error creating configuration file: {e}")
                sys.exit(1)

    def read_config(self):
        """Read database configuration from file"""
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        return {
            'host': config['DATABASE']['Host'],
            'user': config['DATABASE']['User'],
            'password': config['DATABASE']['Password'],
            'database': config['DATABASE']['Database']
        }

    def connect(self):
        """Connect to the MySQL database"""
        try:
            # Create config file if it doesn't exist
            self.create_config_if_not_exists()
            
            # Read configuration
            db_config = self.read_config()
            
            # Connect to the database
            self.connection = mysql.connector.connect(**db_config)
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print(f"Connected to MySQL database: {db_config['database']}")
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            
            # Handle database not existing
            if "Unknown database" in str(e):
                try:
                    # Connect without specifying database to create it
                    db_config = self.read_config()
                    db_name = db_config['database']
                    del db_config['database']
                    
                    self.connection = mysql.connector.connect(**db_config)
                    self.cursor = self.connection.cursor()
                    
                    # Create database and tables from schema file
                    print(f"Creating database '{db_name}'...")
                    self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                    self.cursor.execute(f"USE {db_name}")
                    
                    # Read and execute schema file
                    try:
                        with open('database_schema.sql', 'r') as schema_file:
                            schema_sql = schema_file.read()
                            
                            # Split schema into individual statements
                            statements = schema_sql.split(';')
                            for statement in statements:
                                if statement.strip():
                                    self.cursor.execute(statement)
                            
                            self.connection.commit()
                            print("Database schema created successfully!")
                            
                            # Reconnect with the new database
                            self.cursor.close()
                            self.connection.close()
                            
                            # Update config with the new database
                            db_config['database'] = db_name
                            self.connection = mysql.connector.connect(**db_config)
                            self.cursor = self.connection.cursor(dictionary=True)
                            
                    except FileNotFoundError:
                        print("Schema file not found. Manual database setup required.")
                        sys.exit(1)
                except Error as create_error:
                    print(f"Error creating database: {create_error}")
                    sys.exit(1)

    def execute_query(self, query, params=None):
        """Execute a query and commit changes"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            return False

    def fetch_all(self, query, params=None):
        """Execute a query and fetch all results"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return []

    def fetch_one(self, query, params=None):
        """Execute a query and fetch one result"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

    def close(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")


# Create a singleton instance for global use
db = DatabaseConnection()


# For testing the connection
if __name__ == "__main__":
    test_db = DatabaseConnection()
    result = test_db.fetch_all("SELECT VERSION() as version")
    print(f"MySQL Version: {result[0]['version'] if result else 'Unknown'}")
    test_db.close()
