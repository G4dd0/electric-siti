from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import date

app = Flask(__name__)
DATA_FILE = 'data/progetti.json'

# Funzione che apre il file json dei progetti ed estrae il contenuto
def carica_progetti():
    if not os.path.exists(DATA_FILE):
        return [] # se il file non esiste returno una lista vuota
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file) # return del contenuto del file json

# Funzione che salva il parametro passato sostituendo ("w") il contenuto del file json
def salva_progetti(progetti):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(progetti, file, indent=4, ensure_ascii=False)

# Uso il routing a "/" per caricare la homepage
@app.route('/')
def home():
    return render_template('index.html')

# Routing a "/dashboard": carica la variabile progetti con il file json, verifica se il tag di modifica della pagina è True per caricare il form di modifica
@app.route('/dashboard')
def dashboard():
    progetti = carica_progetti()
    modifica_id = request.args.get('modifica_id', type=int) # verifica se negli argomenti del GET è presente il tag di modifica
    progetto_modifica = None
    if modifica_id:
        progetto_modifica = next((p for p in progetti if p['id'] == modifica_id), None) # vado a prendere il progetto da modificare in base all'id
    return render_template('dashboard.html', progetti=progetti, progetto_modifica=progetto_modifica) # restituisco la pagina con i valori del file json ed eventualmente il progetto da modificare

# Routing della pagina di aggiunta (estesa da dashboard)
@app.route('/dashboard/aggiungi', methods=['POST'])
def aggiungi_progetto():
    progetti = carica_progetti()
    nuovo_id = 0
    for p in progetti: # vado a cercare l'id più grande presente e ne creo uno più grande
        if p['id'] > nuovo_id:
            nuovo_id = p['id']
    nuovo_id += 1
    dati = request.form # estraggo i dati dal form di inserimento
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
    return redirect(url_for('dashboard')) # ricarico la pagina dashboard dopo l'aggiunta

# Routing alla funzione "elimina" --> viene passato il parametro ID (univoco) 
@app.route('/dashboard/elimina/<int:id>', methods=['POST'])
def elimina_progetto(id):
    progetti = carica_progetti()
    progetti2 = []
    for p in progetti:
        if p['id'] != id: # reinserisco nel file json tutti i progetti ad eccezione del progetto con "id" corrispondente a quello eliminato
            progetti2.append(p)
    salva_progetti(progetti2)
    return redirect(url_for('dashboard'))

@app.route('/dashboard/modifica/<int:id>', methods=['POST'])
def modifica_progetto(id):
    progetti = carica_progetti()
    progetto = next((p for p in progetti if p['id'] == id), None) # vado a prendermi il progetto con "id" corrispondente a quello che cerco
    if not progetto:
        return "Progetto non trovato", 404

    dati = request.form
    progetto['titolo'] = dati.get('titolo')
    progetto['descrizione'] = dati.get('descrizione')
    progetto['categoria'] = dati.get('categoria')
    progetto['stato'] = dati.get('stato')
    salva_progetti(progetti)
    return redirect(url_for('dashboard'))


# Routing alla pagina delle conversioni
@app.route('/converter')
def converter():
    return render_template('converter.html')


if __name__ == '__main__':
    app.run(debug=True)