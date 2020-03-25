#!/usr/bin/env python
# coding: utf-8

# In[1]:
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import re


def scrapper(query):
    query = query
    infoboxes = []
    url = 'https://en.wikipedia.org/wiki/'+query
    raw = urlopen(url)
    print('{} opened succesfully'.format(url))
    soup = bs(raw,features="lxml")
    boxes = soup.find_all('table', {'class': 'infobox vcard'})
    for table in boxes:
        content_dict = dict()
        for br in soup.find_all("br"):
            br.replace_with("\n")
        for tr in table.find_all('tr'):
            if len(tr.contents) > 1: 
                content_dict[string_clean(tr.contents[0].text, True)] = string_clean(tr.contents[1].text)
            elif tr.text:
                content_dict[string_clean(tr.text, True)] = None
        infoboxes.append(content_dict)
    return infoboxes


# In[ ]:


def string_clean(string, title=False):
    if not title:
        # print(string)
        if '\n' in string:
            t = string.splitlines()
            while '' in t:
                t.pop(t.index(''))
            t2 = ''
            # print(t)
            for i in range(len(t)-1):
                t2 += t[i]
                t2 += '\n    ----    ----    '
            t2 += t[-1]
            string = t2
    else:
        if '\n' in string:
            t = string.splitlines()
            while '' in t:
                t.pop(t.index(''))
            t2 = ''
            for i in t:
                t2 += i
                t2 += ' '
            string = t2
    s = string.strip()
    s = s.replace('\xa0', ' ')
    s = re.sub('\[.\]','' ,s)
#     s = s.replace('\n', '   ||   ')
    # print(s)

    return s

