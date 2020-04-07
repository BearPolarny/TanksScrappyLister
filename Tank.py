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
        self.chapters = {"Type": None,
                         "Place of origin": None,
                         "In service": None,
                         "Used by": None,
                         "Wars": None,
                         "Designer": None,
                         "Designed": None,
                         "Manufacturer": None,
                         "Unit cost": None,
                         "Produced": None,
                         "No. built": None,
                         "Mass": None,
                         "Length": None,
                         "Width": None,
                         "Height": None,
                         "Crew": None,
                         "Armor": None,
                         "Main armament": None,
                         "Secondary armament": None,
                         "Engine": None,
                         "Power/weight": None,
                         "Suspension": None,
                         "Ground clearance": None,
                         "Fuel capacity": None,
                         "Operational range": None,
                         "Speed": None}

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
            if _data:
                c = _data.splitlines()
            else:
                c = ["Missing information"]
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
        non_keys = []
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
                if key not in tank.chapters.keys():
                    if key == "Maximum speed":
                        tank.chapters["Speed"] = data
                    elif key == "Armour":
                        tank.chapters["Armor"] = data
                    else:
                        print("{} key not found".format(key))
                        non_keys.append(key)
                tank.chapters[key] = data
        print('')
        tanks.append(tank)
    return tanks, non_keys

