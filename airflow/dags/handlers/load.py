import json
import psycopg2
import pandas as pd

# Function to load database configuration from a JSON file
def load_db_config(config_file="config.json"):
    try:
        with open(config_file, "r") as file:
            config = json.load(file)
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

# Function to connect to PostgreSQL
def connect_to_db(config):
    try:
        connection = psycopg2.connect(**config)
        print("Connected to the database successfully.")
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to create the news_article table
def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS news_article (
        id SERIAL PRIMARY KEY,
        topic VARCHAR(100),
        title TEXT NOT NULL,
        description TEXT,
        source_id VARCHAR(50),
        source_name VARCHAR(100),
        author VARCHAR(100),
        published_date DATE,
        content TEXT
    );
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
            print("Table 'news_article' created successfully (if it didn't already exist).")
    except Exception as e:
        print(f"Error creating table: {e}")


# Function to insert data into the news_article table
def insert_data(connection, data):
    insert_query = """
    INSERT INTO news_article (id, topic, title, description, source_id, source_name, author, published_date, content)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING; -- Handle duplicate primary keys
    """
    try:
        with connection.cursor() as cursor:
            for record in data:
                cursor.execute(insert_query, (
                    record["id"],
                    record["topic"],
                    record["title"],
                    record["description"],
                    record["source_id"],
                    record["source_name"],
                    record["author"],
                    record["published_date"],
                    record["content"]
                ))
            connection.commit()
            print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")


def fetch_all_records(connection):
    """
    Fetch and display all records from the 'users' table.

    Args:
        connection (psycopg2.extensions.connection): An active PostgreSQL database connection.

    Returns:
        list: A list of tuples containing all records from the 'users' table.
    """
    query = "SELECT * FROM news_article;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()  # Fetch all rows
            print("All Records:")
            for record in records:
                print(record)
            return records
    except Exception as e:
        print(f"Error fetching records: {e}")
        return []


def main():
    # Step 1: Load database configurations
    db_config = load_db_config()
    if not db_config:
        return
    
    # Step 2: Connect to the database
    connection = connect_to_db(db_config)
    if not connection:
        return

    # Step 3: Create the table (if necessary)
    create_table(connection)

    # Step 4: Read JSON file
    with open("data.json", "r") as json_file:
        data = json.load(json_file)

    # Optional: Load data into a DataFrame (if needed for preprocessing)
    # df = pd.DataFrame(data)
    # print("Data Preview:\n", df)

    # Step 5: Insert data into the database
    insert_data(connection, data)

    # checking to see if records updated in database
    # fetch_all_records(connection)

    # Step 5: Close the connection
    connection.close()
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()



# def load_articles():
#     print("Loading articles to DB...")
#         # Step 1: Connect to the database
#     connection = connect_to_db(DB_CONFIG)
#     if not connection:
#         return

#     # Step 2: Create the table (if necessary)
#     create_table(connection)

#     # Step 3: Read JSON file
#     with open("data.json", "r") as json_file:
#         data = json.load(json_file)

#     # Optional: Load data into a DataFrame (if needed for preprocessing)
#     df = pd.DataFrame(data)
#     print("Data Preview:\n", df)

#     # Step 4: Insert data into the database
#     insert_data(connection, data)
#     fetch_all_records(connection)

#     # Step 5: Close the connection
#     connection.close()
#     print("Pipeline completed successfully.")
