#!/usr/bin/env python
# coding: utf-8

# In[4]:


class Tank:
    def __init__(self, name):
        self.alias = None
        self.wikientry = None
        self.name = name
        self.type = None
        self.country = None
        self.chapters = {}

    def __repr__(self):
        return "Name: {}\nType: {}\nCountry of Origin: {}\n".format(self.name, self.type, self.country)

    def list_of_content(self):
        text = ''
        data = [self.name]
        for key in self.chapters:
            data.append('    ' + key)
        for i in data:
            text += i 
            text += '\n'
        return text
    
    def show_all(self):
        """ show all tank info
            return string
        """
        text = str(self)
#         print(self)
        for key, _data in self.chapters.items():
            text += '    ' + key + ': '
            c = _data.splitlines()
            for k in c:
                k.strip()
            if '' in c:
                c.pop(c.index(''))
            for k in c:
                text += k + '\n'
        text += '\n'
        return text


# In[3]:


def tank_factory(infoboxes, link_end):
    tanks = []
    for infobox in infoboxes:
        chaps = []
        tank = Tank(str(next(iter(infobox))).strip())
        print(tank.name)
        tank.wikientry = link_end
        if 'Place of origin' in infobox:
            tank.country = infobox['Place of origin']
        tank.type = infobox['Type']
        # return tank
        for key, data in infobox.items():
            if data is None:
                if key == 'Service history':
                    print(key + ' found')
                elif key == 'Production history':
                    print(key + ' found')
                elif key[:14] == 'Specifications':
                    print(key + ' found')
            else:
                tank.chapters[key] = data
        print('')
        tanks.append(tank)
    return tanks

