#File di configurazione

#DATASET DI INPUT

dataset_input_path = "dataset_input/input.csv" 
dataset_input_separator = ";"
dataset_input_encoding = 'UTF8'

pos_NOME = 0        #index nel file csv del nome
pos_URL = 10        #index nel file csv dell'url
pos_ID = 2          #index nel file csv dell'id

#DATASET DI OUTPUT

dataset_output_path = "risultati/output.csv"
dataset_output_separator = ";"
dataset_output_encoding = 'UTF8'

header = ['NOME','LINK','ID','LINK_VALIDO','MATCHING','SCORE','PAROLE_TROVATE'] #intestazione output

#PAROLE CHIAVE DA CERCARE NELLA PAGINA WEB

keywords = ['indicazioni','abisso','foca','cucitrice','bere','alimentazione','mazzo','tulipano','limone','proverbio']

#HEADER RICHIESTA HTTP

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }