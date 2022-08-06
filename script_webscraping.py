#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Samuele Leli
@File: script_webscraping.py
@Time: 2022/05/29 02:37 PM
"""

# Python script that allows webscraping given a dataset containing URLs
# by finding a set of words in the web page.
# The results of the search are saved in a dedicated dataset.

# The configuration file is 'config.py'

from bs4 import BeautifulSoup
import csv
import requests
from urllib.parse import urlparse
from urllib.parse import urlsplit
import validators
import time
import re
import config
import utils_text


# method for building URL

def build_link(url, domain_url):
    link_to_build = ""
    u = urlparse(url)

    if u.scheme == "":
        link_to_build += "http://"

    link_to_build = link_to_build + domain_url
    link_to_build = link_to_build.replace("https", "http").strip()
    link_to_build = re.sub(r"\s+", "", link_to_build)
    link_to_build = link_to_build.replace("\\", "")

    if link_to_build[len(link_to_build) - 1] == ".":
        link_to_build = link_to_build[:-1]
    return link_to_build


n_url_not_inserted = 0  # Counter of the number of rows which have no link.
n_url_wrong = 0  # Counter of the number of rows which have wrong or bad formatted link.
n_url_valid = 0  # Counter of the number of rows which have a valid link.
n_items = 0  # Counter of the number of rows.
matching_keyword = 0  # Counter of the number of websites which have at least one word from the keywords list.

# Informative messages

print('\nConfiguration file: config.py')
print('\nPATH TEST DATASET: ', config.dataset_input_path)
print('PATH DATASET SAVING: ', config.dataset_output_path)

time.sleep(config.SLEEP_TIME)

print('\nSTARTING ANALYSIS.... \n')

# parsing input dataset
try:
    with open(config.dataset_output_path, 'w', encoding=config.dataset_input_encoding, newline='') as f:
        writer = csv.writer(f, delimiter=config.dataset_output_separator)
        writer.writerow(config.header)

        with open(config.dataset_input_path, 'r', newline='', encoding=config.dataset_output_encoding,
                  errors='ignore') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=config.dataset_input_separator)
            line_count = 0
            for row in csv_reader:
                line_count += 1
                if line_count == 1:
                    continue
                else:
                    n_items += 1
                    print("parsing element " + str(line_count - 1))

                    name = row[config.pos_NAME]  # get name field
                    link = row[config.pos_URL]  # get website URL field
                    id_row = row[config.pos_ID]  # get id field

                    # ROW INSERTED IF URL IS NOT VALID

                    data_error = [name, link, id_row, 'NO', 'NO', '0', '0']

                    # Analysis and building URL

                    r1 = urlsplit(link)
                    domain = r1.geturl()

                    if domain == "":
                        # missing url
                        n_url_not_inserted += 1
                        writer.writerow(data_error)
                        continue

                    link = build_link(link, domain)

                    if not validators.url(link):
                        # not valid URL
                        n_url_wrong += 1
                        writer.writerow(data_error)
                        continue

                    # Webpage download

                    try:
                        r = requests.get(link, allow_redirects=True, headers=config.headers)
                    except:
                        # Error during webpage downloading
                        n_url_wrong += 1
                        writer.writerow(data_error)
                        print("Can't download webpage")
                        continue

                    # The link is valid here!

                    n_url_valid += 1

                    # Get only text from HTML, cleaning and lowercase

                    soup = BeautifulSoup(r.content, features="html.parser")
                    html_clean = utils_text.clean_text(soup)

                    # Find words
                    (words_list, score) = utils_text.find_word(html_clean)

                    # Intermediate results printing
                    print(name, score)

                    # saving data in CSV file
                    # data_OK is the row that writes on success

                    if score > 0:
                        # MATCHING
                        matching_keyword += 1
                        data_OK = [name, link, id_row, 'YES', 'YES', score, words_list]
                    else:
                        # URL VALID BUT NO MATCHING
                        data_OK = [name, link, id_row, 'YES', 'NO', 0, 0]

                    writer.writerow(data_OK)

                    # Wait 5 seconds
                    time.sleep(config.SLEEP_TIME)
except FileNotFoundError:
    print("ERROR: Input dataset not found! Please check 'config.py' file")
    exit()

if n_items == 0 or n_url_valid == 0:
    print("\nError: EMPTY LIST OR NO VALID URL")
    exit()

# LINK ANALYSIS

print("\nLINK ANALYSIS:\n")
print("TOTAL ITEMS: ", n_items)
print("VALID LINKS: ", n_url_valid, '-', (n_url_valid / n_items) * 100, "%")
print("NOT INSERTED LINKS: ", n_url_not_inserted, '-', (n_url_not_inserted / n_items) * 100, "%")
print("NOT VALID LINKS: ", n_url_wrong, '-', (n_url_wrong / n_items) * 100, "%")

# RESULTS ANALYSIS

print("\nRESULTS ANALYSIS:\n")
print("TOTAL EVALUATED ITEMS: ", n_url_valid)
print("ELEMENTS THAT HAD AT LEAST ONE MATCH: ", matching_keyword, '-', (matching_keyword / n_url_valid) * 100, "%")
