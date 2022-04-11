# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 17:28:12 2022

@author: Nico Mischnick
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class statistik:
    pass

##########bereinigte Liste#################

date_cols = ['Gestartet', 'Beendet',"Monat (MM/JJJJ)"]
meineDaten= pd.read_csv("Alle-ladevorgänge-2022-03-16.csv", sep=";",encoding='latin-1',decimal=",", parse_dates=date_cols)
meineDaten['Ladepunkt'] = meineDaten['Ladepunkt'].replace(['DE*cem*E740796*001'],'Salzgitter 1')
meineDaten['Ladepunkt'] = meineDaten['Ladepunkt'].replace(['DE*cem*E740796*002'],'Salzgitter 2')
meineDaten['Ladepunkt'] = meineDaten['Ladepunkt'].replace(['DE*cem*E740796*003'],'Salzgitter 3')
meineDaten['Ladepunkt'] = meineDaten['Ladepunkt'].replace(['DE*cem*E740796*004'],'Salzgitter 4')

meineDaten['Ladepunkt'] = meineDaten['Ladepunkt'].replace(['DE*cem*E809189*001'],'WF Recht 1')
meineDaten['Ladepunkt'] = meineDaten['Ladepunkt'].replace(['DE*cem*E809189*002'],'WF Recht 2')

meineDaten['Ladepunkt'] = meineDaten['Ladepunkt'].replace(['DE*cem*EMLP1'],'WF Gebäude H 1') #EMLP
meineDaten['Ladepunkt'] = meineDaten['Ladepunkt'].replace(['DE*cem*EMLP2'],'WF Gebäude H 2')

meineDaten['Ladepunkt'] = meineDaten['Ladepunkt'].replace(['DE*cem*ESLP1'],'WF Gebäude H 3') #ESLP2
meineDaten['Ladepunkt'] = meineDaten['Ladepunkt'].replace(['DE*cem*ESLP2'],'WF Gebäude H 4')


####Leere Spalten löschen
meineDaten.drop('Stop-Grund', inplace=True, axis=1)
meineDaten.drop('Grund für die Auffälligkeit', inplace=True, axis=1)
meineDaten.drop('Kosten', inplace=True, axis=1)
meineDaten.drop('Provider', inplace=True, axis=1)
meineDaten.drop('Operator', inplace=True, axis=1)


#print(meineDaten.head())


#print("Anzahl der enthaltenen Datensätze: ", len(meineDaten))
#### Zeitumformen object-datetime
meineDaten['Gestartet'] = pd.to_datetime(meineDaten['Gestartet'])


#print(meineDaten.dtypes)

#######Statistik#################

all_mean = meineDaten['Verbrauch (kWh)'].mean()
all_max = meineDaten['Verbrauch (kWh)'].max()
all_min = meineDaten['Verbrauch (kWh)'].min()
groupby_mean = meineDaten.groupby(['Ladepunkt']).mean()
groupby_max = meineDaten.groupby(['Ladepunkt']).max()
groupby_min = meineDaten.groupby(['Ladepunkt']).min()
groupby_month_mean = meineDaten.groupby(pd.Grouper(key='Gestartet',freq='Y')).sum()
groupby_month_max = meineDaten.groupby(pd.Grouper(key='Gestartet',freq='M')).max()
groupby_month_min = meineDaten.groupby(pd.Grouper(key='Gestartet',freq='M')).min()


print("\nGeringster Verbrauch aller Zeiten, aller Säulen:\n",all_min, "kWh")
print("\nHöchster Verbrauch aller Zeiten, aller Säulen:\n",all_max, "kWh")
print("\nMittlerer Verbrauch aller Säulen in der gesamten Zeit:\n",all_mean, "kWh")
print("\nHöchster Verbrauch aller Zeiten pro Säule:\n",groupby_max['Verbrauch (kWh)'])
print("\nGeringster Verbrauch aller Zeiten pro Säule:\n",groupby_min['Verbrauch (kWh)'])
print("\nMittlerer Verbrauch pro Säule in der Gesamtzeit:\n",groupby_mean['Verbrauch (kWh)'])
print("\nMonatlicher Mittelwert:",groupby_month_mean['Verbrauch (kWh)'])
print("\nMonatlicher Maximalwert:",groupby_month_max['Verbrauch (kWh)'])
print("\nMonatlicher Mindestwert:",groupby_month_min['Verbrauch (kWh)'])


#sns.set_theme(style="whitegrid")
#sns.histplot(groupby_mean, x="Ladepunkt",y="Verbrauch (kWh)")
#plt.show()