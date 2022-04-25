import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

##df, weil "meineDaten" zu lang ist :D
#meineDaten= pd.read_csv("Alle-ladevorgänge-2022-03-16.csv", sep=";",encoding='latin-1',decimal=",", parse_dates=date_cols)

class plotten():
    '''
    Diese Klasse soll auf Basis einer Tabelle Graphen plotten.
    '''
    def __init__(self, daten, name, jahr, monat, woche):
        self.daten = daten
        self.name = name
        self.jahr = jahr
        self.monat = monat
        self.woche = woche
    def ausgeben(self):
        plt.figure()
        df[df[column=0].dt.strftime('%Y-%m-%d') == self.jahr + '-' + self.monat]
        sns.lineplot(data = self.daten, label =self.name)
        plt.xticks(rotation = 25)
        
df= pd.read_csv("Alle-ladevorgänge-2022-03-16.csv", sep=";",encoding='latin-1',decimal=",")
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E740796*001'],'Salzgitter 1')
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E740796*002'],'Salzgitter 2')
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E740796*003'],'Salzgitter 3')
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E740796*004'],'Salzgitter 4')

df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E809189*001'],'WF Recht 1')
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E809189*002'],'WF Recht 2')

df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*EMLP1'],'WF Gebäude H 1') #EMLP
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*EMLP2'],'WF Gebäude H 2')

df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*ESLP1'],'WF Gebäude H 3') #ESLP2
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*ESLP2'],'WF Gebäude H 4')
df.rename(columns={'Monat (MM/JJJJ)': 'Date'}, inplace=True) #Date weil auch hier zu lang :D

####Leere Spalten löschen
df.drop('Stop-Grund', inplace=True, axis=1)
df.drop('Grund für die Auffälligkeit', inplace=True, axis=1)
df.drop('Kosten', inplace=True, axis=1)
df.drop('Provider', inplace=True, axis=1)
df.drop('Operator', inplace=True, axis=1)

df["Date"] = pd.to_datetime(df["Date"]) #Wandelt Date in eine Zeit um

df.set_index("Date", inplace = True)
print(df)
tagesverbrauch = df["Verbrauch (kWh)"].resample("D").sum() #Gibt den Tagesverbrauch aus
print("\nTagersverbrauch:\n",tagesverbrauch)

wochenverbrauch = df["Verbrauch (kWh)"].resample("W").sum() #Gibt den Wochenverbrauch aus
print("\nWochenverbauch:\n",wochenverbrauch)

#%matplotlib inline
gesamtzeit_tagesverbrauch = plotten(tagesverbrauch,"Täglicher Gesamtverbrauch",2020,10,0)
gesamtzeit_tagesverbrauch.ausgeben()

gesamtzeit_wochenverbrauch = plotten(wochenverbrauch,"Wöchentlicher Gesamtverbrauch",0,0,0)
gesamtzeit_wochenverbrauch.ausgeben()


#df["Tagesverbrauch"]= df["Verbrauch (kWh)"].resample("D").sum() Funktioniert noch nicht
#df["Wochenverbrauch"]=df["Verbrauch (kWh)"].resample("W").sum() Funktioniert noch nicht