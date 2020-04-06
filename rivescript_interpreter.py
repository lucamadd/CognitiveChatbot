#!/usr/bin/python3

# Python 3 example

from rivescript import RiveScript
from server_functions import get_random_user_id
import json
import re
import socket
import spell_checker_italian as spell
rs = RiveScript(utf8=True)
rs.unicode_punctuation = re.compile(r'[,!?;:]')
rs.load_directory("./brain/")
rs.sort_replies()
#rs.set_uservar(get_current_user(),'id',get_current_user())


def set_user_var(user,var,value):
    """
    Imposta una variabile all'utente selezionato

    :param user : l'utente a cui assegnare la variabile
    :param var  : il nome della variabile
    :param value: il valore da assegnare
    """
    rs.set_uservar(user,var,value)

def set_metadata(value, user_id='localuser', name='metadata'):
    """
    Imposta la variabile 'metadata' all'utente selezionato
    Usato per gestire i diversi tipi di richieste HTTP

    :param value  : il valore da assegnare
    :param user_id: l'utente a cui assegnare la variabile
    :param name   : il nome della variabile (default metadata)
    
    """
    rs.set_uservar(user_id,name,value)

def get_metadata(user_id='localuser'):
    """
    Recupera la variabile metadata dall'utente selezionato

    :param user_id: l'utente da cui recuperare la variabile (default localuser)
    """
    return rs.get_uservar(user_id,'metadata')

def get_reply(msg, user_id='localuser'):
    """
    Cerca una risposta compatibile per il messaggio inviato

    :param msg    : il messaggio inviato dall'utente
    :param user_id: l'utente a cui inviare la risposta
    """
    return rs.reply(user_id,msg)

def get_last_match(user_id='localuser'):
    """
    Recupera l'ultima risposta inviata dal bot

    :param user_id: l'utente da cui recuperare la risposta
    """
    return rs.last_match(user_id)

def no_responses():
    """
    Recupera l'insieme delle risposte predefinite del bot in caso
    di no-match
    """
    with open('assets/intents.json',encoding='utf-8') as json_data:
        intents = json.load(json_data)
    for intent in intents['intents']:
        if intent['tag'] == 'no_response':
            if 'no_response' in intent['tag']:
                return intent['responses']
            


def check_command(sentence,user):
    """
    Restituisce True se la frase passata in input
    produce una risposta dal bot, restituisce False
    se il bot non è riuscito a capire la frase. 

    :param sentence: la frase da analizzare
    :param user    : l'utente a cui rispondere
    """
    reply = get_reply(sentence,user)
    print(f"check command returns {reply}")
    if reply not in no_responses():
        return reply
    return False


def raw_input():
    """
    Utility per provare il bot da riga di comando
    """
    from rivescript import RiveScript
    rs = RiveScript(utf8=True)
    rs.unicode_punctuation = re.compile(r'[,!?;:]')
    rs.load_directory("./brain/")
    rs.sort_replies()
    user = get_random_user_id()
    rs.set_uservar(user,'id',user)

    while True:
        msg = input("You> ")
        if msg == '/quit':
            quit()
        reply = rs.reply(user, msg)
        print("Bot>", reply)


if __name__ == "__main__":
    raw_input()


        