# Munro

## Problem Statement

BSE publishes a **Bhavcopy** file every day at https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx

1. Develop a python script which does the following :

* Downloads the Equity bhavcopy zip from the above page.
* Extracts and parses the CSV file in it.
* Writes the records into Redis into appropriate data structures (Fields: code, name, open, high, low, close)

2. Develop a simple CherryPy python web application which does the following :

* Renders an HTML5 + CSS3 page that lists the top 10 stock entries from the Redis DB in a table.
* Has a searchbox that lets you search the entries by the `name` field in Redis and renders it in a table.

## Solution (Tested on Python 3.5.2)

**Requirements  -  Redis**
* User can change settings in `config.py`

### Creating Virtual Environment

```sh
virtualenv -p python3 venv
source venv/bin/activate
```

### Installing the dependencies

```sh
pip install -r requirements.txt
```

### Running the script and web app

* Set `APP_CONFIG` enviroment variable (defaults to `production`)

```sh
export APP_CONFIG="development"
```

* Running the script for data of 2 days back
```sh
python stocks.py
```

* Running the script for specific date e.g. 20-06-2019

```sh
python stocks.py 20-06-2019
```

* Running the CherryPy Web App

```sh
python server.py
```