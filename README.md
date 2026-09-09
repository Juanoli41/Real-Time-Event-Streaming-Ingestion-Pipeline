# Real-Time Event Streaming Ingestion Pipeline

A simple real-time event pipeline using:

- **Redpanda (Kafka API)** as the broker
- **Python producer** to generate events
- **Python consumer** to ingest events into **PostgreSQL**
- **Docker Compose** for local infrastructure

---

## Project Structure

```text
.
├── docker-compose.yml
├── producer.py
├── consumer.py
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

---

## How It Works

1. `producer.py` creates synthetic user events and publishes to Kafka topic `user_events`.
2. `consumer.py` reads from `user_events`.
3. Consumer inserts each event into PostgreSQL table `user_events`.

---

## Prerequisites

- Docker Desktop
- Python 3.10+
- Git

---

## Setup

### 1) Clone repo

```bash
git clone https://github.com/Juanoli41/Real-Time-Event-Streaming-Ingestion-Pipeline.git
cd Real-Time-Event-Streaming-Ingestion-Pipeline
```

### 2) Create and activate virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install kafka-python psycopg2-binary faker
```

### 4) Configure environment variables

Create local `.env` from template:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

Edit `.env` and set a real local password for `DB_PASSWORD`.

---

## Run the Project

### 1) Start infrastructure

```bash
docker compose up -d
```

### 2) Run consumer (Terminal 1)

```bash
python consumer.py
```

### 3) Run producer (Terminal 2)

```bash
python producer.py
```

You should see producer events in terminal output and consumer insert confirmations.

---

## Verify Data in PostgreSQL

```bash
docker exec -it postgres_db psql -U postgres -d streaming_db -c "SELECT * FROM user_events ORDER BY id DESC LIMIT 10;"
```

---

## Stop Infrastructure

```bash
docker compose down
```

To remove containers, volumes, and local images:

```bash
docker compose down --rmi local --volumes --remove-orphans
```

---

## Configuration

`consumer.py` reads:

- `DB_NAME` (default: `streaming_db`)
- `DB_USER` (default: `postgres`)
- `DB_PASSWORD` (**required**)
- `DB_HOST` (default: `localhost`)
- `DB_PORT` (default: `5432`)
- `KAFKA_BOOTSTRAP_SERVERS` (default: `localhost:9092`)
- `KAFKA_GROUP_ID` (default: `user-events-group-1`)

---

## Security Notes

- Do **not** commit `.env`.
- Commit only `.env.example` with placeholders.
- Rotate credentials immediately if exposed.

Quick scan before commit:

```bash
git grep -nEi "password|secret|token|api[_-]?key|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY"
```

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE).