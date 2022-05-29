#file di utilità per trovare le parole e pulire il testo

import re
import config

def is_phrase_in(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None

def clean_text(soup):
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text.lower()

def find_word(html_clean):
    score = 0
    words_list = ""
                
    #per ogni parola calcolo il numero di occorrenze nella pagina html

    for word in config.keywords :
        if  is_phrase_in(word, html_clean):
            words_list += word + ", "
            score += 1

    words_list = words_list[:-2]

    score = score/len(config.keywords)

    return words_list,score