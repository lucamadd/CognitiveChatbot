#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py
"""
MIN_WORDS_OCCURENCE=0


CURRENT_USER = 'localuser'


print ("Loading libs...")
import re
import requests
import nltk
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs, unquote_plus

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from flask import Flask, current_app, send_file, request, jsonify, redirect, url_for
from flask_cors import cross_origin, CORS
app = Flask(__name__,
            static_url_path='', 
            static_folder='static')
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)

from urllib.parse import unquote_plus
from nltk.stem.snowball import ItalianStemmer
stemmer = ItalianStemmer()

# italian spellchecker
import spell_checker_italian as spell
import rivescript_interpreter as rs
import server_functions as tools
# things we need for Tensorflow
import numpy as np
import tflearn
import random
import os
import uuid
import base64

# has to suppress warnings cause tflearn is not available in tf 2.0
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# restore all of our data structures
print ("Loading training_data...")
import pickle
data = pickle.load( open( "tf_model/training_data", "rb") )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']
print("\n\n\nDATA_WORDS:")
print(words)
print("\n\n\nDATA_CLASSES:")
print(classes)
print("\n\n\nDATA_TRAIN_X:")
print(train_x)
print("\n\n\nDATA_TRAIN_Y:")
print(train_y)

# import our chat-bot intents file
import json
print ("Loading intents...")
with open('assets/intents.json',encoding='utf-8') as json_data:
    intents = json.load(json_data)
# Build neural network
print ("Preparing neural network...")
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
print ("Neural network ready")

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

def clean_up_sentence(sentence):
    """
    Si occupa di spezzare la frase in token e applicare lo stemmer

    :param sentence: la frase da elaborare

    """ 
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    print(f"SENTENCE WORDS: {sentence_words}")
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    """
    Crea una bag of words dalla frase

    :param sentence    : la frase da analizzare
    :param words       : le parole da cercare nella frase
    :param show_details: parametro di debug
    """
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
                   
    
    return(np.array(bag))

def not_in_bag(sentence, words, show_details=True):
    """
    Trova le parole del vocabolario che non sono presenti
    nella frase

    :param sentence    : la frase da analizzare
    :param words       : le parole da cercare nella frase
    :param show_details: parametro di debug
    """
    # tokenize the pattern
    sentence_words_cleaned = clean_up_sentence(sentence)
    sentence_words = nltk.word_tokenize(sentence)
    words_not_in_bag = []

    for i in range(len(sentence_words_cleaned)):
        if sentence_words_cleaned[i] not in words:
            words_not_in_bag.append(sentence_words[i])
    
    return words_not_in_bag

# load our saved model
model.load('tf_model/model.tflearn')

# create a data structure to hold user context
context = {}

ERROR_THRESHOLD = 0.7
def classify(sentence):
    """
    Trova tutti i possibili intent per la frase

    :param sentence: la frase da analizzare
    """
    # generate probabilities from the model
    bag=[bow(sentence, words)]
    print ("Bag: ", bag)
    results = model.predict(bag)[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r > ERROR_THRESHOLD]
    print("All results: ",results)
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    print("Classes: ", classes)
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    lenBagOccurence=bag[0].sum()
    print("lenBagOccurence:",lenBagOccurence)
    if lenBagOccurence<MIN_WORDS_OCCURENCE:
        print("lenBagOccurence<MIN_WORDS_OCCURENCE")
        return False
    return return_list


def post_request(URL, PARAMS):
    """
    Invia una richiesta HTTP con metodo POST

    :param URL   : l'url a cui mandare la richiesta
    :param PARAMS: i parametri da aggiungere nella richiesta
    """
    # parse json
    result = requests.post(URL, PARAMS)
    return result.json()

def fix_htmls():
    """
    Inserisce i tag e i contesti nei file tags.html e 
    contexts.html
    """
    with open('assets/intents.json', 'r', encoding='utf-8') as json_data:
        intents = json.load(json_data)
    
    tags_html = open('../tags.html','w',encoding='utf-8')
    tags = []
    for field in intents['intents']:
        if 'tag' in field:
            tags.append(field['tag'])
    for tag in tags:
        tags_html.write(f'<br>{tag}')
    tags_html.close()

    contexts_html = open('../contexts.html','w',encoding='utf-8')
    contexts = []
    for field in intents['intents']:
        if 'context_set' in field:
            contexts.append(field['context_set'])
    print(contexts)
    for cont in contexts:
        if cont:
            contexts_html.write(f'<br>{cont}')
    contexts_html.close()


def add_intent(data):
    """
    Aggiunge un nuovo intento semplice al bot

    :param data: il file .json contenente le informazioni
    """
    import ast
    print(f'data is: {data}')
    tag = data[data.find('tag=')+4:data.find('&patterns=')].lower()
    patterns = data[data.find('patterns=')+9:data.find('&responses=')].lower()
    responses = data[data.find('responses=')+10:data.find('&context_set=')]
    if 'context_filter' in data:
        context_set = data[data.find('context_set=')+12:data.find('&context_filter=')]
        context_filter = data[data.find('context_filter=')+15:]
    else:
        context_set = data[data.find('context_set=')+12:]
        context_filter = None
    context_set = context_set.lower()
    # negli intent in json il contesto principale corrisponde al contesto
    # vuoto, mentre in rivescript deve essere specificato che è 'random'
    context_set_json = context_set
    if 'random' in context_set:
        context_set_json = ""
    print(f"tag is {tag}")
    print(f"patterns is {patterns}")
    print(f"responses is {responses}")
    print(f"context_set is {context_set}")
    print(f"context_filter is {context_filter}")

    # convert the string representation of list into actual list
    patterns = ast.literal_eval(patterns)
    responses = ast.literal_eval(responses)

    # add intents to json
    with open('assets/intents.json', 'r', encoding='utf-8') as json_data:
        intents = json.load(json_data)
    
    if context_filter is not None:
        intents['intents'].append({
            "tag": tag,
            "patterns": patterns,
            "responses": ['<msg>' + response + '</msg>' for response in responses],
            "context_set": context_set_json,
            "context_filter": context_filter
        })
    else:
         intents['intents'].append({
            "tag": tag,
            "patterns": patterns,
            "responses": ['<msg>' + response + '</msg>' for response in responses],
            "context_set": context_set_json
        })

    with open('assets/intents.json', 'w', encoding='utf-8') as json_data:
        json.dump(intents, json_data, indent=2)

    # add intent to rivescript brain
    # se non è None allora devo inserirlo nel contesto di riferimento
    if context_filter is not None:
        brain = open('brain/conversation.rive','r',encoding='utf-8')
        from shutil import move
        temp = open('temp', 'w+',encoding='utf-8')
        IS_CONTEXT = 0
        for line in brain:
            if f'> topic {context_filter}' in line:
                IS_CONTEXT = 1
                # se context_set esiste allora setto il contesto
                if context_set:
                    line = line + f'\n\n+ {tag.lower()}'
                    #brain.write(f'\n\n+ {tag}')
                    for response in responses:
                        #brain.write('\n- %s{topic=%s}',response,context_set)
                        line = line + '\n- '+response+'{topic='+context_set+'}'
                else:
                    line = line + f'\n\n+ {tag.lower()}'
                    #brain.write(f'\n\n+ {tag}')
                    for response in responses:
                        #brain.write(f'\n- {response}')
                        line = line + f'\n- {response}'
                        
                line = ''.join(line) + "\n\n"
                for pattern in patterns:
                    line = ''.join(line) + f'\n+ [*] {tools.clean_word(pattern.lower())} [*]\n@ {tag.lower()}\n'
            temp.write(line)
        temp.close()
        if IS_CONTEXT is 1:
            brain.close()
            move('temp','brain/conversation.rive')
        else:
            brain = open('brain/conversation.rive','a+',encoding='utf-8')
            brain.write(f'\n\n> topic {context_filter} inherits exit_topic\n')
            if context_set:
                brain.write(f'\n\n+ {tag.lower()}')
                for response in responses:
                    brain.write('\n- '+response+'{topic='+context_set+'}')
            else:
                brain.write(f'\n\n+ {tag.lower()}')
                for response in responses:
                    brain.write(f'\n- {response}')
            line = "\n\n"
            for pattern in patterns:
                line = ''.join(line) + f'\n+ [*] {tools.clean_word(pattern.lower())} [*]\n@ {tag.lower()}\n'
            brain.write(line)
            brain.write(f'\n\n< topic\n')
        brain.close()
    # altrimenti va inserito fuori dal contesto
    else:
        print(f"no context filter found. Context set is {context_set}")
        brain = open('brain/conversation.rive','a+',encoding='utf-8')
        if context_set:
            brain.write(f'\n\n+ {tag.lower()}')
            for response in responses:
                brain.write('\n- '+response+'{topic='+context_set+'}')
        else:
            brain.write(f'\n\n+ {tag.lower()}')
            for response in responses:
                brain.write(f'\n- {response}')
        line = "\n\n"
        for pattern in patterns:
            line = ''.join(line) + f'\n+ [*] {tools.clean_word(pattern.lower())} [*]\n@ {tag.lower()}\n'
        brain.write(line)
        brain.close()

    # fix html file showing contexts and tags used
    fix_htmls()

    # re-train model and restart server
    import learn
    restart_program()


def add_post_intent(data):
    """
    Aggiunge un nuovo intento complesso al bot

    :param data: il file .json contenente le informazioni
    """
    import ast
    print(f'data is: {data}')
    url = data[data.find('url=')+4:data.find('&tag=')]
    tag = data[data.find('tag=')+4:data.find('&patterns=')]
    tag = tag.lower()
    patterns = data[data.find('patterns=')+9:data.find('&responses=')]
    responses = data[data.find('responses=')+10:data.find('&context_set=')]
    if 'context_filter' in data:
        context_set = data[data.find('context_set=')+12:data.find('&context_filter=')]
        context_filter = data[data.find('context_filter=')+15:data.find('&metadata=')]
    else:
        context_set = data[data.find('context_set=')+12:data.find('&metadata=')]
        context_filter = None
    metadata = data[data.find('&metadata=')+10:]
    context_set = context_set.lower()
    print(f"\nurl is {url}")
    print(f"\ntag is {tag}")
    print(f"\npatterns is {patterns}")
    print(f"\nresponses is {responses}")
    print(f"\ncontext_set is {context_set}")
    print(f"\ncontext_filter is {context_filter}")
    print(f"\nmetadata is {metadata}")

    # convert the string representation of list into actual list
    patterns = ast.literal_eval(patterns)
    responses = ast.literal_eval(responses)
    metadata = ast.literal_eval(metadata)

    # negli intent in json il contesto principale corrisponde al contesto
    # vuoto, mentre in rivescript deve essere specificato che è 'random'
    context_set_json = context_set
    if 'random' in context_set:
        context_set_json = ""
        
    # add intents to json
    with open('assets/intents.json', 'r', encoding='utf-8') as json_data:
        intents = json.load(json_data)

    if context_filter is not None:
        intents['intents'].append({
            "tag": tag,
            "patterns": patterns,
            "responses": ['<msg>' + response + '</msg>' for response in responses],
            "context_set": context_set_json,
            "context_filter": context_filter,
            "metadata:": metadata,
            "url": url
        })
    else:
         intents['intents'].append({
            "tag": tag,
            "patterns": patterns,
            "responses": ['<msg>' + response + '</msg>' for response in responses],
            "context_set": context_set_json,
            "metadata": metadata,
            "url": url
        })

    with open('assets/intents.json', 'w', encoding='utf-8') as json_data:
        json.dump(intents, json_data, indent=2)

    brain = open('brain/conversation.rive','a+',encoding='utf-8')
    if context_set:
        brain.write(f'\n\n+ {tag.lower()}')
        for response in responses:
            brain.write('\n- '+response+'<call>set_metadata '+tag.lower()+'</call>{topic='+context_set+'}')
    else:
        brain.write(f'\n\n+ {tag.lower()}')
        for response in responses:
            brain.write(f'\n- {response}<call>set_metadata {tag.lower()}</call>')
    line = "\n\n"
    for pattern in patterns:
        line = ''.join(line) + f'\n+ [*] {tools.clean_word(pattern.lower())} [*]\n@ {tag.lower()}\n'
    brain.write(line)
    line = f'\n\n> topic {context_set} includes exit_topic_post\n\n+ *\n- <call>post_request <star></call>'+'{topic=random}'+'\n\n< topic'
    brain.write(line)
    brain.close()

    fix_htmls()

    # re-train model and restart server
    import learn
    restart_program()


def restart_program():
    """
    Riavvia il server
    """
    import psutil
    import sys
    import os
    try:
        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logging.error(e)
    

    python = sys.executable
    os.execl(python, python, "\"{}\"".format(sys.argv[0]))

def send_intent_response(sentence,intent,action=''):
    '''
    Invia la risposta al bot

    :param str sentence: la frase inviata 

    :param str[] intent: il dizionario contenente gli intenti

    :param str action: il tipo di azione da intraprendere

    :type action: str or None

    '''

    from rivescript_interpreter import get_reply
    
    #words_not_in_bag = not_in_bag(sentence,words)
    #print(f"WORDS NOT IN BAG ARE {words_not_in_bag}")

    #message = ' ' + ' '.join(words_not_in_bag)
    #responseTxtElement=get_reply(intent['tag'] + message)
    responseTxtElement=get_reply(intent['tag'])
    #print(f"final message: {intent['tag'] + message}")
    attToUser=""
    attTxt=re.search('<att>(.*)</att>', responseTxtElement)
    if attTxt is not None:
        attToUser=attTxt[0].replace('<att>','')
        attToUser=attToUser.replace('</att>','')
    data = {}
    data['message'] = responseTxtElement
    data['attachment'] = attToUser

   
    jsonData = json.dumps(data)
    return jsonData



def send_direct_response(sentence):
    """
    Invia direttamente una risposta all'utente

    :param sentence: la frase inserita dall'utente
    """
    from rivescript_interpreter import get_reply
    
    data = {}
    data['message'] = sentence
   
    jsonData = json.dumps(data)
    return jsonData

def reply_to_user(sentence,user):
    """
    Cerca una risposta da dare all'utente

    :param sentence: la frase inserita dall'utente
    :param user    : l'utente a cui rispondere
    """
    reply = rs.check_command(sentence,user)
    print(f"input message is {sentence}")
    if reply:
        return reply        
    else:
        #print("sentence is NOT spelled correctly")
        # prova ad aggiustare lo spelling
        best_sentence = spell.get_best_sentence(sentence)
        print(f"best sentence is {best_sentence}")
        reply = rs.check_command(best_sentence,user)
        if reply:
            # rispondi all'utente
            return reply
            
        else:
            possible_sentences = spell.correct_sentences(sentence)
            for possible_sentence in possible_sentences:
                possible_sentence = ' '.join(list(possible_sentence))
                print(f"possible sentence is: {possible_sentence}")
                reply = rs.check_command(possible_sentence,user)
                print(f"-Tried: {possible_sentence}\n-Result: {reply}\n\n")
                if reply:
                    # rispondi all'utente
                    return reply
                #else:
                    # controlla gli intent
                    #return False
            return False
                    


def response(sentence, userID='123', show_details=True):
    """
    Usa la rete neurale creata in precedenza per trovare una risposta
    al messaggio inviato dall'utente

    :param sentence    : la frase inserita dall'utente
    :param userID      : l'utente a cui inviare il messaggio (Non utilizzato)
    :param show_details: parametro di debug
    """
    candidate_reply = reply_to_user(sentence, userID)
    print(f"input message is {sentence}")
    if candidate_reply != False:
        #print(f"bot reply: {reply_to_user(sentence)}")
        print(f"candidate reply is {candidate_reply}")
        return send_direct_response(candidate_reply)
    else:
        results = classify(sentence)
        # if we have a classification then find the matching intent tag
        print ("Results: ",results)
        
        
        if results:
            # loop as long as there are matches to process
            print ('Looping results...')
            for r in results:
                print ('Check result:',r)
                for i in intents['intents']:

                    # find a tag matching the first result
                    if i['tag'] == r[0]:
                        print("Intent selected: ",i)

                        if show_details and 'context_filter' in i:
                            print ('context_filter:', i['context_filter'])
                        else:
                            print ('context_filter:')

                        if 'context_set' in i:
                            if show_details: print ('context:', i['context_set'])
                        # set context for this intent if necessary
                        '''if 'context_set' in i:
                            if show_details: print ('context:', i['context_set'])
                            context[userID] = i['context_set']

                            print("Intent selected: ",i)'''
                        # check if this intent is contextual and applies to this user's conversation
                        if not 'context_filter' in i or \
                            (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                            
                            context[userID] = i['context_set']

                            if show_details: print ('tag:', i['tag'])

                            # DEBUG
                            for word in i:
                                print(f"\nelement: {word}")

        
                            return send_intent_response(sentence,i)
                        else:
                            print ("!!! Sentence not in right context")
                            
                results.pop(0)

            # fuori contesto?
            print ("Sentence not in right context or not found")
            data = {}
            # messagetoUser="Sorry, I didn't get."
            messagetoUser=rs.get_reply(sentence)
            data['message'] = messagetoUser
            data['attachment'] = ''
            jsonData = json.dumps(data)

            return jsonData
        else:
            
            data = {}
            # messagetoUser="Sorry, I didn't get. Please specify more words."
            messagetoUser=rs.get_reply(sentence)
            data['message'] = messagetoUser
            jsonData = json.dumps(data)
            return jsonData
          

@app.route('/backend', methods = ['POST', 'GET', 'OPTIONS'])
@cross_origin(origin='*')
def handle_request():
    param = ""
    dictionary = request.form
    for key, value in dictionary.items():
        param += key + '=' + value + '&'
    param = param[:-1]

    body = param

    if 'msg=' in body:  
        body=body.replace('msg=','')
        return response(body,request.remote_addr)

    elif 'url=' in body:
        db.insert_db()
        add_post_intent(body) 
    elif 'tag=' in body:
        db.insert_db()
        add_intent(body)

    elif 'config=true' in body:
        return db.get_string_backups()
    elif 'config=false' in body:
        restore_config(body)

    elif 'old_password=' in body:
        return tools.change_password(body)

    elif 'password=' in body:
        return tools.login_admin(body)
    
    else:
        return 'OK'

@app.route('/')
def index():
    print(f"Base url without port is {request.remote_addr}")
    rs.set_user_var(request.remote_addr, 'id', request.remote_addr)
    CURRENT_USER = request.remote_addr
    return send_file('static/index.html')



if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080)
        
    except RuntimeError as msg:
        exit()





