from bs4 import BeautifulSoup as Bs
from urllib.request import urlopen
from urllib.error import URLError
from tkinter import messagebox
import re


def scrapper(query):
    """
    :parameter str query: end of url to search
    :rtype: list of dict
    """
    query = query
    infoboxes = []
    url = 'https://en.wikipedia.org/wiki/'+query
    try:
        raw = urlopen(url)
        print('{} opened successfully'.format(url))
        soup = Bs(raw, features='lxml')
        boxes = soup.find_all('table', {'class': 'infobox vcard'})
        for table in boxes:
            content_dict = dict()
            for br in soup.find_all('br'):
                br.replace_with('\n')
            for tr in table.find_all('tr'):
                if len(tr.contents) > 1:
                    content_dict[string_clean(tr.contents[0].text, True)] = string_clean(tr.contents[1].text)
                elif tr.text:
                    content_dict[string_clean(tr.text, True)] = None
            infoboxes.append(content_dict)

        return infoboxes
    except URLError as error:
        if str(error.reason) == '[Errno 11001] getaddrinfo failed':
            messagebox.showerror('URLError', message='No connection to internet.\nProbably...')
        else:
            print('|{}|'.format(error.reason))
            messagebox.showerror('URLError', message=error.reason)


def string_clean(string, title=False):
    if not title:
        if '\n' in string:
            t = string.splitlines()
            while '' in t:
                t.pop(t.index(''))
            t2 = ''

            for i in range(len(t)-1):
                t2 += t[i]
                t2 += '\n                    '
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
