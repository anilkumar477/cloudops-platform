from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "CloudOps Platform is running!"


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/api/info")
def info():
    return jsonify({
        "application": "CloudOps Platform",
        "version": "1.0.0",
        "environment": "development"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
