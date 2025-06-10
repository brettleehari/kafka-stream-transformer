from fastapi import FastAPI, WebSocket, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .kafka_consumer import KafkaConsumerManager
from .transform import SchemaTransformer
from kafka import KafkaAdminClient
import logging

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

# Set up logging with timestamp
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

kafka_manager = KafkaConsumerManager()
transformer = SchemaTransformer()

@app.post('/connect')
async def connect_kafka(config: dict):
    try:
        logger.info(f"Received connect request: {config}")
        kafka_manager.connect(config)
        logger.info("Kafka connected successfully.")
        return {'status': 'connected'}
    except Exception as e:
        logger.error(f"Kafka connection failed: {e}")
        raise HTTPException(status_code=400, detail=f"Kafka connection failed: {str(e)}. Please check your server, topic, and group ID.")

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async for message in kafka_manager.stream():
        transformed = transformer.transform(message)
        await websocket.send_json({'raw': message, 'transformed': transformed})

@app.post('/schema')
async def set_schema(schema: dict):
    transformer.set_schema(schema)
    return {'status': 'schema set'}

@app.get('/')
async def index():
    with open('static/index.html') as f:
        return HTMLResponse(f.read())

@app.get('/schema')
async def schema_page():
    with open('static/schema.html') as f:
        return HTMLResponse(f.read())

@app.post('/check-kafka')
async def check_kafka(config: dict):
    try:
        logger.info(f"Checking Kafka server: {config['server']}")
        admin = KafkaAdminClient(
            bootstrap_servers=config['server'],
            client_id='kafka-checker',
            request_timeout_ms=3000
        )
        admin.list_topics()
        admin.close()
        logger.info("Kafka server is accessible!")
        return {'status': 'Kafka server is accessible!'}
    except Exception as e:
        logger.error(f"Kafka server is not accessible: {e}")
        raise HTTPException(status_code=400, detail=f"Kafka server is not accessible: {str(e)}. Please check your server, topic, and group ID.")
