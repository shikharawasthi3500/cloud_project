import os
from flask import Flask, jsonify
import redis

app = Flask(__name__)

# Connect to Redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    # Increment visitor count in Redis
    visitors = redis_client.incr("visitor_count")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cloud Visitor Counter</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #eef2ff;
                text-align: center;
                padding-top: 100px;
            }}
            .container {{
                background: white;
                padding: 40px;
                margin: auto;
                max-width: 450px;
                border-radius: 15px;
                box-shadow: 0 4px 15px #cccccc;
            }}
            h1 {{ color: #1e3a8a; }}
            .count {{
                font-size: 55px;
                color: #2563eb;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Visitor Counter!</h1>
            <p>Total visitors:</p>
            <div class="count">{visitors}</div>
            <p>Powered by Flask + Redis + Docker</p>
        </div>
    </body>
    </html>
    """

@app.route("/health")
def health():
    try:
        redis_client.ping()
        return jsonify(status="healthy", redis="connected"), 200
    except redis.RedisError:
        return jsonify(status="unhealthy", redis="disconnected"), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)