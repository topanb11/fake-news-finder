import json
import psycopg2
import os

# "./config.json"
# Function to load database configuration from a JSON file
def load_db_config(path):
    config_file = path + "/airflow/dags/handlers/config.json"
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
        article_id VARCHAR(64) PRIMARY KEY,
        topic VARCHAR(100),
        title TEXT NOT NULL,
        description TEXT,
        source_id VARCHAR(50),
        source_name VARCHAR(100),
        author VARCHAR(100),
        published_date DATE,
        polarity NUMERIC(3,2),
        subjectivity NUMERIC(3,2)
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
    INSERT INTO news_article (article_id, topic, title, description, source_id, source_name, author, published_date, polarity, subjectivity)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                    record["polarity"],
                    record["subjectivity"]
                ))
            connection.commit()
            print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")


def load_articles(**kwargs):
    print("Loading articles to DB...")
    path_to_file = os.getcwd()

    # Step 1: Load database configurations
    db_config = load_db_config(path_to_file)
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
        task_ids="transform_articles", key="cleaned_headlines"
    )

    # Step 5: Insert data into the database
    insert_data(connection, cleaned_data)

    # Step 5: Close the connection
    connection.close()
    print("Pipeline completed successfully.")
