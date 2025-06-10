# Kafka Streaming Microservice with Live Web Frontend for prototyping

## Overview
This project is a Python-based microservice that connects to a Kafka cluster, streams messages from a specified topic, transforms the data based on user-defined schemas, and displays both raw and transformed messages in real time via a modern web frontend. 

**Features:**
- Connect to any Kafka cluster (local or cloud) with user-provided server, topic, and group ID.
- Live stream messages from Kafka and display them in the browser.
- User-defined JSON schema validation and transformation.
- Responsive, modern frontend (HTML/CSS/JS) served by FastAPI.
- WebSocket-based real-time updates.
- Docker and docker-compose support for easy local deployment.

---

## Folder Structure
```
app/
  main.py            # FastAPI app
  kafka_consumer.py  # Kafka consumer logic
  transform.py       # Schema transformation logic
static/
  index.html         # Main frontend (subscription + live stream)
  schema.html        # (Optional) Schema input and transformation UI
Dockerfile           # For containerizing the app
requirements.txt     # Python dependencies
README.md            # This file
```

---

## Quick Start

### 1. Clone the Repository
```bash
git clone 
cd 
```

### 2. Install Python Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start a Local Kafka Cluster (Optional, for local testing)
If you don't have a Kafka cluster, use Docker Compose:
```bash
docker-compose up --build -d
```
This will start Zookeeper and Kafka on `localhost:9092`.

### 4. Run the FastAPI Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Open the Frontend
Go to [http://localhost:8000](http://localhost:8000) in your browser.

---

## Usage
1. **Enter Kafka details** (server, topic, group ID) in the top form and connect.
2. **See live messages** from Kafka in the lower half of the page.
3. **(Optional)** Use `/static/schema.html` to define input/output schemas and transformation mapping.
4. **Produce test messages** to Kafka (example):
   ```bash
   echo '{"username": "alice", "age": 30, "email": "alice@example.com"}' | \
   kafka-console-producer --broker-list localhost:9092 --topic test_topic
   ```

---

## Example Schemas
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "username": {"type": "string"},
    "age": {"type": "integer"},
    "email": {"type": "string"}
  },
  "required": ["username", "age", "email"]
}
```
**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "user": {"type": "string"},
    "years": {"type": "integer"}
  },
  "required": ["user", "years"]
}
```
**Mapping:**
```json
{
  "user": "username",
  "years": "age"
}
```

---

## requirements.txt
```
fastapi>=0.115.0
kafka-python>=2.2.0
uvicorn>=0.34.0
pydantic>=2.11.0
jsonschema>=4.23.0
```

---

## Docker
To run everything in Docker:
```bash
docker-compose up --build
```
- App will be on [http://localhost:8000](http://localhost:8000)
- Kafka will be on `localhost:9092`

---

## Setting Up a Local Testing Environment

### 1. Start the Services
Start Zookeeper, Kafka, and the app:
```bash
docker-compose up --build -d
```

### 2. Produce Test Messages to a Kafka Topic
Open a shell in the running Kafka container:
```bash
docker exec -it kafka bash
```

Then, use the Kafka console producer to send messages to a topic (e.g., `test_topic`):
```bash
kafka-console-producer.sh --broker-list localhost:9092 --topic test_topic
```
Type your JSON messages (one per line), for example:
```
{"username": "alice", "age": 30, "email": "alice@example.com"}
{"username": "bob", "age": 25, "email": "bob@example.com"}
```
Press `Ctrl+C` to exit the producer.

### 3. (Optional) Consume Messages from a Topic
To verify messages, you can consume them with a specific group ID:
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test_topic --group test_group --from-beginning
```

- The topic (e.g., `test_topic`) and group ID (e.g., `test_group`) must match what you enter in the web frontend.
- You can produce messages from any terminal, or script the producer for automated testing.

### 4. (Optional) Automate Kafka Producer for Testing
You can use the provided script to automatically produce random messages to your Kafka topic every 10 seconds:

#### Run on your local machine:
```bash
python app/kafka_auto_producer.py
```

#### Run inside Docker Compose:
Add this service to your `docker-compose.yml`:
```yaml
  producer:
    build: .
    command: python app/kafka_auto_producer.py
    environment:
      - KAFKA_SERVER=kafka:9092
      - KAFKA_TOPIC=test_topic
    depends_on:
      - kafka
```
Then start it with:
```bash
docker-compose up --build -d producer
```

This will send a random test message to the topic (default: `test_topic`) every 10 seconds. You can edit the script or environment variables to change the topic, interval, or message pool.


---

## License
MIT License

---

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
