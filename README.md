# 🚕 Uber Data Engineering Project — End-to-End Pipeline on GCP

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![GCP](https://img.shields.io/badge/Google_Cloud-Platform-orange?logo=googlecloud)
![Mage](https://img.shields.io/badge/Mage.ai-0.9.79-purple)
![BigQuery](https://img.shields.io/badge/BigQuery-Data_Warehouse-blue?logo=googlebigquery)
![Looker](https://img.shields.io/badge/Looker_Studio-Dashboard-green?logo=looker)

---
🛠️ Tools & Technologies
☁️ Cloud Infrastructure
![GCP](https://img.shields.io/badge/Google_Cloud_Platform-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![GCS](https://img.shields.io/badge/Google_Cloud_Storage-AECBFA?style=for-the-badge&logo=googlecloud&logoColor=black)
![Compute Engine](https://img.shields.io/badge/Compute_Engine_(VM)-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
🔄 Pipeline Orchestration
![Mage.ai](https://img.shields.io/badge/Mage.ai-7C3AED?style=for-the-badge&logo=data:image/png;base64,&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
🗄️ Data Warehouse & SQL
![BigQuery](https://img.shields.io/badge/Google_BigQuery-669DF6?style=for-the-badge&logo=googlebigquery&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)
📊 Visualization & Dashboarding
![Looker Studio](https://img.shields.io/badge/Looker_Studio-4285F4?style=for-the-badge&logo=looker&logoColor=white)
💻 Development & Version Control
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Debian](https://img.shields.io/badge/Debian_Linux-A81D33?style=for-the-badge&logo=debian&logoColor=white)
---
📐 What I Did With Each Tool
Tool	How I Used It
GCP Compute Engine	Hosted Mage.ai pipeline on a Debian VM (e2-medium)
Google Cloud Storage	Stored raw `uber_data.csv` (15.8 MB) as a public bucket
Mage.ai	Orchestrated the 3-block ETL pipeline (Loader → Transformer → Exporter)
Python / Pandas	Transformed raw data into star schema — 7 dimension tables + 1 fact table
Google BigQuery	Loaded and queried 100K rows across 8 tables in a cloud data warehouse
SQL	Wrote analytics queries using CTEs, Window Functions, RANK(), CASE WHEN
Looker Studio	Built an interactive dashboard with KPI cards, bar charts, and slicers
GitHub	Version-controlled all pipeline code, SQL queries, and documentation

## 📌 Project Overview

An end-to-end data engineering pipeline built on **Google Cloud Platform** that ingests raw Uber trip data, transforms it into a dimensional data model using **Mage.ai**, loads it into **BigQuery**, and visualizes key metrics in **Looker Studio**.

The project demonstrates core data engineering concepts including ETL pipeline orchestration, dimensional modeling (star schema), cloud infrastructure setup, and business intelligence reporting.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Data Pipeline Flow                           │
│                                                                     │
│  Raw CSV  ──►  GCS Bucket  ──►  Mage.ai (GCP VM)  ──►  BigQuery   │
│  (Local)       (Storage)        (ETL Pipeline)        (Warehouse)  │
│                                       │                     │       │
│                                  Transform             Analytics    │
│                                  & Model               Queries      │
│                                                             │       │
│                                                      Looker Studio  │
│                                                       (Dashboard)   │
└─────────────────────────────────────────────────────────────────────┘
```

**Tech Stack:**

| Layer | Tool |
|---|---|
| Raw Storage | Google Cloud Storage (GCS) |
| Compute | Google Compute Engine (VM — Debian, e2-medium) |
| Orchestration | Mage.ai 0.9.79 |
| Transformation | Python 3.11 (pandas) |
| Data Warehouse | Google BigQuery |
| Visualization | Looker Studio |
| Language | Python, SQL |

---

## 📊 Dataset

**Source:** NYC TLC Uber Trip Data  
**Size:** 100,000 rows × 19 columns  
**File:** `uber_data.csv` (15.8 MB)

| Column | Description |
|---|---|
| VendorID | Taxi vendor identifier |
| tpep_pickup_datetime | Trip pickup timestamp |
| tpep_dropoff_datetime | Trip dropoff timestamp |
| passenger_count | Number of passengers |
| trip_distance | Distance in miles |
| pickup_longitude / latitude | Pickup GPS coordinates |
| dropoff_longitude / latitude | Dropoff GPS coordinates |
| RatecodeID | Rate code (Standard, JFK, Newark, etc.) |
| payment_type | Payment method |
| fare_amount | Base fare |
| tip_amount | Tip amount |
| total_amount | Total charged |

---

## 🗃️ Data Model (Star Schema)

The raw data was transformed into a **star schema** with 1 fact table and 7 dimension tables:

```
                    ┌─────────────────────┐
                    │   datetime_dim      │
                    │─────────────────────│
                    │ datetime_id (PK)    │
                    │ tpep_pickup_datetime│
                    │ pick_hour           │
                    │ pick_day            │
                    │ pick_month          │
                    │ pick_year           │
                    │ pick_weekday        │
                    │ tpep_dropoff_...    │
                    │ drop_hour/day/...   │
                    └──────────┬──────────┘
                               │
┌──────────────────┐           │          ┌─────────────────────┐
│ passenger_       │           │          │  rate_code_dim      │
│ count_dim        │           │          │─────────────────────│
│──────────────────│           │          │ rate_code_id (PK)   │
│ passenger_       │           │          │ RatecodeID          │
│ count_id (PK)    ├───────────┤          │ rate_code_name      │
│ passenger_count  │           │          └──────────┬──────────┘
└──────────────────┘    ┌──────┴───────┐             │
                        │  fact_table  ├─────────────┘
┌──────────────────┐    │──────────────│
│ trip_distance_   │    │ Trip_id (PK) │    ┌─────────────────────┐
│ dim              ├────┤ VendorID     │    │  pickup_location_   │
│──────────────────│    │ datetime_id  ├────┤  dim                │
│ trip_distance_   │    │ passenger_   │    │─────────────────────│
│ id (PK)          │    │ count_id     │    │ pickup_location_    │
│ trip_distance    │    │ trip_dist_id │    │ id (PK)             │
└──────────────────┘    │ rate_code_id │    │ pickup_latitude     │
                        │ pickup_loc_id│    │ pickup_longitude    │
┌──────────────────┐    │ dropoff_loc_ │    └─────────────────────┘
│ payment_type_    │    │ id           │
│ dim              ├────┤ payment_     │    ┌─────────────────────┐
│──────────────────│    │ type_id      ├────┤  dropoff_location_  │
│ payment_type_    │    │ fare_amount  │    │  dim                │
│ id (PK)          │    │ tip_amount   │    │─────────────────────│
│ payment_type     │    │ total_amount │    │ dropoff_location_   │
│ payment_type_    │    │ ...          │    │ id (PK)             │
│ name             │    └──────────────┘    │ dropoff_latitude    │
└──────────────────┘                        │ dropoff_longitude   │
                                            └─────────────────────┘
```

---

## ⚙️ Mage.ai Pipeline

The pipeline consists of 3 blocks orchestrated in Mage.ai running on a GCP VM:

```
load_uber_data  ──►  uber_transformation  ──►  uber_bigquery_load
 (Data Loader)        (Transformer)             (Data Exporter)
```

### Block 1: Data Loader — `load_uber_data.py`

Loads the raw CSV from a public GCS bucket URL into a pandas DataFrame:

```python
import io
import pandas as pd
import requests

@data_loader
def load_data_from_api(*args, **kwargs):
    url = 'https://storage.googleapis.com/uber-data-praveen/uber_data.csv'
    response = requests.get(url)
    return pd.read_csv(io.StringIO(response.text), sep=',')
```

### Block 2: Transformer — `uber_transformation.py`

Transforms the raw DataFrame into 7 dimension tables and 1 fact table (star schema):

```python
@transformer
def transform(data, *args, **kwargs):
    df = data.copy()

    # Convert datetime columns
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df = df.drop_duplicates().reset_index(drop=True)
    df['Trip_id'] = df.index

    # Datetime Dimension
    datetime_dim = df[['tpep_pickup_datetime','tpep_dropoff_datetime']].reset_index(drop=True)
    datetime_dim['pick_hour'] = datetime_dim['tpep_pickup_datetime'].dt.hour
    datetime_dim['pick_day'] = datetime_dim['tpep_pickup_datetime'].dt.day
    datetime_dim['pick_month'] = datetime_dim['tpep_pickup_datetime'].dt.month
    datetime_dim['pick_year'] = datetime_dim['tpep_pickup_datetime'].dt.year
    datetime_dim['pick_weekday'] = datetime_dim['tpep_pickup_datetime'].dt.weekday
    datetime_dim['datetime_id'] = datetime_dim.index

    # Rate Code Dimension
    rate_code_type = {
        1: "Standard rate", 2: "JFK", 3: "Newark",
        4: "Nassau or Westchester", 5: "Negotiated fare", 6: "Group ride"
    }
    rate_code_dim = df[['RatecodeID']].reset_index(drop=True)
    rate_code_dim['rate_code_id'] = rate_code_dim.index
    rate_code_dim['rate_code_name'] = rate_code_dim['RatecodeID'].map(rate_code_type)

    # Payment Type Dimension
    payment_type_name = {
        1: "Credit card", 2: "Cash", 3: "No charge",
        4: "Dispute", 5: "Unknown", 6: "Voided trip"
    }
    payment_type_dim = df[['payment_type']].reset_index(drop=True)
    payment_type_dim['payment_type_id'] = payment_type_dim.index
    payment_type_dim['payment_type_name'] = payment_type_dim['payment_type'].map(payment_type_name)

    # Fact Table (joins all dimensions)
    fact_table = (df.merge(passenger_count_dim, left_on='Trip_id', right_on='passenger_count_id')
                    .merge(trip_distance_dim, left_on='Trip_id', right_on='trip_distance_id')
                    .merge(rate_code_dim, left_on='Trip_id', right_on='rate_code_id')
                    .merge(pickup_location_dim, left_on='Trip_id', right_on='pickup_location_id')
                    .merge(dropoff_location_dim, left_on='Trip_id', right_on='dropoff_location_id')
                    .merge(datetime_dim, left_on='Trip_id', right_on='datetime_id')
                    .merge(payment_type_dim, left_on='Trip_id', right_on='payment_type_id')
                    [['Trip_id','VendorID', 'datetime_id', 'passenger_count_id',
                      'trip_distance_id', 'rate_code_id', 'store_and_fwd_flag',
                      'pickup_location_id', 'dropoff_location_id', 'payment_type_id',
                      'fare_amount', 'extra', 'mta_tax', 'tip_amount',
                      'tolls_amount', 'improvement_surcharge', 'total_amount']])

    return {
        "datetime_dim": datetime_dim,
        "passenger_count_dim": passenger_count_dim,
        "trip_distance_dim": trip_distance_dim,
        "rate_code_dim": rate_code_dim,
        "pickup_location_dim": pickup_location_dim,
        "dropoff_location_dim": dropoff_location_dim,
        "payment_type_dim": payment_type_dim,
        "fact_table": fact_table
    }
```

### Block 3: Data Exporter — `uber_bigquery_load.py`

Loops through all 8 tables in the dictionary and loads each into BigQuery:

```python
@data_exporter
def export_data_to_big_query(data, **kwargs) -> None:
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    for key, value in data.items():
        df = DataFrame(value)
        table_id = f'project-16b0aeb7-f27f-4df7-b8f.uber_data.{key}'
        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            df,
            table_id,
            if_exists='replace',
        )
```

---

## 🗄️ BigQuery Tables

After the pipeline runs, 8 tables are created in the `uber_data` dataset:

| Table | Rows | Description |
|---|---|---|
| `fact_table` | 100,000 | Central fact table with all foreign keys |
| `datetime_dim` | 100,000 | Pickup/dropoff time attributes |
| `passenger_count_dim` | 100,000 | Passenger count per trip |
| `trip_distance_dim` | 100,000 | Trip distance per trip |
| `rate_code_dim` | 100,000 | Rate code with human-readable names |
| `pickup_location_dim` | 100,000 | Pickup GPS coordinates |
| `dropoff_location_dim` | 100,000 | Dropoff GPS coordinates |
| `payment_type_dim` | 100,000 | Payment method with names |

---

## 📝 SQL Analytics Queries

### 1. Total Revenue by Payment Type
```sql
SELECT pay.payment_type_name,
       COUNT(*) as total_trips,
       ROUND(SUM(f.total_amount), 2) as total_revenue
FROM `project-16b0aeb7-f27f-4df7-b8f.uber_data.fact_table` f
JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.payment_type_dim` pay
    ON f.payment_type_id = pay.payment_type_id
GROUP BY pay.payment_type_name
ORDER BY total_revenue DESC;
```

### 2. Average Fare by Hour of Day
```sql
SELECT d.pick_hour,
       COUNT(*) as total_trips,
       ROUND(AVG(f.fare_amount), 2) as avg_fare
FROM `project-16b0aeb7-f27f-4df7-b8f.uber_data.fact_table` f
JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.datetime_dim` d
    ON f.datetime_id = d.datetime_id
GROUP BY d.pick_hour
ORDER BY d.pick_hour;
```

### 3. Busiest Day of the Week
```sql
SELECT
    CASE d.pick_weekday
        WHEN 0 THEN 'Monday' WHEN 1 THEN 'Tuesday' WHEN 2 THEN 'Wednesday'
        WHEN 3 THEN 'Thursday' WHEN 4 THEN 'Friday'
        WHEN 5 THEN 'Saturday' WHEN 6 THEN 'Sunday'
    END as day_name,
    COUNT(*) as total_trips
FROM `project-16b0aeb7-f27f-4df7-b8f.uber_data.fact_table` f
JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.datetime_dim` d
    ON f.datetime_id = d.datetime_id
GROUP BY d.pick_weekday, day_name
ORDER BY total_trips DESC;
```

### 4. Peak Hours — Running Total (Window Function)
```sql
SELECT d.pick_hour,
       COUNT(*) as trips,
       SUM(COUNT(*)) OVER (ORDER BY d.pick_hour) as running_total_trips
FROM `project-16b0aeb7-f27f-4df7-b8f.uber_data.fact_table` f
JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.datetime_dim` d
    ON f.datetime_id = d.datetime_id
GROUP BY d.pick_hour
ORDER BY d.pick_hour;
```

### 5. Average Trip Duration by Rate Code (CTE)
```sql
WITH trip_duration AS (
    SELECT f.Trip_id,
           f.rate_code_id,
           TIMESTAMP_DIFF(d.tpep_dropoff_datetime, d.tpep_pickup_datetime, MINUTE) as duration_minutes
    FROM `project-16b0aeb7-f27f-4df7-b8f.uber_data.fact_table` f
    JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.datetime_dim` d
        ON f.datetime_id = d.datetime_id
)
SELECT r.rate_code_name,
       ROUND(AVG(td.duration_minutes), 2) as avg_duration_minutes
FROM trip_duration td
JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.rate_code_dim` r
    ON td.rate_code_id = r.rate_code_id
GROUP BY r.rate_code_name
ORDER BY avg_duration_minutes DESC;
```

### 6. Revenue Ranking by Hour — RANK()
```sql
SELECT d.pick_hour,
       ROUND(SUM(f.total_amount), 2) as total_revenue,
       RANK() OVER (ORDER BY SUM(f.total_amount) DESC) as revenue_rank
FROM `project-16b0aeb7-f27f-4df7-b8f.uber_data.fact_table` f
JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.datetime_dim` d
    ON f.datetime_id = d.datetime_id
GROUP BY d.pick_hour
ORDER BY revenue_rank;
```

### 7. Full Analytics Query (All Dimensions Joined)
```sql
SELECT
    f.Trip_id,
    d.tpep_pickup_datetime,
    CASE d.pick_hour
        WHEN 0 THEN '12AM' WHEN 1 THEN '1AM' WHEN 2 THEN '2AM'
        WHEN 3 THEN '3AM' WHEN 4 THEN '4AM' WHEN 5 THEN '5AM'
        WHEN 6 THEN '6AM' WHEN 7 THEN '7AM' WHEN 8 THEN '8AM'
        WHEN 9 THEN '9AM' WHEN 10 THEN '10AM' WHEN 11 THEN '11AM'
        WHEN 12 THEN '12PM' WHEN 13 THEN '1PM' WHEN 14 THEN '2PM'
        WHEN 15 THEN '3PM' WHEN 16 THEN '4PM' WHEN 17 THEN '5PM'
        WHEN 18 THEN '6PM' WHEN 19 THEN '7PM' WHEN 20 THEN '8PM'
        WHEN 21 THEN '9PM' WHEN 22 THEN '10PM' WHEN 23 THEN '11PM'
    END as pick_hour,
    CASE d.pick_weekday
        WHEN 0 THEN 'Monday' WHEN 1 THEN 'Tuesday' WHEN 2 THEN 'Wednesday'
        WHEN 3 THEN 'Thursday' WHEN 4 THEN 'Friday'
        WHEN 5 THEN 'Saturday' WHEN 6 THEN 'Sunday'
    END as pick_weekday,
    p.passenger_count,
    t.trip_distance,
    r.rate_code_name,
    pay.payment_type_name,
    f.fare_amount,
    f.tip_amount,
    f.total_amount
FROM `project-16b0aeb7-f27f-4df7-b8f.uber_data.fact_table` f
JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.datetime_dim` d ON f.datetime_id = d.datetime_id
JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.passenger_count_dim` p ON f.passenger_count_id = p.passenger_count_id
JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.trip_distance_dim` t ON f.trip_distance_id = t.trip_distance_id
JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.rate_code_dim` r ON f.rate_code_id = r.rate_code_id
JOIN `project-16b0aeb7-f27f-4df7-b8f.uber_data.payment_type_dim` pay ON f.payment_type_id = pay.payment_type_id
LIMIT 100;
```

---

## 📈 Looker Studio Dashboard

The dashboard includes interactive filters and the following KPIs:

| Metric | Value |
|---|---|
| Total Passenger Count | 192.9K |
| Total Revenue | $1.33M |
| Average Trip Distance | 3.0 km |
| Average Fare Amount | $13.25 |
| Average Tip Amount | $1.87 |

**Filters:** VendorID, Payment Type, Rate Code, Trip Distance slider

**Charts:**
- Total amount by Rate Code (bar chart)
- Total amount by Payment Type (bar chart)

---

## 🔧 GCP Infrastructure

| Component | Details |
|---|---|
| VM Name | uber-instance |
| Machine Type | e2-medium |
| OS | Debian 13 (Trixie) |
| Region | northamerica-northeast2-a |
| Storage | 10 GB Balanced Persistent Disk |
| GCS Bucket | uber-data-praveen (US Multi-region) |
| BigQuery Dataset | uber_data (US Multi-region) |

---

## 🚀 How to Reproduce

### Prerequisites
- Google Cloud account with billing enabled
- Python 3.11
- GCP SDK installed locally

### Steps

**1. Set up GCS Bucket**
- Create a bucket and upload `uber_data.csv`
- Set public access for `allUsers` with `Storage Object Viewer` role

**2. Create GCP VM**
```bash
# SSH into VM, then install dependencies
sudo apt-get update -y
sudo apt-get install python3-apt wget git -y
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py --break-system-packages
```

**3. Install Python 3.11 via pyenv**
```bash
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl libffi-dev liblzma-dev
curl https://pyenv.run | bash
# Add pyenv to .bashrc, then:
pyenv install 3.11.9
pyenv local 3.11.9
python -m venv mage-env
source mage-env/bin/activate
```

**4. Install Mage.ai**
```bash
pip install mage-ai
pip install pandas==2.2.3
pip install google-cloud-bigquery db-dtypes
```

**5. Start Mage**
```bash
nohup mage start uberdataproject > mage.log 2>&1 &
# Access at http://YOUR_EXTERNAL_IP:6791
```

**6. Configure BigQuery**
- Attach service account to VM with BigQuery Admin + Storage Admin roles
- Update `io_config.yaml`:
```yaml
version: 0.1.1
default:
  GOOGLE_SERVICE_ACC_KEY_FILEPATH: null
  GOOGLE_LOCATION: US
```

**7. Run Pipeline**
- Run `load_uber_data` → `uber_transformation` → `uber_bigquery_load` in sequence

**8. Connect Looker Studio**
- Go to lookerstudio.google.com
- Create new report → Connect BigQuery → Select `uber_data` dataset

---

## 💡 Key Insights

- **Credit card** is the dominant payment method by revenue
- **Nassau or Westchester** and **Newark** rate codes generate the highest average fares
- Trip volume peaks during **evening rush hours**
- Average tip rate varies significantly by **passenger count**

---

## 📁 Repository Structure

```
uber-data-engineering-project/
│
├── README.md
├── uber_data.csv                      ← Raw dataset
│
├── mage_pipeline/
│   ├── load_uber_data.py              ← Data loader block
│   ├── uber_transformation.py         ← Transformer block
│   └── uber_bigquery_load.py          ← BigQuery exporter block
│
├── sql_queries/
│   └── analytics_queries.sql          ← All analytics SQL queries
│
└── screenshots/
    ├── mage_pipeline.png              ← Mage pipeline view
    ├── gcs_bucket.png                 ← GCS bucket with CSV
    ├── bigquery_tables.png            ← BigQuery 8 tables
    └── looker_dashboard.png           ← Looker Studio dashboard
```

---

## 👨‍💻 Author

**Praveen** — Operations/Data Lead | M.Eng Data Analytics, University of Toronto

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com)
