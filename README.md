# webscraping_py
Progetto Python con lo scopo di fare web scraping su una lista di siti contenuta in un file csv. Nello specifico lo script permette di cercare parole chiave o frasi all'interno del sito. 

I risultati della ricerca sono salvati su un file csv separato.

Il file `config.py` permette di configurare:
 - i path, i separatori e la codifica dei caratteri dei dataset di input e di output;
 - gli indici relativi alle colonne da prelevare dal CSV di input;
 - l'intestazione del file di output
 - le parole chiave da cercare nella pagina web
- l'header della richiesta http

N.B. Il cambiamento del numero di colonne del file di output comporta delle piccole modifiche all'interno del file `script_webscraping.py`, in particolare delle variabili `data_error` e `data_OK` e dalla riga 84 a 87.
