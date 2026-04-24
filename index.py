from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Salviamo i log in memoria (Nota: su Vercel questa memoria si azzera periodicamente)
logs_in_memory = []

@app.route('/api/stats', methods=['POST', 'OPTIONS'])
def receive_stats():
    # Gestione preflight requests per CORS
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nessun dato fornito"}), 400
        
        # Aggiungiamo il timestamp e salviamo nella lista dell'API
        log_entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": data
        }
        logs_in_memory.append(log_entry)
        
        print(f"[{log_entry['timestamp']}] Statistiche ricevute da {data.get('nome_pc', 'Sconosciuto')}")
        
        resp = jsonify({
            "status": "success",
            "message": "Statistiche salvate nell'API",
            "data_received": data
        })
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp, 200
        
    except Exception as e:
        print("Errore nel salvataggio statistiche:", e)
        resp = jsonify({"error": "Errore interno del server", "details": str(e)})
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp, 500

@app.route('/api/logs', methods=['GET', 'OPTIONS'])
def get_logs():
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return response, 200

    resp = jsonify({
        "totale_scansioni": len(logs_in_memory),
        "logs": logs_in_memory
    })
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp, 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ScannerSemplice API è attiva su Vercel!"}), 200

# Vercel richiede che l'oggetto app sia disponibile.
# Quando avviato localmente eseguiamo app.run()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
