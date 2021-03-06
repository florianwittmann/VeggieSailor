#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyveggiesailor.vegguide_cache import VGOCache
import pyveggiesailor.veggiesailor as veggiesailor
from pyveggiesailor.time_tools import parse_hour,parse_hours,modify_hours,get_hours_dict

def adjust_entry(entry):
    """Adjust entry - add missing fields and flat some lists.

    Parameters
    ----------
    entry : dict

    Notes
    -----

    Followed colors are being used:

    #b00257 - very dark red
    #e55e16 - red (bad one)
    #155196 - dark blue
    #fab20a - orange
    #97a509 - greenish yellow
    #16ac48 - light green
    """
    if 'address2' not in entry:
        entry['address2'] = ''
    entry['hours_txt'] = ''
    if 'hours' in entry:
        strhours = []
        for elem in entry['hours']:
            strhours.append(elem['days']+' '+(' , '.join(elem['hours'])))
        entry['hours_txt'] = ('\n').join(strhours)
    else:
        entry['hours'] = []
    entry['hours_parsed'] = get_hours_dict(entry['hours'])
    entry['cuisines_txt'] = ', '.join(entry['cuisines'])
    if 'tags' not in entry:
        entry['tags'] = []
    entry['tags_txt'] = ', '.join(entry['tags'])


    if 'weighted_rating' not in entry:
        entry['weighted_rating'] = '0.0'


    entry['rating_parsed'] = int(round(float(entry['weighted_rating'])))

    if not 'veg_level' in entry:
        entry['veg_level'] = 5

    if int(entry['veg_level']) == 0:
         entry['color_txt'] = '#b00257'
    elif int(entry['veg_level']) == 1:
        entry['color_txt'] = '#97a509'
    elif int(entry['veg_level']) == 2:
        entry['color_txt'] = '#155196'
    elif int(entry['veg_level']) == 3:
        entry['color_txt'] = '#fab20a'
    elif int(entry['veg_level']) == 4:
        entry['color_txt'] = '#97a509'
    elif int(entry['veg_level']) == 5:
        entry['color_txt'] = '#16ac48'
    return entry

def get_entry(uri):
    entry = VGOCache(uri)
    return entry.results

def get_entry_image(uri):
    """Fetch main image for the entry.

    Parameters
    ----------
    uri : str
    """
    entry = get_entry(uri)
    try:
        return entry['images'][0]['files'][1]['uri'].replace('https','http')
    except KeyError:
        return ''


def check_has_regions(seq):
    """Updates list with missing values.

    Parameters
    ----------
    seq : list
    """
    for j in range(len(seq)):
        seq[j]['has_entries'] = 0
        if int(seq[j]['entry_count']) != 0 and int(seq[j]['is_country']) != 1:
            seq[j]['has_entries'] = 1

        if int(seq[j]['entry_count']) != 0 and ('regions' not in seq[j] or 'children' not in seq[j]) :
            seq[j]['has_entries'] = 1
        if 'children' in seq[j]:
            seq[j]['has_children'] = 1
        else:
            seq[j]['has_children'] = 0
    return seq

def get_root():
    """Get root VegGuide regions data tree.
    """
    root = VGOCache('https://www.vegguide.org/')
    return check_has_regions(root.results['regions']['primary'])

def get_children(uri):
    """Get root VegGuide regions data tree.
    """
    children = VGOCache(uri).results['children']
    return check_has_regions(children)

def get_entries(uri):
    """Gets entries after providing url.

    Parameters
    ----------
    uri : str

    """
    if not uri.endswith('/entries'):
        uri += '/entries'
    results = VGOCache(uri).results

    results = [ adjust_entry(x) for x in results ]
    return results

def fav_city_check(uri):
    """Check is place is favorite.
    """
    return veggiesailor.StorageFav().exists(uri)


def fav_place_check(uri):
    """Check is place is favorite.
    """
    return veggiesailor.StorageFav().exists(uri)

def fav_city(uri, data={}):
    """Switch favorite status of the place.
    """
    sv = veggiesailor.StorageFav()
    return sv.switch(uri, 0, data)

def fav_place(uri, data={}):
    """Switch favorite status of the place.
    """
    sv = veggiesailor.StorageFav()
    return sv.switch(uri, 1, data)

def fav_places():
    """Get favorite places.
    """
    sv = veggiesailor.StorageFav()
    results = sv.get_favorites()
    return results

def fav_cities():
    """Get favorite places.
    """
    sv = veggiesailor.StorageFav()
    results = sv.get_favorites(0)
    return results
if __name__ == "__main__":
    from  vegguide import VegGuideObject
    from pprint import PrettyPrinter
    p = PrettyPrinter()
#    get_root()

#    root = VGOCache('https://www.vegguide.org/')
#    print(get_root())
#    europe = VGOCache('https://www.vegguide.org/region/52')
#    spain2 = VGOCache('https://www.vegguide.org/region/66')
#    print(get_children('https://www.vegguide.org/region/53'))
#    print(get_children('https://www.vegguide.org/region/2006'))
    giblartar = VGOCache('https://www.vegguide.org/region/2236')


    bcn = VGOCache('https://www.vegguide.org/entry/14683')
    bar  = VGOCache('https://www.vegguide.org/entry/12300')


    p.pprint(get_entry('http://www.vegguide.org/entry/20647'))
#    print(get_entry_image('http://www.vegguide.org/entry/20647'))

#    print(get_entries('http://www.vegguide.org/region/583'))
#    http://www.vegguide.org/entry/20647
#    for i in (spain2,giblartar, bcn, bar):
#        print(i, i.has_children())
#        print(i, i.has_entries())
#        print(i, i.entries())
#        print(i, i.is_country())
#        print(i, i.is_entry())
#        print(i, i.children())



