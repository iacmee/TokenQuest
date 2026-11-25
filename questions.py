INITIAL_QUESTIONS = (
    ("Quale funzione del telefono è un esempio di NLP?",
     ["Regolare la luminosità in base alla luce della stanza",
      "Suggerire la parola successiva mentre scrivi un messaggio",
      "Contare i passi mentre cammini",
      "Ruotare lo schermo quando inclini il telefono"], 1),

    ("Quando il telefono ti consiglia una parola alla fine di una frase che stai scrivendo come ha scelto quella parola",
     ["Ha informazioni in base alla posizione del telefono",
      "Ha stimato quale parola potrebbe venire dopo, in base a quello che hai scritto.",
      "Ha una regola predefinita che dopo la parola precedente va sempre la parola consigliata",
      "Ha cercato nella cronologia del browser"], 1),
      
    ("In una chat ci sono 100 messaggi: 90 normali e 10 di spam. Il filtro li segna tutti come normali. \
     Il tuo compagno dice «Ha indovinato 90 volte su 100, direi che funziona!». Quanti messaggi di spam ha trovato davvero?",
     ["Nessuno.",
      "10.",
      "90.",
      "Abbiamo bisogno di un dataset più grande per capirlo"], 0),

    ("Scrivi in chat «Raga, chi viene?». Il tokenizer separa le parole e conta ogni segno di punteggiatura \
     come un token a sé. Quanti token ottiene?",
     ["3",
      "4",
      "5",
      "6"], 2),

    ("Un tokenizer divide «stracontento» in stra e contento. Un tuo amico dice che è un errore, perché «stracontento» \
     si scrive tutto attaccato. Ha ragione?",
     ["Sì, perché un token deve sempre coincidere con una parola.",
      "No, perché un tokenizer può dividere una parola in più parti.",
      "No, perché in italiano «stra» si scrive sempre staccato.",
      "Sì, perché si possono separare solo i segni di punteggiatura."], 1),

    ("Stai provando la tokenizzazione in Python. Che cosa ottieni se esegui \"Ciao, come va?\".split()?",
     ["[\"Ciao\", \",\", \"come\", \"va\", \"?\"]",
      "[\"Ciao\", \"come\", \"va\"]",
      "[\"Ciao,\", \"come\", \"va?\"]",
      "[\"Ciao, come va?\"]"], 2),

    ("Sul quaderno qualcuno ha scritto «NLP = Natural Language Processing». Quale definizione ci metteresti sotto?",
     ["Lo studio di come i programmi riconoscono oggetti nelle foto.",
      "L’insieme delle tecniche con cui i computer elaborano il linguaggio umano.",
      "Un modo per scrivere codice Python usando parole italiane.",
      "Una tecnica che trasforma le registrazioni audio in file più piccoli."], 1),

    ("«Svegliami alle sette e mezza». Prima di impostare la sveglia, che cosa deve ricavare l’NLU da questa frase?",
     ["La frase esatta da dire per confermare la sveglia.",
      "Il suono da riprodurre alle sette e mezza.",
      "L’azione richiesta e l’orario, cioè impostare una sveglia alle 7:30.",
      "Il numero di parole che ha pronunciato l’utente."], 2),

    ("Il gestionale della scuola ha questi dati: aula 12, incontro alle 15:00, ingresso libero. Quale operazione è un esempio di NLG?",
     ["Estrarre «15:00» da un avviso già scritto.",
      "Ordinare gli incontri per numero di aula.",
      "Capire se «A che ora inizia?» è una richiesta sull’orario.",
      "Scrivere un avviso per gli studenti a partire da quei tre dati."], 3),

    ("Un programma indicizza «leggo», «legge» e «leggiamo» sotto «leggere». "
     "Come si chiama questa operazione?",
     ["Stemming.",
      "Lemmatizzazione.",
      "Riconoscimento di entità.",
      "Analisi del sentiment."], 1),

    ("Il tuo programma conserva solo quante volte compare ogni parola. "
     "Per lui «Marta batte Luca» e «Luca batte Marta» sono la stessa cosa?",
     ["No, perché vince una persona diversa.",
      "No, perché i due nomi occupano posizioni diverse.",
      "Sì, perché le parole e i loro conteggi coincidono.",
      "Sì, ma solo se il programma toglie i nomi."], 2),

    ("Un bot legge correttamente che la biblioteca apre alle 9. La risposta dice «La biblioteca chiude alle 9». "
     "Se il dato passato al bot era corretto, dove cercheresti il problema?",
     ["Nella ricerca della biblioteca.",
      "Nel passaggio che ha formulato la risposta, cioè nella NLG.",
      "Nel modo in cui l’orario è stato ordinato nel database.",
      "Nel riconoscimento della domanda, cioè nella NLU."], 1),

    ("L’assistente capisce che vuoi spostare un appuntamento e poi ti scrive una conferma. "
     "Come si chiamano i due passaggi, nello stesso ordine?",
     ["NLG → NLU.",
      "NLU → NLU.",
      "NLG → NLG.",
      "NLU → NLG."], 3),

    ("Stai raccogliendo gli eventi del weekend. Da «Sabato i Coma_Cose suonano a Bologna» "
     "vuoi ricavare artista e città. Come dovrebbe etichettarli un sistema di riconoscimento delle entità?",
     ["Coma_Cose → gruppo musicale, Bologna → luogo.",
      "Coma_Cose → luogo, Bologna → gruppo musicale.",
      "Coma_Cose → titolo dell’evento, Bologna → data.",
      "Coma_Cose → luogo, Bologna → luogo."], 0),

    ("Hai due compiti: riconoscere se una recensione parla del cibo o del servizio e capire se chi scrive "
     "è soddisfatto. Quale dei due è un esempio di sentiment analysis?",
     ["Capire se chi scrive è soddisfatto.",
      "Capire se la recensione parla del cibo o del servizio.",
      "Entrambi, perché si analizza lo stesso testo.",
      "Nessuno dei due, perché la sentiment analysis si usa solo sui messaggi vocali."], 0),

    ("«Fantastico, è la terza volta che il gioco si blocca proprio alla fine». Che cosa può mandare "
     "fuori strada un programma che conta solo le parole positive e negative?",
     ["La parola «terza» indica che il giocatore ha cambiato idea tre volte.",
      "La frase non esprime un giudizio perché parla di un problema tecnico.",
      "«Fantastico» sembra un complimento, ma qui è usato con ironia.",
      "La recensione diventa positiva perché il giocatore è arrivato alla fine."], 2),

    ("«La pizza era buonissima, ma abbiamo aspettato un’ora». Se il programma deve dare un giudizio "
     "separato su pizza e attesa, che cosa dovrebbe restituire?",
     ["Pizza negativa, attesa positiva.",
      "Pizza positiva, attesa negativa.",
      "Pizza positiva, attesa positiva.",
      "Pizza neutra, attesa neutra."], 1),

    ("Hai messo «non» nella lista delle stop word da scartare. Che guaio può combinare "
     "questa scelta quando analizzi la recensione «Non lo consiglio»?",
     ["La recensione diventa più lunga per il programma.",
      "Il programma scambia «consiglio» per il nome di un prodotto.",
      "Il programma perde la negazione e potrebbe leggere la frase come un consiglio.",
      "La recensione viene scartata per intero."], 2),

    ("In un articolo per il giornalino, «scuola» e «robotica» compaiono tre volte ciascuna. "
     "«Scuola» compare anche in tutti gli altri articoli, «robotica» solo in questo. "
     "A quale parola il TF-IDF assegna più peso in quell’articolo?",
     ["A «robotica», perché distingue questo articolo dagli altri.",
      "A «scuola», perché si trova in più articoli.",
      "A entrambe lo stesso peso, perché qui compaiono tre volte.",
      "A «scuola», perché ha meno lettere."], 0),

    ("Hai diviso «Oggi piove a Roma» in parole. Ora vuoi prendere tutte le coppie di parole "
     "vicine, nell’ordine in cui compaiono. Qual è la lista dei bigrammi?",
     ["«Oggi piove», «a Roma».",
      "«Oggi piove», «piove a», «a Roma».",
      "«Oggi a», «piove Roma».",
      "«Oggi», «piove», «a», «Roma»."], 1),
)
