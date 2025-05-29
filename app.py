from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import date

app = Flask(__name__)
DATA_FILE = 'data/progetti.json'

def carica_progetti():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def salva_progetti(progetti):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(progetti, file, indent=4, ensure_ascii=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    progetti = carica_progetti()
    modifica_id = request.args.get('modifica_id', type=int)
    progetto_modifica = None
    if modifica_id:
        progetto_modifica = next((p for p in progetti if p['id'] == modifica_id), None)
    return render_template('dashboard.html', progetti=progetti, progetto_modifica=progetto_modifica)


@app.route('/dashboard/aggiungi', methods=['POST'])
def aggiungi_progetto():
    progetti = carica_progetti()
    nuovo_id = max([p['id'] for p in progetti], default=0) + 1
    dati = request.form
    nuovo_progetto = {
        "id": nuovo_id,
        "titolo": dati.get('titolo'),
        "descrizione": dati.get('descrizione'),
        "categoria": dati.get('categoria'),
        "data_creazione": str(date.today()),
        "stato": dati.get('stato')
    }
    progetti.append(nuovo_progetto)
    salva_progetti(progetti)
    return redirect(url_for('dashboard'))

@app.route('/dashboard/elimina/<int:id>', methods=['POST'])
def elimina_progetto(id):
    progetti = carica_progetti()
    progetti = [p for p in progetti if p['id'] != id]
    salva_progetti(progetti)
    return redirect(url_for('dashboard'))

@app.route('/dashboard/modifica/<int:id>', methods=['POST'])
def modifica_progetto(id):
    progetti = carica_progetti()
    progetto = next((p for p in progetti if p['id'] == id), None)
    if not progetto:
        return "Progetto non trovato", 404

    dati = request.form
    progetto['titolo'] = dati.get('titolo')
    progetto['descrizione'] = dati.get('descrizione')
    progetto['categoria'] = dati.get('categoria')
    progetto['stato'] = dati.get('stato')
    salva_progetti(progetti)
    return redirect(url_for('dashboard'))



@app.route('/converter')
def converter():
    return render_template('converter.html')


if __name__ == '__main__':
    app.run(debug=True)