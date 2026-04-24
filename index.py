from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Salviamo i log in memoria (Nota: su Vercel questa memoria si azzera periodicamente)
logs_in_memory = []

@app.route('/api/stats', methods=['POST', 'OPTIONS'])
def receive_stats():
    # Gestione preflight requests per CORS (opzionale ma utile)
    if request.method == 'OPTIONS':
        return jsonify({}), 200

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
        
        return jsonify({
            "status": "success",
            "message": "Statistiche salvate nell'API",
            "data_received": data
        }), 200
        
    except Exception as e:
        print("Errore nel salvataggio statistiche:", e)
        return jsonify({"error": "Errore interno del server", "details": str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    # Ritorna tutti i log salvati in memoria
    return jsonify({
        "totale_scansioni": len(logs_in_memory),
        "logs": logs_in_memory
    }), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ScannerSemplice API è attiva su Vercel!"}), 200

# Vercel richiede che l'oggetto app sia disponibile.
# Quando avviato localmente eseguiamo app.run()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
