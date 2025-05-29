from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import json
import pika
import threading
import time
import os

app = Flask(__name__)
CORS(app)

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

events = []

def setup_rabbitmq_consumer():
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            events.append(message)
        
            redis_client.set('events', json.dumps(events))
            print(f"Mensagem recebida: {message}")
        except Exception as e:
            print(f"Erro: {e}")

    while True:
        try:
            rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(rabbitmq_host)
            )
            channel = connection.channel()
            channel.queue_declare(queue='logistics_queue')
            channel.basic_consume(
                queue='logistics_queue',
                on_message_callback=callback,
                auto_ack=True
            )
            print("Consumindo mensagens da fila 'logistics_queue'...")
            channel.start_consuming()
        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(5)

threading.Thread(target=setup_rabbitmq_consumer, daemon=True).start()

@app.route('/event', methods=['POST'])
def receive_event():
    try:
        event_data = request.json
        events.append(event_data)
    
        redis_client.set('events', json.dumps(events))
        return jsonify({"message": "Evento recebido"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/events', methods=['GET'])
def get_events():
    try:
        cached_events = redis_client.get('events')
        if cached_events:
            return jsonify(json.loads(cached_events))
    
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
