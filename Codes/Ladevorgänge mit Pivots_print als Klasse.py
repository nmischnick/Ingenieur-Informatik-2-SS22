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
    def __init__(self, daten, name, start, ende):
        self.daten = daten
        self.name = name
        self.start = start
        self.ende = ende
        
    def gesamtverbrauch_tag(self):
        tagesverbrauch = self.daten["Verbrauch (kWh)"].resample("D").sum() #Gibt den Tagesverbrauch aus
        print("HIER GEHT DAS DATUM KAPUTT:", tagesverbrauch)
        plt.figure()
        sns.set_theme()
        tabelle = tagesverbrauch[self.start :self.ende]
        sns.lineplot(data = tabelle, label =self.name, marker = "o")
        plt.xticks(rotation = 25)
        
    def gesamtverbrauch_woche(self):
        wochenverbrauch = self.daten["Verbrauch (kWh)"].resample("W").sum() #Gibt den Wochenverbrauch aus
        plt.figure()
        sns.set_theme()
        tabelle = wochenverbrauch[self.start :self.ende]
        sns.lineplot(data = tabelle, label =self.name, marker = "o")
        plt.xticks(rotation = 25)
    
    def verbrauchstandorte(self):
        print(df)
        plt.figure()
        sns.set_theme()
        plt.xticks(rotation = 25)
        tabelle = self.daten[self.start :self.ende]
        gruppieren= tabelle.groupby(["Ladepunkt"])
        print("GRUPPIEREN",gruppieren)

        try:
            wfh =gruppieren.get_group("WF Gebäude H")
        except:
            print("Keine Daten H")
            
        try:
            salzgitter =gruppieren.get_group("Salzgitter")
        except:
            print("Keine Daten Salzgitter")
        try:
            wfr =gruppieren.get_group("WF Recht")
        except:
            print("Keine Daten Recht")
        try:
            wfh1 = wfh["Verbrauch (kWh)"].resample("W").sum()
        except:
            print("Keine Daten H")
            
        try:
            salzgitter1 = salzgitter["Verbrauch (kWh)"].resample("W").sum()
        except:
            print("Keine Daten Salzgitter")
        try:
            wfr1 = wfr["Verbrauch (kWh)"].resample("W").sum()
        except:
            print("Keine Daten Recht")

        try:
            sns.lineplot(data = salzgitter1,label = "WF Recht", marker = "o")
        except:
            print("Salzgitter: Keine Daten")
        try:
             sns.lineplot(data = wfh1,label = "Salzgitter", marker = "o")
        except:
            print("WF Gebäude H: Keine Daten")
        try:
            sns.lineplot(data = wfr1,label = "WF Gebäude H", marker = "o")
        except:
            print("WF Recht: Keine Daten")
        
        plt.xlabel("Datum")
        
        
df= pd.read_csv("Alle-ladevorgänge-2022-03-16.csv", sep=";",encoding='latin-1',decimal=",")
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E740796*001'],'Salzgitter')
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E740796*002'],'Salzgitter')
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E740796*003'],'Salzgitter')
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E740796*004'],'Salzgitter')

df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E809189*001'],'WF Recht')
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*E809189*002'],'WF Recht')

df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*EMLP1'],'WF Gebäude H') #EMLP
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*EMLP2'],'WF Gebäude H')

df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*ESLP1'],'WF Gebäude H') #ESLP2
df['Ladepunkt'] = df['Ladepunkt'].replace(['DE*cem*ESLP2'],'WF Gebäude H')
df.rename(columns={'Monat (MM/JJJJ)': 'Date'}, inplace=True) #Date weil auch hier zu lang :D

####Leere Spalten löschen
df.drop('Stop-Grund', inplace=True, axis=1)
df.drop('Grund für die Auffälligkeit', inplace=True, axis=1)
df.drop('Kosten', inplace=True, axis=1)
df.drop('Provider', inplace=True, axis=1)
df.drop('Operator', inplace=True, axis=1)

df["Date"] = pd.to_datetime(df["Date"]) #Wandelt Date in eine Zeit um

df.set_index("Date", inplace = True)
print("HIER IST ES NOCH IN ORDNUNG:",df)


gesamtzeit_tagesverbrauch = plotten(df,"Täglicher Gesamtverbrauch","2021-01-10","2021-01-17")
gesamtzeit_tagesverbrauch.gesamtverbrauch_tag()

gesamtzeit_wochenverbrauch = plotten(df,"Wöchentlicher Gesamtverbrauch","2021-01-01","2021-02-01")
gesamtzeit_wochenverbrauch.gesamtverbrauch_woche()

standorte_wochenverbrauch = plotten(df,"Wöchentlicher Verbrauch nach Standort", "2020-06-01","2024-01-01")
standorte_wochenverbrauch.verbrauchstandorte()