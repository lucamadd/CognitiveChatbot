import requests
import random
import json

def post_request(metadata,args):
    """
    Effettua una richiesta HTTP con metodo POST

    :param metadata: il valore da cercare negli intent
                     per recuperare l'url

    :param args    : i parametri da utilizzare nella richiesta
    """
    try:
        param_names = []
        URL= ""
        PARAMS = {}
        with open('assets/intents.json',encoding='utf-8') as json_data:
            intents = json.load(json_data)
        for intent in intents['intents']:
            if intent['tag'] == metadata and 'metadata' in intent:
                param_names.extend(intent['metadata'])
                URL = intent['url']
        if not param_names:
            try:
                result = requests.post(url = URL)
            except Exception:
                return "C'è stato un errore. Verifica la connessione e riprova."
            return result.text

        if len(args) != len(param_names):
            if len(param_names) is 1:
                return f"Non hai specificato il numero giusto di parametri.\nHo bisogno di un solo parametro. Riprova."
            return f"Non hai specificato il numero giusto di parametri.\nHo bisogno di {len(param_names)} parametri. Riprova."

        PARAMS = dict(zip(param_names,args))

        result = ""
        try:
            result = requests.post(url = URL, params = PARAMS)
        except Exception as e:
            return f"C'è stato un errore. Verifica la connessione e riprova. {e}"
        
    except Exception as e:
        return f"C'è stato un errore. Verifica la connessione e riprova. {e}"
    return result.text



def login_admin(body):
    """
    Controlla la password inserita per il login per la configurazione
    del bot

    :param body: il corpo del messaggio da cui estrapolare la password
    """
    given_password = body[9:]
    pass_file = open('assets/config.ini','r', encoding='utf-8')
    current_password = pass_file.read()
    if given_password == current_password:
        return 'true'
    else:
        return 'false'

def change_password(body):
    """
    Funzione per cambiare password

    :param body: il corpo del messaggio contenente le password inserite
                 (criptate con SHA-256)
    """
    old_password = body[body.find('old_password=')+13:body.find('&new_password=')]
    new_password = body[body.find('new_password=')+13:body.find('&confirm_password=')]
    confirm_password = body[body.find('confirm_password=')+17:]

    if new_password != confirm_password:
        return 'false'

    pass_file = open('assets/config.ini','r', encoding='utf-8')
    current_password = pass_file.read()
    pass_file.close()

    if old_password == current_password:
        pass_file = open('assets/config.ini','w', encoding='utf-8')
        pass_file.write(new_password)
        pass_file.close()
        return 'true'
    else:
        return 'false'

def get_random_user_id():
    """
    Crea un ID random per disambiguare gli utenti
    """
    return ''.join(random.choice('abcdefghijklmnopqrtuvwxyz123456789') for _ in range(7))

def clean_word(word):
    """
    Elimina le lettere accentate dalla parola inserita
    """
    word = word.replace("à","a")
    word = word.replace("è","e")
    word = word.replace("é","e")
    word = word.replace("ì","i")
    word = word.replace("ò","o")
    word = word.replace("ù","u")
    word = word.replace("a'","a")
    word = word.replace("e'","e")
    word = word.replace("i'","i")
    word = word.replace("o'","o")
    word = word.replace("u'","u")

    return word

