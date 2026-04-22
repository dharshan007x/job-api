from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)

@app.route('/v1/answer', methods=['POST'])
def answer():
    data = request.get_json()
    query = data.get("query", "")

    # extract names (capitalized words)
    names = re.findall(r'\b[A-Z][a-z]*\b', query)

    # extract numbers
    numbers = list(map(int, re.findall(r'\d+', query)))

    # pair in order
    pairs = list(zip(names, numbers))

    if pairs:
        best = max(pairs, key=lambda x: x[1])[0]
        return jsonify({"output": best})

    return jsonify({"output": ""})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)