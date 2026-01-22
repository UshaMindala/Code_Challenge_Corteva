
# Weather Data Ingestion & API Service

This project implements an end-to-end weather data pipeline that ingests raw daily weather files, stores them in a relational database, computes yearly summary statistics, and exposes both raw and aggregated data through a FastAPI REST API. The system is designed to be simple, reproducible, and production-oriented, demonstrating data engineering and backend best practices.

## Project Overview

The system consists of three main components:

1. **Data Ingestion Pipeline**  
   Parses raw text weather files, normalizes units, handles missing values, and loads daily observations into the database.

2. **Analytics & Aggregation**  
   Computes yearly aggregated statistics (average temperatures and total precipitation) from daily records and stores results in a separate summary table.

3. **REST API Service**  
   Exposes endpoints to query both raw daily weather data and yearly aggregated statistics with filtering and pagination.

The architecture separates concerns between ingestion, analytics, and API layers, making the system easy to extend and maintain.

## Tech Stack

- Python 3.9+
- FastAPI
- SQLAlchemy ORM
- SQLite (local development)
- PostgreSQL (recommended for production)
- Pydantic
- Docker (optional)
- Git / GitHub

## Project Structure

```
app/
├── main.py          # FastAPI application and API endpoints
├── models.py        # SQLAlchemy ORM models
├── schemas.py       # Pydantic request/response schemas
├── database.py      # Database engine and session management
├── ingestion.py     # Raw weather data ingestion pipeline
├── analysis.py      # Yearly aggregation and analytics
```
 
## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Create a Virtual Environment

```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*Or manually install:*

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### 4. Prepare Data

Place raw weather files in a directory called `wx_data/`:

```
wx_data/
├── USC0010XXXX.txt
├── USC0010YYYY.txt
```

Each file should contain daily records for a single weather station.

## Running the Pipeline

### Step 1: Ingest Raw Weather Data

```bash
python -m app.ingestion
```

- Creates database tables if they don’t exist  
- Reads all `.txt` files in `./wx_data`  
- Inserts daily weather records into the database  

### Step 2: Compute Yearly Statistics

```bash
python -m app.analysis
```

- Aggregates daily records by station and year  
- Computes average max/min temperatures and total precipitation  
- Inserts or updates yearly summary records in the database  

## Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

- API available at: `http://127.0.0.1:8000`  
- Swagger UI: `http://127.0.0.1:8000/docs`  
- ReDoc: `http://127.0.0.1:8000/redoc`  

## API Endpoints

### GET `/api/weather`

Query raw daily weather records.

**Query parameters:**

- `station_id`  
- `date_from` (YYYY-MM-DD)  
- `date_to` (YYYY-MM-DD)  
- `offset` (default: 0)  
- `limit` (default: 100, max: 1000)  

**Example:**  
```
/api/weather?station_id=USC0010XXXX&date_from=2020-01-01
```

### GET `/api/weather/stats`

Query yearly aggregated weather statistics.

**Query parameters:**

- `station_id`   
- `year`  
- `offset` (default: 0)  
- `limit` (default: 100, max: 1000)  

**Example:**  
```
/api/weather/stats?station_id=USC0010XXXX&year=2022
```

## Database Schema

- **stations** — Station metadata  
- **weather_records** — Daily weather observations (one row per station per day)  
- **weather_yearly_stats** — Yearly aggregated summaries (one row per station per year)  

**Unique constraints:**  

- One daily record per station per date  
- One yearly stats record per station per year  

## Extra Credit: AWS Deployment Design

### Services Used

- **Amazon ECS (Fargate)** – Run FastAPI container  
- **Amazon RDS (PostgreSQL)** – Production-grade database  
- **Amazon S3** – Store raw weather data files  
- **AWS Lambda / EventBridge** – Scheduled ingestion & stats jobs  
- **Application Load Balancer (ALB)** – Route traffic  
- **AWS ECR** – Store Docker images  
- **IAM** – Secure service permissions  
- **CloudWatch** – Logging and monitoring  

### Architecture

1. FastAPI app containerized with Docker  
2. Deployed to ECS Fargate behind ALB  
3. RDS PostgreSQL replaces SQLite  
4. Raw data stored in S3  
5. Scheduled ingestion via EventBridge + Lambda or ECS Scheduled Tasks  
6. Secrets managed with AWS Secrets Manager  
7. Logs shipped to CloudWatch  

## Future Improvements

- Migrate SQLite to PostgreSQL for production  
- Add authentication (JWT or OAuth)  
- Add pagination to API endpoints  
- Add automated CI/CD pipeline (GitHub Actions)  
- Add data validation with Great Expectations  
- Add monitoring dashboards

## Author

**Ushasree Mindala**  
Data Engineer  
Expertise: ML, Geospatial and Climate Analytics, Data Engineering, Cloud Pipelines

## License

This project is for educational and assessment purposes.  
Feel free to adapt and extend.
