# TokenQuest

Sito Flask con un quiz sul linguaggio naturale, una classifica per nickname e previsioni da Open-Meteo. Il quiz richiede un account. Ogni round propone 5 domande casuali e assegna 1 punto con almeno 4 risposte corrette.

## Avvio in locale

Con Python 3.12, esegui questi comandi dalla cartella del progetto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Apri `http://localhost:5000`. Al primo avvio l’app crea il database SQLite, la chiave di sessione e carica le domande iniziali.

