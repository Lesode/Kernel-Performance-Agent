from flask import Flask, request, jsonify
from kpa.agent import KernelAgent

app = Flask(__name__)
agent = KernelAgent()

@app.route("/analyze", methods=["POST"])
def analyze():
    trace = request.json["trace"]
    result = agent.run(trace)
    return jsonify(result)

app.run(port=5000)
