from spellchecker import SpellChecker


spell = SpellChecker(language=None, local_dictionary='./dictionaries/italian.gz')

def raw_spell():
    """
    Utility per controllare l'ortografia delle parole da riga di comando
    """
    print("To exit, hit return without input!")
    while True:
        sentence = []
        words = input('Input a word to spell check: ')
        if words == '':  
            break
        words = words.lower()
        words = words.split()
        for word in words:
            if word in spell:
                print("'{}' is spelled correctly!".format(word))
                
                sentence.append(word)
            else:
                cor = spell.correction(word)
                print("The best spelling for '{}' is '{}'".format(word, cor))
                sentence.append(cor)
                print("If that is not enough; here are all possible candidate words:")
                print(spell.candidates(word))
        print(f"\n The sentence entered is {' '.join(sentence)}")

def is_spelled_correctly(sentence):
    """
    Controlla se la frase in input è scritta correttamente

    :param sentence: la frase da controllare
    """
    import string
    sentence = ' '.join(sentence).lower()
    for c in string.punctuation:
        sentence = sentence.replace(c,'')
    sentence = sentence.split()
    for word in sentence:
        if word not in spell:
            return False
    return True

def correct_sentences(sentence):
    """
    Restituisce le frasi con tutte le possibili correzioni

    :param sentence: la frase da analizzare e correggere
    """
    words = sentence.lower().split()
    word_group = [[] for i in range(len(words))]
    
    for i in range(len(words)):
        word_list = [words[i]]
        word_list.extend(list(spell.candidates(words[i])))
        word_group[i] = word_list

    import itertools
    possible_sentences = itertools.product(*word_group)
    possible_sentences = list(possible_sentences)
    return possible_sentences

def get_best_sentence(words):
    """
    Recupera la frase che ha la probabilità più alta di essere
    corretta
    """
    sentence = []
    words = words.lower().split()
    for word in words:
        if word in spell:
            sentence.append(word)
        else:
            cor = spell.correction(word)
            sentence.append(cor)
    return ' '.join(sentence)


   



