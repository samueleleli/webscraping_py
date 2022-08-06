# CONFIGURATION FILE

# INPUT DATASET

dataset_input_path = "dataset_input/input.csv"
dataset_input_separator = ";"
dataset_input_encoding = 'UTF8'

pos_NAME = 0  # Position of field Name in csv file
pos_URL = 10  # Position of field URL in csv file
pos_ID = 2  # Position of field ID in csv file

# TIME DELAY

SLEEP_TIME = 2

# OUTPUT DATASET FILE

dataset_output_path = "results/output.csv"
dataset_output_separator = ";"
dataset_output_encoding = 'UTF8'

# OUTPUT CSV FILE HEADER

header = ['NOME', 'LINK', 'ID', 'LINK_IS_VALID', 'MATCHING', 'SCORE', 'WORDS_FOUND']

# KEYWORDS TO FIND IN WEBPAGE - ONLY LOWERCASE

keywords = ['directions', 'abyss', 'seal', 'seamstress', 'drinking', 'feeding', 'bunch', 'tulip', 'lemon',
            'proverb']

# HTTP REQUEST HEADER

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36 '
}
