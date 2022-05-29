#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Samuele Leli
@File: script_webscraping.py
@Time: 2022/05/29 02:37 PM
"""

# Script python che permette di fare webscraping dato un dataset contenente degli URL
# trovando un set di parole nella pagina web. 
# Vengono salvati in un dataset apposito i risultati della ricerca

# il file di configurazione dei dataset è 'config.py' 

from bs4 import BeautifulSoup
import csv  
import requests
from urllib.parse import urlparse
from urllib.parse import urlsplit
import validators
import time
import re

#import config and utils_text file

import config
import utils_text

n_url_non_inseriti = 0          #contatore del numero di elementi che non hanno inserito link
n_url_errati = 0                #contatore del numero di elementi che hanno inserito il link sbagliato o mal scritto
n_url_validi = 0                #contatore del numero di elementi che hanno inserito il link correttamente
n_elementi = 0                  #contatore del numero di elementi totale
matching_keyword = 0            #contatore del numero di elementi che avevano almeno una parola dell'elenco keywords
                                #nel loro sito web

#messaggi informativi

print('\nFile di configurazione: config.py')

print('\nPATH DATASET DI TEST: ', config.dataset_input_path)
print('PATH DATASET DI SALVATAGGIO: ', config.dataset_output_path)

time.sleep(5)

print('\nINIZIO ANALISI .... \n')

#metodo che permette di costruire l'URL

def build_link(link,dominio):
    u = urlparse(link)
    link = ""
                
    if u.scheme == "":
        link += "http://"
                
    link = link + dominio
    link = link.replace("https","http").strip()
    link = re.sub(r"\s+","",link)
    link = link.replace("\\","")

    if link[len(link)-1] == ".":
        link = link[:-1]
    return link

#scorrimento del dataset

with open(config.dataset_output_path, 'w', encoding=config.dataset_input_encoding, newline='') as f:
    
    writer = csv.writer(f, delimiter=config.dataset_output_separator)

    writer.writerow(config.header)

    with open(config.dataset_input_path,'r', newline='',encoding=config.dataset_output_encoding,errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=config.dataset_input_separator)
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count == 1:
                continue
            else:
                n_elementi+=1
                print("parsing element "+ str(line_count-1)) 

                nome = row[config.pos_NOME]             #prelevo il campo del nome
                link = row[config.pos_URL]              #prelevo l'URL del sito web
                id = row[config.pos_ID]                 #prelevo l'id

                #in caso l'url non fosse valido inserirà questa row

                data_error = [nome,link,id,'NO','NO','0','0'] 

                #ANALISI E COSTRUZIONE DEL LINK
                
                r1 = urlsplit(link)
                dominio = r1.geturl()
                
                if dominio == "":
                    #url mancante
                    n_url_non_inseriti+=1
                    writer.writerow(data_error)
                    continue
                
                link = build_link(link,dominio)
                
                if not validators.url(link):
                    #url non valido
                    n_url_errati+=1
                    writer.writerow(data_error)
                    continue
                
                #scarico pagina web
                
                try:
                    r = requests.get(link, allow_redirects=True,headers=config.headers)
                except:
                    #errore nello scaricamento della pagina
                    n_url_errati += 1
                    writer.writerow(data_error)
                    print("error")
                    continue
                
                #ARRIVATO QUI SIGNIFICA CHE IL LINK E' VALIDO!!
                
                n_url_validi += 1

                #estraggo solo il testo dalla pagina html pulito e in lower case

                soup = BeautifulSoup(r.content, features="html.parser")
                html_clean =  utils_text.clean_text(soup)

                #trovo parole
                (words_list,score) = utils_text.find_word(html_clean)

                #print dei risultati man mano che si scorrono gli elementi
                print(nome,score)                    

                #salvo i dati nel file csv
                # data_OK è la row che scrive in caso di successo
                                
                if score>0 : 
                    #MATCHING
                    matching_keyword+=1
                    data_OK = [nome,link,id,'YES','YES',score,words_list]
                else:  
                    #URL VALIDO MA NON C'E' STATO MATCHING
                    data_OK = [nome,link,id,'YES','NO',0,0]
                
                writer.writerow(data_OK)

                #aspetto 5 secondi
                time.sleep(5)

#ANALISI LINK

print("\nANALISI DEI LINK:\n")
print("TOTALE: ",n_elementi)
print("LINK VALIDI: ",n_url_validi,'-',(n_url_validi/n_elementi)*100,"%")
print("LINK NON INSERITI: ",n_url_non_inseriti,'-',(n_url_non_inseriti/n_elementi)*100,"%")
print("LINK INSERITI NON VALIDI: ",n_url_errati,'-',(n_url_errati/n_elementi)*100,"%")

#ANALISI RISULTATI

print("\nANALISI DEI RISULTATI:\n")
print("TOTALE ELEMENTI VALUTATI: ",n_url_validi)
print("ELEMENTI CHE HANNO AVUTO ALMENO UN MATCH: ",matching_keyword,'-',(matching_keyword/n_url_validi)*100,"%")