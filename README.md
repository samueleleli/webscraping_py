# webscraping_py
Python project with the purpose of web scraping a list of sites contained in a csv file. Specifically, the script allows searching for keywords or phrases within the site. 

The search results are saved to a separate csv file.

The `config.py` file allows you to configure:
 - the paths, separators and character encoding of the input and output datasets;
 - the indexes related to the columns to be taken from the input CSV;
 - the header of the output file
 - the keywords to be searched in the web page
- the header of the http request
- the delay between requests

## Startup
Run the following command to install the libraries:
```bash
pip install -r requirements.txt
```
Stand in the project root and run the following command to begin URL parsing:
```bash
python script_webscraping.py
```

N.B. Changing the number of columns in the output file involves minor changes within the `script_webscraping.py` file, particularly of the variables `data_error` and `data_OK` and from line 80 to 82.