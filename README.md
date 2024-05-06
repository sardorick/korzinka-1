# Korzinka Click Processing ETL

I have set up the ETL process to extract, transform and load the clicks database as provided. This project works with Python, Pandas libraries and Airflow as an ETL tool. 

## Project Overview

The first step I took to work on the project was to do research on data. The data provided shows each individiual click from different sources (Korzinka, LeBazar, social media, etc.) and some characteristics, such as IP, time of the click, location of the click, device of the click user, etc. This data can be useful for analyzing many things, such as:
- when customers are clicking the most, 
- what are the locations that clicks are coming from, 
- where improvements can be made, 
- which available channels are generating the most clicks,
- what is the platform generating most and least clicks and where focus can be improved.

So, to analyze the data, I had to structure the data into SQL tables which can then be connected to various BI platforms to make graphs and reports. Since the amount of data is quite big and I wanted to make the ETL scalable, I chose PostgreSQL as database and Apache Airflow as ETL automated tool. With the help of this tool, we can make it so that each day's data is extracted once a day and then loaded so that it works flawlessly.

## Project Structure

extract.py: Python script responsible for fetching the raw JSON click data.
transform.py: Python script that cleans, transforms, and prepares the data for loading.
dag.py: The Airflow DAG defining the ETL workflow steps.
data: A directory to store the raw JSON (clicks.json) and the transformed CSV (clicks_transformed.csv).
sql: Contains a SQL script (create_tables.sql) for initializing the PostgreSQL tables.

## Setup

Clone the Repository:

Bash
git clone https://github.com/sardorick/korzinka-1

## Install Dependencies:

cd korzinka-1
pip install -r requirements.txt 


Modify Configuration (if needed):

Database Connection: Set up a PostgreSQL connection with the ID analytics_db in your Airflow connections. 


## Running the ETL

Start Airflow: In your project directory, initialize and start the Airflow webserver and scheduler. (airflow webserver & airflow scheduler)

Access Airflow UI: Open the Airflow web interface (typically at http://localhost:8080) and unpause the 'korzinka_click_processing' DAG.

Manually Trigger (optional): If desired, you can manually trigger a DAG run.

This ETL will extract the JSON file from the Google Drive link once a day, transforms the data and saves it into a JSON, and loads it into a database.

The reasoning behind the DAG is that it is automated using Airflow and we don't need to do it manually every day. Given the data is in Google drive, it is not necessary to download it each day since it is going to be the same file, but if the link was a changing file or an API request that would update data on daily basis, it would be useful to get data. The frequency of ETL can be changed to weekly, etc.

## Database Table

The ETL loads the processed data into a PostgreSQL table named clicks. Here's its structure:

Column  Name | Data Type | Description
click_id	integer	Unique identifier for each click
publisher_id	integer	Identifier for the publisher/source
click_timestamp	integer	Click event timestamp (seconds since Unix epoch)
click_date	date	Date of the click
click_time	time	Time of day when the click occurred
country_iso_code	varchar(2)	2-letter country code for the user
city	varchar	User's city
os_name	varchar	Operating system name
os_version	varchar	Operating system version
browser	varchar	User's web browser
browser_version	varchar	Web browser version
device_type	varchar	Device type (e.g., 'Desktop', 'Mobile')
publisher_category	varchar	Categorized publisher source

<image>ER.png<image>