#  
#   Progetto Basi di Dati
#   Settembre 2020
#   Gruppo: M&M
#   Componenti: Melania Gottardo, Mario Coci
#   Opzione: compagnia aerea
#


"""
Import che servono per far funzionare la web app, compresi sqlalchemy e flask_login.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlalchemy
from sqlalchemy import *
import flask_login
from flask_login import LoginManager, login_required, login_user, UserMixin, login_manager, logout_user, current_user
from datetime import date
import re

"""
I settings prima di cominciare con il corpo del codice della web app.
"""
app = Flask(__name__)
app.config['SECRET_KEY']='k4jbW8h23Nd92p1K'
login_manager=LoginManager()
login_manager.init_app(app)

"""
Collegamento al dbms sottostante (in questo caso MySQL) come utente anonimo.
Creazione engine (globale) e attivazione di tutti i ruoli.
"""
uri = 'mysql://anonimo:anonimo@localhost/compagniaaereamm' #collegamento al dbms
engine = create_engine(uri)
conn=engine.connect()
conn.execute("set global activate_all_roles_on_login = on") #attivazione ruoli
conn.close()

"""
Creazione classe utente dove andranno salvati i dati dell'utente che accede tramite login.
Questi dati torneranno poi utili per identificare l'utente e far si che acceda solo alle pagine
e ai dati che spettano al suo ruolo o alla sua persona.
"""
class User (UserMixin) : #costruttore di classe
    def __init__ (self, id, nome, email, pwd, ruolo):
        self.id = id #ID o codice fiscale
        self.email = email #e-mail
        self.pwd = pwd #password
        self.nome = nome #nome
        self.ruolo = ruolo #Cliente o Operatore

    def get_ruolo(self): #da richiamare per ottenere il ruolo dell'utente loggato
        return self.ruolo

    def get_id(self): #da richiamare per ottenere l'id dell'utente loggato
        return self.id

"""
Funzione che serve per il corretto funzionamento dell'autenticazione.
"""
@login_manager.user_loader
def load_user (user_id):
    conn = engine.connect()
    s=text("SELECT * FROM users WHERE ID =:utente")
    rs = conn.execute(s, utente=user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.ID, user.Nome, user.Email, user.Password, user.Ruolo)



##### SEZIONE BASE #####



"""
Route iniziale, home della web app.
Qui sara' possibile accedere a diverse pagine, senza bisogno di autenticazione.
L'autenticazione sara' richiesta per cose piu' specifiche piu' avanti.
Qui e' presente il primo esempio di render_template: si fa riferimento ad una
pagina html (home.html) per snellire e semplificare il codice di flask.
Questa pagina fa l'extends di un'altra pagina html (base.html) dove si trova il
codice html comune a tutte le pagine. In particolare, la barra di navigazione si
trova in base.html. In questa barra e' presente anche l'input per poter accedere
alla pagina di login (e registrazione) o logout (nel caso ci sia gia' autenticati);
per questa ragione, ogni volta che si va a fare il render_template e' necessario
sapere le l'utente corrente e' autenticato. Maggiori dettagli su questo argomento
nei commenti della pagina base.html.
"""
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template ('home.html', logged=current_user.is_authenticated) #render della pagina html "home"

"""
Quando un utente va a cliccare sull'input login, viene semplicemente renderizzata
la pagina dove effettuera' il login vero e proprio o dove potra' accedere alla pagina
per la registrazione, se non l'ha ancora fatta. 
Queste funzioni presentano tutte i metodi GET e POST, in quanto i form delle
pagine html necessitano di utilizzare il metodo POST per poter accedervi.
"""
@app.route('/loginPagina', methods=['GET', 'POST'])
def loginPagina():
    return render_template("login.html", logged=current_user.is_authenticated) #render della pagina html "login"

"""
Quando l'utente compila i campi per poter accedere e preme sull'input "Login",
viene chiamata questa funzione. Per prima cosa si va a fare riferimento all'engine
globale. Si va poi a selezionare l'utente con l'ID inserito. Se questo ID fa parte
della tabella users, allora di va a verificare che la password sia corretta. In tal
caso, si vanno a salvare i dati dell'utente e si procede con la sua autenticazione
tramite flask-login. Una volta autenticato, l'utente si trovera' nella sua area
riservata (prima non accessibile). Se la password e' errata, l'utente sara' invitato a
riprovare. Se l'ID non esiste, l'utente potra' inserirne un'altro o fare la registrazione. 
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    global engine #engine globale
    if request.method == 'POST': #route triggered con metodo POST
        conn = engine.connect() #connessione aperta
        s=text('SELECT * FROM users u WHERE u.ID =:id') #ricerca utente con l'ID specificato
        rs = conn.execute (s, id=request.form['ID']).fetchone()
        if rs: #controllo esistenza di quell'utente
            real_pwd = rs['Password'] #salvataggio password
            conn.close() #connesione chiusa
            if(request.form['password']==real_pwd): #controllo correttezza della password
                user = User(rs['ID'],rs['Nome'],rs['Email'],rs['Password'],rs['Ruolo']) #creazione utente con costruttore
                login_user(user) #chiamata a flask-login
                engine=create_engine("mysql://"+rs['ID']+":"+rs['Password']+"@localhost/compagniaaereamm") #accesso con le credenziali
                return redirect(url_for('areaRiservata')) #rimando all'area riservata dell'utente
            else: #password errata
                flash('Errore: ID o password errati','error') #messaggio di errore
                return redirect(url_for('loginPagina')) #rimando alla pagina di login
        else: #id non esistente
            flash('Errore: ID errato o non esistente','error') #messaggio di errore
            conn.close() #connessione chiusa
            return redirect(url_for('loginPagina')) #rimando alla pagina di login
    else: #route triggered con metodo GET
        return redirect(url_for('home')) #rimando alla home page

"""
Quando un utente autenticato vuole fare logout, premera' l'input "Logout" e verra'
rimandato alla home page, per la quale non serve autenticazione. Si fa riferimento
all'engine globale e si richiama flask-login per fare il logout.
"""
@app.route('/logout', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def logout():
    global engine #engine globale
    engine = create_engine('mysql://anonimo:anonimo@localhost/compagniaaereamm') #accesso come anonimo
    logout_user() #chiamata a flask-login
    return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente si trova nella pagina di login e preme sull'input "Registrazione",
viene caricata la pagina effettiva della registrazione.
"""
@app.route('/registrazionePagina', methods=['GET', 'POST'])
def registrazionePagina():
    return render_template("registrazione.html", logged=current_user.is_authenticated) #render della pagina html "registrazione"

"""
Quando l'utente compila i campi per potersi registrare e preme sull'input "Fatto",
viene chiamata questa funzione. Viene verificato che l'ID inserito non sia mai stato
inserito prima e, in caso negativo invita l'utente ad inserire un altro ID. In caso
positivo, l'utente viene inserito nella tabella users e viene creato un user che potra'
avere accesso al localhost con la propria password; poi, gli viene garantito il ruolo
di "Cliente". Dalla pagina di registrazione possono registrarsi solo utenti con il ruolo
di "Cliente", gli utenti con il ruolo di "Operatore" dovranno essere registrati da un
altro utente con il ruolo di "Operatore".
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"SERIALIZABLE". Infatti, se due utenti tentano di registrarsi con lo stesso codice ID
nello stesso momento, non possono piu' essere distinti correttamente; quindi serve che
avvenga un lock sulla tabella, per permettere ad uno alla volta di accedervi e fare
l'inserimento.
"""
@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE") #livello di isolamento SERIALIZABLE
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("SELECT u.ID FROM users u WHERE u.ID =:codice") #ricerca utente con l'ID specificato
        id = conn.execute (s, codice=request.form['codice']).fetchone()

        if id: #controllo esistenza di quell'utente
            conn.execute("COMMIT") #commit delle operazioni
            conn.close() #connessione chiusa
            flash('Errore: inserire un ID diverso','error') #messaggio di errore
            return redirect(url_for('registrazionePagina')) #rimano alla pagina di registrazione

        s=text("INSERT INTO users VALUES(:codice,:nome,:email,:password,'Cliente')") #inserimento dell'utente nella tabella users
        rs = conn.execute (s, codice=request.form['codice'],nome=request.form['utente'],email=request.form['inputEmail'],password=request.form['password'])

        s=text("create user :codice@'localhost' identified with mysql_native_password by :password") #creazione dell'user per l'accesso al localhost
        rs = conn.execute (s, codice=request.form['codice'],password=request.form['password'])

        s=text("GRANT Cliente to :codice@'localhost'") #garantire il ruolo di "Cliente" all'utente
        rs = conn.execute (s, codice=request.form['codice'])

        rs = conn.execute ("FLUSH PRIVILEGES") #ricarica la tabella dei permessi
        conn.execute("COMMIT") #commit delle operazioni
        conn.close() #connessione chiusa
        return redirect(url_for('loginPagina')) #rimando alla pagina di login per fare l'accesso
    except: #qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: registrazione non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('registrazionePagina')) #rimando alla pagina di registrazione

"""
Nell'area riservata, ciascun utente ha la possibilita di accedere alla pagina di modifica
dei propri dati (nome e email). Quando clicca sull'input, viene caricata la pagina per
la modifica del profilo.
"""
@app.route ('/modificaProfiloPagina', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def modificaProfiloPagina ():
    return render_template("modifica_profilo.html", logged=current_user.is_authenticated, id=current_user.get_id()) #render della pagina html "modifica_profilo"

"""
Quando l'utente compila i campi per la modifica dei dati e preme sull'input "Fatto",
viene chiamata questa funzione. I nuovi dati vengono inseriti nella tabella users con
il comando UPDATE e poi l'utente viene di nuovo indirizzato verso la sua area riservata.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"READ UNCOMMITTED". Infatti, anche se l'utente modifica i suoi dati, nessuna altra
operazione puo' essere intaccata.
"""
@app.route ('/modificaProfilo', methods=['GET', 'POST'])
def modificaProfilo ():
    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED") #livello di isolamento READ UNCOMMITTED
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("UPDATE users SET Nome =:nome, Email =:email WHERE ID =:id") #aggiornamento dei dati dell'utente
        prenotazioni=conn.execute(s, nome=request.form['nome'],email=request.form['inputEmail'],id=current_user.get_id())
        conn.execute("COMMIT") #commit delle operazioni
        conn.close() #connessione chiusa
        return redirect(url_for('areaRiservata')) #rimando all'area riservata dell'utente
    except: #qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: modifica non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('modificaProfiloPagina')) #rimando alla pagina di modifica del profilo

"""
Quando un utente fa il login, viene rimandato alla sua area riservata. Puo' accerevi in
qualunque momento (mentre e' autenticato) dato che l'input per accervi si trova nella
barra di navigazione sempre presente. Dato che ci sono diversi tipi di utenti (Cliente
o Operatore), il contenuto della pagina e' diverso per ognuno di loro. Questa funzione
serve per indirizzare correttamente ogni utente alla pagina html corretta.
Se l'utente e' un "Cliente" allora potra' vedere le sue prenotazioni, se e' un "Operatore"
potra' vedere e portare modifiche ai dati.
"""
@app.route ('/areaRiservata', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def areaRiservata ():
    if (current_user.get_ruolo()=="Cliente"): #Cliente
        return redirect(url_for('prenotazioni')) #rimando alla pagina delle prenotazioni
    elif (current_user.get_ruolo()=="Operatore"): #Operatore
        return redirect(url_for('operatore')) #rimando alla pagina principale dell'operatore
    else: #altro
        return redirect(url_for('home')) #rimando alla home



### SEZIONE SENZA AUTENTICAZIONE ###



"""
Dalla home o dal menu rapido nella barra di navigazione si puo' accedere a questa sezione.
Non e' necessaria l'autenticazione per questa sezione, e' solo una pagina di visualizzazione
di informazioni generali.
L'utente puo' vedere l'elenco completo di tutti i voli presenti nella taballa voli in
partenza da quel momento in poi ordinati per partenza, dalla piu' imminente alla piu' distante.
"""
@app.route ('/voli', methods=['GET', 'POST'])
def voli():
    conn=engine.connect() #connessione aperta
    s=text("SELECT v.CodVoli, v.PrezzoEconomy, l1.Citta AS Parte, l2.Citta AS Arriva FROM voli v JOIN localita l1 ON v.Da = l1.CodLocalita JOIN localita l2 ON v.Verso = l2.CodLocalita WHERE v.Partenza >= NOW() ORDER BY v.Partenza")
    #ricerca di tutti i voli con prezzo dell'economy class e citta' di partenza e di arrivo
    voli=conn.execute(s)
    conn.close() #connessione chiusa
    return render_template("viaggi.html", logged=current_user.is_authenticated, voli=voli) #render della pagina html "voli"

"""
Dalla home o dal menu rapido nella barra di navigazione si puo' accedere a questa sezione.
Non e' necessaria l'autenticazione per questa sezione, e' solo una pagina di visualizzazione
di informazioni generali.
L'utente puo' vedere l'elenco dei 10 voli piu' economici presenti nella taballa voli in
partenza da quel momento in poi ordinati per prezzo, dal piu' economico al piu' costoso.
"""
@app.route ('/lowCost',methods=['GET', 'POST'])
def lowCost():
    conn=engine.connect() #connessione aperta
    s=text("SELECT v.CodVoli, v.PrezzoEconomy, l1.Citta AS Parte, l2.Citta AS Arriva FROM voli v JOIN localita l1 ON v.Da = l1.CodLocalita JOIN localita l2 ON v.Verso = l2.CodLocalita WHERE v.Partenza >= NOW() ORDER BY v.PrezzoEconomy, v.CodVoli LIMIT 10")
    #ricerca dei 10 voli piu' economici con prezzo dell'economy class e citta' di partenza e di arrivo
    voli=conn.execute(s)
    conn.close() #connessione chiusa
    return render_template("low_cost.html", logged=current_user.is_authenticated, voli=voli) #render della pagina html "lowCost"

"""
Dalla home o dal menu rapido nella barra di navigazione si puo' accedere a questa sezione.
Non e' necessaria l'autenticazione per questa sezione, e' solo una pagina di visualizzazione
di informazioni generali.
L'utente puo' vedere l'elenco dei voli presenti nella taballa voli che hanno uno sconto in
partenza da quel momento in poi ordinati per sconto, dal piu' basso al piu' alto.
"""
@app.route ('/offerte',methods=['GET', 'POST'])
def offerte():
    conn=engine.connect() #connessione aperta
    s=text("SELECT v.CodVoli, v.Sconto, l1.Citta AS Parte, l2.Citta AS Arriva FROM voli v JOIN localita l1 ON v.Da = l1.CodLocalita JOIN localita l2 ON v.Verso = l2.CodLocalita WHERE v.Sconto > 0 ORDER BY v.Sconto, v.CodVoli")
    #ricerca dei voli che presentano uno sconto con prezzo dell'economy class e citta' di partenza e di arrivo
    voli=conn.execute(s)
    conn.close() #connessione chiusa
    return render_template("offerte.html", logged=current_user.is_authenticated, voli=voli) #render della pagina html "offerte"

"""
Dalla home o dal menu rapido nella barra di navigazione si puo' accedere a questa sezione.
Non e' necessaria l'autenticazione per questa sezione, e' solo una pagina di visualizzazione
di informazioni generali.
L'utente puo' vedere i dettagli riguardanti un volo selezionato tramite clicl sull'input
"Dettagli" su una delle pagine precedenti (voli, lowCost, offerte). Questo e' l'unico luogo
dove puo' vedere informazioni specifiche sul volo e i clienti possono accervi anche tramite
la loro area riservata per i voli per i quali hanno gia' fatto una prenotazione.
Si visualizzano informazioni su data, orario, luogo e areoporto di partenza e di arrivo,
numero di scali e durata dal viaggio.
"""
@app.route ('/dettagli', methods=['GET', 'POST'])
def dettagli():
    conn=engine.connect() #connessione aperta
    s=text("SELECT l1.Citta AS CittaParte, l1.Nazione AS NazioneParte, l1.NomeAeroporto AS AeroportoParte, l2.*, v.* FROM voli v JOIN localita l1 ON v.Da = l1.CodLocalita JOIN localita l2 ON v.Verso = l2.CodLocalita WHERE v.CodVoli =:volo")
    #ricerca dei dettagli riguardanti un volo scelto con citta' di partenza e di arrivo
    info = conn.execute (s, volo=int(request.form['volo'])).fetchone()
    conn.close() #connessione chiusa
    return render_template("dettagli.html", logged=current_user.is_authenticated, info=info) #render della pagina html "dettagli"

"""
Dalla home o dal menu rapido nella barra di navigazione si puo' accedere a questa sezione.
Non e' necessaria l'autenticazione per questa sezione, e' solo una pagina di visualizzazione
di informazioni generali.
L'utente puo' vedere l'elenco completo di tutte le mete presenti nella taballa localita
ordinate per nazione e citta'.
"""
@app.route ('/mete',methods=['GET', 'POST'])
def mete():
    conn=engine.connect() #connessione aperta
    s=text("SELECT * FROM localita l ORDER BY l.Nazione, l.Citta") #ricerca di tutte le mete
    localita=conn.execute(s)
    conn.close() #connessione chiusa
    return render_template("mete.html", logged=current_user.is_authenticated, localita=localita) #render della pagina html "mete"

"""
Dalla home o dal menu rapido nella barra di navigazione si puo' accedere a questa sezione.
Non e' necessaria l'autenticazione per questa sezione, e' solo una pagina di visualizzazione
di informazioni generali.
L'utente puo' vedere l'elenco delle 5 mete piu' scelte come arrivo dei voli presenti nella taballa
localita ordinate per popolarita'.
"""
@app.route ('/meteGettonate',methods=['GET', 'POST'])
def meteGettonate():
    conn=engine.connect() #connessione aperta
    s=text("SELECT l.Citta, l.Nazione, COUNT(*) AS Scelta FROM posti o NATURAL JOIN prenotazioni p NATURAL JOIN voli v JOIN localita l ON v.Verso=l.CodLocalita GROUP BY v.Verso ORDER BY Scelta DESC LIMIT 5")
    #ricerca delle 5 mete piu' scelte come arrivo dei voli
    localita=conn.execute(s)
    conn.close() #connessione chiusa
    return render_template("mete_gettonate.html", logged=current_user.is_authenticated, localita=localita)  #render della pagina html "mete_gettonate"

"""
Dalla home o dal menu rapido nella barra di navigazione si puo' accedere a questa sezione.
Non e' necessaria l'autenticazione per questa sezione, e' solo una pagina di visualizzazione
di informazioni generali.
L'utente puo' vedere l'elenco dei privilegi delle diverse classi presenti nella taballa classi.
Questo e' l'unico dove puo' vedere informazioni specifiche su cosa caratterizza ciascuna classe.
"""
@app.route ('/classi',methods=['GET', 'POST'])
def classi():
    conn=engine.connect() #connessione aperta
    s=text("SELECT * FROM classi WHERE CodClassi = 'First'") #ricerca delle informazioni della first class
    first=conn.execute(s).fetchone()
    s=text("SELECT * FROM classi WHERE CodClassi = 'Business'") #ricerca delle informazioni della business class
    business=conn.execute(s).fetchone()
    s=text("SELECT * FROM classi WHERE CodClassi = 'Economy'") #ricerca delle informazioni dell'economy class
    economy=conn.execute(s).fetchone()
    conn.close() #connesione chiusa
    return render_template("classi.html", logged=current_user.is_authenticated, first=first, business=business, economy=economy)  #render della pagina html "classi"



##### SEZIONE CLIENTE #####



"""
Questa e' la vera area riservata del "Cliente". Qui sono disponibili tutte le sue
prenotazioni alle quali puo' accedere e l'input per poter modificare i propri dati;
in aggiunta, puo' vedere i dettagli dei voli corrispondenti alle sue prenotazioni.
In questa pagina saranno visualizzati solo i nomi delle citta' di partenza e di
arrivo dei voli delle prenotazioni.
"""
@app.route ('/prenotazioni')
@login_required #richiede autenticazione
def prenotazioni ():
    if (current_user.get_ruolo()=="Cliente"): #Cliente
        conn=engine.connect() #connessione aperta
        s=text("SELECT p.*, l1.Citta AS Parte, l2.Citta AS Arriva FROM prenotazioni p NATURAL JOIN voli v JOIN localita l1 ON l1.CodLocalita = v.Da JOIN localita l2 ON l2.CodLocalita = v.Verso WHERE p.CF =:id AND v.Partenza >= NOW()")
        #ricerca di tutte le prenotazioni dell'utente dal momento corrente in avanti (le prenotazioni passate non sono visualizzabili)
        prenotazioni=conn.execute(s, id=current_user.get_id())
        conn.close() #connessione chiusa
        return render_template("prenotazioni.html", logged=current_user.is_authenticated, prenotazioni=prenotazioni) #render della pagina html "prenotazioni"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando un utente vuole vedere i dati corrispondenti ad una propria prenotazione,
clicca sull'input "La tua prenotazione" e viene chiamata questa funzione. Qua
vengono semplicemente visualizzati i dati relativi alla prenotazione. In questa
pagina si possono aanche compiere altre due azioni: cancellare la prenotazione o
aggiungere deli bagagli in stiva.
"""
@app.route ('/dati', methods=['GET', 'POST'])
@login_required #richiesta autenticazione
def dati():
    if (current_user.get_ruolo()=="Cliente"): #Cliente
        prenotazioni = int(request.form['prenotazioni']) #codice prenotazione dall'html
        conn=engine.connect() #connessione aperta
        s=text("SELECT p.CodPosti FROM posti p NATURAL JOIN prenotazioni o WHERE o.CodPrenotazioni =:book")
        #ricerca posti associati alla prenotazione
        biglietti=conn.execute(s, book=prenotazioni)
        
        t=text("SELECT p.CodPrenotazioni, COUNT(p.CodPosti) AS BagagliMano, o.Bagagli AS BagagliStiva FROM posti p NATURAL JOIN prenotazioni o WHERE o.CodPrenotazioni =:book GROUP BY o.CodPrenotazioni")
        #ricerca informazioni riguardanti la prenotazione (numero bagagli a mano e in stiva)
        bagagli=conn.execute(t, book=prenotazioni).fetchone()
        conn.close() #connessione chiusa
        return render_template("dati.html", logged=current_user.is_authenticated, biglietti=biglietti, bagagli=bagagli) #render della pagina html "dati"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente clicca sull'input "Piu' bagagli in stiva" viene chiamata
questa funzione che carica la pagina dove si puo' specificare quanti
bagagli aggiungere alla prenotazione.
"""
@app.route ('/modificaPrenotazione', methods=['GET', 'POST'])
@login_required #richiesta autenticazione
def modificaPrenotazione():
    if (current_user.get_ruolo()=="Cliente"): #Cliente
        codice = request.form['prenotazioni'] #codice prenotazioni
        stiva = request.form['stiva'] #bagagli in stiva
        return render_template("modifica_prenotazione.html", logged=current_user.is_authenticated, codice=codice, stiva=stiva) #render della pagina html "modifica_prenotazione"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente clicca sull'input "Aggiungi" nella pagina della modifica della sua
prenotazione, viene chiamta questa funzione. Qui viene aggiornata la prenotazione in
questione andando ad incrementare il numero di bagagli in stiva.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"SERIALIZABLE". Infatti, se, mentre un utente vuole aggiungere altri bagagli alla
sua prenotazione, un altro utente sta facendo una nuova prenotazione ed e' rimasto solo
un posto per i bagagli in stiva, entrambi lo sceglieranno, causando un eccesso di bagagli
in stiva; quindi serve che avvenga un lock sulla tabella, per permettere ad uno alla
volta di accedervi e fare l'inserimento o la modifica.
"""
@app.route ('/aggiungiBagagli', methods=['GET', 'POST'])
def aggiungiBagagli():
    codice = request.form['codice'] #codice prenotazione
    aggiungere = request.form['aggiungere']#bagali in stiva da aggiungere
    stiva = request.form['stiva']#bagagli in stiva gia' presenti
    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE") #livello di isolamento SERIALIZABLE
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("UPDATE prenotazioni SET Bagagli =:numero WHERE CodPrenotazioni =:codice") #aggiornamento numero di bagagli in stiva
        rs = conn.execute (s, codice=codice, numero=(int(aggiungere)+int(stiva)))
        conn.execute("COMMIT") #commit delle operazioni
        conn.close() #connessione chiusa
        return redirect(url_for('areaRiservata')) #rimando all'area riservata dell'utente
    except: #qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: modifica non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('areaRiservata')) #rimando all'area riservata dell'utente

"""
Quando l'utente clicca sull'input "Cancella prenotazione" nella pagina della modifica
della sua prenotazione, viene chiamta questa funzione. Qui viene cancellata la
prenotazione in questione.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"READ UNCOMMITTED". Infatti, anche se l'utente cancella i suoi dati, nessuna altra
operazione puo' essere intaccata.
"""
@app.route ('/cancellaPrenotazione', methods=['GET', 'POST'])
def cancellaPrenotazione():
    codice = request.form['prenotazioni'] #codice prenotazione
    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED") #livello di isolamento READ UNCOMMITTED
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("DELETE FROM prenotazioni p WHERE p.CodPrenotazioni =:codice") #cancellazione della prenotazione
        rs = conn.execute (s, codice=codice)
        conn.execute("COMMIT") #commit delle operazioni
        conn.close() #connessione chiusa
        return redirect(url_for('areaRiservata')) #rimando all'area riservata dell'utente
    except: #qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: cancellazione non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('areaRiservata')) #rimando all'area riservata dell'utente

"""
Quando l'utente clicca sull'input "Cerca posti" nella pagina dei dettagli di un volo,
viene chiamata questa funzione. In questa pagina viene visualizzata la mappa dei
posti dell'aereo per il volo selezionato. L'utente puo' selezionare per quale classe
sta cercando i posti, rendendo cosi gli altri posti non selezionabili. In piu', si
devono poter vedere chiaramente (e non selezionare) i posti gia' prenotati da altri
utenti. Per ogni classe, il prezzo del biglietto cambia. L'utente deve anche digitare
quanti bagaglil in stiva vuole. Per ottenere questo bisogna cercare tutti i prezzi dei
biglietti, il numero dei posti (o meglio, delle file) dell'aereo e i posti occupati.
Il file javascript che si occupa della grafica della pagina ha bisogno di un elenco di
posti in ordine numerico, non alfanumerico come quello che si ottiene dalla tabella posti.
Bisogna trasformare l'elenco applicando una codifica in modo da ottenere l'elenco necessario.
Questa pagina puo' essere visualizzata anche da un utente "Operatore", ma ha delle differenze.
L'operatore non puo' prenotare alcun posto, non puo' cambiare classe, non puo' vedere i
prezzi dei biglietti e non puo' digitare il numero di bagagli in stiva. Di conseguenza,
puo' solo vedere se in quell'aereo per quel volo ci sono posti prenotati e quali sono.
Serve comunque attuare la procedura per la visualizzazione dei posti occupati.
"""
@app.route ('/posti', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def posti():
    if (current_user.get_ruolo()=="Cliente"): #Cliente
        volo = request.form['volo'] #codice del volo
        classe = request.form['classe'] #classe
        da = request.form['da'] #luogo di partenza
        verso = request.form['verso'] #luogo di arrivo
        conn=engine.connect() #connessione aperta
        t=text("SELECT v.PrezzoFirst, v.PrezzoBusiness, v.PrezzoEconomy, a.NumFile FROM voli v NATURAL JOIN aerei a WHERE v.CodVoli =:volo")
        #ricerca dei prezzi dei biglietti e del numero di file dell'aereo
        prezzi = conn.execute (t, volo=int(request.form['volo'])).fetchone()
        s=text("SELECT p.CodPosti FROM posti p NATURAL JOIN prenotazioni o NATURAL JOIN voli v WHERE v.CodVoli =:volo")
        #ricerca dei posti gia' prenotati per il volo scelto
        prenotati = conn.execute (s, volo=int(request.form['volo']))
        conn.close() #connessione chiusa
        file = prezzi['NumFile'] #numero delle file
        sedili=[] #lista per i posti con codice alfanumerico
        seats = [] #lista per i posti con codice numerico
        for posto in prenotati: #ciclo for sui posti prenotati con codice alfanumerico
            sedili.append(posto['CodPosti']) #aggiunge il sedile alla lista
        for p in sedili:
            s = re.sub("[^A-Z]+","",p) #rimozione dei numeri dal nome del sedile
            n = re.sub("[^0-9]+","",p) #rimozione delle lettere dal nome del sedile
            n = int(n) #conversione da string a int
            n = n - 1 #decremento perche' l'elenco delle file deve partire da 0 e non da 1
            if n >= int(int(file)*0.1): #stacco - fila saltata tra prima e seconda classe
                n = n+1
            if n >= int(int(file)*0.4)+1: #stacco - fila saltata tra seconda e terza classe
                n = n+1
            n = n * 7 #per ogni fila ci sono 6 posti e il corridoio
            if s == 'B': #secondo posto nella fila
                n = n+1
            elif s == 'C': #terzo posto nella fila - corridoio
                n = n+2
            elif s == 'D': #quarto posto nella fila
                n = n+4
            elif s == 'E': #quinto posto nella fila
                n = n+5
            elif s == 'F': #sesto posto nella fila
                n = n+6
            seats.append(n) #posto aggiunto con codice numerico corretto
        return render_template("posti.html", logged=current_user.is_authenticated, volo=volo, righe=file, classe=classe, prenotati=seats, da=da, verso=verso, prezzi=prezzi) #render della pagina html "posti"
    elif (current_user.get_ruolo()=="Operatore"):
        volo=int(request.form['volo']) #codice del volo
        da = request.form['da'] #luogo di partenza
        verso = request.form['verso'] #luogo di arrivo
        conn=engine.connect() #connessione aperta
        t=text("SELECT a.NumFile FROM voli v NATURAL JOIN aerei a WHERE v.CodVoli =:volo") #ricerca del numero di file dell'aereo
        righe = conn.execute (t, volo=volo).fetchone()
        s=text("SELECT p.CodPosti FROM posti p NATURAL JOIN prenotazioni o NATURAL JOIN voli v WHERE v.CodVoli =:volo")
        #ricerca dei posti gia' prenotati per il volo scelto
        prenotati = conn.execute (s, volo=volo)
        conn.close() #connessione chiusa
        file=righe['NumFile'] #numero di file
        sedili=[] #lista per i posti con codice alfanumerico
        seats = [] #lista per i posti con codice numerico
        for posto in prenotati: #ciclo for sui posti prenotati con codice alfanumerico
            sedili.append(posto['CodPosti']) #aggiunge il sedile alla lista
        for p in sedili:
            s = re.sub("[^A-Z]+","",p) #rimozione dei numeri dal nome del sedile
            n = re.sub("[^0-9]+","",p) #rimozione delle lettere dal nome del sedile
            n = int(n) #conversione da string a int
            n = n - 1 #decremento perche' l'elenco delle file deve partire da 0 e non da 1
            if n >= int(int(file)*0.1): #stacco - fila saltata tra prima e seconda classe
                n = n+1
            if n >= int(int(file)*0.4)+1: #stacco - fila saltata tra seconda e terza classe
                n = n+1
            n = n * 7 #per ogni fila ci sono 6 posti e il corridoio
            if s == 'B': #secondo posto nella fila
                n = n+1
            elif s == 'C': #terzo posto nella fila - corridoio
                n = n+2
            elif s == 'D': #quarto posto nella fila
                n = n+4
            elif s == 'E': #quinto posto nella fila
                n = n+5
            elif s == 'F': #sesto posto nella fila
                n = n+6
            seats.append(n) #posto aggiunto con codice numerico corretto
        return render_template("posti_op.html", logged=current_user.is_authenticated, righe=file, prenotati=seats, da=da, verso=verso) #render della pagina html "posti"
    else: #altro
        return redirect(url_for('home')) #rimanda alla home page

"""
Quando l'utente clicca sull'input "Conferma" nella pagina di selezione dei posti,
viene chiamata questa funzione. Per prima cosa si verifica che sia stato selezionato
almeno un biglietto e, in caso negativo, si manda un messaggio di errrore all'utente.
In caso positivo, invece, vengono calcolati i biglietti, quanti bagagli a mano puo' avere
l'utente e il prezzo totale che ha pagato l'utente in totale (somma del prezzo di ogni
biglietto) applicato anche l'aeventuale sconto. Ogni classe (first, business, economy)
ha un prezzo diverso per i biglietti, quindi bisogna andare a verificare di quale
classe ci stiamo interessando e poi andare a calcolare il tutto. Lo sconto viene visto
come un numero su 100, quindi bisogna applicare una formula per trovare il prezzo giusto.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"SERIALIZABLE". Infatti, se, mentre un utente vuole aggiungere altri bagagli alla
sua prenotazione, un altro utente sta facendo una nuova prenotazione ed e' rimasto solo
un posto per i bagagli in stiva, entrambi lo sceglieranno, causando un eccesso di bagagli
in stiva; quindi serve che avvenga un lock sulla tabella, per permettere ad uno alla
volta di accedervi e fare l'inserimento o la modifica.
"""
@app.route ('/conferma', methods=['GET', 'POST'])
@login_required #richiesta autenticazione
def conferma():
    if (current_user.get_ruolo()=="Cliente"): #Cliente
        if request.form['biglietti'] != "": #verifica che sia stato selezionato almeno un posto 
            biglietti = request.form['biglietti'].split(',') #posti selezionati (viene usata la funzione split per ottenere una lista dei posti da una stringa di partenza)
            bagagli = request.form['bagagli'] #numero di bagagli in stiva
            volo = request.form['volo'] #codice del volo
            cl = request.form['classe'] #classe di riferimento
            if cl == '1':
                classe = 'First' #first class
            elif cl == '2':
                classe = 'Business' #business class
            else:
                classe = 'Economy' #economy class

            conn=engine.connect() #connessione aperta
            conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE") #livello di isolamento SERIALIZABLE
            conn.execute("START TRANSACTION") #inizio transazione
            try:
                if classe == 'First': #first class
                    v=text("SELECT v.PrezzoFirst, v.Sconto FROM voli v WHERE v.CodVoli =:volo") #ricerca prezzo e sconto
                    rs = conn.execute (v, volo=volo).fetchone()
                    sc = int(rs['Sconto']) #sconto x/100
                    prezzo = float(rs['PrezzoFirst']) * len(biglietti) #calcolo prezzo senza sconto
                elif classe == 'Business': #business class
                    v=text("SELECT v.PrezzoBusiness, v.Sconto FROM voli v WHERE v.CodVoli =:volo") #ricerca prezzo e sconto
                    rs = conn.execute (v, volo=volo).fetchone()
                    sc = int(rs['Sconto']) #sconto x/100
                    prezzo = float(rs['PrezzoBusiness']) * len(biglietti) #calcolo prezzo senza sconto
                else: #economy class
                    v=text("SELECT v.PrezzoEconomy, v.Sconto FROM voli v WHERE v.CodVoli =:volo") #ricerca prezzo e sconto
                    rs = conn.execute (v, volo=volo).fetchone()
                    sc = int(rs['Sconto']) #sconto x/100
                    prezzo = float(rs['PrezzoEconomy']) * len(biglietti) #calcolo prezzo senza sconto
                prezzo = prezzo - (prezzo * sc / 100) #calcolo prezzo con sconto applicato

                w=text("INSERT INTO prenotazioni (CodVoli,CF,DataPrenotazione,Prezzo,Bagagli) VALUES(:volo,:cf,:data,:prezzo,:bagagli)")
                #inserimento prenotazione nella tabella prenotazioni con autoincrement sul codice delle prenotazioni
                rs = conn.execute (w, volo=volo, cf=current_user.get_id(), data=date.today(), prezzo=prezzo, bagagli=bagagli)
     
                u=text("SELECT p.CodPrenotazioni FROM prenotazioni p WHERE p.CF =:id AND p.CodVoli =:volo AND p.DataPrenotazione = (SELECT MAX(q.DataPrenotazione) FROM prenotazioni q WHERE q.CF=p.CF AND q.CodVoli=p.CodVoli)")
                #ricerca del codice della prenotazione appena inserito
                rs = conn.execute (u, id=current_user.get_id(), volo=volo).fetchone()
                cp = rs['CodPrenotazioni'] #codice prenotazione

                for s in biglietti: #ciclo for sulla lista dei posti selezionati
                    t=text("INSERT INTO posti VALUES(:classe,:posto,:prenotazione)") #inserimento posto selezionato
                    rs = conn.execute (t, classe=classe, posto=s, prenotazione=cp)

                conn.execute("COMMIT") #commit delle operazioni
                conn.close() #connessione chiusa
                return render_template("conferma.html", logged=current_user.is_authenticated, biglietti=biglietti, bs=bagagli, prezzo=prezzo, sconto=sc) #render della pagina html "conferma"
            except: #qualcosa non e' andato a buon fine
                conn.execute("ROLLBACK") #rollback delle operazioni
                conn.close() #connessione chiusa
                flash('Errore: prenotazione non andata a buon fine','error') #messaggio di errore
                return redirect(url_for('voli')) #rimando alla pagina dei voli
        else: #nessun posto selezionato
            flash('Errore: nessun posto selezionato','error') #messaggio di errore
            return redirect(url_for('voli')) #rimando alla pagina dei voli
    else: #altro
        return redirect(url_for('home')) #rimando alla home page



##### SEZIONE OPERATORE #####



"""
Questa e' la vera area riservata dell' "Operatore". Qui sono disponibili tutte le sue
azioni: modificare i propri dati, vedere le statistiche, inserire, modificare ed
eliminare un volo, un aereo o una meta ed inserire un nuovo operatore.
"""
@app.route ('/operatore')
@login_required #richiede autenticazione
def operatore ():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        return render_template("operatore.html", logged=current_user.is_authenticated) #render della pagina html "operatore"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando un "Operatore" vuole vedere come sono le statistiche, richiama questa funzione
che fa una serie di ricerche per permettergli di vedere i dati che gli servono per fini
commerciali. Ci sono informazioni su prezzi, quantita' di utenti, aerei, scelte degli utenti
per quanto riguarda le classi e c'e' un elenco di tutti i voli con tutti i prezzi, duarata
del volo, arrivo, partenza, scali e sconti.
"""
@app.route ('/statistiche', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def statistiche():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        conn=engine.connect() #connessione aperta

        s=text("SELECT SUM(p.Prezzo) AS Totale FROM prenotazioni p") #incassi totali
        totale = conn.execute (s).fetchone()

        s=text("SELECT u.Ruolo, COUNT(*) AS Tipo FROM users u GROUP BY u.Ruolo") #totale utenti divisi per ruolo (Cliente, Operatore)
        numUtenti = conn.execute (s)

        s=text("SELECT COUNT(*) AS Aerei FROM aerei") #totale aerei
        numAerei = conn.execute (s).fetchone()

        s=text("SELECT AVG(v.PrezzoFirst) AS First, AVG(v.PrezzoBusiness) AS Business, AVG(v.PrezzoEconomy) AS Economy FROM voli v")
        #prezzo medio del biglietto di first class, business class ed economy class
        biglietto = conn.execute (s).fetchone()

        s=text("SELECT c.CodClassi, COUNT(p.CodClassi) AS Numero FROM classi c LEFT JOIN posti p ON c.CodClassi = p.CodClassi GROUP BY c.CodClassi")
        #numero di posti prenotati per classe
        classi = conn.execute (s)

        s=text("SELECT v.CodVoli, v.PrezzoFirst, v.PrezzoBusiness, v.PrezzoEconomy, v.Durata, l1.Citta AS Parte, l2.Citta AS Arriva, v.NumScali, v.Sconto FROM voli v JOIN localita l1 ON v.Da = l1.COdLocalita JOIN localita l2 ON v.Verso = l2.CodLocalita ORDER BY v.PrezzoFirst DESC")
        #informazioni di tutti ogni volo
        prezzi = conn.execute (s)

        conn.close() #connessione chiusa
        
        for row in numUtenti: #ciclo for sul totale degli utenti
            if row['Ruolo']=='Cliente':
                numClienti = row['Tipo'] #Clienti
            elif row['Ruolo']=='Operatore':
                numOperatori = row['Tipo'] #Operatori
        
        for row in classi: #ciclo for sui posti per classe
            if row['CodClassi']=='First':
                first = row['Numero'] #first class
            elif row['CodClassi']=='Business':
                business = row['Numero'] #business class
            else:
                economy = row['Numero'] #economy class

        return render_template("statistiche.html", logged=current_user.is_authenticated, totale=totale['Totale'], numClienti=numClienti, numOperatori=numOperatori, numAerei=numAerei['Aerei'], biglietto=biglietto, first=first, business=business, economy=economy, prezzi = prezzi) #render della pagina html "statistiche"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando un "Operatore" vuole registrare un nuovo "Operatore", richiama questa funzione.
Funziona come la funzione 'registrazionePagina', ma renderizza un'altra pagina html.
"""
@app.route('/regOperatorePagina', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def regOperatorePagina():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        return render_template("reg_operatore.html", logged=current_user.is_authenticated) #render della pagina html "reg_operatore"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente compila i campi per registrare un altro "Operatore" e preme sull'input
"Fatto", viene chiamata questa funzione. Viene verificato che l'ID inserito non sia mai
stato inserito prima e, in caso negativo, invita l'utente ad inserire un altro ID. In caso
positivo, l'utente viene inserito nella tabella users e viene creato un user che potra'
avere accesso al localhost con la propria password; poi, gli viene garantito il ruolo
di "Operatore". Funziona come la funzione 'registrazione', ma al posto di garantire il
ruolo di "Cliente" al nuovo utente registrato, gli assegna quello di "Operatore". Questo
e' fatto affiche' un nuovo utente non possa decidere se registrarsi come "Cliente" o come
"Operatore", preservando cosi la veridicita' dei dati nelle taballe del database che non
possono essere intaccate da utenti che non dovrebbero potervi accedere.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"SERIALIZABLE". Infatti, se due utenti tentano di registrarsi con lo stesso codice ID
nello stesso momento, non possono piu' essere distinti correttamente; quindi serve che
avvenga un lock sulla tabella, per permettere ad uno alla volta di accedervi e fare
l'inserimento.
"""
@app.route('/regOperatore', methods=['GET', 'POST'])
def regOperatore():
    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE") #livello di isolamento SERIALIZABLE
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("SELECT u.ID FROM users u WHERE u.ID =:codice")  #ricerca utente con l'ID specificato
        id = conn.execute (s, codice=request.form['codice']).fetchone()

        if id: #controllo esistenza di quell'utente
            conn.execute("COMMIT") #commit delle operazioni
            conn.close() #connessione chiusa
            flash('Errore: inserire un ID diverso','error') #messaggio di errore
            return redirect(url_for('regOperatorePagina')) #rimando alla pagina di registrazione dell'operatore

        s=text("INSERT INTO users VALUES(:codice,:nome,:email,:password,'Operatore')") #inserimento dell'utente nella tabella users
        rs = conn.execute (s, codice=request.form['codice'],nome=request.form['utente'],email=request.form['inputEmail'],password=request.form['password'])

        s=text("create user :codice@'localhost' identified with mysql_native_password by :password")  #creazione dell'user per l'accesso al localhost
        rs = conn.execute (s, codice=request.form['codice'],password=request.form['password'])

        s=text("GRANT Operatore to :codice@'localhost' WITH ADMIN OPTION") #garantire il ruolo di "Operatore" all'utente
        rs = conn.execute (s, codice=request.form['codice'])

        rs = conn.execute ("FLUSH PRIVILEGES") #ricarica la tabella dei permessi
        conn.execute("COMMIT") #commit delle operazioni
        conn.close() #connessione chiusa
        return redirect(url_for('operatore')) #rimando all'area riservata dell'utente
    except: #qualcosa non e' andata a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: registrazione non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('regOperatorePagina')) #rimando alla pagina di registrazione dell'operatore

"""
Quando un "Operatore" vuole registrare un nuovo volo, richiama questa funzione.
Per registrare un volo serve avere l'elenco di tutte le localita' da cui si puo'
partire e in cui si puo' arrivare, in piu' l' "Operatore" vorra' indicare quanti
posti vuole per quel volo. Si procede, quindi, facendo delle ricerche per le
localita' e per il numero di posti (o meglio, di file) per gli aerei. Poi si
carica la pagina.
"""
@app.route('/regVoloPagina', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def regVoloPagina():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        conn=engine.connect() #connessione aperta
        s=text("SELECT l.CodLocalita, l.Citta, l.NomeAeroporto FROM localita l ORDER BY l.Citta") #ricerca di tutte le localita'
        citta = conn.execute (s)
        s=text("SELECT DISTINCT a.NumFile FROM aerei a ORDER BY a.NumFile") #ricerca del numero di file
        aerei = conn.execute (s)
        conn.close() #connessione chiusa
        return render_template("reg_voli.html", logged=current_user.is_authenticated, citta=citta, aerei=aerei) #render della pagina html "reg_voli"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente compila i campi per registrare un nuovo volo e preme sull'input
"Fatto", viene chiamata questa funzione. Qui vengono estrapolati i codici delle
localita' e del numero di posti dalle stringhe che arrivano dall'html e si trova
il numero di file che deve avere l'aereo. Per trovare il codice dell'aereo che ha
quel numero di file si cerca tra gli aerei non gia' occupati per il giorno della
partenza indicato dell'utente. Viene verificato che ci sia almeno un aereo disponibile
e, in caso positivo, viene inserito il nuovo volo nella tabella voli. In caso negativo,
invita l'utente ad inserire un altro numero di posti.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"SERIALIZABLE". Infatti, se due utenti tentano di inserire un volo per lo stesso giorno
con lo stesso numero di posti e rimane un solo aereo disponibile con quel numero di
posti, entrambi lo sceglieranno, causando un conflitto nell'uso degli aerei per quel
giorno; quindi serve che avvenga un lock sulla tabella, per permettere ad uno alla
volta di accedervi e fare l'inserimento.
"""
@app.route('/regVolo', methods=['GET', 'POST'])
def regVolo():
    da = request.form['da'] #luogo di partenza
    verso = request.form['verso'] #luogo di arrivo
    aereo = request.form['aereo'] #numero posti dell'aereo
    partenza=request.form['partenza'] #data e ora di partenza

    da = re.sub("[^0-9]+","",da) #rimozione delle lettere dal luogo di partenza
    verso = re.sub("[^0-9]+","",verso) #rimozione delle lettere dal luogo di arrivo
    posti = re.sub("[^0-9]+","",aereo) #rimozione delle lettere dal numero di posti dell'aereo
    file = (int(posti) + 2) / 6 #calcolo di quante file servono

    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE") #livello di isolamento SERIALIZABLE
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("SELECT a.CodAerei FROM aerei a WHERE a.NumFile =:file AND a.CodAerei NOT IN (SELECT v.CodAerei FROM voli v WHERE DATE(v.partenza) = DATE(:partenza)) LIMIT 1")
        #ricerca del codice dell'aereo con in numero di file giusto disponibile in quella data
        codA = conn.execute(s, file=file, partenza=partenza).fetchone()

        if codA: #controllo esistenza di quell'aereo
            s=text("INSERT INTO voli (Partenza,Arrivo,Durata,CodAerei,Da,Verso,NumScali,PrezzoFirst,PrezzoBusiness,PrezzoEconomy,Sconto) VALUES(:partenza,:arrivo,:durata,:aereo,:da,:verso,:scali,:first,:business,:economy,:sconto)")
            #inserimento del volo nella taballa voli
            rs = conn.execute (s, partenza=partenza,arrivo=request.form['arrivo'],durata=request.form['durata'],aereo=codA['CodAerei'],da=da,verso=verso,scali=request.form['scali'],first=request.form['first'],business=request.form['business'],economy=request.form['economy'],sconto=request.form['sconto'])
            conn.execute("COMMIT") #commit delle operazioni
            conn.close() #connessione chiusa
            return redirect(url_for('operatore')) #rimando all'area riservata dell'utente
        else: #aereo non esistente
            conn.execute("COMMIT") #commit delle operazioni
            conn.close() #connessione chiusa
            flash('Errore: nessun aereo disponibile, cambiare numero di posti','error') #messaggio di errore
            return redirect(url_for('regVoloPagina')) #rimando all'area riservata dall'utente
    except: #qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollbakc delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: registrazione non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('regVoloPagina')) #rimando alla pagina di registrazione del volo

"""
Quando un "Operatore" vuole registrare un nuovo aereo, richiama questa funzione.
Per registrare un aereo non sono richieste conoscenze esterne, quindi si carica
la pagina.
"""
@app.route('/regAereoPagina', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def regAereoPagina():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        return render_template("reg_aerei.html", logged=current_user.is_authenticated) #render della pagina html "reg_aerei"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente compila i campi per registrare un nuovo aereo e preme sull'input
"Fatto", viene chiamata questa funzione. Qui viene inserito il nuovo aereo nella
tabella aerei.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"READ COMMITTED". Infatti, se un utente sta inserendo un nuovo aereo e un altro utente
sta inserendo un nuovo volo e quest'ultimo seleziona quell'aereo (attraverso la ricerca
dei posti), ma poi il primo utente non completa l'inserimento, il secondo utente si
trovera' con un volo che ha un aereo inesistente; quindi serve che per visualizzare il
nuovo aereo, questo deve aver finito e portato a buon termine il suo inserimento.
"""
@app.route('/regAereo', methods=['GET', 'POST'])
def regAereo():
    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED") #livello di isolamento READ COMMITTED
    conn.execute("START TRANSACTION") #inizio transazione
    try:
       s=text("INSERT INTO aerei (Tipo,NumFile,PesoStiva) VALUES(:tipo,:file,:stiva)") #inserimento dell'aereo nella tabella aerei
       rs = conn.execute (s, tipo=request.form['tipo'],file=request.form['file'],stiva=request.form['stiva'])
       conn.execute("COMMIT") #commit delle operazioni
       conn.close() #connessione chiusa
       return redirect(url_for('operatore')) #rimando all'area riservata dell'utente
    except:
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: registrazione non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('regAereoPagina')) #rimando alla pagina di registrazione dell'aereo

"""
Quando un "Operatore" vuole registrare una nuova meta, richiama questa funzione.
Per registrare una meta non sono richieste conoscenze esterne, quindi si carica
la pagina.
"""
@app.route('/regMetaPagina', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def regMetaPagina():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        return render_template("reg_mete.html", logged=current_user.is_authenticated) #render della pagina html "reg_mete"
    else: #altrp
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente compila i campi per registrare una nuova meta e preme sull'input
"Fatto", viene chiamata questa funzione. Qui viene inserita la nuova meta nella
tabella localita.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"READ COMMITTED". Infatti, se un utente sta inserendo una nuova meta e un altro utente
sta inserendo un nuovo volo e quest'ultimo seleziona quella meta come luogo di arrivo,
ma poi il primo utente non completa l'inserimento, il secondo utente si trovera' con un
volo che arriva in un luogo inesistente; quindi serve che per visualizzare la
nuova meta, questo deve aver finito e portato a buon termine il suo inserimento.
"""
@app.route('/regMeta', methods=['GET', 'POST'])
def regMeta():
    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED") #livello di isolamento READ COMMITTED
    conn.execute("START TRANSACTION") #inizio transazione
    try:
       s=text("INSERT INTO localita (Citta,Nazione,NomeAeroporto) VALUES(:citta,:nazione,:aeroporto)") #inserimento della meta nella tabella localita
       rs = conn.execute (s, citta=request.form['citta'],nazione=request.form['nazione'],aeroporto=request.form['aeroporto'])
       conn.execute("COMMIT") #commit delle operazioni
       conn.close() #connessione chiusa
       return redirect(url_for('operatore')) #rimando all'area riservata dell'utente
    except: #qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: registrazione non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('regMetaPagina')) #rimando alla pagina di registrazione delle mete

"""
Quando un "Operatore" vuole modificare un volo, richiama questa funzione.
Per modificare un volo serve avere l'elenco di tutti i voli con le loro localita'
di partenza e di arrivo. Si procede, quindi, facendo delle ricerche per le
localita' e per la durata dei voli, poi si carica la pagina.
"""
@app.route('/modificaVoloPagina', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def modificaVoloPagina():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        conn=engine.connect() #connessione aperta
        s=text("SELECT v.CodVoli, v.Durata, l1.Citta AS Parte, l2.Citta AS Arriva FROM voli v JOIN localita l1 ON l1.CodLocalita = v.Da JOIN localita l2 ON l2.CodLocalita = v.Verso")
        #ricerca dei voli con le localita' di partenza e di arrivo
        voli = conn.execute (s)
        conn.close() #connessione chiusa
        return render_template("modifica_voli.html", logged=current_user.is_authenticated, voli=voli) #render della pagina html "modifica_voli"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente compila i campi per modificare un volo e preme sull'input
"Modifica", viene chiamata questa funzione. Qui viene estrapolato il codice del volo
da modificare. Dopo viene aggiornato il prezzo dei vari biglietti per le diverse classi
del volo e lo sconto.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"REPEATABLE READ". Infatti, se un utente sta aggiornando un volo e un altro utente
sta facendo una prenotazione questo potrebbe ottenere un totale da pagare che poi e' diverso
da quello che paga veramente perche' nel frattempo il valore del biglietto o dello sconto
e' cambiato; quindi, per non avere lost update, serve che, per calcolare il prezzo da pagare
per un volo, l'aggiornamento di quest'ultimo sia terminato.
"""
@app.route('/modificaVolo', methods=['GET', 'POST'])
def modificaVolo():
    codice = request.form['codice'] #informazioni del volo
    tipo=codice.split(' - ') #separazione delle informazioni del volo
    for p in tipo: #ciclo for sulle informazioni del volo
        cod = p
    volo = re.sub("[^0-9]+","",cod) #rimozione delle lettere per ottenere il codice del volo

    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ") #livello di isolamento REPEATABLE READ
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("UPDATE voli SET PrezzoFirst =:first, PrezzoBusiness =:business, PrezzoEconomy =:economy, Sconto =:sconto WHERE CodVoli =:volo")
        #aggiornamento dei prezzi e dello sconto del volo in questione
        rs = conn.execute (s, first=request.form['first'],business=request.form['business'],economy=request.form['economy'],sconto=request.form['sconto'],volo=volo)
        conn.execute("COMMIT") #commit delle operazioni
        conn.close() #connessione chiusa
        return redirect(url_for('operatore')) #rimando all'area riservata dell'utente
    except: #qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: modifica non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('modificaVoloPagina')) #rimando alla pagina di modifica del volo

"""
Quando un "Operatore" vuole modificare un aereo, richiama questa funzione.
Per modificare un aereo serve avere l'elenco di tutti gli aerei tra cui scegliere
quello da modificare. Poi si carica la pagina.
"""
@app.route('/modificaAereoPagina', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def modificaAereoPagina():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        conn=engine.connect() #connessione aperta
        s=text("SELECT a.CodAerei, a.Tipo FROM aerei a") #ricerca di tutti gli aerei
        aerei = conn.execute (s)
        conn.close() #connessione chiusa
        return render_template("modifica_aerei.html", logged=current_user.is_authenticated, aerei=aerei) #render della pagina html "modifica_aerei"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente compila i campi per modificare un aereo e preme sull'input
"Modifica", viene chiamata questa funzione. Qui viene estrapolato il codice dell'aereo
da modificare, il peso della stiva vecchio e quello da agginugere. Dopo, viene
modificato il numero di file presenti nell'aereo e il peso della stiva.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"REPEATABLE READ". Infatti, se due utenti stanno modificando il peso della stiva dello
stesso aereo e il primo va ad aggiungere 20 kg, mentre il secondo va ad aggiungere 30 kg,
se il primo conclude dopo che il secondo ha iniziato, il secondo avra' preso come
riferimento il peso della stiva senza i 20 kg che il primo utente aveva aggiunto, finendo
con il riportare il peso sbagliato alla fine; quindi, per non avere lost update, serve
che l'aggiornamento del peso della stiva sia terminato prima di farne un altro.
"""
@app.route('/modificaAereo', methods=['GET', 'POST'])
def modificaAereo():
    file = request.form['file'] #numero di file da aggiungere
    stiva = request.form['stiva'] #numero di kg da aggiungere in stiva
    codice = request.form['codice'] #informazioni dell'aereo
    tipo=codice.split(' - ') #separazione delle informazioni dell'aereo
    for p in tipo: #ciclo for sulle informazioni dell'aereo
        cod = p
    aereo = re.sub("[^0-9]+","",cod) #rimozione delle lettere per ottenere il codice dell'aereo

    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ") #livello di isolamento REPEATABLE READ
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("SELECT a.NumFile, a.PesoStiva FROM aerei a WHERE a.CodAerei =:aereo") #ricerca numero file e peso stiva vecchi
        vecchi = conn.execute (s, aereo=aereo).fetchone()
        s=text("UPDATE aerei SET NumFile =:file, PesoStiva =:stiva WHERE CodAerei =:aereo") #aggiornamento numero file aereo
        rs = conn.execute (s, file=((int(file)) + (int(vecchi['NumFile']))),stiva=((int(stiva)) + (int(vecchi['PesoStiva']))),aereo=aereo)
        conn.execute("COMMIT") #commit delle operazioni
        conn.close() #connessione chiusa
        return redirect(url_for('operatore')) #rimando all'area riservata dell'operatore
    except: #qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: modifica non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('modificaAereoPagina')) #rimando alla pagina di modifica dell'aereo

"""
Quando un "Operatore" vuole modificare una meta, richiama questa funzione.
Per modificare una meta serve avere l'elenco di tutte le mete tra cui scegliere
quello da modificare. Poi si carica la pagina.
"""
@app.route('/modificaMetaPagina', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def modificaMetaPagina():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        conn=engine.connect() #connessione aperta
        s=text("SELECT l.CodLocalita, l.Citta, l.NomeAeroporto FROM localita l") #ricerca di tutte le mete
        citta = conn.execute (s)
        conn.close() #connessione chiusa
        return render_template("modifica_mete.html", logged=current_user.is_authenticated, citta=citta) #render della pagina html "modifica_mete"
    else:
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente compila i campi per modificare una meta e preme sull'input
"Modifica", viene chiamata questa funzione. Qui viene estrapolato il codice della meta
da modificare. Dopo, viene modificato il nome dell'areoporto di questa meta.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"READ COMMITTED". Infatti, se un utente sta inserendo una nuova meta e un altro utente
sta inserendo un nuovo volo e quest'ultimo seleziona quella meta come luogo di arrivo e
questa meta sta cambiando nome dell'areoporto con un nome di un altro aeroporto nella
stessa citta', ma poi il primo utente non completa l'inserimento, il secondo utente si
trovera' con un volo che arriva in un luogo con un aeroporto inesistente; quindi serve
che per visualizzare la meta modificata, l'aggiornamento di quest'ultima sia terminato.
"""
@app.route('/modificaMeta', methods=['GET', 'POST'])
def modificaMeta():
    codice = request.form['codice'] #informazioni della meta
    tipo=codice.split(' - ') #separazione delle informazioni della meta
    for p in tipo: #ciclo for sulle informazioni della meta
        cod = p
    citta = re.sub("[^0-9]+","",cod) #rimozione delle lettere per ottenere il codice della meta

    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED") #livello di isolamento READ COMMITTED
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("UPDATE localita SET NomeAeroporto =:aeroporto WHERE CodLocalita =:citta") #aggiornamento nome dell'areoporto
        rs = conn.execute (s, aeroporto=request.form['aeroporto'],citta=citta)
        conn.execute("COMMIT") #commit delle operazioni
        conn.close() #connessione chiusa
        return redirect(url_for('operatore')) #rimando all'area riservata dell'utente
    except: #qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: modifica non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('modificaMetaPagina')) #rimando alla pagina di modifica della meta

"""
Quando un "Operatore" vuole cancellare un volo, richiama questa funzione.
Per cancellare un volo serve avere l'elenco di tutti i voli con le loro localita'
di partenza e di arrivo. Si procede, quindi, facendo delle ricerche per le
localita' dei voli, poi si carica la pagina.
"""
@app.route('/cancellaVoloPagina', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def cancellaVoloPagina():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        conn=engine.connect() #connessione aperta
        s=text("SELECT v.CodVoli, l1.Citta AS Parte, l2.Citta AS Arriva FROM voli v JOIN localita l1 ON l1.CodLocalita = v.Da JOIN localita l2 ON l2.CodLocalita = v.Verso")
        #ricerca di tutti i voli e delle localita' di arrivo e di partenza
        voli = conn.execute (s)
        conn.close() #connessione chiusa
        return render_template("cancella_voli.html", logged=current_user.is_authenticated, voli=voli) #render della pagina html "cancella_voli"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente cancella un volo e preme sull'input "Cancella", viene chiamata questa
funzione. Qui viene estrapolato il codice del volo. Dopo, viene cancellato il volo
dalla tabella voli.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"SERIALIZABLE". Infatti, se un utente sta prenotando un volo e un altro utente sta
cancellando quel volo, il primo utente si ritrovera' con la prenotazione di un volo
che non esiste; quindi serve che avvenga un lock sulla tabella, per permettere al
secondo utente di cancellare il volo senza causare danni.
"""
@app.route('/cancellaVolo', methods=['GET', 'POST'])
def cancellaVolo():
    codice = request.form['codice'] #informazioni del volo
    tipo=codice.split(' - ') #separazione delle informazioni del volo
    for p in tipo: #ciclo for sulle informazioni del volo
        cod = p
    volo = re.sub("[^0-9]+","",cod) #rimozione delle lettere per ottenere il codice del volo

    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE") #livello di isolamento SERIALIZABLE
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("DELETE FROM voli v WHERE v.CodVoli =:volo") #cancellazione del volo
        rs = conn.execute (s, volo=volo)
        conn.execute("COMMIT") #commit delle operazioni
        conn.close() #connessione chiusa
        return redirect(url_for('operatore')) #rimando all'area riservata dell'utente
    except:#qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: cancellazione non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('cancellaVoloPagina')) #rimando alla pagina di cancellazione del volo

"""
Quando un "Operatore" vuole cancellare un aereo, richiama questa funzione.
Per cancellare un aereo serve avere l'elenco di tutti gli aerei tra cui scegliere
quello da cancellare. Poi si carica la pagina.
"""
@app.route('/cancellaAereoPagina', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def cancellaAereoPagina():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        conn=engine.connect() #connessione aperta
        s=text("SELECT a.CodAerei, a.Tipo FROM aerei a") #ricerca di tutti gli aerei
        aerei = conn.execute (s)
        conn.close() #connessione chiusa
        return render_template("cancella_aerei.html", logged=current_user.is_authenticated, aerei=aerei) #render della pagina html "cancellazione_aerei"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente cancella un aereo e preme sull'input "Cancella", viene chiamata questa
funzione. Qui viene estrapolato il codice dell'aereo. Dopo, viene cancellato l'aereo
dalla tabella aerei.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"SERIALIZABLE". Infatti, se un utente sta prenotando un volo e un altro utente sta
cancellando l'aereo di quel volo, il primo utente si ritrovera' con la prenotazione di un volo
che non esiste (per l'ON DELETE CASCADE); quindi serve che avvenga un lock sulla tabella, per
permettere al secondo utente di cancellare l'aereo senza causare danni.
"""
@app.route('/cancellaAereo', methods=['GET', 'POST'])
def cancellaAereo():
    codice = request.form['codice'] #informazioni dell'aereo
    tipo=codice.split(' - ') #separazione delle informazioni dell'aereo
    for p in tipo: #ciclo for suelle informazioni dell'aereo
        cod = p
    aereo = re.sub("[^0-9]+","",cod) #rimozione delle lettere per ottenere il codice dell'aereo

    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE") #livello di isolamento SERIALIZABLE
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("DELETE FROM aerei a WHERE a.CodAerei =:aereo") #cancellazione aereo
        rs = conn.execute (s, aereo=aereo)
        conn.execute("COMMIT") #commit delle operazioni
        conn.close() #connessione chiusa
        return redirect(url_for('operatore')) #rimando all'area riservata dell'utente
    except: #qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: cancellazione non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('cancellaAereoPagina')) #rimando alla pagina di cancellazione dell'aereo

"""
Quando un "Operatore" vuole cancellare una meta, richiama questa funzione.
Per cancellare una meta serve avere l'elenco di tutte le mete tra cui scegliere
quello da cancellare. Poi si carica la pagina.
"""
@app.route('/cancellaMetaPagina', methods=['GET', 'POST'])
@login_required #richiede autenticazione
def cancellaMetaPagina():
    if (current_user.get_ruolo()=="Operatore"): #Operatore
        conn=engine.connect() #connessione aperta
        s=text("SELECT l.CodLocalita, l.Citta, l.NomeAeroporto FROM localita l") #ricerca di tutte le mete
        citta = conn.execute (s)
        conn.close() #connessione chiusa
        return render_template("cancella_mete.html", logged=current_user.is_authenticated, citta=citta) #render della pagina html "cancella_mete"
    else: #altro
        return redirect(url_for('home')) #rimando alla home page

"""
Quando l'utente cancella una meta e preme sull'input "Cancella", viene chiamata questa
funzione. Qui viene estrapolato il codice della meta. Dopo, viene cancellata la meta
dalla tabella localita.
Questa sezione di codice prevede che ci sia una transazione con livello di isolamento
"SERIALIZABLE". Infatti, se un utente sta prenotando un volo e un altro utente sta
cancellando la meta di partenza di quel volo, il primo utente si ritrovera' con la
prenotazione di un volo che non esiste (per l'ON DELETE CASCADE); quindi serve che avvenga
un lock sulla tabella, per permettere al secondo utente di cancellare la meta senza
causare danni.
"""
@app.route('/cancellaMeta', methods=['GET', 'POST'])
def cancellaMeta():
    codice = request.form['codice'] #informazioni della meta
    tipo=codice.split(' - ') #separazione delle informazioni della meta
    for p in tipo: #ciclo for sulle informazioni della meta
        cod = p
    citta = re.sub("[^0-9]+","",cod) #rimozione delle lettere per ottenere il codice della meta

    conn=engine.connect() #connessione aperta
    conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE") #livello di isolamento SERIALIZABLE
    conn.execute("START TRANSACTION") #inizio transazione
    try:
        s=text("DELETE FROM localita l WHERE l.CodLocalita =:citta") #cancellazione meta
        rs = conn.execute (s, citta=citta)
        conn.execute("COMMIT") #commit delle operazioni
        conn.close() #connessione chiusa
        return redirect(url_for('operatore')) #rimando all'area riservata dell'utente
    except: #qualcosa non e' andato a buon fine
        conn.execute("ROLLBACK") #rollback delle operazioni
        conn.close() #connessione chiusa
        flash('Errore: cancellazione non riuscita, riprovare','error') #messaggio di errore
        return redirect(url_for('cancellaMetaPagina')) #rimando alla pagina di cancellazione della meta



"""
Qui c'e' il main che fa funzionare la web app.
"""
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
