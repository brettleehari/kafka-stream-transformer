from kafka import KafkaConsumer
import threading
import json
import queue
import asyncio

class KafkaConsumerManager:
    def __init__(self):
        self.consumer = None
        self.queue = queue.Queue()
        self.thread = None
        self.running = False

    def connect(self, config):
        if self.consumer:
            self.running = False
            if self.thread:
                self.thread.join()
        self.consumer = KafkaConsumer(
            config['topic'],
            bootstrap_servers=config['server'],
            group_id=config['group_id'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        self.running = True
        self.thread = threading.Thread(target=self._consume)
        self.thread.start()

    def _consume(self):
        for msg in self.consumer:
            if not self.running:
                break
            self.queue.put(msg.value)

    async def stream(self):
        while True:
            try:
                msg = self.queue.get(timeout=1)
                yield msg
            except queue.Empty:
                await asyncio.sleep(0.1)

