# trend-finder

A program that analyzes trending news articles and identifies which topics are trending

## Running the application

1. Initialize virtual environment
```bash
python3.12 -m venv venv
source venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Initialize API keys by creating a `.env`. For more details, see `.env.example`
```
NEWS_API_KEY=yourapikey
AWS_ACCESS_KEY_ID=youraccesskeyid
AWS_SECRET_ACCESS_KEY=yoursecretaccesskey
```
4. Initialize DB connection config by creating a `config.json` in `airflow/dags/handlers`, see [airflow/dags/handlers/config_example.json](airflow/dags/handlers/config.json) as example

5. Install airflow
```bash
sh install_airflow.sh
```

1. Start airflow
```bash
sh start_airflow.sh
```

1. Go to [localhost:8080](http://localhost:8080)
2. Open [./airflow/standalone_admin_password.txt](./airflow/standalone_admin_password.txt) and copy the password
3.  Log in with the username "admin" and the provided password
4.  To execute the trending_news_dag, search for it from the home page and select it:  
![search](/media/search.png)
1.  Start the DAG by clicking "Trigger DAG" in the top right:  
![start](/media/start_dag.png)
1.  You can view the status of your execution on the side panel:  
![status](/media/status.png)
1.  Select the status for a specific task by clicking on its square:  
![status_box](/media/status_box.png)
1.   Select "Logs" to view execution logs:  
![logs](/media/logs.png)
