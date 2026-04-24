from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/api/stats', methods=['POST', 'OPTIONS'])
def receive_stats():
    # Gestione preflight requests per CORS (opzionale ma utile)
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nessun dato fornito"}), 400
        
        # Qui potresti salvare i dati in un database cloud (es. MongoDB, Supabase)
        # Per ora stampiamo semplicemente il log nel server
        print(f"[{datetime.datetime.now()}] Statistiche ricevute da {data.get('nome_pc', 'Sconosciuto')}:", data)
        
        return jsonify({
            "status": "success",
            "message": "Statistiche ricevute correttamente",
            "data_received": data
        }), 200
        
    except Exception as e:
        print("Errore nel salvataggio statistiche:", e)
        return jsonify({"error": "Errore interno del server", "details": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ScannerSemplice API è attiva su Vercel!"}), 200

# Vercel richiede che l'oggetto app sia disponibile.
# Quando avviato localmente eseguiamo app.run()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
