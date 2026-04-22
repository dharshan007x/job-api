from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)

@app.route('/v1/answer', methods=['POST'])
def answer():
    data = request.get_json()
    query = data.get("query", "")

    names = re.findall(r'\b[A-Z][a-z]*\b', query)
    numbers = list(map(int, re.findall(r'\d+', query)))

    scores = {}
    for i in range(min(len(names), len(numbers))):
        scores[names[i]] = numbers[i]

    if scores:
        highest = max(scores, key=scores.get)
        return jsonify({"output": highest})

    return jsonify({"output": ""})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))   # IMPORTANT
    app.run(host='0.0.0.0', port=port)