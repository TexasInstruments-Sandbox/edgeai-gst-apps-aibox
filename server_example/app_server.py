from flask import Flask, jsonify, request

app = Flask(__name__)

logs = []

@app.get("/")
def render():
    res = ''
    for log in logs:
        res += f"<p>{log}</p>"
    return res

@app.post("/")
def update_logs():
    data = request.json
    print(data)
    if not data or 'log' not in data:
        return jsonify({'error': 'Sending a log is required'}), 400
    logs.append(data['log'])
    return jsonify({'status': 'Message added'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
