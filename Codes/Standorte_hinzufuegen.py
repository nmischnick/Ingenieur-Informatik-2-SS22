# -*- coding: utf-8 -*-
"""
Created on Mon May  2 19:05:09 2022

@author: Luis
"""


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


        
    df['Standort'] = df.apply (lambda row: lp_to_so(row), axis=1)
    
    return df
    