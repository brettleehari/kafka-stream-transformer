# Kafka Stream Transformer

**Real-time Kafka message streaming with live WebSocket dashboard and schema-based transformations.**

A Python microservice that connects to any Kafka cluster, consumes messages, applies user-defined schema transformations, and displays results through a live browser dashboard via WebSocket.

## Features

- **Real-time streaming** — Consumes messages from Kafka topics with live WebSocket updates to the browser
- **Schema-based transformations** — Define JSON schemas to validate and transform messages on the fly
- **Dynamic configuration** — Set broker addresses, topic names, and consumer group IDs through the web UI
- **Built-in test producer** — Automated message generator for development and demos
- **Fully containerised** — Docker Compose setup for the entire stack (Kafka + Zookeeper + app)

## Architecture

```
Kafka Cluster --> Python Consumer --> Schema Validation --> WebSocket --> Browser Dashboard
                  (kafka-python)      (JSONSchema)          (FastAPI)     (Live updates)
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI, Uvicorn |
| **Messaging** | Kafka-Python |
| **Validation** | Pydantic, JSONSchema |
| **Frontend** | HTML/CSS/JavaScript (WebSocket client) |
| **Infra** | Docker, Docker Compose |

## Quickstart

```bash
git clone https://github.com/brettleehari/kafka-stream-transformer.git
cd kafka-stream-transformer
docker-compose up -d
# Open http://localhost:8000
```

## Author

**Hariprasad Sudharshan** - [GitHub](https://github.com/brettleehari)

## License

MIT
