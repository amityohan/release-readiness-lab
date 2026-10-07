import os
import logging
from flask import Flask, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("checkout-api")

VERSION = "v2.4"

@app.route("/", methods=["GET"])
def index():
    logger.info("Handling request at / endpoint")
    return jsonify({
        "service": "checkout-api",
        "version": VERSION,
        "message": "Release Readiness Demo"
    })

@app.route("/health", methods=["GET"])
def health():
    db_url = os.getenv("DATABASE_URL")
    redis_url = os.getenv("REDIS_URL")
    
    # Report configuration presence without claiming a live dependency connection.
    if db_url:
        db_status = "configured"
        logger.info("Database configuration is present")
    else:
        db_status = "missing_config"
        logger.warning("DATABASE_URL is not set")

    if redis_url:
        redis_status = "configured"
        logger.info("Redis configuration is present")
    else:
        redis_status = "missing_config"
        logger.warning("REDIS_URL is not set")

    status_code = 200
    
    return jsonify({
        "status": "healthy",
        "version": VERSION,
        "checks": {
            "database": db_status,
            "redis": redis_status
        }
    }), status_code

@app.route("/ready", methods=["GET"])
def readiness():
    checks = {
        "database": "configured" if os.getenv("DATABASE_URL") else "missing_config",
        "redis": "configured" if os.getenv("REDIS_URL") else "missing_config",
    }
    ready = all(value == "configured" for value in checks.values())
    return jsonify({
        "status": "ready" if ready else "not_ready",
        "version": VERSION,
        "checks": checks,
    }), 200 if ready else 503

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"Starting checkout-api v{VERSION} on port {port}")
    app.run(host="0.0.0.0", port=port)
