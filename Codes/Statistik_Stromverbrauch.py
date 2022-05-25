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

#all_mean = meineDaten['Verbrauch (kWh)'].mean()
#all_max = meineDaten['Verbrauch (kWh)'].max()
#all_min = meineDaten['Verbrauch (kWh)'].min()
#groupby_mean = meineDaten.groupby(['Ladepunkt']).mean()
#groupby_max = meineDaten.groupby(['Ladepunkt']).max()
#groupby_min = meineDaten.groupby(['Ladepunkt']).min()
#groupby_month_mean = meineDaten.groupby(pd.Grouper(key='Gestartet',freq='M')).mean()
#groupby_month_max = meineDaten.groupby(pd.Grouper(key='Gestartet',freq='M')).max()
#groupby_month_min = meineDaten.groupby(pd.Grouper(key='Gestartet',freq='M')).min()

#print("\nGeringster Verbrauch aller Säulen in der gesamten Zeit:\n",all_min, "kWh")
#print("\nHöchster Verbrauch aller Säulen in der gesamten Zeit:\n",all_max, "kWh")
#print("\nMittlerer Verbrauch aller Säulen in der gesamten Zeit:\n",all_mean, "kWh")
#print("\nHöchster Verbrauch pro Säule in der gesamten Zeit:\n",groupby_max['Verbrauch (kWh)'])
#print("\nGeringster Verbrauch pro Säule in der gesamten Zeit:\n",groupby_min['Verbrauch (kWh)'])
#print("\nMittlerer Verbrauch pro Säule in der gesamten Zeit:\n",groupby_mean['Verbrauch (kWh)'])

#print("\nMonatlicher Mindestwert:\n",groupby_month_min['Verbrauch (kWh)'])
#print("\nMonatlicher Maximalwert:\n",groupby_month_max['Verbrauch (kWh)'])
#print("\nMonatlicher Mittelwert:\n",groupby_month_mean['Verbrauch (kWh)']) 

ladepunkt_zeit_verbrauch = pd.DataFrame(
    {
        "Ladepunkt": meineDaten["Ladepunkt"],
        "Zeit": meineDaten["Gestartet"],
        "Verbrauch": meineDaten["Verbrauch (kWh)"],
        "Monat_Jahr": meineDaten["Gestartet"].dt.to_period('M'),
        "Jahr": meineDaten["Gestartet"].dt.year
    }
)
WF_H_1 = ladepunkt_zeit_verbrauch[ladepunkt_zeit_verbrauch['Ladepunkt']=='WF Gebäude H 1']
print("WF_H_1:",WF_H_1)
##WF_H_1_groupby_month_sum = WF_H_1.groupby(pd.Grouper(key='Uhrzeit',freq='D')).sum()
#print(WF_H_1_groupby_month_max)
##sns.lineplot(data=WF_H_1_groupby_month_sum x="Uhrzeit", y="Verbrauch")
#plt.xlabel("Datum")
#plt.xticks(rotation = 25)


WF_H_1 = ladepunkt_zeit_verbrauch[ladepunkt_zeit_verbrauch['Ladepunkt']=='WF Gebäude H 1']
WF_H_1_groupby_month_sum = WF_H_1.groupby(pd.Grouper(key='Zeit',freq='D')).sum()
WF_H_2 = ladepunkt_zeit_verbrauch[ladepunkt_zeit_verbrauch['Ladepunkt']=='WF Gebäude H 2']
WF_H_2_groupby_month_sum = WF_H_2.groupby(pd.Grouper(key='Zeit',freq='D')).sum()
WF_H_3 = ladepunkt_zeit_verbrauch[ladepunkt_zeit_verbrauch['Ladepunkt']=='WF Gebäude H 3']
WF_H_3_groupby_month_sum = WF_H_3.groupby(pd.Grouper(key='Zeit',freq='D')).sum()
WF_H_4 = ladepunkt_zeit_verbrauch[ladepunkt_zeit_verbrauch['Ladepunkt']=='WF Gebäude H 4']
WF_H_4_groupby_month_sum = WF_H_4.groupby(pd.Grouper(key='Zeit',freq='D')).sum()


# create the time series subplots
fig,ax =  plt.subplots( 2, 2, figsize = ( 10, 8))

sns.lineplot( x = "Zeit", y = "Verbrauch", 
             color = 'r', data = WF_H_1_groupby_month_sum , 
             ax = ax[0][0])
ax[0][0].tick_params(labelrotation = 25)
sns.lineplot( x = "Zeit", y = "Verbrauch", 
             color = 'g', data = WF_H_2_groupby_month_sum,
             ax = ax[0][1])
ax[0][1].tick_params(labelrotation = 25)
sns.lineplot(x = "Zeit", y = "Verbrauch", 
             color = 'b', data = WF_H_3_groupby_month_sum,
             ax = ax[1][0])
ax[1][0].tick_params(labelrotation = 25)
  
sns.lineplot(x = "Zeit", y = "Verbrauch", 
             color = 'y', data = WF_H_4_groupby_month_sum, 
             ax = ax[1][1])
ax[1][1].tick_params(labelrotation = 25)
fig.tight_layout(pad = 1.2)


#sns.lineplot(data=ladepunkt_zeit_verbrauch, x="Monat_Jahr", y="Verbrauch", hue="Ladepunkt")
  
  #df['month_year'] = df['date_column'].dt.to_period('M')

# applying the groupby function on df
#test.sort_values(by=['Ladepunkt','Uhrzeit'], inplace=True)

#print (test)
