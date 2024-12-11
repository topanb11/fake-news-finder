# trend-finder

A program that analyzes trending news articles and identifies which topics are trending

## Running the application

1. Initialize virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Initialize API key by creating a `.env`. For more details, see `.env.example`

### Starting Airflow

1. Install airflow: `sh install_airflow.sh`
2. Start airflow: `sh start_airflow.sh`
   1. Note: This script executes `airflow standalone` which spins up a fresh instance of airflow. This means it uses a fresh new SQLite DB each time (data is not persisted).
3. Go to [localhost:8080](localhost:8080)
4. Open [./airflow/standalone_admin_password.txt](./airflow/standalone_admin_password.txt) and copy the username and password
5. Log in with the provided username and password
