# -*- coding: utf-8 -*-
"""
Created on Mon May  2 19:01:51 2022

@author: Luis
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
#from Standorte_hinzufuegen import addStandort


WF = ['DE*cem*E740796*001','DE*cem*E740796*002','DE*cem*E740796*003','DE*cem*E740796*004']
KA = ['DE*cem*E809189*001','DE*cem*E809189*002']
SZ = ['DE*cem*ESLP1','DE*cem*ESLP2','DE*cem*EMLP1','DE*cem*EMLP2']

def addStandort (df):



    def lp_to_so(row):
        if row['Ladepunkt'] in WF:
            return 'WF'
        if row['Ladepunkt'] in SZ:
            return 'SZ'
        if row['Ladepunkt'] in KA:
            return 'KA'


        
    df['Standort'] = df.apply (lambda row: lp_to_so(row), axis=1)               #für jede Zeile
    
    return df


df = pd.read_csv('Alle-ladevorgänge-2022-03-16.csv', sep=';', encoding='latin-1', decimal=",")

#Standorte zu jedem Ladepunkt hinzufügen
df = addStandort(df)

#löschen hierfür unnützer Columns
df.drop(['Gestartet','Beendet', 'Monat (MM/JJJJ)','Stop-Grund', 'Standzeit', 'Zählerstand Start (kWh', 'Zählerstand Ende (kWh)', 'Vertrag', 'Grund für die Auffälligkeit', 'Kosten', 'Provider', 'Operator'], axis=1, inplace=True)


#groupen nach Ladepunkt+Standort
df = df.groupby(['Ladepunkt','Standort'])['Verbrauch (kWh)'].sum().to_frame()



df = df.reset_index() #um Index als Column zu bekommen


### Anzeigen der Daten mithilfe von Seaborn
g = sns.catplot(kind='bar', data=df, col='Standort', x='Ladepunkt', y='Verbrauch (kWh)', palette='rocket', dodge=False, sharex=False) #col= für die verschiedenen Gruppen(hier Standorte), x= für die Einzelnen Rows, y= fpr die Werte
plt.tight_layout()
plt.show()
###