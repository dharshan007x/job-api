from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/answer', methods=['POST'])
def answer():
    data = request.get_json()
    query = data.get("query", "")

    numbers = re.findall(r'\d+', query)

    if len(numbers) == 2:
        a, b = int(numbers[0]), int(numbers[1])

        if "+" in query:
            result = a + b
        elif "-" in query:
            result = a - b
        elif "*" in query:
            result = a * b
        elif "/" in query:
            result = a / b
        else:
            return jsonify({"output": "Invalid operation"})

        return jsonify({"output": f"The result is {result}."})

    return jsonify({"output": "Invalid input"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)