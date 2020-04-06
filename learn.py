import sys
import logging
import logging.config
logging.config.fileConfig('logging.conf')
logging.getLogger('chatbot')
    
import nltk
logging.info('nltk [imported]')

from nltk.stem.snowball import ItalianStemmer
stemmer = ItalianStemmer()
logging.info('ItalianStemmer [imported]')

# import our chat-bot intents file
import json
with open('assets/intents.json',encoding='utf-8') as json_data:
    intents = json.load(json_data)
logging.info('intents [loaded]')



words = []
classes = []
documents = []
ignore_words = ['?',',','.']
# loop through each sentence in our intents patterns
logging.info('Loop on intents...')
for intent in intents['intents']:
    for pattern in intent['patterns']:
        logging.debug('Evaluate pattern: ' + pattern)
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        print('Tokenize words:',w)
        # add to our words list
        words.extend(w)
        print('words array extended:',words)
        # add to documents in our corpus
        documents.append((w, intent['tag']))
        
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])



# stem and lower each word and remove duplicates
print('documents array extended:',documents)
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))

print()
print (len(documents), "documents",documents)
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)

# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)


# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0] #[0]=sentence,[1]=tag
    print(pattern_words)

    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle our features and turn into np.array
import random
import numpy as np
random.shuffle(training)
training = np.array(training)

# create train and test lists
train_x = list(training[:,0]) #Bag of words 
train_y = list(training[:,1]) #Tags

# things we need for Tensorflow

import tflearn
import tensorflow as tf
import pickle
print('Lib for Tensorflow imported')

# reset underlying graph data
tf.compat.v1.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')

net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_verbose=3)
# Start training (apply gradient descent algorithm)
model.fit(train_x, train_y, n_epoch=300, batch_size=8, show_metric=True)



model.save('tf_model/model.tflearn')

pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "tf_model/training_data", "wb" ) )

