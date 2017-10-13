from bs4 import BeautifulSoup
import requests
import os
import io
import re
import md5

file_list = {}
cwd = os.path.dirname(os.path.realpath(__file__))
url = "https://ar.wikipedia.org/wiki/Special:Random"

def build_file_list():
    current_files = os.listdir(cwd)
    for file in current_files:
        file_list[str(file).replace('.txt', '')] = 1

def _get_HTML_file():
    HTML_file = requests.get(url)
    return HTML_file

def _soup_the_file(HTML_file):
    soup = BeautifulSoup(HTML_file.text, 'html.parser')
    soup = soup.find_all('p')
    doc = ""
    for thing in soup:
        doc = doc + thing.get_text()
    return doc

def _get_stripped_text(text):
    text = re.sub(ur'[^\u0600-\u06FF]', " ", text)
    return text

def _hashed_file(text):
    m = md5.new()
    m.update(text.encode('utf-8'))
    hashed_text = m.hexdigest()
    if hashed_text not in file_list:
        file_list[hashed_text] = 1
        return hashed_text
    else:
        return None
  
def write_article_to_file():
    HTML_file = _get_HTML_file()
    unclean_text = _soup_the_file(HTML_file)
    text = _get_stripped_text(unclean_text)
    hashed_text = _hashed_file(text)
    if hashed_text is not None:
        with io.open(hashed_text + ".txt", "w", encoding='utf-8') as txt_file:
            txt_file.write(unicode(text))
        return True
    else:
        print ("Article already scraped")
        return False

def get_article(no_dup=False):
    HTML_file = _get_HTML_file()
    unclean_text = _soup_the_file(HTML_file)
    text = _get_stripped_text(unclean_text)
    if no_dup:
        hashed_text = _hashed_file(text)
        if hashed_text is not None:
            return unicode(text)
        else:
            get_article(no_dup=True)
    else:
        return text
