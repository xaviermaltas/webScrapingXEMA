import os
import requests
import sys
import csv
import time
from os import path
from bs4 import BeautifulSoup
from requests.api import head

#global variables
url = 'https://www.meteo.cat/observacions/llistat-xema'
fileName = "XEMA_dataset.csv"

def main(url, fileName):

    #Dataset file creation
    currentDir = os.path.dirname(__file__)
    filePath = os.path.join(currentDir, fileName)
    getXEMAlist(url, filePath)


def getXEMAlist(url,filePath):

    html = getHTML(url) #type class 'str'
    soup = parseHTML(html) #type class 'bs4.BeautifulSoup'
    HTML_table = getHTMLTable(soup) #type class 'bs4.element.Tag'

    html_table_headers = getHTMLTableHeader(HTML_table) #type list of class 'bs4.element.Tag'
    headers = getHeaderData(html_table_headers)
    
    html_table_body = getHTMLTableBody(HTML_table) #type list of class 'bs4.element.Tag'
    body = getBodyTable(html_table_body)

    write2CSV(filePath, headers, body)


def getHTML(url):

    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        print("The scraping failed!")

def parseHTML(html):
    return BeautifulSoup(html, 'html.parser')

def parseHTMLlist(list):
    soupList = []
    for e in list:
        soupElement = parseHTML(e)
        soupList += soupElement

def getHTMLTable(soup):
    return soup.find('table')

# HEADERS
def getHTMLTableHeader(table):
    t_headers = []
    for th in table.select('th'):
        t_headers += [th]
    return t_headers

def getHeaderData(html_header):
    headers = []
    for html_header in html_header:
        headers += [html_header.text]
    return headers

# BODY
def getHTMLTableBody(table):
    t_body = []
    for tr in table.select('tr'):
        if all(t.name == 'td' for t in tr.find_all(recursive=False)):
            t_body += [tr]
    return t_body

def getSingleTableBody(row):
    single_data = []
    for param in row:
        single_data += [param.text]
    removeNewLineCharacters(single_data)
    removeEmptyElements(single_data)
    return (single_data)

def getBodyTable(html_body):
    body = []
    for row in html_body:
        clean_row = getSingleTableBody(row)
        body.append(clean_row)
    return (body)

#UTILS
def printList(l):
    for e in l: 
        print(e)

def removeNewLineCharacters(list):
    while '\n' in list:
        list.remove('\n')
    return list

def removeEmptyElements(list):
    while '' in list:
        list.remove('')
    return list

def write2CSV(filePath, headers, body):
    f = open(filePath, 'w')
    for h in headers:
        f.write(h + ";")
    f.write("\n")
    
    for row in body:
        for i in row:
            f.write(i + ";")
        f.write("\n")
    
    f.close()


main(url, fileName)