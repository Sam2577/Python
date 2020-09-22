from bs4 import BeautifulSoup
import requests
import time
import os
import random

ALL_CONTENT = dict()
ALL_LINKS = []

def get_url(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1 : end_quote]
    if url.startswith('/'):
        return 'http://en.wikipedia.org' + url
    return url

def get_page(CURL):
    global ALL_CONTENT
    global ALL_LINKS
    r = requests.get(CURL)
    soup = BeautifulSoup(r.content)
    page_title = soup.h1.text
    randnum = random.randint(1,100000)
    try:
        f = open('%s.txt' % page_title, 'w+')
    except:
        f = open('%s.txt' % randnum, 'w+')
    f.write('\n' + str(page_title).upper() + '\n')
    
    print(page_title) 
    ptags = soup.select('div[id="bodyContent"] p')
    atags = soup.select('div[id="bodyContent"] a[href]')
    for a in atags[:60]:
        str_link = str(get_url(str(a)))
        if a != None and str_link.startswith('http://') and str_link not in ALL_LINKS:
            ALL_LINKS.insert(0, str_link)

    content_string = ""
    for p in ptags:
        content_string += p.text + '\n'
        try:
            f.write(p.text + '\n')
        except:
            print('--ERROR WRITING PTAG TO FILE--')

    f.close()         
    ALL_CONTENT[page_title] = content_string

def main(num_pages_to_get):
    #os.makedirs('Wiki-python', exist_ok=True)
    URL = 'http://en.wikipedia.org/wiki/Python_(programming_language)'
    while num_pages_to_get > 0:
        get_page(URL)
        URL = ALL_LINKS.pop()
        print('LEN OF ALL LINKS:', len(ALL_LINKS))
        print('NUM PAGES TO GET:', num_pages_to_get)
        num_pages_to_get -= 1
        time.sleep(2)

if __name__ == '__main__':
    main(10)     


