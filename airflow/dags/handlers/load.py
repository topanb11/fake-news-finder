import json
import psycopg2

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
        article_id SERIAL PRIMARY KEY,
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
    INSERT INTO news_article (article_id, topic, title, description, source_id, source_name, author, published_date, content)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (article_id) DO NOTHING; -- Handle duplicate primary keys
    """
    try:
        with connection.cursor() as cursor:
            for record in data:
                cursor.execute(insert_query, (
                    record["article_id"],
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


# helper function to look inside DB
def fetch_all_records(connection):
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
    


def load_articles(**kwargs):
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

    # Step 4: Read data from transform function
    cleaned_data = kwargs["ti"].xcom_pull(
        task_ids="fetch_cleaned_headlines", key="cleaned_headlines"
    )

    # Step 5: Insert data into the database
    insert_data(connection, cleaned_data)


    # Step 5: Close the connection
    connection.close()
    print("Pipeline completed successfully.")
