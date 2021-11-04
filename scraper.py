import os
import requests
import csv
from bs4 import BeautifulSoup

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
    metricsList = ['Temperatura mitjana', 'Temperatura màxima', 'Temperatura mínima', 'Humitat relativa mitjana', 'Precipitiació acumulada']
    headers = []
    for html_header in html_header:
        headers += [html_header.text]
    headers = getCodeInBrackets(headers)
    for i in metricsList:
        headers.append(i)
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
        single_data += [str(param.text)]
    removeNewLineCharacters(single_data)
    removeEmptyElements(single_data)
    single_data = replaceCommaByDot(single_data)
    single_data = getCodeInBrackets(single_data)
    single_data = checkOperativeStations(single_data)
    link = getXEMAlinks(row)
    RDtable = getRDTableHTML(link)
    RDinfo = getRDTableInfo(RDtable)
    if(RDinfo != None):
        for i in RDinfo[:5]:
            single_data.append(i.strip())
    return (single_data)

def getBodyTable(html_body):
    body = []
    for row in html_body:
        clean_row = getSingleTableBody(row)
        body.append(clean_row)
    return (body)

#SPECIFIC TABLE
def getXEMAlinks(html_table):
    link = ''
    for l in html_table.select('a'):
        link = (l.get('href'))
    return link

def getRDTableHTML(href):
    if(href != ''):
        link = 'https://www.meteo.cat/' + href
        html = getHTML(link)
        soup = parseHTML(html) 
        table = soup.find_all("div", {"class": "table"})
        return table
    else:
        return None

def getRDTableInfo(html_table):
    if(html_table != None):
        tdList = []
        for tr in html_table[0].select('tr'):
            tdList.append((tr.select('td')[0]).text)
        return tdList
    else:
        return None
        
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

def removeNewLineCarriageReturn(list):
    while '\r\n' in list:
        list.remove('\r\n')
    return list

# (src: https://www.tutorialspoint.com/python3/string_split.htm)
def replaceCommaByDot(list):
    newList = []
    for i in list:
        ni = i.replace(',','.')    
        newList.append(ni)
    return newList

def getCodeInBrackets(list):
    newList = []
    name = ''
    codi = ''
    for i in list:
        if (i.find('[')!=-1):
            split = i.split(' [',1)
            name = split[0]
            split = (split[1]).split(']',1)
            codi = split[0]
            list.remove(i)
    newList.append(name)
    newList.append(codi)
    for i in list:
        newList.append(i)

    return newList

def checkOperativeStations(list):
    newList = []
    for i in list: 
        if ((i.find('Operativa'))!=-1):
            newList.append(None)
            newList.append('Operativa')
        else:
            newList.append(i)  
    return newList

def write2CSV(filePath, headers, body):
    print("Writting " + str(len(body)) + " rows to CSV file!")
    with open(filePath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(headers)
        for row in body:
            writer.writerow(row)
    csvFile.close()
    print("CSV file created successfully!")

main(url, fileName)