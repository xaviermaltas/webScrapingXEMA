## Pràctica 1: Webscraping

##### Som el Xavier Maltas i la Mónica Ortiz i farem la pràctica 1 de webscrapping conjuntament. Deixem una breu explicació de la nostra pràctica.


#### Descripció: 
###### Hem escollit la web del llistat d'estacions meteorològiques automàtiques de Catalunya: https://www.meteo.cat/observacions/llistat-xema, (XEMA) perquè ens ha semblat que conté dades molt interessants per fer el projecte i a més, hem trobat que el llenguatge de marques està bastant bé estructurat, cosa que ajuda alhora de fer scraping. 

###### El llenguatge que hem utilitzat per fer l'scraping ha sigut Python, concretament la versió 3.8, pensem que és bastant adequat per aquesta feina, el més idoni per extreure dades del web, per les seves llibreries dedicades a aquesta feina. 
###### Per tant, les llibreries utilitzades han sigut les següents:
- BeautifulSoup4
- Pandas
- requests
- Sys
- Time
- csv
- path


#### Procediment:
###### Per extreure el data, primer hem anat definint funcions, tant per extreure els 'headers' que són les capçaleres del dataset com per anant exportant el 'body' amb tots els registres de les estacions meteorològiques. 

#### Enllaç del ZENODO del dataset generat
