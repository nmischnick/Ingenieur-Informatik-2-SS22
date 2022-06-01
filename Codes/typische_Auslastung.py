# -*- coding: utf-8 -*-
"""
Created May 2022

@author: Luis Klimpke
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


# -------------------- Lesen der csv-Datei
df = pd.read_csv('Alle-ladevorgänge-2022-03-16.csv', sep=';', encoding='latin-1')


# -------------------- Umwandeln der Zeitpunkte in datetime Format
df['Gestartet'] = pd.to_datetime(df['Gestartet'], format="%d.%m.%Y %H:%M")
df['Beendet'] = pd.to_datetime(df['Beendet'], format="%d.%m.%Y %H:%M")


# -------------------- Für mich nicht nötige Spalten löschen
df.drop(['Monat (MM/JJJJ)','Stop-Grund', 'Standzeit', 'Zählerstand Start (kWh', 'Zählerstand Ende (kWh)', 'Vertrag', 'Verbrauch (kWh)', 'Grund für die Auffälligkeit', 'Kosten', 'Provider', 'Operator'], axis=1, inplace=True)
    

# -------------------- Benenne Spalten um, um besser damit arbeiten zu können
df.rename(columns={'Gestartet':'start','Beendet':'stop'}, inplace=True)


# -------------------- Löschen der Daten, bei denen der stop vor dem start ist
df = df.loc[~(df['start'] > df['stop'])]


# -------------------- bekomme Array aller Ladepunkte
ladepunkte = df['Ladepunkt'].unique()



# -------------------- Bekomme Werte für einen gegebenen Ladepunkt
def get_one(ladepunkt):
    biggerstop = pd.DataFrame()                             #DataFrame für die Werte, welche später größer als der Stopzeitpunkt sind
    new_data = pd.DataFrame()                               #Ausgewertete Werte
    
    print('Calculating Data For: ', ladepunkt)
    
    if ladepunkt == 'all':
        df_lp = df
    else:
        df_lp = df[df['Ladepunkt'] == ladepunkt]                #aus DataFrame nur Werte der gegebenen Ladesäule
    
    print('Anzahl Ladevorgänge: ', len(df_lp))              #Ausgabe Anzahl Ladevorgänge, da bei wenigen Ladevorgängen Diagramm nicht wirklich sinnvoll ist

    #print(df_lp)

    df_lp['nextfullhour'] = df_lp['start'].dt.ceil('h')     #auf nächste volle Stunde setzten. 'h' = hour
    
    while(not df_lp.empty):                                 #solange bis dataframe leer ist, geleert wird indem Werte welche im Laufe größer sind als die Stopzeit herausgelöscht werden und in biggerstop gespeichert werden
        
                                                            # Wenn stop kleiner ist als die Zeit, die zuvor auf die nächste volle Stunde gesetzt wurde dem DataFrame biggerstop hinzufügen und aus dem DataFrame löschen
        biggerthanstop = (df_lp['nextfullhour'] > df_lp['stop'])        #Füge alle Werte hinzu vobei der Stop kleier ist als die nächste-volle-Stunde
        biggerstop = biggerstop.append(df_lp.loc[biggerthanstop])       #Hänge eben herausgesuchten Werte an neuen DataFrame an
        df_lp = df_lp.loc[~biggerthanstop]                              #Lösche die eben herausgesuchten Werte aus dem DataFrame mit restlichen Werten

        #nextfullhour ist nun überall kleiner als stop
    
        df_lp['difftest'] = df_lp['nextfullhour']-df_lp['start']        #Differenz vom start bis zur nächsten vollen Stunde
        df_lp['hour'] = df_lp['nextfullhour'].dt.hour - 1               #Die Stunde zu der die zuvor berechnete Differenz gehört (also wenn von 12-13uhr komplett durchgeladen wurde zählt diese Stunde Ladezeit zu 12uhr)
        
        new_data = new_data.append(df_lp.groupby(df_lp['hour'])['difftest'].sum().to_frame()) #summiere alle Differenzen für jede Stunde und füge diese new_data hinzu
        
        df_lp['start'] = df_lp['nextfullhour']                          #setzte nun die nextfullhour als start, damit geloopt werden kann
        
        df_lp['nextfullhour'] = df_lp['nextfullhour'] + datetime.timedelta(hours=1) #setzte nextfullhour auf die folgende Stunde (auch für loop benötigt)
        
    
    #while loop fertig (alle Ladevorgänge haben den Stop einmal überschritten(gleiche Anzahl Einträge wie vor while loop))
    #aus biggerstop müssen jetzt noch die Differenzen zwischenn dem stop und der angefangenen Stunde berechnet werden
    
    biggerstop['difftest'] = biggerstop['stop']-biggerstop['start'] #start ist ja eine Stude vor der nextfullhour(welche nun schon über stop hinaus ist), deswegen kann hiermit also die Differenz berechnet werden
    biggerstop['hour'] = (biggerstop['nextfullhour'] - datetime.timedelta(hours=1)).dt.hour

    
    new_data = new_data.append(biggerstop.groupby(biggerstop['hour'])['difftest'].sum().to_frame()) #beinhaltet einen Stundenindex und einen Zeitwert, jedoch sind manche Stunden mehrmals vorhanden, aufgrund von verschiedenen durchläufen der while-Schleife. hier werden biggerstop werte zu den anderen hinzugefügt
    
    # -------------------- Nun werden die Zeitwerte noch nach Stunde gegroupt
    final_data = new_data.groupby(level=0)['difftest'].sum().to_frame()

    
    # -------------------- Stunden reichen von einschließlich -1 bis einschließlich 23, wobei -1 das gleiche wie 23 ist. Dies passiert, wenn ein Auto über mehere Tage angeschlossen ist und somit z.B. von 23uhr bis 2uhr dort steht
    final_data.rename(index={-1:23}, inplace=True)
    final_data = final_data.groupby(level=0)['difftest'].sum().to_frame()
    final_data

    
    # -------------------- Nun werden die werte noch durch die gesamte Standzeit geteilt, um einen Prozentualen anteil zu bekommen
    final_data.sum()
    final_data = final_data / final_data.sum()

    return final_data

# -------------------- gibt alle Diagramme zu allen Ladepunkten aus
def plot_all():
    for i in ladepunkte:
        
        data = get_one(i)
        
        #print(data)
    
        fig, ax = plt.subplots(figsize = (20, 7))
    
        sns.despine(bottom = True, left = True)
        sns.barplot(ax=ax, x=data.index, y='difftest', data=data, errwidth=0, ci=None).set_title(i)


# -------------------- gibt Diagramm zu einem Ladepunkt aus
def plot_one(ladepunkt):
    data = get_one(ladepunkt)
    
    #print(data)

    fig, ax = plt.subplots(figsize = (20, 7))

    sns.despine(bottom = True, left = True)
    sns.barplot(ax=ax, x=data.index, y='difftest', data=data, errwidth=0).set_title(ladepunkt)
    
plot_one('all')



