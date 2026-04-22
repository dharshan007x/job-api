from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)

@app.route('/v1/answer', methods=['POST'])
def answer():
    try:
        data = request.get_json()
        query = data.get("query", "")

        # Step 1: Extract all names (capitalized words)
        names = re.findall(r'\b[A-Z][a-z]+\b', query)

        # Step 2: Extract all numbers (including negatives if any)
        numbers = list(map(int, re.findall(r'-?\d+', query)))

        # Step 3: Smart mapping
        scores = {}
        idx = 0

        for word in query.split():
            clean_word = re.sub(r'[^A-Za-z]', '', word)

            if clean_word in names and idx < len(numbers):
                scores[clean_word] = numbers[idx]
                idx += 1

        # Step 4: Fallback mapping if above fails
        if not scores and len(names) == len(numbers):
            for i in range(len(names)):
                scores[names[i]] = numbers[i]

        # Step 5: Return highest scorer
        if scores:
            max_score = max(scores.values())
            for name, score in scores.items():
                if score == max_score:
                    return jsonify({"output": name})

        return jsonify({"output": ""})

    except Exception:
        return jsonify({"output": ""})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)