#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote
import ssl

cache = {}

def getJSON(page):
    params = urlencode({
      'format': 'json',
      'action': 'parse',
      'prop': 'text',
      'redirects': True,
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"
    # désactivation de la vérification SSL pour contourner un problème sur le
    # serveur d'évaluation -- ne pas modifier
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))

    # If page exist recover data from JSON file
    try:
        title = parsed['parse']['title']
        content = parsed['parse']['text']['*']
        return title, content

     # If page don't exist return None title and content
    except KeyError:
        return None, None


def getPage(page):

    global cache

    # Try to recover title and links from cache
    try:
        title = cache[page]['title']
        links = cache[page]['links']

    # If data are not already in cache, ask Wikipedia API
    except:

        title, content = getRawPage(page)

        # If page don't exist return None title and empty links
        if title is None and content is None:
            links = []

        # If page exist recover data by searching in the content
        else:
            soup = BeautifulSoup(content, 'html.parser')
            links = []

            for div_tag in soup.find_all('div'):
                for p_tag in div_tag.find_all('p'):
                    for a_tag in p_tag.find_all('a'):
                        if a_tag.get('href') is not None and not a_tag.get('href').endswith("redlink=1") and a_tag.get('href').startswith("/wiki"):
                            link = a_tag.get('href') + "#"
                            link = link.replace("_", " ")
                            link = unquote(link[len("/wiki/"):link.index("#")])
                            if len(link) != 0 and ":" not in link:
                                links.append(link)
            links = sorted(set(links), key=links.index)[:min(10,len(links))]

        # Add page to the cache variable
        cache[page] = {'title': title, 'links': links}   

    return title, links


if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    print("Ça fonctionne !")
    
    # Voici des idées pour tester vos fonctions :
    # print(getJSON("Utilisateur:A3nm/INF344"))

    # print(getRawPage("Utilisateur:A3nm/INF344"))
    # print(getPage("Socrate"))

    print(getPage("Réussite"))
    # print(getPage("Fondo Strategico Italiano"))

